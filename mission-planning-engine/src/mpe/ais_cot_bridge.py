"""AIS-to-CoT bridge -- converts vessel tracks to CoT events for TAK display.

Takes VesselTrack objects from the VesselTracker and generates CoT XML events
with proper maritime type codes (a-n-S for neutral surface, etc.).

This module uses duck-typing: any object with the expected attributes
(mmsi, latitude, longitude, etc.) works -- no import of VesselTrack needed.

Transport is out of scope; the caller is responsible for sending the XML
strings via PyTAK or multicast UDP (see ``cot_sender.py``).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# Knots-to-m/s conversion factor
_KNOTS_TO_MPS = 0.514444

# Navigation status labels per ITU-R M.1371-5 Table 45
_NAV_STATUS_LABELS: dict[int, str] = {
    0: "Underway",
    1: "At anchor",
    2: "Not under command",
    3: "Restricted manoeuvrability",
    5: "Moored",
    8: "Sailing",
}


class AISCoTBridge:
    """Converts vessel tracks to Cursor on Target 2.0 XML events.

    Parameters
    ----------
    stale_seconds:
        How long events persist on the ATAK map before going stale.
        Default 300 (5 minutes).
    uid_prefix:
        Prefix for vessel UIDs.  Final UID is ``{uid_prefix}-{mmsi}``.
        Default ``"AIS"``.
    """

    def __init__(self, stale_seconds: int = 300, uid_prefix: str = "AIS") -> None:
        self._stale_seconds = stale_seconds
        self._uid_prefix = uid_prefix

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def vessel_to_cot(self, track) -> str:
        """Convert a single vessel track to a CoT XML event string.

        Parameters
        ----------
        track:
            Any object exposing ``mmsi``, ``latitude``, ``longitude``,
            ``course_over_ground``, ``speed_over_ground``, ``vessel_name``,
            ``ship_type``, and optionally ``destination`` and ``nav_status``.

        Returns
        -------
        str
            CoT XML string ready for PyTAK transmission.
        """
        cot_type = self._resolve_cot_type(track)

        now = datetime.now(tz=timezone.utc)
        time_str = _format_iso8601(now)
        stale_str = _format_iso8601(now + timedelta(seconds=self._stale_seconds))

        uid = f"{self._uid_prefix}-{track.mmsi}"
        callsign = track.vessel_name if track.vessel_name else f"MMSI-{track.mmsi}"

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
            "lat": str(track.latitude),
            "lon": str(track.longitude),
            "hae": "0.0",   # Sea level
            "ce": "10.0",   # AIS GPS accuracy ~10 m
            "le": "0.0",
        })

        detail = ET.SubElement(event, "detail")
        ET.SubElement(detail, "contact", attrib={"callsign": callsign})

        speed_mps = (
            track.speed_over_ground * _KNOTS_TO_MPS
            if hasattr(track, "speed_over_ground")
            else 0.0
        )
        course = (
            track.course_over_ground
            if hasattr(track, "course_over_ground")
            else 0.0
        )
        ET.SubElement(detail, "track", attrib={
            "course": f"{course:.1f}",
            "speed": f"{speed_mps:.1f}",
        })

        remarks = ET.SubElement(detail, "remarks")
        remarks.text = self._build_remarks(track)

        return ET.tostring(event, encoding="unicode", xml_declaration=False)

    def tracks_to_cot(self, tracks: list) -> list[str]:
        """Convert multiple vessel tracks to CoT XML strings.

        Tracks with no valid position (lat == 0 and lon == 0) are skipped.
        """
        return [
            self.vessel_to_cot(track)
            for track in tracks
            if not (track.latitude == 0.0 and track.longitude == 0.0)
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_cot_type(track) -> str:
        """Resolve the CoT type code from the vessel's AIS ship type.

        Tries to import ``mpe.ais_types`` (built by another agent).  Falls
        back to ``a-n-S`` (neutral surface) when the module is unavailable.
        """
        try:
            from mpe.ais_types import ais_type_to_cot  # type: ignore[import-untyped]
            return ais_type_to_cot(track.ship_type)
        except (ImportError, AttributeError):
            return "a-n-S"

    @staticmethod
    def _build_remarks(track) -> str:
        """Build the remarks text from available vessel fields."""
        parts: list[str] = []
        if track.vessel_name:
            parts.append(f"Name: {track.vessel_name}")
        parts.append(f"MMSI: {track.mmsi}")
        if hasattr(track, "destination") and track.destination:
            parts.append(f"Dest: {track.destination}")
        if hasattr(track, "nav_status") and track.nav_status != 15:
            label = _NAV_STATUS_LABELS.get(track.nav_status, str(track.nav_status))
            parts.append(f"Status: {label}")
        return " | ".join(parts)


# ------------------------------------------------------------------
# Module-private helpers
# ------------------------------------------------------------------

def _format_iso8601(dt: datetime) -> str:
    """Format a datetime as ISO 8601 with Z suffix (UTC only)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
