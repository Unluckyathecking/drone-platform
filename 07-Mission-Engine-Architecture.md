# Mission Planning Engine — Architecture

## Overview

The mission engine is the primary interface to the drone platform. It takes high-level **goals** as input and produces **MAVLink mission files** that ArduPilot executes autonomously.

```
OPERATOR → GOAL → CONSTRAINT ENGINE → ROUTE PLANNER → .waypoints FILE → ARDUPILOT
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GROUND STATION (Laptop/Tablet)                   │
│                                                                         │
│  ┌───────────────┐    ┌──────────────────────────────────────────────┐  │
│  │   OPERATOR UI  │    │           MISSION PLANNING ENGINE           │  │
│  │                │    │                                              │  │
│  │  Map Display   │    │  ┌─────────┐  ┌───────────┐  ┌──────────┐  │  │
│  │  Mission Viz   │───▶│  │  GOAL   │  │CONSTRAINT │  │  ROUTE   │  │  │
│  │  Telemetry     │    │  │ PARSER  │─▶│  ENGINE   │─▶│ PLANNER  │  │  │
│  │  Alerts        │    │  └─────────┘  └───────────┘  └────┬─────┘  │  │
│  │                │    │                                    │        │  │
│  │  Goal Entry    │    │                                    ▼        │  │
│  │  [structured   │    │                            ┌──────────────┐ │  │
│  │   form or NL]  │    │                            │  WAYPOINT    │ │  │
│  └───────────────┘    │                            │  GENERATOR   │ │  │
│                        │                            └──────┬───────┘ │  │
│  ┌───────────────┐    │                                    ▼        │  │
│  │  DATA SOURCES │    │                            ┌──────────────┐ │  │
│  │  Terrain/Elev │───▶│                            │  MAVLINK     │ │  │
│  │  Weather API  │    │                            │  COMPILER    │ │  │
│  │  Airspace DB  │    │                            └──────┬───────┘ │  │
│  │  No-Fly Zones │    └───────────────────────────────────┼────────┘  │
│  └───────────────┘                                        │           │
│                                                           ▼           │
│                                               ┌──────────────────┐   │
│                                               │  MISSION REVIEW  │   │
│                                               │  3D viz, battery │   │
│                                               │  est, risk score │   │
│                                               │  [APPROVE] [EDIT]│   │
│                                               └────────┬─────────┘   │
│                                                        │              │
└────────────────────────────────────────────────────────┼──────────────┘
                    TELEMETRY RADIO LINK (433MHz)        │
                    MAVLink v2                           │
─────────────────────────────────────────────────────────┼──────────────
                                                        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        DRONE (Airframe)                              │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │              PIXHAWK FLIGHT CONTROLLER (ArduPlane)            │  │
│  │  Navigation │ MAVLink Handler │ Mission Executor │ Failsafes  │  │
│  │  Sensors (GPS, IMU, Baro, Airspeed) │ Servo/PWM Output       │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────┐   ┌───────────────────────────────────┐  │
│  │  COMPANION COMPUTER   │   │  HOTSWAP PAYLOAD BAY             │  │
│  │  (RPi — in-flight     │   │  (Camera, Cargo, Sensors, etc.)  │  │
│  │   replan, video, AI)  │   │                                   │  │
│  └───────────────────────┘   └───────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Language | Python 3.11+ | pymavlink ecosystem, rapid prototyping |
| MAVLink | pymavlink | Direct protocol access |
| Geometry | shapely, numpy/scipy | Polygon ops, route optimization, TSP |
| Terrain | SRTM.py / rasterio | Free global 30m elevation data |
| Weather | OpenWeatherMap API | Wind/visibility/precipitation |
| Validation | pydantic | Data model enforcement |
| Ground station | Mission Planner / QGC | Upload & monitor (don't rebuild these) |
| Simulation | ArduPilot SITL | Full firmware on localhost:5760 |

## Mission Types

### 1. Point-to-Point Delivery
- **Input:** pickup GPS, dropoff GPS, payload weight, priority
- **Algorithm:** Great-circle route → no-fly avoidance → terrain check → range validation
- **Commands:** NAV_TAKEOFF → NAV_WAYPOINT (cruise) → NAV_LOITER_TURNS (confirm drop zone) → DO_SET_SERVO (release cargo) → NAV_RETURN_TO_LAUNCH

### 2. Area Search (SAR Grid)
- **Input:** search polygon vertices, sensor type, overlap %, altitude
- **Algorithm:** Bounding rect → swath width from sensor FOV → lawnmower tracks → optimize for wind
- **Commands:** NAV_WAYPOINT (turn points) → DO_SET_CAM_TRIGG_DIST (photo every Nm) → DO_DIGICAM_CONTROL

### 3. Route Surveillance / ISR
- **Input:** route polyline, offset distance, altitude, camera mode
- **Algorithm:** Buffer polyline by offset → resample at waypoint spacing → set ROI per segment
- **Commands:** NAV_SPLINE_WAYPOINT (smooth path) → DO_SET_ROI (camera lock on route)

### 4. Loiter/Orbit Observation
- **Input:** target GPS, orbit radius, direction, duration
- **Algorithm:** Transit to tangent entry → set orbit (min radius = V²/g·tan(bank))
- **Commands:** NAV_LOITER_TURNS or NAV_LOITER_TIME → DO_SET_ROI (lock on target)

### 5. Multi-Waypoint Delivery
- **Input:** list of drop points [{gps, kg}], order preference
- **Algorithm:** TSP optimization → weight decreases at each drop → recalculate range budget
- **Commands:** Sequential NAV_WAYPOINT + DO_SET_SERVO per drop → RTL

## Data Models

```python
@dataclass
class Goal:
    mission_type: MissionType     # DELIVERY | SAR_SEARCH | ISR_ROUTE | LOITER | MULTI_DELIVERY
    target_points: list[Coord]    # GPS coordinates
    search_area: Polygon | None   # For SAR
    route_path: LineString | None # For ISR
    payload: PayloadConfig        # Type, weight, servo channel
    altitude_agl: float           # Meters above ground
    priority: Priority            # ROUTINE | URGENT | EMERGENCY

