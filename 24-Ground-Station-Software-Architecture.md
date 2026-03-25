# Ground Station Software Architecture

## Document Scope

Complete software architecture for the ground control system (GCS) serving the four-tier drone platform family (MICRO 500g, MINI 5-15kg, MEDIUM 25-50kg, LARGE 100-200kg). Scales from a single laptop in the field to a fully automated airbase control system.

```
  ARCHITECTURE TIERS — PROGRESSIVE CAPABILITY
  ═════════════════════════════════════════════

  TIER 1: FIELD STATION              TIER 2: OPERATIONS CENTER          TIER 3: AUTOMATED AIRBASE
  ┌──────────────────────┐           ┌──────────────────────┐           ┌──────────────────────┐
  │ Single laptop/tablet │           │ Multi-screen workstation│         │ Server rack + robotics│
  │ 1 operator           │           │ Multiple operators    │           │ Zero on-site operators│
  │ 1 drone              │           │ 10-50 drones          │           │ Mission queue 24/7   │
  │ Direct radio link    │           │ Mixed radio + internet│           │ Auto launch/recovery │
  │ Offline-capable      │           │ Central database      │           │ Remote monitoring    │
  │ Field-deployable     │           │ Role-based access     │           │ External integration │
  └──────────────────────┘           └──────────────────────┘           └──────────────────────┘
       ▲                                  ▲                                  ▲
       │                                  │                                  │
       │    Same core software stack      │     Adds fleet + scheduling      │  Adds robotics + autonomy
       └──────────────────────────────────┴──────────────────────────────────┘
```

---

## 1. System Architecture Overview

### 1.1 High-Level Component Diagram

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                        GROUND STATION SOFTWARE                              │
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐    │
  │  │                      PRESENTATION LAYER                             │    │
  │  │                                                                     │    │
  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │    │
  │  │  │ Mission   │  │ Flight   │  │ Fleet    │  │ Airbase Control   │  │    │
  │  │  │ Planner   │  │ Monitor  │  │ Dashboard│  │ Panel             │  │    │
  │  │  │ Screen    │  │ Screen   │  │ Screen   │  │                   │  │    │
  │  │  │ (T1/T2/T3)│  │(T1/T2/T3)│  │ (T2/T3) │  │ (T3 only)        │  │    │
  │  │  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘  │    │
  │  │                                                                     │    │
  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │    │
  │  │  │ Video    │  │ Log      │  │ Maint.   │  │ Airspace          │  │    │
  │  │  │ Viewer   │  │ Analyzer │  │ Tracker  │  │ Manager           │  │    │
  │  │  │ (T1/T2)  │  │ (T1/T2) │  │ (T2/T3)  │  │ (T2/T3)          │  │    │
  │  │  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘  │    │
  │  └─────────────────────────────────────────────────────────────────────┘    │
  │                                    │                                        │
  │                            WebSocket / REST                                 │
  │                                    │                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐    │
  │  │                      APPLICATION LAYER (FastAPI)                     │    │
  │  │                                                                     │    │
  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
  │  │  │ Mission      │  │ Telemetry    │  │ Fleet Management         │  │    │
  │  │  │ Service      │  │ Service      │  │ Service                  │  │    │
  │  │  │              │  │              │  │                          │  │    │
  │  │  │ Plan/Upload  │  │ Decode/Store │  │ Status/Schedule/         │  │    │
  │  │  │ Validate     │  │ Broadcast    │  │ Deconflict               │  │    │
  │  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
  │  │                                                                     │    │
  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
  │  │  │ Payload      │  │ Airspace     │  │ Airbase Automation       │  │    │
  │  │  │ Service      │  │ Service      │  │ Service                  │  │    │
  │  │  │              │  │              │  │                          │  │    │
  │  │  │ Gimbal/Cargo │  │ Geofence/NFZ │  │ Launch/Recovery/Charge   │  │    │
  │  │  │ Camera/Sensor│  │ Weather/ATC  │  │ Health/Queue             │  │    │
  │  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
  │  └─────────────────────────────────────────────────────────────────────┘    │
  │                                    │                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐    │
  │  │                      INTEGRATION LAYER                              │    │
  │  │                                                                     │    │
  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
  │  │  │ MAVLink      │  │ Mission      │  │ External APIs            │  │    │
  │  │  │ Router       │  │ Planning     │  │                          │  │    │
  │  │  │              │  │ Engine (MPE) │  │ Weather / ATC / Customer │  │    │
  │  │  │ pymavlink    │  │ (existing)   │  │ orders / NOTAM           │  │    │
  │  │  │ multi-vehicle│  │ goal→wpts    │  │                          │  │    │
  │  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
  │  │                                                                     │    │
  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
  │  │  │ Video        │  │ Database     │  │ Hardware Abstraction     │  │    │
  │  │  │ Pipeline     │  │ Layer        │  │ Layer (HAL)              │  │    │
  │  │  │              │  │              │  │                          │  │    │
  │  │  │ GStreamer/   │  │ SQLAlchemy + │  │ Charger/Launcher/        │  │    │
  │  │  │ RTSP decode  │  │ migrations   │  │ Recovery hardware        │  │    │
  │  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
  │  └─────────────────────────────────────────────────────────────────────┘    │
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐    │
  │  │                      DATA LAYER                                     │    │
  │  │                                                                     │    │
  │  │  ┌───────────────────────┐  ┌───────────────────────────────────┐  │    │
  │  │  │ PostgreSQL            │  │ Redis                             │  │    │
  │  │  │ (or SQLite for T1)    │  │ (or in-process for T1)           │  │    │
  │  │  │                       │  │                                   │  │    │
  │  │  │ Drones, Missions,     │  │ Live telemetry cache,            │  │    │
  │  │  │ Flights, Logs,        │  │ WebSocket pub/sub,               │  │    │
  │  │  │ Maintenance, Ops      │  │ Session state                    │  │    │
  │  │  └───────────────────────┘  └───────────────────────────────────┘  │    │
  │  └─────────────────────────────────────────────────────────────────────┘    │
  └─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Tier-Specific Deployment Model

