"""Tests for the CLI interface."""

from pathlib import Path

from mpe.cli import main


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
