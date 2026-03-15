"""Manual SITL flight test — upload a mission and watch it fly.

Prerequisites:
    1. Start SITL: sim_vehicle.py -v ArduPlane --map --console
    2. Wait for GPS lock (messages will show in console)
    3. Run this script

Usage:
    python sitl/fly_mission.py                    # uses default triangle mission
    python sitl/fly_mission.py mission.waypoints  # uses a specific file
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mpe.models import BasicMission, Coordinate
from mpe.planner import build_mission
from mpe.upload import upload_mission, UploadError


def default_mission() -> list:
    """A simple triangle near Epsom for SITL testing."""
    mission = BasicMission(
        home=Coordinate(latitude=51.3632, longitude=-0.2652, altitude=84.0),
        waypoints=[
            Coordinate(latitude=51.3680, longitude=-0.2600),
            Coordinate(latitude=51.3720, longitude=-0.2550),
            Coordinate(latitude=51.3650, longitude=-0.2500),
        ],
        cruise_altitude_m=80.0,
    )
    return build_mission(mission)


def main():
    print("=== SITL Flight Test ===\n")

    items = default_mission()
    print(f"Mission: {len(items)} items (HOME + TAKEOFF + {len(items) - 3} WPs + RTL)\n")

    # MAVProxy occupies tcp:5760, so connect to the forwarded UDP port
    connection = "udp:127.0.0.1:14550"
    try:
        upload_mission(items, connection_string=connection)
    except UploadError as e:
        print(f"\nFailed: {e}")
        print("\nMake sure SITL is running:")
        print("  sim_vehicle.py -v ArduPlane --map --console")
        return 1

    print("\n--- Mission uploaded ---")
    print("To fly the mission in SITL:")
    print("  1. In MAVProxy console: 'mode auto'")
    print("  2. Then: 'arm throttle'")
    print("  3. Watch the map — the aircraft will fly the waypoints and RTL")
    print("\nOr use QGroundControl/Mission Planner to arm and start the mission.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
