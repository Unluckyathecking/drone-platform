"""Repository pattern -- all database queries go through here."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from mpe.db.models import Alert, AuditLog, Classification, Entity, TrackUpdate


class TrackRepository:
    """Data access for track position updates."""

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
        """Record a track position update."""
        update = TrackUpdate(
            entity_id=entity_id,
            source=source,
            latitude=lat,
            longitude=lon,
            altitude_m=alt,
            heading=heading,
            speed_mps=speed_mps,
            position=f"SRID=4326;POINT({lon} {lat})",
            raw_data=raw_data or {},
        )
        self._session.add(update)
        await self._session.flush()
        return update

    async def get_track_history(
        self, entity_id: str, hours: int = 24,
    ) -> list[TrackUpdate]:
        """Get position history for an entity."""
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
    """Data access for resolved entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(self, entity_id: str, **kwargs) -> Entity:
        """Create or update an entity."""
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

    async def get_entities_near(
        self, lat: float, lon: float, radius_km: float,
    ) -> list[Entity]:
        """Find entities within radius using PostGIS."""
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        result = await self._session.execute(
            select(Entity).where(
                func.ST_DWithin(
                    Entity.last_position,
                    func.ST_Geography(point),
                    radius_km * 1000,  # ST_DWithin uses metres for geography
                ),
            ),
        )
        return list(result.scalars().all())

    async def get_all_active(self, stale_minutes: int = 10) -> list[Entity]:
        """Get all entities seen within stale_minutes."""
        since = datetime.now(timezone.utc) - timedelta(minutes=stale_minutes)
        result = await self._session.execute(
            select(Entity).where(Entity.last_seen >= since),
        )
        return list(result.scalars().all())


class AlertRepository:
    """Data access for alerts."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_alert(
        self,
        entity_id: str,
        alert_type: str,
        severity: int,
        title: str,
        description: str = "",
    ) -> Alert:
        """Create a new alert."""
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

    async def get_unacknowledged(self) -> list[Alert]:
        """Get all unacknowledged alerts, highest severity first."""
        result = await self._session.execute(
            select(Alert)
            .where(Alert.acknowledged == False)  # noqa: E712
            .order_by(Alert.severity.desc()),
        )
        return list(result.scalars().all())


class AuditRepository:
    """Data access for the immutable audit trail."""

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
        """Record an audit log entry."""
        entry = AuditLog(
            actor=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details or {},
        )
        self._session.add(entry)
        await self._session.flush()
