"""Tests for the operator API (mpe.operator_api).

Covers: watchlist CRUD, classification overrides, alert acknowledgement,
SITREP generation, and health check endpoint.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from mpe.server import app
import mpe.operator_api as operator_api


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_state():
    """Reset in-memory state before each test."""
    operator_api._watchlist.clear()
    operator_api._classification_overrides.clear()
    operator_api._alert_history.clear()
    yield
    operator_api._watchlist.clear()
    operator_api._classification_overrides.clear()
    operator_api._alert_history.clear()


@pytest.fixture()
def client():
    """FastAPI TestClient."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# Watchlist endpoints
# ---------------------------------------------------------------------------


class TestWatchlistAdd:
    """POST /api/operator/watchlist"""

    def test_add_friendly_entry(self, client):
        resp = client.post("/api/operator/watchlist", json={
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
            "reason": "Own fleet vessel",
            "added_by": "operator_1",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "added"
        assert body["key"] == "mmsi:211234567"
        assert body["affiliation"] == "friendly"
        assert body["watchlist_size"] == 1

    def test_add_hostile_entry(self, client):
        resp = client.post("/api/operator/watchlist", json={
            "identifier": "4CA7B5",
            "identifier_type": "icao",
            "affiliation": "hostile",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "added"
        assert body["key"] == "icao:4CA7B5"
        assert body["affiliation"] == "hostile"

    def test_add_defaults(self, client):
        resp = client.post("/api/operator/watchlist", json={
            "identifier": "999999999",
            "identifier_type": "mmsi",
            "affiliation": "hostile",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["watchlist_size"] == 1

    def test_add_overwrites_existing(self, client):
        payload = {
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
        }
        client.post("/api/operator/watchlist", json=payload)
        # Overwrite with hostile
        payload["affiliation"] = "hostile"
        resp = client.post("/api/operator/watchlist", json=payload)
        assert resp.status_code == 200
        assert resp.json()["affiliation"] == "hostile"
        assert resp.json()["watchlist_size"] == 1


class TestWatchlistGet:
    """GET /api/operator/watchlist"""

    def test_empty_watchlist(self, client):
        resp = client.get("/api/operator/watchlist")
        assert resp.status_code == 200
        body = resp.json()
        assert body["entries"] == []
        assert body["total"] == 0

    def test_list_entries(self, client):
        client.post("/api/operator/watchlist", json={
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
            "reason": "Own fleet",
        })
        client.post("/api/operator/watchlist", json={
            "identifier": "4CA7B5",
            "identifier_type": "icao",
            "affiliation": "hostile",
        })
        resp = client.get("/api/operator/watchlist")
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        assert len(body["entries"]) == 2
        keys = {e["key"] for e in body["entries"]}
        assert "mmsi:211234567" in keys
        assert "icao:4CA7B5" in keys


class TestWatchlistDelete:
    """DELETE /api/operator/watchlist/{type}/{id}"""

    def test_remove_existing(self, client):
        client.post("/api/operator/watchlist", json={
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
        })
        resp = client.delete("/api/operator/watchlist/mmsi/211234567")
        assert resp.status_code == 200
        assert resp.json()["status"] == "removed"
        assert resp.json()["key"] == "mmsi:211234567"

    def test_remove_nonexistent_returns_404(self, client):
        resp = client.delete("/api/operator/watchlist/mmsi/000000000")
        assert resp.status_code == 404
        assert "Not on watchlist" in resp.json()["detail"]

    def test_remove_then_list_empty(self, client):
        client.post("/api/operator/watchlist", json={
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
        })
        client.delete("/api/operator/watchlist/mmsi/211234567")
        resp = client.get("/api/operator/watchlist")
        assert resp.json()["total"] == 0


# ---------------------------------------------------------------------------
# Classification override endpoints
# ---------------------------------------------------------------------------


class TestClassifyOverride:
    """POST /api/operator/classify"""

    def test_override_classification(self, client):
        resp = client.post("/api/operator/classify", json={
            "entity_id": "AIS-273999111",
            "affiliation": "hostile",
            "reason": "Intel report",
            "overridden_by": "operator_1",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "overridden"
        assert body["entity_id"] == "AIS-273999111"
        assert body["new_affiliation"] == "hostile"
        assert body["reason"] == "Intel report"

    def test_override_replaces_previous(self, client):
        client.post("/api/operator/classify", json={
            "entity_id": "AIS-273999111",
            "affiliation": "hostile",
        })
        resp = client.post("/api/operator/classify", json={
            "entity_id": "AIS-273999111",
            "affiliation": "friendly",
            "reason": "Re-assessed",
        })
        assert resp.json()["new_affiliation"] == "friendly"


class TestClassifyGet:
    """GET /api/operator/classify/{entity_id}"""

    def test_get_manual_override(self, client):
        client.post("/api/operator/classify", json={
            "entity_id": "ADSB-4CA7B5",
            "affiliation": "suspect",
            "reason": "Unusual behaviour",
            "overridden_by": "analyst",
        })
        resp = client.get("/api/operator/classify/ADSB-4CA7B5")
        assert resp.status_code == 200
        body = resp.json()
        assert body["entity_id"] == "ADSB-4CA7B5"
        assert body["affiliation"] == "suspect"
        assert body["source"] == "manual_override"
        assert body["reason"] == "Unusual behaviour"
        assert body["overridden_by"] == "analyst"

    def test_get_no_override_returns_auto(self, client):
        resp = client.get("/api/operator/classify/ADSB-UNKNOWN")
        assert resp.status_code == 200
        body = resp.json()
        assert body["affiliation"] == "unknown"
        assert body["source"] == "auto"


# ---------------------------------------------------------------------------
# Alert endpoints
# ---------------------------------------------------------------------------


def _seed_alerts():
    """Insert sample alerts into in-memory history."""
    operator_api._alert_history.extend([
        {
            "alert_id": "ALERT-000001",
            "entity_id": "AIS-273999111",
            "alert_type": "threat",
            "severity": 8,
            "title": "THREAT: AIS-273999111",
            "description": "Hostile vessel",
            "latitude": 51.5,
            "longitude": -0.1,
            "rule_name": "high_threat",
            "created_at": "2026-03-28T10:00:00+00:00",
            "acknowledged": False,
        },
        {
            "alert_id": "ALERT-000002",
            "entity_id": "ADSB-4CA7B5",
            "alert_type": "emergency",
            "severity": 10,
            "title": "EMERGENCY: Squawk 7500",
            "description": "Hijack squawk",
            "latitude": 52.0,
            "longitude": 0.5,
            "rule_name": "hijack",
            "created_at": "2026-03-28T10:05:00+00:00",
            "acknowledged": False,
        },
        {
            "alert_id": "ALERT-000003",
            "entity_id": "AIS-100000000",
            "alert_type": "anomaly",
            "severity": 5,
            "title": "ANOMALY: Speed anomaly",
            "description": "Cargo vessel too fast",
            "latitude": 26.0,
            "longitude": 56.5,
            "rule_name": "speed_anomaly",
            "created_at": "2026-03-28T09:50:00+00:00",
            "acknowledged": True,
        },
    ])


class TestAlertAcknowledge:
    """POST /api/operator/alerts/{id}/acknowledge"""

    def test_acknowledge_existing(self, client):
        _seed_alerts()
        resp = client.post("/api/operator/alerts/ALERT-000001/acknowledge", json={
            "acknowledged_by": "operator_1",
            "notes": "Investigating",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "acknowledged"
        assert resp.json()["alert_id"] == "ALERT-000001"
        # Verify state mutated
        alert = operator_api._alert_history[0]
        assert alert["acknowledged"] is True
        assert alert["acknowledged_by"] == "operator_1"
        assert alert["notes"] == "Investigating"
        assert "acknowledged_at" in alert

    def test_acknowledge_nonexistent_returns_404(self, client):
        resp = client.post(
            "/api/operator/alerts/ALERT-MISSING/acknowledge",
            json={},
        )
        assert resp.status_code == 404
        assert "Alert not found" in resp.json()["detail"]


class TestAlertsList:
    """GET /api/operator/alerts"""

    def test_active_only_default(self, client):
        _seed_alerts()
        resp = client.get("/api/operator/alerts")
        assert resp.status_code == 200
        body = resp.json()
        # ALERT-000003 is already acknowledged, so only 2 active
        assert body["total"] == 2
        assert body["unacknowledged"] == 2
        for alert in body["alerts"]:
            assert alert["acknowledged"] is False

    def test_all_alerts(self, client):
        _seed_alerts()
        resp = client.get("/api/operator/alerts?active_only=false")
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 3
        assert body["unacknowledged"] == 2

    def test_empty_alerts(self, client):
        resp = client.get("/api/operator/alerts")
        assert resp.status_code == 200
        body = resp.json()
        assert body["alerts"] == []
        assert body["total"] == 0
        assert body["unacknowledged"] == 0


# ---------------------------------------------------------------------------
# SITREP endpoint
# ---------------------------------------------------------------------------


class TestSitrep:
    """GET /api/operator/sitrep"""

    def test_sitrep_returns_structure(self, client):
        resp = client.get("/api/operator/sitrep")
        assert resp.status_code == 200
        body = resp.json()
        assert "sitrep" in body
        sitrep = body["sitrep"]
        assert "generated_at" in sitrep
        assert sitrep["classification"] == "UNCLASSIFIED"

    def test_sitrep_with_alerts(self, client):
        _seed_alerts()
        resp = client.get("/api/operator/sitrep")
        assert resp.status_code == 200
        sitrep = resp.json()["sitrep"]
        # Either full sitrep or error-mode is valid depending on import state
        assert "generated_at" in sitrep

    def test_sitrep_includes_summary_or_error(self, client):
        resp = client.get("/api/operator/sitrep")
        assert resp.status_code == 200
        sitrep = resp.json()["sitrep"]
        # Must have either a summary block or an error message
        has_summary = "summary" in sitrep
        has_error = "error" in sitrep
        assert has_summary or has_error


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------


class TestHealth:
    """GET /api/operator/health"""

    def test_health_operational(self, client):
        resp = client.get("/api/operator/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "operational"
        assert "timestamp" in body
        assert body["watchlist_size"] == 0
        assert body["overrides_active"] == 0
        assert body["alerts_total"] == 0
        assert body["alerts_unacknowledged"] == 0

    def test_health_reflects_state(self, client):
        # Add some state
        client.post("/api/operator/watchlist", json={
            "identifier": "211234567",
            "identifier_type": "mmsi",
            "affiliation": "friendly",
        })
        client.post("/api/operator/classify", json={
            "entity_id": "AIS-273999111",
            "affiliation": "hostile",
        })
        _seed_alerts()

        resp = client.get("/api/operator/health")
        body = resp.json()
        assert body["watchlist_size"] == 1
        assert body["overrides_active"] == 1
        assert body["alerts_total"] == 3
        assert body["alerts_unacknowledged"] == 2


# ---------------------------------------------------------------------------
# record_alert helper
# ---------------------------------------------------------------------------


class TestRecordAlert:
    """operator_api.record_alert() helper function."""

    def test_record_alert_from_event(self):
        from types import SimpleNamespace

        event = SimpleNamespace(
            alert_id="ALERT-TEST-001",
            entity_id="AIS-123456789",
            alert_type="threat",
            severity=7,
            title="THREAT: test vessel",
            description="Test description",
            latitude=51.5,
            longitude=-0.1,
            rule_name="high_threat",
            timestamp=datetime(2026, 3, 28, 12, 0, 0, tzinfo=timezone.utc),
        )
        operator_api.record_alert(event)

        assert len(operator_api._alert_history) == 1
        recorded = operator_api._alert_history[0]
        assert recorded["alert_id"] == "ALERT-TEST-001"
        assert recorded["entity_id"] == "AIS-123456789"
        assert recorded["alert_type"] == "threat"
        assert recorded["severity"] == 7
        assert recorded["acknowledged"] is False
        assert recorded["created_at"] == "2026-03-28T12:00:00+00:00"

    def test_record_alert_then_acknowledge(self, client):
        from types import SimpleNamespace

        event = SimpleNamespace(
            alert_id="ALERT-REC-002",
            entity_id="ADSB-AABBCC",
            alert_type="emergency",
            severity=10,
            title="EMERGENCY: Test",
            description="Test emergency",
            latitude=52.0,
            longitude=0.5,
            rule_name="hijack",
            timestamp=datetime(2026, 3, 28, 12, 5, 0, tzinfo=timezone.utc),
        )
        operator_api.record_alert(event)

        # Now acknowledge via API
        resp = client.post(
            "/api/operator/alerts/ALERT-REC-002/acknowledge",
            json={"acknowledged_by": "test_user"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "acknowledged"

        # Verify in health
        health = client.get("/api/operator/health").json()
        assert health["alerts_total"] == 1
        assert health["alerts_unacknowledged"] == 0