```
  TIER 1: FIELD STATION
  ═════════════════════
  ┌─────────────────────────────────┐
  │  Electron Desktop App           │
  │  (or PWA on tablet)             │
  │                                 │
  │  Frontend: Svelte + MapLibre    │
  │  Backend:  FastAPI (embedded)   │
  │  Database: SQLite (local file)  │
  │  Cache:    In-process dict      │
  │  Radio:    Direct USB serial    │
  │            to SiK/RFD900x       │
  │                                 │
  │  Single process, offline-ready  │
  │  ~200MB RAM, runs on any laptop │
  └────────────────┬────────────────┘
                   │ USB serial / UDP
                   ▼
              ┌─────────┐
              │  DRONE  │
              └─────────┘

  TIER 2: OPERATIONS CENTER
  ═════════════════════════
  ┌──────────────────────────────────────────────┐
  │  Web Application (browser-based)              │
  │                                               │
  │  Frontend: Svelte + MapLibre + Cesium (3D)    │
  │  Backend:  FastAPI (server, multi-worker)      │
  │  Database: PostgreSQL                          │
  │  Cache:    Redis                               │
  │  Queue:    Redis / Celery (background tasks)   │
  │  Auth:     JWT + RBAC                          │
  │                                               │
  │  Multi-screen layout, multiple concurrent ops  │
  └──────────────────────┬───────────────────────┘
                         │ WebSocket / REST
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌───────────┐ ┌───────┐ ┌─────────────┐
      │ MAVProxy  │ │ Video │ │ Internet    │
      │ Router    │ │ Relay │ │ relay to    │
      │ (multi-   │ │ Server│ │ remote      │
      │  vehicle) │ │       │ │ drones      │
      └─────┬─────┘ └───┬───┘ └──────┬──────┘
            │           │            │
     ┌──────┼───────────┼────────────┼──────┐
     ▼      ▼           ▼            ▼      ▼
   drone1  drone2    drone3      drone4  drone5

  TIER 3: AUTOMATED AIRBASE
  ═════════════════════════
  ┌───────────────────────────────────────────────────┐
  │  Server Cluster (3-node minimum for redundancy)    │
  │                                                    │
  │  Frontend: Web dashboard (remote operators)         │
  │  Backend:  FastAPI + Celery + Event-driven arch     │
  │  Database: PostgreSQL (primary-replica)              │
  │  Cache:    Redis Sentinel (HA)                      │
  │  Queue:    RabbitMQ or Redis Streams                │
  │  Monitoring: Prometheus + Grafana                   │
  │                                                    │
  │  ┌──────────────┐  ┌──────────────┐                │
  │  │ Airbase      │  │ Health       │                │
  │  │ Controller   │  │ Monitor      │                │
  │  │ State Machine│  │ (continuous) │                │
  │  └──────┬───────┘  └──────┬───────┘                │
  │         │                 │                        │
  │  ┌──────┼─────────────────┼──────────────────┐     │
  │  │      ▼                 ▼                  │     │
  │  │  ┌────────┐  ┌────────┐  ┌────────────┐  │     │
  │  │  │Launcher│  │Charger │  │Recovery    │  │     │
  │  │  │ HAL    │  │ HAL    │  │System HAL  │  │     │
  │  │  └────────┘  └────────┘  └────────────┘  │     │
  │  │           HARDWARE LAYER                  │     │
  │  └───────────────────────────────────────────┘     │
  │                                                    │
  │  External Integrations: ATC, Weather, Customers     │
  └────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### 2.1 Complete Stack Selection

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Frontend Framework** | Svelte 5 + SvelteKit | Smallest bundle size (critical for Electron), fast reactivity, excellent DX. Lighter than React for a resource-constrained field laptop. |
| **Map — 2D** | MapLibre GL JS | Open-source fork of Mapbox GL. Vector tiles, WebGL-accelerated. Offline tile support via MBTiles. |
| **Map — 3D** | CesiumJS (Tier 2/3 only) | Full 3D globe with terrain. Required for 3D mission visualization, airspace volumes, multi-altitude deconfliction. |
| **Charts / Gauges** | D3.js + custom SVG components | Instrument-style gauges for attitude, altitude, airspeed. D3 gives full control over flight instrument rendering. |
| **Backend** | Python 3.12 + FastAPI | Integrates directly with existing mission planning engine (same Python process). AsyncIO for concurrent MAVLink + WebSocket handling. |
| **Real-time Comms** | WebSocket (native FastAPI) | Bidirectional telemetry streaming at 10-50 Hz. JSON for control messages, MessagePack for high-rate telemetry. |
| **MAVLink** | pymavlink + MAVProxy | pymavlink for protocol handling. MAVProxy as multi-vehicle router (Tier 2/3). |
| **Video** | GStreamer + WebRTC | GStreamer decodes H.264/H.265 from RTSP camera streams. WebRTC delivers to browser with sub-200ms latency. |
| **Database — T1** | SQLite (via SQLAlchemy) | Zero-config, single-file, offline. Perfect for field laptop. |
| **Database — T2/T3** | PostgreSQL 16 | Multi-user, ACID, PostGIS for spatial queries (geofence, NFZ intersections). |
| **Cache / Pub-Sub** | Redis 7 (T2/T3), in-process dict (T1) | Live telemetry cache, WebSocket fan-out, session state. |
| **Task Queue** | Celery + Redis (T2/T3) | Background: log processing, report generation, weather polling, maintenance scheduling. |
| **ORM / Migrations** | SQLAlchemy 2.0 + Alembic | Async support, same models for SQLite and PostgreSQL. Alembic manages schema migrations. |
| **Auth** | JWT + RBAC (T2/T3) | Stateless tokens, role-based permissions. T1 is single-user, no auth needed. |
| **Desktop Packaging** | Electron (T1) | Packages Svelte frontend + FastAPI backend as a single installable app. Backend runs as a child process. |
| **Tablet** | PWA (Progressive Web App) | Same Svelte frontend, installable on iPad/Android. Connects to FastAPI over local WiFi. |
| **Ops Center** | Standard web deployment | Nginx reverse proxy, FastAPI behind Uvicorn workers. |
| **Containerization** | Docker + Docker Compose (T2/T3) | Reproducible deployment. Each service in its own container. |
| **Monitoring** | Prometheus + Grafana (T3) | System health, latency, throughput metrics. Alert on anomalies. |

### 2.2 Directory Structure

```
  ground-station/
  ├── frontend/                    # Svelte 5 + SvelteKit
  │   ├── src/
  │   │   ├── lib/
  │   │   │   ├── components/
  │   │   │   │   ├── map/         # MapLibre / Cesium components
  │   │   │   │   │   ├── DroneMap.svelte
  │   │   │   │   │   ├── WaypointLayer.svelte
  │   │   │   │   │   ├── GeofenceLayer.svelte
  │   │   │   │   │   ├── DroneMarker.svelte
  │   │   │   │   │   └── AirspaceOverlay.svelte
  │   │   │   │   ├── instruments/  # Flight instruments
  │   │   │   │   │   ├── AttitudeIndicator.svelte
  │   │   │   │   │   ├── AltitudeGauge.svelte
  │   │   │   │   │   ├── AirspeedGauge.svelte
  │   │   │   │   │   ├── BatteryGauge.svelte
  │   │   │   │   │   ├── GPSStatus.svelte
  │   │   │   │   │   └── CompassHeading.svelte
  │   │   │   │   ├── mission/      # Mission planning widgets
  │   │   │   │   │   ├── GoalForm.svelte
  │   │   │   │   │   ├── WaypointEditor.svelte
  │   │   │   │   │   ├── MissionTimeline.svelte
  │   │   │   │   │   ├── ChecklistPanel.svelte
  │   │   │   │   │   └── MissionReview.svelte
  │   │   │   │   ├── fleet/        # Fleet management (T2/T3)
  │   │   │   │   │   ├── FleetGrid.svelte
  │   │   │   │   │   ├── DroneCard.svelte
  │   │   │   │   │   ├── ScheduleTimeline.svelte
  │   │   │   │   │   └── MaintenanceLog.svelte
  │   │   │   │   ├── airbase/      # Airbase automation (T3)
  │   │   │   │   │   ├── LaunchPadStatus.svelte
  │   │   │   │   │   ├── ChargingBayStatus.svelte
  │   │   │   │   │   ├── MissionQueue.svelte
  │   │   │   │   │   └── StateMachineViz.svelte
  │   │   │   │   └── video/        # Video display
  │   │   │   │       ├── VideoFeed.svelte
  │   │   │   │       ├── VideoControls.svelte
  │   │   │   │       └── RecordingIndicator.svelte
  │   │   │   ├── stores/           # Svelte stores (reactive state)
  │   │   │   │   ├── telemetry.ts
  │   │   │   │   ├── mission.ts
  │   │   │   │   ├── fleet.ts
  │   │   │   │   └── settings.ts
  │   │   │   └── services/         # API / WebSocket clients
  │   │   │       ├── websocket.ts
  │   │   │       ├── api.ts
  │   │   │       └── video.ts
  │   │   └── routes/               # SvelteKit pages
  │   │       ├── +layout.svelte
  │   │       ├── mission/+page.svelte
  │   │       ├── monitor/+page.svelte
  │   │       ├── fleet/+page.svelte
  │   │       ├── airbase/+page.svelte
  │   │       ├── logs/+page.svelte
  │   │       └── settings/+page.svelte
  │   └── package.json
  │
  ├── backend/                     # Python FastAPI
  │   ├── app/
  │   │   ├── main.py              # FastAPI app factory
  │   │   ├── config.py            # Tier-aware configuration
  │   │   ├── api/
  │   │   │   ├── routes/
  │   │   │   │   ├── missions.py
  │   │   │   │   ├── telemetry.py
  │   │   │   │   ├── fleet.py
  │   │   │   │   ├── payloads.py
  │   │   │   │   ├── airspace.py
  │   │   │   │   ├── maintenance.py
  │   │   │   │   ├── airbase.py
  │   │   │   │   └── auth.py
  │   │   │   └── websocket/
  │   │   │       ├── telemetry_ws.py
  │   │   │       ├── video_ws.py
  │   │   │       └── fleet_ws.py
  │   │   ├── services/
  │   │   │   ├── mission_service.py
  │   │   │   ├── telemetry_service.py
  │   │   │   ├── fleet_service.py
  │   │   │   ├── payload_service.py
  │   │   │   ├── airspace_service.py
  │   │   │   ├── weather_service.py
  │   │   │   ├── maintenance_service.py
  │   │   │   ├── airbase_service.py
  │   │   │   └── auth_service.py
  │   │   ├── mavlink/
  │   │   │   ├── router.py        # MAVLink message router
  │   │   │   ├── connection.py    # Connection management
  │   │   │   ├── telemetry.py     # Message decode + publish
  │   │   │   ├── commands.py      # Command sending
  │   │   │   └── vehicle.py       # Per-vehicle state tracker
  │   │   ├── models/              # SQLAlchemy ORM models
  │   │   │   ├── drone.py
  │   │   │   ├── mission.py
  │   │   │   ├── flight.py
  │   │   │   ├── telemetry_log.py
  │   │   │   ├── maintenance.py
  │   │   │   ├── operator.py
  │   │   │   ├── payload.py
  │   │   │   └── airbase.py
  │   │   ├── hardware/            # T3 hardware abstraction
  │   │   │   ├── launcher.py
  │   │   │   ├── charger.py
  │   │   │   ├── recovery.py
  │   │   │   └── weather_station.py
  │   │   └── video/
  │   │       ├── pipeline.py      # GStreamer pipeline management
  │   │       └── recorder.py      # Video recording to disk
  │   ├── migrations/              # Alembic migrations
  │   ├── tests/
  │   └── pyproject.toml
  │
  ├── mission-planning-engine/     # EXISTING — symlink or submodule
  │   └── src/mpe/                 # Imported as Python package
  │
  ├── electron/                    # T1 desktop packaging
  │   ├── main.js                  # Electron main process
  │   ├── preload.js
  │   └── package.json
  │
  ├── docker/                      # T2/T3 deployment
  │   ├── docker-compose.yml
  │   ├── docker-compose.t3.yml    # Adds airbase services
  │   ├── Dockerfile.backend
  │   ├── Dockerfile.frontend
  │   └── nginx.conf
  │
  └── docs/
      ├── api.md
      └── deployment.md
