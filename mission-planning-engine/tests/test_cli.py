"""Tests for the CLI interface."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import patch

import pytest

from mpe.cli import _parse_coord, main
from mpe.upload import UploadError


class TestParseCoord:
    def test_lat_lon_only(self):
        coord = _parse_coord("51.3632,-0.2652")
        assert coord.latitude == 51.3632
        assert coord.longitude == -0.2652
        assert coord.altitude == 0.0

    def test_lat_lon_alt(self):
        coord = _parse_coord("51.3632,-0.2652,84.0")
        assert coord.latitude == 51.3632
        assert coord.longitude == -0.2652
        assert coord.altitude == 84.0

    def test_invalid_format_one_part(self):
        with pytest.raises(argparse.ArgumentTypeError, match="lat,lon"):
            _parse_coord("51.3632")

    def test_invalid_format_four_parts(self):
        with pytest.raises(argparse.ArgumentTypeError, match="lat,lon"):
            _parse_coord("51.3632,-0.2652,84.0,extra")

    def test_non_numeric_value(self):
        with pytest.raises(ValueError):
            _parse_coord("abc,-0.2652")


class TestCLI:
    def test_generates_file(self, tmp_path):
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652",
            "--waypoints", "51.3680,-0.2600",
            "--alt", "80",
            "-o", str(output),
        ])
        assert result == 0
        assert output.exists()
        content = output.read_text()
        assert content.startswith("QGC WPL 110")

    def test_multiple_waypoints(self, tmp_path):
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652",
            "--waypoints", "51.3680,-0.2600", "51.3720,-0.2550",
            "--alt", "50",
            "-o", str(output),
        ])
        assert result == 0
        lines = output.read_text().strip().split("\n")
        # Header + HOME + TAKEOFF + 2 WPs + RTL = 6
        assert len(lines) == 6

    def test_validation_failure_returns_1(self, tmp_path):
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652",
            "--waypoints", "51.3680,-0.2600",
            "--alt", "200",  # exceeds 120m CAA limit
            "-o", str(output),
        ])
        assert result == 1

    def test_coordinate_with_altitude(self, tmp_path):
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652,84",
            "--waypoints", "51.3680,-0.2600,60",
            "-o", str(output),
        ])
        assert result == 0

    def test_altitude_exactly_at_caa_limit(self, tmp_path):
        """Altitude == max_altitude_m (120) should pass validation."""
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652",
            "--waypoints", "51.3680,-0.2600",
            "--alt", "120",
            "-o", str(output),
        ])
        assert result == 0

    def test_altitude_just_above_caa_limit_returns_1(self, tmp_path):
        """Altitude 121m exceeds the 120m CAA limit — should fail."""
        output = tmp_path / "test.waypoints"
        result = main([
            "--home", "51.3632,-0.2652",
            "--waypoints", "51.3680,-0.2600",
            "--alt", "121",
            "-o", str(output),
        ])
        assert result == 1

    def test_upload_flag_connection_refused_returns_1(self, tmp_path):
        """--upload with no SITL running should return exit code 1."""
        output = tmp_path / "test.waypoints"
        with patch("mpe.cli.upload_mission", side_effect=UploadError("Connection refused")):
            result = main([
                "--home", "51.3632,-0.2652",
                "--waypoints", "51.3680,-0.2600",
                "--alt", "50",
                "-o", str(output),
                "--upload",
            ])
        assert result == 1

    def test_upload_success_returns_0(self, tmp_path):
        """--upload with mocked successful upload should return 0."""
        output = tmp_path / "test.waypoints"
        with patch("mpe.cli.upload_mission"):
            result = main([
                "--home", "51.3632,-0.2652",
                "--waypoints", "51.3680,-0.2600",
                "--alt", "50",
                "-o", str(output),
                "--upload",
            ])
        assert result == 0
