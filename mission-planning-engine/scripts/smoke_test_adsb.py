#!/usr/bin/env python3
"""Live ADS-B end-to-end smoke test.

Tests the full async pipeline against real airplanes.live data:
  ingest → TrackManager → classify → geofence → predict → alert → CoT output

No TAK Server required -- CoT output is captured in-memory and validated.

Usage:
    cd mission-planning-engine
    source .venv/bin/activate
    PYTHONPATH=src python scripts/smoke_test_adsb.py
    PYTHONPATH=src python scripts/smoke_test_adsb.py --center 26.0,56.5 --radius 150
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from typing import Any


PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"

_results: list[tuple[str, str, str]] = []


def _report(status: str, name: str, detail: str = "") -> None:
    _results.append((status, name, detail))
    icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–"}.get(status, "?")
    print(f"  {icon} [{status}] {name}", f"  ({detail})" if detail else "")


async def smoke_test(center_lat: float, center_lon: float, radius_nm: int) -> int:
    print(f"\nADS-B smoke test: center=({center_lat}, {center_lon}) radius={radius_nm}nm")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Import all pipeline components
    # ------------------------------------------------------------------
    print("\n--- Imports ---")
    try:
        from mpe.engine import CoreEngine, EngineConfig
        from mpe.ingest import AircraftTracker, ADSBReceiver
        from mpe.intelligence import (
            TrackManager, Observation, EntityClassifier,
            AlertEngine, GeofenceManager, GeofenceZone, TrajectoryPredictor,
        )
        from mpe.output import ADSBCoTBridge, CoTOutput
        _report(PASS, "All sub-package imports")
    except ImportError as exc:
        _report(FAIL, "imports", str(exc))
        return 1

    # ------------------------------------------------------------------
    # 2. Fetch live ADS-B data
    # ------------------------------------------------------------------
    print("\n--- Live ADS-B fetch ---")
    tracker = AircraftTracker()
    try:
        receiver = ADSBReceiver(
            tracker,
            center_lat=center_lat,
            center_lon=center_lon,
            radius_nm=radius_nm,
            poll_interval_s=999,  # Single fetch only
            source="airplanes_live",
        )
        # Directly call the internal fetch method once
        receiver.fetch_once()
        aircraft_count = len(tracker.active_tracks)
        _report(PASS, f"ADS-B fetch returned {aircraft_count} aircraft")
    except Exception as exc:
        _report(FAIL, "ADS-B fetch", str(exc))
        return 1

    if aircraft_count == 0:
        _report(SKIP, "No aircraft in range -- skipping pipeline checks")
        print("\nTry a larger radius or a busier center point (e.g. --center 51.47,-0.46)")
        return 0

    # ------------------------------------------------------------------
    # 3. TrackManager fusion
    # ------------------------------------------------------------------
    print("\n--- TrackManager fusion ---")
    try:
        tm = TrackManager()
        for track in tracker.active_tracks:
            obs = Observation(
                source="adsb",
                source_id=track.icao_hex,
                latitude=track.latitude,
                longitude=track.longitude,
                altitude_m=track.altitude_m,
                heading=track.heading,
                speed_mps=track.speed_mps,
                callsign=track.callsign or "",
                domain="air",
            )
            tm.process_observation(obs)
        stats = tm.stats
        _report(PASS, f"TrackManager: {stats['active_entities']} entities from {aircraft_count} observations")
    except Exception as exc:
        _report(FAIL, "TrackManager fusion", str(exc))

    # ------------------------------------------------------------------
    # 4. Classification
    # ------------------------------------------------------------------
    print("\n--- Classifier ---")
    try:
        classifier = EntityClassifier()
        classifications = []
        for track in tracker.active_tracks:
            cls = classifier.classify_aircraft(track)
            classifications.append(cls)

        affiliations = {}
        for cls in classifications:
            affiliations[cls.affiliation] = affiliations.get(cls.affiliation, 0) + 1

        threat_count = sum(1 for cls in classifications if cls.threat_level >= 4)
        _report(PASS, f"Classified {len(classifications)} aircraft: {affiliations}")
        if threat_count:
            _report(PASS, f"{threat_count} aircraft flagged threat_level >= 4")
        else:
            _report(PASS, "No elevated threats (expected for civilian airspace)")
    except Exception as exc:
        _report(FAIL, "Classification", str(exc))

    # ------------------------------------------------------------------
    # 5. Geofence check
    # ------------------------------------------------------------------
    print("\n--- Geofence ---")
    try:
        from mpe.intelligence import DEMO_ZONES
        gfm = GeofenceManager()
        for zone in DEMO_ZONES:
            gfm.add_zone(zone)

        # Also add a test alert zone around the center point
        gfm.add_zone(GeofenceZone(
            name="SMOKE_TEST_ZONE",
            zone_type="alert",
            polygon=[
                (center_lat - 2.0, center_lon - 2.0),
                (center_lat + 2.0, center_lon - 2.0),
                (center_lat + 2.0, center_lon + 2.0),
                (center_lat - 2.0, center_lon + 2.0),
            ],
            priority=5,
        ))

        all_violations = []
        for track in tracker.active_tracks:
            if track.latitude == 0.0 and track.longitude == 0.0:
                continue
            violations = gfm.check(
                entity_id=f"ADSB-{track.icao_hex}",
                lat=track.latitude,
                lon=track.longitude,
                domain="air",
            )
            all_violations.extend(violations)

        smoke_violations = [v for v in all_violations if v.zone_name == "SMOKE_TEST_ZONE"]
        _report(PASS, f"Geofence: {len(all_violations)} total violations, {len(smoke_violations)} in smoke_test_zone")
    except Exception as exc:
        _report(FAIL, "Geofence check", str(exc))

    # ------------------------------------------------------------------
    # 6. Trajectory prediction
    # ------------------------------------------------------------------
    print("\n--- Trajectory prediction ---")
    try:
        predictor = TrajectoryPredictor()
        moving = [t for t in tracker.active_tracks if t.speed_mps >= 1.0]
        predictions_with_entry = 0

        for track in moving[:20]:  # Check first 20 moving aircraft
            entry = predictor.predict_geofence_entry(track, gfm, max_hours=2.0)
            if entry:
                predictions_with_entry += 1

        _report(
            PASS,
            f"Predictor: {len(moving)} moving aircraft checked, "
            f"{predictions_with_entry} predicted geofence entries",
        )

        # Spot check: dead reckoning for first moving aircraft
        if moving:
            forecast = predictor.predict(moving[0], hours=1.0, interval_minutes=15.0)
            assert len(forecast.predictions) == 4  # 1h / 15min = 4 steps
            assert forecast.predictions[0].confidence > forecast.predictions[-1].confidence
            _report(PASS, f"Dead reckoning forecast: {len(forecast.predictions)} steps, confidence degrades correctly")
    except Exception as exc:
        _report(FAIL, "Trajectory prediction", str(exc))

    # ------------------------------------------------------------------
    # 7. Alert engine
    # ------------------------------------------------------------------
    print("\n--- Alert engine ---")
    try:
        alert_engine = AlertEngine()
        all_alerts = []

        for i, track in enumerate(tracker.active_tracks):
            cls = classifications[i] if i < len(classifications) else None
            if cls is None:
                continue
            alerts = alert_engine.evaluate(
                entity_id=f"ADSB-{track.icao_hex}",
                classification=cls,
                domain="air",
                latitude=track.latitude,
                longitude=track.longitude,
                callsign=track.callsign or track.icao_hex,
            )
            all_alerts.extend(alerts)

        _report(PASS, f"Alert engine: {len(all_alerts)} alerts generated from {aircraft_count} aircraft")

        for alert in all_alerts[:3]:
            print(f"         → {alert.alert_type.upper()} {alert.rule_name}: {alert.title}")
    except Exception as exc:
        _report(FAIL, "Alert engine", str(exc))

    # ------------------------------------------------------------------
    # 8. CoT XML generation
    # ------------------------------------------------------------------
    print("\n--- CoT output ---")
    try:
        import xml.etree.ElementTree as ET
        bridge = ADSBCoTBridge(stale_seconds=120)
        cot_events = []

        for track in tracker.active_tracks:
            if track.latitude == 0.0 and track.longitude == 0.0:
                continue
            xml_str = bridge.aircraft_to_cot(track)
            if xml_str:
                cot_events.append(xml_str)

        _report(PASS, f"CoT bridge: {len(cot_events)}/{aircraft_count} tracks produced CoT XML")

        # Validate first 5 CoT events are parseable
        parse_errors = 0
        for xml_str in cot_events[:5]:
            try:
                root = ET.fromstring(xml_str)
                assert root.tag == "event"
                assert root.get("type", "").startswith("a-")
                point = root.find("point")
                assert point is not None
                assert -90 <= float(point.get("lat")) <= 90
                assert -180 <= float(point.get("lon")) <= 180
            except Exception:
                parse_errors += 1

        if parse_errors == 0:
            _report(PASS, "CoT XML validation: all sampled events are well-formed")
        else:
            _report(FAIL, f"CoT XML validation: {parse_errors} malformed events in first 5")
    except Exception as exc:
        _report(FAIL, "CoT XML generation", str(exc))

    # ------------------------------------------------------------------
    # 9. Full async pipeline via CoreEngine
    # ------------------------------------------------------------------
    print("\n--- CoreEngine async pipeline ---")
    try:
        config = CoreEngine.__new__(CoreEngine)  # Don't call __init__ yet

        from mpe.engine import CoreEngine, EngineConfig
        config = EngineConfig(
            adsb_enabled=True,
            adsb_center_lat=center_lat,
            adsb_center_lon=center_lon,
            adsb_radius_nm=radius_nm,
            adsb_poll_interval_s=999,  # Manual control
            ais_enabled=False,
            cot_enabled=False,  # No socket needed for test
            geofence_enabled=True,
            predictor_enabled=True,
            json_logs=False,
            log_level="WARNING",  # Quiet during test
        )
        engine = CoreEngine(config)

        # Seed the tracker with data we already fetched
        for track in tracker.active_tracks:
            engine._aircraft_tracker.update(
                icao_hex=track.icao_hex,
                latitude=track.latitude,
                longitude=track.longitude,
                altitude_baro_ft=track.altitude_baro_ft,
                ground_speed_kts=track.ground_speed_kts,
                heading=track.heading,
                callsign=track.callsign,
                squawk=track.squawk,
            )

        # Run the async pipeline once
        t0 = time.monotonic()
        await engine._run_pipeline()
        elapsed_ms = (time.monotonic() - t0) * 1000

        classified = sum(
            1 for t in engine.aircraft_tracker.active_tracks
            if hasattr(t, "_classification")
        )
        alerts_gen = int(engine.stats["alerts_generated"])

        _report(
            PASS,
            f"CoreEngine._run_pipeline(): {classified} classified, "
            f"{alerts_gen} alerts, {elapsed_ms:.1f}ms",
        )

        if elapsed_ms > 5000:
            _report(FAIL, f"Pipeline took {elapsed_ms:.0f}ms -- too slow for {aircraft_count} aircraft")
        else:
            _report(PASS, f"Pipeline latency {elapsed_ms:.1f}ms (well under 5s threshold)")
    except Exception as exc:
        import traceback
        _report(FAIL, "CoreEngine async pipeline", str(exc))
        traceback.print_exc()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    passed = sum(1 for s, _, _ in _results if s == PASS)
    failed = sum(1 for s, _, _ in _results if s == FAIL)
    skipped = sum(1 for s, _, _ in _results if s == SKIP)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")

    if failed:
        print("\nFailed:")
        for status, name, detail in _results:
            if status == FAIL:
                print(f"  ✗ {name}: {detail}")
        return 1

    print("\nAll checks passed. Async pipeline is working end-to-end.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="MPE ADS-B end-to-end smoke test")
    parser.add_argument(
        "--center",
        default="51.3632,-0.2652",
        help="Center lat,lon (default: Epsom, UK)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=250,
        help="Radius in nautical miles",
    )
    args = parser.parse_args()
    lat, lon = (float(x) for x in args.center.split(","))
    sys.exit(asyncio.run(smoke_test(lat, lon, args.radius)))


if __name__ == "__main__":
    main()
