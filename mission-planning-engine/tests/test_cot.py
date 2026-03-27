"""Tests for the Cursor on Target (CoT) XML writer."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import pytest

from mpe.models import MAVCmd, MAVFrame, MissionItem
from mpe.writers.cot import CoTWriter


def _waypoint(seq: int, lat: float = 51.3680, lon: float = -0.2600, alt: float = 80.0) -> MissionItem:
    return MissionItem(
        seq=seq,
        command=MAVCmd.NAV_WAYPOINT,
        frame=MAVFrame.GLOBAL_RELATIVE_ALT,
        latitude=lat,
        longitude=lon,
        altitude=alt,
    )


def _takeoff(seq: int = 0, alt: float = 80.0) -> MissionItem:
    return MissionItem(
        seq=seq,
        command=MAVCmd.NAV_TAKEOFF,
        frame=MAVFrame.GLOBAL_RELATIVE_ALT,
        latitude=51.3632,
        longitude=-0.2652,
        altitude=alt,
    )


def _rtl(seq: int = 3) -> MissionItem:
    return MissionItem(
        seq=seq,
        command=MAVCmd.NAV_RETURN_TO_LAUNCH,
        frame=MAVFrame.GLOBAL_RELATIVE_ALT,
    )


FIXED_TIME = datetime(2026, 3, 27, 12, 0, 0, tzinfo=timezone.utc)


class TestCoTWriterSingleEvent:
    """Tests for individual CoT event generation."""

    def test_single_waypoint_xml_wellformed(self):
        """XML output should be parseable by xml.etree."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        # Should not raise
        ET.fromstring(xml_str)

    def test_event_has_required_attributes(self):
        """version, type, uid, how, time, start, stale must all be present."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        for attr in ("version", "type", "uid", "how", "time", "start", "stale"):
            assert attr in root.attrib, f"Missing attribute: {attr}"

    def test_point_element_has_required_attributes(self):
        """lat, lon, hae, ce, le must all be present."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None, "Missing <point> element"
        for attr in ("lat", "lon", "hae", "ce", "le"):
            assert attr in point.attrib, f"Missing point attribute: {attr}"

    def test_waypoint_type_code(self):
        """NAV_WAYPOINT should map to b-m-p-w."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == "b-m-p-w"

    def test_takeoff_type_code(self):
        """NAV_TAKEOFF should map to b-m-p-w."""
        writer = CoTWriter()
        xml_str = writer.format_event(_takeoff(), uid="MPE-0", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == "b-m-p-w"

    def test_rtl_type_code(self):
        """NAV_RETURN_TO_LAUNCH should map to b-m-p-w."""
        writer = CoTWriter()
        xml_str = writer.format_event(_rtl(), uid="MPE-3", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == "b-m-p-w"

    def test_latitude_longitude_in_point(self):
        """lat/lon from MissionItem should appear in <point>."""
        writer = CoTWriter()
        xml_str = writer.format_event(
            _waypoint(1, lat=51.3680, lon=-0.2600), uid="MPE-1", base_time=FIXED_TIME,
        )
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert float(point.attrib["lat"]) == pytest.approx(51.3680)
        assert float(point.attrib["lon"]) == pytest.approx(-0.2600)

    def test_altitude_in_hae(self):
        """MissionItem altitude should appear as hae in <point>."""
        writer = CoTWriter()
        xml_str = writer.format_event(
            _waypoint(1, alt=80.0), uid="MPE-1", base_time=FIXED_TIME,
        )
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert float(point.attrib["hae"]) == pytest.approx(80.0)

    def test_geoid_offset_applied(self):
        """When geoid_offset_m is set, hae = altitude + offset."""
        writer = CoTWriter(geoid_offset_m=45.5)
        xml_str = writer.format_event(
            _waypoint(1, alt=80.0), uid="MPE-1", base_time=FIXED_TIME,
        )
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert float(point.attrib["hae"]) == pytest.approx(125.5)

    def test_stale_time_offset(self):
        """Stale should be time + stale_seconds."""
        writer = CoTWriter(stale_seconds=60)
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        stale_str = root.attrib["stale"]
        expected_stale = datetime(2026, 3, 27, 12, 1, 0, tzinfo=timezone.utc)
        assert stale_str == expected_stale.strftime("%Y-%m-%dT%H:%M:%SZ")

    def test_uid_includes_seq(self):
        """UID should contain the sequence number."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(7), uid="MPE-7", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert "7" in root.attrib["uid"]

    def test_callsign_in_contact(self):
        """Callsign should appear in <contact> element."""
        writer = CoTWriter(callsign="TEST-DRONE")
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        detail = root.find("detail")
        assert detail is not None
        contact = detail.find("contact")
        assert contact is not None
        assert contact.attrib["callsign"] == "TEST-DRONE"

    def test_iso8601_format(self):
        """Time attributes should be ISO 8601 with Z suffix."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        for attr in ("time", "start", "stale"):
            val = root.attrib[attr]
            assert val.endswith("Z"), f"{attr} should end with Z, got {val}"
            # Should be parseable as ISO 8601
            datetime.strptime(val, "%Y-%m-%dT%H:%M:%SZ")

    def test_ce_le_defaults(self):
        """ce and le should default to 9999999."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert point.attrib["ce"] == "9999999"
        assert point.attrib["le"] == "9999999"

    def test_version_is_2_0(self):
        """Event version should be 2.0."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["version"] == "2.0"

    def test_how_is_m_g(self):
        """how attribute should be m-g (machine-generated)."""
        writer = CoTWriter()
        xml_str = writer.format_event(_waypoint(1), uid="MPE-1", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["how"] == "m-g"


class TestCoTWriterMission:
    """Tests for full mission conversion."""

    def test_full_mission_multiple_events(self):
        """3-item mission should produce 3 CoT events."""
        writer = CoTWriter()
        items = [_takeoff(0), _waypoint(1), _rtl(2)]
        events = writer.mission_to_events(items, base_time=FIXED_TIME)
        assert len(events) == 3
        # Each should be well-formed XML
        for ev in events:
            ET.fromstring(ev)

    def test_mission_uids_contain_prefix(self):
        """UIDs should use the configured uid_prefix."""
        writer = CoTWriter(uid_prefix="SORTIE")
        items = [_waypoint(0), _waypoint(1)]
        events = writer.mission_to_events(items, base_time=FIXED_TIME)
        for ev in events:
            root = ET.fromstring(ev)
            assert root.attrib["uid"].startswith("SORTIE-")

    def test_mission_uids_contain_seq_numbers(self):
        """Each event UID should include its mission item seq number."""
        writer = CoTWriter()
        items = [_waypoint(0), _waypoint(1), _waypoint(2)]
        events = writer.mission_to_events(items, base_time=FIXED_TIME)
        for i, ev in enumerate(events):
            root = ET.fromstring(ev)
            assert str(i) in root.attrib["uid"]

    def test_mission_callsign_propagated(self):
        """Callsign from constructor should appear in all events."""
        writer = CoTWriter(callsign="ALPHA-1")
        items = [_waypoint(0), _waypoint(1)]
        events = writer.mission_to_events(items, base_time=FIXED_TIME)
        for ev in events:
            root = ET.fromstring(ev)
            contact = root.find("detail/contact")
            assert contact is not None
            assert contact.attrib["callsign"] == "ALPHA-1"


class TestMissionWriterContract:
    """Tests that CoTWriter fulfills the MissionWriter ABC contract."""

    def test_format_returns_string(self):
        """MissionWriter.format() contract -- returns str."""
        writer = CoTWriter()
        items = [_waypoint(0), _waypoint(1)]
        result = writer.format(items)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_contains_all_events(self):
        """format() output should contain all events."""
        writer = CoTWriter()
        items = [_waypoint(0), _waypoint(1), _waypoint(2)]
        result = writer.format(items)
        assert result.count("<event ") == 3

    def test_write_creates_file(self, tmp_path):
        """MissionWriter.write() should create a file on disk."""
        writer = CoTWriter()
        items = [_waypoint(0), _waypoint(1)]
        path = writer.write(items, tmp_path / "mission.cot.xml")
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<event " in content

    def test_write_file_is_valid_xml(self, tmp_path):
        """Written file should be parseable as XML."""
        writer = CoTWriter()
        items = [_waypoint(0)]
        path = writer.write(items, tmp_path / "mission.cot.xml")
        content = path.read_text(encoding="utf-8")
        # The wrapper should make it valid XML
        ET.fromstring(content)

    def test_unknown_command_uses_default_type(self):
        """Commands not in MAVCMD_TO_COT should use WAYPOINT as fallback."""
        writer = CoTWriter()
        item = MissionItem(
            seq=0,
            command=MAVCmd.NAV_LOITER_UNLIM,
            latitude=51.3680,
            longitude=-0.2600,
            altitude=80.0,
        )
        xml_str = writer.format_event(item, uid="MPE-0", base_time=FIXED_TIME)
        root = ET.fromstring(xml_str)
        assert root.attrib["type"] == "b-m-p-w"
