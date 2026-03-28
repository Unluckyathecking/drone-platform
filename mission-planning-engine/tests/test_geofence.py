"""Tests for the geofencing system."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mpe.geofence import (
    DEMO_ZONES,
    GeofenceManager,
    GeofenceViolation,
    GeofenceZone,
    point_in_polygon,
)


# ---------------------------------------------------------------------------
# point_in_polygon tests
# ---------------------------------------------------------------------------

SQUARE = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]


class TestPointInPolygon:
    def test_point_in_polygon_inside(self) -> None:
        assert point_in_polygon(0.5, 0.5, SQUARE) is True

    def test_point_in_polygon_outside(self) -> None:
        assert point_in_polygon(2.0, 2.0, SQUARE) is False

    def test_point_in_polygon_on_edge(self) -> None:
        # Points on edge should be treated as inside.
        assert point_in_polygon(0.0, 0.5, SQUARE) is True
        assert point_in_polygon(0.5, 0.0, SQUARE) is True

    def test_point_in_polygon_complex_shape(self) -> None:
        # L-shape polygon:
        #   (0,0)-(0,3)-(1,3)-(1,1)-(2,1)-(2,0)
        l_shape = [
            (0.0, 0.0), (0.0, 3.0), (1.0, 3.0),
            (1.0, 1.0), (2.0, 1.0), (2.0, 0.0),
        ]
        # Inside the bottom-right arm
        assert point_in_polygon(1.5, 0.5, l_shape) is True
        # Inside the upper-left arm
        assert point_in_polygon(0.5, 2.0, l_shape) is True
        # Outside (in the concave notch)
        assert point_in_polygon(1.5, 2.0, l_shape) is False


# ---------------------------------------------------------------------------
# GeofenceManager zone management tests
# ---------------------------------------------------------------------------

class TestZoneManagement:
    def test_add_zone(self) -> None:
        mgr = GeofenceManager()
        zone = GeofenceZone(name="Z1", zone_type="keep_out", polygon=SQUARE)
        mgr.add_zone(zone)
        assert len(mgr.zones) == 1
        assert mgr.zones[0].name == "Z1"

    def test_remove_zone(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(name="Z1", zone_type="keep_out", polygon=SQUARE))
        mgr.add_zone(GeofenceZone(name="Z2", zone_type="alert", polygon=SQUARE))
        mgr.remove_zone("Z1")
        assert len(mgr.zones) == 1
        assert mgr.zones[0].name == "Z2"

    def test_remove_zone_nonexistent(self) -> None:
        mgr = GeofenceManager()
        mgr.remove_zone("NOPE")  # Should not raise


# ---------------------------------------------------------------------------
# Violation detection tests
# ---------------------------------------------------------------------------

class TestViolationDetection:
    def test_check_keep_out_violation(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="RESTRICTED",
            zone_type="keep_out",
            polygon=SQUARE,
        ))
        violations = mgr.check("drone-1", 0.5, 0.5)
        assert len(violations) == 1
        assert violations[0].zone_type == "keep_out"
        assert violations[0].zone_name == "RESTRICTED"

    def test_check_keep_in_violation(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="SAFE_AREA",
            zone_type="keep_in",
            polygon=SQUARE,
        ))
        # Point OUTSIDE the keep-in zone triggers a violation.
        violations = mgr.check("drone-1", 5.0, 5.0)
        assert len(violations) == 1
        assert violations[0].zone_type == "keep_in"
        assert "left keep-in" in violations[0].message

    def test_check_alert_zone(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="ALERT_AREA",
            zone_type="alert",
            polygon=SQUARE,
        ))
        violations = mgr.check("vessel-1", 0.5, 0.5)
        assert len(violations) == 1
        assert violations[0].zone_type == "alert"

    def test_check_no_violation(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="RESTRICTED",
            zone_type="keep_out",
            polygon=SQUARE,
        ))
        # Point outside a keep-out zone -- no violation.
        violations = mgr.check("drone-1", 5.0, 5.0)
        assert len(violations) == 0

    def test_domain_filter(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="SEA_ZONE",
            zone_type="alert",
            polygon=SQUARE,
            domains=["sea"],
        ))
        # Air entity inside the zone -- should NOT trigger (wrong domain).
        violations = mgr.check("aircraft-1", 0.5, 0.5, domain="air")
        assert len(violations) == 0
        # Sea entity inside the zone -- should trigger.
        violations = mgr.check("vessel-1", 0.5, 0.5, domain="sea")
        assert len(violations) == 1

    def test_inactive_zone_ignored(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="DISABLED",
            zone_type="keep_out",
            polygon=SQUARE,
            active=False,
        ))
        violations = mgr.check("drone-1", 0.5, 0.5)
        assert len(violations) == 0

    def test_check_all_with_entities(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="RESTRICTED",
            zone_type="keep_out",
            polygon=SQUARE,
        ))
        entities = [
            {"entity_id": "e1", "latitude": 0.5, "longitude": 0.5},
            {"entity_id": "e2", "latitude": 5.0, "longitude": 5.0},
            {"entity_id": "e3", "latitude": 0.2, "longitude": 0.8},
        ]
        violations = mgr.check_all(entities)
        violating_ids = {v.entity_id for v in violations}
        assert "e1" in violating_ids
        assert "e3" in violating_ids
        assert "e2" not in violating_ids

    def test_violation_has_correct_fields(self) -> None:
        mgr = GeofenceManager()
        mgr.add_zone(GeofenceZone(
            name="ZONE_A",
            zone_type="keep_out",
            polygon=SQUARE,
            priority=8,
        ))
        violations = mgr.check("drone-X", 0.5, 0.5)
        assert len(violations) == 1
        v = violations[0]
        assert v.zone_name == "ZONE_A"
        assert v.zone_type == "keep_out"
        assert v.entity_id == "drone-X"
        assert v.latitude == 0.5
        assert v.longitude == 0.5
        assert isinstance(v.message, str)
        assert isinstance(v.timestamp, datetime)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

class TestLoadFromDict:
    def test_load_from_dict(self) -> None:
        mgr = GeofenceManager()
        config = [
            {
                "name": "TEST_ZONE",
                "zone_type": "keep_out",
                "polygon": [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]],
                "priority": 6,
                "domains": ["air"],
                "active": True,
            },
            {
                "name": "ZONE_B",
                "zone_type": "alert",
                "polygon": [[10.0, 20.0], [10.0, 21.0], [11.0, 21.0], [11.0, 20.0]],
            },
        ]
        mgr.load_from_dict(config)
        assert len(mgr.zones) == 2
        names = {z.name for z in mgr.zones}
        assert "TEST_ZONE" in names
        assert "ZONE_B" in names


# ---------------------------------------------------------------------------
# Demo zones sanity check
# ---------------------------------------------------------------------------

class TestDemoZones:
    def test_demo_zones_valid(self) -> None:
        """All demo zones have valid structure."""
        assert len(DEMO_ZONES) >= 4
        for zone in DEMO_ZONES:
            assert isinstance(zone.name, str) and zone.name
            assert zone.zone_type in ("keep_in", "keep_out", "alert")
            assert len(zone.polygon) >= 3
            assert 1 <= zone.priority <= 10
            for lat, lon in zone.polygon:
                assert -90 <= lat <= 90
                assert -180 <= lon <= 180
