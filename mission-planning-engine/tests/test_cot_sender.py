"""Tests for the live CoT streaming module (cot_sender).

All tests mock pytak so no real network connection is required.
The module handles missing pytak gracefully via StreamError.
"""

from __future__ import annotations

import asyncio
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from mpe.cot_types import FRIENDLY_UAV_FIXEDWING, WAYPOINT
from mpe.models import MAVCmd, MAVFrame, MissionItem
from mpe.writers.cot import CoTWriter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXED_TIME = datetime(2026, 3, 27, 12, 0, 0, tzinfo=timezone.utc)


def _waypoint(seq: int, lat: float = 51.3680, lon: float = -0.2600, alt: float = 80.0) -> MissionItem:
    return MissionItem(
        seq=seq,
        command=MAVCmd.NAV_WAYPOINT,
        frame=MAVFrame.GLOBAL_RELATIVE_ALT,
        latitude=lat,
        longitude=lon,
        altitude=alt,
    )


def _sample_mission() -> list[MissionItem]:
    """Minimal 3-item mission."""
    return [
        MissionItem(
            seq=0, command=MAVCmd.NAV_TAKEOFF,
            latitude=51.3632, longitude=-0.2652, altitude=80.0,
        ),
        _waypoint(1),
        MissionItem(seq=2, command=MAVCmd.NAV_RETURN_TO_LAUNCH),
    ]


# ---------------------------------------------------------------------------
# CoTWriter.format_event cot_type override (non-breaking change)
# ---------------------------------------------------------------------------

