"""Core data models for mission planning.

Phase A: minimal models — MissionItem + BasicMission.
Full Goal/ConstraintSet hierarchy deferred to Phase B.
"""

from __future__ import annotations

from enum import IntEnum
from pydantic import BaseModel, field_validator


class MAVFrame(IntEnum):
    """MAVLink coordinate frame types used in mission items."""

    GLOBAL = 0
    GLOBAL_RELATIVE_ALT = 3  # Altitude relative to home — most common
    GLOBAL_TERRAIN_ALT = 10  # Altitude above terrain (needs SRTM data)


class MAVCmd(IntEnum):
    """MAVLink command IDs used in ArduPlane missions.

    Only commands needed for Phase A are included.
    Extend as mission types are added in Phase B+.
    """

    NAV_WAYPOINT = 16
    NAV_LOITER_UNLIM = 17
    NAV_LOITER_TURNS = 18
    NAV_LOITER_TIME = 19
    NAV_RETURN_TO_LAUNCH = 20
    NAV_LAND = 21
    NAV_TAKEOFF = 22
    DO_SET_SERVO = 183


class MissionItem(BaseModel):
    """A single MAVLink mission item — maps directly to one line in a .waypoints file.

    QGC WPL 110 format:
    seq  current  frame  command  p1  p2  p3  p4  lat  lon  alt  autocontinue
    """

    seq: int
    current: bool = False
    frame: MAVFrame = MAVFrame.GLOBAL_RELATIVE_ALT
    command: MAVCmd
    param1: float = 0.0
    param2: float = 0.0
    param3: float = 0.0
    param4: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    altitude: float = 0.0
    autocontinue: bool = True

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if v != 0.0 and not (-90 <= v <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if v != 0.0 and not (-180 <= v <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return v

    @field_validator("altitude")
    @classmethod
    def validate_altitude(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"Altitude must be non-negative, got {v}")
        return v


class Coordinate(BaseModel):
    """A GPS coordinate with altitude."""

    latitude: float
    longitude: float
    altitude: float = 0.0

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90 <= v <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180 <= v <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return v


class BasicMission(BaseModel):
    """A simple mission: home position + ordered waypoints + cruise altitude.

    Phase A model — no Goal/ConstraintSet hierarchy yet.
    The planner converts this into a list of MissionItems.
    """

    home: Coordinate
    waypoints: list[Coordinate]
    cruise_altitude_m: float = 50.0
    takeoff_pitch_deg: float = 15.0
    max_altitude_m: float = 120.0  # UK CAA Open A3 limit
    max_range_km: float = 30.0  # Conservative default for Skywalker X8

    @field_validator("cruise_altitude_m")
    @classmethod
    def validate_cruise_altitude(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"Cruise altitude must be positive, got {v}")
        return v

    @field_validator("waypoints")
    @classmethod
    def validate_waypoints_not_empty(cls, v: list[Coordinate]) -> list[Coordinate]:
        if len(v) == 0:
            raise ValueError("Mission must have at least one waypoint")
        return v
