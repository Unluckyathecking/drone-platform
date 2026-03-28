"""Tests for the LLM-powered intelligence module (mpe.intelligence).

Covers: template-based SITREP generation, IntelligenceEngine availability,
keyword query fallback, and flash report template fallback.
Does NOT test actual LLM calls -- urllib is mocked where needed.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

import pytest

from mpe.intelligence import (
    IntelligenceEngine,
    generate_sitrep_template,
)
from mpe.track_manager import TrackManager, TrackedEntity, Observation


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_sitrep_data(
    air_total: int = 5,
    air_friendly: int = 3,
    air_neutral: int = 1,
    air_hostile: int = 1,
    air_unknown: int = 0,
    sea_total: int = 10,
    sea_friendly: int = 5,
    sea_neutral: int = 3,
    sea_hostile: int = 1,
    sea_unknown: int = 1,
    threats: list | None = None,
    active_threats: int | None = None,
    unacknowledged_alerts: int = 0,
    own_forces: int = 2,
) -> dict:
    """Build a mock sitrep_data dict matching the /api/operator/sitrep shape."""
    if threats is None:
        threats = []
    if active_threats is None:
        active_threats = len(threats)
    return {
        "generated_at": "2026-03-28T12:00:00+00:00",
        "classification": "UNCLASSIFIED",
        "summary": {
            "air_tracks": air_total,
            "sea_tracks": sea_total,
            "total_tracks": air_total + sea_total,
            "active_threats": active_threats,
            "active_emergencies": 0,
            "unacknowledged_alerts": unacknowledged_alerts,
            "watchlist_entries": 0,
            "own_forces": own_forces,
        },
        "air_picture": {
            "total": air_total,
            "by_affiliation": {
                "friendly": air_friendly,
                "neutral": air_neutral,
                "hostile": air_hostile,
                "suspect": 0,
                "unknown": air_unknown,
            },
        },
        "sea_picture": {
            "total": sea_total,
            "by_affiliation": {
                "friendly": sea_friendly,
                "neutral": sea_neutral,
                "hostile": sea_hostile,
                "suspect": 0,
                "unknown": sea_unknown,
            },
        },
        "threats": threats,
        "emergencies": [],
        "overrides": 0,
    }


def _make_track_manager_with_entities() -> TrackManager:
    """Create a TrackManager pre-populated with a mix of entities."""
    tm = TrackManager()

    # Friendly aircraft
    tm.process_observation(Observation(
        source="adsb", source_id="A1B2C3",
        latitude=51.5, longitude=-0.1,
        callsign="BA123", domain="air",
        entity_type="fixed_wing",
    ))
    # Hostile vessel
    ent = tm.process_observation(Observation(
        source="ais", source_id="211999111",
        latitude=26.0, longitude=56.5,
        callsign="SHADOW-7", domain="sea",
        entity_type="surface_vessel",
    ))
    ent.affiliation = "hostile"
    ent.threat_level = 8

    # Suspect vessel
    ent2 = tm.process_observation(Observation(
        source="ais", source_id="211999222",
        latitude=26.1, longitude=56.6,
        callsign="GHOST-3", domain="sea",
        entity_type="surface_vessel",
    ))
    ent2.affiliation = "suspect"
    ent2.threat_level = 5

    # Friendly aircraft (another)
    tm.process_observation(Observation(
        source="adsb", source_id="DDDDD1",
        latitude=51.4, longitude=-0.2,
        callsign="RAF01", domain="air",
        entity_type="fixed_wing",
    ))

    # Friendly drone
    ent3 = tm.process_observation(Observation(
        source="mavlink", source_id="DRONE-1",
        latitude=51.36, longitude=-0.26,
        callsign="MPE-UAV-1", domain="air",
        entity_type="uav",
    ))
    ent3.affiliation = "friendly"

    return tm


# ---------------------------------------------------------------------------
# Template SITREP tests
# ---------------------------------------------------------------------------


class TestGenerateSitrepTemplate:
    """Tests for the template-based (offline) SITREP generator."""

    def test_generate_sitrep_template(self):
        """Template SITREP returns non-empty string with key sections."""
        data = _make_sitrep_data()
        result = generate_sitrep_template(data)
        assert isinstance(result, str)
        assert len(result) > 100
        assert "SITUATION REPORT" in result

    def test_template_includes_air_picture(self):
        """Template includes air picture counts."""
        data = _make_sitrep_data(air_total=5, air_friendly=3, air_hostile=1)
        result = generate_sitrep_template(data)
        assert "5 tracks" in result
        assert "3 friendly" in result
        assert "1 hostile" in result

    def test_template_includes_sea_picture(self):
        """Template includes maritime picture counts."""
        data = _make_sitrep_data(sea_total=10, sea_friendly=5, sea_hostile=1)
        result = generate_sitrep_template(data)
        assert "10 tracks" in result
        assert "5 friendly" in result

    def test_template_includes_threats(self):
        """Template lists individual threats when present."""
        threats = [
            {
                "callsign": "SHADOW-7",
                "domain": "sea",
                "threat_level": 8,
                "affiliation": "hostile",
            },
        ]
        data = _make_sitrep_data(threats=threats, active_threats=1)
        result = generate_sitrep_template(data)
        assert "SHADOW-7" in result
        assert "8/10" in result

    def test_template_no_threats_says_normal(self):
        """Template assessment says 'Normal operations' when no threats."""
        data = _make_sitrep_data(threats=[], active_threats=0)
        result = generate_sitrep_template(data)
        assert "Normal operations" in result

    def test_template_high_threats_says_elevated(self):
        """Template assessment says 'Elevated' when many threats."""
        threats = [
            {"callsign": f"T-{i}", "domain": "sea", "threat_level": 7, "affiliation": "hostile"}
            for i in range(5)
        ]
        data = _make_sitrep_data(threats=threats, active_threats=5)
        result = generate_sitrep_template(data)
        assert "Elevated" in result


# ---------------------------------------------------------------------------
# IntelligenceEngine availability tests
# ---------------------------------------------------------------------------


class TestIntelligenceEngineAvailability:
    """Tests for engine availability based on API key presence."""

    def test_not_available_without_key(self):
        """Engine reports not available when no API key provided."""
        engine = IntelligenceEngine(api_key=None)
        assert engine.is_available is False

    def test_available_with_key(self):
        """Engine reports available when API key provided."""
        engine = IntelligenceEngine(api_key="sk-test-key-123")
        assert engine.is_available is True


# ---------------------------------------------------------------------------
# Keyword query fallback tests
# ---------------------------------------------------------------------------


class TestKeywordQuery:
    """Tests for the keyword-based query fallback (no LLM)."""

    def test_keyword_query_aircraft_filter(self):
        """Keyword query filters by aircraft domain."""
        tm = _make_track_manager_with_entities()
        engine = IntelligenceEngine(api_key=None)
        result = asyncio.run(
            engine.natural_language_query("show me all aircraft", tm),
        )
        assert result["count"] > 0
        # All referenced entities should be air domain
        for eid in result["entities_referenced"]:
            ent = tm.get(eid)
            assert ent is not None
            assert ent.domain == "air"

    def test_keyword_query_hostile_filter(self):
        """Keyword query filters by hostile affiliation."""
        tm = _make_track_manager_with_entities()
        engine = IntelligenceEngine(api_key=None)
        result = asyncio.run(
            engine.natural_language_query("hostile entities", tm),
        )
        assert result["count"] >= 1
        for eid in result["entities_referenced"]:
            ent = tm.get(eid)
            assert ent is not None
            assert ent.affiliation == "hostile"

    def test_keyword_query_threat_filter(self):
        """Keyword query filters by threat level."""
        tm = _make_track_manager_with_entities()
        engine = IntelligenceEngine(api_key=None)
        result = asyncio.run(
            engine.natural_language_query("show me all threats", tm),
        )
        assert result["count"] >= 1
        for eid in result["entities_referenced"]:
            ent = tm.get(eid)
            assert ent is not None
            assert ent.threat_level >= 4

    def test_keyword_query_vessel_filter(self):
        """Keyword query filters by vessel/sea domain."""
        tm = _make_track_manager_with_entities()
        engine = IntelligenceEngine(api_key=None)
        result = asyncio.run(
            engine.natural_language_query("show me all vessels", tm),
        )
        assert result["count"] >= 1
        for eid in result["entities_referenced"]:
            ent = tm.get(eid)
            assert ent is not None
            assert ent.domain == "sea"


# ---------------------------------------------------------------------------
# Flash report fallback test
# ---------------------------------------------------------------------------


class TestFlashReport:
    """Tests for the flash report template fallback."""

    def test_flash_report_template_fallback(self):
        """Flash report falls back to simple template when no API key."""
        engine = IntelligenceEngine(api_key=None)

        alert = SimpleNamespace(
            title="High threat detected: SHADOW-7",
            description="Hostile vessel SHADOW-7 at threat level 8/10",
            alert_type="threat",
            severity=8,
            entity_id="AIS-211999111",
            latitude=26.0,
            longitude=56.5,
        )

        result = asyncio.run(
            engine.generate_flash_report(alert),
        )
        assert "FLASH" in result
        assert "SHADOW-7" in result


# ---------------------------------------------------------------------------
# SITREP generation with LLM fallback
# ---------------------------------------------------------------------------


class TestSitrepLLMFallback:
    """Verify that generate_sitrep falls back to template without API key."""

    def test_sitrep_uses_template_without_key(self):
        """generate_sitrep returns template output when engine is unavailable."""
        engine = IntelligenceEngine(api_key=None)
        data = _make_sitrep_data()
        result = asyncio.run(
            engine.generate_sitrep(data),
        )
        assert "SITUATION REPORT" in result
        assert "UNCLASSIFIED" in result
