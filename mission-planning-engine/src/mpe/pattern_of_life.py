"""Pattern of Life analysis — detects behavioral anomalies from track history.

Computes baseline behavior for tracked entities (typical area, active hours,
mean speed, heading patterns) and flags deviations. This is the intelligence
feature that justifies the platform over a simple AIS/ADS-B viewer.

Example: "This fishing boat always stays within 20nm of port but today
it's 60nm offshore heading toward a foreign-flagged vessel."

Works in two modes:
1. In-memory: analyse from a list of position records (for testing)
2. DB-backed: query TrackUpdate table for history (production)
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional


@dataclass
class PositionRecord:
    """A single historical position for analysis."""
    latitude: float
    longitude: float
    altitude_m: float = 0.0
    speed_mps: float = 0.0
    heading: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PatternReport:
    """Analysis results for a single entity's pattern of life."""
    entity_id: str
    record_count: int = 0
    analysis_window_hours: float = 0.0

    # Operating area
    centroid_lat: float = 0.0
    centroid_lon: float = 0.0
    bounding_box: tuple[float, float, float, float] = (0, 0, 0, 0)  # min_lat, min_lon, max_lat, max_lon
    max_distance_from_centroid_km: float = 0.0
    typical_radius_km: float = 0.0  # 1 standard deviation

    # Speed profile
    mean_speed_mps: float = 0.0
    speed_stddev_mps: float = 0.0
    max_speed_mps: float = 0.0

    # Heading profile
    mean_heading: float = 0.0
    heading_variance: float = 0.0  # High = circling/loitering

    # Temporal
    active_hours: list[int] = field(default_factory=list)  # Hours (0-23) when entity is most active

    # Anomaly flags
    anomalies: list[str] = field(default_factory=list)
    is_anomalous: bool = False