```

---

## 3. UI/UX Design

### 3.1 Mission Planning Screen (Tier 1/2/3)

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  [Mission Plan]  [Monitor]  [Fleet]  [Airbase]  [Logs]  [Settings]    ● ONLINE  │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                  │
  │  ┌─── MISSION SETUP ──────────┐  ┌──────────────────────────────────────────┐   │
  │  │                            │  │                                          │   │
  │  │  Mission Type:             │  │              MAP VIEW                    │   │
  │  │  [Delivery ▼]              │  │                                          │   │
  │  │                            │  │         ╱ geofence boundary              │   │
  │  │  Drone:                    │  │       ╱                                  │   │
  │  │  [MINI-003 "Kestrel" ▼]   │  │     ╱    ① ─── ② ─── ③                 │   │
  │  │                            │  │   ╱     ╱              │                 │   │
  │  │  Payload:                  │  │  │    H (home)         │                 │   │
  │  │  [Cargo Pod 1kg ▼]        │  │   ╲                    ④                 │   │
  │  │                            │  │     ╲                ╱                   │   │
  │  │  ─────────────────────     │  │       ╲           ╱                     │   │
  │  │                            │  │         ╲───────╱                       │   │
  │  │  Goal Parameters:          │  │                                          │   │
  │  │  Pickup:  51.3632, -0.265  │  │     ▓▓▓ No-Fly Zone (Heathrow CTR)     │   │
  │  │  Dropoff: 51.3720, -0.250  │  │                                          │   │
  │  │  Altitude: [80m AGL    ]   │  │  ┌─────────────────────────────────┐    │   │
  │  │  Speed:    [18 m/s     ]   │  │  │ Terrain profile: home → WP3    │    │   │
  │  │                            │  │  │  120m ┤                         │    │   │
  │  │  ─────────────────────     │  │  │   80m ┤ ═══════════════════     │    │   │
  │  │                            │  │  │   40m ┤▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │    │   │
  │  │  MISSION SUMMARY           │  │  │    0m ┤____ground_profile___    │    │   │
  │  │  Distance:   4.2 km        │  │  │       └──────────────────────   │    │   │
  │  │  Est. Time:  8 min         │  │  └─────────────────────────────────┘    │   │
  │  │  Battery:    ~35%          │  │                                          │   │
  │  │  Risk Score: LOW (0.12)    │  │  Tools: [+WP] [Geofence] [NFZ] [Ruler] │   │
  │  │                            │  │  Layers: [☑ Terrain] [☑ Airspace] [Wind]│   │
  │  │  [VALIDATE] [PLAN ROUTE]   │  │                                          │   │
  │  │  [UPLOAD TO DRONE]         │  └──────────────────────────────────────────┘   │
  │  └────────────────────────────┘                                                  │
  │                                                                                  │
  │  ┌──── PRE-FLIGHT CHECKLIST ────────────────────────────────────────────────┐   │
  │  │  [✓] GPS lock (12 sats, HDOP 0.8)    [✓] Battery 98% (14.7V)            │   │
  │  │  [✓] Airspeed sensor calibrated       [✓] Payload locked (CG check OK)  │   │
  │  │  [✓] Geofence uploaded                [✓] Rally points set (2)           │   │
  │  │  [✓] Weather: wind 4m/s SW, vis 10km  [ ] Airspace clear (check NOTAM)  │   │
  │  │  [✓] Failsafes configured             [ ] Operator confirmation          │   │
  │  │                                                                          │   │
  │  │  Status: 8/10 checks passed — AWAITING OPERATOR CONFIRMATION             │   │
  │  │                                                  [■ ARM & LAUNCH]        │   │
  │  └──────────────────────────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Flight Monitoring Screen (Primary Flight Display)

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  [Mission Plan]  [Monitor]  [Fleet]  [Airbase]  [Logs]  [Settings]   ● FLYING   │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                  │
  │  ┌─── INSTRUMENTS ─────────┐  ┌────────── MAP + TRACK ─────────────────────┐   │
  │  │                          │  │                                            │   │
  │  │     ATTITUDE             │  │       geofence                             │   │
  │  │   ┌──────────────┐      │  │      ╱        ╲                            │   │
  │  │   │     ──────── │      │  │    ╱    ①──②──③  ╲                         │   │
  │  │   │   ╱ sky  ╱   │      │  │  ╱    ╱    ✈→     ╲                        │   │
  │  │   │──────────────│      │  │ │   H           ④   │                      │   │
  │  │   │  ╲ground╲    │      │  │  ╲              ╱   ╱                      │   │
  │  │   │    ──────── │      │  │    ╲          ╱  ╱                          │   │
  │  │   └──────────────┘      │  │      ╲──────╱                              │   │
  │  │   Roll: -3°  Pitch: 5°  │  │                                            │   │
  │  │                          │  │  ✈ MINI-003 "Kestrel"                     │   │
  │  │     ALTITUDE    SPEED    │  │  Heading: 047°  │  WP: 3/5                │   │
  │  │   ┌────────┐ ┌────────┐ │  │  Dist to WP: 1.2km │ ETA: 67s             │   │
  │  │   │   80   │ │   18   │ │  │                                            │   │
  │  │   │   ▊    │ │   ▊    │ │  │  ───── trail ───── (last 60s of track)    │   │
  │  │   │   m    │ │  m/s   │ │  │                                            │   │
  │  │   └────────┘ └────────┘ │  └────────────────────────────────────────────┘   │
  │  │                          │                                                   │
  │  │     BATTERY   GPS        │  ┌────────── VIDEO FEED ─────────────────────┐   │
  │  │   ┌────────┐ ┌────────┐ │  │                                            │   │
  │  │   │  72%   │ │ 14 sat │ │  │  ┌──────────────────────────────────────┐  │   │
  │  │   │ ████░░ │ │ 3D Fix │ │  │  │                                      │  │   │
  │  │   │ 14.2V  │ │HDOP0.7 │ │  │  │     EO camera feed (720p)           │  │   │
  │  │   └────────┘ └────────┘ │  │  │     or IR overlay                    │  │   │
  │  │                          │  │  │                                      │  │   │
  │  │  Mode: AUTO              │  │  │            [+] crosshair             │  │   │
  │  │  Armed: YES              │  │  │                                      │  │   │
  │  │  Failsafe: NONE         │  │  └──────────────────────────────────────┘  │   │
  │  │                          │  │  Gimbal: P-15° T0°  [Stow] [Track] [Scan]│   │
  │  │  ─── COMMANDS ────       │  │  Record: ● REC 00:04:23  [Snapshot]       │   │
  │  │  [RTL] [LOITER] [LAND]   │  └────────────────────────────────────────────┘   │
  │  │  [RESUME] [GUIDED]       │                                                   │
  │  └──────────────────────────┘                                                   │
  │                                                                                  │
  │  ┌──── TELEMETRY LOG ──────────────────────────────────────────────────────┐    │
  │  │  14:32:01  Reached WP 2, turning to WP 3 (heading 047°)                │    │
  │  │  14:31:45  Crosswind component 3.2 m/s — within limits                  │    │
  │  │  14:31:12  Battery 72% — 14.2V — estimated 18 min remaining             │    │
  │  │  14:30:55  Takeoff complete, transitioning to AUTO mode                  │    │
  │  │  14:30:30  Armed — launching                                             │    │
  │  └──────────────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Fleet Dashboard (Tier 2/3)

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  [Mission Plan]  [Monitor]  [Fleet]  [Airbase]  [Logs]  [Settings]   ● 47 ONLINE│
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                  │
  │  ┌──── FLEET STATUS GRID ──────────────────────────────────────────────────┐    │
  │  │                                                                          │    │
  │  │  MICRO (12 active)     MINI (8 active)      MEDIUM (3 active)           │    │
  │  │  ┌──┐┌──┐┌──┐┌──┐    ┌────────┐┌────────┐  ┌──────────┐               │    │
  │  │  │●1││●2││●3││●4│    │ ✈ M-03 ││ ✈ M-07 │  │ ✈ MD-01  │               │    │
  │  │  │  ││  ││  ││  │    │ 72% ▊▊ ││ 45% ▊░ │  │ 88% ▊▊▊  │               │    │
  │  │  └──┘└──┘└──┘└──┘    │ AUTO   ││ AUTO   │  │ LOITER   │               │    │
  │  │  ┌──┐┌──┐┌──┐┌──┐    │ ISR    ││ CARGO  │  │ ASW      │               │    │
  │  │  │●5││●6││●7││●8│    └────────┘└────────┘  └──────────┘               │    │
  │  │  │  ││  ││  ││  │    ┌────────┐┌────────┐  ┌──────────┐               │    │
  │  │  └──┘└──┘└──┘└──┘    │ ✈ M-11 ││ ◌ M-14 │  │ ✈ MD-02  │               │    │
  │  │  ┌──┐┌──┐┌──┐┌──┐    │ 91% ▊▊ ││ MAINT  │  │ 62% ▊▊░  │               │    │
  │  │  │●9││10││11││12│    │ RTL    ││ GROUND │  │ TRANSIT  │  LARGE (1)    │    │
  │  │  │  ││  ││  ││  │    │ SAR    ││ ──     │  │ PATROL   │  ┌──────────┐ │    │
  │  │  └──┘└──┘└──┘└──┘    └────────┘└────────┘  └──────────┘  │ ✈ LG-01  │ │    │
  │  │                       ┌────────┐┌────────┐  ┌──────────┐  │ 94% ▊▊▊  │ │    │
  │  │  ● = active swarm     │ ✈ M-18 ││ ◌ M-22 │  │ ◌ MD-03  │  │ RELAY   │ │    │
  │  │  ◌ = grounded         │ 55% ▊░ ││ CHARGE │  │ CHARGE   │  │ COMMS   │ │    │
  │  │                       │ AUTO   ││ GROUND │  │ GROUND   │  └──────────┘ │    │
  │  │                       │ RELAY  ││ ──     │  │ ──       │               │    │
  │  │                       └────────┘└────────┘  └──────────┘               │    │
  │  └──────────────────────────────────────────────────────────────────────────┘    │
  │                                                                                  │
  │  ┌──── FLEET MAP (all drones) ──────────┐  ┌──── MISSION SCHEDULE ──────────┐  │
  │  │                                       │  │                                │  │
  │  │        ✈3                             │  │  TIME    DRONE   MISSION       │  │
  │  │   ✈1    ✈2         ✈5                │  │  14:30   M-03    ISR patrol #4 │  │
  │  │              ✈4                       │  │  14:45   M-11    RTL (low bat) │  │
  │  │     ●●●● (swarm)                     │  │  15:00   M-22    Cargo run #7  │  │
  │  │                        ✈6             │  │  15:00   MD-01   ASW buoy drop │  │
  │  │                                       │  │  15:30   M-14    Post-maint    │  │
  │  │   [─] zoom  [layer] [filter]          │  │  16:00   MICRO   Swarm deploy  │  │
  │  └───────────────────────────────────────┘  │                                │  │
  │                                              │  Queue: 12 pending, 3 blocked │  │
  │  ┌──── ALERTS ──────────────────────────┐   └────────────────────────────────┘  │
  │  │  ⚠ M-07 battery 45% — RTL in 8 min  │                                       │
  │  │  ⚠ MD-02 entering restricted zone    │                                       │
  │  │  ● M-14 maintenance complete — ready │                                       │
  │  └──────────────────────────────────────┘                                       │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Automated Airbase Status Panel (Tier 3)

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  [Mission Plan]  [Monitor]  [Fleet]  [Airbase]  [Logs]  [Settings]  ● AUTOMATED │
  ├──────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                  │
  │  ┌──── LAUNCH / RECOVERY PADS ────────────────────────────────────────────┐     │
  │  │                                                                         │     │
  │  │  PAD 1 (catapult)       PAD 2 (catapult)       RECOVERY NET            │     │
  │  │  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐      │     │
  │  │  │  State: LOADING  │   │  State: READY    │   │  State: WAITING │      │     │
  │  │  │  Drone: M-22    │   │  Drone: (empty)  │   │  Expected: M-11│      │     │
  │  │  │  Mission: CG-07 │   │                   │   │  ETA: 3:42     │      │     │
  │  │  │  Checklist: 7/10│   │  [LOAD NEXT]     │   │                 │      │     │
  │  │  │  Launch in: 2:15│   │                   │   │  Net: DEPLOYED  │      │     │
  │  │  └─────────────────┘   └─────────────────┘   └─────────────────┘      │     │
  │  └─────────────────────────────────────────────────────────────────────────┘     │
  │                                                                                  │
  │  ┌──── CHARGING / BATTERY BAYS ───────────────────────────────────────────┐     │
  │  │                                                                         │     │
  │  │  Bay 1          Bay 2          Bay 3          Bay 4          Bay 5     │     │
  │  │  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐   │     │
  │  │  │ M-03   │    │ M-14   │    │ EMPTY  │    │ MD-01  │    │ MD-03  │   │     │
  │  │  │ ████░░ │    │ ██████ │    │        │    │ ███░░░ │    │ █░░░░░ │   │     │
  │  │  │  72%   │    │  100%  │    │  ──    │    │  55%   │    │  18%   │   │     │
  │  │  │ 38 min │    │ READY  │    │  AVAIL │    │ 1:12   │    │ 2:45   │   │     │
  │  │  └────────┘    └────────┘    └────────┘    └────────┘    └────────┘   │     │
  │  │                                                                         │     │
  │  │  Swap Robot: IDLE — next swap scheduled for M-11 landing (ETA 3:42)    │     │
  │  └─────────────────────────────────────────────────────────────────────────┘     │
  │                                                                                  │
  │  ┌─── MISSION QUEUE ──────────┐  ┌──── STATE MACHINE ──────────────────┐       │
  │  │                             │  │                                      │       │
  │  │  PRI  MISSION    DRONE  ETA │  │  CURRENT CYCLE: M-11 RECOVERY       │       │
  │  │  ──── ────────── ───── ──── │  │                                      │       │
  │  │   1   CG-07 dlv  M-22  2m  │  │  [PREFLIGHT] → [LAUNCH] → [TRANSIT] │       │
  │  │   2   ISR-12     M-14  8m  │  │       → [ON STATION] → [RTL]        │       │
  │  │   3   SAR-03     M-03  38m │  │       → ■ APPROACH → [CAPTURE]      │       │
  │  │   4   CG-08 dlv  (any) 40m │  │       → [BATTERY SWAP] → [REQUEUE]  │       │
  │  │   5   ASW-02     MD-01 1h  │  │                                      │       │
  │  │   6   RELAY ext  LG-01 2h  │  │  ■ = current state                   │       │
  │  │                             │  │  M-11 on final approach, 1.2km out   │       │
  │  │  AUTO-ASSIGN: ON           │  │  Recovery net deployed, wind 3m/s NW  │       │
  │  │  [+ADD] [PAUSE] [REORDER]  │  │                                      │       │
  │  └─────────────────────────────┘  └──────────────────────────────────────┘       │
  │                                                                                  │
  │  ┌──── HEALTH / GROUNDING DECISIONS ──────────────────────────────────────┐     │
  │  │  DRONE   FLIGHTS  HRS   NEXT MAINT    HEALTH    DECISION              │     │
  │  │  M-03      47    12.3   Servo check   ●● OK     FLY                   │     │
  │  │  M-07      52    14.1   OVERDUE        ●○ WARN  GROUND after RTL      │     │
  │  │  M-11      23     6.1   In 8 flights  ●● OK     FLY                   │     │
  │  │  M-14      51    13.8   Just completed ●● OK     FLY                   │     │
  │  │  MD-01     18    22.4   In 3 flights   ●● OK     FLY                   │     │
  │  │  MD-03      9    11.2   Motor check    ●○ WARN  GROUND until checked  │     │
  │  │  LG-01      6    48.0   In 100 hrs     ●● OK     FLY                   │     │
  │  └──────────────────────────────────────────────────────────────────────────┘     │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. MAVLink Integration

### 4.1 Connection Architecture

```
  TIER 1: DIRECT CONNECTION
  ═════════════════════════

  ┌──────────────┐     USB Serial      ┌────────────────┐    433/900 MHz    ┌───────────┐
  │ Ground Station│ ──────────────────► │ SiK Radio      │ ◄──────────────► │   DRONE   │
  │ (laptop)      │     /dev/ttyUSB0   │ (RFD900x)      │    MAVLink v2    │ Pixhawk   │
  │               │     57600 baud     │ Ground module   │    20km range    │           │
  └──────────────┘                     └────────────────┘                   └───────────┘

  Connection string: serial:/dev/ttyUSB0:57600
  Fallback: udp:0.0.0.0:14550 (if using WiFi link)


  TIER 2: MULTI-VEHICLE ROUTING VIA MAVPROXY
  ═══════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         MAVPROXY ROUTER                                 │
  │                                                                         │
  │  Inputs (from drones):              Outputs (to GCS clients):           │
  │  ┌─────────────────────┐            ┌───────────────────────────┐      │
  │  │ serial:/dev/ttyUSB0 │ ◄─ radio   │ udp:127.0.0.1:14550      │ → GCS│
  │  │ serial:/dev/ttyUSB1 │ ◄─ radio   │ udp:127.0.0.1:14551      │ → GCS│
  │  │ tcp:192.168.1.10:5760│◄─ WiFi    │ udp:0.0.0.0:14560        │ → Web│
  │  │ tcp:relay.ops:5762  │ ◄─ internet│                           │      │
  │  └─────────────────────┘            └───────────────────────────┘      │
  │                                                                         │
  │  System ID routing:                                                     │
  │  SysID 1  → drone MINI-003                                             │
  │  SysID 2  → drone MINI-007                                             │
  │  SysID 3  → drone MEDIUM-001                                           │
  │  ...                                                                    │
  │  SysID 50 → drone LARGE-001                                            │
  │                                                                         │
  │  Each drone gets a unique MAVLink System ID (1-255).                    │
  │  MAVProxy routes messages by System ID.                                 │
  │  GCS filters messages by System ID to display the selected drone.       │
  └─────────────────────────────────────────────────────────────────────────┘


  TIER 3: INTERNET RELAY + REDUNDANCY
  ════════════════════════════════════

  ┌──────────┐  radio  ┌──────────────┐  internet  ┌─────────────────┐
  │ DRONE    │ ◄─────► │ Field relay  │ ─────────► │ Ops Center      │
  │ (remote) │         │ (RPi + SiK   │    VPN     │ MAVProxy master │
  │          │         │  + cellular) │            │                 │
  └──────────┘         └──────────────┘            └────────┬────────┘
                                                            │
  ┌──────────┐  radio  ┌──────────────┐  internet          │
  │ DRONE    │ ◄─────► │ Field relay  │ ─────────────────►─┤
  │ (local)  │         │ (at airbase) │    VPN              │
  └──────────┘         └──────────────┘                     │
                                                            ▼
                                                  ┌─────────────────┐
                                                  │ MAVProxy backup │
                                                  │ (hot standby)   │
                                                  └─────────────────┘
