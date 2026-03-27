"""Live CoT event sender -- streams drone position and mission data to TAK networks.

Uses PyTAK for async transport over UDP multicast, UDP unicast, or TCP to TAK Server.

Default endpoint: udp+wo://239.2.3.1:6969 (ATAK multicast, write-only)

PyTAK is an **optional** dependency. Import this module only when streaming is
needed; a missing ``pytak`` raises ``StreamError`` at construction time rather
than ``ImportError`` at import time.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from configparser import ConfigParser
from typing import TYPE_CHECKING

from mpe.cot_types import FRIENDLY_UAV_FIXEDWING
from mpe.models import MAVCmd, MissionItem
from mpe.writers.cot import CoTWriter

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default network configuration
# ---------------------------------------------------------------------------
DEFAULT_COT_URL = "udp+wo://239.2.3.1:6969"
DEFAULT_CALLSIGN = "MPE-DRONE"
DEFAULT_UID = "MPE-LIVE"
DEFAULT_INTERVAL = 5


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class StreamError(Exception):
    """Raised when CoT streaming fails or pytak is unavailable."""


# ---------------------------------------------------------------------------
# Lazy pytak import helper
# ---------------------------------------------------------------------------

def _require_pytak():
    """Return the ``pytak`` module or raise ``StreamError``."""
    try:
        import pytak  # noqa: F811
        return pytak
    except ImportError as exc:
        raise StreamError(
            "pytak is not installed. Run: pip install 'mission-planning-engine[tak]' "
            "or: pip install pytak"
        ) from exc


# ---------------------------------------------------------------------------
# PyTAK Queue Workers
# ---------------------------------------------------------------------------

class MissionPublisher:
    """One-shot publisher that puts all mission waypoints onto a TX queue.

    Not a ``pytak.QueueWorker`` subclass to avoid requiring pytak at import
    time. Instead, it duck-types the async ``run()`` protocol expected by
    ``CLITool.add_task``.
    """

    def __init__(
        self,
        tx_queue: asyncio.Queue,
        items: list[MissionItem],
        cot_writer: CoTWriter,
    ) -> None:
        self._tx_queue = tx_queue
        self._items = items
        self._writer = cot_writer

    async def run(self, _=-1) -> None:
        """Generate CoT XML for every mission item and enqueue."""
        events = self._writer.mission_to_events(self._items)
        for event_xml in events:
            await self._tx_queue.put(event_xml.encode("utf-8"))
            await asyncio.sleep(0.1)  # avoid flooding the network
        logger.info("Published %d mission waypoints as CoT events", len(events))


class PositionReporter:
    """Continuous position broadcaster -- sends drone position CoT at a fixed interval.

    Position can be updated externally via ``update_position()``.  The reporter
    runs until ``stop()`` is called.
    """

    def __init__(
        self,
        tx_queue: asyncio.Queue,
        cot_writer: CoTWriter,
        uid: str = DEFAULT_UID,
        interval: int = DEFAULT_INTERVAL,
    ) -> None:
        self._tx_queue = tx_queue
        self._writer = cot_writer
        self._uid = uid
        self._interval = interval

        self._lat = 0.0
        self._lon = 0.0
        self._alt = 0.0
        self._course = 0.0
        self._speed = 0.0
        self._running = True

    # -- external API -------------------------------------------------------

    def update_position(
        self,
        lat: float,
        lon: float,
        alt: float,
        course: float = 0.0,
        speed: float = 0.0,
    ) -> None:
        """Update the current drone position (thread-safe for simple floats)."""
        self._lat = lat
        self._lon = lon
        self._alt = alt
        self._course = course
        self._speed = speed

    def stop(self) -> None:
        """Signal the reporter to stop after the current iteration."""
        self._running = False

    # -- async run loop -----------------------------------------------------

    async def run(self, _=-1) -> None:
        """Broadcast current position as a CoT event every *interval* seconds."""
        stale_seconds = self._interval * 3

        while self._running:
            item = MissionItem(
                seq=0,
                command=MAVCmd.NAV_WAYPOINT,
                latitude=self._lat,
                longitude=self._lon,
                altitude=self._alt,
            )
            event_xml = self._writer.format_event(
                item,
                uid=self._uid,
                stale_seconds=stale_seconds,
                cot_type=FRIENDLY_UAV_FIXEDWING,
            )
            await self._tx_queue.put(event_xml.encode("utf-8"))
            logger.debug(
                "Position broadcast: lat=%.6f lon=%.6f alt=%.1f",
                self._lat,
                self._lon,
                self._alt,
            )
            await asyncio.sleep(self._interval)


# ---------------------------------------------------------------------------
# High-level coordinator
# ---------------------------------------------------------------------------

class CoTStreamer:
    """Synchronous facade for live CoT streaming via PyTAK.

    Manages an internal asyncio event loop on a background thread so callers
    do not need to deal with ``async`` / ``await``.

    Parameters
    ----------
    cot_url:
        PyTAK-style URL, e.g. ``udp+wo://239.2.3.1:6969``.
    callsign:
        Drone callsign embedded in CoT ``<contact>`` elements.
    uid:
        Unique identifier for the live position reports.
    """

    def __init__(
        self,
        cot_url: str = DEFAULT_COT_URL,
        callsign: str = DEFAULT_CALLSIGN,
        uid: str = DEFAULT_UID,
    ) -> None:
        self._pytak = _require_pytak()
        self._cot_url = cot_url
        self._callsign = callsign
        self._uid = uid
        self._writer = CoTWriter(callsign=callsign, uid_prefix=uid)

        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._cli_tool: object | None = None
        self._position_reporter: PositionReporter | None = None

    # -- public synchronous API ---------------------------------------------

    def publish_mission(self, items: list[MissionItem]) -> None:
        """One-shot publish all mission waypoints to the TAK network."""
        asyncio.run(self._async_publish_mission(items))

    def start_position_reporting(
        self,
        lat: float,
        lon: float,
        alt: float,
        interval_seconds: int = DEFAULT_INTERVAL,
    ) -> None:
        """Start continuous position reporting on a background thread."""
        self._loop = asyncio.new_event_loop()
        self._position_reporter = PositionReporter(
            tx_queue=asyncio.Queue(),  # placeholder, replaced in setup
            cot_writer=self._writer,
            uid=self._uid,
            interval=interval_seconds,
        )
        self._position_reporter.update_position(lat, lon, alt)

        self._thread = threading.Thread(
            target=self._run_position_loop,
            args=(lat, lon, alt, interval_seconds),
            daemon=True,
            name="cot-streamer",
        )
        self._thread.start()
        logger.info(
            "Position reporting started: lat=%.6f lon=%.6f alt=%.1f interval=%ds",
            lat, lon, alt, interval_seconds,
        )

    def update_position(
        self,
        lat: float,
        lon: float,
        alt: float,
        course: float = 0.0,
        speed: float = 0.0,
    ) -> None:
        """Update the current drone position for the next broadcast."""
        if self._position_reporter is None:
            raise StreamError(
                "Position reporting not started. Call start_position_reporting() first."
            )
        self._position_reporter.update_position(lat, lon, alt, course, speed)

    def stop(self) -> None:
        """Cleanly stop the background event loop and position reporter."""
        if self._position_reporter is not None:
            self._position_reporter.stop()
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread is not None:
            self._thread.join(timeout=5)
        logger.info("CoT streamer stopped")

    # -- internal async helpers ---------------------------------------------

    async def _async_publish_mission(self, items: list[MissionItem]) -> None:
        """Set up a CLITool, publish waypoints, then tear down."""
        config = self._build_config()
        cli = self._pytak.CLITool(config)
        await cli.setup()

        publisher = MissionPublisher(cli.tx_queue, items, self._writer)
        cli.add_task(publisher)
        cli.run_tasks()

        # Give TX worker time to flush
        await asyncio.sleep(0.5 + 0.1 * len(items))
        logger.info("Mission publish complete (%d items)", len(items))

    def _run_position_loop(
        self,
        lat: float,
        lon: float,
        alt: float,
        interval: int,
    ) -> None:
        """Entry point for the background thread running the asyncio loop."""
        asyncio.set_event_loop(self._loop)
        assert self._loop is not None
        self._loop.run_until_complete(
            self._async_position_loop(lat, lon, alt, interval)
        )

    async def _async_position_loop(
        self,
        lat: float,
        lon: float,
        alt: float,
        interval: int,
    ) -> None:
        """Set up CLITool + PositionReporter and run until stopped."""
        config = self._build_config()
        cli = self._pytak.CLITool(config)
        await cli.setup()

        reporter = PositionReporter(
            tx_queue=cli.tx_queue,
            cot_writer=self._writer,
            uid=self._uid,
            interval=interval,
        )
        reporter.update_position(lat, lon, alt)
        # Share reporter reference for update_position calls
        self._position_reporter = reporter

        cli.add_task(reporter)
        cli.run_tasks()

        await asyncio.wait(cli.running_tasks, return_when=asyncio.FIRST_COMPLETED)

    def _build_config(self) -> ConfigParser:
        """Build a ConfigParser with the COT_URL for PyTAK."""
        config = ConfigParser()
        config.add_section("pytak")
        config.set("pytak", "COT_URL", self._cot_url)
        config.set("pytak", "PYTAK_NO_HELLO", "true")
        return config["pytak"]
