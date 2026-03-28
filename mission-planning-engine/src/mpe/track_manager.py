"""Track Manager -- unified entity registry with multi-source correlation.

Takes raw observations from any sensor (AIS, ADS-B, CoT, MAVLink) and
resolves them into a single set of tracked entities. This is the core
fusion layer that turns multiple noisy inputs into one coherent picture.

Algorithm (per observation):
1. Exact ID match -- MMSI, ICAO hex, CoT UID -> known entity
2. Spatial correlation -- if no ID match, search for entities within
   correlation_radius that have compatible domain/heading/speed
3. Create new -- if no correlation found, create new entity
4. Merge -- update matched entity with new observation data
5. Classify -- run classifier on updated entity
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger("mpe.track_manager")


@dataclass
class Observation:
    """A raw observation from any sensor source."""

    source: str              # "ais", "adsb", "cot", "mavlink", "manual"
    source_id: str           # Original ID from source (MMSI, ICAO hex, CoT UID)
    latitude: float
    longitude: float
    altitude_m: float = 0.0
    heading: float = 0.0
    speed_mps: float = 0.0

    # Identity hints (may be empty)
    callsign: str = ""
    name: str = ""
    entity_type: str = ""    # "fixed_wing", "surface_vessel", "person", etc.
    domain: str = ""         # "air", "sea", "land"

    # Source-specific metadata
    metadata: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class TrackedEntity:
    """A resolved entity in the operational picture.

    May have observations from multiple sources merged together.
    """

    entity_id: str           # Our internal ID: "ENT-{counter}"
    domain: str = "unknown"

    # Position (latest)
    latitude: float = 0.0
    longitude: float = 0.0
    altitude_m: float = 0.0
    heading: float = 0.0
    speed_mps: float = 0.0

    # Identity
    callsign: str = ""
    name: str = ""
    entity_type: str = ""
    affiliation: str = "unknown"
    threat_level: int = 0
    threat_category: str = "none"

    # Source tracking
    source_ids: dict[str, str] = field(default_factory=dict)  # {"ais": "211234567", "adsb": "4CA7B5"}
    sources_seen: set[str] = field(default_factory=set)
    observation_count: int = 0

    # Timing
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Classification
    anomalies: list = field(default_factory=list)
    reasoning: list = field(default_factory=list)
    confidence: float = 0.5

    # Metadata from all sources
    metadata: dict = field(default_factory=dict)

    @property
    def is_stale(self) -> bool:
        age = (datetime.now(timezone.utc) - self.last_seen).total_seconds()
        if self.domain == "air":
            return age > 60
        elif self.domain == "sea":
            return age > 300
        else:
            return age > 120

    @property
    def is_multi_source(self) -> bool:
        return len(self.sources_seen) > 1

    @property
    def primary_id(self) -> str:
        """Best human-readable identifier."""
        return self.callsign or self.name or self.entity_id


class TrackManager:
    """Unified entity registry with multi-source correlation.

    This is the core of the C2 system -- it maintains the single
    operational picture from all sensor inputs.
    """

    def __init__(
        self,
        correlation_radius_m: float = 500.0,
        correlation_time_window_s: float = 120.0,
        max_speed_diff_mps: float = 20.0,
    ):
        self._entities: dict[str, TrackedEntity] = {}

        # Index: source_type:source_id -> entity_id (for fast exact match)
        self._source_index: dict[str, str] = {}

        self._correlation_radius = correlation_radius_m
        self._correlation_time = correlation_time_window_s
        self._max_speed_diff = max_speed_diff_mps

        self._entity_counter = 0
        self._observations_processed = 0
        self._correlations_made = 0

    def process_observation(self, obs: Observation) -> TrackedEntity:
        """Process a new observation and return the matched/created entity.

        This is the main entry point -- called for every sensor update.
        """
        self._observations_processed += 1

        # Step 1: Exact ID match
        entity = self._exact_match(obs)

        # Step 2: Spatial correlation (if no exact match)
        if entity is None:
            entity = self._spatial_correlate(obs)
            if entity is not None:
                self._correlations_made += 1
                logger.debug(
                    "Correlated %s:%s -> %s (spatial, %s)",
                    obs.source,
                    obs.source_id,
                    entity.entity_id,
                    entity.primary_id,
                )

        # Step 3: Create new entity
        if entity is None:
            entity = self._create_entity(obs)
            logger.debug(
                "New entity: %s from %s:%s",
                entity.entity_id,
                obs.source,
                obs.source_id,
            )

        # Step 4: Merge observation data
        self._merge_observation(entity, obs)

        return entity

    def _exact_match(self, obs: Observation) -> TrackedEntity | None:
        """Look up entity by exact source ID."""
        key = f"{obs.source}:{obs.source_id}"
        entity_id = self._source_index.get(key)
        if entity_id and entity_id in self._entities:
            return self._entities[entity_id]
        return None

    def _spatial_correlate(self, obs: Observation) -> TrackedEntity | None:
        """Find a nearby entity that could be the same physical object.

        Criteria:
        - Within correlation_radius_m
        - Same domain (air/sea/land)
        - Compatible speed (within max_speed_diff_mps)
        - Last seen within correlation_time_window_s
        """
        if obs.latitude == 0.0 and obs.longitude == 0.0:
            return None

        best_match = None
        best_distance = float("inf")
        now = datetime.now(timezone.utc)

        for entity in self._entities.values():
            # Skip stale entities
            if (now - entity.last_seen).total_seconds() > self._correlation_time:
                continue

            # Domain must match (or be unknown)
            if obs.domain and entity.domain and obs.domain != entity.domain and entity.domain != "unknown":
                continue

            # Already has this source type -> probably different entity
            if obs.source in entity.source_ids and entity.source_ids[obs.source] != obs.source_id:
                continue

            # Distance check
            dist = self._haversine_m(
                obs.latitude, obs.longitude,
                entity.latitude, entity.longitude,
            )

            if dist > self._correlation_radius:
                continue

            # Speed compatibility
            if obs.speed_mps > 0 and entity.speed_mps > 0:
                speed_diff = abs(obs.speed_mps - entity.speed_mps)
                if speed_diff > self._max_speed_diff:
                    continue

            if dist < best_distance:
                best_distance = dist
                best_match = entity

        return best_match

    def _create_entity(self, obs: Observation) -> TrackedEntity:
        """Create a new tracked entity from an observation."""
        self._entity_counter += 1
        entity_id = f"ENT-{self._entity_counter:06d}"

        entity = TrackedEntity(
            entity_id=entity_id,
            domain=obs.domain or "unknown",
            latitude=obs.latitude,
            longitude=obs.longitude,
            altitude_m=obs.altitude_m,
            heading=obs.heading,
            speed_mps=obs.speed_mps,
            callsign=obs.callsign,
            name=obs.name,
            entity_type=obs.entity_type,
        )

        self._entities[entity_id] = entity

        # Index by source ID
        key = f"{obs.source}:{obs.source_id}"
        self._source_index[key] = entity_id

        return entity

    def _merge_observation(self, entity: TrackedEntity, obs: Observation):
        """Merge new observation data into existing entity."""
        # Update position
        if obs.latitude != 0.0 or obs.longitude != 0.0:
            entity.latitude = obs.latitude
            entity.longitude = obs.longitude
        if obs.altitude_m != 0.0:
            entity.altitude_m = obs.altitude_m
        if obs.heading != 0.0:
            entity.heading = obs.heading
        if obs.speed_mps != 0.0:
            entity.speed_mps = obs.speed_mps

        # Update identity (prefer non-empty values)
        if obs.callsign:
            entity.callsign = obs.callsign
        if obs.name:
            entity.name = obs.name
        if obs.entity_type:
            entity.entity_type = obs.entity_type
        if obs.domain and obs.domain != "unknown":
            entity.domain = obs.domain

        # Track sources
        key = f"{obs.source}:{obs.source_id}"
        self._source_index[key] = entity.entity_id
        entity.source_ids[obs.source] = obs.source_id
        entity.sources_seen.add(obs.source)
        entity.observation_count += 1
        entity.last_seen = obs.timestamp

        # Merge metadata
        entity.metadata.update(obs.metadata)

        # Increase confidence for multi-source
        if entity.is_multi_source:
            entity.confidence = min(0.95, 0.5 + 0.15 * len(entity.sources_seen))

    # -- Query methods --

    @property
    def active_entities(self) -> list[TrackedEntity]:
        return [e for e in self._entities.values() if not e.is_stale]

    @property
    def all_entities(self) -> list[TrackedEntity]:
        return list(self._entities.values())

    def get(self, entity_id: str) -> TrackedEntity | None:
        return self._entities.get(entity_id)

    def get_by_source(self, source: str, source_id: str) -> TrackedEntity | None:
        key = f"{source}:{source_id}"
        entity_id = self._source_index.get(key)
        if entity_id:
            return self._entities.get(entity_id)
        return None

    def entities_near(self, lat: float, lon: float, radius_m: float) -> list[TrackedEntity]:
        results = []
        for entity in self.active_entities:
            dist = self._haversine_m(lat, lon, entity.latitude, entity.longitude)
            if dist <= radius_m:
                results.append(entity)
        return results

    def entities_by_domain(self, domain: str) -> list[TrackedEntity]:
        return [e for e in self.active_entities if e.domain == domain]

    def threats(self, min_level: int = 4) -> list[TrackedEntity]:
        return [e for e in self.active_entities if e.threat_level >= min_level]

    def multi_source_entities(self) -> list[TrackedEntity]:
        return [e for e in self.active_entities if e.is_multi_source]

    def purge_stale(self) -> int:
        stale_ids = [eid for eid, e in self._entities.items() if e.is_stale]
        for eid in stale_ids:
            entity = self._entities.pop(eid)
            # Remove source index entries
            for src, sid in entity.source_ids.items():
                key = f"{src}:{sid}"
                self._source_index.pop(key, None)
        return len(stale_ids)

    @property
    def stats(self) -> dict:
        active = self.active_entities
        return {
            "total_entities": len(self._entities),
            "active_entities": len(active),
            "observations_processed": self._observations_processed,
            "correlations_made": self._correlations_made,
            "multi_source": len(self.multi_source_entities()),
            "by_domain": {
                "air": sum(1 for e in active if e.domain == "air"),
                "sea": sum(1 for e in active if e.domain == "sea"),
                "land": sum(1 for e in active if e.domain == "land"),
                "unknown": sum(1 for e in active if e.domain == "unknown"),
            },
        }

    @staticmethod
    def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine distance in metres."""
        R = 6371000  # Earth radius in metres
        lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
        )
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
