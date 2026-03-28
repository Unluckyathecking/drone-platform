"""Tests for the MPE Core Engine -- the headless C2 daemon.

Tests cover:
- EngineConfig defaults and custom values
- CoreEngine creation and component wiring
- Classification of mock tracks
- Stale track purging
- Stats tracking
- IngestSource protocol compliance of existing receivers
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from mpe.engine import CoreEngine, EngineConfig


# ---------------------------------------------------------------------------
# EngineConfig tests
# ---------------------------------------------------------------------------


class TestEngineConfig:
    """Test EngineConfig dataclass defaults and custom values."""

    def test_defaults(self) -> None:
        config = EngineConfig()

        assert config.adsb_enabled is True
        assert config.adsb_source == "airplanes_live"
        assert config.adsb_center_lat == 51.3632
        assert config.adsb_center_lon == -0.2652
        assert config.adsb_radius_nm == 250
        assert config.adsb_poll_interval_s == 10.0

        assert config.ais_enabled is False
        assert config.ais_udp_port == 5050

        assert config.cot_enabled is True
        assert config.cot_url == "udp+wo://239.2.3.1:6969"
        assert config.cot_callsign == "MPE-ENGINE"
        assert config.cot_stale_seconds == 120

        assert config.known_friendly_mmsis == set()
        assert config.known_hostile_mmsis == set()
        assert config.known_friendly_icaos == set()

        assert config.classify_interval_s == 5.0
        assert config.output_interval_s == 5.0
        assert config.purge_interval_s == 60.0
        assert config.log_level == "INFO"

    def test_custom_values(self) -> None:
        config = EngineConfig(
            adsb_enabled=False,
            adsb_source="opensky",
            adsb_center_lat=26.0,
            adsb_center_lon=56.5,
            adsb_radius_nm=100,
            adsb_poll_interval_s=30.0,
            ais_enabled=True,
            ais_udp_port=6060,
            cot_enabled=False,
            cot_url="tcp://takserver:8087",
            cot_callsign="ALPHA-1",
            cot_stale_seconds=300,
            known_friendly_mmsis={123456789},
            known_hostile_mmsis={987654321},
            known_friendly_icaos={"AABBCC"},
            classify_interval_s=10.0,
            output_interval_s=15.0,
            purge_interval_s=120.0,
            log_level="DEBUG",
        )

        assert config.adsb_enabled is False
        assert config.adsb_source == "opensky"
        assert config.adsb_center_lat == 26.0
        assert config.adsb_center_lon == 56.5
        assert config.adsb_radius_nm == 100
        assert config.ais_enabled is True
        assert config.ais_udp_port == 6060
        assert config.cot_enabled is False
        assert config.cot_url == "tcp://takserver:8087"
        assert config.cot_callsign == "ALPHA-1"
        assert config.known_friendly_mmsis == {123456789}
        assert config.known_hostile_mmsis == {987654321}
        assert config.known_friendly_icaos == {"AABBCC"}
        assert config.classify_interval_s == 10.0
        assert config.log_level == "DEBUG"

    def test_set_fields_are_independent(self) -> None:
        """Each config instance should have its own set instances."""
        config_a = EngineConfig()
        config_b = EngineConfig()
        config_a.known_friendly_mmsis.add(111)

        assert 111 not in config_b.known_friendly_mmsis


# ---------------------------------------------------------------------------
# CoreEngine creation tests
# ---------------------------------------------------------------------------


class TestCoreEngineCreation:
    """Test CoreEngine initialization and component wiring."""

    def test_default_creation(self) -> None:
        engine = CoreEngine()

        assert engine.running is False
        assert engine.aircraft_tracker is not None
        assert engine.vessel_tracker is not None

    def test_custom_config_creation(self) -> None:
        config = EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
            log_level="WARNING",
        )
        engine = CoreEngine(config)

        assert engine.running is False
        assert engine._config is config

    def test_stats_initial_values(self) -> None:
        engine = CoreEngine()
        stats = engine.stats

        assert stats["aircraft_tracked"] == 0
        assert stats["vessels_tracked"] == 0
        assert stats["cot_events_sent"] == 0
        assert stats["classifications_run"] == 0
        assert stats["alerts_generated"] == 0
        assert stats["uptime_start"] is None

    def test_stats_returns_copy(self) -> None:
        """Modifying the returned stats dict must not affect the engine."""
        engine = CoreEngine()
        stats = engine.stats
        stats["aircraft_tracked"] = 999

        assert engine.stats["aircraft_tracked"] == 0


# ---------------------------------------------------------------------------
# Classification tests
# ---------------------------------------------------------------------------


class TestClassifyAll:
    """Test CoreEngine._classify_all with mock tracks."""

    def test_classify_aircraft_tracks(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        # Insert a mock aircraft track
        engine.aircraft_tracker.update(
            icao_hex="AABBCC",
            latitude=51.5,
            longitude=-0.1,
            altitude_baro_ft=35000,
            ground_speed_kts=450,
            callsign="BAW123",
            squawk="1234",
        )

        engine._classify_all()

        assert int(engine.stats["classifications_run"]) == 1
        tracks = engine.aircraft_tracker.active_tracks
        assert len(tracks) == 1
        assert hasattr(tracks[0], "_classification")
        assert tracks[0]._classification.affiliation == "neutral"

    def test_classify_vessel_tracks(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        engine.vessel_tracker.update(
            mmsi=211000001,
            latitude=51.0,
            longitude=1.0,
            speed_over_ground=12.0,
            ship_type=70,
            vessel_name="CARGO ONE",
        )

        engine._classify_all()

        assert int(engine.stats["classifications_run"]) == 1
        tracks = engine.vessel_tracker.active_tracks
        assert len(tracks) == 1
        assert hasattr(tracks[0], "_classification")

    def test_classify_hostile_vessel_generates_alert(self) -> None:
        config = EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
            known_hostile_mmsis={999000001},
        )
        engine = CoreEngine(config)

        engine.vessel_tracker.update(
            mmsi=999000001,
            latitude=25.0,
            longitude=55.0,
            speed_over_ground=8.0,
        )

        engine._classify_all()

        assert int(engine.stats["alerts_generated"]) >= 1
        track = engine.vessel_tracker.active_tracks[0]
        assert track._classification.affiliation == "hostile"
        assert track._classification.threat_level >= 7

    def test_classify_emergency_squawk_generates_alert(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        engine.aircraft_tracker.update(
            icao_hex="ABCDEF",
            latitude=51.5,
            longitude=-0.1,
            altitude_baro_ft=10000,
            squawk="7700",
            callsign="MAYDAY",
        )

        engine._classify_all()

        assert int(engine.stats["alerts_generated"]) >= 1
        track = engine.aircraft_tracker.active_tracks[0]
        assert track._classification.threat_level >= 7

    def test_classify_mixed_tracks(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        engine.aircraft_tracker.update(
            icao_hex="AA0001",
            latitude=51.0,
            longitude=-0.5,
        )
        engine.aircraft_tracker.update(
            icao_hex="AA0002",
            latitude=51.1,
            longitude=-0.4,
        )
        engine.vessel_tracker.update(
            mmsi=200000001,
            latitude=50.0,
            longitude=0.0,
        )

        engine._classify_all()

        assert int(engine.stats["classifications_run"]) == 3


# ---------------------------------------------------------------------------
# CoT output tests
# ---------------------------------------------------------------------------


class TestOutputCoT:
    """Test CoreEngine._output_cot with real bridges."""

    def test_output_cot_counts_events(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        # Add tracks with valid positions (not 0,0 which are skipped)
        engine.aircraft_tracker.update(
            icao_hex="AABBCC",
            latitude=51.5,
            longitude=-0.1,
            altitude_baro_ft=35000,
            callsign="TEST1",
        )
        engine.vessel_tracker.update(
            mmsi=200000001,
            latitude=50.5,
            longitude=-1.0,
            vessel_name="TEST SHIP",
        )

        # Use a dummy cot_sender (the current implementation does not
        # actually call methods on it -- it just counts generated XML)
        dummy_sender = SimpleNamespace()
        engine._output_cot(dummy_sender)

        assert int(engine.stats["cot_events_sent"]) == 2

    def test_output_cot_skips_zero_position(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        # Track with no position (lat=0, lon=0) should be skipped
        engine.aircraft_tracker.update(icao_hex="DEAD01")

        dummy_sender = SimpleNamespace()
        engine._output_cot(dummy_sender)

        assert int(engine.stats["cot_events_sent"]) == 0


# ---------------------------------------------------------------------------
# Purge tests
# ---------------------------------------------------------------------------


class TestPurgeStale:
    """Test CoreEngine._purge_stale."""

    def test_purge_stale_aircraft(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        # Add a track and artificially age it
        track = engine.aircraft_tracker.update(
            icao_hex="STALE1",
            latitude=51.0,
            longitude=-0.5,
        )
        track.last_update = datetime.now(timezone.utc) - timedelta(seconds=120)

        assert len(engine.aircraft_tracker.all_tracks) == 1

        engine._purge_stale()

        assert len(engine.aircraft_tracker.all_tracks) == 0

    def test_purge_stale_vessels(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        track = engine.vessel_tracker.update(
            mmsi=300000001,
            latitude=50.0,
            longitude=0.0,
        )
        track.last_update = datetime.now(timezone.utc) - timedelta(seconds=600)

        assert len(engine.vessel_tracker.all_tracks) == 1

        engine._purge_stale()

        assert len(engine.vessel_tracker.all_tracks) == 0

    def test_purge_keeps_fresh_tracks(self) -> None:
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False,
            ais_enabled=False,
            cot_enabled=False,
        ))

        engine.aircraft_tracker.update(
            icao_hex="FRESH1",
            latitude=51.0,
            longitude=-0.5,
        )

        engine._purge_stale()

        assert len(engine.aircraft_tracker.all_tracks) == 1


# ---------------------------------------------------------------------------
# IngestSource protocol compliance
# ---------------------------------------------------------------------------


class TestIngestSourceProtocol:
    """Verify existing receivers satisfy the IngestSource protocol."""

    def test_adsb_receiver_has_stop(self) -> None:
        from mpe.adsb_receiver import ADSBReceiver
        from mpe.aircraft_tracker import AircraftTracker

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker)

        assert hasattr(receiver, "stop")
        assert callable(receiver.stop)
        assert hasattr(receiver, "start_polling")
        assert callable(receiver.start_polling)

    def test_ais_receiver_has_stop(self) -> None:
        from mpe.ais_receiver import AISReceiver
        from mpe.vessel_tracker import VesselTracker

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)

        assert hasattr(receiver, "stop")
        assert callable(receiver.stop)
        assert hasattr(receiver, "start_udp")
        assert callable(receiver.start_udp)


# ---------------------------------------------------------------------------
# Source setup tests
# ---------------------------------------------------------------------------


class TestSetupSources:
    """Test CoreEngine._setup_sources builds correct source lists."""

    def test_adsb_only(self) -> None:
        config = EngineConfig(adsb_enabled=True, ais_enabled=False)
        engine = CoreEngine(config)
        engine._setup_sources()

        assert len(engine._sources) == 1

    def test_both_sources(self) -> None:
        config = EngineConfig(adsb_enabled=True, ais_enabled=True)
        engine = CoreEngine(config)
        engine._setup_sources()

        assert len(engine._sources) == 2

    def test_no_sources(self) -> None:
        config = EngineConfig(adsb_enabled=False, ais_enabled=False)
        engine = CoreEngine(config)
        engine._setup_sources()

        assert len(engine._sources) == 0


# ---------------------------------------------------------------------------
# Database persistence tests (no actual PostgreSQL required)
# ---------------------------------------------------------------------------


class TestDatabaseConfig:
    """Test EngineConfig database fields and CoreEngine DB integration."""

    def test_db_disabled_by_default(self) -> None:
        config = EngineConfig()

        assert config.db_url is None
        assert config.db_enabled is False

    def test_db_url_configurable(self) -> None:
        url = "postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2"
        config = EngineConfig(db_url=url)

        assert config.db_url == url
        assert config.db_enabled is False  # Not enabled until connected

    def test_engine_db_none_by_default(self) -> None:
        engine = CoreEngine()

        assert engine._db is None
        assert engine._pending_db_ops == []

    def test_pending_db_ops_starts_empty(self) -> None:
        engine = CoreEngine(EngineConfig(db_url="postgresql+asyncpg://x:x@localhost/test"))

        assert engine._pending_db_ops == []
        assert engine._db is None  # Not connected until start()


class TestDbOpsQueue:
    """Test that DB operations are queued during classification."""

    def test_no_db_ops_without_db(self) -> None:
        """Without a DB configured, no ops should be queued."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))

        engine.aircraft_tracker.update(
            icao_hex="AABBCC", latitude=51.5, longitude=-0.1,
            altitude_baro_ft=35000, callsign="TEST1",
        )

        engine._classify_all()

        assert len(engine._pending_db_ops) == 0

    def test_ops_queued_with_db(self) -> None:
        """With a DB object set, classify should queue persistence ops."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))
        # Simulate DB being available (set a truthy sentinel)
        engine._db = object()

        engine.aircraft_tracker.update(
            icao_hex="AABBCC", latitude=51.5, longitude=-0.1,
            altitude_baro_ft=35000, callsign="TEST1",
        )

        engine._classify_all()

        # Should have queued at least track + classification ops
        assert len(engine._pending_db_ops) >= 2

    def test_ops_queued_for_vessels_with_db(self) -> None:
        """Vessel classification should also queue DB ops."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))
        engine._db = object()

        engine.vessel_tracker.update(
            mmsi=211000001, latitude=51.0, longitude=1.0,
            speed_over_ground=12.0, ship_type=70, vessel_name="CARGO ONE",
        )

        engine._classify_all()

        assert len(engine._pending_db_ops) >= 2

    def test_alert_ops_queued_for_high_threat(self) -> None:
        """High-threat classification should queue alert persistence."""
        config = EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
            known_hostile_mmsis={999000001},
        )
        engine = CoreEngine(config)
        engine._db = object()

        engine.vessel_tracker.update(
            mmsi=999000001, latitude=25.0, longitude=55.0,
            speed_over_ground=8.0,
        )

        engine._classify_all()

        # track + classification + alert = at least 3 ops
        assert len(engine._pending_db_ops) >= 3

    def test_ops_queued_for_emergency_squawk(self) -> None:
        """Emergency squawk aircraft should queue alert persistence."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))
        engine._db = object()

        engine.aircraft_tracker.update(
            icao_hex="ABCDEF", latitude=51.5, longitude=-0.1,
            altitude_baro_ft=10000, squawk="7700", callsign="MAYDAY",
        )

        engine._classify_all()

        # track + classification + alert = at least 3 ops
        assert len(engine._pending_db_ops) >= 3


class TestFlushDbOps:
    """Test _flush_db_ops edge cases."""

    def test_flush_noop_without_db(self) -> None:
        """Flush with no DB should be a no-op."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))
        engine._pending_db_ops.append(lambda s: None)

        asyncio.run(engine._flush_db_ops())

        # Ops remain because DB is None (they aren't executed)
        assert len(engine._pending_db_ops) == 1

    def test_flush_clears_queue_with_empty_ops(self) -> None:
        """Flush with DB but empty queue should be a no-op."""
        engine = CoreEngine(EngineConfig(
            adsb_enabled=False, ais_enabled=False, cot_enabled=False,
        ))
        engine._db = object()

        asyncio.run(engine._flush_db_ops())

        assert len(engine._pending_db_ops) == 0
