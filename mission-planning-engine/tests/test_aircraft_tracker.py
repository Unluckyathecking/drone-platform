"""Tests for the aircraft track cache (aircraft_tracker module).

Pure-Python data structures -- no external dependencies required.
Follows the same test pattern as test_vessel_tracker.py.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from mpe.aircraft_tracker import AircraftTrack, AircraftTracker


# ---------------------------------------------------------------------------
# AircraftTrack dataclass
# ---------------------------------------------------------------------------

class TestAircraftTrack:
    """Tests for the AircraftTrack dataclass."""

    def test_creation_with_all_fields(self):
        """AircraftTrack should accept all fields at construction."""
        now = datetime.now(timezone.utc)
        track = AircraftTrack(
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
            last_update=now,
        )
        assert track.icao_hex == "4CA87C"
        assert track.latitude == 51.47
        assert track.longitude == -0.45
        assert track.altitude_baro_ft == 3500.0
        assert track.altitude_geom_ft == 3550.0
        assert track.ground_speed_kts == 180.5
        assert track.heading == 270.3
        assert track.vertical_rate_fpm == -500.0
        assert track.callsign == "RYR1234"
        assert track.squawk == "4521"
        assert track.category == "A3"
        assert track.aircraft_type == "B738"
        assert track.registration == "EI-DCL"
        assert track.on_ground is False
        assert track.last_update == now

    def test_defaults(self):
        """AircraftTrack should have sensible defaults for optional fields."""
        track = AircraftTrack(icao_hex="ABCDEF")
        assert track.latitude == 0.0
        assert track.longitude == 0.0
        assert track.altitude_baro_ft == 0.0
        assert track.altitude_geom_ft == 0.0
        assert track.ground_speed_kts == 0.0
        assert track.callsign == ""
        assert track.squawk == ""
        assert track.category == ""
        assert track.on_ground is False

    def test_is_stale_false_for_fresh_track(self):
        """A freshly created track should not be stale."""
        track = AircraftTrack(icao_hex="ABCDEF")
        assert track.is_stale is False

    def test_is_stale_true_for_old_track(self):
        """A track with last_update > 60 seconds ago should be stale."""
        old_time = datetime.now(timezone.utc) - timedelta(seconds=61)
        track = AircraftTrack(icao_hex="ABCDEF", last_update=old_time)
        assert track.is_stale is True

    def test_is_stale_false_at_boundary(self):
        """A track exactly under 60 seconds old should not be stale."""
        boundary = datetime.now(timezone.utc) - timedelta(seconds=59)
        track = AircraftTrack(icao_hex="ABCDEF", last_update=boundary)
        assert track.is_stale is False

    def test_altitude_m_prefers_geometric(self):
        """altitude_m should prefer geometric altitude over barometric."""
        track = AircraftTrack(
            icao_hex="ABCDEF",
            altitude_baro_ft=3500.0,
            altitude_geom_ft=3550.0,
        )
        expected = 3550.0 * 0.3048
        assert track.altitude_m == pytest.approx(expected, rel=1e-3)

    def test_altitude_m_falls_back_to_baro(self):
        """altitude_m should fall back to baro when geom is zero."""
        track = AircraftTrack(
            icao_hex="ABCDEF",
            altitude_baro_ft=3500.0,
            altitude_geom_ft=0.0,
        )
        expected = 3500.0 * 0.3048
        assert track.altitude_m == pytest.approx(expected, rel=1e-3)

    def test_altitude_m_zero_when_both_zero(self):
        """altitude_m should be zero when both altitudes are zero."""
        track = AircraftTrack(icao_hex="ABCDEF")
        assert track.altitude_m == 0.0

    def test_speed_mps_conversion(self):
        """speed_mps should convert knots to m/s correctly."""
        track = AircraftTrack(icao_hex="ABCDEF", ground_speed_kts=10.0)
        assert track.speed_mps == pytest.approx(5.14444, rel=1e-3)

    def test_speed_mps_zero(self):
        """Zero speed should convert to zero."""
        track = AircraftTrack(icao_hex="ABCDEF", ground_speed_kts=0.0)
        assert track.speed_mps == 0.0

    def test_is_emergency_7700(self):
        """Squawk 7700 should be flagged as emergency."""
        track = AircraftTrack(icao_hex="ABCDEF", squawk="7700")
        assert track.is_emergency is True

    def test_is_emergency_7600(self):
        """Squawk 7600 (radio failure) should be flagged as emergency."""
        track = AircraftTrack(icao_hex="ABCDEF", squawk="7600")
        assert track.is_emergency is True

    def test_is_emergency_7500(self):
        """Squawk 7500 (hijack) should be flagged as emergency."""
        track = AircraftTrack(icao_hex="ABCDEF", squawk="7500")
        assert track.is_emergency is True

    def test_is_not_emergency_normal_squawk(self):
        """Normal squawk should not be flagged as emergency."""
        track = AircraftTrack(icao_hex="ABCDEF", squawk="4521")
        assert track.is_emergency is False

    def test_is_not_emergency_empty_squawk(self):
        """Empty squawk should not be flagged as emergency."""
        track = AircraftTrack(icao_hex="ABCDEF", squawk="")
        assert track.is_emergency is False


# ---------------------------------------------------------------------------
# AircraftTracker cache
# ---------------------------------------------------------------------------

class TestAircraftTracker:
    """Tests for the AircraftTracker cache."""

    def test_update_creates_new_track(self):
        """update() for an unknown ICAO hex should create a new AircraftTrack."""
        tracker = AircraftTracker()
        track = tracker.update(icao_hex="4ca87c", latitude=51.47, longitude=-0.45)
        assert track.icao_hex == "4CA87C"
        assert track.latitude == 51.47
        assert track.longitude == -0.45

    def test_update_normalises_icao_to_upper(self):
        """update() should normalise ICAO hex to uppercase."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="abcdef")
        assert tracker.get("ABCDEF") is not None
        assert tracker.get("abcdef") is not None  # get also normalises

    def test_update_merges_with_existing(self):
        """update() for a known ICAO hex should merge new fields."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="4CA87C", latitude=51.47, longitude=-0.45)
        tracker.update(icao_hex="4CA87C", callsign="RYR1234", aircraft_type="B738")

        track = tracker.get("4CA87C")
        assert track is not None
        assert track.latitude == 51.47        # preserved from first update
        assert track.callsign == "RYR1234"    # added by second update
        assert track.aircraft_type == "B738"

    def test_update_ignores_none_values(self):
        """update() should skip None values without overwriting existing data."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="4CA87C", callsign="RYR1234")
        tracker.update(icao_hex="4CA87C", callsign=None, latitude=52.0)

        track = tracker.get("4CA87C")
        assert track is not None
        assert track.callsign == "RYR1234"  # not overwritten by None
        assert track.latitude == 52.0

    def test_get_returns_none_for_unknown_icao(self):
        """get() for an unknown ICAO hex should return None."""
        tracker = AircraftTracker()
        assert tracker.get("FFFFFF") is None

    def test_active_tracks_excludes_stale(self):
        """active_tracks should exclude tracks older than stale timeout."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5)
        # Make the track stale by backdating last_update
        tracker._tracks["AAA111"].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=61)
        )
        tracker.update(icao_hex="BBB222", latitude=52.0)

        active = tracker.active_tracks
        assert len(active) == 1
        assert active[0].icao_hex == "BBB222"

    def test_all_tracks_includes_stale(self):
        """all_tracks should include stale tracks."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5)
        tracker._tracks["AAA111"].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=61)
        )
        tracker.update(icao_hex="BBB222", latitude=52.0)

        assert len(tracker.all_tracks) == 2

    def test_aircraft_near_within_radius(self):
        """aircraft_near should return aircraft within the given radius."""
        tracker = AircraftTracker()
        # Two aircraft near London
        tracker.update(icao_hex="AAA111", latitude=51.5074, longitude=-0.1278)
        tracker.update(icao_hex="BBB222", latitude=51.5100, longitude=-0.1300)
        # One aircraft far away (Paris)
        tracker.update(icao_hex="CCC333", latitude=48.8566, longitude=2.3522)

        near = tracker.aircraft_near(51.5074, -0.1278, radius_km=5.0)
        icaos = {t.icao_hex for t in near}
        assert "AAA111" in icaos
        assert "BBB222" in icaos
        assert "CCC333" not in icaos

    def test_aircraft_near_excludes_zero_position(self):
        """aircraft_near should skip aircraft with lat/lon still at 0.0."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111")  # no position yet
        tracker.update(icao_hex="BBB222", latitude=51.5, longitude=-0.1)

        near = tracker.aircraft_near(51.5, -0.1, radius_km=100.0)
        assert len(near) == 1
        assert near[0].icao_hex == "BBB222"

    def test_emergencies_returns_emergency_squawks(self):
        """emergencies() should return aircraft with emergency squawks."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5, squawk="7700")
        tracker.update(icao_hex="BBB222", latitude=52.0, squawk="4521")
        tracker.update(icao_hex="CCC333", latitude=52.5, squawk="7500")

        emergencies = tracker.emergencies()
        icaos = {t.icao_hex for t in emergencies}
        assert "AAA111" in icaos
        assert "CCC333" in icaos
        assert "BBB222" not in icaos

    def test_emergencies_excludes_stale(self):
        """emergencies() should only return active (non-stale) emergency tracks."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5, squawk="7700")
        tracker._tracks["AAA111"].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=61)
        )

        assert len(tracker.emergencies()) == 0

    def test_purge_stale_removes_old_tracks(self):
        """purge_stale should remove stale tracks and return count."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5)
        tracker.update(icao_hex="BBB222", latitude=52.0)
        # Make one stale
        tracker._tracks["AAA111"].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=61)
        )

        removed = tracker.purge_stale()
        assert removed == 1
        assert tracker.get("AAA111") is None
        assert tracker.get("BBB222") is not None

    def test_purge_stale_returns_zero_when_none_stale(self):
        """purge_stale should return 0 when no tracks are stale."""
        tracker = AircraftTracker()
        tracker.update(icao_hex="AAA111", latitude=51.5)
        assert tracker.purge_stale() == 0
