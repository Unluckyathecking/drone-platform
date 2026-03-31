"""MPE mission sub-package.

Re-exports the mission planning layer (MAVLink, waypoints, tasks).

Modules grouped here:
- models: MAVLink-specific MissionItem, BasicMission, Coordinate
- planner: validate() + build_mission()
- upload: MAVLink MISSION_ITEM_INT upload
- c2_models: generic C2 Entity, Track, Task, TaskPlan, Waypoint
- task_translator: TaskPlan → MAVLink MissionItems
- cli: argparse entry point helpers
"""

from mpe.c2_models import (
    Affiliation,
    Domain,
    Entity,
    EntityType,
    Position,
    Task,
    TaskPlan,
    TaskStatus,
    TaskType,
    Track,
    TrackSource,
    Waypoint,
)
from mpe.models import BasicMission, Coordinate, MAVCmd, MAVFrame, MissionItem
from mpe.planner import build_mission, validate
from mpe.task_translator import MAVLinkTranslator

__all__ = [
    # C2 models
    "Affiliation",
    "Domain",
    "Entity",
    "EntityType",
    "Position",
    "Task",
    "TaskPlan",
    "TaskStatus",
    "TaskType",
    "Track",
    "TrackSource",
    "Waypoint",
    # MAVLink models
    "BasicMission",
    "Coordinate",
    "MAVCmd",
    "MAVFrame",
    "MissionItem",
    # Planner
    "build_mission",
    "validate",
    # Translators
    "MAVLinkTranslator",
]