```

### 4.2 Telemetry Message Handling

```
  MAVLink MESSAGE SUBSCRIPTION TABLE
  ═══════════════════════════════════

  Message                    Rate (Hz)  Used For                          Priority
  ─────────────────────────  ─────────  ─────────────────────────────     ────────
  HEARTBEAT                  1          Mode, armed state, system status  CRITICAL
  SYS_STATUS                 2          Battery voltage, current, load    CRITICAL
  GPS_RAW_INT                5          GPS fix, sat count, HDOP          HIGH
  GLOBAL_POSITION_INT        10         Lat/lon/alt/heading — map pos     CRITICAL
  ATTITUDE                   20         Roll/pitch/yaw — instruments      CRITICAL
  VFR_HUD                    10         Airspeed, groundspeed, throttle   HIGH
  MISSION_CURRENT            1          Current waypoint index            HIGH
  NAV_CONTROLLER_OUTPUT      4          Crosstrack error, WP distance     MEDIUM
  BATTERY_STATUS             0.5        Cell voltages, remaining %        HIGH
  WIND                       2          Wind speed/direction              MEDIUM
  TERRAIN_REPORT             1          Terrain alt below drone           MEDIUM
  RC_CHANNELS                5          RC input status (failsafe check)  MEDIUM
  STATUSTEXT                 event      Text messages from autopilot      HIGH
  MISSION_ITEM_REACHED       event      Waypoint reached notification     HIGH
  PARAM_VALUE                on-demand  Parameter read response           LOW
  HOME_POSITION              0.1        Home position (for distance calc) LOW
  FENCE_STATUS               1          Geofence breach status            CRITICAL

  TOTAL BANDWIDTH (single drone, all messages):
  ≈ 8-12 kB/s inbound telemetry
  ≈ 0.5-1 kB/s outbound commands

  At 50 drones (Tier 2): ≈ 400-600 kB/s total telemetry
  Well within modern network capacity.
```

### 4.3 Command Interface

```
  COMMAND CATEGORIES AND MAVLINK MAPPING
  ══════════════════════════════════════

  FLIGHT MODE CHANGES (MAV_CMD_DO_SET_MODE):
  ┌─────────────────────────────────────────────────────┐
  │  GCS Button    │  ArduPilot Mode  │  Use Case       │
  │────────────────┤──────────────────┤─────────────────│
  │  [AUTO]        │  AUTO             │  Follow mission │
  │  [RTL]         │  RTL              │  Return home    │
  │  [LOITER]      │  LOITER           │  Hold position  │
  │  [GUIDED]      │  GUIDED           │  Go to point    │
  │  [LAND]        │  LAND*            │  Land now       │
  └─────────────────────────────────────────────────────┘
  * ArduPlane lands at nearest rally point or home

  MISSION COMMANDS:
  ┌─────────────────────────────────────────────────────┐
  │  Action                   │  Protocol               │
  │───────────────────────────┤─────────────────────────│
  │  Upload mission           │  MISSION_COUNT →        │
  │                           │  MISSION_REQUEST ←      │
  │                           │  MISSION_ITEM →         │
  │                           │  MISSION_ACK ←          │
  │  Set current waypoint     │  MISSION_SET_CURRENT     │
  │  Clear mission            │  MISSION_CLEAR_ALL       │
  │  Download mission         │  MISSION_REQUEST_LIST →  │
  │                           │  MISSION_COUNT ←         │
  │                           │  MISSION_REQUEST →       │
  │                           │  MISSION_ITEM ←          │
  └─────────────────────────────────────────────────────┘

  PAYLOAD COMMANDS:
  ┌─────────────────────────────────────────────────────┐
  │  Action                   │  MAVLink Command         │
  │───────────────────────────┤─────────────────────────│
  │  Move gimbal              │  MAV_CMD_DO_MOUNT_CONTROL│
  │  Set region of interest   │  MAV_CMD_DO_SET_ROI      │
  │  Trigger camera           │  MAV_CMD_DO_DIGICAM_CTRL │
  │  Set camera interval      │  MAV_CMD_DO_SET_CAM_TRIGG│
  │  Release cargo            │  MAV_CMD_DO_SET_SERVO    │
  │  Set servo position       │  MAV_CMD_DO_SET_SERVO    │
  └─────────────────────────────────────────────────────┘

  PARAMETER MANAGEMENT:
  ┌─────────────────────────────────────────────────────┐
  │  Read parameter           │  PARAM_REQUEST_READ →    │
  │                           │  PARAM_VALUE ←           │
  │  Write parameter          │  PARAM_SET →             │
  │                           │  PARAM_VALUE ←           │
  │  Read all parameters      │  PARAM_REQUEST_LIST →    │
  │                           │  PARAM_VALUE × N ←       │
  └─────────────────────────────────────────────────────┘
```

### 4.4 Video Streaming Integration

```
  VIDEO PIPELINE
  ══════════════

  ON THE DRONE (companion computer):
  ┌──────────────────────────────────────────────────┐
  │  Camera (CSI/USB)                                │
  │       │                                          │
  │       ▼                                          │
  │  GStreamer encode pipeline:                      │
  │  v4l2src → videoconvert → x264enc →              │
  │  rtph264pay → udpsink host=GCS port=5600         │
  │                                                  │
  │  OR for companion with hardware encode:          │
  │  libcamerasrc → v4l2h264enc →                    │
  │  rtph264pay → udpsink                            │
  │                                                  │
  │  Resolution: 1280x720 @ 30fps (EO)              │
  │              640x480 @ 9fps (IR — FLIR Lepton)   │
  │  Bitrate: 2-4 Mbps (EO), 0.5 Mbps (IR)         │
  │  Latency: 100-200ms (local radio)               │
  │           300-800ms (internet relay)             │
  └──────────────────────────────────────────────────┘
         │
         │  UDP/RTP stream over data link
         │  (WiFi, 2.4/5.8 GHz data radio, or internet)
         ▼
  ON THE GCS (backend):
  ┌──────────────────────────────────────────────────┐
  │  GStreamer receive + transcode:                  │
  │  udpsrc port=5600 → rtph264depay → h264parse →   │
  │  ┌──► filesink (recording to MP4)                │
  │  │                                               │
  │  └──► WebRTC sender → browser                    │
  │       (via GStreamer webrtcbin or Janus gateway)  │
  │                                                  │
  │  Alternative: use mediamtx (lightweight RTSP     │
  │  to WebRTC proxy) — single binary, zero config   │
  └──────────────────────────────────────────────────┘
         │
         │  WebRTC (sub-200ms browser delivery)
         ▼
  IN THE BROWSER (frontend):
  ┌──────────────────────────────────────────────────┐
  │  <video> element with WebRTC source              │
  │  Canvas overlay for:                             │
  │  - Crosshair / reticle                           │
  │  - Target tracking box (AI overlay)              │
  │  - Telemetry HUD (heading, alt, speed)           │
  │  - GPS coordinates at cursor position            │
  │  - IR colormap selection (for thermal feed)      │
  └──────────────────────────────────────────────────┘


  MULTI-DRONE VIDEO (Tier 2/3):
  ═════════════════════════════
  Each drone streams to a unique port (5600 + drone_index).
  mediamtx acts as a proxy, publishing each stream at:
    rtsp://gcs:8554/drone/MINI-003/eo
    rtsp://gcs:8554/drone/MINI-003/ir
    rtsp://gcs:8554/drone/MEDIUM-001/eo

  The frontend subscribes to whichever stream the operator selects.
  Up to 4 simultaneous video feeds in a grid view.
```

---

## 5. Data Model

### 5.1 Entity-Relationship Diagram

```
  ┌──────────────┐       ┌───────────────────┐       ┌───────────────────┐
  │   OPERATOR    │       │      DRONE         │       │     PAYLOAD       │
  ├──────────────┤       ├───────────────────┤       ├───────────────────┤
  │ id (UUID)    │       │ id (UUID)          │       │ id (UUID)         │
  │ username     │       │ serial_number      │       │ serial_number     │
  │ display_name │       │ callsign           │       │ type (enum)       │
  │ email        │       │ tier (MICRO/MINI/  │       │ subtype           │
  │ password_hash│       │   MEDIUM/LARGE)    │       │ weight_g          │
  │ role (enum)  │       │ mavlink_sysid      │       │ description       │
  │ permissions  │       │ airframe_type      │       │ status            │
  │ last_login   │       │ firmware_version   │       │ config_json       │
  │ active       │       │ status (enum)      │       │ last_calibration  │
  └──────────────┘       │ home_position_lat  │       │ created_at        │
        │                │ home_position_lon  │       └───────────────────┘
        │ operates       │ current_battery_id │             │
        ▼                │ total_flight_hours │             │ installed_on
  ┌──────────────┐       │ total_flights      │             ▼
  │   MISSION     │       │ last_maintenance   │       ┌───────────────────┐
  ├──────────────┤       │ config_params_json │       │ PAYLOAD_ASSIGNMENT │
  │ id (UUID)    │       │ notes              │       ├───────────────────┤
  │ name         │◄──────│ created_at         │       │ payload_id (FK)   │
  │ type (enum)  │       └───────────────────┘       │ drone_id (FK)     │
  │ drone_id(FK) │             │                     │ installed_at      │
  │ operator_id  │             │ has many             │ removed_at        │
  │ status (enum)│             ▼                     └───────────────────┘
  │ priority     │       ┌───────────────────┐
  │ goal_json    │       │      FLIGHT        │
  │ waypoints_json       ├───────────────────┤
  │ geofence_json│       │ id (UUID)          │
  │ constraints  │       │ drone_id (FK)      │
  │ planned_at   │       │ mission_id (FK)    │
  │ started_at   │       │ operator_id (FK)   │
  │ completed_at │       │ started_at         │
  │ result (enum)│       │ ended_at           │
  │ distance_km  │       │ duration_s         │
  │ est_time_s   │       │ distance_km        │
  │ risk_score   │       │ max_altitude_m     │
  │ weather_json │       │ battery_start_pct  │
  │ notes        │       │ battery_end_pct    │
  └──────────────┘       │ result (enum)      │
                         │ log_file_path      │
                         │ telemetry_summary  │
                         │ notes              │
                         └───────────────────┘
                               │
                               │ has many
                               ▼
                         ┌───────────────────┐
                         │  TELEMETRY_SAMPLE  │
                         ├───────────────────┤
                         │ id (bigint)        │
                         │ flight_id (FK)     │
                         │ timestamp_ms       │
                         │ lat, lon, alt_msl  │
                         │ alt_agl            │
                         │ roll, pitch, yaw   │
                         │ airspeed, gndspeed │
                         │ heading            │
                         │ battery_v, bat_pct │
                         │ battery_current_a  │
                         │ gps_sats, hdop     │
                         │ wind_speed, wind_dir│
                         │ throttle_pct       │
                         │ wp_index           │
                         │ mode               │
                         └───────────────────┘

  ┌───────────────────┐       ┌───────────────────┐
  │  MAINTENANCE_LOG   │       │   BATTERY          │
  ├───────────────────┤       ├───────────────────┤
  │ id (UUID)          │       │ id (UUID)          │
  │ drone_id (FK)      │       │ serial_number      │
  │ type (enum)        │       │ chemistry          │
  │ description        │       │ capacity_mah       │
  │ parts_replaced     │       │ cell_count         │
  │ performed_by       │       │ cycles             │
  │ performed_at       │       │ health_pct         │
  │ next_due_hours     │       │ last_full_charge   │
  │ next_due_flights   │       │ internal_resist_mohm│
  │ cost               │       │ status (enum)      │
  │ notes              │       │ current_drone_id   │
  │ attachments_json   │       │ notes              │
  └───────────────────┘       └───────────────────┘
