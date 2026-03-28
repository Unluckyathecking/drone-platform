"""Multi-domain C2 data models -- protocol-agnostic abstractions.

These models represent entities, tracks, tasks, and plans at the C2 level.
They are translated to protocol-specific formats (MAVLink, CoT, etc.) by
backend modules.

The existing BasicMission/MissionItem models remain as the MAVLink backend.
These new models sit above them in the abstraction hierarchy.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


# -- Enums -------------------------------------------------------------------


class Domain(StrEnum):
    """Operational domain of an entity."""

    AIR = "air"
    SEA = "sea"
    LAND = "land"
    SUBSURFACE = "subsurface"
    SPACE = "space"
    CYBER = "cyber"


class Affiliation(StrEnum):
    """Entity affiliation in the operational picture."""

    FRIENDLY = "friendly"
    HOSTILE = "hostile"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"
    SUSPECT = "suspect"


class EntityType(StrEnum):
    """Type of entity in the C2 picture."""

    UAV = "uav"
    FIXED_WING = "fixed_wing"
    ROTARY_WING = "rotary_wing"
    GROUND_VEHICLE = "ground_vehicle"
    SURFACE_VESSEL = "surface_vessel"
    SUBMARINE = "submarine"
    PERSON = "person"
    SENSOR = "sensor"
    BASE_STATION = "base_station"


class TaskType(StrEnum):
    """Type of task that can be assigned to an entity."""

    GOTO = "goto"
    PATROL = "patrol"
    SURVEY = "survey"
    TRACK = "track"
    DELIVER = "deliver"
    RETURN = "return"
    LOITER = "loiter"
    RELAY = "relay"


class TaskStatus(StrEnum):
    """Current status of a task."""

    PLANNED = "planned"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TrackSource(StrEnum):
    """Source of a track observation."""

    AIS = "ais"
    ADSB = "adsb"
    RADAR = "radar"
    VISUAL = "visual"
    IR = "ir"
    SIGINT = "sigint"
    MANUAL = "manual"
    COT = "cot"


# -- Core Models -------------------------------------------------------------


class Position(BaseModel):
    """A geographic position with optional altitude and timestamp."""

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    altitude_m: float = 0.0
    heading: float = 0.0
    speed_mps: float = 0.0
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class Entity(BaseModel):
    """Any identifiable thing in the operational picture.

    An Entity is anything with an identity -- your drone, a friendly vehicle,
    a person, a base station.  Entities you control are assets.  Entities you
    observe are tracks.
    """

    uid: str = Field(default_factory=lambda: str(uuid4())[:8])
    name: str = ""
    entity_type: EntityType = EntityType.UAV
    domain: Domain = Domain.AIR
    affiliation: Affiliation = Affiliation.FRIENDLY
    position: Position | None = None
    callsign: str = ""

    # Platform-specific identifiers
    mavlink_sysid: int | None = None
    mmsi: int | None = None
    icao_hex: str | None = None


class Track(BaseModel):
    """An observed entity -- something detected by a sensor.

    Tracks come from external sources (AIS, radar, visual, etc.) and represent
    things in the operational picture that you don't control but need to know
    about.
    """

    track_id: str = Field(
        default_factory=lambda: f"TRK-{str(uuid4())[:8]}",
    )
    source: TrackSource = TrackSource.MANUAL
    entity: Entity = Field(default_factory=Entity)
    first_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    last_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    # Source-specific identifiers
    mmsi: int | None = None
    ais_ship_type: int | None = None


class Waypoint(BaseModel):
    """A generic waypoint -- protocol-agnostic.

    Unlike MissionItem (which is MAVLink-specific), a Waypoint just says
    "go here" with optional constraints.  The backend translates it to
    protocol-specific commands.
    """

    position: Position
    name: str = ""
    altitude_m: float | None = None
    speed_mps: float | None = None
    loiter_seconds: float = 0.0
    radius_m: float = 0.0


class Task(BaseModel):
    """An assignable action in the C2 system.

    A Task is what you want done -- "patrol this area", "go to this point",
    "track this vessel".  It's assigned to an Entity and translated to
    protocol-specific commands by a backend.
    """

    task_id: str = Field(
        default_factory=lambda: f"TSK-{str(uuid4())[:8]}",
    )
    task_type: TaskType = TaskType.GOTO
    status: TaskStatus = TaskStatus.PLANNED
    assigned_to: str | None = None
    priority: int = Field(default=5, ge=1, le=10)

    # Task geometry
    waypoints: list[Waypoint] = Field(default_factory=list)
    area_of_interest: list[Position] | None = None
    target_track_id: str | None = None

    # Constraints
    min_altitude_m: float = 0.0
    max_altitude_m: float = 120.0
    max_speed_mps: float = 30.0

    # Timing
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    start_after: datetime | None = None
    complete_by: datetime | None = None

    @field_validator("waypoints")
    @classmethod
    def check_waypoints_for_goto(
        cls,
        v: list[Waypoint],
        info,
    ) -> list[Waypoint]:
        """GOTO tasks need at least one waypoint."""
        if info.data.get("task_type") == TaskType.GOTO and len(v) == 0:
            raise ValueError("GOTO task requires at least one waypoint")
        return v


class TaskPlan(BaseModel):
    """A collection of tasks forming an operational plan.

    This is the C2-level equivalent of BasicMission.  A TaskPlan contains
    one or more Tasks, each potentially assigned to different entities.
    The plan can be translated to:
      - MissionItem list (for drone upload via MAVLink)
      - CoT events (for ATAK display)
      - Other protocol-specific formats
    """

    plan_id: str = Field(
        default_factory=lambda: f"PLAN-{str(uuid4())[:8]}",
    )
    name: str = ""
    description: str = ""
    tasks: list[Task] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)

    # Plan-level defaults
    home_position: Position | None = None
    default_altitude_m: float = 50.0
    default_speed_mps: float = 15.0

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
