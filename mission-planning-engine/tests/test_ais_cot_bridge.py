"""Tests for AIS-to-CoT bridge — TDD-first for vessel track to CoT conversion."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from types import SimpleNamespace

import pytest


def _make_track(**kwargs):
    """Create a mock VesselTrack-like object with sensible defaults."""
    defaults = dict(
        mmsi=211234567,
        latitude=51.5074,
        longitude=-0.1278,
        course_over_ground=180.5,
        speed_over_ground=12.3,
        heading=179.0,
        vessel_name="TEST VESSEL",
        callsign="DABC",
        ship_type=70,  # Cargo
        destination="LONDON",
        nav_status=0,  # Underway
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class TestVesselToCot:
    """Test single vessel-to-CoT conversion."""

    def test_produces_valid_xml(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        track = _make_track()
        result = bridge.vessel_to_cot(track)

        # Must parse without error
        event = ET.fromstring(result)
        assert event.tag == "event"

    def test_event_version_is_2(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        assert event.get("version") == "2.0"

    def test_event_type_fallback_neutral_surface(self):
        """Without ais_types module, should fall back to a-n-S."""
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        # Type will be a-n-S (fallback) or a mapped type if ais_types exists
        cot_type = event.get("type")
        assert cot_type is not None
        assert cot_type.startswith("a-")

    def test_uid_contains_mmsi(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(mmsi=123456789)))
        assert "123456789" in event.get("uid")

    def test_uid_has_prefix(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge(uid_prefix="VESSEL")
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(mmsi=999)))
        assert event.get("uid") == "VESSEL-999"

    def test_callsign_uses_vessel_name(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(vessel_name="HMS VICTORY")))
        contact = event.find(".//contact")
        assert contact is not None
        assert contact.get("callsign") == "HMS VICTORY"

    def test_callsign_falls_back_to_mmsi(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(vessel_name="", mmsi=211234567)))
        contact = event.find(".//contact")
        assert contact.get("callsign") == "MMSI-211234567"

    def test_callsign_falls_back_to_mmsi_when_none(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(vessel_name=None, mmsi=211234567)))
        contact = event.find(".//contact")
        assert contact.get("callsign") == "MMSI-211234567"

    def test_point_has_correct_lat_lon(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(latitude=48.8566, longitude=2.3522)))
        point = event.find("point")
        assert point is not None
        assert point.get("lat") == "48.8566"
        assert point.get("lon") == "2.3522"

    def test_hae_is_zero_sea_level(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        point = event.find("point")
        assert point.get("hae") == "0.0"

    def test_ce_is_10_for_ais_gps(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        point = event.find("point")
        assert point.get("ce") == "10.0"

    def test_speed_conversion_knots_to_mps(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(speed_over_ground=10.0)))
        track_elem = event.find(".//track")
        assert track_elem is not None
        speed = float(track_elem.get("speed"))
        # 10 knots * 0.514444 = 5.14444 m/s
        assert abs(speed - 5.1) < 0.1

    def test_course_in_track_element(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(course_over_ground=270.3)))
        track_elem = event.find(".//track")
        assert track_elem.get("course") == "270.3"

    def test_how_is_machine_generated(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        assert event.get("how") == "m-g"

    def test_remarks_include_vessel_name(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(vessel_name="MV EXPLORER")))
        remarks = event.find(".//remarks")
        assert "MV EXPLORER" in remarks.text

    def test_remarks_include_mmsi(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(mmsi=211234567)))
        remarks = event.find(".//remarks")
        assert "211234567" in remarks.text

    def test_remarks_include_destination(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(destination="ROTTERDAM")))
        remarks = event.find(".//remarks")
        assert "ROTTERDAM" in remarks.text

    def test_remarks_include_nav_status(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track(nav_status=1)))
        remarks = event.find(".//remarks")
        assert "At anchor" in remarks.text

    def test_stale_time_offset(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge(stale_seconds=600)
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        from datetime import datetime

        time_str = event.get("time")
        stale_str = event.get("stale")
        time_dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        stale_dt = datetime.strptime(stale_str, "%Y-%m-%dT%H:%M:%SZ")
        delta = (stale_dt - time_dt).total_seconds()
        assert delta == 600

    def test_default_stale_is_300_seconds(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        event = ET.fromstring(bridge.vessel_to_cot(_make_track()))
        from datetime import datetime

        time_dt = datetime.strptime(event.get("time"), "%Y-%m-%dT%H:%M:%SZ")
        stale_dt = datetime.strptime(event.get("stale"), "%Y-%m-%dT%H:%M:%SZ")
        assert (stale_dt - time_dt).total_seconds() == 300


class TestTracksToCot:
    """Test batch conversion of multiple tracks."""

    def test_skips_zero_position_tracks(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        tracks = [
            _make_track(latitude=0.0, longitude=0.0, mmsi=1),
            _make_track(latitude=51.5, longitude=-0.1, mmsi=2),
        ]
        results = bridge.tracks_to_cot(tracks)
        assert len(results) == 1
        event = ET.fromstring(results[0])
        assert "2" in event.get("uid")

    def test_handles_multiple_vessels(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        tracks = [
            _make_track(mmsi=111, latitude=50.0, longitude=1.0),
            _make_track(mmsi=222, latitude=51.0, longitude=2.0),
            _make_track(mmsi=333, latitude=52.0, longitude=3.0),
        ]
        results = bridge.tracks_to_cot(tracks)
        assert len(results) == 3
        uids = {ET.fromstring(r).get("uid") for r in results}
        assert uids == {"AIS-111", "AIS-222", "AIS-333"}

    def test_empty_list_returns_empty(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        assert bridge.tracks_to_cot([]) == []

    def test_all_zero_position_returns_empty(self):
        from mpe.ais_cot_bridge import AISCoTBridge

        bridge = AISCoTBridge()
        tracks = [
            _make_track(latitude=0.0, longitude=0.0, mmsi=1),
            _make_track(latitude=0.0, longitude=0.0, mmsi=2),
        ]
        assert bridge.tracks_to_cot(tracks) == []