```

### 5.2 Enum Definitions

```
  STATUS AND TYPE ENUMERATIONS
  ════════════════════════════

  DroneStatus:
    READY           — Pre-flight checks passed, awaiting mission
    PREFLIGHT       — Running automated checks
    ARMED           — Motors armed, about to launch
    FLYING          — In the air (any mode)
    RETURNING       — RTL in progress
    LANDING         — Final approach
    LANDED          — On ground, disarming
    CHARGING        — Battery charging in bay
    MAINTENANCE     — Undergoing maintenance, not flyable
    GROUNDED        — Grounded by health monitor
    OFFLINE         — No heartbeat received
    RETIRED         — Permanently out of service

  MissionType:
    DELIVERY        — Point-to-point cargo
    MULTI_DELIVERY  — Multiple drop points (TSP)
    SAR_SEARCH      — Area search grid pattern
    ISR_ROUTE       — Route surveillance
    LOITER          — Orbit observation
    PATROL          — Repeated route patrol
    RELAY           — Communications relay station-keeping
    SWARM_DEPLOY    — Deploy MICRO swarm from carrier
    ASW_BUOY        — Sonar buoy deployment pattern
    MAPPING         — Photogrammetry survey
    PEST_CONTROL    — Spray/bait pattern

  MissionStatus:
    DRAFT           — Being planned
    VALIDATED       — Passed constraint checks
    QUEUED          — In mission queue awaiting execution
    UPLOADING       — Being uploaded to drone
    ACTIVE          — Currently executing
    PAUSED          — Loitering, awaiting resume
    RETURNING       — Mission complete, RTL in progress
    COMPLETED       — Successfully completed
    ABORTED         — Operator aborted
    FAILED          — Failed (crash, lost link, fence breach)

  FlightResult:
    SUCCESS         — Completed as planned
    PARTIAL         — Some objectives completed
    ABORTED         — Operator-initiated abort
    FAILSAFE_RTL    — Triggered RTL failsafe
    FAILSAFE_LAND   — Triggered emergency land
    CRASH           — Uncontrolled impact
    LOST_LINK       — Comms lost, fate unknown

  OperatorRole:
    VIEWER          — Read-only dashboard access
    PILOT           — Can fly single drone (T1 equivalent)
    MISSION_PLANNER — Can create and schedule missions
    FLEET_MANAGER   — Can manage fleet, assign drones
    ADMIN           — Full access including airbase control
    SYSTEM          — Automated system account (T3)

  MaintenanceType:
    SCHEDULED       — Regular interval maintenance
    UNSCHEDULED     — Fault-driven maintenance
    INSPECTION      — Visual or sensor inspection
    CALIBRATION     — Sensor/actuator calibration
    REPAIR          — Part replacement or repair
    FIRMWARE_UPDATE — Software/firmware update
    BATTERY_SERVICE — Battery health check or replacement

  PayloadType:
    CARGO_POD       — Cargo delivery container
    EO_CAMERA       — Electro-optical camera (visible)
    IR_CAMERA       — Thermal infrared camera
    DUAL_SENSOR     — Combined EO + IR gimbal
    LIDAR           — LiDAR scanner
    COMMS_RELAY     — Communications relay package
    SONAR_DEPLOYER  — Sonar buoy dispenser
    SPRAY_SYSTEM    — Agricultural/pest control sprayer
    GENERIC_SENSOR  — Custom/generic sensor bay

  BatteryStatus:
    CHARGING        — Currently charging
    CHARGED         — Fully charged, ready for use
    IN_USE          — Installed in a flying drone
    DEPLETED        — Needs charging
    DEGRADED        — Health below threshold, restricted use
    RETIRED         — End of life, do not use
```

### 5.3 Telemetry Storage Strategy

```
  TELEMETRY DATA TIERING
  ══════════════════════

  TIER 1 — HOT (Redis / in-memory):
  Latest values only. Overwritten every update cycle.
  Used for: real-time dashboard, instrument displays.
  Retention: current session only.
  Structure: hash per drone → {lat, lon, alt, roll, pitch, yaw, ...}

  TIER 2 — WARM (PostgreSQL time-series table):
  Sampled at 1 Hz (downsampled from 10-20 Hz raw).
  Used for: flight replay, post-flight analysis, trend graphs.
  Retention: 1 year.
  Indexed on: (flight_id, timestamp_ms).
  Partitioned by month for query performance.

  TIER 3 — COLD (compressed binary log files):
  Full MAVLink .tlog files (binary, every message at original rate).
  Used for: crash investigation, detailed forensics.
  Retention: indefinite.
  Storage: local disk or S3-compatible object store.
  Compressed: gzip, ~2-5 MB per flight hour.

  ESTIMATED STORAGE:
  1 Hz sampled telemetry: ~100 bytes/sample × 3600 samples/hr = ~360 KB/hr
  At 50 drones, 5 hrs/day: ~90 MB/day = ~33 GB/year
  Raw .tlog files: ~5 MB/hr × 250 hrs/day = ~1.25 GB/day = ~456 GB/year
```

---

## 6. Automated Airbase Software (Tier 3)

### 6.1 Launch/Recovery Cycle State Machine

```
  AIRBASE DRONE LIFECYCLE STATE MACHINE
  ═════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │                    ┌──────────┐                                         │
  │           ┌────────│  IDLE    │◄───────────────────────────┐           │
  │           │        │ (in bay) │                            │           │
  │           │        └────┬─────┘                            │           │
  │           │             │ mission assigned                 │           │
  │           │             ▼                                  │           │
  │           │        ┌──────────────┐                        │           │
  │           │        │  PRE-FLIGHT  │                        │           │
  │           │        │  CHECKS      │                        │           │
  │           │        │              │                        │           │
  │           │        │  1. Battery OK (>95%)?                │           │
  │           │        │  2. GPS lock?                         │           │
  │           │        │  3. IMU calibrated?                   │           │
  │           │        │  4. Airspeed sensor OK?               │           │
  │           │        │  5. Payload installed + CG check?     │           │
  │           │        │  6. Geofence + rally uploaded?        │           │
  │           │        │  7. Failsafes configured?             │           │
  │           │        │  8. Servo sweep test?                 │           │
  │           │        │  9. Comms link quality > threshold?   │           │
  │           │        │ 10. Weather within limits?            │           │
  │  FAIL:    │        └────┬─────────┘                        │           │
  │  ground   │             │ all checks PASS                  │           │
  │  + alert  │             ▼                                  │           │
  │           │        ┌──────────────┐                        │           │
  │    ┌──────┤        │  LOAD TO PAD │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  Robot moves drone                    │           │
  │    │      │        │  from bay to catapult                 │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  ARM + LAUNCH│                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  Arm motors                           │           │
  │    │      │        │  Catapult release                     │           │
  │    │      │        │  Verify climb rate > 2 m/s            │           │
  │    │      │        │  Handoff to AUTO mode                 │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  ON MISSION  │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  Monitored by health system           │           │
  │    │      │        │  Can be recalled (RTL) at any time    │           │
  │    │      │        │  Auto-RTL on low battery              │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │ mission complete OR RTL           │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  APPROACH    │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  Sequence approach waypoints           │           │
  │    │      │        │  Align with recovery system           │           │
  │    │      │        │  Deploy recovery net/arresting wire   │           │
  │    │      │        │  Wind check (abort if gusts > limit)  │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  CAPTURE     │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  Net capture / belly landing           │           │
  │    │      │        │  Verify drone secured                 │           │
  │    │      │        │  Disarm motors                        │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  POST-FLIGHT │                        │           │
  │    │      │        │  CHECKS      │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │  1. Download flight log               │           │
  │    │      │        │  2. Check structural damage           │           │
  │    │      │        │  3. Record battery end voltage        │           │
  │    │      │        │  4. Update flight hours/count         │           │
  │    │      │        │  5. Flag if maintenance due           │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │ BATTERY SWAP │                        │           │
  │    │      │        │              │                        │           │
  │    │      │        │ Robot removes spent battery            │           │
  │    │      │        │ Installs charged battery from bay     │           │
  │    │      │        │ Spent battery → charging slot         │           │
  │    │      │        │ Verify new battery voltage + health   │           │
  │    │      │        └────┬─────────┘                        │           │
  │    │      │             │                                  │           │
  │    │      │             ▼                                  │           │
  │    │      │        ┌──────────────┐                        │           │
  │    │      │        │  REQUEUE     │────────────────────────┘           │
  │    │      │        │              │                                    │
  │    │      │        │  If next mission pending: → PRE-FLIGHT           │
  │    │      │        │  If no mission: → IDLE                           │
  │    │      │        └──────────────┘                                    │
  │    │      │                                                            │
  │    │      │                                                            │
  │    │      │        FAULT STATES (any state can transition here):       │
  │    │      │        ┌──────────────┐                                    │
  │    └──────┼───────►│  GROUNDED    │                                    │
  │           │        │              │                                    │
  │           │        │  Reason logged (health fail, maintenance due,    │
  │           │        │  crash damage, operator command)                  │
  │           │        │  Requires human intervention to clear             │
  │           │        └──────────────┘                                    │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  TIMING TARGETS (fully automated cycle):
  ═══════════════════════════════════════
  Pre-flight checks:     60-120 seconds
  Load to pad:           30-60 seconds
  Arm + launch:          15-30 seconds
  Recovery + capture:    30-60 seconds
  Post-flight checks:    60-120 seconds
  Battery swap:          60-120 seconds
  ──────────────────────────────────────
  TOTAL TURNAROUND:      4-8 minutes

  With 5 charging bays and 2 catapults:
  Sustained sortie rate: ~8-12 flights per hour per drone
  Fleet of 10 drones:    ~60-80 sorties per 8-hour shift