class TestCoTWriterTypeOverride:
    """Verify the new optional cot_type parameter on format_event."""

    def test_default_type_unchanged(self):
        """When cot_type is not passed, behaviour is unchanged."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == WAYPOINT

    def test_override_type_to_uav(self):
        """Passing cot_type should override the auto-resolved type."""
        writer = CoTWriter()
        xml_str = writer.format_event(
            _waypoint(1),
            uid="MPE-1",
            base_time=FIXED_TIME,
            cot_type=FRIENDLY_UAV_FIXEDWING,
        )
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == FRIENDLY_UAV_FIXEDWING

    def test_override_with_arbitrary_type(self):
        """Any string can be used as cot_type."""
        writer = CoTWriter()
        xml_str = writer.format_event(
            _waypoint(1),
            uid="MPE-1",
            base_time=FIXED_TIME,
            cot_type="a-h-A-M-F-Q",
        )
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == "a-h-A-M-F-Q"

    def test_none_cot_type_uses_default(self):
        """Explicitly passing cot_type=None behaves like omitting it."""
        writer = CoTWriter()
        xml_str = writer.format_event(
            _waypoint(1),
            uid="MPE-1",
            base_time=FIXED_TIME,
            cot_type=None,
        )
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == WAYPOINT


# ---------------------------------------------------------------------------
# MissionPublisher
# ---------------------------------------------------------------------------

class TestMissionPublisher:
    """Test the one-shot mission publisher."""

    def test_publishes_correct_count(self):
        """Publisher should put one event per mission item onto the queue."""
        from mpe.cot_sender import MissionPublisher

        queue: asyncio.Queue = asyncio.Queue()
        items = _sample_mission()
        writer = CoTWriter()
        publisher = MissionPublisher(queue, items, writer)

        asyncio.run(publisher.run())

        assert queue.qsize() == len(items)

    def test_published_events_are_valid_xml(self):
        """Each queued event should be well-formed CoT XML."""
        from mpe.cot_sender import MissionPublisher

        queue: asyncio.Queue = asyncio.Queue()
        items = _sample_mission()
        writer = CoTWriter()
        publisher = MissionPublisher(queue, items, writer)

        asyncio.run(publisher.run())

        while not queue.empty():
            data = queue.get_nowait()
            assert isinstance(data, bytes)
            root = ET.fromstring(data.decode("utf-8"))
            assert root.tag == "event"
            assert root.attrib["version"] == "2.0"

    def test_published_events_are_waypoint_type(self):
        """Mission waypoints should use the default MAVCMD_TO_COT mapping."""
        from mpe.cot_sender import MissionPublisher

        queue: asyncio.Queue = asyncio.Queue()
        items = [_waypoint(0), _waypoint(1)]
        writer = CoTWriter()
        publisher = MissionPublisher(queue, items, writer)

        asyncio.run(publisher.run())

        while not queue.empty():
            data = queue.get_nowait()
            root = ET.fromstring(data.decode("utf-8"))
            assert root.attrib["type"] == WAYPOINT


# ---------------------------------------------------------------------------
# PositionReporter
# ---------------------------------------------------------------------------

class TestPositionReporter:
    """Test the continuous position reporter."""

    def test_generates_uav_type(self):
        """Position events should use the friendly UAV fixedwing type."""
        from mpe.cot_sender import PositionReporter

        queue: asyncio.Queue = asyncio.Queue()
        writer = CoTWriter()
        reporter = PositionReporter(queue, writer, uid="TEST-POS", interval=1)
        reporter.update_position(51.3680, -0.2600, 80.0)

        async def run_one_cycle():
            # Run reporter briefly then stop
            task = asyncio.create_task(reporter.run())
            await asyncio.sleep(0.2)
            reporter.stop()
            # Give it time to finish the current iteration
            await asyncio.sleep(1.2)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_one_cycle())

        assert queue.qsize() >= 1
        data = queue.get_nowait()
        root = ET.fromstring(data.decode("utf-8"))
        assert root.attrib["type"] == FRIENDLY_UAV_FIXEDWING

    def test_includes_updated_position(self):
        """After update_position(), the next broadcast should reflect the new coords."""
        from mpe.cot_sender import PositionReporter

        queue: asyncio.Queue = asyncio.Queue()
        writer = CoTWriter()
        reporter = PositionReporter(queue, writer, uid="TEST-POS", interval=1)
        reporter.update_position(52.0, -1.0, 100.0)

        async def run_one_cycle():
            task = asyncio.create_task(reporter.run())
            await asyncio.sleep(0.2)
            reporter.stop()
            await asyncio.sleep(1.2)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_one_cycle())

        assert queue.qsize() >= 1
        data = queue.get_nowait()
        root = ET.fromstring(data.decode("utf-8"))
        point = root.find("point")
        assert point is not None
        assert float(point.attrib["lat"]) == pytest.approx(52.0)
        assert float(point.attrib["lon"]) == pytest.approx(-1.0)
        assert float(point.attrib["hae"]) == pytest.approx(100.0)

    def test_uid_matches(self):
        """The event uid should match the configured uid."""
        from mpe.cot_sender import PositionReporter

        queue: asyncio.Queue = asyncio.Queue()
        writer = CoTWriter()
        reporter = PositionReporter(queue, writer, uid="ALPHA-1", interval=1)
        reporter.update_position(51.0, -0.5, 50.0)

        async def run_one_cycle():
            task = asyncio.create_task(reporter.run())
            await asyncio.sleep(0.2)
            reporter.stop()
            await asyncio.sleep(1.2)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_one_cycle())

        data = queue.get_nowait()
        root = ET.fromstring(data.decode("utf-8"))
        assert root.attrib["uid"] == "ALPHA-1"

    def test_stale_is_3x_interval(self):
        """Stale time should be 3x the update interval."""
        from mpe.cot_sender import PositionReporter

        queue: asyncio.Queue = asyncio.Queue()
        writer = CoTWriter()
        reporter = PositionReporter(queue, writer, uid="TEST", interval=10)
        reporter.update_position(51.0, -0.5, 50.0)

        async def run_one_cycle():
            task = asyncio.create_task(reporter.run())
            await asyncio.sleep(0.2)
            reporter.stop()
            await asyncio.sleep(10.2)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_one_cycle())

        data = queue.get_nowait()
        root = ET.fromstring(data.decode("utf-8"))
        time_str = root.attrib["time"]
        stale_str = root.attrib["stale"]
        time_dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        stale_dt = datetime.strptime(stale_str, "%Y-%m-%dT%H:%M:%SZ")
        diff = (stale_dt - time_dt).total_seconds()
        assert diff == pytest.approx(30, abs=1)  # 3 * 10s interval


# ---------------------------------------------------------------------------
# CoTStreamer construction
# ---------------------------------------------------------------------------

class TestCoTStreamer:
    """Test the high-level CoTStreamer coordinator."""

    def test_construction_with_pytak_available(self):
        """CoTStreamer should construct successfully when pytak is importable."""
        from mpe.cot_sender import CoTStreamer

        streamer = CoTStreamer(cot_url="udp+wo://239.2.3.1:6969")
        assert streamer is not None

    def test_update_position_before_start_raises(self):
        """Calling update_position before start_position_reporting should raise."""
        from mpe.cot_sender import CoTStreamer, StreamError

        streamer = CoTStreamer()
        with pytest.raises(StreamError, match="not started"):
            streamer.update_position(51.0, -0.5, 80.0)


# ---------------------------------------------------------------------------
# Graceful handling of missing pytak
# ---------------------------------------------------------------------------

class TestMissingPytak:
    """Verify that the module handles missing pytak gracefully."""

    def test_require_pytak_raises_stream_error(self):
        """_require_pytak should raise StreamError when pytak is not importable."""
        saved = {}
        keys = [k for k in sys.modules if k == "pytak" or k.startswith("pytak.")]
        for k in keys:
            saved[k] = sys.modules.pop(k)

        try:
            with patch.dict(sys.modules, {"pytak": None}):
                from mpe.cot_sender import _require_pytak, StreamError
                with pytest.raises(StreamError, match="pytak is not installed"):
                    _require_pytak()
        finally:
            for k, v in saved.items():
                sys.modules[k] = v

    def test_cot_streamer_raises_when_pytak_missing(self):
        """CoTStreamer() should raise StreamError if pytak cannot be imported."""
        saved = {}
        keys = [k for k in sys.modules if k == "pytak" or k.startswith("pytak.")]
        for k in keys:
            saved[k] = sys.modules.pop(k)

        try:
            with patch.dict(sys.modules, {"pytak": None}):
                # Re-import to trigger the lazy import
                from mpe.cot_sender import CoTStreamer, StreamError
                with pytest.raises(StreamError, match="pytak is not installed"):
                    CoTStreamer()
        finally:
            for k, v in saved.items():
                sys.modules[k] = v
