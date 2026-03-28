"""ADS-B receiver -- fetches aircraft data from free web APIs.

Primary: airplanes.live (free, no auth, ~1 req/sec)
Backup: OpenSky Network (free with registration)

No hardware required -- uses HTTP APIs from community ADS-B networks.
No external dependencies -- uses only stdlib (urllib, json, threading).
"""

from __future__ import annotations

import json
import threading
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

from mpe.aircraft_tracker import AircraftTracker


class ADSBError(Exception):
    """Raised when ADS-B receiver encounters an error."""


class ADSBReceiver:
    """Fetches ADS-B data from web APIs and updates an AircraftTracker.

    Parameters
    ----------
    tracker:
        AircraftTracker instance to update with received data.
    center_lat, center_lon:
        Centre point for queries (default: Epsom area).
    radius_nm:
        Query radius in nautical miles (max 250 for airplanes.live).
    poll_interval_s:
        Seconds between API polls (default 5, respect rate limits).
    source:
        API source -- ``"airplanes_live"`` or ``"opensky"``.
    """

    def __init__(
        self,
        tracker: AircraftTracker,
        center_lat: float = 51.3632,
        center_lon: float = -0.2652,
        radius_nm: int = 100,
        poll_interval_s: float = 5.0,
        source: str = "airplanes_live",
    ) -> None:
        self._tracker = tracker
        self._lat = center_lat
        self._lon = center_lon
        self._radius_nm = min(radius_nm, 250)
        self._interval = poll_interval_s
        self._source = source
        self._running = False
        self._thread: threading.Thread | None = None

    def fetch_once(self) -> int:
        """Fetch current aircraft data and update tracker.

        Returns
        -------
        int
            Number of aircraft updated.
        """
        if self._source == "airplanes_live":
            return self._fetch_airplanes_live()
        elif self._source == "opensky":
            return self._fetch_opensky()
        else:
            raise ADSBError(f"Unknown source: {self._source}")

    def _fetch_airplanes_live(self) -> int:
        """Fetch from airplanes.live free API."""
        url = (
            f"https://api.airplanes.live/v2/point/"
            f"{self._lat}/{self._lon}/{self._radius_nm}"
        )
        req = Request(url, headers={"User-Agent": "MPE-C2/1.0"})

        try:
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
        except (URLError, json.JSONDecodeError, OSError) as exc:
            raise ADSBError(f"Failed to fetch from airplanes.live: {exc}")

        aircraft_list = data.get("ac", [])
        count = 0
        for ac in aircraft_list:
            hex_code = ac.get("hex", "").strip()
            if not hex_code:
                continue

            self._tracker.update(
                icao_hex=hex_code,
                latitude=ac.get("lat"),
                longitude=ac.get("lon"),
                altitude_baro_ft=(
                    ac.get("alt_baro")
                    if isinstance(ac.get("alt_baro"), (int, float))
                    else None
                ),
                altitude_geom_ft=ac.get("alt_geom"),
                ground_speed_kts=ac.get("gs"),
                heading=ac.get("track"),
                vertical_rate_fpm=ac.get("baro_rate"),
                callsign=(ac.get("flight") or "").strip(),
                squawk=str(ac.get("squawk", "")),
                category=ac.get("category"),
                aircraft_type=ac.get("t", ""),
                registration=ac.get("r", ""),
                on_ground=bool(ac.get("ground")),
            )
            count += 1

        return count

    def _fetch_opensky(self) -> int:
        """Fetch from OpenSky Network free API."""
        # OpenSky uses bounding box (lat/lon in degrees)
        delta = self._radius_nm * 1.852 / 111.0  # rough degree conversion
        url = (
            f"https://opensky-network.org/api/states/all"
            f"?lamin={self._lat - delta}&lomin={self._lon - delta}"
            f"&lamax={self._lat + delta}&lomax={self._lon + delta}"
        )
        req = Request(url, headers={"User-Agent": "MPE-C2/1.0"})

        try:
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
        except (URLError, json.JSONDecodeError, OSError) as exc:
            raise ADSBError(f"Failed to fetch from OpenSky: {exc}")

        states = data.get("states", [])
        if states is None:
            return 0

        count = 0
        for state in states:
            # OpenSky state vector format:
            # [0]  icao24          [1]  callsign       [2]  origin_country
            # [3]  time_position   [4]  last_contact   [5]  longitude
            # [6]  latitude        [7]  baro_altitude  [8]  on_ground
            # [9]  velocity        [10] true_track      [11] vertical_rate
            # [12] sensors         [13] geo_altitude    [14] squawk
            # [15] spi             [16] position_source
            if len(state) < 17:
                continue
            hex_code = state[0]
            if not hex_code:
                continue

            self._tracker.update(
                icao_hex=hex_code,
                callsign=(state[1] or "").strip(),
                latitude=state[6],
                longitude=state[5],
                altitude_baro_ft=(
                    (state[7] or 0) * 3.28084 if state[7] else None
                ),  # OpenSky gives metres
                altitude_geom_ft=(
                    (state[13] or 0) * 3.28084 if state[13] else None
                ),
                on_ground=bool(state[8]),
                ground_speed_kts=(
                    (state[9] or 0) * 1.94384 if state[9] else None
                ),  # m/s to knots
                heading=state[10],
                vertical_rate_fpm=(
                    (state[11] or 0) * 196.85 if state[11] else None
                ),  # m/s to ft/min
                squawk=str(state[14]) if state[14] else "",
            )
            count += 1

        return count

    def start_polling(self) -> None:
        """Start polling in background thread."""
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop polling."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _poll_loop(self) -> None:
        """Background polling loop."""
        while self._running:
            try:
                self.fetch_once()
            except ADSBError:
                pass  # Log in future, continue polling
            time.sleep(self._interval)
