"""Command-line interface for the Mission Planning Engine.

Usage:
    # Generate a waypoint file
    mpe --home 51.3632,-0.2652 --waypoints 51.3680,-0.2600 51.3720,-0.2550 --alt 80 -o mission.waypoints

    # Generate and upload to SITL
    mpe --home 51.3632,-0.2652 --waypoints 51.3680,-0.2600 --alt 80 --upload

    # Upload an existing waypoint file
    mpe --upload --file mission.waypoints
"""

from __future__ import annotations

import argparse
import sys

from .models import BasicMission, Coordinate
from .planner import ValidationError, build_mission
from .writers import QGCWPLWriter, CoTWriter
from .upload import upload_mission, UploadError


def _parse_coord(s: str) -> Coordinate:
    """Parse 'lat,lon' or 'lat,lon,alt' into a Coordinate."""
    parts = s.split(",")
    if len(parts) == 2:
        return Coordinate(latitude=float(parts[0]), longitude=float(parts[1]))
    elif len(parts) == 3:
        return Coordinate(
            latitude=float(parts[0]),
            longitude=float(parts[1]),
            altitude=float(parts[2]),
        )
    else:
        raise argparse.ArgumentTypeError(
            f"Coordinate must be 'lat,lon' or 'lat,lon,alt', got '{s}'"
        )


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments, build a mission, write waypoints, and optionally upload."""
    parser = argparse.ArgumentParser(
        description="Mission Planning Engine — generate ArduPilot waypoint files",
    )
    parser.add_argument(
        "--home",
        type=_parse_coord,
        required=True,
        help="Home/launch position as lat,lon or lat,lon,alt",
    )
    parser.add_argument(
        "--waypoints",
        type=_parse_coord,
        nargs="+",
        required=True,
        help="Waypoint coordinates as lat,lon or lat,lon,alt (space-separated)",
    )
    parser.add_argument(
        "--alt",
        type=float,
        default=50.0,
        help="Cruise altitude in meters AGL (default: 50)",
    )
    parser.add_argument(
        "--max-range",
        type=float,
        default=30.0,
        help="Maximum range in km for sanity check (default: 30)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="mission.waypoints",
        help="Output file path (default: mission.waypoints)",
    )
    parser.add_argument(
        "--format",
        choices=["qgc-wpl", "cot"],
        default="qgc-wpl",
        help="Output format (default: qgc-wpl)",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload mission to ArduPilot (SITL or vehicle) after generating",
    )
    parser.add_argument(
        "--connection",
        default="tcp:127.0.0.1:5760",
        help="MAVLink connection string (default: tcp:127.0.0.1:5760 for SITL)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream CoT events live to a TAK network (requires --format cot)",
    )
    parser.add_argument(
        "--cot-url",
        default="udp+wo://239.2.3.1:6969",
        help="TAK endpoint URL (default: udp+wo://239.2.3.1:6969)",
    )
    parser.add_argument(
        "--callsign",
        default="MPE-DRONE",
        help="Drone callsign for CoT events (default: MPE-DRONE)",
    )

    args = parser.parse_args(argv)

    # Build mission
    mission = BasicMission(
        home=args.home,
        waypoints=args.waypoints,
        cruise_altitude_m=args.alt,
        max_range_km=args.max_range,
    )

    # Plan (validate + generate items)
    try:
        items = build_mission(mission)
    except ValidationError as e:
        print(f"MISSION REJECTED: {e}", file=sys.stderr)
        return 1

    # Select writer based on format
    if args.format == "qgc-wpl":
        writer = QGCWPLWriter()
    elif args.format == "cot":
        writer = CoTWriter()
    else:
        print(f"Format '{args.format}' is not yet supported.", file=sys.stderr)
        return 1

    # Write waypoint file
    path = writer.write(items, args.output)
    print(f"Waypoint file written: {path} ({len(items)} items)")

    # Print mission summary
    print(f"  Home: {mission.home.latitude:.7f}, {mission.home.longitude:.7f}")
    print(f"  Waypoints: {len(mission.waypoints)}")
    print(f"  Altitude: {mission.cruise_altitude_m}m AGL")

    # Optional: upload to vehicle
    if args.upload:
        try:
            upload_mission(items, args.connection)
        except UploadError as e:
            print(f"UPLOAD FAILED: {e}", file=sys.stderr)
            return 1

    # Optional: live CoT streaming
    if args.stream:
        if args.format != "cot":
            print("--stream requires --format cot", file=sys.stderr)
            return 1

        try:
            from .cot_sender import CoTStreamer, StreamError
        except StreamError as e:
            print(f"STREAM FAILED: {e}", file=sys.stderr)
            return 1

        try:
            streamer = CoTStreamer(
                cot_url=args.cot_url,
                callsign=args.callsign,
            )
            print(f"Publishing {len(items)} waypoints to {args.cot_url}...")
            streamer.publish_mission(items)

            # Start position reporting from home position
            home_lat = mission.home.latitude
            home_lon = mission.home.longitude
            home_alt = mission.cruise_altitude_m
            print(
                f"Starting position reporting from home "
                f"({home_lat:.6f}, {home_lon:.6f}, {home_alt:.1f}m)"
            )
            print("Press Ctrl+C to stop.")
            streamer.start_position_reporting(home_lat, home_lon, home_alt)

            # Block until interrupted
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping streamer...")
                streamer.stop()
                print("Stopped.")
        except StreamError as e:
            print(f"STREAM FAILED: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
