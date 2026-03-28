"""MPE Core Engine -- headless C2 intelligence daemon.

This is the product. It ingests multi-domain sensor data, classifies
entities, detects anomalies, and outputs enriched CoT events to TAK
networks. Operators use ATAK as their interface.

Usage:
    python -m mpe --config engine.toml

Or programmatically:
    engine = CoreEngine(config)
    await engine.start()
"""

from __future__ import annotations

import asyncio
import logging
import signal
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol

logger = logging.getLogger("mpe.engine")


@dataclass
class EngineConfig:
    """Configuration for the core engine."""

    # ADS-B
    adsb_enabled: bool = True
    adsb_source: str = "airplanes_live"
    adsb_center_lat: float = 51.3632
    adsb_center_lon: float = -0.2652
    adsb_radius_nm: int = 250
    adsb_poll_interval_s: float = 10.0

    # AIS
    ais_enabled: bool = False  # Needs hardware
    ais_udp_port: int = 5050

    # CoT Output
    cot_enabled: bool = True
    cot_url: str = "udp+wo://239.2.3.1:6969"
    cot_callsign: str = "MPE-ENGINE"
    cot_stale_seconds: int = 120

    # Classifier
    known_friendly_mmsis: set[int] = field(default_factory=set)
    known_hostile_mmsis: set[int] = field(default_factory=set)
    known_friendly_icaos: set[str] = field(default_factory=set)

    # Engine
    classify_interval_s: float = 5.0
    output_interval_s: float = 5.0
    purge_interval_s: float = 60.0
    log_level: str = "INFO"


class IngestSource(Protocol):
    """Protocol for data ingest sources."""

    def start(self) -> None: ...
    def stop(self) -> None: ...


