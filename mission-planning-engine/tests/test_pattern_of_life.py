"""Tests for pattern-of-life analyser.

Generates 50 positions clustered around Epsom (51.36, -0.26) with small
random offsets, consistent speed ~5 m/s, heading ~180 degrees. Then tests
anomaly detection with a position 50km away.
"""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta, timezone

import pytest

from mpe.pattern_of_life import (
    BehaviorAnomaly,
    PatternOfLifeAnalyser,
    PatternReport,
    PositionRecord,
)

# ---------------------------------------------------------------------------
# Fixtures — deterministic test data
# ---------------------------------------------------------------------------

CENTER_LAT = 51.36
CENTER_LON = -0.26
BASE_TIME = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)


def _make_positions(
    count: int = 50,
    center_lat: float = CENTER_LAT,
    center_lon: float = CENTER_LON,
    lat_jitter: float = 0.005,
    lon_jitter: float = 0.005,
    speed: float = 5.0,
    speed_jitter: float = 0.5,
    heading: float = 180.0,
    heading_jitter: float = 5.0,
    hour_start: int = 10,
    seed: int = 42,
) -> list[PositionRecord]:
    """Generate deterministic clustered positions for testing."""
    rng = random.Random(seed)
    positions: list[PositionRecord] = []
    for i in range(count):
        positions.append(PositionRecord(
            latitude=center_lat + rng.uniform(-lat_jitter, lat_jitter),
            longitude=center_lon + rng.uniform(-lon_jitter, lon_jitter),
            speed_mps=speed + rng.uniform(-speed_jitter, speed_jitter),
            heading=heading + rng.uniform(-heading_jitter, heading_jitter),
            timestamp=BASE_TIME + timedelta(minutes=i * 10),
        ))
    return positions


@pytest.fixture()
def positions() -> list[PositionRecord]:
    return _make_positions()


@pytest.fixture()
def analyser() -> PatternOfLifeAnalyser:
    return PatternOfLifeAnalyser(min_records=20)


@pytest.fixture()
def baseline(analyser: PatternOfLifeAnalyser, positions: list[PositionRecord]) -> PatternReport:
    return analyser.analyse("AIS-211234567", positions)


# ---------------------------------------------------------------------------
# Tests — analyse()
# ---------------------------------------------------------------------------


class TestAnalyseTooFewRecords:
    def test_analyse_too_few_records(self, analyser: PatternOfLifeAnalyser) -> None:
        few = _make_positions(count=5)
        report = analyser.analyse("AIS-SHORT", few)
        assert report.record_count == 5
        assert report.centroid_lat == 0.0
        assert report.centroid_lon == 0.0
        assert report.mean_speed_mps == 0.0
        assert report.active_hours == []


class TestAnalyseComputesCentroid:
    def test_analyse_computes_centroid(self, baseline: PatternReport) -> None:
        # Centroid should be close to the cluster center
        assert abs(baseline.centroid_lat - CENTER_LAT) < 0.01
        assert abs(baseline.centroid_lon - CENTER_LON) < 0.01


class TestAnalyseComputesBoundingBox:
    def test_analyse_computes_bounding_box(self, baseline: PatternReport) -> None:
        min_lat, min_lon, max_lat, max_lon = baseline.bounding_box
        assert min_lat < baseline.centroid_lat < max_lat
        assert min_lon < baseline.centroid_lon < max_lon
        # Box should be small — within the jitter range
        assert (max_lat - min_lat) < 0.02
        assert (max_lon - min_lon) < 0.02


class TestAnalyseComputesMaxDistance:
    def test_analyse_computes_max_distance(self, baseline: PatternReport) -> None:
        # Max distance from centroid should be small (< 1 km for our jitter)
        assert baseline.max_distance_from_centroid_km > 0
        assert baseline.max_distance_from_centroid_km < 1.0


class TestAnalyseComputesTypicalRadius:
    def test_analyse_computes_typical_radius(self, baseline: PatternReport) -> None:
        assert baseline.typical_radius_km > 0
        # Typical radius (1 stddev) should be smaller than max distance
        assert baseline.typical_radius_km < baseline.max_distance_from_centroid_km


class TestAnalyseComputesMeanSpeed:
    def test_analyse_computes_mean_speed(self, baseline: PatternReport) -> None:
        # Mean speed should be near 5.0 m/s
        assert 4.0 < baseline.mean_speed_mps < 6.0


class TestAnalyseComputesSpeedStddev:
    def test_analyse_computes_speed_stddev(self, baseline: PatternReport) -> None:
        # Stddev should be small (jitter of ±0.5)
        assert baseline.speed_stddev_mps > 0
        assert baseline.speed_stddev_mps < 1.0


class TestAnalyseComputesActiveHours:
    def test_analyse_computes_active_hours(self, baseline: PatternReport) -> None:
        # Positions span from hour 10 onward (50 positions * 10 min each = ~8 hours)
        assert len(baseline.active_hours) > 0
        assert len(baseline.active_hours) <= 6
        assert 10 in baseline.active_hours


class TestAnalyseComputesHeadingVariance:
    def test_analyse_computes_heading_variance(self, baseline: PatternReport) -> None:
        # Heading ~180 with ±5 jitter — variance should be modest
        assert baseline.heading_variance > 0
        assert baseline.heading_variance < 100  # Small jitter


# ---------------------------------------------------------------------------
# Tests — check_current()
# ---------------------------------------------------------------------------


