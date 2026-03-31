"""Integration tests for the MPE C2 pipeline.

Tests the full system end-to-end:
  - Engine lifecycle
  - ADS-B ingest → TrackManager → Classification
  - Classification → Alert → CoT output
  - Geofence violation detection
  - Trajectory prediction → geofence entry warning
  - Operator API watchlist round-trip
  - CoT receiver XML parsing
  - Server API GeoJSON response format
  - Pattern of life anomaly detection
  - Full pipeline smoke test (10-second run)

Run:
    PYTHONPATH=src pytest tests/test_integration.py -v --tb=short

Live tests (skip in CI, hit airplanes.live):
    PYTHONPATH=src pytest tests/test_integration.py -v -m live
"""

from __future__ import annotations

import asyncio
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio

pytest_plugins = ("pytest_asyncio",)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_aircraft(
    icao: str = "4CA7B5",
    lat: float = 51.5,
    lon: float = -0.1,
    alt_ft: float = 35000,
    speed_kts: float = 450,
    heading: float = 90.0,
    callsign: str = "BAW123",
    squawk: str = "1234",
    on_ground: bool = False,
):
    """Return a minimal duck-typed aircraft track object."""
    return SimpleNamespace(
        icao_hex=icao,
        latitude=lat,
        longitude=lon,
        altitude_baro_ft=alt_ft,
        altitude_m=alt_ft * 0.3048,
        ground_speed_kts=speed_kts,
        speed_mps=speed_kts * 0.5144,
        heading=heading,
        callsign=callsign,
        squawk=squawk,
        on_ground=on_ground,
        category="A3",
        last_seen=datetime.now(timezone.utc),
    )


def _make_vessel(
    mmsi: int = 211234567,
    lat: float = 51.5,
    lon: float = -1.0,
    sog: float = 12.0,
    cog: float = 180.0,
    ship_type: int = 70,
    vessel_name: str = "CARGO STAR",
    nav_status: int = 0,
):
    """Return a minimal duck-typed vessel track object."""
    return SimpleNamespace(
        mmsi=mmsi,
        latitude=lat,
        longitude=lon,
        speed_over_ground=sog,
        course_over_ground=cog,
        speed_mps=sog * 0.5144,
        heading=cog,
        ship_type=ship_type,
        vessel_name=vessel_name,
        nav_status=nav_status,
        callsign=vessel_name,
        last_seen=datetime.now(timezone.utc),
    )


# ---------------------------------------------------------------------------
# 1. Engine startup and shutdown
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_engine_startup_and_shutdown():
    """Engine starts with default config (no network), runs, shuts down cleanly."""
    from mpe.engine import CoreEngine, EngineConfig

    config = EngineConfig(
        adsb_enabled=False,
        ais_enabled=False,
        cot_enabled=False,
        geofence_enabled=False,
        predictor_enabled=False,
        classify_interval_s=1.0,
        purge_interval_s=999.0,
        json_logs=False,
    )
    engine = CoreEngine(config)
    assert not engine.running

    # Start engine in background, let it tick once, then stop it
    task = asyncio.create_task(engine.start())
    await asyncio.sleep(2.0)

    assert engine.running
    await engine.stop()
    # Give the task a moment to finish
    try:
        await asyncio.wait_for(task, timeout=3.0)
    except (asyncio.CancelledError, asyncio.TimeoutError):
        pass

    assert not engine.running


# ---------------------------------------------------------------------------
# 2. ADS-B ingest → TrackManager → Classification
# ---------------------------------------------------------------------------


