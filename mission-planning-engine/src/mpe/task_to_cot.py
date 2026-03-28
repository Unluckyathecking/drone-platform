"""Task-to-CoT translator -- converts C2 Tasks to CoT events for ATAK display.

Translates TaskPlan/Task objects into CoT XML events so operators on ATAK
can see planned missions, assigned tasks, and entity positions.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# CoT affiliation codes
_AFF_MAP = {
    "friendly": "f",
    "hostile": "h",
    "neutral": "n",
    "unknown": "u",
    "suspect": "j",
}

# CoT dimension codes (domain -> battle dimension)
_DOMAIN_MAP = {
    "air": "A",
    "sea": "S",
    "land": "G",
    "subsurface": "U",
}

# Entity-type suffixes for more specific CoT typing
_TYPE_SUFFIX: dict[str, str] = {
    "uav": "-M-F-Q",
    "fixed_wing": "-M-F-Q",
    "rotary_wing": "-M-H-Q",
    "person": "",  # handled specially
}


def _cot_type_for_entity(entity) -> str:
    """Build a CoT type string from an entity's affiliation, domain, and type."""
    aff = _AFF_MAP.get(str(entity.affiliation), "u")
    dim = _DOMAIN_MAP.get(str(entity.domain), "A")

    entity_type = str(entity.entity_type)

    if entity_type == "person":
        return f"a-{aff}-G-U-C"

    base = f"a-{aff}-{dim}"
    suffix = _TYPE_SUFFIX.get(entity_type, "")
    return base + suffix


def _time_pair(stale_seconds: int) -> tuple[str, str]:
    """Return (now_iso, stale_iso) formatted for CoT."""
    now = datetime.now(tz=timezone.utc)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    return (
        now.strftime(fmt),
        (now + timedelta(seconds=stale_seconds)).strftime(fmt),
    )


class CoTTranslator:
    """Translates C2 models to CoT XML events.

    Maps:
    - Entity -> position report event (a-f-A for friendly air, etc.)
    - Task waypoints -> waypoint events (b-m-p-w)
    - Track -> observed entity event (a-n-S for neutral surface, etc.)
    """

    def __init__(self, stale_seconds: int = 120) -> None:
        self._stale_seconds = stale_seconds

    def entity_to_cot(self, entity) -> str | None:
        """Convert an Entity to a CoT position report.

        Returns None if entity has no position.
        """
        if entity.position is None:
            return None

        cot_type = _cot_type_for_entity(entity)
        time_str, stale_str = _time_pair(self._stale_seconds)

        uid = entity.uid
        callsign = entity.callsign or entity.name or uid

        event = ET.Element(
            "event",
            attrib={
                "version": "2.0",
                "type": cot_type,
                "uid": uid,
                "how": "m-g",
                "time": time_str,
                "start": time_str,
                "stale": stale_str,
            },
        )

        ET.SubElement(
            event,
            "point",
            attrib={
                "lat": str(entity.position.latitude),
                "lon": str(entity.position.longitude),
                "hae": str(entity.position.altitude_m),
                "ce": "9999999",
                "le": "9999999",
            },
        )

        detail = ET.SubElement(event, "detail")
        ET.SubElement(detail, "contact", attrib={"callsign": callsign})
        ET.SubElement(
            detail,
            "track",
            attrib={
                "course": str(entity.position.heading),
                "speed": str(entity.position.speed_mps),
            },
        )

        return ET.tostring(event, encoding="unicode", xml_declaration=False)

    def task_waypoints_to_cot(
        self,
        task,
        uid_prefix: str = "TSK",
    ) -> list[str]:
        """Convert a Task's waypoints to CoT waypoint events.

        Each waypoint becomes a b-m-p-w (waypoint) event on ATAK.
        """
        events: list[str] = []

        for i, wp in enumerate(task.waypoints):
            time_str, stale_str = _time_pair(self._stale_seconds)
            uid = f"{uid_prefix}-{task.task_id}-WP{i}"

            event = ET.Element(
                "event",
                attrib={
                    "version": "2.0",
                    "type": "b-m-p-w",
                    "uid": uid,
                    "how": "h-e",
                    "time": time_str,
                    "start": time_str,
                    "stale": stale_str,
                },
            )

            alt = wp.altitude_m if wp.altitude_m is not None else 0.0

            ET.SubElement(
                event,
                "point",
                attrib={
                    "lat": str(wp.position.latitude),
                    "lon": str(wp.position.longitude),
                    "hae": str(alt),
                    "ce": "9999999",
                    "le": "9999999",
                },
            )

            detail = ET.SubElement(event, "detail")
            name = wp.name or f"WP{i}"
            ET.SubElement(detail, "contact", attrib={"callsign": name})
            remarks = ET.SubElement(detail, "remarks")
            remarks.text = f"Task: {task.task_id} ({task.task_type}) waypoint {i}"

            events.append(
                ET.tostring(event, encoding="unicode", xml_declaration=False)
            )

        return events
