"""Vessel track cache -- maintains a live picture of nearby vessels from AIS data.

Pure-Python in-memory cache of vessel tracks keyed by MMSI.  No external
dependencies -- this module works without pyais installed.

The cache is designed for the mission-planning engine to query during flight:
  - Which vessels are near a planned waypoint?
  - Is the shipping lane clear for low-altitude overwater transit?
  - What is the closest point of approach for a given track?
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class VesselTrack:
    """A single vessel's current state, updated from AIS messages."""

    mmsi: int
    latitude: float = 0.0
    longitude: float = 0.0
    course_over_ground: float = 0.0    # degrees true
    speed_over_ground: float = 0.0     # knots
    heading: float = 0.0               # degrees true
    vessel_name: str = ""
    callsign: str = ""
    imo_number: int = 0
    ship_type: int = 0                 # AIS type code 0-99
    destination: str = ""
    nav_status: int = 15               # 15 = undefined (default)
    last_update: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_stale(self) -> bool:
        """Track is stale if not updated in 5 minutes (300 s)."""
        age = (datetime.now(timezone.utc) - self.last_update).total_seconds()
        return age > 300

    @property
    def speed_mps(self) -> float:
        """Speed in metres per second (1 knot = 0.514444 m/s)."""
        return self.speed_over_ground * 0.514444


class VesselTracker:
    """Thread-safe vessel track cache.

    Maintains a dict of ``{mmsi: VesselTrack}`` updated from decoded AIS
    messages.  Provides query methods for the mission engine.

    Parameters
    ----------
    stale_timeout_s:
        Seconds after which a track without updates is considered stale.
        Defaults to 300 (5 minutes).
    """

    def __init__(self, stale_timeout_s: float = 300) -> None:
        self._tracks: dict[int, VesselTrack] = {}
        self._stale_timeout = stale_timeout_s
        self._lock = threading.Lock()  # FIX #4: Thread safety

    def update(self, mmsi: int, **kwargs) -> VesselTrack:
        """Update or create a vessel track.

        Merges new data with the existing track (AIS sends position and
        static data in separate message types).  ``None`` values in
        *kwargs* are silently ignored so callers can pass raw decoded
        fields without filtering.
        """
        with self._lock:
            if mmsi in self._tracks:
                track = self._tracks[mmsi]
                for key, value in kwargs.items():
                    if hasattr(track, key) and value is not None:
                        setattr(track, key, value)
                track.last_update = datetime.now(timezone.utc)
            else:
                filtered = {k: v for k, v in kwargs.items() if v is not None}
                track = VesselTrack(mmsi=mmsi, **filtered)
                self._tracks[mmsi] = track
        return track

    def get(self, mmsi: int) -> Optional[VesselTrack]:
        """Get a vessel track by MMSI, or ``None`` if not tracked."""
        return self._tracks.get(mmsi)

    @property
    def active_tracks(self) -> list[VesselTrack]:
        """All non-stale vessel tracks."""
        with self._lock:  # FIX #4: Thread-safe snapshot
            return [t for t in self._tracks.values() if not t.is_stale]

    @property
    def all_tracks(self) -> list[VesselTrack]:
        """All vessel tracks including stale."""
        with self._lock:  # FIX #4: Thread-safe snapshot
            return list(self._tracks.values())

    def vessels_near(self, lat: float, lon: float, radius_km: float) -> list[VesselTrack]:
        """Find active vessels within *radius_km* of a point.

        Uses haversine distance from the planner module.  Vessels with
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
            vessel_pos = Coordinate(latitude=track.latitude, longitude=track.longitude)
            dist = _haversine_km(center, vessel_pos)
            if dist <= radius_km:
                results.append(track)
        return results

    def purge_stale(self) -> int:
        """Remove all stale tracks.  Returns number removed."""
        with self._lock:  # FIX #4: Thread-safe purge
            stale_mmsis = [mmsi for mmsi, t in self._tracks.items() if t.is_stale]
            for mmsi in stale_mmsis:
                del self._tracks[mmsi]
        return len(stale_mmsis)