def test_adsb_ingest_to_track_manager_to_classification():
    """Aircraft observations flow through TrackManager and get classified."""
    from mpe.track_manager import TrackManager, Observation
    from mpe.classifier import EntityClassifier

    tm = TrackManager()
    classifier = EntityClassifier()

    # Inject 3 aircraft observations
    tracks = [
        _make_aircraft("AABBCC", lat=51.5, lon=-0.1, callsign="TEST01"),
        _make_aircraft("DDEEFF", lat=52.0, lon=0.5, callsign="TEST02"),
        _make_aircraft("112233", lat=50.0, lon=-1.5, callsign="TEST03"),
    ]

    for t in tracks:
        obs = Observation(
            source="adsb",
            source_id=t.icao_hex,
            latitude=t.latitude,
            longitude=t.longitude,
            altitude_m=t.altitude_m,
            heading=t.heading,
            speed_mps=t.speed_mps,
            callsign=t.callsign,
            domain="air",
        )
        tm.process_observation(obs)

    entities = tm.active_entities
    assert len(entities) == 3, f"Expected 3 entities, got {len(entities)}"

    # Classify each and verify output structure
    for entity in entities:
        cls = classifier.classify_aircraft(entity)
        assert hasattr(cls, "affiliation")
        assert hasattr(cls, "threat_level")
        assert isinstance(cls.threat_level, int)
        assert 0 <= cls.threat_level <= 10
        assert cls.affiliation in (
            "friendly", "neutral", "hostile", "suspect", "unknown"
        )


# ---------------------------------------------------------------------------
# 3. Classification → Alert → CoT output
# ---------------------------------------------------------------------------


def test_hostile_track_generates_alert_and_cot():
    """A mock hostile track triggers the classifier, alert engine, and CoT XML."""
    from mpe.classifier import EntityClassifier
    from mpe.alerts import AlertEngine

    classifier = EntityClassifier()
    alert_engine = AlertEngine()

    # Squawk 7500 = hijack — guaranteed hostile + threat_level 10
    track = _make_aircraft(icao="DEAD01", squawk="7500", callsign="HIJACK1")
    cls = classifier.classify_aircraft(track)

    assert cls.affiliation == "hostile"
    assert cls.threat_level == 10
    assert cls.threat_category == "critical"
    assert any(a.anomaly_type == "emergency" for a in cls.anomalies)

    alerts = alert_engine.evaluate(
        entity_id="ADSB-DEAD01",
        classification=cls,
        domain="air",
        latitude=track.latitude,
        longitude=track.longitude,
        callsign=track.callsign,
    )
    assert len(alerts) >= 1, "Expected at least one alert for threat_level=10"

    alert = alerts[0]
    assert alert.cot_xml, "Alert must have CoT XML"

    # Verify CoT XML is well-formed and has correct type
    root = ET.fromstring(alert.cot_xml)
    assert root.tag == "event"
    cot_type = root.get("type", "")
    # Alert events use b-a-o-* types
    assert cot_type.startswith("b-a-o-"), f"Unexpected CoT type: {cot_type}"
    assert root.get("uid"), "CoT event must have UID"


# ---------------------------------------------------------------------------
# 4. Geofence violation flow
# ---------------------------------------------------------------------------


def test_geofence_violation_detected_and_alert_cot_generated():
    """Entity inside a keep-out zone generates a violation and alert CoT."""
    from mpe.geofence import GeofenceManager, GeofenceZone
    from mpe.engine import CoreEngine

    manager = GeofenceManager()
    # Small box around (51.5, -0.1)
    zone = GeofenceZone(
        name="TEST_KEEPOUT",
        zone_type="keep_out",
        polygon=[
            (51.45, -0.15),
            (51.55, -0.15),
            (51.55, -0.05),
            (51.45, -0.05),
        ],
        priority=8,
    )
    manager.add_zone(zone)

    violations = manager.check(
        entity_id="ADSB-TEST001",
        lat=51.50,
        lon=-0.10,
        domain="air",
    )
    assert len(violations) == 1
    v = violations[0]
    assert v.zone_name == "TEST_KEEPOUT"
    assert v.zone_type == "keep_out"
    assert "ADSB-TEST001" in v.message

    # Build CoT from the violation (uses engine's static method)
    cot_xml = CoreEngine._geofence_violation_to_cot(v, callsign="TEST001")
    assert cot_xml, "Geofence violation must produce CoT XML"

    root = ET.fromstring(cot_xml)
    assert root.tag == "event"
    assert root.get("type") == "b-a-o-tbl"
    point = root.find("point")
    assert point is not None
    assert float(point.get("lat")) == pytest.approx(51.50, abs=0.0001)
    assert float(point.get("lon")) == pytest.approx(-0.10, abs=0.0001)


