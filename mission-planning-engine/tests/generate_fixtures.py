"""Generate golden fixture files for writer tests.

Run this once to create the initial fixtures, then verify them
by loading into Mission Planner or QGroundControl.

Usage:
    python -m tests.generate_fixtures
"""

from pathlib import Path

from mpe.models import BasicMission, Coordinate
from mpe.planner import build_mission
from mpe.writer import write_waypoints

FIXTURES = Path(__file__).parent / "fixtures"
EPSOM_HOME = Coordinate(latitude=51.3632000, longitude=-0.2652000, altitude=84.0)


def generate():
    FIXTURES.mkdir(exist_ok=True)

    # 1. Single waypoint
    mission = BasicMission(
        home=EPSOM_HOME,
        waypoints=[Coordinate(latitude=51.3680, longitude=-0.2600)],
        cruise_altitude_m=50.0,
    )
    items = build_mission(mission)
    path = write_waypoints(items, FIXTURES / "single_waypoint.waypoints")
    print(f"Generated: {path}")

    # 2. Simple triangle
    mission = BasicMission(
        home=EPSOM_HOME,
        waypoints=[
            Coordinate(latitude=51.3680, longitude=-0.2600),
            Coordinate(latitude=51.3720, longitude=-0.2550),
            Coordinate(latitude=51.3650, longitude=-0.2500),
        ],
        cruise_altitude_m=80.0,
    )
    items = build_mission(mission)
    path = write_waypoints(items, FIXTURES / "simple_triangle.waypoints")
    print(f"Generated: {path}")

    # 3. Long route (20 waypoints in a line heading north)
    waypoints = []
    for i in range(20):
        waypoints.append(
            Coordinate(
                latitude=51.3632 + (i + 1) * 0.001,  # ~111m per 0.001 deg
                longitude=-0.2652,
            )
        )
    mission = BasicMission(
        home=EPSOM_HOME,
        waypoints=waypoints,
        cruise_altitude_m=100.0,
    )
    items = build_mission(mission)
    path = write_waypoints(items, FIXTURES / "long_route.waypoints")
    print(f"Generated: {path}")

    print(f"\nDone. Verify fixtures by loading into Mission Planner or QGroundControl.")


if __name__ == "__main__":
    generate()
