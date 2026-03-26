"""Tests for the waypoint file writer."""

from pathlib import Path

import pytest

from mpe.models import BasicMission, Coordinate, MAVCmd, MAVFrame, MissionItem
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

    def test_lat_exactly_7_decimal_places(self):
        """Verify latitude field has exactly 7 decimal digits, not more or fewer."""
        item = MissionItem(
            seq=0, command=MAVCmd.NAV_WAYPOINT,
            latitude=51.1, longitude=-0.2, altitude=50.0,
        )
        line = format_item(item)
        lat_field = line.split("\t")[8]
        # Should be "51.1000000" — 7 digits after the decimal point
        decimal_part = lat_field.split(".")[1]
        assert len(decimal_part) == 7

    def test_lon_exactly_7_decimal_places(self):
        """Verify longitude field has exactly 7 decimal digits."""
        item = MissionItem(
            seq=0, command=MAVCmd.NAV_WAYPOINT,
            latitude=51.1, longitude=-0.123456789, altitude=50.0,
        )
        line = format_item(item)
        lon_field = line.split("\t")[9]
        # Strip leading minus sign for the decimal-place check
        decimal_part = lon_field.lstrip("-").split(".")[1]
        assert len(decimal_part) == 7

    def test_alt_exactly_6_decimal_places(self):
        """Verify altitude field has exactly 6 decimal digits."""
        item = MissionItem(
            seq=0, command=MAVCmd.NAV_WAYPOINT,
            latitude=51.1, longitude=-0.2, altitude=84.123,
        )
        line = format_item(item)
        alt_field = line.split("\t")[10]
        decimal_part = alt_field.split(".")[1]
        assert len(decimal_part) == 6

    def test_negative_longitude_preserved(self):
        """Negative longitude should appear with a minus sign in output."""
        item = MissionItem(
            seq=0, command=MAVCmd.NAV_WAYPOINT,
            latitude=51.3632, longitude=-0.2652, altitude=50.0,
        )
        line = format_item(item)
        lon_field = line.split("\t")[9]
        assert lon_field.startswith("-")
        assert "-0.2652000" == lon_field

    def test_format_item_field_order(self):
        """Verify the 12 fields appear in the correct QGC WPL 110 order."""
        item = MissionItem(
            seq=5, current=True, frame=MAVFrame.GLOBAL,
            command=MAVCmd.NAV_WAYPOINT,
            param1=1.0, param2=2.0, param3=3.0, param4=4.0,
            latitude=51.3632, longitude=-0.2652, altitude=84.0,
            autocontinue=False,
        )
        line = format_item(item)
        parts = line.split("\t")
        assert parts[0] == "5"          # seq
        assert parts[1] == "1"          # current
        assert parts[2] == "0"          # frame (GLOBAL=0)
        assert parts[3] == "16"         # command (NAV_WAYPOINT=16)
        assert parts[4] == "1.000000"   # param1
        assert parts[5] == "2.000000"   # param2
        assert parts[6] == "3.000000"   # param3
        assert parts[7] == "4.000000"   # param4
        assert parts[8] == "51.3632000" # latitude
        assert parts[9] == "-0.2652000" # longitude
        assert parts[10] == "84.000000" # altitude
        assert parts[11] == "0"         # autocontinue


class TestToString:
    def test_starts_with_header(self):
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        output = to_string(items)
        assert output.startswith("QGC WPL 110\n")

    def test_header_is_exactly_qgc_wpl_110(self):
        """Header line must be exactly 'QGC WPL 110' with no trailing whitespace."""
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        output = to_string(items)
        header_line = output.split("\n")[0]
        assert header_line == "QGC WPL 110"

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

    def test_file_ends_with_exactly_one_newline(self):
        """Output should end with exactly one newline, not two."""
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        output = to_string(items)
        assert output.endswith("\n")
        assert not output.endswith("\n\n")


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

    def test_file_written_as_utf8(self, tmp_path):
        """Verify the waypoint file is written with UTF-8 encoding."""
        items = _build([Coordinate(latitude=51.3680, longitude=-0.2600)])
        path = write_waypoints(items, tmp_path / "test.waypoints")
        # Read back with explicit UTF-8 — should not raise
        content = path.read_text(encoding="utf-8")
        assert content.startswith("QGC WPL 110")


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
