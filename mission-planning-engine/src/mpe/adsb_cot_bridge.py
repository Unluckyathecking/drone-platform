"""ADS-B-to-CoT bridge -- converts aircraft tracks to CoT events for TAK display.

Takes AircraftTrack objects from the AircraftTracker and generates CoT XML
events with proper airborne type codes (a-n-A-C-F for neutral civilian
fixed-wing, etc.).

This module uses duck-typing: any object with the expected attributes
(icao_hex, latitude, longitude, etc.) works -- no import of AircraftTrack
needed.

Transport is out of scope; the caller is responsible for sending the XML
strings via PyTAK or multicast UDP (see ``cot_sender.py``).

Follows the same pattern as ais_cot_bridge.py for consistency.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# Knots-to-m/s conversion factor
_KNOTS_TO_MPS = 0.514444

# Feet-to-metres conversion factor
_FT_TO_M = 0.3048

# Emergency squawk descriptions
_SQUAWK_LABELS: dict[str, str] = {
    "7500": "HIJACK",
    "7600": "RADIO FAILURE",
    "7700": "EMERGENCY",
}


class ADSBCoTBridge:
    """Converts aircraft tracks to Cursor on Target 2.0 XML events.

    Parameters
    ----------
    stale_seconds:
        How long events persist on the ATAK map before going stale.
        Default 120 (2 minutes -- aircraft move fast).
    uid_prefix:
        Prefix for aircraft UIDs.  Final UID is ``{uid_prefix}-{icao_hex}``.
        Default ``"ADSB"``.
    """

    def __init__(self, stale_seconds: int = 120, uid_prefix: str = "ADSB") -> None:
        self._stale_seconds = stale_seconds
        self._uid_prefix = uid_prefix

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def aircraft_to_cot(self, track) -> str:
        """Convert a single aircraft track to a CoT XML event string.

        Parameters
        ----------
        track:
            Any object exposing ``icao_hex``, ``latitude``, ``longitude``,
            ``heading``, ``ground_speed_kts``, ``callsign``, ``category``,
            ``altitude_geom_ft``, ``altitude_baro_ft``, and optionally
            ``aircraft_type``, ``registration``, ``squawk``.

        Returns
        -------
        str
            CoT XML string ready for PyTAK transmission.
        """
        cot_type = self._resolve_cot_type(track)

        now = datetime.now(tz=timezone.utc)
        time_str = _format_iso8601(now)
        stale_str = _format_iso8601(now + timedelta(seconds=self._stale_seconds))

        uid = f"{self._uid_prefix}-{track.icao_hex}"
        callsign = self._resolve_callsign(track)

        event = ET.Element("event", attrib={
            "version": "2.0",
            "type": cot_type,
            "uid": uid,
            "how": "m-g",
            "time": time_str,
            "start": time_str,
            "stale": stale_str,
        })

        # Height above ellipsoid from geometric altitude (preferred) or baro
        hae = self._resolve_altitude_m(track)

        ET.SubElement(event, "point", attrib={
            "lat": str(track.latitude),
            "lon": str(track.longitude),
            "hae": f"{hae:.1f}",
            "ce": "50.0",   # ADS-B GPS accuracy ~50 m typical
            "le": "30.0",   # Altitude accuracy ~30 m
        })

        detail = ET.SubElement(event, "detail")
        ET.SubElement(detail, "contact", attrib={"callsign": callsign})

        speed_mps = (
            track.ground_speed_kts * _KNOTS_TO_MPS
            if hasattr(track, "ground_speed_kts")
            else 0.0
        )
        course = (
            track.heading
            if hasattr(track, "heading")
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
        """Convert multiple aircraft tracks to CoT XML strings.

        Tracks with no valid position (lat == 0 and lon == 0) are skipped.
        """
        return [
            self.aircraft_to_cot(track)
            for track in tracks
            if not (track.latitude == 0.0 and track.longitude == 0.0)
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_cot_type(track) -> str:
        """Resolve the CoT type code from the aircraft's ADS-B category.

        Tries to import ``mpe.adsb_types``.  Falls back to ``a-u-A``
        (unknown air) when the module is unavailable.
        """
        try:
            from mpe.adsb_types import adsb_category_to_cot
            category = getattr(track, "category", None)
            return adsb_category_to_cot(category)
        except (ImportError, AttributeError):
            return "a-u-A"

    @staticmethod
    def _resolve_callsign(track) -> str:
        """Resolve the best callsign: flight > registration > ICAO hex."""
        callsign = getattr(track, "callsign", "")
        if callsign:
            return callsign
        registration = getattr(track, "registration", "")
        if registration:
            return registration
        return track.icao_hex

    @staticmethod
    def _resolve_altitude_m(track) -> float:
        """Best altitude in metres (prefer geometric, fall back to baro)."""
        geom = getattr(track, "altitude_geom_ft", 0.0) or 0.0
        baro = getattr(track, "altitude_baro_ft", 0.0) or 0.0
        alt_ft = geom if geom else baro
        return alt_ft * _FT_TO_M

    @staticmethod
    def _build_remarks(track) -> str:
        """Build the remarks text from available aircraft fields."""
        parts: list[str] = []

        callsign = getattr(track, "callsign", "")
        if callsign:
            parts.append(f"Callsign: {callsign}")

        parts.append(f"ICAO: {track.icao_hex}")

        aircraft_type = getattr(track, "aircraft_type", "")
        if aircraft_type:
            parts.append(f"Type: {aircraft_type}")

        registration = getattr(track, "registration", "")
        if registration:
            parts.append(f"Reg: {registration}")

        squawk = getattr(track, "squawk", "")
        if squawk:
            label = _SQUAWK_LABELS.get(squawk)
            if label:
                parts.append(f"Squawk: {squawk} [{label}]")
            else:
                parts.append(f"Squawk: {squawk}")

        return " | ".join(parts)


# ------------------------------------------------------------------
# Module-private helpers
# ------------------------------------------------------------------

def _format_iso8601(dt: datetime) -> str:
    """Format a datetime as ISO 8601 with Z suffix (UTC only)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
