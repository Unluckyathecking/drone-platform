"""Tests for the TrackManager -- unified entity registry with multi-source correlation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from mpe.track_manager import Observation, TrackedEntity, TrackManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _obs(
    source: str = "ais",
    source_id: str = "211234567",
    lat: float = 51.5,
    lon: float = -0.1,
    **kwargs,
) -> Observation:
    """Shortcut to build an Observation with sane defaults."""
    return Observation(
        source=source,
        source_id=source_id,
        latitude=lat,
        longitude=lon,
        **kwargs,
    )


# ===========================================================================
# Observation basics
# ===========================================================================


class TestObservationBasics:
    def test_observation_creation(self):
        obs = Observation(
            source="ais",
            source_id="211234567",
            latitude=51.5,
            longitude=-0.1,
        )
        assert obs.source == "ais"
        assert obs.source_id == "211234567"
        assert obs.latitude == 51.5
        assert obs.longitude == -0.1

    def test_observation_defaults(self):
        obs = Observation(
            source="adsb",
            source_id="4CA7B5",
            latitude=51.0,
            longitude=-0.2,
        )
        assert obs.altitude_m == 0.0
        assert obs.heading == 0.0
        assert obs.speed_mps == 0.0
        assert obs.callsign == ""
        assert obs.name == ""
        assert obs.entity_type == ""
        assert obs.domain == ""
        assert obs.metadata == {}
        assert isinstance(obs.timestamp, datetime)


# ===========================================================================
# Entity creation
# ===========================================================================


class TestEntityCreation:
    def test_first_observation_creates_entity(self):
        tm = TrackManager()
        obs = _obs()
        entity = tm.process_observation(obs)
        assert entity is not None
        assert len(tm.all_entities) == 1

    def test_entity_gets_unique_id(self):
        tm = TrackManager()
        e1 = tm.process_observation(_obs(source_id="AAA"))
        e2 = tm.process_observation(_obs(source_id="BBB"))
        assert e1.entity_id != e2.entity_id
        assert e1.entity_id.startswith("ENT-")
        assert e2.entity_id.startswith("ENT-")

    def test_entity_inherits_observation_fields(self):
        tm = TrackManager()
        obs = _obs(
            callsign="BRAVO",
            name="Test Vessel",
            entity_type="surface_vessel",
            domain="sea",
            altitude_m=0.0,
            heading=180.0,
            speed_mps=5.0,
        )
        entity = tm.process_observation(obs)
        assert entity.callsign == "BRAVO"
        assert entity.name == "Test Vessel"
        assert entity.entity_type == "surface_vessel"
        assert entity.domain == "sea"
        assert entity.heading == 180.0
        assert entity.speed_mps == 5.0


# ===========================================================================
# Exact ID match
# ===========================================================================


class TestExactIDMatch:
    def test_same_source_id_matches_same_entity(self):
        tm = TrackManager()
        e1 = tm.process_observation(_obs(source="ais", source_id="123"))
        e2 = tm.process_observation(_obs(source="ais", source_id="123"))
        assert e1.entity_id == e2.entity_id
        assert len(tm.all_entities) == 1

    def test_different_source_id_creates_new_entity(self):
        tm = TrackManager()
        e1 = tm.process_observation(_obs(source="ais", source_id="123"))
        e2 = tm.process_observation(_obs(source="ais", source_id="456"))
        assert e1.entity_id != e2.entity_id
        assert len(tm.all_entities) == 2

    def test_ais_then_ais_same_mmsi_matches(self):
        tm = TrackManager()
        obs1 = _obs(source="ais", source_id="211234567", lat=51.5, lon=-0.1)
        obs2 = _obs(source="ais", source_id="211234567", lat=51.50001, lon=-0.10001)
        e1 = tm.process_observation(obs1)
        e2 = tm.process_observation(obs2)
        assert e1.entity_id == e2.entity_id


# ===========================================================================
# Spatial correlation
# ===========================================================================


class TestSpatialCorrelation:
    def test_nearby_observation_different_source_correlates(self):
        """An ADS-B observation near an AIS entity should fuse."""
        tm = TrackManager(correlation_radius_m=1000)
        # AIS observation
        tm.process_observation(_obs(
            source="ais", source_id="211234567",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        # ADS-B observation very close by, compatible
        entity = tm.process_observation(_obs(
            source="adsb", source_id="4CA7B5",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
        ))
        assert len(tm.all_entities) == 1
        assert "ais" in entity.sources_seen
        assert "adsb" in entity.sources_seen

    def test_far_observation_does_not_correlate(self):
        tm = TrackManager(correlation_radius_m=500)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea",
        ))
        # Far away (roughly 11 km north)
        tm.process_observation(_obs(
            source="adsb", source_id="BBB",
            lat=51.6, lon=-0.1, domain="sea",
        ))
        assert len(tm.all_entities) == 2

    def test_same_domain_required_for_correlation(self):
        tm = TrackManager(correlation_radius_m=5000)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea",
        ))
        # Same location but different domain
        tm.process_observation(_obs(
            source="cot", source_id="BBB",
            lat=51.5, lon=-0.1, domain="air",
        ))
        assert len(tm.all_entities) == 2

    def test_speed_compatibility_check(self):
        tm = TrackManager(correlation_radius_m=5000, max_speed_diff_mps=5.0)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=3.0,
        ))
        # Same location, same domain, but wildly different speed
        tm.process_observation(_obs(
            source="cot", source_id="BBB",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=50.0,
        ))
        assert len(tm.all_entities) == 2

    def test_stale_entity_not_correlated(self):
        tm = TrackManager(correlation_radius_m=5000, correlation_time_window_s=60)
        obs1 = _obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea",
        )
        # Backdate the observation so entity is old
        obs1.timestamp = _now() - timedelta(seconds=120)
        tm.process_observation(obs1)

        # New observation at same spot should NOT correlate (entity too old)
        tm.process_observation(_obs(
            source="cot", source_id="BBB",
            lat=51.5, lon=-0.1, domain="sea",
        ))
        assert len(tm.all_entities) == 2


# ===========================================================================
# Multi-source fusion
# ===========================================================================


class TestMultiSourceFusion:
    def test_ais_plus_adsb_same_location_fuses(self):
        tm = TrackManager(correlation_radius_m=1000)
        e1 = tm.process_observation(_obs(
            source="ais", source_id="211234567",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        e2 = tm.process_observation(_obs(
            source="adsb", source_id="4CA7B5",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
        ))
        assert e1.entity_id == e2.entity_id
        assert e2.is_multi_source

    def test_multi_source_increases_confidence(self):
        tm = TrackManager(correlation_radius_m=1000)
        e = tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        initial_conf = e.confidence
        tm.process_observation(_obs(
            source="adsb", source_id="BBB",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
        ))
        assert e.confidence > initial_conf

    def test_callsign_updated_from_second_source(self):
        tm = TrackManager(correlation_radius_m=1000)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        e = tm.process_observation(_obs(
            source="adsb", source_id="BBB",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
            callsign="ALPHA",
        ))
        assert e.callsign == "ALPHA"

    def test_sources_seen_tracks_all_sources(self):
        tm = TrackManager(correlation_radius_m=1000)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        e = tm.process_observation(_obs(
            source="cot", source_id="BBB",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
        ))
        assert e.sources_seen == {"ais", "cot"}


# ===========================================================================
# Merge behavior
# ===========================================================================


class TestMergeBehavior:
    def test_position_updated_on_new_observation(self):
        tm = TrackManager()
        tm.process_observation(_obs(
            source="ais", source_id="AAA", lat=51.5, lon=-0.1,
        ))
        e = tm.process_observation(_obs(
            source="ais", source_id="AAA", lat=51.6, lon=-0.2,
        ))
        assert e.latitude == 51.6
        assert e.longitude == -0.2

    def test_zero_position_does_not_overwrite(self):
        tm = TrackManager()
        tm.process_observation(_obs(
            source="ais", source_id="AAA", lat=51.5, lon=-0.1,
        ))
        e = tm.process_observation(_obs(
            source="ais", source_id="AAA", lat=0.0, lon=0.0,
        ))
        assert e.latitude == 51.5
        assert e.longitude == -0.1

    def test_empty_callsign_does_not_overwrite(self):
        tm = TrackManager()
        tm.process_observation(_obs(
            source="ais", source_id="AAA", callsign="BRAVO",
        ))
        e = tm.process_observation(_obs(
            source="ais", source_id="AAA", callsign="",
        ))
        assert e.callsign == "BRAVO"

    def test_observation_count_increments(self):
        tm = TrackManager()
        e = tm.process_observation(_obs(source="ais", source_id="AAA"))
        assert e.observation_count == 1
        tm.process_observation(_obs(source="ais", source_id="AAA"))
        assert e.observation_count == 2
        tm.process_observation(_obs(source="ais", source_id="AAA"))
        assert e.observation_count == 3


# ===========================================================================
# Query methods
# ===========================================================================


class TestQueryMethods:
    def test_active_entities_excludes_stale(self):
        tm = TrackManager()
        obs = _obs(source="ais", source_id="AAA", domain="sea")
        # Backdate so it's stale (sea = 300s threshold)
        obs.timestamp = _now() - timedelta(seconds=600)
        tm.process_observation(obs)

        # Fresh entity
        tm.process_observation(_obs(source="ais", source_id="BBB", domain="sea"))

        assert len(tm.all_entities) == 2
        assert len(tm.active_entities) == 1

    def test_entities_near_radius(self):
        tm = TrackManager()
        tm.process_observation(_obs(
            source="ais", source_id="AAA", lat=51.5, lon=-0.1,
        ))
        tm.process_observation(_obs(
            source="ais", source_id="BBB", lat=52.5, lon=-0.1,
        ))
        # 51.5 to 52.5 is about 111 km -- only nearby should match
        nearby = tm.entities_near(51.5, -0.1, 1000)
        assert len(nearby) == 1

    def test_entities_by_domain(self):
        tm = TrackManager()
        tm.process_observation(_obs(source="ais", source_id="AAA", domain="sea"))
        tm.process_observation(_obs(source="adsb", source_id="BBB", domain="air"))
        tm.process_observation(_obs(source="cot", source_id="CCC", domain="land"))

        assert len(tm.entities_by_domain("sea")) == 1
        assert len(tm.entities_by_domain("air")) == 1
        assert len(tm.entities_by_domain("land")) == 1
        assert len(tm.entities_by_domain("space")) == 0

    def test_threats_filter(self):
        tm = TrackManager()
        e1 = tm.process_observation(_obs(source="ais", source_id="AAA"))
        e2 = tm.process_observation(_obs(source="ais", source_id="BBB"))
        e1.threat_level = 7
        e2.threat_level = 2

        threats = tm.threats(min_level=4)
        assert len(threats) == 1
        assert threats[0].entity_id == e1.entity_id

    def test_get_by_source(self):
        tm = TrackManager()
        e = tm.process_observation(_obs(source="ais", source_id="211234567"))
        found = tm.get_by_source("ais", "211234567")
        assert found is not None
        assert found.entity_id == e.entity_id

        assert tm.get_by_source("ais", "999999999") is None
        assert tm.get_by_source("adsb", "211234567") is None


# ===========================================================================
# Purge
# ===========================================================================


class TestPurge:
    def test_purge_removes_stale(self):
        tm = TrackManager()
        obs = _obs(source="ais", source_id="AAA", domain="sea")
        obs.timestamp = _now() - timedelta(seconds=600)
        tm.process_observation(obs)

        tm.process_observation(_obs(source="ais", source_id="BBB", domain="sea"))

        assert len(tm.all_entities) == 2
        removed = tm.purge_stale()
        assert removed == 1
        assert len(tm.all_entities) == 1

    def test_purge_cleans_source_index(self):
        tm = TrackManager()
        obs = _obs(source="ais", source_id="STALE1", domain="sea")
        obs.timestamp = _now() - timedelta(seconds=600)
        tm.process_observation(obs)

        assert tm.get_by_source("ais", "STALE1") is not None
        tm.purge_stale()
        assert tm.get_by_source("ais", "STALE1") is None


# ===========================================================================
# Stats
# ===========================================================================


class TestStats:
    def test_stats_counts(self):
        tm = TrackManager()
        tm.process_observation(_obs(source="ais", source_id="AAA", domain="sea"))
        tm.process_observation(_obs(source="adsb", source_id="BBB", domain="air"))

        stats = tm.stats
        assert stats["total_entities"] == 2
        assert stats["active_entities"] == 2
        assert stats["by_domain"]["sea"] == 1
        assert stats["by_domain"]["air"] == 1

    def test_observations_processed_counter(self):
        tm = TrackManager()
        tm.process_observation(_obs(source="ais", source_id="AAA"))
        tm.process_observation(_obs(source="ais", source_id="AAA"))
        tm.process_observation(_obs(source="ais", source_id="BBB"))

        assert tm.stats["observations_processed"] == 3

    def test_correlations_made_counter(self):
        tm = TrackManager(correlation_radius_m=1000)
        tm.process_observation(_obs(
            source="ais", source_id="AAA",
            lat=51.5, lon=-0.1, domain="sea", speed_mps=5.0,
        ))
        tm.process_observation(_obs(
            source="adsb", source_id="BBB",
            lat=51.5001, lon=-0.1001, domain="sea", speed_mps=5.0,
        ))
        assert tm.stats["correlations_made"] == 1


# ===========================================================================
# TrackedEntity properties
# ===========================================================================


class TestTrackedEntityProperties:
    def test_is_stale_air(self):
        e = TrackedEntity(entity_id="E1", domain="air")
        e.last_seen = _now() - timedelta(seconds=61)
        assert e.is_stale is True

        e.last_seen = _now() - timedelta(seconds=30)
        assert e.is_stale is False

    def test_is_stale_sea(self):
        e = TrackedEntity(entity_id="E1", domain="sea")
        e.last_seen = _now() - timedelta(seconds=301)
        assert e.is_stale is True

        e.last_seen = _now() - timedelta(seconds=100)
        assert e.is_stale is False

    def test_is_stale_default(self):
        e = TrackedEntity(entity_id="E1", domain="land")
        e.last_seen = _now() - timedelta(seconds=121)
        assert e.is_stale is True

        e.last_seen = _now() - timedelta(seconds=60)
        assert e.is_stale is False

    def test_is_multi_source(self):
        e = TrackedEntity(entity_id="E1")
        e.sources_seen = {"ais"}
        assert e.is_multi_source is False
        e.sources_seen = {"ais", "adsb"}
        assert e.is_multi_source is True

    def test_primary_id_prefers_callsign(self):
        e = TrackedEntity(entity_id="ENT-000001", callsign="ALPHA", name="Ship")
        assert e.primary_id == "ALPHA"

    def test_primary_id_falls_back_to_name(self):
        e = TrackedEntity(entity_id="ENT-000001", callsign="", name="Ship")
        assert e.primary_id == "Ship"

    def test_primary_id_falls_back_to_entity_id(self):
        e = TrackedEntity(entity_id="ENT-000001")
        assert e.primary_id == "ENT-000001"


# ===========================================================================
# Haversine sanity check
# ===========================================================================


class TestHaversine:
    def test_same_point_is_zero(self):
        d = TrackManager._haversine_m(51.5, -0.1, 51.5, -0.1)
        assert d == pytest.approx(0.0, abs=0.01)

    def test_known_distance(self):
        # London to Paris is roughly 344 km
        d = TrackManager._haversine_m(51.5074, -0.1278, 48.8566, 2.3522)
        assert 340_000 < d < 350_000
