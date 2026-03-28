"""Tests for trajectory prediction (dead reckoning)."""

from __future__ import annotations

import math
from types import SimpleNamespace

import pytest

from mpe.predictor import TrajectoryPredictor, PredictedPosition, TrajectoryForecast
from mpe.geofence import GeofenceManager, GeofenceZone


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_entity(
    entity_id: str = "ENT-001",
    latitude: float = 51.0,
    longitude: float = -0.1,
    speed_mps: float = 5.0,
    heading: float = 0.0,
    altitude_m: float = 0.0,
    domain: str = "sea",
) -> SimpleNamespace:
    return SimpleNamespace(
        entity_id=entity_id,
        latitude=latitude,
        longitude=longitude,
        speed_mps=speed_mps,
        heading=heading,
        altitude_m=altitude_m,
        domain=domain,
    )


@pytest.fixture
def predictor() -> TrajectoryPredictor:
    return TrajectoryPredictor()


# ---------------------------------------------------------------------------
# Dead reckoning basics
# ---------------------------------------------------------------------------

class TestStationary:
    def test_stationary_entity_single_prediction(self, predictor):
        entity = _make_entity(speed_mps=0.0)
        forecast = predictor.predict(entity, hours=6)
        assert len(forecast.predictions) == 1
        assert forecast.predictions[0].latitude == entity.latitude
        assert forecast.predictions[0].longitude == entity.longitude

    def test_zero_speed_returns_single_position(self, predictor):
        entity = _make_entity(speed_mps=0.0, heading=90.0)
        forecast = predictor.predict(entity, hours=2)
        assert len(forecast.predictions) == 1
        assert forecast.predictions[0].speed_mps == 0


class TestDirectionalMovement:
    def test_northbound_vessel_latitude_increases(self, predictor):
        entity = _make_entity(heading=0.0, speed_mps=10.0)
        forecast = predictor.predict(entity, hours=1, interval_minutes=60)
        assert len(forecast.predictions) == 1
        assert forecast.predictions[0].latitude > entity.latitude

    def test_eastbound_vessel_longitude_increases(self, predictor):
        entity = _make_entity(heading=90.0, speed_mps=10.0)
        forecast = predictor.predict(entity, hours=1, interval_minutes=60)
        assert len(forecast.predictions) == 1
        assert forecast.predictions[0].longitude > entity.longitude


class TestPredictionCount:
    def test_prediction_count_matches_intervals(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=6, interval_minutes=30)
        # 6 hours / 30 minutes = 12 predictions
        assert len(forecast.predictions) == 12


class TestConfidence:
    def test_confidence_degrades_over_time(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=6, interval_minutes=30)
        confidences = [p.confidence for p in forecast.predictions]
        # Each subsequent confidence should be <= the previous one
        for i in range(1, len(confidences)):
            assert confidences[i] <= confidences[i - 1]

    def test_confidence_never_below_0_1(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=24, interval_minutes=30)
        for pred in forecast.predictions:
            assert pred.confidence >= 0.1

    def test_first_prediction_high_confidence(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=6, interval_minutes=30)
        # First prediction is at 30 min into a 6 hour window → high confidence
        assert forecast.predictions[0].confidence > 0.8

    def test_last_prediction_low_confidence(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=6, interval_minutes=30)
        # Last prediction at 6 hours → confidence near 0.1
        assert forecast.predictions[-1].confidence < 0.2


class TestSpeedEffect:
    def test_fast_entity_moves_further(self, predictor):
        slow = _make_entity(speed_mps=2.0, heading=0.0)
        fast = _make_entity(speed_mps=20.0, heading=0.0)

        slow_forecast = predictor.predict(slow, hours=1, interval_minutes=60)
        fast_forecast = predictor.predict(fast, hours=1, interval_minutes=60)

        slow_lat = slow_forecast.predictions[0].latitude
        fast_lat = fast_forecast.predictions[0].latitude

        # Both move north; fast should be further north
        assert fast_lat > slow_lat


