"""Tests for the MAVLink task translator."""

from __future__ import annotations

import pytest
from types import SimpleNamespace

from mpe.models import MAVCmd
from mpe.task_translator import MAVLinkTranslator, TranslationError


# ---------------------------------------------------------------------------
# Helpers -- build duck-typed C2 objects without importing c2_models
# ---------------------------------------------------------------------------


def _pos(lat: float = 51.0, lon: float = -0.3, alt: float = 0.0):
    return SimpleNamespace(
        latitude=lat, longitude=lon, altitude_m=alt, heading=0.0, speed_mps=0.0
    )


def _wp(lat: float = 51.0, lon: float = -0.3, alt: float | None = None, name: str = ""):
    return SimpleNamespace(
        position=_pos(lat, lon),
        name=name,
        altitude_m=alt,
        speed_mps=None,
        loiter_seconds=0.0,
        radius_m=0.0,
    )


def _task(
    task_type: str = "goto",
    waypoints=None,
    area_of_interest=None,
    max_altitude_m: float = 120.0,
):
    return SimpleNamespace(
        task_id="TSK-0001",
        task_type=task_type,
        waypoints=waypoints or [],
        area_of_interest=area_of_interest,
        max_altitude_m=max_altitude_m,
    )


def _plan(
    tasks=None,
    home=None,
    default_alt: float = 50.0,
):
    return SimpleNamespace(
        home_position=home,
        default_altitude_m=default_alt,
        tasks=tasks or [],
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestTranslatePlan:
    """Tests for MAVLinkTranslator.translate_plan."""

    def test_simple_goto_produces_mission_items(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[_wp(51.01, -0.29)])
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        items, warnings = translator.translate_plan(plan)

        # HOME + TAKEOFF + 1 WP + RTL = 4 items
        assert len(items) == 4
        assert all(hasattr(item, "seq") for item in items)

    def test_no_home_position_raises_translation_error(self):
        task = _task("goto", waypoints=[_wp(51.01, -0.29)])
        plan = _plan(tasks=[task], home=None)

        translator = MAVLinkTranslator()
        with pytest.raises(TranslationError, match="home_position"):
            translator.translate_plan(plan)

    def test_no_waypoints_raises_translation_error(self):
        home = _pos(51.0, -0.3, 0.0)
        # Task type "track" has no waypoint extraction logic
        task = _task("track", waypoints=[])
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        with pytest.raises(TranslationError, match="No translatable waypoints"):
            translator.translate_plan(plan)

    def test_patrol_with_area_of_interest(self):
        home = _pos(51.0, -0.3, 0.0)
        corners = [
            _pos(51.01, -0.31),
            _pos(51.01, -0.29),
            _pos(51.02, -0.29),
            _pos(51.02, -0.31),
        ]
        task = _task("patrol", area_of_interest=corners)
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # HOME + TAKEOFF + 4 corners + RTL = 7 items
        assert len(items) == 7

    def test_preserves_waypoint_altitude(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[_wp(51.01, -0.29, alt=80.0)])
        plan = _plan(tasks=[task], home=home, default_alt=50.0)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # The waypoint item is at index 2 (HOME=0, TAKEOFF=1, WP=2, RTL=3)
        wp_item = items[2]
        assert wp_item.altitude == 80.0

    def test_uses_default_altitude_when_waypoint_is_none(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[_wp(51.01, -0.29, alt=None)])
        plan = _plan(tasks=[task], home=home, default_alt=60.0)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # Waypoint at index 2 should use default altitude (60m)
        # The planner uses cruise_altitude_m when coord.altitude == 0
        wp_item = items[2]
        assert wp_item.altitude == 60.0

    def test_sequence_numbers_are_correct(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[
            _wp(51.01, -0.29, alt=50.0),
            _wp(51.02, -0.28, alt=50.0),
        ])
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        for i, item in enumerate(items):
            assert item.seq == i, f"Item {i} has seq={item.seq}"

    def test_first_item_is_home_last_is_rtl(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[_wp(51.01, -0.29, alt=50.0)])
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # First item: HOME (NAV_WAYPOINT at seq 0 with current=True)
        assert items[0].seq == 0
        assert items[0].current is True
        assert items[0].latitude == 51.0
        assert items[0].longitude == -0.3

        # Last item: RTL
        assert items[-1].command == MAVCmd.NAV_RETURN_TO_LAUNCH

    def test_multiple_tasks_combine_waypoints(self):
        home = _pos(51.0, -0.3, 0.0)
        t1 = _task("goto", waypoints=[_wp(51.01, -0.29, alt=50.0)])
        t2 = _task("survey", waypoints=[
            _wp(51.02, -0.28, alt=50.0),
            _wp(51.03, -0.27, alt=50.0),
        ])
        plan = _plan(tasks=[t1, t2], home=home)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # HOME + TAKEOFF + 3 WPs + RTL = 6
        assert len(items) == 6

    def test_loiter_task_single_waypoint(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("loiter", waypoints=[_wp(51.01, -0.29, alt=70.0)])
        plan = _plan(tasks=[task], home=home)

        translator = MAVLinkTranslator()
        items, _ = translator.translate_plan(plan)

        # HOME + TAKEOFF + 1 loiter point + RTL = 4
        assert len(items) == 4


class TestTranslateTask:
    """Tests for MAVLinkTranslator.translate_task convenience method."""

    def test_translate_single_task(self):
        home = _pos(51.0, -0.3, 0.0)
        task = _task("goto", waypoints=[_wp(51.01, -0.29, alt=50.0)])

        translator = MAVLinkTranslator()
        items = translator.translate_task(task, home, default_altitude_m=50.0)

        assert len(items) == 4
        assert items[0].seq == 0
        assert items[-1].command == MAVCmd.NAV_RETURN_TO_LAUNCH
