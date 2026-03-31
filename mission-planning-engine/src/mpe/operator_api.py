"""Operator API -- endpoints for C2 operator interactions.

These endpoints allow operators to:
- Manage watchlists (add/remove friendly/hostile entities)
- Override classifications manually
- Acknowledge alerts
- Generate situation reports (SITREP)
- Query entity details and track history
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from mpe.auth import CurrentUser, require_operator, require_viewer
from mpe.intelligence import IntelligenceEngine

router = APIRouter(prefix="/api/operator", tags=["operator"])

# Shorthand dependency aliases used in signatures
_Viewer   = Annotated[CurrentUser, Depends(require_viewer)]
_Operator = Annotated[CurrentUser, Depends(require_operator)]


# -- Request/Response Models --------------------------------------------------


class WatchlistEntry(BaseModel):
    identifier: str          # MMSI (int as string) or ICAO hex
    identifier_type: str     # "mmsi" or "icao"
    affiliation: str         # "friendly" or "hostile"
    reason: str = ""         # Why this entity is on the list
    added_by: str = "operator"


class ClassificationOverride(BaseModel):
    entity_id: str           # e.g. "AIS-273999111" or "ADSB-4CA7B5"
    affiliation: str         # "friendly", "hostile", "neutral", "suspect", "unknown"
    reason: str = ""
    overridden_by: str = "operator"


class AlertAcknowledge(BaseModel):
    acknowledged_by: str = "operator"
    notes: str = ""


# -- In-memory state (will be backed by DB later) ----------------------------
# These are shared with the engine via reference

_watchlist: dict[str, WatchlistEntry] = {}
_classification_overrides: dict[str, ClassificationOverride] = {}
_alert_history: list[dict] = []


# -- Endpoints ----------------------------------------------------------------


@router.post("/watchlist")
async def add_to_watchlist(entry: WatchlistEntry, _user: _Operator):
    """Add an entity to the friendly or hostile watchlist."""
    key = f"{entry.identifier_type}:{entry.identifier}"
    _watchlist[key] = entry
    return {
        "status": "added",
        "key": key,
        "affiliation": entry.affiliation,
        "watchlist_size": len(_watchlist),
    }


@router.delete("/watchlist/{identifier_type}/{identifier}")
async def remove_from_watchlist(identifier_type: str, identifier: str, _user: _Operator):
    """Remove an entity from the watchlist."""
    key = f"{identifier_type}:{identifier}"
    if key not in _watchlist:
        raise HTTPException(status_code=404, detail=f"Not on watchlist: {key}")
    del _watchlist[key]
    return {"status": "removed", "key": key}


@router.get("/watchlist")
async def get_watchlist(_user: _Viewer):
    """Get the current watchlist."""
    return {
        "entries": [
            {
                "key": k,
                "identifier": v.identifier,
                "identifier_type": v.identifier_type,
                "affiliation": v.affiliation,
                "reason": v.reason,
                "added_by": v.added_by,
            }
            for k, v in _watchlist.items()
        ],
        "total": len(_watchlist),
    }


@router.post("/classify")
async def override_classification(override: ClassificationOverride, _user: _Operator):
    """Manually override an entity's classification."""
    _classification_overrides[override.entity_id] = override
    return {
        "status": "overridden",
        "entity_id": override.entity_id,
        "new_affiliation": override.affiliation,
        "reason": override.reason,
    }


@router.get("/classify/{entity_id}")
async def get_classification(entity_id: str, _user: _Viewer):
    """Get the current classification for an entity."""
    override = _classification_overrides.get(entity_id)
    if override:
        return {
            "entity_id": entity_id,
            "affiliation": override.affiliation,
            "source": "manual_override",
            "reason": override.reason,
            "overridden_by": override.overridden_by,
        }
    return {
        "entity_id": entity_id,
        "affiliation": "unknown",
        "source": "auto",
        "reason": "No manual override -- using automatic classification",
    }


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, ack: AlertAcknowledge, _user: _Operator):
    """Acknowledge an alert."""
    for alert in _alert_history:
        if alert.get("alert_id") == alert_id:
            alert["acknowledged"] = True
            alert["acknowledged_by"] = ack.acknowledged_by
            alert["acknowledged_at"] = datetime.now(timezone.utc).isoformat()
            alert["notes"] = ack.notes
            return {"status": "acknowledged", "alert_id": alert_id}
    raise HTTPException(status_code=404, detail=f"Alert not found: {alert_id}")


