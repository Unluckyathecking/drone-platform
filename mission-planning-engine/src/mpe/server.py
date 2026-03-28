"""C2 Dashboard API server.

Serves live multi-domain tracking data (aircraft, vessels, own forces)
as GeoJSON endpoints for the web frontend.

Global coverage: fetches aircraft from 30+ regions in parallel via
airplanes.live (including military endpoint), generates 570+ realistic
vessel tracks along every major shipping lane, and simulates 5 own-force
drones at strategic locations.

Run: uvicorn mpe.server:app --reload --port 8080
"""

from __future__ import annotations

import json
import math
import random
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from mpe.aircraft_tracker import AircraftTracker
from mpe.adsb_receiver import ADSBReceiver, ADSBError
from mpe.vessel_tracker import VesselTracker
from mpe.classifier import EntityClassifier
from mpe.adsb_types import adsb_category_to_cot
from mpe.ais_types import ais_type_to_cot
from mpe.operator_api import router as operator_router

app = FastAPI(title="MPE C2 Dashboard", version="0.3.0")
app.include_router(operator_router)

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global state ──
aircraft_tracker = AircraftTracker()
vessel_tracker = VesselTracker()
classifier = EntityClassifier()
adsb_receiver = ADSBReceiver(
    aircraft_tracker,
    center_lat=51.3632,  # Default: Epsom
    center_lon=-0.2652,
    radius_nm=250,
)

# ── Cache for global data ──
_cache: dict = {
    "aircraft_raw": None,
    "aircraft_ts": 0.0,
    "vessels_generated": False,
}
CACHE_TTL = 10  # seconds

# ── Global fetch points for airplanes.live point queries (30+ regions) ──
GLOBAL_FETCH_POINTS: list[tuple[float, float, int]] = [
    # Europe
    (51.5, -0.1, 250),      # London/UK
    (48.9, 2.3, 250),       # Paris/France
    (52.5, 13.4, 200),      # Berlin/Germany
    (41.9, 12.5, 200),      # Rome/Italy
    (40.4, -3.7, 200),      # Madrid/Spain
    (59.3, 18.1, 200),      # Stockholm/Baltic
    (60.2, 24.9, 200),      # Helsinki/Finland

    # Middle East — CRITICAL (Strait of Hormuz)
    (26.0, 56.5, 250),      # Strait of Hormuz
    (25.3, 55.3, 200),      # Dubai/UAE
    (24.5, 54.6, 200),      # Abu Dhabi
    (21.4, 39.8, 200),      # Jeddah/Red Sea
    (30.0, 48.0, 200),      # Persian Gulf north
    (27.0, 50.5, 200),      # Bahrain/Qatar

    # Suez Canal area
    (30.0, 32.5, 200),      # Suez Canal
    (12.8, 45.0, 200),      # Bab el-Mandeb/Gulf of Aden

    # Asia
    (1.35, 103.8, 250),     # Singapore/Strait of Malacca
    (35.7, 139.7, 250),     # Tokyo/Japan
    (37.5, 127.0, 200),     # Seoul/Korea
    (22.3, 114.2, 200),     # Hong Kong
    (25.0, 121.5, 200),     # Taiwan Strait
    (31.2, 121.5, 200),     # Shanghai
    (14.5, 121.0, 200),     # Manila/Philippines
    (10.8, 106.7, 200),     # Ho Chi Minh/South China Sea

    # Americas
    (40.7, -74.0, 250),     # New York
    (33.9, -118.2, 250),    # Los Angeles
    (25.8, -80.2, 200),     # Miami/Caribbean
    (9.0, -79.5, 200),      # Panama Canal
    (4.6, -74.1, 200),      # Bogota/Colombia
    (-23.5, -46.6, 200),    # Sao Paulo/Brazil

    # Africa
    (-34.0, 18.5, 200),     # Cape Town/Cape of Good Hope
    (6.5, 3.4, 200),        # Lagos/Gulf of Guinea
    (-1.3, 36.8, 200),      # Nairobi

    # Oceania
    (-33.9, 151.2, 250),    # Sydney
]

# ── Country display names ──
COUNTRY_NAMES: dict[str, str] = {
    "co": "Colombia",
    "ph": "Philippines",
    "ee": "Estonia",
    "lv": "Latvia",
    "lt": "Lithuania",
    "pl": "Poland",
    "ro": "Romania",
    "gb": "United Kingdom",
    "fi": "Finland",
    "no": "Norway",
    "se": "Sweden",
    "jp": "Japan",
    "kr": "South Korea",
    "in": "India",
    "sa": "Saudi Arabia",
    "ae": "UAE",
    "br": "Brazil",
    "mx": "Mexico",
    "ng": "Nigeria",
    "ke": "Kenya",
    "au": "Australia",
    "ca": "Canada",
    "tw": "Taiwan",
    "ua": "Ukraine",
    "global": "Global",
}

