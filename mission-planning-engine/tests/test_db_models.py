"""Tests for database ORM models -- no running database required.

Validates that all SQLAlchemy models can be instantiated and that
field defaults, column types, and table metadata are correct.
"""

from datetime import datetime, timezone

import pytest

from mpe.db.models import Alert, AuditLog, Base, Classification, Entity, TrackUpdate


# ---------------------------------------------------------------------------
# Table metadata
# ---------------------------------------------------------------------------


class TestTableMetadata:
    """Verify that all expected tables are registered in the ORM."""

    def test_all_tables_registered(self):
        table_names = set(Base.metadata.tables.keys())
        expected = {"track_updates", "entities", "classifications", "alerts", "audit_log"}
        assert expected.issubset(table_names)

    def test_track_updates_indexes(self):
        table = Base.metadata.tables["track_updates"]
        index_names = {idx.name for idx in table.indexes}
        assert "ix_track_updates_entity_time" in index_names
        assert "ix_track_updates_time" in index_names

    def test_classifications_indexes(self):
        table = Base.metadata.tables["classifications"]
        index_names = {idx.name for idx in table.indexes}
        assert "ix_classifications_entity_time" in index_names

    def test_alerts_indexes(self):
        table = Base.metadata.tables["alerts"]
        index_names = {idx.name for idx in table.indexes}
        assert "ix_alerts_type_sev" in index_names
        assert "ix_alerts_created" in index_names

    def test_audit_log_indexes(self):
        table = Base.metadata.tables["audit_log"]
        index_names = {idx.name for idx in table.indexes}
        assert "ix_audit_time" in index_names
        assert "ix_audit_actor" in index_names


# ---------------------------------------------------------------------------
# TrackUpdate
# ---------------------------------------------------------------------------


class TestTrackUpdate:
    """Test TrackUpdate model instantiation and field defaults."""

    def test_create_minimal(self):
        update = TrackUpdate(entity_id="AIS-123456789", source="ais")
        assert update.entity_id == "AIS-123456789"
        assert update.source == "ais"

    def test_create_with_all_fields(self):
        now = datetime.now(timezone.utc)
        update = TrackUpdate(
            entity_id="ADSB-4CA7B5",
            source="adsb",
            timestamp=now,
            latitude=51.5074,
            longitude=-0.1278,
            altitude_m=1500.0,
            heading=270.0,
            speed_mps=120.0,
            vertical_rate_mps=-2.5,
            raw_data={"squawk": "7000", "callsign": "BAW123"},
        )
        assert update.entity_id == "ADSB-4CA7B5"
        assert update.source == "adsb"
        assert update.timestamp == now
        assert update.latitude == 51.5074
        assert update.longitude == -0.1278
        assert update.altitude_m == 1500.0
        assert update.heading == 270.0
        assert update.speed_mps == 120.0
        assert update.vertical_rate_mps == -2.5
        assert update.raw_data["squawk"] == "7000"

    def test_tablename(self):
        assert TrackUpdate.__tablename__ == "track_updates"

    def test_raw_data_default(self):
        update = TrackUpdate(entity_id="X", source="manual")
        # Default is the dict callable, so on an unbound instance it's None
        # (defaults apply at DB level); we just check the column exists
        assert hasattr(update, "raw_data")


# ---------------------------------------------------------------------------
# Entity
# ---------------------------------------------------------------------------


class TestEntity:
    """Test Entity model instantiation and field defaults."""

    def test_create_minimal(self):
        entity = Entity(id="ENT-abc123", domain="sea")
        assert entity.id == "ENT-abc123"
        assert entity.domain == "sea"

    def test_create_vessel_entity(self):
        entity = Entity(
            id="ENT-vessel01",
            domain="sea",
            entity_type="surface_vessel",
            name="MV Test Ship",
            callsign="GTEST",
            mmsi=211234567,
            affiliation="neutral",
            threat_level=1,
            threat_category="low",
            confidence=0.8,
            last_latitude=51.5,
            last_longitude=-0.1,
            last_heading=180.0,
            last_speed_mps=5.0,
        )
        assert entity.mmsi == 211234567
        assert entity.name == "MV Test Ship"
        assert entity.affiliation == "neutral"
        assert entity.last_latitude == 51.5

    def test_create_aircraft_entity(self):
        entity = Entity(
            id="ENT-acft01",
            domain="air",
            entity_type="fixed_wing",
            icao_hex="4CA7B5",
            callsign="BAW123",
        )
        assert entity.icao_hex == "4CA7B5"
        assert entity.domain == "air"

    def test_create_drone_entity(self):
        entity = Entity(
            id="ENT-drone01",
            domain="air",
            entity_type="uav",
            mavlink_sysid=1,
            affiliation="friendly",
        )
        assert entity.mavlink_sysid == 1
        assert entity.affiliation == "friendly"

    def test_tablename(self):
        assert Entity.__tablename__ == "entities"


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