@dataclass
class BehaviorAnomaly:
    """A detected behavioral anomaly."""
    entity_id: str
    anomaly_type: str       # "area_deviation", "speed_deviation", "heading_change", "unusual_hours"
    description: str
    severity: float = 0.0   # 0-1 (how many stddevs from normal)
    current_value: float = 0.0
    baseline_value: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PatternOfLifeAnalyser:
    """Analyses track history to establish baselines and detect anomalies.

    Usage:
        analyser = PatternOfLifeAnalyser()
        report = analyser.analyse("AIS-211234567", positions)
        anomalies = analyser.check_current(report, current_lat, current_lon, current_speed)
    """

    def __init__(
        self,
        min_records: int = 20,
        area_deviation_sigma: float = 2.0,
        speed_deviation_sigma: float = 2.0,
    ):
        self._min_records = min_records
        self._area_sigma = area_deviation_sigma
        self._speed_sigma = speed_deviation_sigma
        self._baselines: dict[str, PatternReport] = {}

    def analyse(self, entity_id: str, positions: list[PositionRecord]) -> PatternReport:
        """Analyse a list of historical positions to build a baseline.

        Returns a PatternReport. Requires min_records positions to be meaningful.
        """
        report = PatternReport(entity_id=entity_id, record_count=len(positions))

        if len(positions) < self._min_records:
            return report

        # Time window
        timestamps = [p.timestamp for p in positions]
        if timestamps:
            window = (max(timestamps) - min(timestamps)).total_seconds() / 3600
            report.analysis_window_hours = window

        # Centroid
        lats = [p.latitude for p in positions if p.latitude != 0]
        lons = [p.longitude for p in positions if p.longitude != 0]

        if not lats or not lons:
            return report

        report.centroid_lat = statistics.mean(lats)
        report.centroid_lon = statistics.mean(lons)
        report.bounding_box = (min(lats), min(lons), max(lats), max(lons))

        # Distances from centroid
        distances = [
            self._haversine_km(report.centroid_lat, report.centroid_lon, p.latitude, p.longitude)
            for p in positions if p.latitude != 0
        ]

        if distances:
            report.max_distance_from_centroid_km = max(distances)
            report.typical_radius_km = statistics.stdev(distances) if len(distances) > 1 else 0.0

        # Speed profile
        speeds = [p.speed_mps for p in positions if p.speed_mps > 0]
        if speeds:
            report.mean_speed_mps = statistics.mean(speeds)
            report.speed_stddev_mps = statistics.stdev(speeds) if len(speeds) > 1 else 0.0
            report.max_speed_mps = max(speeds)

        # Heading profile
        headings = [p.heading for p in positions if p.heading > 0]
        if headings:
            report.mean_heading = statistics.mean(headings)
            report.heading_variance = statistics.variance(headings) if len(headings) > 1 else 0.0

        # Active hours
        hours = [p.timestamp.hour for p in positions]
        if hours:
            hour_counts: dict[int, int] = {}
            for h in hours:
                hour_counts[h] = hour_counts.get(h, 0) + 1
            # Top 6 most active hours
            report.active_hours = sorted(hour_counts, key=hour_counts.get, reverse=True)[:6]

        # Store baseline
        self._baselines[entity_id] = report

        return report

    def check_current(
        self,
        report: PatternReport,
        current_lat: float,
        current_lon: float,
        current_speed_mps: float = 0.0,
        current_heading: float = 0.0,
    ) -> list[BehaviorAnomaly]:
        """Check current position/behavior against the baseline.

        Returns list of anomalies detected.
        """
        anomalies: list[BehaviorAnomaly] = []

        if report.record_count < self._min_records:
            return anomalies

        # Area deviation
        if report.typical_radius_km > 0:
            distance_from_centroid = self._haversine_km(
                report.centroid_lat, report.centroid_lon,
                current_lat, current_lon,
            )

            threshold = report.typical_radius_km * self._area_sigma
            if distance_from_centroid > max(threshold, 1.0):  # At least 1km threshold
                sigma_val = distance_from_centroid / report.typical_radius_km if report.typical_radius_km > 0 else 0
                anomalies.append(BehaviorAnomaly(
                    entity_id=report.entity_id,
                    anomaly_type="area_deviation",
                    description=f"Entity is {distance_from_centroid:.1f}km from typical area (baseline radius: {report.typical_radius_km:.1f}km, {sigma_val:.1f}\u03c3)",
                    severity=min(1.0, sigma_val / 5.0),
                    current_value=distance_from_centroid,
                    baseline_value=report.typical_radius_km,
                ))

        # Speed deviation
        if report.speed_stddev_mps > 0 and current_speed_mps > 0:
            speed_diff = abs(current_speed_mps - report.mean_speed_mps)
            sigma_val = speed_diff / report.speed_stddev_mps

            if sigma_val > self._speed_sigma:
                anomalies.append(BehaviorAnomaly(
                    entity_id=report.entity_id,
                    anomaly_type="speed_deviation",
                    description=f"Speed {current_speed_mps:.1f} m/s vs baseline {report.mean_speed_mps:.1f}\u00b1{report.speed_stddev_mps:.1f} m/s ({sigma_val:.1f}\u03c3)",
                    severity=min(1.0, sigma_val / 5.0),
                    current_value=current_speed_mps,
                    baseline_value=report.mean_speed_mps,
                ))

        # Heading change (high variance = loitering, sudden change = course alteration)
        if report.heading_variance > 0 and current_heading > 0:
            heading_diff = abs(current_heading - report.mean_heading)
            if heading_diff > 180:
                heading_diff = 360 - heading_diff

            if heading_diff > 90 and report.heading_variance < 1000:  # Normally stable heading, now 90+ off
                anomalies.append(BehaviorAnomaly(
                    entity_id=report.entity_id,
                    anomaly_type="heading_change",
                    description=f"Heading {current_heading:.0f}\u00b0 vs baseline {report.mean_heading:.0f}\u00b0 (diff: {heading_diff:.0f}\u00b0)",
                    severity=heading_diff / 180.0,
                    current_value=current_heading,
                    baseline_value=report.mean_heading,
                ))

        return anomalies

    def get_baseline(self, entity_id: str) -> PatternReport | None:
        """Retrieve a previously computed baseline for an entity."""
        return self._baselines.get(entity_id)

    @staticmethod
    def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine distance in kilometres -- standalone, no external deps."""
        R = 6371.0
        lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
