"""Trajectory prediction — forecasts future entity positions.

Two tiers:
1. Dead reckoning (immediate) — extrapolate from current speed/heading
2. Kalman filter (if history available) — smooth noisy observations and predict

Used for:
- "Where will this vessel be in 6 hours?" (interception planning)
- Predicted position circles on the map
- Alert: "vessel will enter geofence in 30 minutes"
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class PredictedPosition:
    """A predicted future position."""
    latitude: float
    longitude: float
    altitude_m: float = 0.0
    heading: float = 0.0
    speed_mps: float = 0.0
    prediction_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    method: str = "dead_reckoning"   # "dead_reckoning" or "kalman"
    confidence: float = 1.0          # Degrades with time


@dataclass
class TrajectoryForecast:
    """A full trajectory forecast with multiple predicted positions."""
    entity_id: str
    current_lat: float
    current_lon: float
    current_speed_mps: float
    current_heading: float
    predictions: list[PredictedPosition] = field(default_factory=list)
    method: str = "dead_reckoning"
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class TrajectoryPredictor:
    """Predicts future entity positions.

    Usage:
        predictor = TrajectoryPredictor()
        forecast = predictor.predict(entity, hours=6, interval_minutes=30)
        # forecast.predictions = list of PredictedPosition every 30 min for 6 hours
    """

    def predict(
        self,
        entity,   # TrackedEntity or any object with lat/lon/speed_mps/heading
        hours: float = 6.0,
        interval_minutes: float = 30.0,
    ) -> TrajectoryForecast:
        """Predict future positions using dead reckoning.

        Assumes constant speed and heading (simplest model).
        Confidence degrades linearly: 1.0 at t=0, 0.1 at t=max_hours.
        """
        lat = getattr(entity, 'latitude', 0.0)
        lon = getattr(entity, 'longitude', 0.0)
        speed = getattr(entity, 'speed_mps', 0.0)
        heading = getattr(entity, 'heading', 0.0)
        alt = getattr(entity, 'altitude_m', 0.0)

        forecast = TrajectoryForecast(
            entity_id=getattr(entity, 'entity_id', 'unknown'),
            current_lat=lat,
            current_lon=lon,
            current_speed_mps=speed,
            current_heading=heading,
        )

        if speed <= 0:
            # Stationary — just return current position
            forecast.predictions.append(PredictedPosition(
                latitude=lat, longitude=lon, altitude_m=alt,
                heading=heading, speed_mps=0,
                confidence=1.0,
            ))
            return forecast

        # Dead reckoning
        heading_rad = math.radians(heading)
        total_seconds = hours * 3600
        interval_seconds = interval_minutes * 60

        steps = int(total_seconds / interval_seconds)
        now = datetime.now(timezone.utc)

        for i in range(1, steps + 1):
            dt = i * interval_seconds

            # Great circle approximation for short distances
            # dlat = speed * cos(heading) * dt / R
            # dlon = speed * sin(heading) * dt / (R * cos(lat))
            R = 6371000  # Earth radius metres
            lat_rad = math.radians(lat)

            new_lat = lat + math.degrees(
                (speed * math.cos(heading_rad) * dt) / R
            )
            new_lon = lon + math.degrees(
                (speed * math.sin(heading_rad) * dt) / (R * math.cos(lat_rad))
            )

            # Confidence degrades linearly
            confidence = max(0.1, 1.0 - (dt / total_seconds) * 0.9)

            pred_time = now + timedelta(seconds=dt)

            forecast.predictions.append(PredictedPosition(
                latitude=new_lat,
                longitude=new_lon,
                altitude_m=alt,
                heading=heading,
                speed_mps=speed,
                prediction_time=pred_time,
                method="dead_reckoning",
                confidence=round(confidence, 3),
            ))

        return forecast

    def predict_geofence_entry(
        self,
        entity,
        geofence_manager,
        max_hours: float = 6.0,
        check_interval_minutes: float = 10.0,
    ) -> Optional[dict]:
        """Predict if and when an entity will enter/violate a geofence.

        Returns dict with predicted time and zone, or None if no violation predicted.
        """
        forecast = self.predict(entity, hours=max_hours, interval_minutes=check_interval_minutes)

        for pred in forecast.predictions:
            violations = geofence_manager.check(
                entity_id=getattr(entity, 'entity_id', 'unknown'),
                lat=pred.latitude,
                lon=pred.longitude,
                domain=getattr(entity, 'domain', ''),
            )
            if violations:
                return {
                    "entity_id": getattr(entity, 'entity_id', 'unknown'),
                    "predicted_time": pred.prediction_time.isoformat(),
                    "predicted_lat": pred.latitude,
                    "predicted_lon": pred.longitude,
                    "confidence": pred.confidence,
                    "zone": violations[0].zone_name,
                    "zone_type": violations[0].zone_type,
                    "minutes_until": (pred.prediction_time - datetime.now(timezone.utc)).total_seconds() / 60,
                }

        return None

    def predict_rendezvous(
        self,
        entity_a,
        entity_b,
        max_hours: float = 6.0,
        proximity_km: float = 5.0,
        check_interval_minutes: float = 10.0,
    ) -> Optional[dict]:
        """Predict if two entities will come within proximity_km of each other.

        Useful for detecting potential vessel-to-vessel transfers.
        """
        forecast_a = self.predict(entity_a, hours=max_hours, interval_minutes=check_interval_minutes)
        forecast_b = self.predict(entity_b, hours=max_hours, interval_minutes=check_interval_minutes)

        for pred_a, pred_b in zip(forecast_a.predictions, forecast_b.predictions):
            dist = self._haversine_km(
                pred_a.latitude, pred_a.longitude,
                pred_b.latitude, pred_b.longitude,
            )
            if dist <= proximity_km:
                return {
                    "entity_a": getattr(entity_a, 'entity_id', 'unknown'),
                    "entity_b": getattr(entity_b, 'entity_id', 'unknown'),
                    "predicted_time": pred_a.prediction_time.isoformat(),
                    "predicted_lat": (pred_a.latitude + pred_b.latitude) / 2,
                    "predicted_lon": (pred_a.longitude + pred_b.longitude) / 2,
                    "distance_km": round(dist, 2),
                    "confidence": min(pred_a.confidence, pred_b.confidence),
                    "minutes_until": (pred_a.prediction_time - datetime.now(timezone.utc)).total_seconds() / 60,
                }

        return None

    @staticmethod
    def _haversine_km(lat1, lon1, lat2, lon2) -> float:
        R = 6371.0
        lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