# Country bounding boxes [sw_lat, sw_lon, ne_lat, ne_lon] — ISO alpha-2 keys
COUNTRY_BOUNDS: dict[str, list[str]] = {
    "co": ["-4.23", "-79.00", "12.46", "-66.87"],
    "ph": ["4.64", "116.93", "21.12", "126.60"],
    "ee": ["57.52", "21.83", "59.68", "28.21"],
    "lv": ["55.67", "20.97", "58.08", "28.24"],
    "lt": ["53.89", "20.95", "56.45", "26.87"],
    "pl": ["49.00", "14.12", "54.84", "24.15"],
    "ro": ["43.62", "20.26", "48.27", "29.69"],
    "gb": ["49.96", "-7.57", "58.64", "1.68"],
    "fi": ["59.81", "20.55", "70.09", "31.59"],
    "no": ["57.96", "4.99", "71.19", "31.17"],
    "se": ["55.34", "11.11", "69.06", "24.17"],
    "jp": ["24.40", "122.93", "45.52", "153.99"],
    "kr": ["33.19", "124.60", "38.61", "131.87"],
    "in": ["6.75", "68.16", "35.50", "97.40"],
    "sa": ["16.38", "34.63", "32.16", "55.67"],
    "ae": ["22.63", "51.58", "26.08", "56.38"],
    "br": ["-33.75", "-73.98", "5.27", "-34.79"],
    "mx": ["14.53", "-118.60", "32.72", "-86.71"],
    "ng": ["4.27", "2.69", "13.89", "14.68"],
    "ke": ["-4.68", "33.91", "5.03", "41.90"],
    "au": ["-43.64", "113.15", "-10.06", "153.64"],
    "ca": ["41.68", "-141.00", "83.11", "-52.62"],
    "tw": ["21.90", "119.53", "25.30", "122.01"],
    "ua": ["44.39", "22.14", "52.38", "40.23"],
    "global": ["-60", "-180", "75", "180"],
}

# ---------------------------------------------------------------------------
# Global aircraft fetcher — parallel multi-region (30+ points + military)
# ---------------------------------------------------------------------------

_USER_AGENT = "MPE-C2/1.0"


