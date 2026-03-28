"""Database persistence layer for the C2 engine.

PostgreSQL + PostGIS via SQLAlchemy 2.0 async and GeoAlchemy2.
"""

from mpe.db.engine import Database
from mpe.db.models import Base, TrackUpdate, Entity, Classification, Alert, AuditLog
from mpe.db.repository import (
    TrackRepository,
    EntityRepository,
    AlertRepository,
    AuditRepository,
)

__all__ = [
    "Database",
    "Base",
    "TrackUpdate",
    "Entity",
    "Classification",
    "Alert",
    "AuditLog",
    "TrackRepository",
    "EntityRepository",
    "AlertRepository",
    "AuditRepository",
]