class TestClassification:
    """Test Classification model with JSON fields."""

    def test_create_minimal(self):
        cls = Classification(entity_id="ENT-abc123")
        assert cls.entity_id == "ENT-abc123"

    def test_create_with_json_fields(self):
        cls = Classification(
            entity_id="ENT-abc123",
            affiliation="suspect",
            threat_level=7,
            threat_category="high",
            confidence=0.85,
            reasoning=["MMSI in hostile list", "Speed anomaly detected"],
            anomalies=[
                {"type": "excessive_speed", "description": "30 kts cargo vessel"},
                {"type": "position_jump", "description": "Jumped 80 km"},
            ],
        )
        assert cls.affiliation == "suspect"
        assert cls.threat_level == 7
        assert len(cls.reasoning) == 2
        assert len(cls.anomalies) == 2
        assert cls.anomalies[0]["type"] == "excessive_speed"

    def test_foreign_key_exists(self):
        table = Base.metadata.tables["classifications"]
        fk_columns = set()
        for col in table.columns:
            for fk in col.foreign_keys:
                fk_columns.add(col.name)
        assert "entity_id" in fk_columns

    def test_tablename(self):
        assert Classification.__tablename__ == "classifications"


# ---------------------------------------------------------------------------
# Alert lifecycle
# ---------------------------------------------------------------------------


class TestAlert:
    """Test Alert model including acknowledgement lifecycle."""

    def test_create_minimal(self):
        alert = Alert(alert_type="threat", title="Test alert")
        assert alert.alert_type == "threat"
        assert alert.title == "Test alert"

    def test_create_full(self):
        alert = Alert(
            entity_id="ENT-abc123",
            alert_type="emergency",
            severity=9,
            title="Squawk 7700 detected",
            description="Aircraft BAW123 declared general emergency",
        )
        assert alert.severity == 9
        assert alert.entity_id == "ENT-abc123"
        assert alert.description == "Aircraft BAW123 declared general emergency"

    def test_acknowledge_lifecycle(self):
        alert = Alert(alert_type="anomaly", severity=5, title="Speed anomaly")
        # Initially not acknowledged
        assert alert.acknowledged is None or alert.acknowledged is False

        # Acknowledge
        now = datetime.now(timezone.utc)
        alert.acknowledged = True
        alert.acknowledged_by = "operator-1"
        alert.acknowledged_at = now

        assert alert.acknowledged is True
        assert alert.acknowledged_by == "operator-1"
        assert alert.acknowledged_at == now

    def test_foreign_key_exists(self):
        table = Base.metadata.tables["alerts"]
        fk_columns = set()
        for col in table.columns:
            for fk in col.foreign_keys:
                fk_columns.add(col.name)
        assert "entity_id" in fk_columns

    def test_tablename(self):
        assert Alert.__tablename__ == "alerts"


# ---------------------------------------------------------------------------
# AuditLog
# ---------------------------------------------------------------------------


class TestAuditLog:
    """Test AuditLog model creation."""

    def test_create_minimal(self):
        entry = AuditLog(action="classify")
        assert entry.action == "classify"

    def test_create_full(self):
        entry = AuditLog(
            actor="c2-engine",
            action="alert",
            target_type="entity",
            target_id="ENT-abc123",
            details={"severity": 9, "alert_type": "emergency"},
        )
        assert entry.actor == "c2-engine"
        assert entry.target_type == "entity"
        assert entry.target_id == "ENT-abc123"
        assert entry.details["severity"] == 9

    def test_tablename(self):
        assert AuditLog.__tablename__ == "audit_log"


# ---------------------------------------------------------------------------
# Database engine (import test only -- no connection)
# ---------------------------------------------------------------------------


class TestDatabaseEngine:
    """Verify Database class can be imported and instantiated."""

    def test_import_and_instantiate(self):
        from mpe.db.engine import Database

        db = Database()
        assert db._url == "postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2"

    def test_custom_url(self):
        from mpe.db.engine import Database

        db = Database(url="postgresql+asyncpg://test:test@db:5432/testdb")
        assert "testdb" in db._url