def _fetch_url(url: str) -> list[dict]:
    """Fetch a single airplanes.live endpoint, return list of aircraft dicts."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return data.get("ac", [])
    except (URLError, json.JSONDecodeError, OSError):
        return []


def _fetch_global_aircraft() -> list[dict]:
    """Fetch from 30+ airplanes.live endpoints in parallel.

    Builds URLs for each of the global fetch points plus the military
    endpoint, fires them all concurrently via ThreadPoolExecutor, and
    deduplicates by ICAO hex address.
    """
    now = time.monotonic()
    cached = _cache.get("aircraft_raw")
    cached_ts = _cache.get("aircraft_ts", 0.0)

    if cached is not None and (now - cached_ts) < CACHE_TTL:
        return cached

    urls: list[str] = []
    for lat, lon, radius in GLOBAL_FETCH_POINTS:
        urls.append(
            f"https://api.airplanes.live/v2/point/{lat}/{lon}/{radius}"
        )
    # Military aircraft globally
    urls.append("https://api.airplanes.live/v2/mil")

    all_aircraft: dict[str, dict] = {}  # dedupe by hex

    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = {pool.submit(_fetch_url, url): url for url in urls}
        for future in as_completed(futures):
            try:
                aircraft_list = future.result()
            except Exception:
                continue
            for ac in aircraft_list:
                hex_code = ac.get("hex", "").strip()
                if hex_code:
                    all_aircraft[hex_code] = ac

    result = list(all_aircraft.values())
    _cache["aircraft_raw"] = result
    _cache["aircraft_ts"] = now
    return result


def _ingest_aircraft_to_tracker(aircraft_list: list[dict]) -> None:
    """Feed raw airplanes.live dicts into the AircraftTracker."""
    for ac in aircraft_list:
        hex_code = ac.get("hex", "").strip()
        if not hex_code:
            continue
        aircraft_tracker.update(
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


# ---------------------------------------------------------------------------
# Global vessel generation — 570+ realistic vessels along shipping lanes
# ---------------------------------------------------------------------------

# Seed for reproducible vessel fleet; positions drift each refresh
_rng = random.Random(42)

# Ship type codes: 30=fishing, 35=military, 60=passenger, 70=cargo,
# 79=cargo-no-further, 80=tanker, 89=tanker-no-further

_VESSEL_TEMPLATES: list[dict] = []

# ── Shipping lane definitions ──
SHIPPING_LANES: dict[str, dict] = {
    "strait_of_hormuz": {
        "path": [(26.5, 56.0), (26.0, 56.5), (25.5, 57.0), (25.0, 57.5)],
        "count": 40,
        "types": [80, 80, 80, 80, 70, 70, 89],
        "speed_range": (8, 16),
    },
    "strait_of_malacca": {
        "path": [(1.2, 103.5), (2.5, 101.5), (4.0, 99.5), (5.5, 98.0)],
        "count": 50,
        "types": [70, 70, 79, 80, 89, 60],
        "speed_range": (8, 18),
    },
    "suez_canal_approaches": {
        "path": [(30.5, 32.3), (30.0, 32.5), (29.5, 32.6), (28.0, 33.5)],
        "count": 30,
        "types": [70, 79, 80, 89],
        "speed_range": (5, 14),
    },
    "english_channel": {
        "path": [(50.8, -1.0), (50.5, 0.5), (51.0, 1.5), (51.3, 2.0)],
        "count": 35,
        "types": [60, 70, 79, 80, 30, 30],
        "speed_range": (5, 20),
    },
    "bab_el_mandeb": {
        "path": [(12.5, 43.5), (12.8, 44.0), (13.0, 44.5), (13.5, 45.0)],
        "count": 25,
        "types": [70, 80, 89],
        "speed_range": (8, 16),
    },
    "south_china_sea": {
        "path": [(10.0, 110.0), (14.0, 114.0), (18.0, 117.0), (22.0, 120.0)],
        "count": 45,
        "types": [70, 70, 79, 80, 30],
        "speed_range": (8, 18),
    },
    "taiwan_strait": {
        "path": [(24.0, 119.0), (24.5, 119.5), (25.0, 120.0), (25.5, 120.5)],
        "count": 25,
        "types": [70, 79, 35, 35],
        "speed_range": (8, 22),
    },
    "panama_canal_approaches": {
        "path": [(8.8, -79.8), (9.0, -79.5), (9.2, -79.3), (9.4, -79.0)],
        "count": 20,
        "types": [70, 79, 80],
        "speed_range": (5, 12),
    },
    "caribbean_sea": {
        "path": [(10.0, -65.0), (12.0, -70.0), (14.0, -75.0), (16.0, -80.0)],
        "count": 30,
        "types": [70, 80, 60, 30],
        "speed_range": (8, 18),
    },
    "north_sea": {
        "path": [(53.0, 2.0), (55.0, 4.0), (57.0, 5.0), (58.0, 6.0)],
        "count": 30,
        "types": [70, 80, 89, 30],
        "speed_range": (8, 16),
    },
    "baltic_sea": {
        "path": [(54.5, 13.0), (56.0, 16.0), (58.0, 20.0), (59.5, 24.0)],
        "count": 25,
        "types": [70, 80, 60, 35],
        "speed_range": (6, 16),
    },
    "mediterranean": {
        "path": [(36.0, -5.0), (36.5, 5.0), (37.0, 15.0), (35.0, 25.0)],
        "count": 40,
        "types": [60, 70, 79, 80, 30],
        "speed_range": (8, 20),
    },
    "cape_of_good_hope": {
        "path": [(-34.5, 18.0), (-34.0, 19.0), (-33.5, 20.0), (-33.0, 22.0)],
        "count": 15,
        "types": [70, 80, 89],
        "speed_range": (10, 18),
    },
    "east_coast_usa": {
        "path": [(25.0, -80.0), (30.0, -78.0), (35.0, -75.0), (40.0, -73.0)],
        "count": 25,
        "types": [70, 79, 80, 60],
        "speed_range": (8, 18),
    },
    "west_coast_usa": {
        "path": [(32.0, -117.5), (34.0, -118.5), (37.5, -122.5), (47.5, -122.5)],
        "count": 20,
        "types": [70, 79, 80],
        "speed_range": (8, 16),
    },
    "gulf_of_guinea": {
        "path": [(4.0, 2.0), (4.5, 4.0), (5.0, 6.0), (5.5, 8.0)],
        "count": 15,
        "types": [80, 89, 30],
        "speed_range": (6, 14),
    },
    "persian_gulf": {
        "path": [(29.0, 48.5), (28.0, 50.0), (27.0, 51.5), (26.0, 53.0)],
        "count": 35,
        "types": [80, 80, 89, 89, 70],
        "speed_range": (6, 14),
    },
    "indian_ocean_trade": {
        "path": [(-6.0, 39.0), (0.0, 50.0), (5.0, 60.0), (10.0, 72.0)],
        "count": 20,
        "types": [70, 80, 89],
        "speed_range": (10, 18),
    },
    "korea_strait": {
        "path": [(33.5, 128.0), (34.0, 129.0), (34.5, 130.0), (35.0, 131.0)],
        "count": 20,
        "types": [70, 79, 60, 35],
        "speed_range": (8, 18),
    },
    "red_sea": {
        "path": [(20.0, 38.5), (22.0, 37.0), (24.0, 36.5), (27.0, 35.0)],
        "count": 25,
        "types": [70, 80, 89],
        "speed_range": (8, 16),
    },
}

# ── Vessel name pools ──
_TANKER_NAMES = [
    "NORDIC SPIRIT", "PACIFIC VOYAGER", "GULF STAR", "BRITISH COURAGE",
    "STENA INTEGRITY", "TEEKAY ENDURANCE", "EURONAV RESOLVE",
    "FRONTLINE PHOENIX", "DHT AURORA", "SCORPIO MERIDIAN",
    "TRAFIGURA TITAN", "NORDIC NEPTUNE", "SUEZMAX TRITON",
    "AFRAMAX PIONEER", "HAFNIA GRACE", "BW ORINOCO", "TORM HELENE",
    "MINERVA CLARA", "THENAMARIS ZEUS", "NAVIOS POLLUX",
    "OKEANIS NISSOS", "PYXIS EPSILON", "MARAN SELENE",
    "DELTA TANKERS ALPHA", "DORIAN LPG COMET",
]
_CARGO_NAMES = [
    "MAERSK SEVILLE", "MSC FLORENCE", "CMA CGM LIBERTY",
    "EVERGREEN CHAMPION", "COSCO GALAXY", "HAPAG LLOYD EXPRESS",
    "ONE HARMONY", "YANG MING VENTURE", "ZIM EAGLE",
    "HYUNDAI DISCOVERY", "PIL ENTERPRISE", "OOCL PROGRESS",
    "SITC ADVANCE", "PACIFIC TRADER", "ATLANTIC SOVEREIGN",
    "GLOBAL NAVIGATOR", "ORIENT PIONEER", "BALTIC FORTUNE",
    "JADE SPIRIT", "RUBY STAR", "PEARL GLORY", "AMBER WAVE",
    "HORIZON EXPRESS", "CORAL PRIDE", "AEGEAN HARMONY",
    "MAERSK EINDHOVEN", "MSC GULSUN", "CMA CGM PALAIS ROYAL",
    "EVER ACE", "COSCO UNIVERSE", "HMM ALGECIRAS",
]
_PASSENGER_NAMES = [
    "CALAIS EXPRESS", "DOVER SPIRIT", "CHANNEL QUEEN", "BALTIC FERRY",
    "ISLAND PRINCESS", "SEA BREEZE", "HARBOR STAR", "COAST RUNNER",
    "FJORD KING", "CORINTH LADY", "STOCKHOLM FERRY", "HELSINKI LINER",
    "TALLINN EXPRESS", "RIGA STAR", "MANILA BAY", "CEBU QUEEN",
    "SPIRIT OF BRITAIN", "PRIDE OF KENT", "NORMANDIE EXPRESS",
    "STENA BRITANNICA",
]
_FISHING_NAMES = [
    "TRAWLER", "FISHER", "CATCH", "NETMAN", "SEAHAWK", "PELICAN",
    "MARLIN", "SWORDFISH", "BARRACUDA", "SKIPJACK", "ALBACORE",
    "BONITO", "WAHOO", "TARPON", "GROUPER",
]
_FISHING_PREFIXES = [
    "NORTH SEA", "BALTIC", "CHANNEL", "BISCAY", "AEGEAN", "ADRIATIC",
    "MEKONG", "MANILA", "TOKYO", "SYDNEY", "SCOTIA", "IRISH",
]

# MMSI country prefixes
_COUNTRY_PREFIXES = [
    211, 219, 224, 227, 228, 230, 235, 236, 240, 241,
    244, 245, 246, 247, 249, 255, 256, 259, 261, 263,
    265, 269, 271, 273, 275, 276, 277, 304, 305, 308,
    309, 311, 316, 319, 338, 341, 351, 352, 353, 354,
    355, 356, 357, 366, 367, 368, 369, 370, 371, 372,
    373, 374, 375, 376, 377, 412, 413, 414, 416, 417,
    419, 431, 432, 436, 437, 438, 440, 441, 443, 445,
    447, 450, 451, 453, 455, 456, 457, 459, 461, 462,
    463, 466, 467, 468, 470, 471, 472, 473, 475, 477,
    478, 501, 503, 506, 508, 510, 511, 512, 514, 515,
    516, 518, 520, 521, 522, 523, 525, 529, 531, 533,
    536, 538, 540, 541, 542, 543, 544, 545, 546, 548,
    553, 555, 557, 559, 561, 563, 564, 565, 566, 567,
    570, 572, 574, 576, 577, 578, 601, 603, 605, 607,
    608, 609, 610, 611, 612, 613, 616, 617, 618, 619,
    620, 621, 622, 624, 625, 626, 627,
]

# Destinations by vessel type
_CARGO_DESTINATIONS = [
    "ROTTERDAM", "SHANGHAI", "SINGAPORE", "HAMBURG", "ANTWERP",
    "LOS ANGELES", "BUSAN", "HONG KONG", "DUBAI", "FELIXSTOWE",
    "VALENCIA", "PIRAEUS", "TOKYO", "KAOHSIUNG", "COLOMBO", "MUMBAI",
    "LONG BEACH", "SAVANNAH", "CHARLESTON", "JEBEL ALI",
]
_TANKER_DESTINATIONS = [
    "RAS TANURA", "FUJAIRAH", "ROTTERDAM", "HOUSTON", "SINGAPORE",
    "ULSAN", "JEBEL ALI", "YANBU", "MILFORD HAVEN", "WILHELMSHAVEN",
    "CORPUS CHRISTI", "LOUISIANA", "BONNY", "BASRAH",
]
_PASSENGER_DESTINATIONS = [
    "CALAIS", "DOVER", "HELSINKI", "TALLINN", "STOCKHOLM", "PIRAEUS",
    "NAPLES", "LIVORNO", "BARCELONA", "GENOA",
]

# ── Military vessel locations (strategic naval bases) ──
_MILITARY_BASES: list[tuple[float, float, float, float]] = [
    (50.8, -1.1, 190, 18.0),     # Solent / Portsmouth
    (36.8, -76.0, 150, 22.0),    # Norfolk VA
    (32.7, -117.2, 240, 20.0),   # San Diego
    (1.3, 103.9, 90, 15.0),      # Singapore Strait
    (35.3, 139.7, 180, 16.0),    # Yokosuka Japan
    (21.3, -157.9, 270, 12.0),   # Pearl Harbor
    (59.5, 24.5, 200, 14.0),     # Baltic (near Tallinn)
    (10.3, -75.5, 340, 19.0),    # Caribbean / Colombia
    (26.2, 56.3, 120, 17.0),     # Strait of Hormuz
    (33.3, 132.5, 90, 21.0),     # Pacific / Japan
    (38.0, -75.5, 170, 18.0),    # Norfolk anchorage
    (22.3, 114.2, 210, 14.0),    # Hong Kong approaches
    (25.0, 55.1, 140, 16.0),     # Jebel Ali naval
    (-33.9, 18.4, 260, 13.0),    # Simon's Town SA
    (28.3, 129.5, 100, 20.0),    # Okinawa
]


def _interpolate_path(
    path: list[tuple[float, float]],
    t: float,
) -> tuple[float, float]:
    """Interpolate a position along a polyline path at parameter t in [0, 1]."""
    n = len(path) - 1
    idx = min(int(t * n), n - 1)
    local_t = (t * n) - idx
    lat = path[idx][0] + local_t * (path[idx + 1][0] - path[idx][0])
    lon = path[idx][1] + local_t * (path[idx + 1][1] - path[idx][1])
    return (lat, lon)


def _path_bearing(
    path: list[tuple[float, float]],
    t: float,
) -> float:
    """Approximate bearing along a path at parameter t."""
    n = len(path) - 1
    idx = min(int(t * n), n - 1)
    dlat = path[idx + 1][0] - path[idx][0]
    dlon = path[idx + 1][1] - path[idx][1]
    return math.degrees(math.atan2(dlon, dlat)) % 360


def _generate_global_vessels() -> list[dict]:
    """Generate 570+ realistic vessel positions along major shipping lanes.

    Called once to build templates, then positions drift each call.
    """
    if _VESSEL_TEMPLATES:
        # Drift existing positions
        for v in _VESSEL_TEMPLATES:
            speed_deg_per_sec = (v["sog"] * 1.852 / 3600) / 111.0
            drift = speed_deg_per_sec * 10  # ~10 seconds of movement
            rad = math.radians(v["cog"])
            v["lat"] += drift * math.cos(rad) + _rng.gauss(0, 0.001)
            v["lon"] += drift * math.sin(rad) + _rng.gauss(0, 0.001)
            v["lat"] = max(-85, min(85, v["lat"]))
        return _VESSEL_TEMPLATES

    vessel_id = 0

    def _make_name(ship_type: int) -> tuple[str, str]:
        """Return (vessel_name, destination) for a given ship type."""
        if ship_type in (80, 81, 82, 83, 84, 89):
            return (
                _rng.choice(_TANKER_NAMES),
                _rng.choice(_TANKER_DESTINATIONS),
            )
        if ship_type in (70, 71, 72, 73, 74, 79):
            return (
                _rng.choice(_CARGO_NAMES),
                _rng.choice(_CARGO_DESTINATIONS),
            )
        if ship_type in (60, 61, 62, 69):
            return (
                _rng.choice(_PASSENGER_NAMES),
                _rng.choice(_PASSENGER_DESTINATIONS),
            )
        if ship_type == 30:
            return (
                f"{_rng.choice(_FISHING_PREFIXES)} {_rng.choice(_FISHING_NAMES)}",
                "",
            )
        if ship_type == 35:
            return ("", "")
        return ("UNKNOWN VESSEL", "")

    # --- Generate vessels for each shipping lane ---
    for lane_name, lane in SHIPPING_LANES.items():
        path = lane["path"]
        count = lane["count"]
        types = lane["types"]
        speed_lo, speed_hi = lane["speed_range"]

        for i in range(count):
            vessel_id += 1
            t = _rng.random()
            base_lat, base_lon = _interpolate_path(path, t)
            # Random lateral offset (simulate lane width)
            lat = base_lat + _rng.gauss(0, 0.15)
            lon = base_lon + _rng.gauss(0, 0.15)
            bearing = _path_bearing(path, t)
            cog = (bearing + _rng.gauss(0, 15)) % 360
            sog = _rng.uniform(speed_lo, speed_hi)
            ship_type = _rng.choice(types)
            name, dest = _make_name(ship_type)
            prefix = _rng.choice(_COUNTRY_PREFIXES)
            mmsi = prefix * 1000000 + 100000 + vessel_id

            _VESSEL_TEMPLATES.append({
                "mmsi": mmsi,
                "lat": lat,
                "lon": lon,
                "cog": round(cog, 1),
                "sog": round(sog, 1),
                "name": name,
                "type": ship_type,
                "dest": dest,
            })

    # --- Military vessels at strategic naval bases ---
    for mlat, mlon, mcog, msog in _MILITARY_BASES:
        vessel_id += 1
        _VESSEL_TEMPLATES.append({
            "mmsi": 273000000 + vessel_id,
            "lat": mlat + _rng.gauss(0, 0.01),
            "lon": mlon + _rng.gauss(0, 0.01),
            "cog": float(mcog),
            "sog": msog + _rng.gauss(0, 1.5),
            "name": "",
            "type": 35,
            "dest": "",
        })

    return _VESSEL_TEMPLATES


# ---------------------------------------------------------------------------
# Own-force drones (5 at global strategic locations)
# ---------------------------------------------------------------------------

OWN_DRONES: list[dict] = [
    {
        "id": "DRONE-ALPHA",
        "lat": 51.35,
        "lon": -0.27,
        "alt_m": 120,
        "speed_kts": 35,
        "heading": 90,
        "mission": "ISR patrol — English Channel",
    },
    {
        "id": "DRONE-BRAVO",
        "lat": 50.80,
        "lon": 0.10,
        "alt_m": 250,
        "speed_kts": 50,
        "heading": 210,
        "mission": "Maritime overwatch — Dover Strait",
    },
    {
        "id": "DRONE-CHARLIE",
        "lat": 10.40,
        "lon": -75.50,
        "alt_m": 300,
        "speed_kts": 45,
        "heading": 15,
        "mission": "Counter-narcotics surveillance — Caribbean",
    },
    {
        "id": "DRONE-DELTA",
        "lat": 1.30,
        "lon": 104.0,
        "alt_m": 180,
        "speed_kts": 40,
        "heading": 270,
        "mission": "Shipping lane monitoring — Strait of Malacca",
    },
    {
        "id": "DRONE-ECHO",
        "lat": 59.40,
        "lon": 24.80,
        "alt_m": 200,
        "speed_kts": 55,
        "heading": 45,
        "mission": "Baltic ISR — Estonia AOR",
    },
]


def _build_drone_features() -> list[dict]:
    """Build GeoJSON features for own-force drones."""
    features = []
    for d in OWN_DRONES:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [d["lon"], d["lat"]],
            },
            "properties": {
                "id": d["id"],
                "domain": "drone",
                "cot_type": "a-f-A-M-F-Q",  # friendly, air, UAV
                "callsign": d["id"],
                "altitude_m": d["alt_m"],
                "speed_kts": d["speed_kts"],
                "heading": d["heading"],
                "mission": d["mission"],
                "affiliation": "friendly",
                "threat_level": "none",
                "threat_category": "own_force",
                "anomalies": [],
                "reasoning": "Own-force drone asset",
            },
        })
    return features


# ---------------------------------------------------------------------------
# Helper: build aircraft features from tracker
# ---------------------------------------------------------------------------

def _build_aircraft_features(
    bbox: tuple[float, float, float, float] | None = None,
) -> list[dict]:
    """Build GeoJSON features from active aircraft tracks.

    Parameters
    ----------
    bbox:
        Optional (sw_lat, sw_lon, ne_lat, ne_lon) bounding box filter.
    """
    features = []
    for track in aircraft_tracker.active_tracks:
        if track.latitude == 0 and track.longitude == 0:
            continue

        if bbox is not None:
            sw_lat, sw_lon, ne_lat, ne_lon = bbox
            if not (sw_lat <= track.latitude <= ne_lat):
                continue
            # Handle longitude wrapping
            if sw_lon <= ne_lon:
                if not (sw_lon <= track.longitude <= ne_lon):
                    continue
            else:
                # Wraps around antimeridian
                if not (track.longitude >= sw_lon or track.longitude <= ne_lon):
                    continue

        cls = classifier.classify_aircraft(track)

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [track.longitude, track.latitude],
            },
            "properties": {
                "id": f"ADSB-{track.icao_hex}",
                "domain": "air",
                "cot_type": adsb_category_to_cot(track.category),
                "callsign": track.callsign or track.registration or track.icao_hex,
                "icao_hex": track.icao_hex,
                "aircraft_type": track.aircraft_type,
                "registration": track.registration,
                "altitude_ft": track.altitude_baro_ft,
                "altitude_m": track.altitude_m,
                "speed_kts": track.ground_speed_kts,
                "heading": track.heading,
                "vertical_rate_fpm": track.vertical_rate_fpm,
                "squawk": track.squawk,
                "on_ground": track.on_ground,
                "affiliation": cls.affiliation,
                "threat_level": cls.threat_level,
                "threat_category": cls.threat_category,
                "anomalies": [
                    {"type": a.anomaly_type, "desc": a.description}
                    for a in cls.anomalies
                ],
                "reasoning": cls.reasoning,
            },
        })

    return features


def _build_vessel_features(
    bbox: tuple[float, float, float, float] | None = None,
) -> list[dict]:
    """Build GeoJSON features from active vessel tracks.

    Parameters
    ----------
    bbox:
        Optional (sw_lat, sw_lon, ne_lat, ne_lon) bounding box filter.
    """
    features = []
    for track in vessel_tracker.active_tracks:
        if track.latitude == 0 and track.longitude == 0:
            continue

        if bbox is not None:
            sw_lat, sw_lon, ne_lat, ne_lon = bbox
            if not (sw_lat <= track.latitude <= ne_lat):
                continue
            if sw_lon <= ne_lon:
                if not (sw_lon <= track.longitude <= ne_lon):
                    continue
            else:
                if not (track.longitude >= sw_lon or track.longitude <= ne_lon):
                    continue

        cls = classifier.classify_vessel(track)

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [track.longitude, track.latitude],
            },
            "properties": {
                "id": f"AIS-{track.mmsi}",
                "domain": "sea",
                "cot_type": ais_type_to_cot(track.ship_type),
                "callsign": track.vessel_name or f"MMSI-{track.mmsi}",
                "mmsi": track.mmsi,
                "ship_type": track.ship_type,
                "destination": track.destination,
                "speed_kts": track.speed_over_ground,
                "heading": track.course_over_ground,
                "nav_status": track.nav_status,
                "affiliation": cls.affiliation,
                "threat_level": cls.threat_level,
                "threat_category": cls.threat_category,
                "anomalies": [
                    {"type": a.anomaly_type, "desc": a.description}
                    for a in cls.anomalies
                ],
                "reasoning": cls.reasoning,
            },
        })

    return features


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.get("/api/aircraft")
async def get_aircraft(
    lat: float = Query(51.3632),
    lon: float = Query(-0.2652),
    radius_nm: int = Query(250),
):
    """Fetch live aircraft globally and return as GeoJSON.

    Uses cached global data plus an optional targeted fetch for the
    requested region.
    """
    # Fetch global aircraft (cached, parallel)
    global_ac = _fetch_global_aircraft()
    _ingest_aircraft_to_tracker(global_ac)

    # Also do a targeted fetch for the specific requested region
    # (may already be covered by a global point, but ensures freshness)
    adsb_receiver._lat = lat
    adsb_receiver._lon = lon
    adsb_receiver._radius_nm = min(radius_nm, 250)
    try:
        adsb_receiver.fetch_once()
    except ADSBError:
        pass

    features = _build_aircraft_features()

    return {
        "type": "FeatureCollection",
        "features": features,
        "meta": {
            "count": len(features),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "airplanes.live",
            "regions_fetched": len(GLOBAL_FETCH_POINTS) + 1,
        },
    }


@app.get("/api/vessels")
async def get_vessels():
    """Return vessel tracks as GeoJSON — 570+ globally distributed vessels."""
    vessel_list = _generate_global_vessels()

    for v in vessel_list:
        vessel_tracker.update(
            mmsi=v["mmsi"],
            latitude=v["lat"],
            longitude=v["lon"],
            speed_over_ground=v["sog"],
            vessel_name=v["name"],
            ship_type=v["type"],
            destination=v["dest"],
        )

    features = _build_vessel_features()

    return {
        "type": "FeatureCollection",
        "features": features,
        "meta": {
            "count": len(features),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "simulated_ais",
        },
    }


@app.get("/api/tracks")
async def get_all_tracks(
    lat: float = Query(51.3632),
    lon: float = Query(-0.2652),
    radius_nm: int = Query(250),
    country: str | None = Query(None),
):
    """Combined endpoint -- all domains (aircraft, vessels, drones).

    When ``country`` is provided, filters results to that country's
    bounding box.
    """
    aircraft = await get_aircraft(lat=lat, lon=lon, radius_nm=radius_nm)
    vessels = await get_vessels()
    drone_features = _build_drone_features()

    combined = aircraft["features"] + vessels["features"] + drone_features

    # Filter by country bounding box if requested
    if country and country.lower() in COUNTRY_BOUNDS and country.lower() != "global":
        bounds = COUNTRY_BOUNDS[country.lower()]
        sw_lat, sw_lon = float(bounds[0]), float(bounds[1])
        ne_lat, ne_lon = float(bounds[2]), float(bounds[3])
        combined = [
            f for f in combined
            if _point_in_bbox(
                f["geometry"]["coordinates"][1],
                f["geometry"]["coordinates"][0],
                sw_lat, sw_lon, ne_lat, ne_lon,
            )
        ]

    threat_count = sum(
        1 for f in combined
        if isinstance(f["properties"].get("threat_level"), int) and f["properties"]["threat_level"] >= 4
    )

    return {
        "type": "FeatureCollection",
        "features": combined,
        "meta": {
            "aircraft": aircraft["meta"]["count"],
            "vessels": vessels["meta"]["count"],
            "drones": len(drone_features),
            "threats": threat_count,
            "total": len(combined),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def _point_in_bbox(
    lat: float, lon: float,
    sw_lat: float, sw_lon: float,
    ne_lat: float, ne_lon: float,
) -> bool:
    """Check if a point falls within a bounding box, handling antimeridian."""
    if not (sw_lat <= lat <= ne_lat):
        return False
    if sw_lon <= ne_lon:
        return sw_lon <= lon <= ne_lon
    # Wraps antimeridian
    return lon >= sw_lon or lon <= ne_lon


@app.get("/api/countries")
async def get_countries():
    """List available country focus regions with display names."""
    return {
        "countries": [
            {"code": code, "name": COUNTRY_NAMES.get(code, code)}
            for code in COUNTRY_BOUNDS
        ]
    }


@app.get("/api/country/{code}")
async def get_country_bounds(code: str):
    """Get bounding box for a country."""
    bounds = COUNTRY_BOUNDS.get(code.lower())
    if bounds is None:
        return {"error": f"Unknown country: {code}"}
    return {
        "code": code.lower(),
        "name": COUNTRY_NAMES.get(code.lower(), code),
        "bounds": [
            [float(bounds[1]), float(bounds[0])],
            [float(bounds[3]), float(bounds[2])],
        ],
    }


# Serve the frontend
DASHBOARD_DIR = Path(__file__).parent.parent.parent / "dashboard"


@app.get("/")
async def serve_dashboard():
    index = DASHBOARD_DIR / "index.html"
    if index.exists():
        return FileResponse(index, media_type="text/html")
    return HTMLResponse(
        "<h1>MPE C2 Dashboard</h1>"
        "<p>Dashboard not found. Place index.html in dashboard/</p>"
    )
