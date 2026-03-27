"""Tests for the vessel track cache (vessel_tracker module).

Pure-Python data structures — no external dependencies required.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from mpe.vessel_tracker import VesselTrack, VesselTracker


# ---------------------------------------------------------------------------
# VesselTrack dataclass
# ---------------------------------------------------------------------------

class TestVesselTrack:
    """Tests for the VesselTrack dataclass."""

    def test_creation_with_all_fields(self):
        """VesselTrack should accept all fields at construction."""
        now = datetime.now(timezone.utc)
        track = VesselTrack(
            mmsi=211234567,
            latitude=51.5074,
            longitude=-0.1278,
            course_over_ground=180.0,
            speed_over_ground=12.5,
            heading=179.0,
            vessel_name="TEST SHIP",
            callsign="DABC",
            imo_number=1234567,
            ship_type=70,
            destination="LONDON",
            nav_status=0,
            last_update=now,
        )
        assert track.mmsi == 211234567
        assert track.latitude == 51.5074
        assert track.longitude == -0.1278
        assert track.course_over_ground == 180.0
        assert track.speed_over_ground == 12.5
        assert track.heading == 179.0
        assert track.vessel_name == "TEST SHIP"
        assert track.callsign == "DABC"
        assert track.imo_number == 1234567
        assert track.ship_type == 70
        assert track.destination == "LONDON"
        assert track.nav_status == 0
        assert track.last_update == now

    def test_defaults(self):
        """VesselTrack should have sensible defaults for optional fields."""
        track = VesselTrack(mmsi=123456789)
        assert track.latitude == 0.0
        assert track.longitude == 0.0
        assert track.vessel_name == ""
        assert track.nav_status == 15  # undefined

    def test_is_stale_false_for_fresh_track(self):
        """A freshly created track should not be stale."""
        track = VesselTrack(mmsi=123456789)
        assert track.is_stale is False

    def test_is_stale_true_for_old_track(self):
        """A track with last_update > 5 minutes ago should be stale."""
        old_time = datetime.now(timezone.utc) - timedelta(seconds=301)
        track = VesselTrack(mmsi=123456789, last_update=old_time)
        assert track.is_stale is True

    def test_is_stale_false_at_boundary(self):
        """A track exactly 5 minutes old should not be stale (edge case)."""
        boundary = datetime.now(timezone.utc) - timedelta(seconds=299)
        track = VesselTrack(mmsi=123456789, last_update=boundary)
        assert track.is_stale is False

    def test_speed_mps_conversion(self):
        """speed_mps should convert knots to m/s correctly."""
        track = VesselTrack(mmsi=123456789, speed_over_ground=10.0)
        assert track.speed_mps == pytest.approx(5.14444, rel=1e-3)

    def test_speed_mps_zero(self):
        """Zero speed should convert to zero."""
        track = VesselTrack(mmsi=123456789, speed_over_ground=0.0)
        assert track.speed_mps == 0.0


# ---------------------------------------------------------------------------
# VesselTracker cache
# ---------------------------------------------------------------------------

class TestVesselTracker:
    """Tests for the VesselTracker cache."""

    def test_update_creates_new_track(self):
        """update() for an unknown MMSI should create a new VesselTrack."""
        tracker = VesselTracker()
        track = tracker.update(mmsi=211000001, latitude=51.5, longitude=-0.1)
        assert track.mmsi == 211000001
        assert track.latitude == 51.5
        assert track.longitude == -0.1

    def test_update_merges_with_existing(self):
        """update() for a known MMSI should merge new fields."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, latitude=51.5, longitude=-0.1)
        tracker.update(mmsi=211000001, vessel_name="EVER GIVEN", ship_type=70)

        track = tracker.get(211000001)
        assert track is not None
        assert track.latitude == 51.5         # preserved from first update
        assert track.vessel_name == "EVER GIVEN"  # added by second update
        assert track.ship_type == 70

    def test_update_ignores_none_values(self):
        """update() should skip None values without overwriting existing data."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, vessel_name="TEST SHIP")
        tracker.update(mmsi=211000001, vessel_name=None, latitude=52.0)

        track = tracker.get(211000001)
        assert track is not None
        assert track.vessel_name == "TEST SHIP"  # not overwritten by None
        assert track.latitude == 52.0

    def test_get_returns_none_for_unknown_mmsi(self):
        """get() for an unknown MMSI should return None."""
        tracker = VesselTracker()
        assert tracker.get(999999999) is None

    def test_active_tracks_excludes_stale(self):
        """active_tracks should exclude tracks older than stale timeout."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, latitude=51.5)
        # Make the track stale by backdating last_update
        tracker._tracks[211000001].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=301)
        )
        tracker.update(mmsi=211000002, latitude=52.0)

        active = tracker.active_tracks
        assert len(active) == 1
        assert active[0].mmsi == 211000002

    def test_all_tracks_includes_stale(self):
        """all_tracks should include stale tracks."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, latitude=51.5)
        tracker._tracks[211000001].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=301)
        )
        tracker.update(mmsi=211000002, latitude=52.0)

        assert len(tracker.all_tracks) == 2

    def test_vessels_near_within_radius(self):
        """vessels_near should return vessels within the given radius."""
        tracker = VesselTracker()
        # Two vessels near London
        tracker.update(mmsi=211000001, latitude=51.5074, longitude=-0.1278)
        tracker.update(mmsi=211000002, latitude=51.5100, longitude=-0.1300)
        # One vessel far away (Paris)
        tracker.update(mmsi=211000003, latitude=48.8566, longitude=2.3522)

        near = tracker.vessels_near(51.5074, -0.1278, radius_km=5.0)
        mmsis = {t.mmsi for t in near}
        assert 211000001 in mmsis
        assert 211000002 in mmsis
        assert 211000003 not in mmsis

    def test_vessels_near_excludes_zero_position(self):
        """vessels_near should skip vessels with lat/lon still at 0.0."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001)  # no position yet
        tracker.update(mmsi=211000002, latitude=51.5, longitude=-0.1)

        near = tracker.vessels_near(51.5, -0.1, radius_km=100.0)
        assert len(near) == 1
        assert near[0].mmsi == 211000002

    def test_purge_stale_removes_old_tracks(self):
        """purge_stale should remove stale tracks and return count."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, latitude=51.5)
        tracker.update(mmsi=211000002, latitude=52.0)
        # Make one stale
        tracker._tracks[211000001].last_update = (
            datetime.now(timezone.utc) - timedelta(seconds=301)
        )

        removed = tracker.purge_stale()
        assert removed == 1
        assert tracker.get(211000001) is None
        assert tracker.get(211000002) is not None

    def test_purge_stale_returns_zero_when_none_stale(self):
        """purge_stale should return 0 when no tracks are stale."""
        tracker = VesselTracker()
        tracker.update(mmsi=211000001, latitude=51.5)
        assert tracker.purge_stale() == 0
