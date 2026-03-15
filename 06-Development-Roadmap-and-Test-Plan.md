# Development Roadmap & Master Test Plan

## Multipurpose Mini-UAV Drone Platform

**Author:** Mohammed Ali Bhai
**Created:** 2026-03-15
**Location:** Surrey, UK
**Status:** PLANNING

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Phased Roadmap](#phased-roadmap)
3. [Test Plans per Phase](#test-plans-per-phase)
4. [Parallel Work Streams](#parallel-work-streams)
5. [Risk Register](#risk-register)
6. [Decision Log Template](#decision-log-template)

---

## Project Summary

**Objective:** Build a multipurpose fixed-wing UAV platform with hotswappable payloads and an intelligent mission planning engine, starting from zero flight experience.

**Approach:** Buy an off-the-shelf airframe (Skywalker class), install ArduPilot on Pixhawk, and incrementally add capabilities across 8 phases.

**End State:** A platform that can accept different payload modules (camera, cargo drop, sensors), plan missions autonomously given high-level goals, and execute them safely under ArduPilot control.

**Regulatory Framework:** UK CAA — Drone and Model Aircraft Registration, Flyer ID, and eventually Operational Authorisation for BVLOS if required.

---

## Phased Roadmap

---

### Phase 0: FOUNDATION (Software + Regulatory)

**Duration:** 3-4 weeks
**Estimated Cost:** GBP 12 (CAA registration only)

#### Prerequisites
- None. This is the starting point.

#### Deliverables
- ArduPilot SITL running on laptop (simulated ArduPlane)
- Mission Planning Engine Phase A — Python CLI that generates valid .waypoints files
- Successful autonomous mission in SITL (takeoff → waypoints → RTL)
- UK Flyer ID obtained (mandatory free online test via CAA)
- Operator ID registered (GBP 11.79/year)
- BMFA membership applied for (insurance + club access)
- ERFC or Caterham club contacted for site access

#### What to Set Up
| Item | Cost (GBP) | Notes |
|------|-----------|-------|
| ArduPilot SITL (sim_vehicle.py) | 0 | Open source, runs on any laptop |
| Python 3.11+ environment | 0 | pymavlink, pydantic, pytest |
| Mission Planner or QGroundControl | 0 | For mission visualization |
| UK Flyer ID (online test) | 0 | 40 questions, 30 minutes |
| UK Operator ID | 12 | Annual |
| BMFA membership | ~40 | Insurance + club access |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| SITL setup fails on macOS | Medium | Use Docker container or Linux VM. ArduPilot SITL has good macOS support via Homebrew. |
| MAVLink protocol complexity | Medium | Start with .waypoints file output (text), not live MAVLink. Add upload later. |
| No test site access | High | Contact ERFC and Caterham clubs early. BMFA membership is prerequisite for most sites. |

#### Skills Learned (enabling next phase)
- ArduPilot mission planning concepts (waypoints, commands, frames)
- MAVLink protocol basics (message types, mission upload)
- SITL simulation workflow (launch, upload, fly, verify)
- Python project structure for drone software
- QGC WPL 110 file format

#### Test Criteria — Phase 0 Complete When:
- [ ] SITL launches and displays simulated aircraft on map
- [ ] Mission engine CLI generates valid .waypoints file
- [ ] .waypoints file loads correctly in Mission Planner / QGC
- [ ] Mission uploads to SITL and executes (takeoff → waypoints → RTL)
- [ ] All unit tests pass (models, planner, writer)
- [ ] Golden file tests pass (3 fixture files)
- [ ] Hold valid UK Flyer ID and Operator ID
- [ ] BMFA membership active

---

### Phase 1: FIRST PLATFORM

**Duration:** 4-6 weeks
**Estimated Cost:** GBP 400-700

#### Prerequisites
- Phase 0 complete (SITL working, mission engine Phase A functional)
- UK Flyer ID and Operator ID active
- BMFA membership and club site access confirmed

#### Deliverables
- Skywalker-class airframe built and configured
- Pixhawk flight controller installed and calibrated
- ArduPilot firmware flashed and configured for manual + stabilised flight
- Telemetry radio link working (ground station can see live data)
- Successful maiden flight in MANUAL and FBWA (Fly-By-Wire A) modes
- Ground station software installed and configured (Mission Planner or QGroundControl)

#### What to Buy
| Item | Approx Cost (GBP) | Notes |
|------|-------------------|-------|
| Skywalker 1900 or X8 airframe | 80-130 | EPO foam, proven design, large payload bay |
| Pixhawk 6C or Pixhawk 4 Mini | 120-200 | Holybro recommended for first build |
| GPS module (M10 or M9N) | 30-50 | Holybro or mRo |
| Power module | 20-30 | Included with some Pixhawk kits |
| Telemetry radios (915 MHz pair) | 30-50 | SiK radios, Holybro or mRo |
| Servos (4x, metal gear) | 20-40 | Aileron x2, elevator, rudder |
| Motor + ESC + propeller | 40-70 | Appropriate for airframe (check Skywalker wiki) |
| LiPo batteries (4S 5000mAh x2) | 50-70 | |
| Misc (wiring, connectors, heatshrink, Velcro) | 20-40 | |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Incorrect CG placement causes crash on maiden | High | Use manufacturer's recommended CG. Verify with CG calculator. Do a glide test (hand toss with motor off at safe height) before powered flight. |
| ArduPilot configuration wrong (reversed servos, wrong PID) | High | Follow ArduPilot first-setup wiki exactly. Do ALL ground checks. Use MANUAL mode first. |
| Maiden flight crash destroys expensive electronics | High | Mount Pixhawk and GPS on vibration-dampened plate with foam. Use sacrificial nose. Keep electronics in centre of fuselage. |
| Telemetry link drops at range | Medium | Test telemetry range on ground first. Start with short-range flights (within 200m). |

#### Skills Learned
- ArduPilot configuration and parameter tuning
- Pixhawk wiring and integration
- Ground station software operation
- Telemetry interpretation (attitude, battery, GPS)
- Airframe construction and CG balancing

#### Test Criteria — Phase 1 Complete When:
- [ ] Airframe passes structural inspection (no flex, all surfaces move correctly)
- [ ] Pixhawk passes all pre-arm checks (gyro, accel, compass, GPS lock)
- [ ] Motor runs correct direction, ESC calibrated
- [ ] Telemetry link confirmed working at 500m+ range (ground test)
- [ ] Successful maiden flight in MANUAL mode (minimum 5 min)
- [ ] Successful flight in FBWA mode (stabilised, pilot still controlling)
- [ ] 3 consecutive flights without incident
- [ ] Ground station logs reviewed — no errors, good GPS, stable attitude

---

### Phase 2: AUTONOMOUS

**Duration:** 4-8 weeks
**Estimated Cost:** GBP 50-150 (mostly batteries and spares)

#### Prerequisites
- Phase 1 complete (stable platform flying in MANUAL and FBWA)
- Confident with ground station software
- Understanding of ArduPilot flight modes

#### Deliverables
- Waypoint missions planned and executed autonomously
- AUTO, RTL (Return to Launch), LOITER modes tested and reliable
- Geofence configured and tested
- Failsafe behaviours configured and tested (RC loss, battery low, GPS loss)
- Full telemetry logging and post-flight analysis workflow
- OSD (On-Screen Display) showing key flight data

#### What to Buy
| Item | Approx Cost (GBP) | Notes |
|------|-------------------|-------|
| Spare propellers, batteries | 30-50 | You will be flying a lot |
| Airspeed sensor (if not already fitted) | 15-25 | Critical for fixed-wing AUTO mode |
| OSD module (if Pixhawk doesn't include) | 10-20 | Optional but useful |
| MicroSD cards for logging | 10 | High-endurance cards |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Autonomous flight goes wrong, flyaway | Critical | ALWAYS configure geofence. Set RTL as default failsafe. Test RTL manually first before trusting AUTO. |
| Airspeed sensor failure causes stall in AUTO | High | Calibrate airspeed sensor on ground. Set ARSPD_USE = 1 only after ground validation. Configure minimum airspeed parameter. |
| Regulatory breach (flying BVLOS without authorisation) | High | Phase 2 should remain VLOS (Visual Line of Sight). Keep all waypoints within 500m and visual range. |
| Poor tuning causes oscillation in AUTO | Medium | Use ArduPilot AUTOTUNE mode. Fly in calm conditions. |

#### Skills Learned
- Mission planning (waypoints, actions, rally points)
- ArduPilot AUTO mode tuning
- Failsafe configuration
- Post-flight log analysis (using MAVExplorer or UAV Log Viewer)
- Geofencing and safety boundaries
- Regulatory awareness for autonomous operations

#### Test Criteria — Phase 2 Complete When:
- [ ] 3-waypoint mission executed and completed autonomously
- [ ] RTL tested from 3 different positions — aircraft returns and loiters correctly
- [ ] LOITER mode holds position within 50m radius
- [ ] Geofence triggers correctly (aircraft turns back at boundary)
- [ ] RC-loss failsafe tested (turn off TX — aircraft executes RTL)
- [ ] Battery failsafe tested (triggers RTL at configured voltage)
- [ ] 10-waypoint mission with altitude changes completed
- [ ] Post-flight logs show stable attitude, no EKF errors, good GPS throughout
- [ ] Airspeed sensor reads within 10% of GPS-derived groundspeed in calm conditions

---

### Phase 3: PAYLOAD INTERFACE

**Duration:** 6-10 weeks
**Estimated Cost:** GBP 100-300

#### Prerequisites
- Phase 2 complete (reliable autonomous flight)
- Basic CAD skills (learn Fusion 360 or OnShape — free for personal use)
- Basic understanding of electrical connectors and wiring

#### Deliverables
- Standardised payload bay with defined mechanical interface
- Electrical interface specification (power rails, data bus, servo/PWM channels)
- Quick-release mounting system (tool-free swap in under 2 minutes)
- CG management system (payload position adjustable or constrained to maintain CG)
- Weight budget document (max payload weight, CG envelope)
- First test with dummy payload (correct weight, no functionality)

#### Design Decisions Required
| Decision | Options | Considerations |
|----------|---------|----------------|
| Mounting method | Rails + latch, dovetail, magnetic + pin, Velcro (temporary) | Must be vibration-resistant, tool-free, repeatable positioning |
| Electrical connector | XT30 (power) + JST-GH (data), single multi-pin connector (e.g., Deutsch), custom PCB | Standardise early. Connector must handle vibration. Consider moisture. |
| Data interface to Pixhawk | MAVLink serial, PWM/servo channels, I2C, or companion computer relay | Serial/MAVLink gives most flexibility. PWM is simplest for servos. |
| Payload bay location | Under wing, belly pod, internal fuselage bay | Belly pod most common in Skywalker. CG impact must be calculated. |

#### What to Buy / Make
| Item | Approx Cost (GBP) | Notes |
|------|-------------------|-------|
| 3D printer filament (PETG) | 20-30 | For mounting brackets, rails |
| Connectors (XT30, JST-GH, or chosen standard) | 15-25 | Buy extras |
| Aluminium rail stock (if using rail system) | 10-20 | |
| 3D printing (if no printer — library or online service) | 20-50 | Or buy an Ender 3 for ~GBP 150 |
| Dummy payload weights | 5-10 | Lead shot, fishing weights |
| CG balance tool / jig | 10-15 | |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payload shifts in flight causing CG issue | Critical | Test with dummy weights in turbulence. Use positive locking mechanism, not friction-fit. Conduct CG check before every flight. |
| Connector fails in flight (vibration) | High | Use locking connectors. Strain-relief all cables. Vibration test on ground (run motor at full throttle for 60 sec, check connections). |
| Over-engineering the interface (scope creep) | Medium | Start with the simplest system that works. Version 1 does NOT need to be perfect. |
| Weight of interface eats into payload budget | Medium | Track weight budget rigorously. Aim for interface weight under 100g. |

#### Skills Learned
- Mechanical design and CAD
- 3D printing for functional parts
- Electrical connector standards
- CG management and weight budgeting
- Systems integration thinking

#### Test Criteria — Phase 3 Complete When:
- [ ] Payload bay accommodates a 500g dummy payload securely
- [ ] Payload can be swapped (removed and refitted) in under 2 minutes without tools
- [ ] CG remains within safe envelope with payload installed (verified by measurement)
- [ ] Electrical connector mates and de-mates cleanly 50 times without degradation
- [ ] Vibration test passed (motor at full throttle for 60 sec, payload does not shift)
- [ ] Flight test with dummy payload — aircraft handles normally in FBWA and AUTO
- [ ] Flight test with NO payload — aircraft handles normally (CG still safe with empty bay)
- [ ] Interface specification documented (drawing, pinout, weight limits)

---

### Phase 4: FIRST PAYLOAD — Camera/FPV Module

**Duration:** 4-6 weeks
**Estimated Cost:** GBP 100-250

#### Prerequisites
- Phase 3 complete (working payload interface)
- Understanding of video transmission basics

#### Deliverables
- Camera payload module that plugs into the standard interface
- Live FPV video feed to ground (analog or digital)
- Triggered still photo capability (servo-actuated or electronic)
- Recorded video (onboard SD card)
- Gimbal or fixed-mount camera with vibration isolation
- Ground station can view video feed

#### What to Buy
| Item | Approx Cost (GBP) | Notes |
|------|-------------------|-------|
| FPV camera (e.g., RunCam, Caddx) | 20-40 | Wide-angle, suitable for mapping or FPV |
| Video transmitter (5.8 GHz analog or DJI/HDZero digital) | 30-80 | Check UK power limits (25mW without license, 600mW with amateur license) |
| FPV goggles or monitor | 40-100 | Eachine EV800D (budget) or similar |
| Camera mount / small gimbal | 20-40 | 2-axis or fixed dampened mount |
| Recording module or camera with SD slot | 0-30 | Many FPV cameras record onboard |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Video interference / black-out at range | Medium | Test range on ground first. Use circular polarised antennas. Keep VTX antenna clear of carbon fibre. |
| Camera vibration causing jello effect | Medium | Use vibration-dampening mount (silicone grommets). Balance propeller. |
| Exceeding UK RF power limits | High | Stay at 25mW unless holding amateur radio license. Keep within VLOS so FPV is supplementary, not primary control. |
| Added weight/drag affects flight characteristics | Low | Camera module should be under 200g. Re-trim aircraft after installation. |

#### Skills Learned
- Video systems (analog vs digital FPV)
- RF basics and antenna selection
- Vibration isolation techniques
- Payload integration with flight controller
- Image/video quality assessment

#### Test Criteria — Phase 4 Complete When:
- [ ] Camera module plugs into payload bay using standard interface
- [ ] Swap time under 2 minutes (same as Phase 3 requirement)
- [ ] Clear video feed received on ground at 500m range
- [ ] Video recording captured onboard with usable quality (no jello, acceptable resolution)
- [ ] Still photo triggered remotely via TX switch or ground station command
- [ ] CG verified in-limits with camera module installed
- [ ] Full autonomous mission flown with camera recording — video reviewed post-flight
- [ ] No interference between video TX and telemetry/GPS

---

### Phase 5: MISSION ENGINE v1

**Duration:** 8-12 weeks (much of this done in parallel with Phases 1-4)
**Estimated Cost:** GBP 0-50 (software development)

#### Prerequisites
- Phase 2 complete (at minimum — to understand ArduPilot mission format)
- Python proficiency
- Understanding of MAVLink protocol
- ArduPilot SITL (Software In The Loop) installed and working

#### Deliverables
- Python-based mission planner that generates ArduPilot-compatible waypoint files
- Basic route planning: given start, end, and constraints (no-fly zones, altitude limits), output a waypoint mission
- Integration with ArduPilot via MAVLink (upload mission, start mission, monitor progress)
- SITL test suite that validates missions before real-world flight
- Map-based UI (even if basic — web map with Leaflet or similar)
- UK airspace data integration (at minimum, a static no-fly zone database)

#### Architecture
```
[User Input: start, end, constraints]
        |
        v
[Route Planner] ---> [Waypoint Generator] ---> [MAVLink Mission File]
        |                                              |
        v                                              v
[Constraint Checker]                          [ArduPilot SITL or Real FC]
  - No-fly zones                                       |
  - Max altitude                                       v
  - Battery range                              [Mission Execution]
  - Wind (future)                                      |
                                                       v
                                              [Telemetry Monitor]
```

#### Technology Choices
| Component | Recommended | Why |
|-----------|-------------|-----|
| Language | Python 3.10+ | MAVLink libraries, rapid prototyping, GIS libraries |
| MAVLink library | pymavlink or dronekit-python | Direct ArduPilot integration |
| SITL | ArduPilot SITL (native or Docker) | Free, accurate simulation |
| Mapping | Leaflet.js (web) or folium (Python) | Lightweight, open-source |
| Airspace data | OpenAIP or NATS drone assist API | UK airspace information |
| Persistence | SQLite or JSON files | Simple, no server needed |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Mission engine generates invalid/dangerous waypoints | Critical | ALWAYS validate in SITL before uploading to real aircraft. Build in hard limits (max altitude, max distance, geofence). |
| MAVLink integration unreliable | Medium | Use well-tested libraries (pymavlink). Start with file-based mission upload, then add real-time control later. |
| Scope creep (trying to build too much too soon) | High | v1 is a BASIC route planner. It generates a list of waypoints. Nothing more. No AI, no dynamic replanning. |
| Airspace data outdated or incorrect | High | Use official sources (NATS). Always cross-check with Drone Assist app before real flights. Never rely solely on the engine for airspace compliance. |

#### Skills Learned
- MAVLink protocol
- ArduPilot SITL development workflow
- GIS basics (coordinates, projections, distance calculations)
- Software architecture for safety-critical systems
- Test-driven development for robotics

#### Test Criteria — Phase 5 Complete When:
- [ ] Can generate a valid waypoint mission from start/end coordinates
- [ ] Mission respects altitude constraints (min/max)
- [ ] Mission avoids at least one defined no-fly zone (routes around it)
- [ ] Generated mission loads and executes successfully in ArduPilot SITL
- [ ] Mission uploads to real Pixhawk via MAVLink and executes correctly
- [ ] Route planner handles edge cases: start inside no-fly zone (error), destination unreachable (error), zero-length mission (error)
- [ ] Basic UI shows route on a map with waypoints
- [ ] 5 different missions generated, validated in SITL, and 2 flown on real aircraft

---

### Phase 6: ADDITIONAL PAYLOADS

**Duration:** 8-12 weeks
**Estimated Cost:** GBP 150-400

#### Prerequisites
- Phase 3 complete (payload interface)
- Phase 4 complete (proven the interface works with one payload)
- Phase 2 complete (autonomous flight for cargo drop testing)

#### Deliverables

**Payload A: Cargo Drop Module**
- Servo-actuated release mechanism
- Payload bay holds up to 500g cargo
- Triggered via TX switch or MAVLink command
- GPS-guided drop point in mission plan

**Payload B: Environmental Sensor Module**
- Temperature, humidity, pressure sensor package
- Data logged onboard (SD card) with GPS timestamp
- Optional: live telemetry of sensor data to ground station
- Post-flight data export (CSV)

#### What to Buy
| Item | Approx Cost (GBP) | Notes |
|------|-------------------|-------|
| High-torque servo for cargo release | 10-20 | Metal gear, reliable |
| 3D printed cargo bay / release mechanism | 10-20 | PETG or nylon |
| BME280 sensor breakout (temp/humidity/pressure) | 5-10 | I2C interface |
| Arduino Nano or Raspberry Pi Pico | 5-10 | Onboard data logger for sensor payload |
| MicroSD breakout for logging | 5-10 | |
| Misc (wiring, enclosures, fasteners) | 20-40 | |

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Cargo release fails (doesn't open or opens prematurely) | High | Extensive ground testing. Use a positive-lock mechanism (servo must actively hold closed). Test with vibration. |
| Dropped cargo hits person/property | Critical | Only test cargo drop over open, unpopulated areas. Start with lightweight dummy cargo (soft ball). Use a spotter. |
| Sensor data corrupted or not logging | Medium | Test logging on bench for hours before flight. Use checksums. Verify data post-flight on first flight. |
| Each new payload requires re-tuning aircraft | Medium | Standardise payload weight. Use consistent CG position. Tune PID for mid-weight payload. |

#### Skills Learned
- Servo control and mechanical actuation
- Embedded systems (Arduino/Pico programming)
- Sensor data acquisition and logging
- Multi-payload operations
- Drop-point accuracy and timing

#### Test Criteria — Phase 6 Complete When:

**Cargo Drop:**
- [ ] Release mechanism actuates reliably 20/20 times on ground test
- [ ] Mechanism holds 500g payload through full-throttle vibration test
- [ ] Cargo drop executed from 50m altitude — cargo lands within 20m of target
- [ ] Cargo drop triggered via MAVLink command during autonomous mission
- [ ] 5 successful drop tests with no mechanism failures

**Sensor Module:**
- [ ] Sensor logs temperature, humidity, pressure at 1 Hz for 30 min on bench
- [ ] Data includes GPS coordinates and timestamp
- [ ] Data exports cleanly to CSV
- [ ] Flight test: data shows expected altitude-based pressure variation
- [ ] No data gaps or corruption in 3 consecutive flight tests

---

### Phase 7: MISSION ENGINE v2

**Duration:** 12-20 weeks
**Estimated Cost:** GBP 0-100 (software development)

#### Prerequisites
- Phase 5 complete (v1 working)
- Phase 6 complete (multiple payload types available)
- Significant flight experience from all previous phases

#### Deliverables
- Goal-based mission input: "Survey this area" or "Deliver to this location" rather than manually specifying waypoints
- Constraint engine: battery endurance, wind, payload weight, airspace, daylight hours
- Mission templates: survey pattern, delivery route, search pattern
- Payload-aware planning: mission type selects appropriate payload and adjusts parameters
- Pre-flight risk assessment: engine evaluates weather, airspace, battery state and gives go/no-go
- Post-mission reporting: automated flight report with map, telemetry summary, payload data

#### Architecture
```
[Goal Input: "Survey field X at 80m AGL, 70% overlap"]
        |
        v
[Goal Interpreter] --> selects mission template (lawnmower survey)
        |
        v
[Constraint Engine]
  - Battery: enough for mission + 20% reserve + RTL?
  - Airspace: all waypoints in legal airspace?
  - Weather: wind within limits? Daylight sufficient?
  - Payload: camera module required — is it installed?
        |
        v
[Route Optimiser]
  - Minimise distance / energy
  - Respect turn radius
  - Optimise for wind (fly upwind legs first)
        |
        v
[Mission Generator] --> MAVLink waypoints + payload commands
        |
        v
[SITL Validation] --> automated pass/fail
        |
        v
[Upload to Aircraft] or [Reject with reasons]
```

#### Key Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
| Constraint engine has bugs, approves unsafe mission | Critical | Defence in depth: ArduPilot geofence is always the last line of defence, independent of mission engine. Manual review step before every real flight. |
| Over-engineering / never finishing | High | Define MVP for v2 clearly. Ship when 3 mission templates work end-to-end. Iterate. |
| Weather data integration unreliable | Medium | Use conservative defaults. If weather API unavailable, require manual input. |
| Goal interpreter misunderstands intent | Medium | Start with structured input (forms/menus), not natural language. |

#### Skills Learned
- Constraint satisfaction and optimisation
- Path planning algorithms
- Systems-level software architecture
- Risk modelling
- Automated testing for safety-critical software

#### Test Criteria — Phase 7 Complete When:
- [ ] "Survey area" goal generates correct lawnmower pattern
- [ ] "Deliver to point" goal generates route avoiding no-fly zones
- [ ] Constraint engine correctly rejects mission when battery insufficient
- [ ] Constraint engine correctly rejects mission when route crosses no-fly zone
- [ ] Wind-aware routing demonstrably produces shorter flight times in SITL with simulated wind
- [ ] 3 mission templates work end-to-end (survey, delivery, search)
- [ ] Pre-flight risk assessment catches at least 5 defined hazard scenarios
- [ ] Automated SITL validation catches an intentionally invalid mission
- [ ] 3 real-world missions planned by v2 engine, validated in SITL, and flown successfully

---

## Test Plans per Phase

### Universal Safety Procedures

#### Pre-Flight Checklist (ALL PHASES)

```
STRUCTURAL
[ ] Airframe inspected — no cracks, delamination, loose parts
[ ] All control surfaces move freely, correct direction, full range
[ ] Propeller secure, no chips or cracks, balanced
[ ] Motor mount secure
[ ] Battery secured with Velcro + strap (cannot shift)
[ ] CG verified (balance point within marked range)
[ ] Payload secured (if installed) — tug test passed
[ ] All hatches and covers closed and latched

ELECTRONICS
[ ] Battery voltage correct (fully charged: 4.2V/cell = 16.8V for 4S)
[ ] Pixhawk boots cleanly — no persistent error tones
[ ] GPS lock obtained (minimum 8 satellites, HDOP < 2.0)
[ ] Compass calibration current (no large mag interference)
[ ] Telemetry link active — ground station receiving data
[ ] RC link active — all channels responding
[ ] Failsafe configured: RC loss = RTL, battery low = RTL
[ ] Flight mode switch verified — correct modes on each position
[ ] Airspeed sensor reading (if fitted) — should read near zero on ground

CONTROLS
[ ] Ailerons: TX stick right = right aileron UP, left aileron DOWN
[ ] Elevator: TX stick back = elevator UP
[ ] Rudder: TX stick right = rudder RIGHT
[ ] Throttle: TX stick forward = motor spins faster
[ ] In FBWA mode: tilt aircraft right = left aileron UP (correcting)
[ ] Kill switch / motor disarm tested

ENVIRONMENT
[ ] Wind: measured or estimated, within aircraft limits (< 20 mph for early phases)
[ ] Weather: no rain, no thunderstorms within 30 miles
[ ] Temperature: LiPo batteries above 10 degrees C
[ ] Flying site: clear of people, animals, buildings within safety zone
[ ] Airspace: confirmed legal to fly (Drone Assist app checked)
[ ] NOTAMs checked for area
[ ] Spotter briefed (if using one)

GO / NO-GO DECISION
[ ] All above items checked
[ ] Pilot feels alert and confident
[ ] Emergency plan briefed: if loss of control, cut throttle, let it glide down
```

#### In-Flight Monitoring

```
CONTINUOUS MONITORING
- Battery voltage (land immediately if cell voltage drops below 3.5V)
- GPS satellite count (abort mission if drops below 6)
- Telemetry link (if lost, continue visually, shorten mission)
- Aircraft attitude (any unusual oscillation = land immediately)
- Airspeed (if reading zero in flight, switch to MANUAL and land)
- Distance from pilot (maintain VLOS at all times in Phases 0-4)

ABORT CRITERIA (land immediately if any occur)
- Battery cell voltage below 3.3V
- Unusual vibration or sound
- Control surface not responding
- GPS lock lost
- EKF error on ground station
- Unexpected weather change (sudden wind increase, approaching rain)
- Any person or animal enters the flying area
```

#### Post-Flight Checklist

```
IMMEDIATE
[ ] Aircraft inspected for damage
[ ] Battery voltage recorded
[ ] Flight time logged
[ ] Any anomalies noted
[ ] Propeller inspected for damage

DATA
[ ] Flight log downloaded from Pixhawk
[ ] Telemetry log saved from ground station
[ ] Payload data retrieved (if applicable)
[ ] Log reviewed for: EKF health, vibration levels, battery performance, GPS quality

MAINTENANCE
[ ] Battery stored at storage voltage (3.8V/cell) if not flying again today
[ ] Propeller replaced if any damage noted
[ ] Airframe cleaned if muddy/wet
[ ] Issues logged in maintenance log
```

---

### Phase-Specific Test Plans

#### Phase 0 Test Plan: LEARN

| Test | Type | Pass Criteria |
|------|------|---------------|
| TX range check | Ground | TX connects to RX at 100m with no dropouts |
| Control direction check | Ground | All surfaces move correct direction |
| Hand launch | Flight | Aircraft climbs away cleanly, no stall |
| Straight and level | Flight | Maintain heading +/- 20 degrees for 200m |
| Turns | Flight | Complete 360-degree turn in each direction without altitude loss > 10m |
| Landing approach | Flight | Aircraft touches down within 20m of target, no damage |
| Stall recovery | Flight | At altitude, reduce throttle until stall. Recover by lowering nose and adding throttle. Altitude loss < 30m. |
| Wind handling | Flight | Fly circuits in 10-15 mph wind. Maintain control throughout. |
| Emergency throttle cut | Flight | Cut throttle at altitude. Aircraft glides. Pilot lands without power. |

#### Phase 1 Test Plan: FIRST PLATFORM

| Test | Type | Pass Criteria |
|------|------|---------------|
| Pixhawk power-on | Ground | Clean boot, no error tones, LEDs show correct state |
| Accelerometer calibration | Ground | ArduPilot reports calibration successful |
| Compass calibration | Ground | No compass-motor interference above threshold |
| GPS lock | Ground | 3D fix with 8+ satellites within 2 minutes |
| Servo direction and range | Ground | All surfaces move correct direction and reach full deflection |
| Motor spin test | Ground | Motor spins correct direction, ESC calibrated |
| Telemetry link test | Ground | Ground station receives data at 500m |
| Glide test | Flight | Hand toss without motor — aircraft glides nose-slightly-down. If nose pitches up or down sharply, adjust CG. |
| Maiden flight — MANUAL | Flight | 5-minute flight, all controls responsive, no oscillation |
| Flight — FBWA mode | Flight | Switch to FBWA in flight. Aircraft self-levels when sticks centred. Pilot can still steer. |
| Vibration check | Post-flight | Review logs — vibration levels within ArduPilot acceptable range (accel clipping < 100 in 10 min) |

#### Phase 2 Test Plan: AUTONOMOUS

| Test | Type | Pass Criteria |
|------|------|---------------|
| Mission upload | Ground | 10-waypoint mission uploads to Pixhawk via MAVLink in < 30 sec |
| Geofence upload | Ground | Geofence polygon loaded, verified on ground station map |
| RTL test | Flight | Switch to RTL from 300m away. Aircraft returns and loiters over home point within 50m. |
| LOITER test | Flight | Switch to LOITER. Aircraft circles within 50m radius for 2 minutes. |
| AUTO mission (3 waypoints) | Flight | Aircraft follows 3-waypoint route. Cross-track error < 20m at each waypoint. |
| AUTO mission (10 waypoints) | Flight | Complex route completed. All waypoints reached. |
| Geofence breach test | Flight | Fly toward geofence boundary. Aircraft turns back before crossing. |
| RC loss failsafe | Flight | Turn off TX. Aircraft enters RTL within 5 seconds. Turn TX back on, regain control. |
| Battery failsafe | Flight | Wait for battery to reach failsafe voltage. Verify RTL triggers. (Only if safe to test — can also verify in logs from normal flights.) |
| Airspeed sensor validation | Flight | Compare airspeed sensor reading with GPS-derived groundspeed in calm conditions. Delta < 15%. |

#### Phase 3 Test Plan: PAYLOAD INTERFACE

| Test | Type | Pass Criteria |
|------|------|---------------|
| Mechanical fit test | Ground | Payload module clicks into bay. Secure. No play or rattle when shaken. |
| Swap time test | Ground | Remove and re-install payload in under 2 minutes, 5 consecutive times. |
| Electrical connectivity | Ground | Power and data connections verified with multimeter and test script. |
| Vibration test | Ground | Motor at full throttle for 60 sec. Payload does not shift. Connectors remain seated. |
| CG test — with payload | Ground | CG measured within safe range with 500g dummy payload. |
| CG test — without payload | Ground | CG measured within safe range with empty bay. |
| Flight test — dummy payload | Flight | 10-minute flight in FBWA and AUTO with dummy payload. Normal handling. |
| Flight test — empty bay | Flight | Flight immediately after removing payload. No handling issues. |
| Connector durability | Ground | Mate/de-mate connector 50 times. Inspect for wear. Test electrical continuity. |

#### Phase 4 Test Plan: CAMERA/FPV

| Test | Type | Pass Criteria |
|------|------|---------------|
| Camera module fit | Ground | Plugs into payload bay. Swap under 2 min. |
| Video link range test | Ground | Walk 500m from aircraft with motor running. Clear video throughout. |
| Video interference test | Ground | Telemetry and GPS unaffected when VTX powered on. |
| Vibration test (video quality) | Ground | Record video with motor at cruise throttle. No jello or rolling shutter artefacts. |
| Photo trigger | Ground | Trigger still photo via TX switch. Verify image captured. |
| Flight test — video quality | Flight | Record full flight. Review video — stable, clear, usable. |
| Flight test — photo trigger in AUTO | Flight | Pre-program photo triggers at waypoints. Verify photos captured at correct locations (check GPS in EXIF). |

#### Phase 5 Test Plan: MISSION ENGINE v1

| Test | Type | Pass Criteria |
|------|------|---------------|
| Unit tests | Software | All unit tests pass (route calculation, no-fly zone avoidance, distance checks). |
| SITL end-to-end test | Software | Generated mission loads in SITL, aircraft flies route, completes mission without error. |
| No-fly zone avoidance | Software | Route correctly avoids a defined no-fly zone. Verified visually on map. |
| Invalid input handling | Software | Engine returns appropriate errors for: no GPS coordinates, start in no-fly zone, destination beyond range. |
| Mission upload to real Pixhawk | Ground | Generated mission uploads via MAVLink. Waypoints verified on ground station. |
| Real flight from engine-generated mission | Flight | Aircraft follows engine-generated mission. Completes successfully. |
| Performance benchmark | Software | Mission generation completes in under 5 seconds for any valid input. |

#### Phase 6 Test Plan: CARGO DROP & SENSORS

| Test | Type | Pass Criteria |
|------|------|---------------|
| Cargo release — bench test | Ground | 20/20 successful releases. No jams. |
| Cargo hold — vibration test | Ground | 500g cargo remains locked through full-throttle vibration test. |
| Cargo drop — flight test | Flight | Drop from 50m AGL. Cargo lands within 20m of GPS target. |
| Cargo drop — MAVLink trigger | Flight | Drop triggered via mission command (DO_SET_SERVO) during AUTO flight. |
| Sensor logging — bench test | Ground | 30 min continuous logging at 1 Hz. No data gaps. Data valid. |
| Sensor — flight test | Flight | Pressure data shows altitude variation matching Pixhawk barometer (within 5%). Temperature data plausible. |
| Sensor data export | Post-flight | CSV export opens cleanly in Excel/Python. All fields populated. GPS coordinates valid. |

#### Phase 7 Test Plan: MISSION ENGINE v2

| Test | Type | Pass Criteria |
|------|------|---------------|
| Survey pattern generation | Software | "Survey area X" produces correct lawnmower pattern with specified overlap. Validated visually. |
| Delivery route generation | Software | "Deliver to Y" produces route avoiding all no-fly zones. Fuel/battery sufficient. |
| Battery constraint | Software | Engine rejects mission when calculated endurance exceeds battery capacity. |
| Airspace constraint | Software | Engine rejects or re-routes when flight path crosses restricted airspace. |
| Wind-aware routing | SITL | With simulated 20 km/h wind, engine produces route with upwind legs first. Total flight time shorter than naive routing. |
| Pre-flight risk assessment | Software | Engine evaluates 5 hazard scenarios and gives correct go/no-go for each. |
| End-to-end: survey mission | Flight | Survey mission planned by v2, validated in SITL, flown on real aircraft. Camera captures images with correct coverage. |
| End-to-end: delivery mission | Flight | Delivery mission planned by v2. Cargo dropped successfully at target. |

---

## Parallel Work Streams

### What Can Be Done Simultaneously

```
Timeline (weeks):
0         8         16        24        32        40        48        56        64

Phase 0: LEARN
|========|
          Phase 1: FIRST PLATFORM
          |==========|
                      Phase 2: AUTONOMOUS
                      |==============|
                                      Phase 3: PAYLOAD INTERFACE
                                      |==============|
                                                      Phase 4: CAMERA
                                                      |========|
                                                                Phase 6: PAYLOADS
                                                                |==============|

PARALLEL STREAMS:

Software (SITL):
     |--- Learn Python/MAVLink ---|--- Phase 5: Mission Engine v1 ---|--- Phase 7: v2 ---------|
     (start week 4)               (start week 16)                     (start week 40)

CAD/Payload Design:
               |--- Learn Fusion 360 ---|--- Design payload interface ---|--- Design payloads --|
               (start week 8)            (start week 16, feed into Ph3)   (start week 28)

Regulatory:
|--- Flyer ID + Operator ID ---|--- Research BVLOS requirements ---|--- Apply if needed ---|
(immediate)                     (start week 12)                      (start week 30)

3D Printing Skills:
          |--- Learn 3D printing ---|--- Print test brackets ---|--- Print payload parts ----|
          (start week 8)             (ongoing)                    (Phase 3 onwards)
```

### Stream Details

#### Stream A: Software Development (parallel from Week 4)
- **Week 4-8:** Learn Python, install ArduPilot SITL, run first simulated flight
- **Week 8-16:** Learn pymavlink, write first mission uploader, experiment with SITL
- **Week 16-32:** Build Mission Engine v1 (Phase 5) — can proceed entirely in SITL without real aircraft
- **Week 32-40:** Integrate v1 with real aircraft (requires Phase 2 complete)
- **Week 40+:** Mission Engine v2 (Phase 7) — mostly SITL, periodic real-world validation

#### Stream B: CAD and Mechanical Design (parallel from Week 8)
- **Week 8-12:** Learn Fusion 360 (free tutorials, design simple objects)
- **Week 12-20:** Design payload interface (can start before Phase 3 begins)
- **Week 20-28:** Iterate on payload interface design based on test results
- **Week 28+:** Design specific payload modules (cargo drop mechanism, sensor enclosure)

#### Stream C: Regulatory Compliance (parallel from Week 0)
- **Immediate:** Obtain Flyer ID and Operator ID
- **Week 12-20:** Research UK CAA requirements for various flight types
- **Week 20-30:** Determine if Operational Authorisation needed for intended operations
- **Week 30+:** Apply for any necessary permissions (Article 16 exemptions, operational authorisations)

**Key UK Regulatory Milestones:**
| Requirement | When Needed | How to Obtain |
|-------------|-------------|---------------|
| Flyer ID | Before any flight | Free online test on CAA website |
| Operator ID | Before any flight | Register online, GBP 10.33/year |
| A2 CofC (Certificate of Competency) | If flying near people (< 50m in reduced distance mode) | Online course + exam, ~GBP 150-250 |
| Operational Authorisation | For BVLOS, flights over 120m AGL, flights in restricted airspace | Application to CAA, demonstrations required |
| PfCO equivalent / GVC | For commercial operations | Training course, ~GBP 1000-1500 |

#### Stream D: Knowledge Building (continuous)
- ArduPilot documentation and forums
- RCGroups.com Skywalker threads
- MAVLink protocol documentation
- UK drone regulations (CAA CAP 722)
- Join a local BMFA club for mentorship and flying site access

---

## Risk Register

### Top 10 Project Risks

| # | Risk | Category | Likelihood | Impact | Score | Mitigation | Owner |
|---|------|----------|------------|--------|-------|------------|-------|
| R1 | Crash destroys airframe and electronics during early flights | Technical | High | High | **Critical** | Budget for 2 airframes. Protect electronics with foam. Start with cheap trainer. Keep Pixhawk separate from trainer. | Builder |
| R2 | Unable to find suitable flying site in Surrey | Operational | Medium | High | **High** | Research BMFA clubs before buying. Epsom & Ewell MFC, Farnborough clubs, Surrey Model Flyers. Backup: travel to open areas (Salisbury Plain perimeter, Sussex Downs). | Builder |
| R3 | UK regulations prevent intended operations (BVLOS, cargo drop) | Regulatory | Medium | High | **High** | Start within Open Category limits. Research Specific Category requirements early (parallel stream). Join a drone industry group for regulatory updates. Design all operations to work within VLOS first. | Builder |
| R4 | Scope creep — project grows beyond personal capacity | Scope | High | Medium | **High** | Strict phase gates. Each phase must be "done" before next begins (except designated parallel streams). Minimum viable version of everything. Re-evaluate scope quarterly. | Builder |
| R5 | Budget overrun — cumulative spending exceeds comfort zone | Budget | Medium | Medium | **Medium** | Track all spending. Set hard budget cap per phase. Buy incrementally — don't purchase Phase 3 parts until Phase 2 is complete. Total project budget target: GBP 1000-2000. | Builder |
| R6 | ArduPilot configuration errors cause flyaway or crash | Technical | Medium | High | **High** | Follow ArduPilot wiki step-by-step. ALWAYS configure geofence and RTL failsafe before first autonomous flight. Test every mode on the ground first. Join ArduPilot Discord for support. | Builder |
| R7 | Payload interface doesn't work reliably (vibration, disconnects) | Technical | Medium | Medium | **Medium** | Prototype early and test on the ground extensively. Use locking connectors. Design for worst-case vibration. Accept that v1 interface may need redesign. | Builder |
| R8 | Losing interest or motivation (project takes 12+ months) | Personal | Medium | High | **High** | Each phase delivers something flyable/usable. Celebrate milestones. Document progress (blog, video). Join communities for accountability. Don't set unrealistic deadlines. | Builder |
| R9 | Knowledge gaps in electronics/software block progress | Knowledge | Medium | Medium | **Medium** | Identify skill gaps early and learn in parallel streams. Use ArduPilot community for help. Don't try to learn everything before starting — learn by doing. | Builder |
| R10 | Injury or property damage from drone | Safety | Low | Critical | **High** | ALWAYS follow pre-flight checklist. Fly in open areas away from people. Never fly over people or roads. Keep a first aid kit at flying site. Have third-party liability insurance (BMFA membership includes this). | Builder |

### Risk Response Quick Reference

**If a crash occurs:**
1. Assess damage. Photograph everything before disassembly.
2. Download flight logs before disconnecting battery.
3. Analyse logs to determine root cause.
4. Document in decision log: what happened, why, how to prevent recurrence.
5. Fix or rebuild. Do not fly again until root cause is understood.

**If regulatory issues arise:**
1. Stop all flights immediately if any doubt about legality.
2. Contact CAA drone team for clarification.
3. Join BMFA for insurance and regulatory guidance.
4. Adjust project scope to fit within available permissions.

**If budget is exceeded:**
1. Pause purchasing. Fly what you have.
2. Re-evaluate remaining phases — which can be deferred?
3. Consider whether some components can be salvaged from other sources.

---

## Decision Log Template

### How to Use This Log
Record every significant decision that shapes the project. When you wonder "why did I choose X?" six months from now, this log provides the answer.

### Decision Log

| ID | Date | Decision | Options Considered | Rationale | Status | Phase |
|----|------|----------|-------------------|-----------|--------|-------|
| D001 | YYYY-MM-DD | [Brief description of decision] | 1. Option A: [description] 2. Option B: [description] 3. Option C: [description] | [Why this option was chosen. What factors mattered most.] | [ACTIVE / SUPERSEDED / REVERSED] | [Phase #] |
| D002 | | | | | | |

### Example Entries

| ID | Date | Decision | Options Considered | Rationale | Status | Phase |
|----|------|----------|-------------------|-----------|--------|-------|
| D001 | 2026-03-20 | Chose Skywalker 1900 as first platform airframe | 1. Skywalker 1900 (GBP 90) 2. X-UAV Talon (GBP 120) 3. RMRC Anaconda (GBP 200) | Skywalker 1900 has largest user community, most ArduPilot documentation, proven payload bay, and lowest cost. Wingspan (1.9m) is manageable for transport. Community support reduces risk of Phase 1 failure. | ACTIVE | 1 |
| D002 | 2026-03-20 | Selected Pixhawk 6C as flight controller | 1. Pixhawk 6C (GBP 150) 2. Pixhawk 4 Mini (GBP 120) 3. Matek H743 (GBP 60) 4. CubeOrange (GBP 250) | Pixhawk 6C is latest standard, well-supported by ArduPilot, includes power module. Not the cheapest, but best documentation and community support for first-time builder. Matek is cheaper but less beginner-friendly. Cube is overkill. | ACTIVE | 1 |
| D003 | 2026-04-01 | Chose ELRS for RC link protocol | 1. ELRS (open source, GBP 15-30 for RX) 2. FrSky ACCESS (GBP 25-40 for RX) 3. Crossfire (GBP 50-70 for RX) | ELRS offers best range per GBP, open source, large community. 2.4 GHz version sufficient for VLOS operations. Can upgrade to 900 MHz later if needed for range. | ACTIVE | 0 |

### Categories for Decision Tracking
- **AIRFRAME** — Airframe selection, modifications
- **ELECTRONICS** — Flight controller, sensors, radio, ESC
- **SOFTWARE** — Firmware choices, ground station, mission engine
- **PAYLOAD** — Interface design, payload module choices
- **REGULATORY** — Compliance decisions, operational limits
- **PROCESS** — How to test, what order to build, methodology

---

## Appendix: Cumulative Budget Estimate

| Phase | Low Estimate (GBP) | High Estimate (GBP) | Cumulative Low | Cumulative High |
|-------|--------------------|--------------------|----------------|-----------------|
| 0: Learn | 150 | 350 | 150 | 350 |
| 1: First Platform | 400 | 700 | 550 | 1,050 |
| 2: Autonomous | 50 | 150 | 600 | 1,200 |
| 3: Payload Interface | 100 | 300 | 700 | 1,500 |
| 4: Camera/FPV | 100 | 250 | 800 | 1,750 |
| 5: Mission Engine v1 | 0 | 50 | 800 | 1,800 |
| 6: Additional Payloads | 150 | 400 | 950 | 2,200 |
| 7: Mission Engine v2 | 0 | 100 | 950 | 2,300 |
| **TOTAL** | **950** | **2,300** | | |

**Note:** Does not include a 3D printer (GBP 150-200 for Ender 3 if purchased), BMFA membership (GBP 39/year), or A2 CofC training (GBP 150-250). Add GBP 200-500 for contingency/crash replacement.

---

## Appendix: Key Resources

| Resource | URL | Use |
|----------|-----|-----|
| ArduPilot Plane Documentation | ardupilot.org/plane | Primary reference for all ArduPilot configuration |
| ArduPilot SITL Setup | ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html | Setting up simulation environment |
| Mission Planner | ardupilot.org/planner | Ground station software (Windows) |
| QGroundControl | qgroundcontrol.com | Ground station software (cross-platform) |
| MAVLink Developer Guide | mavlink.io/en | MAVLink protocol reference |
| pymavlink | github.com/ArduPilot/pymavlink | Python MAVLink library |
| UK CAA Drone Code | caa.co.uk/drones | UK regulations |
| NATS Drone Assist | nats.aero/airspace-explorer | Airspace checking |
| BMFA | bmfa.org | UK model flying association — insurance and club access |
| RCGroups Skywalker Thread | rcgroups.com | Community knowledge for airframe builds |
| OpenAIP | openaip.net | Open airspace data |

---

*This document is a living plan. Update it as decisions are made, phases are completed, and lessons are learned. Review the risk register monthly. Update the decision log with every significant choice.*
