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

    # Database (optional -- engine works without PostgreSQL)
    db_url: str | None = None  # e.g. "postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2"
    db_enabled: bool = False


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

        # Alert engine
        from mpe.alerts import AlertEngine

        self._alert_engine = AlertEngine()
        self._pending_alert_cots: list[str] = []

        # CoT output (plain socket sender, wired in start())
        self._cot_output = None  # CoTOutput instance

        # Database (optional persistence layer)
        self._db = None  # Optional Database instance
        self._pending_db_ops: list = []  # Queue of async callables to run

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

        # Setup optional database persistence
        if self._config.db_url:
            try:
                from mpe.db.engine import Database

                self._db = Database(self._config.db_url)
                await self._db.connect()
                await self._db.create_tables()
                self._config.db_enabled = True
                logger.info(
                    "Database connected: %s",
                    self._config.db_url.split("@")[-1],
                )
            except Exception as exc:
                logger.warning(
                    "Database unavailable, running in-memory only: %s", exc,
                )
                self._db = None
                self._config.db_enabled = False

        # Setup CoT output (plain socket sender -- no PyTAK dependency)
        if self._config.cot_enabled:
            try:
                from mpe.cot_output import CoTOutput

                self._cot_output = CoTOutput(self._config.cot_url)
                self._cot_output.connect()
                logger.info("CoT output: %s", self._config.cot_url)
            except Exception as exc:
                logger.warning("CoT output disabled: %s", exc)
                self._cot_output = None

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
                    await self._flush_db_ops()
                    last_classify = now

                # Output CoT
                if now - last_output >= self._config.output_interval_s:
                    self._output_cot()
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

        # Disconnect CoT output
        if self._cot_output:
            self._cot_output.disconnect()

        # Flush remaining DB operations and disconnect
        if self._db:
            await self._flush_db_ops()
            await self._db.disconnect()
            logger.info("Database disconnected")

        logger.info("Engine stopped.")

    # -- database persistence -----------------------------------------------

    async def _flush_db_ops(self) -> None:
        """Execute pending database operations in a single transaction."""
        if not self._db or not self._pending_db_ops:
            return
        ops = self._pending_db_ops[:]
        self._pending_db_ops.clear()
        try:
            async with self._db.session() as session:
                for op in ops:
                    try:
                        await op(session)
                    except Exception as exc:
                        logger.error("DB operation failed: %s", exc)
                await session.commit()
        except Exception as exc:
            logger.error("DB flush failed: %s", exc)

    def _queue_track_persist(
        self, entity_id: str, domain: str, track: object,
    ) -> None:
        """Queue a track position write for the next DB flush."""
        lat = getattr(track, "latitude", 0.0)
        lon = getattr(track, "longitude", 0.0)
        alt = getattr(track, "altitude_baro_ft", None) or getattr(
            track, "altitude_m", 0.0,
        )
        heading = getattr(track, "heading", 0.0) or getattr(
            track, "course_over_ground", 0.0,
        ) or 0.0
        speed = getattr(track, "ground_speed_kts", None) or getattr(
            track, "speed_over_ground", 0.0,
        ) or 0.0
        source = "adsb" if domain == "air" else "ais"

        async def persist_track(
            session,
            eid=entity_id,
            _lat=lat,
            _lon=lon,
            _alt=alt,
            _heading=heading,
            _speed=speed,
            _source=source,
        ):
            from mpe.db.repository import TrackRepository

            repo = TrackRepository(session)
            await repo.record_update(
                eid,
                source=_source,
                lat=_lat,
                lon=_lon,
                alt=_alt,
                heading=_heading,
                speed_mps=_speed,
            )

        self._pending_db_ops.append(persist_track)

    def _queue_classification_persist(
        self, entity_id: str, domain: str, cls: object,
    ) -> None:
        """Queue a classification write for the next DB flush."""

        async def persist_cls(session, eid=entity_id, d=domain, c=cls):
            from mpe.db.models import Classification as DBClassification
            from mpe.db.repository import EntityRepository

            # Upsert entity with latest classification
            entity_repo = EntityRepository(session)
            await entity_repo.upsert(
                eid,
                domain=d,
                affiliation=c.affiliation,
                threat_level=c.threat_level,
                threat_category=c.threat_category,
                confidence=c.confidence,
            )

            # Record classification history
            db_cls = DBClassification(
                entity_id=eid,
                affiliation=c.affiliation,
                threat_level=c.threat_level,
                threat_category=c.threat_category,
                confidence=c.confidence,
                reasoning=[str(r) for r in c.reasoning],
                anomalies=[
                    {"type": a.anomaly_type, "description": a.description}
                    for a in c.anomalies
                ],
            )
            session.add(db_cls)

        self._pending_db_ops.append(persist_cls)

    def _queue_alert_persist(
        self, entity_id: str, cls: object,
    ) -> None:
        """Queue an alert + audit log write for the next DB flush."""

        async def persist_alert(session, eid=entity_id, c=cls):
            from mpe.db.repository import AlertRepository, AuditRepository

            alert_repo = AlertRepository(session)
            await alert_repo.create_alert(
                entity_id=eid,
                alert_type="threat",
                severity=c.threat_level,
                title=f"High threat: {eid}",
                description="; ".join(str(r) for r in c.reasoning),
            )

            audit_repo = AuditRepository(session)
            await audit_repo.log(
                action="alert_generated",
                target_type="entity",
                target_id=eid,
                details={
                    "threat_level": c.threat_level,
                    "reasoning": [str(r) for r in c.reasoning],
                },
            )

        self._pending_db_ops.append(persist_alert)

    # -- periodic tasks -----------------------------------------------------

    def _classify_all(self) -> None:
        """Run classifier on all active tracks."""
        count = 0

        for track in self._aircraft_tracker.active_tracks:
            cls = self._classifier.classify_aircraft(track)
            # Store classification result on the track object for CoT output
            track._classification = cls  # noqa: SLF001
            count += 1

            entity_id = f"ADSB-{track.icao_hex}"

            # Queue DB persistence (no-op if DB not configured)
            if self._db:
                self._queue_track_persist(entity_id, "air", track)
                self._queue_classification_persist(entity_id, "air", cls)

            # Evaluate alert rules
            alerts = self._alert_engine.evaluate(
                entity_id=entity_id,
                classification=cls,
                domain="air",
                latitude=track.latitude,
                longitude=track.longitude,
                callsign=track.callsign or track.icao_hex,
            )
            for alert in alerts:
                self._pending_alert_cots.append(alert.cot_xml)
                self._stats["alerts_generated"] = (
                    int(self._stats.get("alerts_generated", 0)) + 1
                )
                if self._db:
                    self._queue_alert_persist(entity_id, cls)

            # Legacy high-threat logging (kept for backwards compatibility)
            if cls.threat_level >= 7:
                logger.warning(
                    "HIGH THREAT: %s threat=%d %s reason=%s",
                    track.callsign or track.icao_hex,
                    cls.threat_level,
                    cls.threat_category,
                    cls.reasoning,
                )

        for track in self._vessel_tracker.active_tracks:
            cls = self._classifier.classify_vessel(track)
            track._classification = cls  # noqa: SLF001
            count += 1

            entity_id = f"AIS-{track.mmsi}"

            # Queue DB persistence (no-op if DB not configured)
            if self._db:
                self._queue_track_persist(entity_id, "sea", track)
                self._queue_classification_persist(entity_id, "sea", cls)

            # Evaluate alert rules
            alerts = self._alert_engine.evaluate(
                entity_id=entity_id,
                classification=cls,
                domain="sea",
                latitude=track.latitude,
                longitude=track.longitude,
                callsign=track.vessel_name or str(track.mmsi),
            )
            for alert in alerts:
                self._pending_alert_cots.append(alert.cot_xml)
                self._stats["alerts_generated"] = (
                    int(self._stats.get("alerts_generated", 0)) + 1
                )
                if self._db:
                    self._queue_alert_persist(entity_id, cls)

            if cls.threat_level >= 7:
                logger.warning(
                    "HIGH THREAT: %s threat=%d %s reason=%s",
                    track.vessel_name or track.mmsi,
                    cls.threat_level,
                    cls.threat_category,
                    cls.reasoning,
                )

        self._stats["classifications_run"] = (
            int(self._stats.get("classifications_run", 0)) + count
        )

    def _output_cot(self) -> None:
        """Generate and send CoT events for all active tracks."""
        if not self._cot_output:
            return

        events: list[str] = []

        # Aircraft -> CoT
        events.extend(
            self._adsb_bridge.tracks_to_cot(
                self._aircraft_tracker.active_tracks,
            ),
        )

        # Vessels -> CoT
        events.extend(
            self._ais_bridge.tracks_to_cot(
                self._vessel_tracker.active_tracks,
            ),
        )

        # Pending alerts -> CoT
        events.extend(self._pending_alert_cots)
        self._pending_alert_cots.clear()

        sent = self._cot_output.send_batch(events)
        self._stats["cot_events_sent"] = (
            int(self._stats.get("cot_events_sent", 0)) + sent
        )

        if sent > 0:
            logger.debug(
                "Sent %d/%d CoT events to %s",
                sent,
                len(events),
                self._config.cot_url,
            )

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
