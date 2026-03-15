"""Mission planner — converts a BasicMission into a sequence of MissionItems.

Phase A: simple linear planner.
  HOME → TAKEOFF → WAYPOINT × N → RTL

Future phases add mission-type-specific planners (SAR grid, ISR route, etc.)

  ┌───────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐
  │ BasicMission│───▶│ validate  │───▶│ build_items   │───▶│ Mission  │
  │            │     │ (sanity)  │     │ (takeoff+wp  │     │ Items[]  │
  └───────────┘     └──────────┘     │  +RTL)        │     └──────────┘
                                      └──────────────┘
"""

from __future__ import annotations

import math

from .models import BasicMission, Coordinate, MAVCmd, MAVFrame, MissionItem


def _haversine_km(a: Coordinate, b: Coordinate) -> float:
    """Great-circle distance between two coordinates in kilometres."""
    R = 6371.0  # Earth radius in km
    lat1, lat2 = math.radians(a.latitude), math.radians(b.latitude)
    dlat = math.radians(b.latitude - a.latitude)
    dlon = math.radians(b.longitude - a.longitude)
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(h))


class ValidationError(Exception):
    """Raised when a mission fails sanity checks."""


def validate(mission: BasicMission) -> list[str]:
    """Run basic sanity checks. Returns list of warnings. Raises on hard failures.

    This is NOT the full constraint engine (Phase C). It catches the
    "will definitely crash or violate regulations" cases only.
    """
    warnings: list[str] = []

    # Check cruise altitude against CAA limit
    if mission.cruise_altitude_m > mission.max_altitude_m:
        raise ValidationError(
            f"Cruise altitude {mission.cruise_altitude_m}m exceeds max "
            f"{mission.max_altitude_m}m (UK CAA Open A3 limit is 120m AGL)"
        )

    # Check each waypoint altitude
    for i, wp in enumerate(mission.waypoints):
        if wp.altitude > 0 and wp.altitude > mission.max_altitude_m:
            raise ValidationError(
                f"Waypoint {i} altitude {wp.altitude}m exceeds max {mission.max_altitude_m}m"
            )

    # Check total route distance
    total_km = 0.0
    prev = mission.home
    for wp in mission.waypoints:
        leg = _haversine_km(prev, wp)
        total_km += leg
        prev = wp
    # Add return leg
    total_km += _haversine_km(prev, mission.home)

    if total_km > mission.max_range_km:
        raise ValidationError(
            f"Total route distance {total_km:.1f}km exceeds max range "
            f"{mission.max_range_km}km (including return to home)"
        )

    # Check individual waypoint distance from home — warn at 40% of max range
    # (not 50%, because headwind on return can effectively halve remaining range)
    warn_threshold = mission.max_range_km * 0.4
    for i, wp in enumerate(mission.waypoints):
        dist = _haversine_km(mission.home, wp)
        if dist > warn_threshold:
            warnings.append(
                f"Waypoint {i} is {dist:.1f}km from home — "
                f"beyond safe threshold ({warn_threshold:.1f}km). "
                f"Return may not be possible with headwind."
            )

    return warnings


def build_mission(mission: BasicMission) -> list[MissionItem]:
    """Convert a BasicMission into an ordered list of MissionItems.

    Output sequence:
      0: HOME (sets home position)
      1: TAKEOFF to cruise altitude
      2..N+1: WAYPOINT for each coordinate
      N+2: RTL (return to launch)
    """
    warnings = validate(mission)
    for w in warnings:
        # In Phase A, print warnings. Phase B+ should use proper logging.
        print(f"WARNING: {w}")

    items: list[MissionItem] = []
    seq = 0

    # Item 0: HOME position
    items.append(
        MissionItem(
            seq=seq,
            current=True,
            frame=MAVFrame.GLOBAL,
            command=MAVCmd.NAV_WAYPOINT,
            latitude=mission.home.latitude,
            longitude=mission.home.longitude,
            altitude=mission.home.altitude,
        )
    )
    seq += 1

    # Item 1: TAKEOFF
    items.append(
        MissionItem(
            seq=seq,
            command=MAVCmd.NAV_TAKEOFF,
            param1=mission.takeoff_pitch_deg,
            altitude=mission.cruise_altitude_m,
        )
    )
    seq += 1

    # Items 2..N+1: WAYPOINTS
    for coord in mission.waypoints:
        alt = coord.altitude if coord.altitude > 0 else mission.cruise_altitude_m
        items.append(
            MissionItem(
                seq=seq,
                command=MAVCmd.NAV_WAYPOINT,
                latitude=coord.latitude,
                longitude=coord.longitude,
                altitude=alt,
            )
        )
        seq += 1

    # Final item: RTL
    items.append(
        MissionItem(
            seq=seq,
            command=MAVCmd.NAV_RETURN_TO_LAUNCH,
        )
    )

    return items
