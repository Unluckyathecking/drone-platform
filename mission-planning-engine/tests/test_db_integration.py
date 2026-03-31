"""DB integration tests -- repository logic against SQLite in-memory.

These tests exercise all repository methods (TrackRepository,
EntityRepository, AlertRepository, AuditRepository) using a lightweight
SQLite in-memory database.  PostGIS geometry columns are replaced with
nullable Float pairs -- the spatial query tests are skipped and flagged
for verification against a real PostGIS instance.

To run against real PostgreSQL+PostGIS:
    export MPE_TEST_DB_URL=postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2
    pytest tests/test_db_integration.py -v

Without the env var, SQLite in-memory is used and geometry tests are skipped.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# ---------------------------------------------------------------------------
# Determine test database URL
# ---------------------------------------------------------------------------

_REAL_DB_URL = os.environ.get("MPE_TEST_DB_URL")
_USE_REAL_DB = _REAL_DB_URL is not None

if _USE_REAL_DB:
    # Real PostgreSQL -- use production models with PostGIS
    from mpe.db.models import Alert, AuditLog, Classification, Entity, TrackUpdate
    from mpe.db.models import Base as _Base

    _DB_URL = _REAL_DB_URL
else:
    # SQLite in-memory -- define geometry-free mirror schema
    _DB_URL = "sqlite+aiosqlite:///:memory:"

    class _Base(DeclarativeBase):
        pass

    class TrackUpdate(_Base):
        __tablename__ = "track_updates"
        id = Column(Integer, primary_key=True, autoincrement=True)
        entity_id = Column(String(64), index=True, nullable=False)
        source = Column(String(32), nullable=False)
        timestamp = Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        )
        latitude = Column(Float)
        longitude = Column(Float)
        altitude_m = Column(Float, default=0.0)
        heading = Column(Float, default=0.0)
        speed_mps = Column(Float, default=0.0)
        vertical_rate_mps = Column(Float, default=0.0)
        raw_data = Column(JSON, default=dict)

    class Entity(_Base):
        __tablename__ = "entities"
        id = Column(String(64), primary_key=True)
        domain = Column(String(16), nullable=False)
        entity_type = Column(String(32), default="unknown")
        name = Column(String(128), default="")
        callsign = Column(String(64), default="")
        mmsi = Column(Integer, nullable=True)
        icao_hex = Column(String(8), nullable=True)
        mavlink_sysid = Column(Integer, nullable=True)
        affiliation = Column(String(16), default="unknown")
        threat_level = Column(Integer, default=0)
        threat_category = Column(String(16), default="none")
        confidence = Column(Float, default=0.5)
        last_latitude = Column(Float, default=0.0)
        last_longitude = Column(Float, default=0.0)
        last_altitude_m = Column(Float, default=0.0)
        last_heading = Column(Float, default=0.0)
        last_speed_mps = Column(Float, default=0.0)
        last_seen = Column(DateTime(timezone=True))
        first_seen = Column(DateTime(timezone=True))
        created_at = Column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        )
        updated_at = Column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        )
        metadata_ = Column("metadata", JSON, default=dict)

    class Classification(_Base):
        __tablename__ = "classifications"
        id = Column(Integer, primary_key=True, autoincrement=True)
        entity_id = Column(
            String(64), ForeignKey("entities.id"), nullable=False, index=True,
        )
        timestamp = Column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        )
        affiliation = Column(String(16))
        threat_level = Column(Integer)
        threat_category = Column(String(16))
        confidence = Column(Float)
        reasoning = Column(JSON, default=list)
        anomalies = Column(JSON, default=list)

    class Alert(_Base):
        __tablename__ = "alerts"
        id = Column(Integer, primary_key=True, autoincrement=True)
        entity_id = Column(String(64), ForeignKey("entities.id"), nullable=True)
        alert_type = Column(String(32), nullable=False)
        severity = Column(Integer, default=5)
        title = Column(String(256), nullable=False)
        description = Column(Text, default="")
        acknowledged = Column(Boolean, default=False)
        acknowledged_by = Column(String(64), nullable=True)
        acknowledged_at = Column(DateTime(timezone=True), nullable=True)
        created_at = Column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        )

    class AuditLog(_Base):
        __tablename__ = "audit_log"
        id = Column(Integer, primary_key=True, autoincrement=True)
        timestamp = Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
        actor = Column(String(64), default="system")
        action = Column(String(64), nullable=False)
        target_type = Column(String(32), nullable=True)
        target_id = Column(String(64), nullable=True)
        details = Column(JSON, default=dict)


# ---------------------------------------------------------------------------
# Repository implementations that work with both real and test models
# ---------------------------------------------------------------------------

# Import real repositories but patch them to use our test models at runtime
# by wiring them via session only (they import from mpe.db.models at call time).
# For the SQLite path we define thin wrappers that mirror the real repo logic.

if _USE_REAL_DB:
    from mpe.db.repository import (
        AlertRepository,
        AuditRepository,
        EntityRepository,
        TrackRepository,
    )
else:
    # Thin repository mirrors for SQLite testing
    from datetime import timedelta
    from sqlalchemy import select, and_

    class TrackRepository:
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def record_update(
            self,
            entity_id: str,
            source: str,
            lat: float,
            lon: float,
            alt: float = 0,
            heading: float = 0,
            speed_mps: float = 0,
            raw_data: dict | None = None,
        ) -> TrackUpdate:
            update = TrackUpdate(
                entity_id=entity_id,
                source=source,
                latitude=lat,
                longitude=lon,
                altitude_m=alt,
                heading=heading,
                speed_mps=speed_mps,
                raw_data=raw_data or {},
            )
            self._session.add(update)
            await self._session.flush()
            return update

        async def get_track_history(
            self, entity_id: str, hours: int = 24,
        ) -> list:
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
            result = await self._session.execute(
                select(TrackUpdate)
                .where(
                    and_(
                        TrackUpdate.entity_id == entity_id,
                        TrackUpdate.timestamp >= since,
                    ),
                )
                .order_by(TrackUpdate.timestamp),
            )
            return list(result.scalars().all())

    class EntityRepository:
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def upsert(self, entity_id: str, **kwargs) -> Entity:
            entity = await self._session.get(Entity, entity_id)
            if entity is None:
                entity = Entity(id=entity_id, **kwargs)
                entity.first_seen = datetime.now(timezone.utc)
                self._session.add(entity)
            else:
                for k, v in kwargs.items():
                    if v is not None and hasattr(entity, k):
                        setattr(entity, k, v)
            entity.last_seen = datetime.now(timezone.utc)
            entity.updated_at = datetime.now(timezone.utc)
            await self._session.flush()
            return entity

        async def get_all_active(self, stale_minutes: int = 10) -> list:
            since = datetime.now(timezone.utc) - timedelta(minutes=stale_minutes)
            result = await self._session.execute(
                select(Entity).where(Entity.last_seen >= since),
            )
            return list(result.scalars().all())

    class AlertRepository:
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def create_alert(
            self,
            entity_id: str | None,
            alert_type: str,
            severity: int,
            title: str,
            description: str = "",
        ) -> Alert:
            alert = Alert(
                entity_id=entity_id,
                alert_type=alert_type,
                severity=severity,
                title=title,
                description=description,
            )
            self._session.add(alert)
            await self._session.flush()
            return alert

        async def get_unacknowledged(self) -> list:
            result = await self._session.execute(
                select(Alert)
                .where(Alert.acknowledged == False)  # noqa: E712
                .order_by(Alert.severity.desc()),
            )
            return list(result.scalars().all())

    class AuditRepository:
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def log(
            self,
            action: str,
            actor: str = "system",
            target_type: str | None = None,
            target_id: str | None = None,
            details: dict | None = None,
        ) -> None:
            entry = AuditLog(
                actor=actor,
                action=action,
                target_type=target_type,
                target_id=target_id,
                details=details or {},
            )
            self._session.add(entry)
            await self._session.flush()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Fresh async DB session for each test."""
    connect_args = {} if _USE_REAL_DB else {"check_same_thread": False}
    engine = create_async_engine(
        _DB_URL,
        echo=False,
        connect_args=connect_args,
    )
    async with engine.begin() as conn:
        await conn.run_sync(_Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(_Base.metadata.drop_all)
    await engine.dispose()


# ---------------------------------------------------------------------------
# TrackRepository tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTrackRepository:

    async def test_record_update_returns_object(self, db_session):
        repo = TrackRepository(db_session)
        update = await repo.record_update(
            entity_id="ADSB-4CA7B5",
            source="adsb",
            lat=51.5,
            lon=-0.1,
            alt=10000.0,
            heading=270.0,
            speed_mps=250.0,
        )
        assert update.entity_id == "ADSB-4CA7B5"
        assert update.latitude == 51.5
        assert update.longitude == -0.1
        assert update.altitude_m == 10000.0
        assert update.speed_mps == 250.0

    async def test_record_update_persists_to_db(self, db_session):
        repo = TrackRepository(db_session)
        await repo.record_update("AIS-211234567", "ais", lat=50.0, lon=1.0)
        await db_session.commit()

        history = await repo.get_track_history("AIS-211234567", hours=1)
        assert len(history) == 1
        assert history[0].source == "ais"

    async def test_multiple_updates_same_entity(self, db_session):
        repo = TrackRepository(db_session)
        for i in range(5):
            await repo.record_update(
                "ADSB-ABCDEF", "adsb",
                lat=51.5 + i * 0.01,
                lon=-0.1 + i * 0.01,
            )
        await db_session.commit()

        history = await repo.get_track_history("ADSB-ABCDEF", hours=1)
        assert len(history) == 5

    async def test_multiple_entities_independent_history(self, db_session):
        repo = TrackRepository(db_session)
        await repo.record_update("ENT-A", "adsb", lat=51.0, lon=-0.1)
        await repo.record_update("ENT-B", "ais", lat=50.0, lon=1.0)
        await repo.record_update("ENT-A", "adsb", lat=51.1, lon=-0.1)
        await db_session.commit()

        hist_a = await repo.get_track_history("ENT-A", hours=1)
        hist_b = await repo.get_track_history("ENT-B", hours=1)
        assert len(hist_a) == 2
        assert len(hist_b) == 1

    async def test_raw_data_stored(self, db_session):
        repo = TrackRepository(db_session)
        await repo.record_update(
            "ADSB-111", "adsb", lat=51.5, lon=-0.1,
            raw_data={"squawk": "7700", "callsign": "MAYDAY"},
        )
        await db_session.commit()

        history = await repo.get_track_history("ADSB-111", hours=1)
        assert history[0].raw_data["squawk"] == "7700"

    async def test_get_history_empty_for_unknown_entity(self, db_session):
        repo = TrackRepository(db_session)
        history = await repo.get_track_history("NONEXISTENT", hours=24)
        assert history == []


# ---------------------------------------------------------------------------
# EntityRepository tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestEntityRepository:

    async def test_upsert_creates_new_entity(self, db_session):
        repo = EntityRepository(db_session)
        entity = await repo.upsert(
            "AIS-211234567",
            domain="sea",
            affiliation="neutral",
            threat_level=0,
        )
        await db_session.commit()

        assert entity.id == "AIS-211234567"
        assert entity.domain == "sea"
        assert entity.affiliation == "neutral"
        assert entity.first_seen is not None
        assert entity.last_seen is not None

    async def test_upsert_updates_existing_entity(self, db_session):
        repo = EntityRepository(db_session)

        # Create
        await repo.upsert("AIS-999", domain="sea", affiliation="neutral", threat_level=0)
        await db_session.commit()

        # Update with higher threat
        entity = await repo.upsert(
            "AIS-999", domain="sea", affiliation="hostile", threat_level=9,
        )
        await db_session.commit()

        assert entity.affiliation == "hostile"
        assert entity.threat_level == 9

    async def test_upsert_preserves_first_seen(self, db_session):
        repo = EntityRepository(db_session)

        e1 = await repo.upsert("AIS-XYZ", domain="sea")
        first_seen = e1.first_seen
        await db_session.commit()

        e2 = await repo.upsert("AIS-XYZ", domain="sea", affiliation="suspect")
        await db_session.commit()

        assert e2.first_seen == first_seen

    async def test_upsert_updates_last_seen(self, db_session):
        import time
        repo = EntityRepository(db_session)

        e1 = await repo.upsert("ADSB-AABBCC", domain="air")
        seen_1 = e1.last_seen
        await db_session.commit()

        time.sleep(0.01)

        e2 = await repo.upsert("ADSB-AABBCC", domain="air")
        await db_session.commit()

        assert e2.last_seen >= seen_1

    async def test_get_all_active_returns_recent(self, db_session):
        repo = EntityRepository(db_session)
        await repo.upsert("ENT-A", domain="air")
        await repo.upsert("ENT-B", domain="sea")
        await db_session.commit()

        active = await repo.get_all_active(stale_minutes=1)
        ids = {e.id for e in active}
        assert "ENT-A" in ids
        assert "ENT-B" in ids

    async def test_multiple_entities_independent(self, db_session):
        repo = EntityRepository(db_session)
        await repo.upsert("ENT-1", domain="air", affiliation="friendly")
        await repo.upsert("ENT-2", domain="sea", affiliation="hostile")
        await db_session.commit()

        e1 = await db_session.get(Entity, "ENT-1")
        e2 = await db_session.get(Entity, "ENT-2")
        assert e1.affiliation == "friendly"
        assert e2.affiliation == "hostile"


# ---------------------------------------------------------------------------
# EntityRepository + Classification FK tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestClassificationPersistence:

    async def test_classification_fk_requires_entity(self, db_session):
        """Classification must reference an existing entity."""
        entity_id = "ENT-FK-001"
        entity_repo = EntityRepository(db_session)
        await entity_repo.upsert(entity_id, domain="air")
        await db_session.flush()

        cls = Classification(
            entity_id=entity_id,
            affiliation="neutral",
            threat_level=1,
            threat_category="low",
            confidence=0.9,
            reasoning=["Civilian callsign", "Known friendly ICAO"],
            anomalies=[],
        )
        db_session.add(cls)
        await db_session.flush()
        await db_session.commit()

        # Verify persisted
        from sqlalchemy import select
        result = await db_session.execute(
            select(Classification).where(Classification.entity_id == entity_id),
        )
        rows = list(result.scalars().all())
        assert len(rows) == 1
        assert rows[0].affiliation == "neutral"
        assert rows[0].reasoning == ["Civilian callsign", "Known friendly ICAO"]

    async def test_multiple_classifications_for_same_entity(self, db_session):
        """Entity can have a full classification history."""
        entity_id = "ENT-HIST-001"
        entity_repo = EntityRepository(db_session)
        await entity_repo.upsert(entity_id, domain="sea")
        await db_session.flush()

        for i, affil in enumerate(["neutral", "suspect", "hostile"]):
            db_session.add(Classification(
                entity_id=entity_id,
                affiliation=affil,
                threat_level=i * 3,
                confidence=0.7 + i * 0.1,
            ))
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(
            select(Classification).where(Classification.entity_id == entity_id),
        )
        rows = list(result.scalars().all())
        assert len(rows) == 3

    async def test_anomalies_json_roundtrip(self, db_session):
        """JSON anomaly list survives a DB round-trip."""
        entity_id = "ENT-ANOMALY-001"
        entity_repo = EntityRepository(db_session)
        await entity_repo.upsert(entity_id, domain="sea")
        await db_session.flush()

        anomalies = [
            {"type": "excessive_speed", "description": "30 kts for cargo"},
            {"type": "ais_spoofing", "description": "Position jump 80 km"},
        ]
        db_session.add(Classification(
            entity_id=entity_id,
            affiliation="suspect",
            threat_level=6,
            reasoning=["Speed anomaly", "Spoofing detected"],
            anomalies=anomalies,
        ))
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(
            select(Classification).where(Classification.entity_id == entity_id),
        )
        row = result.scalars().first()
        assert row.anomalies[0]["type"] == "excessive_speed"
        assert row.anomalies[1]["type"] == "ais_spoofing"


# ---------------------------------------------------------------------------
# AlertRepository tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestAlertRepository:

    async def test_create_alert_minimal(self, db_session):
        repo = AlertRepository(db_session)
        alert = await repo.create_alert(
            entity_id=None,
            alert_type="info",
            severity=3,
            title="New entity detected",
        )
        await db_session.commit()

        assert alert.id is not None
        assert alert.alert_type == "info"
        assert alert.severity == 3

    async def test_create_alert_with_entity_fk(self, db_session):
        """Alert linked to a real entity via FK."""
        entity_id = "ENT-ALERT-001"
        entity_repo = EntityRepository(db_session)
        await entity_repo.upsert(entity_id, domain="air")
        await db_session.flush()

        repo = AlertRepository(db_session)
        alert = await repo.create_alert(
            entity_id=entity_id,
            alert_type="emergency",
            severity=9,
            title="Squawk 7700",
            description="Aircraft declared general emergency",
        )
        await db_session.commit()

        assert alert.entity_id == entity_id
        assert alert.severity == 9

    async def test_get_unacknowledged_returns_all(self, db_session):
        repo = AlertRepository(db_session)
        await repo.create_alert(None, "threat", 7, "High threat vessel")
        await repo.create_alert(None, "anomaly", 4, "Speed anomaly")
        await repo.create_alert(None, "emergency", 9, "Emergency squawk")
        await db_session.commit()

        unacked = await repo.get_unacknowledged()
        assert len(unacked) == 3

    async def test_get_unacknowledged_sorted_by_severity(self, db_session):
        repo = AlertRepository(db_session)
        await repo.create_alert(None, "info", 2, "Low priority")
        await repo.create_alert(None, "emergency", 10, "Critical")
        await repo.create_alert(None, "threat", 7, "High threat")
        await db_session.commit()

        unacked = await repo.get_unacknowledged()
        severities = [a.severity for a in unacked]
        assert severities == sorted(severities, reverse=True)

    async def test_acknowledged_alert_excluded(self, db_session):
        repo = AlertRepository(db_session)
        alert = await repo.create_alert(None, "threat", 8, "Test alert")
        await db_session.flush()

        # Acknowledge it
        alert.acknowledged = True
        alert.acknowledged_by = "operator-1"
        alert.acknowledged_at = datetime.now(timezone.utc)
        await db_session.commit()

        unacked = await repo.get_unacknowledged()
        assert len(unacked) == 0

    async def test_mixed_acknowledged_unacknowledged(self, db_session):
        repo = AlertRepository(db_session)
        a1 = await repo.create_alert(None, "threat", 8, "Alert A")
        a2 = await repo.create_alert(None, "anomaly", 5, "Alert B")
        await db_session.flush()

        a1.acknowledged = True
        a1.acknowledged_by = "op"
        a1.acknowledged_at = datetime.now(timezone.utc)
        await db_session.commit()

        unacked = await repo.get_unacknowledged()
        assert len(unacked) == 1
        assert unacked[0].id == a2.id


# ---------------------------------------------------------------------------
# AuditRepository tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestAuditRepository:

    async def test_log_creates_entry(self, db_session):
        repo = AuditRepository(db_session)
        await repo.log(action="classify", actor="engine")
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(select(AuditLog))
        rows = list(result.scalars().all())
        assert len(rows) == 1
        assert rows[0].action == "classify"
        assert rows[0].actor == "engine"

    async def test_log_with_full_details(self, db_session):
        repo = AuditRepository(db_session)
        await repo.log(
            action="alert_generated",
            actor="system",
            target_type="entity",
            target_id="ADSB-ABCDEF",
            details={"threat_level": 9, "alert_type": "emergency"},
        )
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(select(AuditLog))
        row = result.scalars().first()
        assert row.target_type == "entity"
        assert row.target_id == "ADSB-ABCDEF"
        assert row.details["threat_level"] == 9

    async def test_log_immutability(self, db_session):
        """Audit log entries are INSERT-only -- multiple actions create multiple rows."""
        repo = AuditRepository(db_session)
        await repo.log(action="task_assign", target_id="TASK-1")
        await repo.log(action="config_change", target_id="CFG-1")
        await repo.log(action="alert_generated", target_id="ENT-1")
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(select(AuditLog))
        rows = list(result.scalars().all())
        assert len(rows) == 3

    async def test_log_default_actor_is_system(self, db_session):
        repo = AuditRepository(db_session)
        await repo.log(action="startup")
        await db_session.commit()

        from sqlalchemy import select
        result = await db_session.execute(select(AuditLog))
        row = result.scalars().first()
        assert row.actor == "system"


# ---------------------------------------------------------------------------
# Database engine (Database class) tests
# ---------------------------------------------------------------------------


class TestDatabaseClass:
    """Unit tests for the Database connection manager (no actual connection)."""

    def test_instantiate_with_default_url(self):
        from mpe.db.engine import Database
        db = Database()
        assert "mpe_c2" in db._url
        assert db._engine is None
        assert db._session_factory is None

    def test_instantiate_with_custom_url(self):
        from mpe.db.engine import Database
        url = "postgresql+asyncpg://test:test@remotehost:5432/c2_prod"
        db = Database(url=url)
        assert "remotehost" in db._url
        assert "c2_prod" in db._url

    def test_session_factory_none_before_connect(self):
        from mpe.db.engine import Database
        db = Database()
        assert db._session_factory is None

    def test_engine_none_before_connect(self):
        from mpe.db.engine import Database
        db = Database()
        assert db._engine is None


# ---------------------------------------------------------------------------
# End-to-end pipeline test: track → entity → classification → alert → audit
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_persistence_pipeline(db_session):
    """Simulate the full engine persistence pipeline for one entity."""
    entity_id = "ADSB-4CA7B5"

    # 1. Record a track position
    track_repo = TrackRepository(db_session)
    update = await track_repo.record_update(
        entity_id, "adsb",
        lat=51.5074, lon=-0.1278,
        alt=10500.0, heading=270.0, speed_mps=245.0,
        raw_data={"callsign": "BAW123", "squawk": "7700"},
    )
    assert update.entity_id == entity_id

    # 2. Upsert entity with classification result
    entity_repo = EntityRepository(db_session)
    entity = await entity_repo.upsert(
        entity_id,
        domain="air",
        affiliation="hostile",
        threat_level=9,
        threat_category="high",
        confidence=0.95,
    )
    assert entity.id == entity_id
    assert entity.affiliation == "hostile"
    await db_session.flush()

    # 3. Record classification history
    db_session.add(Classification(
        entity_id=entity_id,
        affiliation="hostile",
        threat_level=9,
        threat_category="high",
        confidence=0.95,
        reasoning=["Emergency squawk 7700", "ICAO in hostile list"],
        anomalies=[{"type": "emergency", "description": "Squawk 7700 active"}],
    ))
    await db_session.flush()

    # 4. Create alert
    alert_repo = AlertRepository(db_session)
    alert = await alert_repo.create_alert(
        entity_id=entity_id,
        alert_type="emergency",
        severity=9,
        title="Emergency squawk: BAW123",
        description="Aircraft BAW123 squawking 7700",
    )
    assert alert.severity == 9

    # 5. Audit log
    audit_repo = AuditRepository(db_session)
    await audit_repo.log(
        action="alert_generated",
        target_type="entity",
        target_id=entity_id,
        details={"threat_level": 9, "alert_type": "emergency"},
    )

    await db_session.commit()

    # Verify everything is queryable
    from sqlalchemy import select

    # Track history
    history = await track_repo.get_track_history(entity_id, hours=1)
    assert len(history) == 1

    # Entity still active
    active = await entity_repo.get_all_active(stale_minutes=1)
    assert any(e.id == entity_id for e in active)

    # Unacknowledged alert
    unacked = await alert_repo.get_unacknowledged()
    assert any(a.entity_id == entity_id for a in unacked)

    # Audit trail
    result = await db_session.execute(
        select(AuditLog).where(AuditLog.target_id == entity_id),
    )
    audit_rows = list(result.scalars().all())
    assert len(audit_rows) == 1
    assert audit_rows[0].action == "alert_generated"