# ---------------------------------------------------------------------------
# 5. Predictor → Geofence entry prediction
# ---------------------------------------------------------------------------


def test_predictor_geofence_entry_prediction():
    """Entity heading toward a geofence zone returns a predicted entry."""
    from mpe.predictor import TrajectoryPredictor
    from mpe.geofence import GeofenceManager, GeofenceZone

    manager = GeofenceManager()
    # Zone to the east — entity heading east at 50 m/s should enter it
    zone = GeofenceZone(
        name="EAST_ZONE",
        zone_type="alert",
        polygon=[
            (51.49, 1.5),
            (51.51, 1.5),
            (51.51, 2.0),
            (51.49, 2.0),
        ],
        priority=5,
    )
    manager.add_zone(zone)

    predictor = TrajectoryPredictor()

    # Entity at 51.5°N, heading east (90°) at 200 m/s
    entity = SimpleNamespace(
        entity_id="ENT-001",
        latitude=51.50,
        longitude=0.0,
        altitude_m=10000.0,
        speed_mps=200.0,   # Fast — will cross 1.5° lon in a few hours
        heading=90.0,
        domain="air",
    )

    result = predictor.predict_geofence_entry(
        entity,
        manager,
        max_hours=6.0,
        check_interval_minutes=10.0,
    )
    assert result is not None, "Expected a predicted geofence entry"
    assert result["zone"] == "EAST_ZONE"
    assert "predicted_time" in result
    assert result["minutes_until"] > 0


# ---------------------------------------------------------------------------
# 6. Operator API watchlist round-trip
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_operator_api_watchlist_roundtrip():
    """POST a watchlist entry, confirm it appears in the store."""
    from httpx import AsyncClient, ASGITransport
    from mpe.server import app
    from mpe.auth import _make_token
    import time

    # Generate a valid operator JWT
    token = _make_token("admin", "operator", 900, "access")
    headers = {"Authorization": f"Bearer {token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        payload = {
            "identifier": "AABB11",
            "identifier_type": "icao",
            "affiliation": "hostile",
            "reason": "integration test",
            "added_by": "qa_agent",
        }
        resp = await client.post(
            "/api/operator/watchlist",
            json=payload,
            headers=headers,
        )
        assert resp.status_code == 200, f"Unexpected status: {resp.status_code} {resp.text}"
        data = resp.json()
        assert data["status"] == "added"
        assert data["affiliation"] == "hostile"
        assert "icao:AABB11" == data["key"]

        # GET the watchlist and verify entry is present
        resp2 = await client.get("/api/operator/watchlist", headers=headers)
        assert resp2.status_code == 200
        body = resp2.json()
        # Response is {"entries": [...], "total": N} or similar
        entries = body if isinstance(body, list) else body.get("entries", [])
        assert any(
            (e.get("identifier") == "AABB11" if isinstance(e, dict) else False)
            for e in entries
        ), f"AABB11 not found in watchlist: {body}"


# ---------------------------------------------------------------------------
# 7. CoT receiver parsing
# ---------------------------------------------------------------------------


