"""Run the MPE Core Engine.

Usage:
    python -m mpe
    python -m mpe --adsb-center 26.0,56.5 --adsb-radius 250
    python -m mpe --cot-url tcp://takserver:8087
    python -m mpe --no-cot  (disable CoT output)
"""

from __future__ import annotations

import argparse
import asyncio

from mpe.engine import EngineConfig, run_engine


def main() -> None:
    """Parse arguments and launch the engine."""
    parser = argparse.ArgumentParser(
        description="MPE Core Engine -- Multi-Domain C2",
    )

    # ADS-B
    parser.add_argument(
        "--adsb-center",
        default="51.3632,-0.2652",
        help="ADS-B center lat,lon",
    )
    parser.add_argument(
        "--adsb-radius",
        type=int,
        default=250,
        help="ADS-B radius in nm",
    )
    parser.add_argument(
        "--adsb-interval",
        type=float,
        default=10.0,
        help="ADS-B poll interval seconds",
    )
    parser.add_argument(
        "--no-adsb",
        action="store_true",
        help="Disable ADS-B ingest",
    )

    # AIS
    parser.add_argument(
        "--ais-port",
        type=int,
        default=5050,
        help="AIS UDP port",
    )
    parser.add_argument(
        "--ais",
        action="store_true",
        help="Enable AIS ingest",
    )

    # CoT
    parser.add_argument(
        "--cot-url",
        default="udp+wo://239.2.3.1:6969",
        help="CoT output URL",
    )
    parser.add_argument(
        "--no-cot",
        action="store_true",
        help="Disable CoT output",
    )
    parser.add_argument(
        "--callsign",
        default="MPE-ENGINE",
        help="Engine callsign",
    )

    # Engine
    parser.add_argument(
        "--classify-interval",
        type=float,
        default=5.0,
        help="Classification interval seconds",
    )
    parser.add_argument(
        "--output-interval",
        type=float,
        default=5.0,
        help="CoT output interval seconds",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    args = parser.parse_args()

    # Parse center coordinates
    lat, lon = (float(x) for x in args.adsb_center.split(","))

    config = EngineConfig(
        adsb_enabled=not args.no_adsb,
        adsb_center_lat=lat,
        adsb_center_lon=lon,
        adsb_radius_nm=args.adsb_radius,
        adsb_poll_interval_s=args.adsb_interval,
        ais_enabled=args.ais,
        ais_udp_port=args.ais_port,
        cot_enabled=not args.no_cot,
        cot_url=args.cot_url,
        cot_callsign=args.callsign,
        classify_interval_s=args.classify_interval,
        output_interval_s=args.output_interval,
        log_level=args.log_level,
    )

    asyncio.run(run_engine(config))


if __name__ == "__main__":
    main()
