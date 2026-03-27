"""Cursor on Target (CoT) XML writer for mission items.

Generates CoT 2.0 event XML from MissionItem data. Each waypoint becomes
a CoT ``<event>`` element with point, detail/contact, detail/track, and
detail/remarks sub-elements.

Limitations:
    - ``hae`` (height above ellipsoid) is approximated from AGL altitude plus
      an optional ``geoid_offset_m``. For accurate HAE you need a geoid model
      (e.g. EGM96) to convert the WGS-84 altitude — this is deferred to a
      future geoid lookup module.
    - ``ce`` and ``le`` (circular / linear error) default to 9999999 (unknown).
    - ``course`` and ``speed`` default to 0.0 for static waypoint plans.

Transport (e.g. via PyTAK or multicast UDP) is out of scope for this module.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from mpe.cot_types import MAVCMD_TO_COT, WAYPOINT
from mpe.models import MissionItem
from mpe.writers.base import MissionWriter


class CoTWriter(MissionWriter):
    """Writes mission items as Cursor on Target 2.0 XML events.

    Parameters
    ----------
    callsign:
        Radio callsign placed in ``<contact callsign="..."/>``.
    uid_prefix:
        Prefix for auto-generated UIDs (``{uid_prefix}-{seq}``).
    stale_seconds:
        Seconds after ``time`` before the event is considered stale.
    geoid_offset_m:
        Metres to add to AGL altitude to approximate HAE.
        Set to the local geoid undulation for better accuracy.
    """

    def __init__(
        self,
        callsign: str = "MPE-DRONE",
        uid_prefix: str = "MPE",
        stale_seconds: int = 120,
        geoid_offset_m: float = 0.0,
    ) -> None:
        self._callsign = callsign
        self._uid_prefix = uid_prefix
        self._stale_seconds = stale_seconds
        self._geoid_offset_m = geoid_offset_m

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def format(self, items: list[MissionItem]) -> str:
        """Format mission items as a single CoT XML string.

        Wraps all events in a ``<events>`` root element so the output is
        well-formed XML even with multiple events.
        """
        now = datetime.now(tz=timezone.utc)
        events = self.mission_to_events(items, base_time=now)
        root = ET.Element("events")
        for event_xml in events:
            root.append(ET.fromstring(event_xml))
        return ET.tostring(root, encoding="unicode", xml_declaration=False)

    def format_event(
        self,
        item: MissionItem,
        uid: str,
        base_time: datetime | None = None,
        stale_seconds: int | None = None,
        cot_type: str | None = None,
    ) -> str:
        """Render a single MissionItem as a CoT event XML string.

        Parameters
        ----------
        item:
            The mission item to convert.
        uid:
            Unique identifier for this event.
        base_time:
            Timestamp for the event. Defaults to now (UTC).
        stale_seconds:
            Override the instance default for stale offset.
        cot_type:
            Override the CoT type code. If ``None``, the type is resolved
            from the item's MAVCmd via ``MAVCMD_TO_COT``.
        """
        if base_time is None:
            base_time = datetime.now(tz=timezone.utc)
        if stale_seconds is None:
            stale_seconds = self._stale_seconds

        if cot_type is None:
            cot_type = MAVCMD_TO_COT.get(item.command, WAYPOINT)
        time_str = _format_iso8601(base_time)
        stale_str = _format_iso8601(base_time + timedelta(seconds=stale_seconds))
        hae = item.altitude + self._geoid_offset_m

        event = ET.Element("event", attrib={
            "version": "2.0",
            "type": cot_type,
            "uid": uid,
            "how": "m-g",
            "time": time_str,
            "start": time_str,
            "stale": stale_str,
        })

        ET.SubElement(event, "point", attrib={
            "lat": str(item.latitude),
            "lon": str(item.longitude),
            "hae": str(hae),
            "ce": "9999999",
            "le": "9999999",
        })

        detail = ET.SubElement(event, "detail")
        ET.SubElement(detail, "contact", attrib={"callsign": self._callsign})
        ET.SubElement(detail, "track", attrib={"course": "0.0", "speed": "0.0"})
        remarks = ET.SubElement(detail, "remarks")
        remarks.text = f"Mission item seq={item.seq} cmd={item.command.name}"

        return ET.tostring(event, encoding="unicode", xml_declaration=False)

    def mission_to_events(
        self,
        items: list[MissionItem],
        base_time: datetime | None = None,
        stale_seconds: int | None = None,
    ) -> list[str]:
        """Convert all mission items to a list of CoT event XML strings.

        Parameters
        ----------
        items:
            Ordered list of mission items.
        base_time:
            Timestamp for all events. Defaults to now (UTC).
        stale_seconds:
            Override the instance default for stale offset.
        """
        if base_time is None:
            base_time = datetime.now(tz=timezone.utc)

        return [
            self.format_event(
                item,
                uid=f"{self._uid_prefix}-{item.seq}",
                base_time=base_time,
                stale_seconds=stale_seconds,
            )
            for item in items
        ]


# ------------------------------------------------------------------
# Private helpers
# ------------------------------------------------------------------

def _format_iso8601(dt: datetime) -> str:
    """Format a datetime as ISO 8601 with Z suffix (UTC only)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
