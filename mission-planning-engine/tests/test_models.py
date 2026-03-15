"""Tests for mission data models."""

import pytest
from pydantic import ValidationError

from mpe.models import BasicMission, Coordinate, MAVCmd, MAVFrame, MissionItem


class TestCoordinate:
    def test_valid_coordinate(self):
        c = Coordinate(latitude=51.3632, longitude=-0.2652)
        assert c.latitude == 51.3632
        assert c.longitude == -0.2652
        assert c.altitude == 0.0

    def test_coordinate_with_altitude(self):
        c = Coordinate(latitude=51.3632, longitude=-0.2652, altitude=84.0)
        assert c.altitude == 84.0

    def test_latitude_out_of_range(self):
        with pytest.raises(ValidationError, match="Latitude"):
            Coordinate(latitude=91.0, longitude=0.0)

    def test_latitude_negative_boundary(self):
        c = Coordinate(latitude=-90.0, longitude=0.0)
        assert c.latitude == -90.0

    def test_longitude_out_of_range(self):
        with pytest.raises(ValidationError, match="Longitude"):
            Coordinate(latitude=0.0, longitude=181.0)

    def test_negative_longitude(self):
        c = Coordinate(latitude=51.0, longitude=-0.2652)
        assert c.longitude == -0.2652


class TestMissionItem:
    def test_valid_waypoint(self):
        item = MissionItem(
            seq=0,
            command=MAVCmd.NAV_WAYPOINT,
            latitude=51.3632,
            longitude=-0.2652,
            altitude=50.0,
        )
        assert item.frame == MAVFrame.GLOBAL_RELATIVE_ALT
        assert item.autocontinue is True

    def test_takeoff_item(self):
        item = MissionItem(
            seq=1,
            command=MAVCmd.NAV_TAKEOFF,
            param1=15.0,
            altitude=50.0,
        )
        assert item.command == MAVCmd.NAV_TAKEOFF
        assert item.param1 == 15.0

    def test_negative_altitude_rejected(self):
        with pytest.raises(ValidationError, match="Altitude"):
            MissionItem(seq=0, command=MAVCmd.NAV_WAYPOINT, altitude=-10.0)

    def test_invalid_latitude_rejected(self):
        with pytest.raises(ValidationError, match="Latitude"):
            MissionItem(
                seq=0, command=MAVCmd.NAV_WAYPOINT, latitude=100.0, longitude=0.0
            )

    def test_zero_lat_lon_allowed(self):
        """Zero lat/lon is valid (used for commands like RTL that don't need coords)."""
        item = MissionItem(seq=0, command=MAVCmd.NAV_RETURN_TO_LAUNCH)
        assert item.latitude == 0.0
        assert item.longitude == 0.0


class TestBasicMission:
    def _home(self):
        return Coordinate(latitude=51.3632, longitude=-0.2652)

    def _waypoints(self):
        return [
            Coordinate(latitude=51.3680, longitude=-0.2600),
            Coordinate(latitude=51.3720, longitude=-0.2550),
        ]

    def test_valid_mission(self):
        m = BasicMission(
            home=self._home(),
            waypoints=self._waypoints(),
            cruise_altitude_m=80.0,
        )
        assert len(m.waypoints) == 2
        assert m.cruise_altitude_m == 80.0

    def test_empty_waypoints_rejected(self):
        with pytest.raises(ValidationError, match="at least one waypoint"):
            BasicMission(home=self._home(), waypoints=[])

    def test_negative_altitude_rejected(self):
        with pytest.raises(ValidationError, match="Cruise altitude must be positive"):
            BasicMission(
                home=self._home(), waypoints=self._waypoints(), cruise_altitude_m=-10.0
            )

    def test_default_max_altitude(self):
        m = BasicMission(home=self._home(), waypoints=self._waypoints())
        assert m.max_altitude_m == 120.0  # UK CAA limit

    def test_default_max_range(self):
        m = BasicMission(home=self._home(), waypoints=self._waypoints())
        assert m.max_range_km == 30.0