@router.get("/alerts")
async def get_alerts(
    _user: _Viewer,
    active_only: bool = Query(True, description="Only show unacknowledged alerts"),
):
    """Get alerts."""
    if active_only:
        alerts = [a for a in _alert_history if not a.get("acknowledged")]
    else:
        alerts = _alert_history
    return {
        "alerts": alerts,
        "total": len(alerts),
        "unacknowledged": sum(
            1 for a in _alert_history if not a.get("acknowledged")
        ),
    }


@router.get("/sitrep")
async def generate_sitrep(_user: _Viewer):
    """Generate a situation report (SITREP) from the current picture.

    Returns a structured summary of the operational picture suitable
    for briefing or logging.
    """
    now = datetime.now(timezone.utc)

    # Import engine state (will be injected properly later)
    # For now, use the global trackers from server.py
    try:
        from mpe.server import aircraft_tracker, vessel_tracker, classifier

        air_tracks = aircraft_tracker.active_tracks
        sea_tracks = vessel_tracker.active_tracks

        # Classify and count
        air_by_affil: dict[str, int] = {
            "friendly": 0,
            "neutral": 0,
            "hostile": 0,
            "suspect": 0,
            "unknown": 0,
        }
        sea_by_affil: dict[str, int] = {
            "friendly": 0,
            "neutral": 0,
            "hostile": 0,
            "suspect": 0,
            "unknown": 0,
        }
        threats: list[dict] = []
        emergencies: list[dict] = []

        for t in air_tracks:
            cls = classifier.classify_aircraft(t)
            air_by_affil[cls.affiliation] = (
                air_by_affil.get(cls.affiliation, 0) + 1
            )
            if cls.threat_level >= 7:
                threats.append({
                    "id": f"ADSB-{t.icao_hex}",
                    "callsign": t.callsign or t.icao_hex,
                    "domain": "air",
                    "threat_level": cls.threat_level,
                    "affiliation": cls.affiliation,
                })
            if t.squawk in ("7500", "7600", "7700"):
                emergencies.append({
                    "id": f"ADSB-{t.icao_hex}",
                    "callsign": t.callsign,
                    "squawk": t.squawk,
                })

        for t in sea_tracks:
            cls = classifier.classify_vessel(t)
            sea_by_affil[cls.affiliation] = (
                sea_by_affil.get(cls.affiliation, 0) + 1
            )
            if cls.threat_level >= 7:
                threats.append({
                    "id": f"AIS-{t.mmsi}",
                    "callsign": t.vessel_name or str(t.mmsi),
                    "domain": "sea",
                    "threat_level": cls.threat_level,
                    "affiliation": cls.affiliation,
                })

        unack_alerts = sum(
            1 for a in _alert_history if not a.get("acknowledged")
        )

        return {
            "sitrep": {
                "generated_at": now.isoformat(),
                "classification": "UNCLASSIFIED",
                "summary": {
                    "air_tracks": len(air_tracks),
                    "sea_tracks": len(sea_tracks),
                    "total_tracks": len(air_tracks) + len(sea_tracks),
                    "active_threats": len(threats),
                    "active_emergencies": len(emergencies),
                    "unacknowledged_alerts": unack_alerts,
                    "watchlist_entries": len(_watchlist),
                },
                "air_picture": {
                    "total": len(air_tracks),
                    "by_affiliation": air_by_affil,
                },
                "sea_picture": {
                    "total": len(sea_tracks),
                    "by_affiliation": sea_by_affil,
                },
                "threats": threats,
                "emergencies": emergencies,
                "overrides": len(_classification_overrides),
            },
        }
    except ImportError:
        return {
            "sitrep": {
                "generated_at": now.isoformat(),
                "classification": "UNCLASSIFIED",
                "error": "Engine not running -- no data available",
            },
        }


@router.get("/health")
async def health_check(_user: _Viewer):
    """System health check."""
    return {
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "watchlist_size": len(_watchlist),
        "overrides_active": len(_classification_overrides),
        "alerts_total": len(_alert_history),
        "alerts_unacknowledged": sum(
            1 for a in _alert_history if not a.get("acknowledged")
        ),
    }


# -- LLM-powered intelligence endpoints -------------------------------------