```

### 6.2 Charging and Battery Swap System

```
  BATTERY MANAGEMENT ARCHITECTURE
  ═══════════════════════════════

  ┌─────────────────────────────────────────────────────────────────┐
  │                    BATTERY MANAGEMENT SERVICE                    │
  │                                                                 │
  │  ┌─────────────────────────────────────────────────────────┐   │
  │  │  BATTERY STATE TRACKER                                   │   │
  │  │                                                         │   │
  │  │  Monitors all batteries in the system:                  │   │
  │  │  - Voltage, current, temperature (via smart BMS)        │   │
  │  │  - Charge state (%, estimated minutes remaining)        │   │
  │  │  - Health (internal resistance, capacity fade)          │   │
  │  │  - Cycle count                                          │   │
  │  │  - Location (which bay, which drone, or storage)        │   │
  │  └─────────────────────────────────────────────────────────┘   │
  │                                                                 │
  │  ┌─────────────────────────────────────────────────────────┐   │
  │  │  CHARGING SCHEDULER                                      │   │
  │  │                                                         │   │
  │  │  Priority queue for charging:                           │   │
  │  │  1. Batteries assigned to upcoming missions             │   │
  │  │  2. Batteries below 50%                                 │   │
  │  │  3. Balance charging (oldest charged batteries first)   │   │
  │  │                                                         │   │
  │  │  Charge profiles per chemistry:                         │   │
  │  │  - LiPo 4S: CC/CV at 1C to 16.8V, taper to 0.1C       │   │
  │  │  - Li-ion 6S: CC/CV at 0.5C to 25.2V                   │   │
  │  │  - Storage charge: 3.8V/cell if idle > 24 hours         │   │
  │  └─────────────────────────────────────────────────────────┘   │
  │                                                                 │
  │  ┌─────────────────────────────────────────────────────────┐   │
  │  │  HEALTH MONITOR                                          │   │
  │  │                                                         │   │
  │  │  Retire battery when:                                   │   │
  │  │  - Internal resistance > 150% of new value              │   │
  │  │  - Capacity < 80% of rated                              │   │
  │  │  - Any cell voltage imbalance > 0.1V under load         │   │
  │  │  - Physical damage detected (temperature anomaly)       │   │
  │  │  - Cycle count > rated cycle life                       │   │
  │  └─────────────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────────────┘

  PHYSICAL LAYOUT:
  ════════════════

  ┌────────────────────────────────────────────────────────────────┐
  │                        AIRBASE FLOOR PLAN                       │
  │                                                                │
  │  ┌────────┐  ┌────────┐                                       │
  │  │ PAD 1  │  │ PAD 2  │   LAUNCH AREA                        │
  │  │catapult│  │catapult│   (clear of obstacles)                │
  │  └───┬────┘  └───┬────┘                                       │
  │      │           │                                             │
  │  ────┼───────────┼─────── ROBOT RAIL TRACK ─────────────┐     │
  │      │           │                                       │     │
  │  ┌───┴───────────┴────────────────────────────────────┐  │     │
  │  │                  DRONE BAYS (10 slots)              │  │     │
  │  │  ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌──┐┌──┐│  │     │
  │  │  │ 1 ││ 2 ││ 3 ││ 4 ││ 5 ││ 6 ││ 7 ││ 8 ││9 ││10││  │     │
  │  │  └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└──┘└──┘│  │     │
  │  └────────────────────────────────────────────────────┘  │     │
  │                                                          │     │
  │  ┌────────────────────────────────────────────────────┐  │     │
  │  │            BATTERY CHARGING STATION (20 slots)     │  │     │
  │  │  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐       │  │     │
  │  │  │C1││C2││C3││C4││C5││C6││C7││C8││C9││10│       │  │     │
  │  │  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘       │  │     │
  │  │  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐       │  │     │
  │  │  │11││12││13││14││15││16││17││18││19││20│       │  │     │
  │  │  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘       │  │     │
  │  └────────────────────────────────────────────────────┘  │     │
  │                                                          │     │
  │  ┌──────────────────┐  ┌────────────────────────────┐    │     │
  │  │ RECOVERY NET     │  │ WEATHER STATION             │    │     │
  │  │ (retractable)    │  │ wind, temp, vis, pressure   │    │     │
  │  └──────────────────┘  └────────────────────────────┘    │     │
  │                                                          │     │
  │  ◄──────────── ROBOT on linear rail ────────────────────►│     │
  │    (moves drones between bays, pads, and charging)       │     │
  └──────────────────────────────────────────────────────────┘     │
  │                                                                │
  └────────────────────────────────────────────────────────────────┘
```

### 6.3 Mission Queue Management

```
  MISSION QUEUE SYSTEM
  ═══════════════════

  ┌──────────────────────────────────────────────────────────────────┐
  │                   MISSION QUEUE MANAGER                          │
  │                                                                  │
  │  INPUTS:                                                         │
  │  ├── Operator-submitted missions (via web UI)                    │
  │  ├── Scheduled recurring missions (patrol patterns)              │
  │  ├── External API orders (customer delivery requests)            │
  │  ├── Auto-generated missions (relay rotation, health checks)     │
  │  └── Emergency overrides (SAR, security response)                │
  │                                                                  │
  │  PRIORITY LEVELS:                                                │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │  P0 — EMERGENCY    Immediate, preempts all others       │    │
  │  │  P1 — URGENT       Next available drone, queue jump     │    │
  │  │  P2 — HIGH         Scheduled within 15 minutes          │    │
  │  │  P3 — NORMAL       Scheduled in order                   │    │
  │  │  P4 — LOW          Fill gaps, opportunistic              │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                                                                  │
  │  ASSIGNMENT ALGORITHM:                                           │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │  For each pending mission (highest priority first):      │    │
  │  │                                                         │    │
  │  │  1. Filter drones by capability:                        │    │
  │  │     - Tier matches mission requirements                 │    │
  │  │     - Payload type available and installed               │    │
  │  │     - Range sufficient for mission distance              │    │
  │  │                                                         │    │
  │  │  2. Filter by availability:                             │    │
  │  │     - Status = READY or IDLE                            │    │
  │  │     - Battery >= mission_requirement + 25% reserve      │    │
  │  │     - Not grounded or in maintenance                    │    │
  │  │                                                         │    │
  │  │  3. Score remaining candidates:                         │    │
  │  │     - Battery level (higher = better)                   │    │
  │  │     - Proximity to mission start point                  │    │
  │  │     - Maintenance hours remaining until next service    │    │
  │  │     - Payload already installed (avoids swap time)      │    │
  │  │                                                         │    │
  │  │  4. Assign top-scoring drone                            │    │
  │  │     - If no drone available: queue mission, set ETA     │    │
  │  │     - If ETA > deadline: alert operator                 │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                                                                  │
  │  DECONFLICTION:                                                  │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │  Before assigning any mission:                          │    │
  │  │                                                         │    │
  │  │  1. Spatial check:                                      │    │
  │  │     - No two drones within 200m horizontal, 50m vert    │    │
  │  │     - No route intersections at same altitude + time     │    │
  │  │     - Launch/recovery windows don't overlap             │    │
  │  │                                                         │    │
  │  │  2. Temporal check:                                     │    │
  │  │     - Stagger launches by 60 seconds minimum            │    │
  │  │     - Stagger recoveries by 120 seconds minimum         │    │
  │  │     - Don't exceed airspace density limit               │    │
  │  │                                                         │    │
  │  │  3. Resource check:                                     │    │
  │  │     - Sufficient charged batteries for the mission      │    │
  │  │     - Charging bays available for returned batteries    │    │
  │  │     - Launch pad availability at scheduled time         │    │
  │  └─────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────┘
```

### 6.4 Health Check Automation

```
  DRONE HEALTH MONITORING SYSTEM
  ══════════════════════════════

  ┌──────────────────────────────────────────────────────────────────┐
  │                   HEALTH MONITOR (continuous)                     │
  │                                                                  │
  │  IN-FLIGHT MONITORING (real-time):                               │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │                                                         │    │
  │  │  CHECK                     THRESHOLD        ACTION      │    │
  │  │  ──────────────────────── ──────────────── ──────────── │    │
  │  │  Battery voltage           < 3.3V/cell      LAND NOW    │    │
  │  │  Battery voltage           < 3.5V/cell      RTL         │    │
  │  │  Battery current spike     > 150% nominal   LOG + ALERT │    │
  │  │  GPS satellite count       < 6              LOITER+ALERT│    │
  │  │  GPS HDOP                  > 2.5            LOG + ALERT │    │
  │  │  Attitude oscillation      roll/pitch > 30° LAND NOW    │    │
  │  │  Airspeed sensor           disagree > 5m/s  RTL + ALERT │    │
  │  │  Vibration (IMU accel)     > 30 m/s²        LOG + ALERT │    │
  │  │  Motor temperature*        > 80°C           REDUCE POWER│    │
  │  │  ESC current*              > 90% rated      LOG + WARN  │    │
  │  │  Compass consistency       heading err > 30° ALERT       │    │
  │  │  Geofence proximity        < 100m of fence  WARN        │    │
  │  │  Comms link RSSI           < -95 dBm        WARN        │    │
  │  │  Comms link loss           > 30 seconds     RTL (auto)  │    │
  │  │                                                         │    │
  │  │  * requires companion computer telemetry                │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                                                                  │
  │  POST-FLIGHT ANALYSIS (automated after every flight):            │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │                                                         │    │
  │  │  1. Log download and parse                              │    │
  │  │  2. Vibration analysis (FFT on IMU data)                │    │
  │  │     - Detect propeller imbalance                        │    │
  │  │     - Detect bearing wear                               │    │
  │  │  3. Battery discharge curve analysis                    │    │
  │  │     - Compare to baseline for capacity fade             │    │
  │  │     - Detect voltage sag under load                     │    │
  │  │  4. Servo response analysis                             │    │
  │  │     - Compare demanded vs achieved deflection           │    │
  │  │     - Detect servo wear or binding                      │    │
  │  │  5. Navigation accuracy                                 │    │
  │  │     - Crosstrack error statistics                        │    │
  │  │     - Altitude hold accuracy                            │    │
  │  │  6. Anomaly detection (ML model, Phase 4+)              │    │
  │  │     - Trained on historical flight data                 │    │
  │  │     - Flags flights that deviate from learned baseline  │    │
  │  │                                                         │    │
  │  │  OUTPUT: Health score 0-100                             │    │
  │  │  > 80: FLY                                              │    │
  │  │  60-80: FLY WITH CAUTION (shorter missions only)        │    │
  │  │  40-60: GROUND (schedule maintenance)                   │    │
  │  │  < 40: GROUND IMMEDIATELY (do not fly)                  │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                                                                  │
  │  MAINTENANCE SCHEDULING:                                         │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │                                                         │    │
  │  │  Interval-based (whichever comes first):                │    │
  │  │  ──────────────────────────────────────────────────     │    │
  │  │  MINI tier:                                             │    │
  │  │    Every 20 flights: visual inspection, servo check     │    │
  │  │    Every 50 flights: propeller replacement              │    │
  │  │    Every 100 flights: full teardown inspection          │    │
  │  │    Every 50 hours: motor replacement                    │    │
  │  │                                                         │    │
  │  │  MEDIUM tier:                                           │    │
  │  │    Every 10 flights: visual + structural check          │    │
  │  │    Every 25 flights: servo replacement                  │    │
  │  │    Every 200 hours: engine overhaul (hybrid)            │    │
  │  │                                                         │    │
  │  │  LARGE tier:                                            │    │
  │  │    Every 5 flights: full inspection                     │    │
  │  │    Every 50 hours: detailed structural check            │    │
  │  │    Every 500 hours: major overhaul                      │    │
  │  │                                                         │    │
  │  │  Condition-based (triggered by health analysis):        │    │
  │  │    Vibration spike → propeller/motor inspection         │    │
  │  │    Servo lag → servo replacement                        │    │
  │  │    Battery sag → battery retirement                     │    │
  │  │    Navigation drift → sensor calibration                │    │
  │  └─────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────┘
