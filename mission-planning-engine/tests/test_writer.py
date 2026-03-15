"""Tests for the waypoint file writer."""

from pathlib import Path

import pytest

from mpe.models import BasicMission, Coordinate
from mpe.planner import build_mission
from mpe.writer import format_item, to_string, write_waypoints


FIXTURES = Path(__file__).parent / "fixtures"

EPSOM_HOME = Coordinate(latitude=51.3632000, longitude=-0.2652000, altitude=84.0)


def _build(waypoints, alt=80.0):
    mission = BasicMission(home=EPSOM_HOME, waypoints=waypoints, cruise_altitude_m=alt)
    return build_mission(mission)


class TestFormatItem:
    def test_tab_separated(self):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        line = format_item(items[0])
        assert "\t" in line
        assert len(line.split("\t")) == 12

    def test_float_precision_lat_lon(self):
        """Latitude and longitude should have 7 decimal places."""
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        line = format_item(items[0])
        parts = line.split("\t")
        assert "51.3632000" in parts[8]
        assert "-0.2652000" in parts[9]

    def test_float_precision_alt(self):
        """Altitude should have 6 decimal places."""
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        line = format_item(items[1])  # TAKEOFF
        parts = line.split("\t")
        assert "80.000000" in parts[10]


class TestToString:
    def test_starts_with_header(self):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        output = to_string(items)
        assert output.startswith("QGC WPL 110\n")

    def test_correct_line_count(self):
        wps = [
            Coordinate(latitude=51.3680, longitude=-0.2600),
            Coordinate(latitude=51.3720, longitude=-0.2550),
        ]
        items = _build(wps)
        output = to_string(items)
        lines = output.strip().split("\n")
        # Header + HOME + TAKEOFF + 2 WPs + RTL = 6 lines
        assert len(lines) == 6

    def test_ends_with_newline(self):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        output = to_string(items)
        assert output.endswith("\n")


class TestWriteWaypoints:
    def test_writes_file(self, tmp_path):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        path = write_waypoints(items, tmp_path / "test.waypoints")
        assert path.exists()
        content = path.read_text()
        assert content.startswith("QGC WPL 110\n")

    def test_roundtrip_string_matches_file(self, tmp_path):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        path = write_waypoints(items, tmp_path / "test.waypoints")
        from_file = path.read_text()
        from_string = to_string(items)
        assert from_file == from_string


class TestGoldenFiles:
    """Compare writer output against verified fixture files.

    To regenerate fixtures after intentional format changes:
        pytest tests/test_writer.py --update-fixtures
    """

    def test_single_waypoint(self):
        fixture = FIXTURES / "single_waypoint.waypoints"
        if not fixture.exists():
            pytest.skip("Fixture not generated yet — run: python -m tests.generate_fixtures")
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)], alt=50.0)
        assert to_string(items) == fixture.read_text()

    def test_simple_triangle(self):
        fixture = FIXTURES / "simple_triangle.waypoints"
        if not fixture.exists():
            pytest.skip("Fixture not generated yet — run: python -m tests.generate_fixtures")
        wps = [
            Coordinate(latitude=51.3680, longitude=-0.2600),
            Coordinate(latitude=51.3720, longitude=-0.2550),
            Coordinate(latitude=51.3650, longitude=-0.2500),
        ]
        items = _build(wps, alt=80.0)
        assert to_string(items) == fixture.read_text()
