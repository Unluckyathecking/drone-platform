"""Task translator -- converts C2 TaskPlans to protocol-specific commands.

The MAVLink translator converts generic Tasks/Waypoints into ArduPilot
MissionItems. This is the bridge between the C2 abstraction layer and
the drone-specific upload/execution layer.

Future translators could handle:
- Ground vehicle waypoints (ROS/MAVROS)
- Maritime vessel commands
- Personnel task assignments (CoT)
"""

from __future__ import annotations

from .models import BasicMission, Coordinate, MissionItem
from .planner import build_mission, validate


class TranslationError(Exception):
    """Raised when a task cannot be translated to the target protocol."""


def _extract_waypoints_from_task(
    task,
    default_altitude_m: float,
) -> list[Coordinate]:
    """Extract Coordinates from a single task based on its type.

    Duck-types on task.task_type, task.waypoints, and task.area_of_interest
    so that any object with the right attributes works (no hard import of
    c2_models required).
    """
    coords: list[Coordinate] = []
    task_type = str(task.task_type)

    if task_type in ("goto", "survey", "deliver"):
        for wp in task.waypoints:
            alt = wp.altitude_m if wp.altitude_m is not None else default_altitude_m
            coords.append(
                Coordinate(
                    latitude=wp.position.latitude,
                    longitude=wp.position.longitude,
                    altitude=alt,
                )
            )

    elif task_type == "patrol":
        if task.waypoints:
            for wp in task.waypoints:
                alt = wp.altitude_m if wp.altitude_m is not None else default_altitude_m
                coords.append(
                    Coordinate(
                        latitude=wp.position.latitude,
                        longitude=wp.position.longitude,
                        altitude=alt,
                    )
                )
        elif task.area_of_interest:
            for pos in task.area_of_interest:
                coords.append(
                    Coordinate(
                        latitude=pos.latitude,
                        longitude=pos.longitude,
                        altitude=default_altitude_m,
                    )
                )

    elif task_type == "loiter":
        if task.waypoints:
            wp = task.waypoints[0]
            alt = wp.altitude_m if wp.altitude_m is not None else default_altitude_m
            coords.append(
                Coordinate(
                    latitude=wp.position.latitude,
                    longitude=wp.position.longitude,
                    altitude=alt,
                )
            )

    return coords


class MAVLinkTranslator:
    """Translates C2 Tasks into ArduPilot MissionItems.

    This is the drone backend -- it takes generic task descriptions and
    produces MAVLink-compatible mission items for upload to ArduPilot.
    """

    def translate_plan(
        self,
        plan,
    ) -> tuple[list[MissionItem], list[str]]:
        """Translate a TaskPlan to a list of MissionItems.

        Converts the plan's tasks into a BasicMission, then uses the
        existing planner to build MissionItems.

        Args:
            plan: A TaskPlan (or duck-typed equivalent) with *tasks*,
                  *home_position*, and *default_altitude_m*.

        Returns:
            Tuple of (MissionItems ready for upload, validation warnings).

        Raises:
            TranslationError: If the plan cannot be translated.
        """
        if plan.home_position is None:
            raise TranslationError(
                "TaskPlan requires a home_position for MAVLink translation"
            )

        waypoints: list[Coordinate] = []
        for task in plan.tasks:
            waypoints.extend(
                _extract_waypoints_from_task(task, plan.default_altitude_m)
            )

        if not waypoints:
            raise TranslationError("No translatable waypoints found in TaskPlan")

        home = Coordinate(
            latitude=plan.home_position.latitude,
            longitude=plan.home_position.longitude,
            altitude=plan.home_position.altitude_m,
        )

        max_alt = (
            max(t.max_altitude_m for t in plan.tasks)
            if plan.tasks
            else 120.0
        )

        mission = BasicMission(
            home=home,
            waypoints=waypoints,
            cruise_altitude_m=plan.default_altitude_m,
            max_altitude_m=max_alt,
        )

        warnings = validate(mission)
        items = build_mission(mission)

        return items, warnings

    def translate_task(
        self,
        task,
        home_position,
        default_altitude_m: float = 50.0,
    ) -> list[MissionItem]:
        """Translate a single Task to MissionItems.

        Convenience method for single-task plans.

        Args:
            task: A Task (or duck-typed equivalent).
            home_position: A Position-like object with latitude, longitude,
                           altitude_m.
            default_altitude_m: Fallback altitude for waypoints without one.

        Returns:
            List of MissionItems ready for upload.
        """
        from types import SimpleNamespace

        plan = SimpleNamespace(
            home_position=home_position,
            default_altitude_m=default_altitude_m,
            tasks=[task],
        )
        items, _ = self.translate_plan(plan)
        return items