```

### 6.5 External System Integration

```
  EXTERNAL INTEGRATION POINTS (Tier 3)
  ═════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐   │
  │  │  ATC / UTM    │    │  WEATHER       │    │  CUSTOMER     │   │
  │  │  Integration  │    │  Services      │    │  Order API    │   │
  │  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘   │
  │          │                    │                    │            │
  │          ▼                    ▼                    ▼            │
  │  ┌───────────────────────────────────────────────────────────┐ │
  │  │                   INTEGRATION GATEWAY                      │ │
  │  │                                                           │ │
  │  │  ATC / UTM:                                               │ │
  │  │  ├── Submit flight plans (NOTAM, UAS Zone Mgmt)           │ │
  │  │  ├── Receive airspace restrictions                        │ │
  │  │  ├── Broadcast ADS-B position (if equipped)               │ │
  │  │  ├── Receive ADS-B traffic (conflict avoidance)           │ │
  │  │  └── Protocol: REST API to UTM provider (e.g., Altitude   │ │
  │  │      Angel, AirMap, or CAA-approved UTM)                  │ │
  │  │                                                           │ │
  │  │  Weather:                                                 │ │
  │  │  ├── Current conditions (wind, vis, precip, temp)         │ │
  │  │  ├── Forecast (1-6 hour lookahead for scheduling)         │ │
  │  │  ├── METAR/TAF from nearby airfields                      │ │
  │  │  ├── Sources: OpenWeatherMap, Met Office DataPoint,       │ │
  │  │  │   local weather station (on-site anemometer)           │ │
  │  │  └── Decision: pause launches if wind > limits            │ │
  │  │                                                           │ │
  │  │  Customer Orders:                                         │ │
  │  │  ├── Receive delivery orders via REST API                 │ │
  │  │  ├── Validate pickup/dropoff coordinates                  │ │
  │  │  ├── Create mission from order                            │ │
  │  │  ├── Assign priority and deadline                         │ │
  │  │  ├── Return tracking status and ETA                       │ │
  │  │  └── Webhook notifications (dispatched, delivered, failed)│ │
  │  │                                                           │ │
  │  │  NOTAM Database:                                          │ │
  │  │  ├── Poll for new NOTAMs in operational area              │ │
  │  │  ├── Parse and convert to no-fly zone polygons            │ │
  │  │  ├── Auto-update geofence constraints                     │ │
  │  │  └── Alert if active mission conflicts with new NOTAM     │ │
  │  └───────────────────────────────────────────────────────────┘ │
  └─────────────────────────────────────────────────────────────────┘
```

### 6.6 Redundancy and Failover

```
  TIER 3 REDUNDANCY ARCHITECTURE
  ══════════════════════════════

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  PRIMARY SERVER                  STANDBY SERVER              │
  │  ┌─────────────────┐           ┌─────────────────┐          │
  │  │ FastAPI          │           │ FastAPI          │          │
  │  │ MAVLink Router   │  sync →  │ MAVLink Router   │          │
  │  │ Airbase Control  │           │ Airbase Control  │          │
  │  │ Mission Queue    │           │ Mission Queue    │          │
  │  └────────┬────────┘           └────────┬────────┘          │
  │           │                             │                    │
  │  ┌────────┴────────┐           ┌────────┴────────┐          │
  │  │ PostgreSQL       │  stream  │ PostgreSQL       │          │
  │  │ (primary)        │ ──────►  │ (replica)        │          │
  │  └─────────────────┘           └─────────────────┘          │
  │                                                              │
  │  ┌─────────────────┐           ┌─────────────────┐          │
  │  │ Redis            │  replicate│ Redis            │          │
  │  │ (primary)        │ ────────►│ (replica)        │          │
  │  └─────────────────┘           └─────────────────┘          │
  │                                                              │
  │  FAILOVER BEHAVIOUR:                                         │
  │  1. Heartbeat between primary/standby every 1 second         │
  │  2. If primary fails 3 consecutive heartbeats: standby       │
  │     promotes itself to primary                               │
  │  3. PostgreSQL replica promotes to primary                   │
  │  4. MAVLink connections re-establish to new primary          │
  │  5. In-flight drones continue on ArduPilot failsafes        │
  │     until GCS link restored (typically < 30 seconds)         │
  │  6. Recovery: old primary restarts as standby                │
  │                                                              │
  │  CRITICAL SAFETY RULE:                                       │
  │  All drones have ArduPilot failsafes configured              │
  │  independently of the GCS. If the entire ground station      │
  │  fails, every drone will RTL on comm loss timeout            │
  │  (FS_LONG_ACTN = 1, FS_LONG_TIMEOUT = 120 seconds).         │
  │  The GCS is never a single point of failure for safety.      │
  └──────────────────────────────────────────────────────────────┘
```

---

## 7. Integration with Existing Mission Planning Engine

### 7.1 How the GCS Wraps the MPE

```
  INTEGRATION ARCHITECTURE
  ═══════════════════════

  The existing mission-planning-engine (src/mpe/) is imported as a Python
  package into the GCS backend. The GCS does NOT fork or rewrite it — it
  wraps it with a service layer.

  ┌──────────────────────────────────────────────────────────────────┐
  │  GCS Backend (FastAPI)                                           │
  │                                                                  │
  │  ┌────────────────────────────────────────────────────────────┐  │
  │  │  MissionService                                            │  │
  │  │                                                            │  │
  │  │  def plan_mission(goal: GoalRequest) -> MissionResponse:   │  │
  │  │      # 1. Convert web form input to MPE BasicMission       │  │
  │  │      mission = BasicMission(                               │  │
  │  │          home=Coordinate(...),                             │  │
  │  │          waypoints=[Coordinate(...)],                      │  │
  │  │          cruise_altitude_m=goal.altitude,                  │  │
  │  │      )                                                     │  │
  │  │                                                            │  │
  │  │      # 2. Call existing planner                            │  │
  │  │      items = build_mission(mission)  # from mpe.planner   │  │
  │  │                                                            │  │
  │  │      # 3. Generate .waypoints file                         │  │
  │  │      wpt_string = to_string(items)  # from mpe.writer     │  │
  │  │                                                            │  │
  │  │      # 4. Store in database                                │  │
  │  │      db_mission = MissionORM(                              │  │
  │  │          type=goal.mission_type,                           │  │
  │  │          waypoints_json=items_to_json(items),              │  │
  │  │          ...                                               │  │
  │  │      )                                                     │  │
  │  │      db.add(db_mission)                                    │  │
  │  │                                                            │  │
  │  │      # 5. Return to frontend for review                    │  │
  │  │      return MissionResponse(                               │  │
  │  │          id=db_mission.id,                                 │  │
  │  │          waypoints=items,                                  │  │
  │  │          distance_km=...,                                  │  │
  │  │          est_time_s=...,                                   │  │
  │  │          risk_score=...,                                   │  │
  │  │      )                                                     │  │
  │  │                                                            │  │
  │  │  def upload_mission(mission_id: UUID, drone_id: UUID):     │  │
  │  │      # Retrieve mission items from DB                      │  │
  │  │      # Call mpe.upload.upload_mission() with               │  │
  │  │      # the drone's connection string                       │  │
  │  │      upload_mission(items, connection_string)               │  │
  │  └────────────────────────────────────────────────────────────┘  │
  │                                                                  │
  │  As the MPE grows (Phase B-D: SAR, ISR, constraint engine),      │
  │  the GCS service layer stays thin — it just calls the             │
  │  appropriate planner with the goal parameters from the UI.        │
  └──────────────────────────────────────────────────────────────────┘
```

### 7.2 API Surface

```
  REST API ENDPOINTS
  ═════════════════

  MISSIONS:
  POST   /api/missions              Create a new mission from goal
  GET    /api/missions              List missions (filterable)
  GET    /api/missions/{id}         Get mission details
  PUT    /api/missions/{id}         Update mission (edit waypoints)
  DELETE /api/missions/{id}         Delete draft mission
  POST   /api/missions/{id}/validate   Run constraint checks
  POST   /api/missions/{id}/upload     Upload to assigned drone
  POST   /api/missions/{id}/start      Arm and start mission

  DRONES:
  GET    /api/drones                List all drones
  GET    /api/drones/{id}           Get drone details + status
  PUT    /api/drones/{id}           Update drone config
  GET    /api/drones/{id}/params    Get ArduPilot parameters
  PUT    /api/drones/{id}/params    Set ArduPilot parameter
  POST   /api/drones/{id}/command   Send command (mode change, etc.)
  GET    /api/drones/{id}/telemetry Latest telemetry snapshot

  FLIGHTS:
  GET    /api/flights               List flights (filterable)
  GET    /api/flights/{id}          Get flight details
  GET    /api/flights/{id}/telemetry   Telemetry time series
  GET    /api/flights/{id}/log      Download raw .tlog file

  FLEET (Tier 2/3):
  GET    /api/fleet/status          All drones at a glance
  POST   /api/fleet/schedule        Schedule a mission for future
  GET    /api/fleet/conflicts       Check for airspace conflicts

  PAYLOADS:
  GET    /api/payloads              List all payloads
  POST   /api/payloads/{id}/assign  Assign payload to drone
  POST   /api/payloads/{id}/command Gimbal/camera control

  MAINTENANCE:
  GET    /api/maintenance           List maintenance records
  POST   /api/maintenance           Log maintenance event
  GET    /api/maintenance/due       List overdue maintenance

  AIRBASE (Tier 3):
  GET    /api/airbase/status        Full airbase status
  GET    /api/airbase/queue         Mission queue
  POST   /api/airbase/queue         Add mission to queue
  PUT    /api/airbase/queue/reorder Reorder queue
  GET    /api/airbase/batteries     Battery bay status
  POST   /api/airbase/launch/{pad}  Manual launch command
  POST   /api/airbase/recover       Initiate recovery sequence

  AUTH (Tier 2/3):
  POST   /api/auth/login            Get JWT token
  POST   /api/auth/refresh          Refresh token
  GET    /api/auth/me               Current user info


  WEBSOCKET ENDPOINTS
  ═══════════════════

  ws://host/ws/telemetry/{drone_id}
    Streams: attitude, position, battery, GPS, mode, alerts
    Format: MessagePack (binary, compact)
    Rate: 10 Hz position, 20 Hz attitude, 1 Hz system status

  ws://host/ws/fleet
    Streams: all drone positions + status (summary)
    Format: JSON (lower rate, human-readable)
    Rate: 2 Hz per drone

  ws://host/ws/airbase
    Streams: pad status, queue changes, battery status, state machine
    Format: JSON
    Rate: event-driven (push on state change)

  ws://host/ws/alerts
    Streams: all alerts and warnings across the system
    Format: JSON
    Rate: event-driven
```

---

## 8. Security Architecture

```
  SECURITY LAYERS
  ═══════════════

  TIER 1 (field laptop):
  ┌─────────────────────────────────────────────────────────┐
  │  - Single user, no authentication required               │
  │  - MAVLink link is direct radio (not internet-exposed)   │
  │  - Disk encryption (OS-level) protects flight logs       │
  │  - No secrets in source code (API keys in .env file)     │
  └─────────────────────────────────────────────────────────┘

  TIER 2/3 (multi-user, internet-connected):
  ┌─────────────────────────────────────────────────────────┐
  │  AUTHENTICATION:                                         │
  │  ├── JWT tokens (short-lived: 15 min access, 7d refresh) │
  │  ├── bcrypt password hashing                             │
  │  ├── Optional 2FA (TOTP) for ADMIN and FLEET_MANAGER    │
  │  └── Session invalidation on role change                 │
  │                                                         │
  │  AUTHORIZATION (RBAC):                                   │
  │  ├── VIEWER: read telemetry, view map, read logs         │
  │  ├── PILOT: + control single assigned drone              │
  │  ├── MISSION_PLANNER: + create/edit/schedule missions    │
  │  ├── FLEET_MANAGER: + assign drones, manage fleet        │
  │  ├── ADMIN: + user management, airbase control, config   │
  │  └── Every mutating API call checks role + ownership     │
  │                                                         │
  │  NETWORK:                                                │
  │  ├── HTTPS/WSS only (TLS 1.3)                           │
  │  ├── VPN for MAVLink internet relay (WireGuard)          │
  │  ├── MAVLink signing enabled (MAVLink v2 message signing)│
  │  ├── Rate limiting on all API endpoints                  │
  │  └── Firewall: only 443 (HTTPS) and VPN port exposed    │
  │                                                         │
  │  DATA:                                                   │
  │  ├── Database encryption at rest (PostgreSQL TDE)        │
  │  ├── Flight logs encrypted before archive                │
  │  ├── No PII stored beyond operator accounts              │
  │  └── Audit log for all commands sent to drones           │
  │                                                         │
  │  MAVLink SECURITY:                                       │
  │  ├── MAVLink v2 message signing (shared secret per drone)│
  │  ├── Prevents command injection from rogue transmitters  │
  │  ├── Link encryption via data radio (AES on RFD900x)    │
  │  └── System ID validation (reject unknown SysIDs)        │
  └─────────────────────────────────────────────────────────┘