class TestCheckCurrentAreaDeviation:
    def test_check_current_area_deviation(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        # Position 50km north — well outside typical area
        far_lat = CENTER_LAT + 0.45  # ~50km north
        anomalies = analyser.check_current(baseline, far_lat, CENTER_LON)
        area_anomalies = [a for a in anomalies if a.anomaly_type == "area_deviation"]
        assert len(area_anomalies) == 1
        assert area_anomalies[0].current_value > 10.0  # Should be ~50km


class TestCheckCurrentNoAnomaly:
    def test_check_current_no_anomaly(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        # Position right at centroid with normal speed and heading
        anomalies = analyser.check_current(
            baseline,
            baseline.centroid_lat,
            baseline.centroid_lon,
            current_speed_mps=5.0,
            current_heading=180.0,
        )
        assert len(anomalies) == 0


class TestCheckCurrentSpeedDeviation:
    def test_check_current_speed_deviation(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        # Speed 20 m/s — well above baseline ~5 m/s
        anomalies = analyser.check_current(
            baseline,
            baseline.centroid_lat,
            baseline.centroid_lon,
            current_speed_mps=20.0,
        )
        speed_anomalies = [a for a in anomalies if a.anomaly_type == "speed_deviation"]
        assert len(speed_anomalies) == 1
        assert speed_anomalies[0].current_value == 20.0


class TestCheckCurrentSpeedNormal:
    def test_check_current_speed_normal(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        anomalies = analyser.check_current(
            baseline,
            baseline.centroid_lat,
            baseline.centroid_lon,
            current_speed_mps=5.2,
        )
        speed_anomalies = [a for a in anomalies if a.anomaly_type == "speed_deviation"]
        assert len(speed_anomalies) == 0


class TestCheckCurrentHeadingChange:
    def test_check_current_heading_change(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        # Heading 10° — ~170° off from baseline ~180°
        anomalies = analyser.check_current(
            baseline,
            baseline.centroid_lat,
            baseline.centroid_lon,
            current_heading=10.0,
        )
        heading_anomalies = [a for a in anomalies if a.anomaly_type == "heading_change"]
        assert len(heading_anomalies) == 1


class TestCheckCurrentHeadingNormal:
    def test_check_current_heading_normal(
        self,
        analyser: PatternOfLifeAnalyser,
        baseline: PatternReport,
    ) -> None:
        # Heading 185° — close to baseline ~180°
        anomalies = analyser.check_current(
            baseline,
            baseline.centroid_lat,
            baseline.centroid_lon,
            current_heading=185.0,
        )
        heading_anomalies = [a for a in anomalies if a.anomaly_type == "heading_change"]
        assert len(heading_anomalies) == 0


class TestAnomalySeverityScales:
    def test_anomaly_severity_scales(self) -> None:
        # Use wider speed jitter to get a larger stddev for testable severity
        positions = _make_positions(count=50, speed=5.0, speed_jitter=0.5)
        analyser = PatternOfLifeAnalyser(min_records=20, speed_deviation_sigma=2.0)
        baseline = analyser.analyse("SEVER", positions)

        # Higher speed deviation should produce higher severity
        high_anomalies = analyser.check_current(
            baseline, baseline.centroid_lat, baseline.centroid_lon,
            current_speed_mps=7.0,  # ~4 sigma from mean
        )
        moderate_anomalies = analyser.check_current(
            baseline, baseline.centroid_lat, baseline.centroid_lon,
            current_speed_mps=6.0,  # ~2 sigma from mean
        )
        high_speed = [a for a in high_anomalies if a.anomaly_type == "speed_deviation"]
        mod_speed = [a for a in moderate_anomalies if a.anomaly_type == "speed_deviation"]
        assert len(high_speed) == 1
        assert len(mod_speed) == 1
        assert high_speed[0].severity >= mod_speed[0].severity


class TestBaselineStoredAndRetrievable:
    def test_baseline_stored_and_retrievable(
        self,
        analyser: PatternOfLifeAnalyser,
        positions: list[PositionRecord],
    ) -> None:
        analyser.analyse("VESSEL-A", positions)
        stored = analyser.get_baseline("VESSEL-A")
        assert stored is not None
        assert stored.entity_id == "VESSEL-A"
        assert stored.record_count == 50

        # Non-existent entity returns None
        assert analyser.get_baseline("VESSEL-MISSING") is None


class TestAnalyseIgnoresZeroPositions:
    def test_analyse_ignores_zero_positions(
        self,
        analyser: PatternOfLifeAnalyser,
    ) -> None:
        # Mix valid and zero-lat positions
        positions = _make_positions(count=30)
        # Insert some zero-latitude records
        for i in range(0, 10):
            positions[i] = PositionRecord(
                latitude=0.0,
                longitude=0.0,
                speed_mps=5.0,
                heading=180.0,
                timestamp=BASE_TIME + timedelta(minutes=i * 10),
            )
        report = analyser.analyse("MIXED", positions)
        # Centroid should still be near the valid cluster, not pulled toward 0
        assert abs(report.centroid_lat - CENTER_LAT) < 0.01


class TestAnalysisWindowHours:
    def test_analysis_window_hours(self, baseline: PatternReport) -> None:
        # 50 records at 10-min intervals = 490 min ≈ 8.17 hours
        expected_hours = 49 * 10 / 60  # 8.166...
        assert abs(baseline.analysis_window_hours - expected_hours) < 0.1