class CoreEngine:
    """The central intelligence engine.

    Lifecycle: init -> start -> [running] -> stop

    While running, it:
    1. Ingests data from all enabled sources (background threads)
    2. Periodically classifies all active tracks
    3. Periodically outputs enriched CoT events to TAK
    4. Purges stale tracks
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        self._config = config or EngineConfig()
        self._running = False
        self._sources: list[IngestSource] = []

        # Trackers (in-memory, will add DB persistence later)
        from mpe.aircraft_tracker import AircraftTracker
        from mpe.vessel_tracker import VesselTracker

        self._aircraft_tracker = AircraftTracker()
        self._vessel_tracker = VesselTracker()

        # Classifier
        from mpe.classifier import EntityClassifier

        self._classifier = EntityClassifier(
            known_friendly_mmsis=self._config.known_friendly_mmsis,
            known_hostile_mmsis=self._config.known_hostile_mmsis,
            known_friendly_icaos=self._config.known_friendly_icaos,
        )

        # CoT bridges
        from mpe.adsb_cot_bridge import ADSBCoTBridge
        from mpe.ais_cot_bridge import AISCoTBridge

        self._adsb_bridge = ADSBCoTBridge(
            stale_seconds=self._config.cot_stale_seconds,
        )
        self._ais_bridge = AISCoTBridge(
            stale_seconds=self._config.cot_stale_seconds,
        )

        # Stats
        self._stats: dict[str, object] = {
            "aircraft_tracked": 0,
            "vessels_tracked": 0,
            "cot_events_sent": 0,
            "classifications_run": 0,
            "alerts_generated": 0,
            "uptime_start": None,
        }

        logging.basicConfig(
            level=getattr(logging, self._config.log_level),
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

    # -- properties ---------------------------------------------------------

    @property
    def aircraft_tracker(self):
        """Expose aircraft tracker for testing and external access."""
        return self._aircraft_tracker

    @property
    def vessel_tracker(self):
        """Expose vessel tracker for testing and external access."""
        return self._vessel_tracker

    @property
    def stats(self) -> dict[str, object]:
        """Current engine statistics snapshot."""
        return dict(self._stats)

    @property
    def running(self) -> bool:
        """Whether the engine is currently running."""
        return self._running

    # -- source setup -------------------------------------------------------

    def _setup_sources(self) -> None:
        """Initialize all enabled ingest sources."""
        if self._config.adsb_enabled:
            from mpe.adsb_receiver import ADSBReceiver

            receiver = ADSBReceiver(
                self._aircraft_tracker,
                center_lat=self._config.adsb_center_lat,
                center_lon=self._config.adsb_center_lon,
                radius_nm=self._config.adsb_radius_nm,
                poll_interval_s=self._config.adsb_poll_interval_s,
                source=self._config.adsb_source,
            )
            self._sources.append(receiver)
            logger.info("ADS-B source enabled: %s", self._config.adsb_source)

        if self._config.ais_enabled:
            from mpe.ais_receiver import AISReceiver

            receiver = AISReceiver(
                self._vessel_tracker,
                port=self._config.ais_udp_port,
            )
            self._sources.append(receiver)
            logger.info("AIS source enabled: UDP port %d", self._config.ais_udp_port)

    # -- lifecycle ----------------------------------------------------------

    async def start(self) -> None:
        """Start the engine. Blocks until stopped."""
        logger.info("MPE Core Engine starting...")
        self._running = True
        self._stats["uptime_start"] = datetime.now(timezone.utc)

        # Setup ingest sources
        self._setup_sources()

        # Start all ingest sources (they run in background threads)
        for source in self._sources:
            if hasattr(source, "start_polling"):
                source.start_polling()
            elif hasattr(source, "start_udp"):
                source.start_udp()
            else:
                source.start()

        logger.info("Started %d ingest source(s)", len(self._sources))

        # Setup CoT output
        cot_sender = None
        if self._config.cot_enabled:
            try:
                from mpe.cot_sender import CoTStreamer

                cot_sender = CoTStreamer(
                    cot_url=self._config.cot_url,
                    callsign=self._config.cot_callsign,
                )
                logger.info("CoT output enabled: %s", self._config.cot_url)
            except Exception as exc:
                logger.warning("CoT output disabled: %s", exc)

        # Main loop
        logger.info("Engine running. Press Ctrl+C to stop.")
        last_classify = 0.0
        last_output = 0.0
        last_purge = 0.0

        try:
            while self._running:
                now = time.monotonic()

                # Classify
                if now - last_classify >= self._config.classify_interval_s:
                    self._classify_all()
                    last_classify = now

                # Output CoT
                if now - last_output >= self._config.output_interval_s:
                    if cot_sender is not None:
                        self._output_cot(cot_sender)
                    last_output = now

                # Purge stale
                if now - last_purge >= self._config.purge_interval_s:
                    self._purge_stale()
                    last_purge = now

                # Update stats
                self._stats["aircraft_tracked"] = len(
                    self._aircraft_tracker.active_tracks,
                )
                self._stats["vessels_tracked"] = len(
                    self._vessel_tracker.active_tracks,
                )

                await asyncio.sleep(1.0)

        except asyncio.CancelledError:
            pass
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop the engine gracefully."""
        if not self._running:
            return
        logger.info("Engine stopping...")
        self._running = False
        for source in self._sources:
            source.stop()
        logger.info("Engine stopped.")

    # -- periodic tasks -----------------------------------------------------

    def _classify_all(self) -> None:
        """Run classifier on all active tracks."""
        count = 0

        for track in self._aircraft_tracker.active_tracks:
            cls = self._classifier.classify_aircraft(track)
            # Store classification result on the track object for CoT output
            track._classification = cls  # noqa: SLF001
            count += 1

            # Check for alerts
            if cls.threat_level >= 7:
                logger.warning(
                    "HIGH THREAT: %s threat=%d %s reason=%s",
                    track.callsign or track.icao_hex,
                    cls.threat_level,
                    cls.threat_category,
                    cls.reasoning,
                )
                self._stats["alerts_generated"] = (
                    int(self._stats.get("alerts_generated", 0)) + 1
                )

        for track in self._vessel_tracker.active_tracks:
            cls = self._classifier.classify_vessel(track)
            track._classification = cls  # noqa: SLF001
            count += 1

            if cls.threat_level >= 7:
                logger.warning(
                    "HIGH THREAT: %s threat=%d %s reason=%s",
                    track.vessel_name or track.mmsi,
                    cls.threat_level,
                    cls.threat_category,
                    cls.reasoning,
                )
                self._stats["alerts_generated"] = (
                    int(self._stats.get("alerts_generated", 0)) + 1
                )

        self._stats["classifications_run"] = (
            int(self._stats.get("classifications_run", 0)) + count
        )

    def _output_cot(self, cot_sender: object) -> None:
        """Generate and send CoT events for all active tracks."""
        count = 0

        # Aircraft -> CoT
        for _xml in self._adsb_bridge.tracks_to_cot(
            self._aircraft_tracker.active_tracks,
        ):
            try:
                # TODO: Send through cot_sender transport when wired up
                count += 1
            except Exception:
                logger.exception("Error sending aircraft CoT event")

        # Vessels -> CoT
        for _xml in self._ais_bridge.tracks_to_cot(
            self._vessel_tracker.active_tracks,
        ):
            try:
                count += 1
            except Exception:
                logger.exception("Error sending vessel CoT event")

        self._stats["cot_events_sent"] = (
            int(self._stats.get("cot_events_sent", 0)) + count
        )

        if count > 0:
            logger.debug("Output %d CoT events", count)

    def _purge_stale(self) -> None:
        """Remove stale tracks."""
        air_purged = self._aircraft_tracker.purge_stale()
        sea_purged = self._vessel_tracker.purge_stale()
        if air_purged or sea_purged:
            logger.info(
                "Purged %d aircraft + %d vessel stale tracks",
                air_purged,
                sea_purged,
            )


async def run_engine(config: EngineConfig | None = None) -> None:
    """Entry point for running the engine."""
    engine = CoreEngine(config)

    loop = asyncio.get_event_loop()

    def handle_signal() -> None:
        logger.info("Received shutdown signal")
        asyncio.ensure_future(engine.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handle_signal)

    await engine.start()
