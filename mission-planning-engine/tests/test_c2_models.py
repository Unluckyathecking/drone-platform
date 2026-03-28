"""Tests for the generic C2 data models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

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


# -- Enum tests --------------------------------------------------------------


class TestDomainEnum:
    def test_all_values(self):
        assert set(Domain) == {
            Domain.AIR,
            Domain.SEA,
            Domain.LAND,
            Domain.SUBSURFACE,
            Domain.SPACE,
            Domain.CYBER,
        }

    def test_string_values(self):
        assert Domain.AIR == "air"
        assert Domain.SEA == "sea"
        assert Domain.LAND == "land"


class TestAffiliationEnum:
    def test_all_values(self):
        assert set(Affiliation) == {
            Affiliation.FRIENDLY,
            Affiliation.HOSTILE,
            Affiliation.NEUTRAL,
            Affiliation.UNKNOWN,
            Affiliation.SUSPECT,
        }

    def test_string_values(self):
        assert Affiliation.FRIENDLY == "friendly"
        assert Affiliation.HOSTILE == "hostile"


class TestEntityTypeEnum:
    def test_all_values(self):
        expected = {
            EntityType.UAV,
            EntityType.FIXED_WING,
            EntityType.ROTARY_WING,
            EntityType.GROUND_VEHICLE,
            EntityType.SURFACE_VESSEL,
            EntityType.SUBMARINE,
            EntityType.PERSON,
            EntityType.SENSOR,
            EntityType.BASE_STATION,
        }
        assert set(EntityType) == expected


class TestTaskTypeEnum:
    def test_all_values(self):
        expected = {
            TaskType.GOTO,
            TaskType.PATROL,
            TaskType.SURVEY,
            TaskType.TRACK,
            TaskType.DELIVER,
            TaskType.RETURN,
            TaskType.LOITER,
            TaskType.RELAY,
        }
        assert set(TaskType) == expected


class TestTaskStatusEnum:
    def test_lifecycle(self):
        """Status values support a PLANNED -> ASSIGNED -> IN_PROGRESS -> COMPLETED flow."""
        lifecycle = [
            TaskStatus.PLANNED,
            TaskStatus.ASSIGNED,
            TaskStatus.IN_PROGRESS,
            TaskStatus.COMPLETED,
        ]
        assert all(isinstance(s, TaskStatus) for s in lifecycle)
        assert lifecycle[0] == "planned"
        assert lifecycle[-1] == "completed"

    def test_failure_and_cancellation(self):
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.CANCELLED == "cancelled"


# -- Position tests -----------------------------------------------------------


class TestPosition:
    def test_valid_position(self):
        pos = Position(latitude=51.3, longitude=-0.26)
        assert pos.latitude == 51.3
        assert pos.longitude == -0.26
        assert pos.altitude_m == 0.0
        assert pos.heading == 0.0
        assert pos.speed_mps == 0.0
        assert pos.timestamp is not None

    def test_latitude_out_of_range(self):
        with pytest.raises(ValidationError):
            Position(latitude=91.0, longitude=0.0)

    def test_latitude_negative_out_of_range(self):
        with pytest.raises(ValidationError):
            Position(latitude=-91.0, longitude=0.0)

    def test_longitude_out_of_range(self):
        with pytest.raises(ValidationError):
            Position(latitude=0.0, longitude=181.0)

    def test_longitude_negative_out_of_range(self):
        with pytest.raises(ValidationError):
            Position(latitude=0.0, longitude=-181.0)

    def test_boundary_values(self):
        pos = Position(latitude=90.0, longitude=180.0)
        assert pos.latitude == 90.0
        assert pos.longitude == 180.0

        pos2 = Position(latitude=-90.0, longitude=-180.0)
        assert pos2.latitude == -90.0
        assert pos2.longitude == -180.0


# -- Entity tests -------------------------------------------------------------


class TestEntity:
    def test_defaults(self):
        entity = Entity()
        assert len(entity.uid) == 8
        assert entity.name == ""
        assert entity.entity_type == EntityType.UAV
        assert entity.domain == Domain.AIR
        assert entity.affiliation == Affiliation.FRIENDLY
        assert entity.position is None
        assert entity.callsign == ""
        assert entity.mavlink_sysid is None
        assert entity.mmsi is None
        assert entity.icao_hex is None

    def test_all_fields_populated(self):
        pos = Position(latitude=51.3, longitude=-0.26, altitude_m=100.0)
        entity = Entity(
            uid="drone-01",
            name="Skywalker X8",
            entity_type=EntityType.FIXED_WING,
            domain=Domain.AIR,
            affiliation=Affiliation.FRIENDLY,
            position=pos,
            callsign="ALPHA1",
            mavlink_sysid=1,
            mmsi=None,
            icao_hex=None,
        )
        assert entity.uid == "drone-01"
        assert entity.name == "Skywalker X8"
        assert entity.entity_type == EntityType.FIXED_WING
        assert entity.callsign == "ALPHA1"
        assert entity.mavlink_sysid == 1
        assert entity.position is not None
        assert entity.position.altitude_m == 100.0

    def test_mavlink_sysid(self):
        entity = Entity(mavlink_sysid=1)
        assert entity.mavlink_sysid == 1

    def test_uid_auto_generation_unique(self):
        e1 = Entity()
        e2 = Entity()
        assert e1.uid != e2.uid


# -- Track tests --------------------------------------------------------------


class TestTrack:
    def test_defaults(self):
        track = Track()
        assert track.track_id.startswith("TRK-")
        assert track.source == TrackSource.MANUAL
        assert track.confidence == 1.0
        assert track.entity is not None
        assert track.mmsi is None
        assert track.ais_ship_type is None

    def test_with_source_and_confidence(self):
        track = Track(source=TrackSource.RADAR, confidence=0.7)
        assert track.source == TrackSource.RADAR
        assert track.confidence == 0.7

    def test_ais_source_with_mmsi(self):
        track = Track(
            source=TrackSource.AIS,
            mmsi=211234567,
            ais_ship_type=70,
            entity=Entity(
                name="MV Example",
                entity_type=EntityType.SURFACE_VESSEL,
                domain=Domain.SEA,
                affiliation=Affiliation.NEUTRAL,
                mmsi=211234567,
            ),
        )
        assert track.source == TrackSource.AIS
        assert track.mmsi == 211234567
        assert track.ais_ship_type == 70
        assert track.entity.entity_type == EntityType.SURFACE_VESSEL

    def test_confidence_bounds(self):
        with pytest.raises(ValidationError):
            Track(confidence=1.5)

        with pytest.raises(ValidationError):
            Track(confidence=-0.1)


# -- Waypoint tests -----------------------------------------------------------


class TestWaypoint:
    def test_creation(self):
        pos = Position(latitude=51.3, longitude=-0.26)
        wp = Waypoint(position=pos, name="WP1")
        assert wp.position.latitude == 51.3
        assert wp.name == "WP1"
        assert wp.altitude_m is None
        assert wp.speed_mps is None
        assert wp.loiter_seconds == 0.0
        assert wp.radius_m == 0.0

    def test_with_overrides(self):
        pos = Position(latitude=51.3, longitude=-0.26)
        wp = Waypoint(
            position=pos,
            altitude_m=80.0,
            speed_mps=20.0,
            loiter_seconds=30.0,
            radius_m=50.0,
        )
        assert wp.altitude_m == 80.0
        assert wp.speed_mps == 20.0
        assert wp.loiter_seconds == 30.0
        assert wp.radius_m == 50.0


# -- Task tests ---------------------------------------------------------------


class TestTask:
    def _make_waypoint(self) -> Waypoint:
        return Waypoint(position=Position(latitude=51.3, longitude=-0.26))

    def test_goto_with_waypoint(self):
        task = Task(
            task_type=TaskType.GOTO,
            waypoints=[self._make_waypoint()],
        )
        assert task.task_type == TaskType.GOTO
        assert task.status == TaskStatus.PLANNED
        assert len(task.waypoints) == 1
        assert task.task_id.startswith("TSK-")

    def test_goto_requires_waypoints(self):
        with pytest.raises(ValidationError, match="GOTO task requires at least one waypoint"):
            Task(task_type=TaskType.GOTO, waypoints=[])

    def test_patrol_no_waypoints_required(self):
        task = Task(task_type=TaskType.PATROL)
        assert task.task_type == TaskType.PATROL
        assert len(task.waypoints) == 0

    def test_priority_bounds(self):
        task_low = Task(
            task_type=TaskType.PATROL,
            priority=1,
        )
        assert task_low.priority == 1

        task_high = Task(
            task_type=TaskType.PATROL,
            priority=10,
        )
        assert task_high.priority == 10

    def test_priority_below_minimum(self):
        with pytest.raises(ValidationError):
            Task(task_type=TaskType.PATROL, priority=0)

    def test_priority_above_maximum(self):
        with pytest.raises(ValidationError):
            Task(task_type=TaskType.PATROL, priority=11)

    def test_defaults(self):
        task = Task(
            task_type=TaskType.PATROL,
        )
        assert task.priority == 5
        assert task.assigned_to is None
        assert task.min_altitude_m == 0.0
        assert task.max_altitude_m == 120.0
        assert task.max_speed_mps == 30.0
        assert task.start_after is None
        assert task.complete_by is None


# -- TaskPlan tests -----------------------------------------------------------


class TestTaskPlan:
    def _make_task(self, task_type: TaskType = TaskType.PATROL) -> Task:
        if task_type == TaskType.GOTO:
            wp = Waypoint(position=Position(latitude=51.3, longitude=-0.26))
            return Task(task_type=task_type, waypoints=[wp])
        return Task(task_type=task_type)

    def test_creation(self):
        plan = TaskPlan(name="Test Plan")
        assert plan.plan_id.startswith("PLAN-")
        assert plan.name == "Test Plan"
        assert plan.tasks == []
        assert plan.entities == []
        assert plan.default_altitude_m == 50.0
        assert plan.default_speed_mps == 15.0

    def test_with_multiple_tasks(self):
        plan = TaskPlan(
            name="Multi-task plan",
            tasks=[
                self._make_task(TaskType.GOTO),
                self._make_task(TaskType.PATROL),
                self._make_task(TaskType.LOITER),
            ],
        )
        assert len(plan.tasks) == 3
        assert plan.tasks[0].task_type == TaskType.GOTO
        assert plan.tasks[1].task_type == TaskType.PATROL
        assert plan.tasks[2].task_type == TaskType.LOITER

    def test_with_entities(self):
        drone = Entity(
            name="Skywalker X8",
            entity_type=EntityType.FIXED_WING,
            mavlink_sysid=1,
        )
        base = Entity(
            name="GCS",
            entity_type=EntityType.BASE_STATION,
            domain=Domain.LAND,
        )
        plan = TaskPlan(
            name="Patrol mission",
            entities=[drone, base],
        )
        assert len(plan.entities) == 2
        assert plan.entities[0].entity_type == EntityType.FIXED_WING
        assert plan.entities[1].entity_type == EntityType.BASE_STATION

    def test_with_home_position(self):
        home = Position(latitude=51.3, longitude=-0.26)
        plan = TaskPlan(home_position=home)
        assert plan.home_position is not None
        assert plan.home_position.latitude == 51.3