def _get_intel_engine() -> IntelligenceEngine:
    """Get or create the intelligence engine."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    return IntelligenceEngine(api_key=api_key)


@router.get("/sitrep/narrative")
async def generate_narrative_sitrep(
    _user: _Operator,
    format: str = Query("nato", description="nato, flash, or brief"),
):
    """Generate a narrative SITREP using LLM (or template fallback)."""
    raw = await generate_sitrep()
    sitrep_data = raw.get("sitrep", {})

    intel = _get_intel_engine()
    narrative = await intel.generate_sitrep(sitrep_data, format=format)

    return {
        "format": format,
        "narrative": narrative,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "llm_available": intel.is_available,
    }


@router.post("/query")
async def natural_language_query(body: dict, _user: _Operator):
    """Natural language query against the operational picture."""
    query = body.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query' field")

    intel = _get_intel_engine()

    # Try to get a TrackManager from the running server
    tm = None
    try:
        from mpe.server import track_manager as _tm

        tm = _tm
    except (ImportError, AttributeError):
        pass

    # Fall back to building one from aircraft/vessel trackers
    if tm is None:
        try:
            from mpe.track_manager import TrackManager

            tm = TrackManager()
        except ImportError:
            pass

    if tm is not None:
        result = await intel.natural_language_query(query, tm)
    else:
        result = {"answer": "Track manager not available", "count": 0}

    return result


# -- Mission tasking ---------------------------------------------------------


class WaypointInput(BaseModel):
    latitude: float
    longitude: float
    altitude_m: float = 50.0
    speed_mps: float | None = None
    loiter_seconds: float = 0.0


class TaskRequest(BaseModel):
    drone_id: str                        # e.g. "DRONE-ALPHA"
    task_type: str = "goto"              # goto | patrol | survey | loiter
    waypoints: list[WaypointInput]
    priority: int = 5
    max_altitude_m: float = 120.0
    max_speed_mps: float = 30.0
    notes: str = ""
    submitted_by: str = "cop-dashboard"


# In-memory task store (replaced by DB later)
_task_plans: list[dict] = []


@router.post("/task")
async def submit_task(req: TaskRequest, _user: _Operator):
    """Submit a mission task plan for a drone asset.

    Accepts a list of waypoints and drone target ID.
    Returns plan_id which can be used to track status.
    """
    if not req.waypoints:
        raise HTTPException(status_code=400, detail="At least one waypoint required")

    plan_id = f"PLAN-{str(uuid4())[:8].upper()}"
    now = datetime.now(timezone.utc).isoformat()

    plan = {
        "plan_id": plan_id,
        "drone_id": req.drone_id,
        "task_type": req.task_type,
        "status": "planned",
        "priority": req.priority,
        "waypoints": [w.model_dump() for w in req.waypoints],
        "max_altitude_m": req.max_altitude_m,
        "max_speed_mps": req.max_speed_mps,
        "notes": req.notes,
        "submitted_by": req.submitted_by,
        "created_at": now,
        "updated_at": now,
    }
    _task_plans.append(plan)

    return {
        "status": "accepted",
        "plan_id": plan_id,
        "drone_id": req.drone_id,
        "waypoint_count": len(req.waypoints),
        "task_type": req.task_type,
        "created_at": now,
    }


@router.get("/tasks")
async def list_tasks(_user: _Viewer, drone_id: str | None = Query(None)):
    """List submitted task plans, optionally filtered by drone_id."""
    plans = _task_plans
    if drone_id:
        plans = [p for p in plans if p["drone_id"] == drone_id]
    return {"tasks": plans, "total": len(plans)}


@router.get("/tasks/{plan_id}")
async def get_task(plan_id: str, _user: _Viewer):
    """Get a specific task plan by ID."""
    for p in _task_plans:
        if p["plan_id"] == plan_id:
            return p
    raise HTTPException(status_code=404, detail=f"Plan not found: {plan_id}")


@router.delete("/tasks/{plan_id}")
async def cancel_task(plan_id: str, _user: _Operator):
    """Cancel a task plan."""
    for p in _task_plans:
        if p["plan_id"] == plan_id:
            p["status"] = "cancelled"
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
            return {"status": "cancelled", "plan_id": plan_id}
    raise HTTPException(status_code=404, detail=f"Plan not found: {plan_id}")


# -- Helper to register alerts from the engine -------------------------------


def record_alert(alert_event) -> None:
    """Record an alert in the history (called by the engine)."""
    _alert_history.append({
        "alert_id": alert_event.alert_id,
        "entity_id": alert_event.entity_id,
        "alert_type": alert_event.alert_type,
        "severity": alert_event.severity,
        "title": alert_event.title,
        "description": alert_event.description,
        "latitude": alert_event.latitude,
        "longitude": alert_event.longitude,
        "rule_name": alert_event.rule_name,
        "created_at": alert_event.timestamp.isoformat(),
        "acknowledged": False,
    })