```

---

## 9. Development Roadmap

```
  DEVELOPMENT PHASES
  ═════════════════

  PHASE 1: FIELD STATION MVP (Tier 1)                      12-16 weeks
  ═══════════════════════════════════
  Deliverable: Electron desktop app, single drone, offline
  ┌───────────────────────────────────────────────────────────────┐
  │  Week 1-2:  Project scaffold (Svelte + FastAPI + SQLite)      │
  │  Week 3-4:  MAVLink connection (USB serial, single drone)     │
  │             Telemetry decode + WebSocket broadcast            │
  │  Week 5-6:  Map view (MapLibre, offline tiles, drone marker)  │
  │             Waypoint display on map                          │
  │  Week 7-8:  Mission planning screen (goal form → MPE → map)   │
  │             Pre-flight checklist (manual + automated items)  │
  │  Week 9-10: Flight instruments (attitude, alt, speed, battery)│
  │             Command panel (RTL, loiter, mode changes)        │
  │  Week 11-12: Video feed (GStreamer → WebRTC, single stream)  │
  │              Payload control (gimbal, camera trigger)        │
  │  Week 13-14: Post-flight log download and basic analysis     │
  │              Electron packaging and installer               │
  │  Week 15-16: SITL integration testing, bug fixes             │
  └───────────────────────────────────────────────────────────────┘

  PHASE 2: OPERATIONS CENTER (Tier 2)                      12-16 weeks
  ══════════════════════════════════
  Deliverable: Web app, multi-drone, multi-operator
  ┌───────────────────────────────────────────────────────────────┐
  │  Week 1-2:  Docker deployment (PostgreSQL, Redis, Nginx)      │
  │  Week 3-4:  Auth system (JWT, RBAC, user management)          │
  │  Week 5-6:  Multi-drone MAVLink routing (MAVProxy)            │
  │             Fleet status WebSocket                           │
  │  Week 7-8:  Fleet dashboard (grid view, fleet map)            │
  │  Week 9-10: Mission scheduling and deconfliction              │
  │             Airspace management (NFZ, geofence editor)       │
  │  Week 11-12: Weather integration (OpenWeatherMap + Met Office)│
  │              Maintenance tracking and alerts                 │
  │  Week 13-14: Multi-drone video (mediamtx, grid view)         │
  │              Data fusion (overlay multiple drones on map)    │
  │  Week 15-16: CesiumJS 3D view, airspace volume visualization │
  │              Load testing with 50 simulated drones           │
  └───────────────────────────────────────────────────────────────┘

  PHASE 3: AUTOMATED AIRBASE (Tier 3)                      16-24 weeks
  ═══════════════════════════════════
  Deliverable: Server + hardware integration, autonomous ops
  ┌───────────────────────────────────────────────────────────────┐
  │  Week 1-4:  State machine framework and unit tests            │
  │             Hardware abstraction layer (HAL) interfaces       │
  │  Week 5-8:  Mission queue manager with priority scheduling    │
  │             Auto-assignment algorithm                         │
  │  Week 9-12: Battery management system integration             │
  │             Charging bay HAL (smart charger protocol)         │
  │  Week 13-16: Launch/recovery automation                       │
  │              Catapult control HAL                             │
  │              Recovery net/arresting wire HAL                  │
  │  Week 17-20: Health monitoring and grounding logic            │
  │              Post-flight auto-analysis                        │
  │  Week 21-22: External integrations (ATC/UTM, customer API)   │
  │  Week 23-24: Redundancy (primary-standby failover)            │
  │              Remote monitoring dashboard                      │
  └───────────────────────────────────────────────────────────────┘

  TOTAL: ~40-56 weeks for full system
  Phase 1 alone is sufficient for first flights with the MINI tier.
```

---

## 10. Platform Family Considerations

```
  HOW THE GCS HANDLES EACH DRONE TIER
  ════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────────────┐
  │  MICRO (500g, swarm):                                               │
  │  ├── Displayed as cluster/group, not individual markers             │
  │  ├── Commands sent to swarm leader (which relays to members)        │
  │  ├── Swarm status: count alive, formation health, centroid position │
  │  ├── Individual telemetry: only on click/expand                     │
  │  ├── MAVLink System IDs: 200-254 (high range, up to 55 per swarm)  │
  │  └── Missions: created for swarm as unit (pattern, not per-drone)   │
  ├─────────────────────────────────────────────────────────────────────┤
  │  MINI (5-15kg, multirole):                                          │
  │  ├── Full individual tracking and control                           │
  │  ├── All mission types supported                                    │
  │  ├── Video feed (single stream, EO or IR)                           │
  │  ├── Payload control (gimbal, cargo release)                        │
  │  ├── MAVLink System IDs: 1-50                                       │
  │  └── This is the primary drone class — most UI features built for it│
  ├─────────────────────────────────────────────────────────────────────┤
  │  MEDIUM (25-50kg, extended):                                         │
  │  ├── Full tracking + expanded payload control                        │
  │  ├── Multi-sensor payload management (EO + IR + LiDAR)              │
  │  ├── Longer missions — need power management display                │
  │  ├── Hybrid propulsion telemetry (fuel level, generator RPM)        │
  │  ├── MAVLink System IDs: 51-100                                      │
  │  └── Carrier operations: deploy/recall MINI drones from mothership  │
  ├─────────────────────────────────────────────────────────────────────┤
  │  LARGE (100-200kg, persistent):                                      │
  │  ├── Extended endurance display (12-48 hour timeline)                │
  │  ├── Relay link health (upstream/downstream link quality)            │
  │  ├── Solar power management (panel output, charge state)            │
  │  ├── Station-keeping fuel/power budget                              │
  │  ├── Constellation topology view (all relay nodes in chain)         │
  │  ├── MAVLink System IDs: 101-150                                     │
  │  └── Regulatory compliance dashboard (certified category)           │
  └─────────────────────────────────────────────────────────────────────┘

  PARAMETER PROFILES PER TIER:
  ════════════════════════════
  The GCS stores ArduPilot parameter templates per tier + airframe.
  When a new drone is registered, the appropriate template is loaded:

  params/
  ├── micro_default.param       # Conservative, small-drone limits
  ├── mini_skywalker_x8.param   # Current build
  ├── mini_generic.param
  ├── medium_hybrid.param
  ├── medium_electric.param
  ├── large_solar.param
  └── large_hybrid.param

  This matches the existing params/ directory in the project root.
```

---

## 11. Offline and Connectivity Handling

```
  OFFLINE CAPABILITY (critical for field operations)
  ═════════════════════════════════════════════════

  TIER 1 FIELD STATION — FULLY OFFLINE CAPABLE:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  MAP TILES:                                                 │
  │  ├── Pre-downloaded MBTiles files for operational area      │
  │  ├── Tool: download tiles from OpenStreetMap before deploy  │
  │  ├── Stored locally: ~500MB per 100km² at zoom 1-18        │
  │  └── MapLibre loads from local file, no internet needed     │
  │                                                             │
  │  TERRAIN DATA:                                              │
  │  ├── Pre-downloaded SRTM 30m elevation tiles                │
  │  ├── Stored locally: ~50MB per 1°×1° tile                   │
  │  └── Mission planner uses local terrain for AGL calculations│
  │                                                             │
  │  WEATHER:                                                   │
  │  ├── Manual entry (operator observes conditions)            │
  │  ├── On-device weather station via USB (optional)           │
  │  └── Cached forecast from last online sync                  │
  │                                                             │
  │  AIRSPACE DATA:                                             │
  │  ├── Pre-loaded no-fly zone database (updated weekly)       │
  │  ├── UK CAA airspace GeoJSON (open data)                    │
  │  └── Manual NOTAM entry                                     │
  │                                                             │
  │  SYNC ON RECONNECT:                                         │
  │  ├── When internet becomes available:                       │
  │  │   1. Upload completed flight logs to central database    │
  │  │   2. Download updated airspace data                      │
  │  │   3. Sync maintenance records                            │
  │  │   4. Pull latest weather forecast                        │
  │  └── Conflict resolution: last-write-wins with timestamps   │
  └─────────────────────────────────────────────────────────────┘
```

---

## 12. Performance Targets

```
  PERFORMANCE REQUIREMENTS
  ═══════════════════════

  ┌────────────────────────────────────────────────────────────────┐
  │  METRIC                        │  TARGET        │  TIER       │
  │────────────────────────────────┤────────────────┤─────────────│
  │  Telemetry display latency     │  < 100 ms      │  T1/T2/T3  │
  │  Map update rate               │  10 Hz         │  T1/T2/T3  │
  │  Video feed latency            │  < 200 ms      │  T1/T2     │
  │  Command round-trip            │  < 500 ms      │  T1/T2/T3  │
  │  Mission planning (goal→wpts)  │  < 2 seconds   │  T1/T2/T3  │
  │  Fleet dashboard refresh       │  2 Hz          │  T2/T3     │
  │  Simultaneous video streams    │  4             │  T2/T3     │
  │  Max concurrent drones (T2)    │  50            │  T2        │
  │  Max concurrent drones (T3)    │  200           │  T3        │
  │  Frontend bundle size          │  < 5 MB        │  T1        │
  │  RAM usage (T1 app)            │  < 500 MB      │  T1        │
  │  Database query (flight list)  │  < 100 ms      │  T2/T3     │
  │  Airbase state machine cycle   │  10 Hz         │  T3        │
  │  Failover time                 │  < 30 seconds  │  T3        │
  │  Uptime target                 │  99.9%         │  T3        │
  └────────────────────────────────────────────────────────────────┘
```

---

## Summary

This architecture delivers a single codebase that scales across three deployment tiers: a field laptop for single-drone operations, a multi-screen operations center for fleet management, and a fully automated airbase for 24/7 autonomous sortie generation.

The key design decisions are:

1. **Svelte + FastAPI** -- lightweight frontend and Python backend that directly imports the existing mission planning engine without rewrites.
2. **SQLite for field / PostgreSQL for operations** -- same SQLAlchemy models, different backends based on tier.
3. **WebSocket for telemetry, REST for CRUD** -- real-time where it matters, standard HTTP elsewhere.
4. **MAVProxy for multi-vehicle routing** -- proven in the ArduPilot ecosystem, handles the hard routing problem.
5. **GStreamer + WebRTC for video** -- low-latency path from camera to browser.
6. **State machine architecture for airbase automation** -- deterministic, testable, auditable cycle management.
7. **ArduPilot failsafes as the safety net** -- the GCS is never a single point of failure for flight safety.

Phase 1 (Field Station) is the immediate priority -- it provides the operator interface for the MINI tier Skywalker X8 currently under development. Phases 2 and 3 build on the same codebase as the fleet grows.
