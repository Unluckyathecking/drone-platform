"""Tests for the CoT translator."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
from types import SimpleNamespace

from mpe.task_to_cot import CoTTranslator


# ---------------------------------------------------------------------------
# Helpers -- duck-typed C2 objects
# ---------------------------------------------------------------------------


def _pos(lat: float = 51.0, lon: float = -0.3, alt: float = 0.0):
    return SimpleNamespace(
        latitude=lat, longitude=lon, altitude_m=alt, heading=90.0, speed_mps=5.0
    )


def _entity(
    uid: str = "E001",
    name: str = "Alpha",
    callsign: str = "ALPHA-1",
    entity_type: str = "uav",
    domain: str = "air",
    affiliation: str = "friendly",
    position=None,
):
    return SimpleNamespace(
        uid=uid,
        name=name,
        callsign=callsign,
        entity_type=entity_type,
        domain=domain,
        affiliation=affiliation,
        position=position,
    )


def _wp(lat: float = 51.0, lon: float = -0.3, alt: float | None = 50.0, name: str = ""):
    return SimpleNamespace(
        position=_pos(lat, lon),
        name=name,
        altitude_m=alt,
    )


def _task(task_id: str = "TSK-001", task_type: str = "goto", waypoints=None):
    return SimpleNamespace(
        task_id=task_id,
        task_type=task_type,
        waypoints=waypoints or [],
    )


# ---------------------------------------------------------------------------
# Tests -- entity_to_cot
# ---------------------------------------------------------------------------


class TestEntityToCot:
    """Tests for CoTTranslator.entity_to_cot."""

    def test_produces_valid_xml(self):
        entity = _entity(position=_pos())
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        assert xml_str is not None
        root = ET.fromstring(xml_str)
        assert root.tag == "event"

    def test_friendly_air_type(self):
        entity = _entity(
            affiliation="friendly", domain="air", position=_pos()
        )
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        assert root.attrib["type"].startswith("a-f-A")

    def test_hostile_sea_type(self):
        entity = _entity(
            affiliation="hostile",
            domain="sea",
            entity_type="surface_vessel",
            position=_pos(),
        )
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        assert root.attrib["type"].startswith("a-h-S")

    def test_no_position_returns_none(self):
        entity = _entity(position=None)
        translator = CoTTranslator()
        result = translator.entity_to_cot(entity)
        assert result is None

    def test_callsign_in_contact(self):
        entity = _entity(callsign="BRAVO-2", position=_pos())
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        contact = root.find(".//contact")
        assert contact is not None
        assert contact.attrib["callsign"] == "BRAVO-2"

    def test_person_entity_ground_type(self):
        entity = _entity(
            affiliation="friendly",
            domain="land",
            entity_type="person",
            position=_pos(),
        )
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        # Person should map to a-f-G-U-C
        assert root.attrib["type"].startswith("a-f-G")

    def test_uid_matches_entity(self):
        entity = _entity(uid="DRONE-42", position=_pos())
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        assert root.attrib["uid"] == "DRONE-42"

    def test_point_element_coordinates(self):
        entity = _entity(position=_pos(lat=52.5, lon=-1.2, alt=100.0))
        translator = CoTTranslator()
        xml_str = translator.entity_to_cot(entity)

        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert point.attrib["lat"] == "52.5"
        assert point.attrib["lon"] == "-1.2"
        assert point.attrib["hae"] == "100.0"


# ---------------------------------------------------------------------------
# Tests -- task_waypoints_to_cot
# ---------------------------------------------------------------------------


class TestTaskWaypointsToCot:
    """Tests for CoTTranslator.task_waypoints_to_cot."""

    def test_correct_number_of_events(self):
        task = _task(waypoints=[_wp(), _wp(51.01, -0.29), _wp(51.02, -0.28)])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)
        assert len(events) == 3

    def test_waypoint_type_is_b_m_p_w(self):
        task = _task(waypoints=[_wp()])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        assert root.attrib["type"] == "b-m-p-w"

    def test_waypoint_how_is_human_entered(self):
        task = _task(waypoints=[_wp()])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        assert root.attrib["how"] == "h-e"

    def test_waypoint_uid_contains_task_id(self):
        task = _task(task_id="TSK-ABC", waypoints=[_wp()])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        assert "TSK-ABC" in root.attrib["uid"]

    def test_waypoint_altitude_in_point(self):
        task = _task(waypoints=[_wp(alt=75.0)])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        point = root.find("point")
        assert point is not None
        assert point.attrib["hae"] == "75.0"

    def test_waypoint_none_altitude_defaults_to_zero(self):
        task = _task(waypoints=[_wp(alt=None)])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        point = root.find("point")
        assert point is not None
        assert point.attrib["hae"] == "0.0"

    def test_empty_waypoints_returns_empty_list(self):
        task = _task(waypoints=[])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)
        assert events == []

    def test_remarks_contain_task_info(self):
        task = _task(task_id="TSK-XYZ", task_type="survey", waypoints=[_wp()])
        translator = CoTTranslator()
        events = translator.task_waypoints_to_cot(task)

        root = ET.fromstring(events[0])
        remarks = root.find(".//remarks")
        assert remarks is not None
        assert "TSK-XYZ" in remarks.text
        assert "survey" in remarks.text
