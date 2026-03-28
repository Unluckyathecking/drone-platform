"""Tests for ADS-B-to-CoT bridge -- TDD-first for aircraft track to CoT conversion.

Follows the same test pattern as test_ais_cot_bridge.py.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from types import SimpleNamespace

import pytest


def _make_track(**kwargs):
    """Create a mock AircraftTrack-like object with sensible defaults."""
    defaults = dict(
        icao_hex="4CA87C",
        latitude=51.47,
        longitude=-0.45,
        altitude_baro_ft=3500.0,
        altitude_geom_ft=3550.0,
        ground_speed_kts=180.5,
        heading=270.3,
        vertical_rate_fpm=-500.0,
        callsign="RYR1234",
        squawk="4521",
        category="A3",
        aircraft_type="B738",
        registration="EI-DCL",
        on_ground=False,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


class TestAircraftToCot:
    """Test single aircraft-to-CoT conversion."""

    def test_produces_valid_xml(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        track = _make_track()
        result = bridge.aircraft_to_cot(track)

        # Must parse without error
        event = ET.fromstring(result)
        assert event.tag == "event"

    def test_event_version_is_2(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track()))
        assert event.get("version") == "2.0"

    def test_event_type_from_category(self):
        """Should map ADS-B category to correct CoT type."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        # A3 = large aircraft → a-n-A-C-F (neutral civilian fixed-wing)
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(category="A3")))
        assert event.get("type") == "a-n-A-C-F"

    def test_event_type_rotorcraft(self):
        """A7 should map to helicopter type."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(category="A7")))
        assert event.get("type") == "a-n-A-C-H"

    def test_event_type_uav(self):
        """B6 should map to UAV type."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(category="B6")))
        assert event.get("type") == "a-n-A-M-F-Q"

    def test_event_type_unknown_category(self):
        """Unknown category should map to unknown air."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(category=None)))
        assert event.get("type") == "a-u-A"

    def test_uid_contains_icao_hex(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(icao_hex="4CA87C")))
        assert "4CA87C" in event.get("uid")

    def test_uid_has_prefix(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge(uid_prefix="AIRCRAFT")
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(icao_hex="ABCDEF")))
        assert event.get("uid") == "AIRCRAFT-ABCDEF"

    def test_default_uid_prefix_is_adsb(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track(icao_hex="ABCDEF")))
        assert event.get("uid") == "ADSB-ABCDEF"

    def test_callsign_uses_flight_number(self):
        """Callsign should prefer flight number (callsign field)."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(callsign="RYR1234", registration="EI-DCL")
        ))
        contact = event.find(".//contact")
        assert contact is not None
        assert contact.get("callsign") == "RYR1234"

    def test_callsign_falls_back_to_registration(self):
        """Callsign should fall back to registration when no flight number."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(callsign="", registration="G-ABCD")
        ))
        contact = event.find(".//contact")
        assert contact.get("callsign") == "G-ABCD"

    def test_callsign_falls_back_to_icao_hex(self):
        """Callsign should fall back to ICAO hex when nothing else available."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(callsign="", registration="", icao_hex="4CA87C")
        ))
        contact = event.find(".//contact")
        assert contact.get("callsign") == "4CA87C"

    def test_point_has_correct_lat_lon(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(latitude=48.8566, longitude=2.3522)
        ))
        point = event.find("point")
        assert point is not None
        assert point.get("lat") == "48.8566"
        assert point.get("lon") == "2.3522"

    def test_hae_uses_geometric_altitude(self):
        """HAE should use geometric altitude in metres."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(altitude_geom_ft=3550.0, altitude_baro_ft=3500.0)
        ))
        point = event.find("point")
        hae = float(point.get("hae"))
        # 3550 ft * 0.3048 = 1081.64 m
        assert abs(hae - 1081.6) < 1.0

    def test_hae_falls_back_to_baro(self):
        """HAE should fall back to baro altitude when geom is zero."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(altitude_geom_ft=0.0, altitude_baro_ft=3500.0)
        ))
        point = event.find("point")
        hae = float(point.get("hae"))
        # 3500 ft * 0.3048 = 1066.8 m
        assert abs(hae - 1066.8) < 1.0

    def test_speed_conversion_knots_to_mps(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(ground_speed_kts=10.0)
        ))
        track_elem = event.find(".//track")
        assert track_elem is not None
        speed = float(track_elem.get("speed"))
        # 10 knots * 0.514444 = 5.14444 m/s
        assert abs(speed - 5.1) < 0.1

    def test_course_in_track_element(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(heading=270.3)
        ))
        track_elem = event.find(".//track")
        assert track_elem.get("course") == "270.3"

    def test_how_is_machine_generated(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track()))
        assert event.get("how") == "m-g"

    def test_remarks_include_callsign(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(callsign="RYR1234")
        ))
        remarks = event.find(".//remarks")
        assert "RYR1234" in remarks.text

    def test_remarks_include_icao(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(icao_hex="4CA87C")
        ))
        remarks = event.find(".//remarks")
        assert "4CA87C" in remarks.text

    def test_remarks_include_aircraft_type(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(aircraft_type="B738")
        ))
        remarks = event.find(".//remarks")
        assert "B738" in remarks.text

    def test_remarks_include_registration(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(registration="EI-DCL")
        ))
        remarks = event.find(".//remarks")
        assert "EI-DCL" in remarks.text

    def test_remarks_include_squawk(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(squawk="4521")
        ))
        remarks = event.find(".//remarks")
        assert "4521" in remarks.text

    def test_emergency_squawk_7700_in_remarks(self):
        """Emergency squawk 7700 should be flagged in remarks."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(squawk="7700")
        ))
        remarks = event.find(".//remarks")
        assert "EMERGENCY" in remarks.text

    def test_emergency_squawk_7500_in_remarks(self):
        """Emergency squawk 7500 should be flagged as hijack in remarks."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(squawk="7500")
        ))
        remarks = event.find(".//remarks")
        assert "HIJACK" in remarks.text

    def test_emergency_squawk_7600_in_remarks(self):
        """Emergency squawk 7600 should be flagged as radio failure in remarks."""
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(
            _make_track(squawk="7600")
        ))
        remarks = event.find(".//remarks")
        assert "RADIO FAILURE" in remarks.text

    def test_stale_time_offset(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge(stale_seconds=600)
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track()))
        from datetime import datetime

        time_str = event.get("time")
        stale_str = event.get("stale")
        time_dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        stale_dt = datetime.strptime(stale_str, "%Y-%m-%dT%H:%M:%SZ")
        delta = (stale_dt - time_dt).total_seconds()
        assert delta == 600

    def test_default_stale_is_120_seconds(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        event = ET.fromstring(bridge.aircraft_to_cot(_make_track()))
        from datetime import datetime

        time_dt = datetime.strptime(event.get("time"), "%Y-%m-%dT%H:%M:%SZ")
        stale_dt = datetime.strptime(event.get("stale"), "%Y-%m-%dT%H:%M:%SZ")
        assert (stale_dt - time_dt).total_seconds() == 120


class TestTracksToCot:
    """Test batch conversion of multiple aircraft tracks."""

    def test_skips_zero_position_tracks(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        tracks = [
            _make_track(latitude=0.0, longitude=0.0, icao_hex="AAA111"),
            _make_track(latitude=51.5, longitude=-0.1, icao_hex="BBB222"),
        ]
        results = bridge.tracks_to_cot(tracks)
        assert len(results) == 1
        event = ET.fromstring(results[0])
        assert "BBB222" in event.get("uid")

    def test_handles_multiple_aircraft(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        tracks = [
            _make_track(icao_hex="AAA111", latitude=50.0, longitude=1.0),
            _make_track(icao_hex="BBB222", latitude=51.0, longitude=2.0),
            _make_track(icao_hex="CCC333", latitude=52.0, longitude=3.0),
        ]
        results = bridge.tracks_to_cot(tracks)
        assert len(results) == 3
        uids = {ET.fromstring(r).get("uid") for r in results}
        assert uids == {"ADSB-AAA111", "ADSB-BBB222", "ADSB-CCC333"}

    def test_empty_list_returns_empty(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        assert bridge.tracks_to_cot([]) == []

    def test_all_zero_position_returns_empty(self):
        from mpe.adsb_cot_bridge import ADSBCoTBridge

        bridge = ADSBCoTBridge()
        tracks = [
            _make_track(latitude=0.0, longitude=0.0, icao_hex="AAA111"),
            _make_track(latitude=0.0, longitude=0.0, icao_hex="BBB222"),
        ]
        assert bridge.tracks_to_cot(tracks) == []
