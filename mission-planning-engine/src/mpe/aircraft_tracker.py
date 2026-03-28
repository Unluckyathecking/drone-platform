"""Aircraft track cache -- maintains a live picture of nearby aircraft from ADS-B data.

Pure-Python in-memory cache of aircraft tracks keyed by ICAO 24-bit address.
No external dependencies -- this module works with only the standard library.

The cache is designed for the mission-planning engine to query during flight:
  - Which aircraft are near a planned waypoint?
  - Is the airspace clear for a given altitude band?
  - Are there any emergency squawks nearby?

Follows the same pattern as vessel_tracker.py for consistency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class AircraftTrack:
    """A single aircraft's current state from ADS-B."""

    icao_hex: str                        # 24-bit ICAO address (e.g. "4CA7B5")
    latitude: float = 0.0
    longitude: float = 0.0
    altitude_baro_ft: float = 0.0        # Barometric altitude in feet
    altitude_geom_ft: float = 0.0        # Geometric (GPS) altitude in feet
    ground_speed_kts: float = 0.0        # Ground speed in knots
    heading: float = 0.0                 # Track angle degrees true
    vertical_rate_fpm: float = 0.0       # Vertical rate ft/min
    callsign: str = ""                   # Flight number or registration
    squawk: str = ""                     # Transponder squawk code
    category: str = ""                   # ADS-B emitter category (A1-A7, B1-B7)
    aircraft_type: str = ""              # ICAO type designator (e.g. "B738")
    registration: str = ""               # Aircraft registration (e.g. "G-ABCD")
    on_ground: bool = False
    last_update: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_stale(self) -> bool:
        """Track is stale if not updated in 60 seconds (aircraft move fast)."""
        age = (datetime.now(timezone.utc) - self.last_update).total_seconds()
        return age > 60

    @property
    def altitude_m(self) -> float:
        """Best altitude in metres (prefer geometric, fall back to baro)."""
        alt_ft = self.altitude_geom_ft if self.altitude_geom_ft else self.altitude_baro_ft
        return alt_ft * 0.3048

    @property
    def speed_mps(self) -> float:
        """Ground speed in metres per second (1 knot = 0.514444 m/s)."""
        return self.ground_speed_kts * 0.514444

    @property
    def is_emergency(self) -> bool:
        """Check for emergency squawk codes.

        7500 = hijack, 7600 = radio failure, 7700 = general emergency.
        """
        return self.squawk in ("7500", "7600", "7700")


class AircraftTracker:
    """Thread-safe aircraft track cache, following VesselTracker pattern.

    Maintains a dict of ``{icao_hex: AircraftTrack}`` updated from decoded
    ADS-B data.  Provides query methods for the mission engine.

    Parameters
    ----------
    stale_timeout_s:
        Seconds after which a track without updates is considered stale.
        Defaults to 60 (1 minute -- aircraft move much faster than vessels).
    """

    def __init__(self, stale_timeout_s: float = 60) -> None:
        self._tracks: dict[str, AircraftTrack] = {}
        self._stale_timeout = stale_timeout_s

    def update(self, icao_hex: str, **kwargs) -> AircraftTrack:
        """Update or create an aircraft track.

        Merges new data with the existing track (ADS-B sends various data
        fields across different message types).  ``None`` values in *kwargs*
        are silently ignored so callers can pass raw decoded fields without
        filtering.
        """
        icao = icao_hex.upper()
        if icao in self._tracks:
            track = self._tracks[icao]
            for key, value in kwargs.items():
                if hasattr(track, key) and value is not None:
                    setattr(track, key, value)
            track.last_update = datetime.now(timezone.utc)
        else:
            filtered = {k: v for k, v in kwargs.items() if v is not None}
            track = AircraftTrack(icao_hex=icao, **filtered)
            self._tracks[icao] = track
        return track

    def get(self, icao_hex: str) -> Optional[AircraftTrack]:
        """Get an aircraft track by ICAO hex, or ``None`` if not tracked."""
        return self._tracks.get(icao_hex.upper())

    @property
    def active_tracks(self) -> list[AircraftTrack]:
        """All non-stale aircraft tracks."""
        return [t for t in self._tracks.values() if not t.is_stale]

    @property
    def all_tracks(self) -> list[AircraftTrack]:
        """All aircraft tracks including stale."""
        return list(self._tracks.values())

    def aircraft_near(self, lat: float, lon: float, radius_km: float) -> list[AircraftTrack]:
        """Find active aircraft within *radius_km* of a point.

        Uses haversine distance from the planner module.  Aircraft with
        latitude/longitude still at 0.0 (no position report received yet)
        are excluded.
        """
        from mpe.planner import _haversine_km
        from mpe.models import Coordinate

        center = Coordinate(latitude=lat, longitude=lon)
        results = []
        for track in self.active_tracks:
            if track.latitude == 0.0 and track.longitude == 0.0:
                continue
            pos = Coordinate(latitude=track.latitude, longitude=track.longitude)
            dist = _haversine_km(center, pos)
            if dist <= radius_km:
                results.append(track)
        return results

    def emergencies(self) -> list[AircraftTrack]:
        """Get all active aircraft currently squawking emergency."""
        return [t for t in self.active_tracks if t.is_emergency]

    def purge_stale(self) -> int:
        """Remove all stale tracks.  Returns number removed."""
        stale_keys = [k for k, t in self._tracks.items() if t.is_stale]
        for k in stale_keys:
            del self._tracks[k]
        return len(stale_keys)
