"""Geofencing system with violation alerts.

Provides keep-in, keep-out, and alert zones defined by polygonal boundaries.
Uses ray-casting algorithm for point-in-polygon checks -- pure Python, no
external dependencies.

Usage:
    manager = GeofenceManager()
    manager.add_zone(GeofenceZone(name="TEST", zone_type="keep_out", polygon=[...]))
    violations = manager.check("entity-1", lat, lon, domain="air")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

logger = logging.getLogger("mpe.geofence")


@dataclass(frozen=True)
class GeofenceZone:
    """A geofence zone defined by a polygon boundary."""

    name: str
    zone_type: Literal["keep_in", "keep_out", "alert"] = "alert"
    polygon: tuple[tuple[float, float], ...] | list[tuple[float, float]] = ()
    priority: int = 5
    domains: list[str] | None = None
    active: bool = True


@dataclass(frozen=True)
class GeofenceViolation:
    """Record of a geofence violation."""

    zone_name: str
    zone_type: str
    entity_id: str
    latitude: float
    longitude: float
    message: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


def point_in_polygon(
    lat: float, lon: float, polygon: list[tuple[float, float]] | tuple[tuple[float, float], ...],
) -> bool:
    """Determine if a point is inside a polygon using ray-casting.

    Vertices on the boundary are treated as inside.

    Args:
        lat: Latitude of the test point.
        lon: Longitude of the test point.
        polygon: Sequence of (lat, lon) vertices defining the polygon.

    Returns:
        True if the point is inside (or on the boundary of) the polygon.
    """
    n = len(polygon)
    if n < 3:
        return False

    # Check if the point lies exactly on any edge.
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        # Check collinearity via cross product.
        cross = (lat - x1) * (y2 - y1) - (lon - y1) * (x2 - x1)
        if abs(cross) < 1e-10:
            # Point is on the line -- check if it's within the segment.
            if min(x1, x2) - 1e-10 <= lat <= max(x1, x2) + 1e-10 and \
               min(y1, y2) - 1e-10 <= lon <= max(y1, y2) + 1e-10:
                return True

    # Standard ray-casting.
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > lon) != (yj > lon)) and \
           (lat < (xj - xi) * (lon - yi) / (yj - yi) + xi):
            inside = not inside
        j = i

    return inside


class GeofenceManager:
    """Manages geofence zones and checks entities against them."""

    def __init__(self) -> None:
        self._zones: dict[str, GeofenceZone] = {}

    def add_zone(self, zone: GeofenceZone) -> None:
        """Register a geofence zone."""
        self._zones[zone.name] = zone
        logger.info("Geofence added: %s (%s)", zone.name, zone.zone_type)

    def remove_zone(self, name: str) -> None:
        """Remove a geofence zone by name."""
        removed = self._zones.pop(name, None)
        if removed:
            logger.info("Geofence removed: %s", name)

    def check(
        self,
        entity_id: str,
        lat: float,
        lon: float,
        domain: str | None = None,
    ) -> list[GeofenceViolation]:
        """Check whether a single point violates any active zones.

        Args:
            entity_id: Identifier for the entity being checked.
            lat: Latitude of the entity.
            lon: Longitude of the entity.
            domain: Optional domain filter (air/sea/land).

        Returns:
            List of violations (may be empty).
        """
        violations: list[GeofenceViolation] = []

        for zone in self._zones.values():
            if not zone.active:
                continue

            # Domain filter: if the zone specifies domains, entity must match.
            if zone.domains is not None and domain is not None:
                if domain not in zone.domains:
                    continue

            inside = point_in_polygon(lat, lon, zone.polygon)

            if zone.zone_type == "keep_out" and inside:
                violations.append(GeofenceViolation(
                    zone_name=zone.name,
                    zone_type=zone.zone_type,
                    entity_id=entity_id,
                    latitude=lat,
                    longitude=lon,
                    message=f"{entity_id} entered keep-out zone {zone.name}",
                ))
            elif zone.zone_type == "keep_in" and not inside:
                violations.append(GeofenceViolation(
                    zone_name=zone.name,
                    zone_type=zone.zone_type,
                    entity_id=entity_id,
                    latitude=lat,
                    longitude=lon,
                    message=f"{entity_id} left keep-in zone {zone.name}",
                ))
            elif zone.zone_type == "alert" and inside:
                violations.append(GeofenceViolation(
                    zone_name=zone.name,
                    zone_type=zone.zone_type,
                    entity_id=entity_id,
                    latitude=lat,
                    longitude=lon,
                    message=f"{entity_id} entered alert zone {zone.name}",
                ))

        # Sort by zone priority (highest first).
        zone_lookup = self._zones
        violations.sort(
            key=lambda v: zone_lookup.get(v.zone_name, GeofenceZone(name="")).priority,
            reverse=True,
        )
        return violations

    def check_all(
        self,
        entities: list[dict],
    ) -> list[GeofenceViolation]:
        """Check all entities against all zones.

        Args:
            entities: List of dicts with keys: entity_id, latitude, longitude,
                      and optionally domain.

        Returns:
            Combined list of all violations.
        """
        all_violations: list[GeofenceViolation] = []
        for entity in entities:
            violations = self.check(
                entity_id=entity["entity_id"],
                lat=entity["latitude"],
                lon=entity["longitude"],
                domain=entity.get("domain"),
            )
            all_violations.extend(violations)
        return all_violations

    def load_from_dict(self, zones_config: list[dict]) -> None:
        """Load zones from a list of config dicts.

        Each dict should have keys matching GeofenceZone fields:
        name, zone_type, polygon, priority, domains, active.
        """
        for cfg in zones_config:
            polygon = [tuple(p) for p in cfg.get("polygon", [])]
            zone = GeofenceZone(
                name=cfg["name"],
                zone_type=cfg.get("zone_type", "alert"),
                polygon=polygon,
                priority=cfg.get("priority", 5),
                domains=cfg.get("domains"),
                active=cfg.get("active", True),
            )
            self.add_zone(zone)

    @property
    def zones(self) -> list[GeofenceZone]:
        """Return all registered zones."""
        return list(self._zones.values())


# ---------------------------------------------------------------------------
# Preset demo zones
# ---------------------------------------------------------------------------

DEMO_ZONES: list[GeofenceZone] = [
    GeofenceZone(
        name="CARTAGENA_HARBOUR",
        zone_type="alert",
        polygon=[(10.38, -75.58), (10.42, -75.58), (10.42, -75.50), (10.38, -75.50)],
        priority=7,
    ),
    GeofenceZone(
        name="STRAIT_OF_HORMUZ",
        zone_type="alert",
        polygon=[(25.5, 56.0), (26.5, 56.0), (26.5, 57.0), (25.5, 57.0)],
        priority=8,
        domains=["sea"],
    ),
    GeofenceZone(
        name="TAIWAN_STRAIT_ADIZ",
        zone_type="alert",
        polygon=[(23.5, 118.5), (25.5, 118.5), (25.5, 121.0), (23.5, 121.0)],
        priority=9,
    ),
    GeofenceZone(
        name="EPSOM_TEST_ZONE",
        zone_type="keep_in",
        polygon=[(51.33, -0.30), (51.40, -0.30), (51.40, -0.20), (51.33, -0.20)],
        priority=5,
    ),
]
