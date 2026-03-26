"""Tests for the mission planner."""

import pytest

from mpe.models import BasicMission, Coordinate, MAVCmd
from mpe.planner import ValidationError, build_mission, validate


# ── Fixtures ──────────────────────────────────────────────────────────

EPSOM_HOME = Coordinate(latitude=51.3632, longitude=-0.2652, altitude=84.0)

NEARBY_WAYPOINTS = [
    Coordinate(latitude=51.3680, longitude=-0.2600),
    Coordinate(latitude=51.3720, longitude=-0.2550),
]


def _mission(**kwargs):
    defaults = dict(home=EPSOM_HOME, waypoints=NEARBY_WAYPOINTS, cruise_altitude_m=80.0)
    defaults.update(kwargs)
    return BasicMission(**defaults)


# ── Validation Tests ──────────────────────────────────────────────────


class TestValidation:
    def test_valid_mission_no_errors(self):
        warnings = validate(_mission())
        # Nearby waypoints should produce no warnings
        assert len(warnings) == 0

    def test_altitude_exceeds_caa_limit(self):
        with pytest.raises(ValidationError, match="120m"):
            validate(_mission(cruise_altitude_m=150.0))

    def test_range_exceeded(self):
        """Waypoint 100km away should fail range check."""
        far_wp = [Coordinate(latitude=52.3632, longitude=-0.2652)]  # ~111km north
        with pytest.raises(ValidationError, match="exceeds max range"):
            validate(_mission(waypoints=far_wp))

    def test_warning_for_distant_waypoint(self):
        """Waypoint beyond 40% of max range triggers headwind warning.

        With threshold at 40%: a waypoint 5km away warns if max_range=10
        (threshold=4km, 5>4). Round trip for single wp = 10km = max_range,
        so we need a multi-wp route where total is within range but one wp is far.
        Route: home → close_wp → far_wp → home. Total ≈ 0.1 + 5 + 5 = 10.1km.
        Use max_range=11 to pass the hard check.
        """
        close_wp = Coordinate(latitude=51.3635, longitude=-0.2650)  # ~0.04km
        far_wp = Coordinate(latitude=51.4082, longitude=-0.2652)  # ~5km north
        warnings = validate(_mission(
            waypoints=[close_wp, far_wp],
            max_range_km=11.0,
        ))
        assert any("beyond safe threshold" in w for w in warnings)


# ── Planner Tests ─────────────────────────────────────────────────────


class TestBuildMission:
    def test_output_starts_with_home(self):
        items = build_mission(_mission())
        assert items[0].seq == 0
        assert items[0].current is True
        assert items[0].latitude == EPSOM_HOME.latitude
        assert items[0].longitude == EPSOM_HOME.longitude

    def test_second_item_is_takeoff(self):
        items = build_mission(_mission())
        assert items[1].command == MAVCmd.NAV_TAKEOFF
        assert items[1].altitude == 80.0
        assert items[1].param1 == 15.0  # takeoff pitch

    def test_waypoints_in_order(self):
        items = build_mission(_mission())
        # Items 2 and 3 should be the two waypoints
        assert items[2].command == MAVCmd.NAV_WAYPOINT
        assert items[2].latitude == NEARBY_WAYPOINTS[0].latitude
        assert items[3].command == MAVCmd.NAV_WAYPOINT
        assert items[3].latitude == NEARBY_WAYPOINTS[1].latitude

    def test_last_item_is_rtl(self):
        items = build_mission(_mission())
        assert items[-1].command == MAVCmd.NAV_RETURN_TO_LAUNCH

    def test_sequence_numbers_contiguous(self):
        items = build_mission(_mission())
        for i, item in enumerate(items):
            assert item.seq == i

    def test_total_items_count(self):
        """HOME + TAKEOFF + N waypoints + RTL = N + 3."""
        items = build_mission(_mission())
        assert len(items) == len(NEARBY_WAYPOINTS) + 3

    def test_single_waypoint(self):
        single = _mission(waypoints=[NEARBY_WAYPOINTS[0]])
        items = build_mission(single)
        assert len(items) == 4  # HOME + TAKEOFF + 1 WP + RTL

    def test_waypoint_uses_cruise_alt_when_no_explicit_alt(self):
        items = build_mission(_mission())
        # Waypoints have altitude=0 in fixture, so should use cruise_altitude_m
        assert items[2].altitude == 80.0

    def test_waypoint_uses_explicit_alt_when_set(self):
        wps = [Coordinate(latitude=51.3680, longitude=-0.2600, altitude=60.0)]
        items = build_mission(_mission(waypoints=wps))
        assert items[2].altitude == 60.0

    def test_altitude_zero_waypoint_uses_cruise_alt(self):
        """Silent logic hole: when coord.altitude == 0, the planner substitutes
        cruise_altitude_m because the condition is `if coord.altitude > 0`.

        This means a genuine sea-level waypoint (altitude=0) can never be
        expressed — it will silently become cruise altitude. This test documents
        the current behaviour so any future fix is intentional.
        """
        sea_level_wp = Coordinate(latitude=51.3680, longitude=-0.2600, altitude=0.0)
        items = build_mission(_mission(waypoints=[sea_level_wp]))
        # Current behaviour: altitude 0 is treated as "unset" and replaced
        assert items[2].altitude == 80.0  # cruise_altitude_m from _mission()


class TestWarningThreshold:
    """Tests for the 40% headwind-warning threshold.

    The 40% figure (rather than 50%) is a conservative safety margin.
    Rationale: headwinds on return can effectively halve range, so warning
    at 40% of max_range leaves a buffer. This is an engineering judgement
    call, not a physics-derived constant — document it here so future
    reviewers understand it is intentionally conservative, not arbitrary.
    """

    def test_waypoint_below_threshold_no_warning(self):
        """Waypoint at 39% of max_range should produce no warning."""
        # max_range=10 → threshold=4km. Need wp ~3.5km away.
        close_wp = Coordinate(latitude=51.3947, longitude=-0.2652)  # ~3.5km north
        warnings = validate(_mission(
            waypoints=[close_wp],
            max_range_km=10.0,
        ))
        assert len(warnings) == 0

    def test_waypoint_above_threshold_triggers_warning(self):
        """Waypoint beyond 40% of max_range triggers headwind warning."""
        # max_range=10 → threshold=4km. Need wp ~5km away but total < 10km.
        far_wp = Coordinate(latitude=51.4082, longitude=-0.2652)  # ~5km north
        warnings = validate(_mission(
            waypoints=[far_wp],
            max_range_km=11.0,
        ))
        assert any("beyond safe threshold" in w for w in warnings)