@dataclass
class ConstraintSet:
    aircraft: AircraftProfile     # Range, speeds, turn radius, battery
    no_fly_zones: list[Polygon]
    terrain: TerrainModel
    weather: WeatherForecast
    min_battery_reserve: float    # e.g., 0.25 = 25%
    rally_points: list[Coord]
    home_position: Coord

@dataclass
class Mission:
    id: UUID
    goal: Goal
    waypoints: list[MissionItem]  # MAVLink mission items
    rally_points: list[RallyPoint]
    geofence: Polygon
    total_distance_km: float
    estimated_flight_time: timedelta
    estimated_battery_usage: float
    risk_score: float
    feasibility: FeasibilityResult
    status: MissionStatus         # DRAFT | VALIDATED | UPLOADED | ACTIVE | COMPLETED
```

## Output Format — QGC WPL 110

```
QGC WPL 110
0  1  0  16  0  0  0  0  51.3632620  -0.2652370  84.0  1
1  0  3  22  15  0  0  0  0  0  50.0  1
2  0  3  16  0  0  0  0  51.3612520  -0.2632370  100.0  1
3  0  3  183 0  0  0  0  0  0  0  1
4  0  3  20  0  0  0  0  0  0  0  1
```

Fields: seq, current, frame, command, p1-p4, lat, lon, alt, autocontinue

## Development Phases

| Phase | Deliverable | Duration |
|-------|-------------|----------|
| **A** | Basic waypoint generator → .waypoints → SITL test | Weeks 1-3 |
| **B** | Mission type templates (delivery, SAR, ISR, loiter, multi-drop) | Weeks 4-7 |
| **C** | Constraint engine (terrain, no-fly zones, battery model, weather) | Weeks 8-13 |
| **D** | Goal-to-mission intelligence (UI, NL parsing, in-flight replan) | Weeks 14-21 |

## ArduPilot Failsafe Configuration

| Parameter | Value | Action |
|-----------|-------|--------|
| FS_SHORT_ACTN | 0 | Circle on short comms loss |
| FS_LONG_ACTN | 1 | RTL on long comms loss |
| BATT_FS_LOW_ACT | 1 | RTL on battery low |
| BATT_FS_CRT_ACT | 3 | Land immediately on battery critical |
| FENCE_ENABLE | 1 | Geofence active |
| FENCE_ACTION | 1 | RTL on fence breach |

## Project Structure

```
mission-planning-engine/
├── src/mpe/
│   ├── models/          # goal.py, constraints.py, mission.py, geo.py
│   ├── planners/        # base.py, delivery.py, search.py, isr.py, loiter.py
│   ├── constraints/     # terrain.py, airspace.py, battery.py, weather.py, validator.py
│   ├── output/          # waypoints.py, mavlink_upload.py, rally.py
│   └── cli.py
├── tests/
│   ├── test_planners/
│   ├── test_constraints/
│   └── fixtures/        # Known-good .waypoints files
└── sitl/
    └── run_sitl_test.py # Automated SITL test harness
```

## Phase A First Task

Write a Python script that outputs a .waypoints file:
1. Takeoff to 50m
2. Fly to a point 500m away
3. Fly to a second point 500m further
4. RTL

Load into SITL (`sim_vehicle.py -v ArduPlane --map --console`). Watch it fly.
