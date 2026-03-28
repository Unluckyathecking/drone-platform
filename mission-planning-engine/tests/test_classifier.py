"""Tests for the entity auto-classifier (classifier module).

Uses SimpleNamespace as duck-typed mock tracks -- same pattern as the rest
of the test suite.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from mpe.classifier import (
    Anomaly,
    Classification,
    EntityClassifier,
    ThreatLevel,
    _threat_level_to_category,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _vessel(**kwargs) -> SimpleNamespace:
    """Build a mock vessel track with sensible defaults."""
    defaults = dict(
        mmsi=211000000,
        latitude=51.5,
        longitude=-0.1,
        speed_over_ground=10.0,
        course_over_ground=180.0,
        heading=180.0,
        ship_type=70,  # cargo
        vessel_name="TEST CARGO",
        nav_status=0,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _aircraft(**kwargs) -> SimpleNamespace:
    """Build a mock aircraft track with sensible defaults."""
    defaults = dict(
        icao_hex="400123",
        callsign="BAW123",
        altitude_baro_ft=35000,
        ground_speed_kts=450,
        heading=90.0,
        squawk="1234",
        category="A3",
        on_ground=False,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


# ---------------------------------------------------------------------------
# Vessel classification
# ---------------------------------------------------------------------------


class TestVesselClassification:
    """Tests for EntityClassifier.classify_vessel."""

    def test_default_vessel_is_neutral(self):
        clf = EntityClassifier()
        result = clf.classify_vessel(_vessel())
        assert result.affiliation == "neutral"
        assert result.threat_level == 1
        assert any("neutral" in r.lower() for r in result.reasoning)

    def test_known_friendly_mmsi(self):
        clf = EntityClassifier(known_friendly_mmsis={211000000})
        result = clf.classify_vessel(_vessel(mmsi=211000000))
        assert result.affiliation == "friendly"
        assert result.threat_level == 0
        assert result.confidence == 0.95

    def test_known_hostile_mmsi(self):
        clf = EntityClassifier(known_hostile_mmsis={999999999})
        result = clf.classify_vessel(_vessel(mmsi=999999999))
        assert result.affiliation == "hostile"
        assert result.threat_level == 9
        assert result.confidence == 0.95

    def test_military_ship_type_35(self):
        clf = EntityClassifier()
        result = clf.classify_vessel(_vessel(ship_type=35))
        assert result.affiliation == "unknown"
        assert result.threat_level >= 5
        assert any("military" in r.lower() for r in result.reasoning)

    def test_law_enforcement_is_friendly(self):
        clf = EntityClassifier()
        result = clf.classify_vessel(_vessel(ship_type=55))
        assert result.affiliation == "friendly"
        assert result.threat_level == 0
        assert any("law enforcement" in r.lower() for r in result.reasoning)

    def test_sar_vessel_is_friendly(self):
        clf = EntityClassifier()
        result = clf.classify_vessel(_vessel(ship_type=51))
        assert result.affiliation == "friendly"
        assert result.threat_level == 0
        assert any("search and rescue" in r.lower() for r in result.reasoning)

    def test_cargo_excessive_speed_anomaly(self):
        clf = EntityClassifier(max_cargo_speed_kts=25.0)
        result = clf.classify_vessel(_vessel(ship_type=70, speed_over_ground=30.0))
        assert result.has_anomalies
        assert any(a.anomaly_type == "excessive_speed" for a in result.anomalies)
        assert result.threat_level >= 4

    def test_tanker_excessive_speed_anomaly(self):
        clf = EntityClassifier(max_tanker_speed_kts=20.0)
        result = clf.classify_vessel(_vessel(ship_type=80, speed_over_ground=25.0))
        assert result.has_anomalies
        assert any(a.anomaly_type == "excessive_speed" for a in result.anomalies)
        assert result.threat_level >= 4

    def test_cargo_normal_speed_no_anomaly(self):
        clf = EntityClassifier(max_cargo_speed_kts=25.0)
        result = clf.classify_vessel(_vessel(ship_type=70, speed_over_ground=15.0))
        speed_anomalies = [
            a for a in result.anomalies if a.anomaly_type == "excessive_speed"
        ]
        assert len(speed_anomalies) == 0

    def test_position_jump_detects_spoofing(self):
        """A vessel that jumps >50 km between updates should be flagged."""
        clf = EntityClassifier(position_jump_km=50.0)
        prev = _vessel(latitude=51.5, longitude=-0.1)
        # ~500 km away (London to Edinburgh-ish)
        curr = _vessel(latitude=55.9, longitude=-3.2)
        result = clf.classify_vessel(curr, previous_track=prev)
        assert result.affiliation == "suspect"
        assert result.threat_level >= 7
        assert any(a.anomaly_type == "position_jump" for a in result.anomalies)

    def test_position_jump_normal_movement_no_anomaly(self):
        """A vessel that moves a small distance should not be flagged."""
        clf = EntityClassifier(position_jump_km=50.0)
        prev = _vessel(latitude=51.5000, longitude=-0.1000)
        curr = _vessel(latitude=51.5010, longitude=-0.1010)
        result = clf.classify_vessel(curr, previous_track=prev)
        jump_anomalies = [
            a for a in result.anomalies if a.anomaly_type == "position_jump"
        ]
        assert len(jump_anomalies) == 0

    def test_missing_vessel_name_large_ship(self):
        clf = EntityClassifier()
        result = clf.classify_vessel(_vessel(ship_type=70, vessel_name=""))
        assert any(a.anomaly_type == "missing_identity" for a in result.anomalies)
        assert result.threat_level >= 3

    def test_threat_level_to_category_mapping(self):
        assert _threat_level_to_category(0) == "none"
        assert _threat_level_to_category(1) == "low"
        assert _threat_level_to_category(3) == "low"
        assert _threat_level_to_category(4) == "medium"
        assert _threat_level_to_category(6) == "medium"
        assert _threat_level_to_category(7) == "high"
        assert _threat_level_to_category(8) == "high"
        assert _threat_level_to_category(9) == "critical"
        assert _threat_level_to_category(10) == "critical"


# ---------------------------------------------------------------------------
# Aircraft classification
# ---------------------------------------------------------------------------


class TestAircraftClassification:
    """Tests for EntityClassifier.classify_aircraft."""

    def test_default_aircraft_is_neutral(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft())
        assert result.affiliation == "neutral"
        assert result.threat_level == 1

    def test_known_friendly_icao(self):
        clf = EntityClassifier(known_friendly_icaos={"400123"})
        result = clf.classify_aircraft(_aircraft(icao_hex="400123"))
        assert result.affiliation == "friendly"
        assert result.threat_level == 0
        assert result.confidence == 0.95

    def test_squawk_7700_emergency(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft(squawk="7700"))
        assert result.threat_level >= 8
        assert any(a.anomaly_type == "emergency" for a in result.anomalies)
        assert any("7700" in a.description for a in result.anomalies)

    def test_squawk_7600_comms_failure(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft(squawk="7600"))
        assert result.threat_level >= 6
        assert any(a.anomaly_type == "emergency" for a in result.anomalies)
        assert any("7600" in a.description for a in result.anomalies)

    def test_squawk_7500_hijack(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft(squawk="7500"))
        assert result.affiliation == "hostile"
        assert result.threat_level == 10
        assert result.threat_category == "critical"
        assert any("HIJACK" in a.description for a in result.anomalies)

    def test_uk_military_icao_range(self):
        clf = EntityClassifier()
        # 0x43C000 = 4439040 -> hex "43C000"
        result = clf.classify_aircraft(_aircraft(icao_hex="43C100"))
        assert result.affiliation == "friendly"
        assert any("UK military" in r for r in result.reasoning)

    def test_us_military_icao_range(self):
        clf = EntityClassifier()
        # 0xADF7C8 = hex "ADF7C8"
        result = clf.classify_aircraft(_aircraft(icao_hex="AE0000"))
        assert result.affiliation == "friendly"
        assert any("US military" in r for r in result.reasoning)

    def test_low_altitude_anomaly(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft(altitude_baro_ft=200, on_ground=False))
        assert any(a.anomaly_type == "low_altitude" for a in result.anomalies)
        assert result.threat_level >= 4

    def test_normal_altitude_no_anomaly(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(_aircraft(altitude_baro_ft=35000, on_ground=False))
        alt_anomalies = [
            a for a in result.anomalies if a.anomaly_type == "low_altitude"
        ]
        assert len(alt_anomalies) == 0

    def test_on_ground_low_alt_no_anomaly(self):
        clf = EntityClassifier()
        result = clf.classify_aircraft(
            _aircraft(altitude_baro_ft=100, on_ground=True),
        )
        alt_anomalies = [
            a for a in result.anomalies if a.anomaly_type == "low_altitude"
        ]
        assert len(alt_anomalies) == 0


# ---------------------------------------------------------------------------
# Classification result properties
# ---------------------------------------------------------------------------


class TestClassificationResult:
    """Tests for Classification dataclass properties."""

    def test_is_suspect_true_when_hostile(self):
        c = Classification(affiliation="hostile", threat_level=5)
        assert c.is_suspect is True

    def test_is_suspect_true_when_high_threat(self):
        c = Classification(affiliation="neutral", threat_level=8)
        assert c.is_suspect is True

    def test_is_suspect_false_for_low_threat_neutral(self):
        c = Classification(affiliation="neutral", threat_level=2)
        assert c.is_suspect is False

    def test_has_anomalies_true(self):
        c = Classification(anomalies=[
            Anomaly(anomaly_type="test", description="test anomaly"),
        ])
        assert c.has_anomalies is True

    def test_has_anomalies_false_when_empty(self):
        c = Classification()
        assert c.has_anomalies is False