def test_cot_receiver_parse_cot_xml():
    """parse_cot_xml produces a CotEvent with correct domain and affiliation."""
    from mpe.cot_receiver import parse_cot_xml

    sample_xml = """<event version="2.0"
        uid="PYTEST-AIRCRAFT-001"
        type="a-f-A-M-F"
        time="2024-01-01T12:00:00Z"
        start="2024-01-01T12:00:00Z"
        stale="2024-01-01T12:30:00Z"
        how="m-g">
        <point lat="51.5074" lon="-0.1278" hae="10000" ce="10" le="20"/>
        <detail>
            <contact callsign="RAF1"/>
            <track course="270" speed="200"/>
            <remarks>Test aircraft</remarks>
        </detail>
    </event>"""

    event = parse_cot_xml(sample_xml)

    assert event is not None
    assert event.uid == "PYTEST-AIRCRAFT-001"
    assert event.event_type == "a-f-A-M-F"
    assert event.latitude == pytest.approx(51.5074, abs=0.0001)
    assert event.longitude == pytest.approx(-0.1278, abs=0.0001)
    assert event.callsign == "RAF1"
    assert event.heading == pytest.approx(270.0, abs=0.1)
    assert event.speed_mps == pytest.approx(200.0, abs=0.1)

    # Domain and affiliation from type code
    assert event.domain == "air"           # "A" = air
    assert event.affiliation == "friendly"  # "f" = friendly


def test_cot_receiver_parse_malformed_xml():
    """parse_cot_xml returns None for malformed or invalid XML."""
    from mpe.cot_receiver import parse_cot_xml

    assert parse_cot_xml("not xml at all") is None
    assert parse_cot_xml("<notanevent/>") is None
    assert parse_cot_xml("<event uid='x' type='a-f-G'/>") is None  # no point element
    assert parse_cot_xml("") is None


def test_cot_receiver_parse_hostile_sea_unit():
    """Hostile surface vessel CoT type parses correctly."""
    from mpe.cot_receiver import parse_cot_xml

    xml = """<event version="2.0"
        uid="TEST-VESSEL-002"
        type="a-h-S-X-V"
        time="2024-01-01T00:00:00Z"
        start="2024-01-01T00:00:00Z"
        stale="2024-01-01T01:00:00Z"
        how="m-g">
        <point lat="25.5" lon="56.5" hae="0" ce="9999" le="9999"/>
    </event>"""

    event = parse_cot_xml(xml)
    assert event is not None
    assert event.domain == "sea"
    assert event.affiliation == "hostile"


# ---------------------------------------------------------------------------
# 8. Server API response format
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_server_api_tracks_geojson_structure():
    """GET /api/tracks returns valid GeoJSON FeatureCollection with meta counts."""
    from httpx import AsyncClient, ASGITransport
    from mpe.server import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/api/tracks")

    assert resp.status_code == 200
    data = resp.json()

    # Must be GeoJSON FeatureCollection
    assert data.get("type") == "FeatureCollection"
    assert "features" in data
    assert isinstance(data["features"], list)

    # Must have meta object with counts
    meta = data.get("meta", {})
    assert "total" in meta
    assert "aircraft" in meta or "vessels" in meta or "total" in meta
    assert isinstance(meta["total"], int)


# ---------------------------------------------------------------------------
# 9. Pattern of life → anomaly detection
# ---------------------------------------------------------------------------


def test_pattern_of_life_area_deviation_anomaly():
    """Build a 50-position baseline, check a far-away position triggers area_deviation."""
    from mpe.pattern_of_life import PatternOfLifeAnalyser, PositionRecord

    analyser = PatternOfLifeAnalyser(min_records=20, area_deviation_sigma=2.0)

    # Build baseline: entity operates around (51.5, -0.1) within ~5km
    import math, random
    random.seed(42)

    positions = []
    for i in range(50):
        # Small random scatter within ~3km of centroid
        dlat = random.uniform(-0.02, 0.02)
        dlon = random.uniform(-0.02, 0.02)
        positions.append(PositionRecord(
            latitude=51.5 + dlat,
            longitude=-0.1 + dlon,
            speed_mps=random.uniform(2.0, 8.0),
            heading=random.uniform(0, 360),
            timestamp=datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=i * 10),
        ))

    report = analyser.analyse("AIS-211234567", positions)
    assert report.record_count == 50
    assert report.centroid_lat == pytest.approx(51.5, abs=0.05)
    assert report.typical_radius_km > 0

    # Current position 50km away from centroid — should trigger area_deviation
    anomalies = analyser.check_current(
        report,
        current_lat=51.95,   # ~50km north of 51.5
        current_lon=-0.1,
        current_speed_mps=5.0,
    )

    anomaly_types = [a.anomaly_type for a in anomalies]
    assert "area_deviation" in anomaly_types, (
        f"Expected area_deviation anomaly; got: {anomaly_types}. "
        f"typical_radius={report.typical_radius_km:.2f}km"
    )