class TestForecastMetadata:
    def test_forecast_has_correct_entity_id(self, predictor):
        entity = _make_entity(entity_id="VESSEL-42")
        forecast = predictor.predict(entity, hours=1)
        assert forecast.entity_id == "VESSEL-42"

    def test_forecast_method_is_dead_reckoning(self, predictor):
        entity = _make_entity(speed_mps=5.0)
        forecast = predictor.predict(entity, hours=1, interval_minutes=30)
        assert forecast.method == "dead_reckoning"
        for pred in forecast.predictions:
            assert pred.method == "dead_reckoning"

    def test_prediction_preserves_heading(self, predictor):
        entity = _make_entity(heading=135.0, speed_mps=5.0)
        forecast = predictor.predict(entity, hours=1, interval_minutes=30)
        for pred in forecast.predictions:
            assert pred.heading == 135.0


# ---------------------------------------------------------------------------
# Geofence entry prediction
# ---------------------------------------------------------------------------

class TestGeofenceEntry:
    @pytest.fixture
    def geofence_manager(self) -> GeofenceManager:
        gm = GeofenceManager()
        # A keep-out zone north of the entity's start position
        gm.add_zone(GeofenceZone(
            name="RESTRICTED_NORTH",
            zone_type="keep_out",
            polygon=[
                (52.0, -1.0),
                (53.0, -1.0),
                (53.0, 1.0),
                (52.0, 1.0),
            ],
        ))
        return gm

    def test_predict_geofence_entry(self, predictor, geofence_manager):
        # Entity heading north at 10 m/s from lat 51 → will reach lat ~52 zone
        entity = _make_entity(
            latitude=51.0, longitude=0.0,
            heading=0.0, speed_mps=10.0,
        )
        result = predictor.predict_geofence_entry(
            entity, geofence_manager,
            max_hours=6.0, check_interval_minutes=10.0,
        )
        assert result is not None
        assert result["zone"] == "RESTRICTED_NORTH"
        assert result["zone_type"] == "keep_out"
        assert result["entity_id"] == "ENT-001"
        assert result["confidence"] > 0

    def test_predict_no_geofence_entry(self, predictor, geofence_manager):
        # Entity heading south — away from the northern zone
        entity = _make_entity(
            latitude=51.0, longitude=0.0,
            heading=180.0, speed_mps=10.0,
        )
        result = predictor.predict_geofence_entry(
            entity, geofence_manager,
            max_hours=6.0, check_interval_minutes=10.0,
        )
        assert result is None


# ---------------------------------------------------------------------------
# Rendezvous prediction
# ---------------------------------------------------------------------------

class TestRendezvous:
    def test_predict_rendezvous(self, predictor):
        # Two entities heading toward each other
        entity_a = _make_entity(
            entity_id="A",
            latitude=51.0, longitude=0.0,
            heading=90.0, speed_mps=10.0,   # heading east
        )
        entity_b = _make_entity(
            entity_id="B",
            latitude=51.0, longitude=1.0,
            heading=270.0, speed_mps=10.0,  # heading west
        )
        result = predictor.predict_rendezvous(
            entity_a, entity_b,
            max_hours=6.0, proximity_km=5.0,
            check_interval_minutes=10.0,
        )
        assert result is not None
        assert result["entity_a"] == "A"
        assert result["entity_b"] == "B"
        assert result["distance_km"] <= 5.0

    def test_predict_no_rendezvous(self, predictor):
        # Two entities heading away from each other
        entity_a = _make_entity(
            entity_id="A",
            latitude=51.0, longitude=0.0,
            heading=270.0, speed_mps=5.0,   # heading west
        )
        entity_b = _make_entity(
            entity_id="B",
            latitude=51.0, longitude=1.0,
            heading=90.0, speed_mps=5.0,    # heading east
        )
        result = predictor.predict_rendezvous(
            entity_a, entity_b,
            max_hours=2.0, proximity_km=5.0,
            check_interval_minutes=10.0,
        )
        assert result is None

    def test_rendezvous_returns_midpoint(self, predictor):
        # Converging entities — midpoint should be between their positions
        entity_a = _make_entity(
            entity_id="A",
            latitude=51.0, longitude=0.0,
            heading=90.0, speed_mps=10.0,
        )
        entity_b = _make_entity(
            entity_id="B",
            latitude=51.0, longitude=1.0,
            heading=270.0, speed_mps=10.0,
        )
        result = predictor.predict_rendezvous(
            entity_a, entity_b,
            max_hours=6.0, proximity_km=5.0,
            check_interval_minutes=10.0,
        )
        assert result is not None
        # Midpoint longitude should be between 0.0 and 1.0
        assert 0.0 < result["predicted_lon"] < 1.0