# ---------------------------------------------------------------------------
# 10. Full pipeline smoke test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_pipeline_smoke_test():
    """Engine with ADS-B mocked, runs for ~6 seconds, checks stats."""
    from mpe.engine import CoreEngine, EngineConfig
    from mpe.aircraft_tracker import AircraftTrack

    # Build 5 real AircraftTrack objects (they have is_stale property)
    fake_tracks = [
        AircraftTrack(
            icao_hex=f"AA{i:04X}",
            latitude=51.5 + i * 0.1,
            longitude=-0.1 + i * 0.05,
            altitude_baro_ft=35000,
            ground_speed_kts=450,
            heading=90.0,
            callsign=f"SMOKE{i}",
        )
        for i in range(5)
    ]

    config = EngineConfig(
        adsb_enabled=False,       # Don't poll real network
        ais_enabled=False,
        cot_enabled=False,
        geofence_enabled=True,
        geofence_load_demo_zones=True,
        predictor_enabled=True,
        classify_interval_s=1.0,
        purge_interval_s=999.0,
        json_logs=False,
    )
    engine = CoreEngine(config)

    # Pre-populate aircraft tracker with proper AircraftTrack objects
    for t in fake_tracks:
        engine.aircraft_tracker._tracks[t.icao_hex] = t  # noqa: SLF001

    task = asyncio.create_task(engine.start())
    # Let the engine run for 4 seconds (enough for 3+ classify cycles at 1s interval)
    await asyncio.sleep(4.0)

    # Capture stats while engine is running
    stats = engine.stats
    is_running = engine.running

    await engine.stop()
    try:
        await asyncio.wait_for(task, timeout=3.0)
    except (asyncio.CancelledError, asyncio.TimeoutError):
        pass

    assert is_running, "Engine should have been running during the sleep"

    # Verify stats show actual activity
    assert stats["classifications_run"] > 0, (
        f"Expected classifications_run > 0, got: {stats}"
    )
    assert stats["aircraft_tracked"] >= 0


# ---------------------------------------------------------------------------
# 11. Live test (tags @pytest.mark.live — skipped in CI)
# ---------------------------------------------------------------------------


@pytest.mark.live
def test_live_adsb_airplanes_live():
    """Fetch real aircraft from airplanes.live and verify they appear in TrackManager.

    Tagged @pytest.mark.live so it is skipped in CI by default.
    Run manually: pytest tests/test_integration.py -v -m live
    """
    from mpe.adsb_receiver import ADSBReceiver
    from mpe.aircraft_tracker import AircraftTracker
    from mpe.track_manager import TrackManager, Observation

    tracker = AircraftTracker()
    tm = TrackManager()

    receiver = ADSBReceiver(
        tracker,
        center_lat=51.3632,
        center_lon=-0.2652,
        radius_nm=100,
        source="airplanes_live",
    )

    # Single poll — fetch once and check we got some data
    try:
        receiver._poll_once()  # noqa: SLF001
    except Exception as exc:
        pytest.skip(f"airplanes.live unreachable: {exc}")

    active = tracker.active_tracks
    if not active:
        pytest.skip("No aircraft returned (may be a quiet period or API down)")

    # Feed into TrackManager
    for t in active:
        obs = Observation(
            source="adsb",
            source_id=t.icao_hex,
            latitude=t.latitude,
            longitude=t.longitude,
            altitude_m=t.altitude_m,
            heading=t.heading,
            speed_mps=t.speed_mps,
            callsign=t.callsign or "",
            domain="air",
        )
        tm.process_observation(obs)

    entities = tm.entities
    assert len(entities) > 0, "TrackManager should have entities after ADS-B poll"
    assert len(entities) == len(active)
