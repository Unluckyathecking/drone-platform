# Development and Funding Roadmap: From Bedroom to National Infrastructure

## Multipurpose Autonomous Drone Platform — Full Lifecycle Plan

**Author:** Mohammed Ali Bhai
**Created:** 2026-03-26
**Status:** ACTIVE — Phase 0 in progress
**Document scope:** 10-year roadmap integrating all 34+ research documents

---

## TABLE OF CONTENTS

1. Where You Stand Today
2. Phase 0: Foundation (Now — Summer 2026)
3. Phase 1: First Flight (Summer 2026)
4. Phase 2: Demonstrate and Compete (2026-2027)
5. Phase 3: University Years (2027-2030)
6. Phase 4: Startup Scale (2030-2032)
7. Phase 5: Infrastructure Build (2032-2035)
8. Phase 6: National Network (2035+)
9. Funding Sources — Detailed Timeline
10. Milestone Map
11. Risk Register
12. Key Decision Points
13. Honest Assessment

---

## 1. WHERE YOU STAND TODAY (March 2026)

### Assets In Hand

```
SOFTWARE
  Mission Planning Engine (Phase A)
    src/mpe/models.py ........... Pydantic data models (Mission, MissionItem, Waypoint)
    src/mpe/planner.py .......... Basic waypoint route planner
    src/mpe/writer.py ........... QGC WPL 110 file writer
    src/mpe/cli.py .............. Command-line interface
    tests/ ...................... 43 passing tests (models, planner, writer, CLI)
    pyproject.toml .............. Packaged, installable

  ArduPilot SITL
    install-sitl.sh ............. Setup script exists
    sitl/ ....................... Simulation directory present

HARDWARE DESIGNS
  payload-cad/
    Dovetail rail + quick-release pin interface (Fusion 360 / parametric)
    200mm x 300mm x 150mm payload bay, 4kg max
    Anderson PowerPole + JST-GH 8-pin electrical interface
    Auto-detection via ID pins

RESEARCH (160+ pages across 34 documents)
  Core:         Platform overview, specs, physics, mission engine architecture
  Payloads:     6 deep-dive sensor docs (cameras, thermal, LiDAR)
  Military:     Loitering munitions, counter-UAS, swarm, naval ASW, radar
  Civil:        Pest control, conservation, maritime, agricultural
  Platform:     4-tier family (MICRO/MINI/MEDIUM/LARGE), tileable microdrone
  Comms:        Mesh network, directional antenna tracking, FSO laser
  Infrastructure: Automated bases, ground stations, in-flight power transfer
  Regulatory:   UK CAA rules, international strategy (14 countries analysed)
  Vision:       Stratospheric platforms, aerial command bases, unified airship network

REGULATORY
  UK CAA framework fully researched
  International regulatory strategy for 14+ countries documented
  BVLOS pathway mapped (PDRA01 -> UK SORA -> full authorisation)
  Dual UK/Canadian citizenship — strategic asset for international PoC
    (Canada has routine BVLOS since Nov 2025, no barriers to entry)

GIT REPOSITORY
  Version-controlled, commit history showing sustained development
```

### What You Do NOT Have Yet

```
  [ ] CAA Flyer ID + Operator ID (not yet obtained)
  [ ] BMFA membership (not yet applied)
  [ ] Physical airframe (not yet purchased)
  [ ] Any real-world flight experience
  [ ] Revenue, customers, or team members
  [ ] Company registration
  [ ] External funding
```

---

## 2. PHASE 0: FOUNDATION (Now — Summer 2026)

**Duration:** ~14 weeks (March — June 2026)
**Budget:** £0-100
**Status:** IN PROGRESS

### The Logic

Everything in this phase costs nothing or almost nothing. This is the phase where you build intellectual property, regulatory readiness, and community before spending a penny on hardware. Every hour invested here compounds — software written now flies on every future aircraft.

### Workstreams

```
WORKSTREAM A: SOFTWARE (ongoing, 10-15 hrs/week)
==================================================

  A1. Mission Engine Phase B Planning               Weeks 1-4
      - Design Goal/ConstraintSet hierarchy (doc 07)
      - Spec out SAR search patterns (expanding square, sector, parallel track)
      - Spec out ISR loiter/orbit patterns
      - Spec out delivery corridor planning
      Deliverable: Phase B architecture document + data model diagrams

  A2. SITL Automated Test Harness                   Weeks 2-6
      - Script: launch SITL -> upload mission -> monitor MISSION_ITEM_REACHED
      - Assert mission completion, log telemetry
      - Run as CI check on every commit
      Deliverable: E2E test passing in GitHub Actions

  A3. Waypoint File Parser                          Weeks 3-5
      - Read .waypoints -> Mission objects (inverse of writer)
      - Enables roundtrip testing + QGC/Mission Planner import
      Deliverable: Parser + roundtrip golden-file tests

  A4. SAR Planner Implementation                    Weeks 5-10
      - Expanding square search from last-known-position
      - Parallel track search over defined area
      - Sector search for small areas
      Deliverable: SAR planner with SITL demonstration video

  A5. ISR/Loiter Planner                            Weeks 8-12
      - Orbit patterns (circular, racetrack, figure-8)
      - Timed loiter with configurable duration
      - Multi-point surveillance route
      Deliverable: ISR planner with SITL demo

  A6. Open-Source Release (credibility strategy)     Week 6+
      - Clean up README, add CONTRIBUTING.md
      - Add Apache 2.0 or MIT license
      - GitHub release v0.1.0 (Phase A)
      - Post to ArduPilot community forums
      - Post to r/ardupilot, r/drones, Hacker News (Show HN)
      - PURPOSE: Open source is a credibility strategy, not a revenue model.
        It builds community trust, demonstrates engineering maturity to
        regulators and investors, and creates a hiring pipeline. Revenue
        comes from services (DaaS), not from the software itself.
      Deliverable: Public GitHub repo with stars and forks


WORKSTREAM B: REGULATORY (one-time tasks, 5 hrs total)
=======================================================

  B1. CAA Flyer ID                                  This week
      - register-drones.caa.co.uk
      - 40 questions, 30 minutes, free
      Deliverable: Flyer ID number

  B2. Operator ID                                   This week
      - Same portal, £11.79/year
      Deliverable: Operator ID for airframe labelling

  B3. BMFA Membership Application                   This week
      - ~£40/year
      - Provides £5M public liability insurance
      - Required for most flying club access
      Deliverable: BMFA membership card

  B4. Contact Flying Clubs                          Weeks 1-2
      - Email ERFC (erfc.bmfa.club) — fixed-wing up to 20kg, Wed/Thu/Sun
      - Email Caterham CDMFC (cdmfc.org.uk) — 7 days/week
      - Visit both, introduce yourself, explain project
      Deliverable: Site access confirmed for summer flights


WORKSTREAM C: COMMUNITY + PORTFOLIO (2-3 hrs/week)
====================================================

  C1. Technical Blog                                Ongoing
      - Document mission engine design decisions
      - "How I built an autonomous mission planner at 17"
      - Post to Medium, dev.to, or personal site
      Deliverable: 3-5 blog posts by summer

  C2. Competition Research                          Weeks 1-4
      - IMechE UAS Challenge (entry deadline varies, usually autumn)
      - BAE Systems STEM Challenge
      - UK Young Engineer of the Year
      - IET Engineering Open House / YPE awards
      - Arkwright Engineering Scholarship (may have passed deadline)
      Deliverable: List of competitions with deadlines, entry started

  C3. UCAS Preparation                              Weeks 8-14
      - Draft personal statement section on drone project
      - Link to GitHub repo, blog posts, competition entries
      - Quantify: "43 tests, 160+ pages of research, open-source"
      Deliverable: Personal statement draft ready for September revision

  C4. Customer Conversations                         Weeks 1-14
      - Have at least 3 conversations with potential customers
        before the summer build (conservation orgs, farms, survey firms)
      - Understand their actual needs, pricing sensitivity, existing solutions
      - Document each conversation: who, what they need, what they'd pay

  C5. YouTube / Documentation Videos                Weeks 6+
      - Screen recordings of SITL missions
      - Narrated design walkthroughs
      - Build a portfolio reel for university/grant applications
      Deliverable: 2-3 YouTube videos


WORKSTREAM D: STUDY (integrated with A-levels)
================================================

  D1. Physics                                       Ongoing
      - Fluid dynamics (directly applies to aerodynamics)
      - Mechanics (forces, moments, CG calculations)
      - Electronics (for payload interface, power systems)

  D2. Maths / Further Maths                         Ongoing
      - Vectors and matrices (flight path computation)
      - Calculus (range equations, optimisation)
      - Statistics (sensor noise, Kalman filtering concepts)

  D3. Computer Science                              Ongoing
      - Algorithms (A*, graph search — route planning)
      - Software engineering (testing, architecture)
      - Data structures (mission data models)
```

### Phase 0 Milestones

| # | Milestone | Target Date | Evidence |
|---|-----------|-------------|----------|
| M0.1 | Flyer ID + Operator ID obtained | April 2026 | Certificate screenshots |
| M0.2 | BMFA membership active | April 2026 | Membership card |
| M0.3 | SITL E2E test harness passing in CI | May 2026 | GitHub Actions green badge |
| M0.4 | Waypoint parser with roundtrip tests | May 2026 | Test output |
| M0.5 | Mission engine open-sourced (v0.1.0) | May 2026 | GitHub release URL |
| M0.6 | SAR planner demonstrated in SITL | June 2026 | SITL recording + blog post |
| M0.7 | Flying club site access confirmed | June 2026 | Email confirmation |
| M0.8 | First blog post published | May 2026 | Published URL |
| M0.9 | Competition entry submitted | June 2026 | Confirmation email |

### Phase 0 Budget

| Item | Cost |
|------|------|
| Operator ID | £12 |
| BMFA membership | £40 |
| Domain name (optional, for blog/project site) | £10 |
| **Total** | **£62** |

---

## 3. PHASE 1: FIRST FLIGHT (Summer 2026)

**Duration:** 8-12 weeks (July — September 2026)
**Budget:** £850

### The Logic

This is the validation phase. Everything built in software must now prove it works on a real aircraft. The Skywalker X8 is chosen because it is the most forgiving, best-documented fixed-wing platform in the ArduPilot ecosystem. It has a cavernous payload bay, it is hand-launchable, and hundreds of people have built one before — so every problem you encounter has a forum post with the answer.

### Bill of Materials

| Item | Est. Cost (£) | Source |
|------|---------------|--------|
| Skywalker X8 airframe | 100-130 | HobbyKing, Banggood |
| Holybro Pixhawk 6C | 150-200 | Holybro direct, GetFPV |
| GPS module (M10) | 30-50 | Holybro |
| Power module | 20-30 | Included with Pixhawk kit |
| SiK telemetry radios (433 MHz pair) | 30-50 | Holybro, mRo |
| Metal gear servos x4 | 20-40 | HobbyKing |
| Motor + ESC + prop (Skywalker spec) | 40-70 | HobbyKing |
| 4S 5000mAh LiPo x2 | 50-70 | HobbyKing, Overlander |
| RC transmitter + receiver (budget) | 40-80 | RadioMaster Boxer or similar |
| Miscellaneous (wiring, connectors, heatshrink) | 20-40 | Amazon, local hobby shop |
| Airspeed sensor (MS4525DO) | 15-25 | Holybro |
| **Total** | **£515-785** | |

### Week-by-Week Plan

```
Week 1-2: BUILD
  - Assemble Skywalker X8 fuselage and wings
  - Install servos, linkages, control horns
  - Mount motor, ESC, propeller
  - Install Pixhawk 6C, GPS, power module, telemetry radio
  - Wire everything per ArduPilot Skywalker wiki
  - Bench power test (motor spin, servo deflection)

Week 3: CONFIGURE
  - Flash ArduPilot Plane firmware
  - Follow mandatory first-setup: accel cal, compass cal, RC cal
  - Configure servo directions and limits
  - Set up geofence (500m radius, 120m altitude)
  - Set failsafes: RC loss -> RTL, battery low -> RTL
  - Airspeed sensor calibration
  - Telemetry range test (walk 500m with radio, confirm link)

Week 4: GROUND TESTING
  - Motor run-up test (vibration check with Pixhawk logs)
  - CG verification (manufacturer spec for X8)
  - Pre-arm check pass (all sensors green)
  - Hand-toss glide test (motor off, gentle throw, assess trim)
  - Taxi test if suitable flat area available

Week 5-6: MAIDEN FLIGHTS (at BMFA club site)
  - Flight 1: MANUAL mode, 3-5 minutes, gentle turns, assess handling
  - Flight 2: FBWA mode (fly-by-wire), pilot in loop with stabilisation
  - Flight 3-5: Build confidence, trim aircraft, extend duration
  - RC safety pilot present at all times
  - Video record every flight from ground

Week 7-8: AUTONOMOUS FLIGHTS
  - Upload 3-waypoint mission via telemetry
  - First AUTO mode flight: takeoff -> 3 waypoints -> RTL
  - Test RTL from multiple positions
  - Test LOITER mode (hold position in wind)
  - Test geofence trigger (aircraft turns at boundary)
  - Test failsafes (turn off TX -> RTL activates)
  - Upload mission engine-generated .waypoints file -> fly it
  >>> THIS IS THE KEY MILESTONE: your software just flew a real aircraft <<<

Week 8-10: PAYLOAD INTERFACE
  - 3D print dovetail rail and tray (use library or online service if no printer)
  - Install rail in Skywalker X8 payload bay
  - Wire Anderson PowerPole + JST-GH connector
  - Test with 500g dummy payload (lead shot in tray)
  - CG check with and without payload
  - Vibration test (motor full throttle, 60 sec, check tray doesn't shift)
  - Flight test with dummy payload in FBWA and AUTO

Week 10-11: COST-PER-MISSION ANALYSIS
  - Create cost-per-mission spreadsheet covering:
    - Hardware depreciation per flight hour
    - Battery cycle cost
    - Insurance per mission
    - Operator time cost
    - Travel/fuel to site
    - Maintenance reserve per flight hour
  - Use this to set realistic service pricing for Phase 2

Week 11-12: DOCUMENTATION + PORTFOLIO
  - Compile flight logs, photos, video into portfolio
  - Write blog post: "First autonomous mission with a self-built mission engine"
  - Record demonstration video for competitions/university applications
  - Submit to any open competition deadlines
```

### Phase 1 Test Criteria

| # | Test | Pass Criteria |
|---|------|---------------|
| T1.1 | Structural inspection | No flex, all surfaces deflect correctly, CG within spec |
| T1.2 | Pre-arm checks | All sensors green: gyro, accel, compass, GPS 3D lock |
| T1.3 | Telemetry range | Clean data at 500m+ on ground |
| T1.4 | MANUAL maiden | 5+ min stable flight, controlled turns, safe landing |
| T1.5 | FBWA flight | Stabilised flight, level attitude maintained in turns |
| T1.6 | 3 consecutive clean flights | No incidents, no warnings in logs |
| T1.7 | AUTO 3-waypoint mission | Autonomous takeoff -> waypoints -> RTL, < 10m cross-track error |
| T1.8 | RTL from 3 positions | Aircraft returns and loiters within 50m of home |
| T1.9 | Geofence | Turns back at boundary within 2 seconds |
| T1.10 | RC-loss failsafe | RTL activates within 3 seconds of TX off |
| T1.11 | Mission engine file flown | .waypoints from mpe CLI executed successfully on real aircraft |
| T1.12 | Payload tray installed | Dummy 500g payload survives full-throttle vibration test |
| T1.13 | Payload swap time | < 2 minutes, no tools |

### Phase 1 Milestones

| # | Milestone | Target Date | Evidence |
|---|-----------|-------------|----------|
| M1.1 | Airframe assembled and bench-tested | July 2026 | Photos + motor spin video |
| M1.2 | ArduPilot configured, pre-arm pass | July 2026 | Log file screenshot |
| M1.3 | First MANUAL flight | August 2026 | Flight video + log |
| M1.4 | First AUTO waypoint mission | August 2026 | Log showing MISSION_ITEM_REACHED |
| M1.5 | Mission engine-generated file flown | August 2026 | CLI output + flight log |
| M1.6 | Payload interface demonstrated | September 2026 | Swap video + flight log with payload |
| M1.7 | Portfolio video compiled | September 2026 | YouTube or Vimeo link |

---

## 4. PHASE 2: DEMONSTRATE AND COMPETE (Academic Year 2026-2027)

**Duration:** September 2026 — June 2027
**Budget:** £500-2,000 (self-funded + prize money + small grants)

### The Logic

You now have a flying, autonomous, payload-swappable drone with working mission software. This phase is about accumulating evidence: competition results, first revenue, published work, and a community. Every achievement here becomes ammunition for university applications, grant proposals, and investor conversations.

### Workstreams

```
WORKSTREAM A: PAYLOAD MODULES
===============================

  A1. Camera/FPV Module                             Sept-Oct 2026
      - RunCam or Caddx FPV camera (£20-40)
      - 5.8 GHz VTX at 25mW (legal without license) (£30)
      - FPV monitor or goggles (£40-100)
      - Fixed dampened mount (vibration isolation)
      - Onboard SD recording
      Cost: £90-170
      Deliverable: Aerial video/photo capability

  A2. Cargo Drop Module                             Oct-Nov 2026
      - Servo-actuated bay door or release mechanism
      - 500g-1kg drop payload capacity
      - GPS-triggered release point
      - Mission engine integration (DROP_AT_WP command)
      Cost: £20-40
      Deliverable: Precision drop within 10m of target

  A3. Thermal Camera Module (stretch)               Jan-Feb 2027
      - FLIR Lepton 3.5 or similar (£150-250 if budget allows)
      - Raspberry Pi Zero companion computer
      - Real-time thermal overlay
      Cost: £200-350
      Deliverable: Wildlife/heat-signature detection capability


WORKSTREAM B: MISSION ENGINE PHASE B
======================================

  B1. Full Goal/ConstraintSet Architecture          Sept-Nov 2026
      - Goal parser (structured + natural language input)
      - Constraint engine (no-fly zones, altitude, weather, battery)
      - Risk scoring per mission

  B2. Delivery Corridor Planner                     Nov-Dec 2026
      - A-to-B with terrain following
      - Wind-adjusted ETAs
      - Drop zone approach pattern

  B3. ISR Multi-Point Surveillance                  Dec-Jan 2027
      - Configurable dwell time per point
      - Priority-weighted route optimisation
      - Camera trigger integration

  B4. Mission Engine v0.2.0 Release                 Feb 2027
      - All Phase B planners functional
      - Full SITL E2E test suite
      - Published as open-source release

  Deliverable: Mission engine handles SAR, ISR, delivery, survey mission types


WORKSTREAM C: GROUND COMMS PROJECT (standalone, transferable skills)
=====================================================================

  C1. Hill-Climbing Antenna Tracker                 Oct-Dec 2026
      - ESP32 + 2x servo gimbal + 2.4 GHz antenna
      - RSSI-based gradient ascent algorithm
      - Auto-aim at strongest signal source
      Cost: £40-60
      Deliverable: Working antenna tracker demo + blog post

  C2. 2-Node Mesh Link                              Jan-Mar 2027
      - Two tracker nodes + LoRa 868 MHz radios
      - Point-to-point data link, auto-tracking
      - Throughput and range testing
      Cost: £60-100
      Deliverable: Demonstrated 1km+ directional data link

  C3. FSO Laser Link (stretch)                      Apr-Jun 2027
      - 650nm laser diode + photodiode receiver
      - Same gimbal + tracking algorithm
      - Data over modulated laser beam
      Cost: £40-60
      Deliverable: Proof of concept laser comms at 100m+


WORKSTREAM D: COMPETITIONS + OUTREACH
=======================================

  D1. IMechE UAS Challenge                          Entry: autumn 2026
      - Design report submission
      - Flight demonstration (spring 2027)
      - Prize: up to £1,000 + industry exposure

  D2. BAE Systems STEM Awards                       Check deadline
      - Young engineer category
      - Portfolio submission

  D3. IET Young Professionals                       Check deadline
      - Engineering innovation category

  D4. UK Young Engineer of the Year                 Autumn 2026
      - Project presentation

  D5. Outreach
      - Talk at school STEM assembly
      - Present at BMFA club meeting
      - ArduPilot community contribution (docs, forum help)

  Deliverable: 2-3 competition entries, 1+ award/prize


WORKSTREAM E: FIRST REVENUE (stretch goal)
============================================

  E1. Conservation Survey Inquiry                   Jan-Mar 2027
      - Contact Surrey Wildlife Trust
      - Contact local ecology consultants
      - Offer aerial survey at cost (£50-100/flight)
      - Build case study from results

  E2. Agricultural Mapping                          Mar-Jun 2027
      - Contact local farms near club sites
      - Offer crop health mapping (if camera module working)
      - Charge nominal fee (£50-150/survey)

  Revenue target: £100-500 (proof of concept, not profit)


WORKSTREAM F: UNIVERSITY APPLICATIONS
=======================================

  F1. UCAS Personal Statement                       Sept-Oct 2026
      - Lead with drone project: design, build, code, fly, open-source
      - Quantify everything: tests, pages, flights, payload swaps
      - Link GitHub, blog, videos

  F2. Target Universities (Engineering)
      - Imperial College London (Aeronautics / EEE)
      - University of Cambridge (Engineering)
      - University of Bristol (Aerospace Engineering)
      - University of Southampton (Aeronautics & Astronautics)
      - University of Bath (Mechanical / Aerospace Engineering)
      - Loughborough (Aeronautical Engineering)

  F3. Interview Preparation                         Nov 2026 - Jan 2027
      - Be ready to discuss: aerodynamics, control theory, software architecture
      - Bring demo video on phone
      - Explain mission engine architecture on whiteboard

  Deliverable: Offers from 2+ target universities by March 2027
```

### Phase 2 Milestones

| # | Milestone | Target Date | Evidence |
|---|-----------|-------------|----------|
| M2.1 | Camera module flying and recording | Oct 2026 | Aerial footage |
| M2.2 | Cargo drop demonstration | Nov 2026 | Drop accuracy test results |
| M2.3 | Mission engine v0.2.0 released | Feb 2027 | GitHub release |
| M2.4 | Antenna tracker working | Dec 2026 | Demo video |
| M2.5 | Competition entry submitted | Autumn 2026 | Confirmation |
| M2.6 | UCAS submitted | Jan 2027 | UCAS confirmation |
| M2.7 | First paid survey or mapping flight | Mar 2027 | Invoice/receipt |
| M2.8 | University offers received | Mar 2027 | Offer letters |
| M2.9 | PDRA01 application submitted | Jun 2027 | CAA submission reference |

### Phase 2 Budget

| Item | Cost |
|------|------|
| Camera/FPV module | £90-170 |
| Cargo drop mechanism | £20-40 |
| Spare parts (props, batteries, foam) | £50-100 |
| Antenna tracker project | £40-60 |
| Mesh link radios | £60-100 |
| Competition entry fees | £0-50 |
| 3D printing (payload trays, brackets) | £30-50 |
| Thermal camera (stretch, if budget allows) | £200-350 |
| **Total (minimum)** | **£290-520** |
| **Total (with stretch items)** | **£490-870** |

---

## 5. PHASE 3: UNIVERSITY YEARS (2027-2030)

**Duration:** 3 academic years
**Budget:** £5,000-50,000 (grants, prizes, early revenue)

> **Timeline buffer note:** All dates after Phase 2 should be read with a 2-year buffer. University timelines slip (resits, placement years, personal circumstances), grant applications take longer than expected, and hardware development rarely hits its first target date. If Phase 3 takes 4 years instead of 3, the overall plan still works — the milestones matter more than the dates.

### The Logic

University provides four critical things: (1) access to workshops, labs, and equipment you cannot afford; (2) a peer talent pool to build a team; (3) credibility for grant applications; (4) three years of focused time before real-world financial pressures hit. The engineering degree itself directly advances the drone project — every module in aerodynamics, control systems, electronics, and materials science has immediate application.

---

### Phase 3A: First Year (2027-2028) — Establish

**Budget:** £2,000-10,000

```
ACADEMIC INTEGRATION
  - Join/form university drone society or UAV research group
  - Seek individual project (Year 1 design project) aligned with drone platform
  - Access wind tunnel, 3D printers, CNC, composite layup facilities
  - Take every relevant module: dynamics, materials, programming

TECHNICAL MILESTONES
  - Mission engine Phase C: multi-vehicle coordination, real-time replanning
  - Ground station web UI (React/Leaflet map, mission planning, telemetry)
  - Second airframe build (improved, lighter, custom composite if possible)
  - Camera + thermal dual-payload module
  - Remote ID hardware integration (mandatory UK Jan 2028)
  - Begin UK SORA documentation (Specific Operations Risk Assessment)
  - PDRA01 operational authorisation obtained (£500, if not already)

TEAM BUILDING
  - Recruit 2-3 collaborators from engineering cohort
  - Assign roles: one hardware lead, one software lead, one business/comms
  - Form university startup team (for competitions, grants)

FUNDING APPLICATIONS
  - University enterprise/innovation fund (most unis have £1-5K startup grants)
  - BMFA grant for youth development or club project
  - Apply to IMechE UAS Challenge as university team
  - Apply to Innovate UK Young Innovators Programme (if running)
  - Begin DASA Explorer application (see funding section)

BUSINESS FOUNDATIONS
  - Register UK Ltd company (£12 on Companies House)
  - Open business bank account (Starling, Tide — free)
  - Build simple website (project documentation, service descriptions)
  - Set up basic accounting (FreeAgent or spreadsheet)
  - Begin building a client pipeline (conservation, agriculture, survey)

FIRST COMMERCIAL OPERATIONS
  - Offer aerial survey services at university and locally
  - Target: 5-10 paid flights at £100-300 each
  - Build case studies from every engagement
  - Revenue target: £500-3,000
```

| # | Milestone | Target | Evidence |
|---|-----------|--------|----------|
| M3A.1 | University drone group joined/formed | Oct 2027 | Group photo/registration |
| M3A.2 | Company registered | Dec 2027 | Companies House confirmation |
| M3A.3 | PDRA01 operational authorisation | Mar 2028 | CAA authorisation letter |
| M3A.4 | Ground station web UI v1 | Jun 2028 | Screenshot + demo |
| M3A.5 | 5 paid operations completed | Jun 2028 | Invoices + case studies |
| M3A.6 | First grant awarded | Jun 2028 | Award letter |
| M3A.7 | Team of 3 formed | Jun 2028 | LinkedIn / team page |

---

### Phase 3B: Second Year (2028-2029) — Prove

**Budget:** £5,000-20,000

```
TECHNICAL MILESTONES
  - MEDIUM tier prototype (4-6m wingspan, 25-50kg class)
    - Likely requires university workshop access (composite layup)
    - Hybrid propulsion investigation (generator + electric)
    - 5-15 kg payload capacity
  - Tileable microdrone first prototype (130mm x 130mm quad, doc 29)
    - PCB design + fabrication
    - 3-unit swarm demonstration (basic formation flight)
  - Tube-launched folding-wing variant prototype (doc 29)
  - Mission engine multi-vehicle support (coordinate 2+ aircraft)
  - UK SORA SAIL I submission for BVLOS authorisation

INTERNATIONAL PROOF OF CONCEPT
  - Research trip to Canada (Mohammed has dual UK/Canadian citizenship — strategic asset)
    - Routine BVLOS since November 2025, no SFOC needed
    - No visa or work permit barriers
    - Strong regulatory data transfers to UK CAA and FAA applications
    - Identify Canadian university or industry partner
    - Demonstrate survey/mapping capability in approved conditions
    - Build evidence base for "tested in multiple regulatory environments"
  - Alternative: India (cheapest entry, startup-friendly, doc 27) if budget constrained

DEFENCE ENGAGEMENT
  - Apply to DASA Open Call for Innovation (£25K-350K typically)
  - Attend DSEI (Defence & Security Equipment International) exhibition
  - Contact Defence Science and Technology Laboratory (Dstl)
  - Target: ISR or logistics demonstration for MOD evaluation

FUNDING
  - Innovate UK Smart Grant application (£25K-500K, 50% match funding)
  - Connected Places Catapult programme application
  - University innovation competition
  - Prize money from engineering competitions
  - Revenue from operations: target £3,000-10,000

SWARM DEMONSTRATION
  - 3-5 microdrones flying coordinated patterns
  - GPS-denied relative navigation (using UWB or optical flow)
  - Video documentation for defence/investor audiences
```

| # | Milestone | Target | Evidence |
|---|-----------|--------|----------|
| M3B.1 | MEDIUM tier prototype first flight | Dec 2028 | Flight video + log |
| M3B.2 | Tileable microdrone first flight | Mar 2029 | Flight video |
| M3B.3 | 3-unit swarm demonstration | Jun 2029 | Multi-drone video |
| M3B.4 | UK SORA BVLOS application submitted | Mar 2029 | CAA reference number |
| M3B.5 | International demonstration completed (Canada) | Jun 2029 | Photos, partner letter |
| M3B.6 | DASA application submitted | Dec 2028 | Submission confirmation |
| M3B.7 | Innovate UK Smart Grant submitted | Mar 2029 | Application reference |
| M3B.8 | Revenue exceeds £5,000 cumulative | Jun 2029 | Accounts |

---

### Phase 3C: Third Year (2029-2030) — Launch

**Budget:** £10,000-50,000

```
TECHNICAL MILESTONES
  - LARGE tier design study (100-200kg, solar-assisted, doc 22)
  - Automated ground station prototype (doc 28)
    - Automated charging pad
    - Payload swap mechanism (robotic or assisted)
    - Weather monitoring + auto-launch-decision
  - Laser power beaming proof of concept (ground-based, doc 31)
    - 980nm diode laser -> GaAs PV receiver
    - Demonstrate 100W delivered at 50-100m range
    - Safety interlocks and exclusion zone protocol
  - Mission engine v1.0: production-ready release
    - All mission types operational
    - Web-based ground station
    - Fleet management for 2-5 aircraft
    - Customer-facing portal

BUSINESS
  - Multiple paying customers across 2-3 sectors
    - Conservation: wildlife survey, habitat mapping
    - Agriculture: crop health, livestock monitoring
    - Survey: construction sites, solar farms, coastal erosion
  - Revenue target: £10,000-30,000
  - Hire first part-time employees or contractors (2-3)
  - Apply for RAEng Enterprise Fellowship (£75K, no equity — competitive: ~20% acceptance rate, not guaranteed — see funding section)

REGULATORY
  - UK SORA BVLOS authorisation obtained
  - Begin planning for commercial operator certificate

GRADUATION
  - Final year project: publish paper on mission engine or swarm coordination
  - Graduate with engineering degree
  - Decision point: full-time on company, or employed + side project?
```

| # | Milestone | Target | Evidence |
|---|-----------|--------|----------|
| M3C.1 | Automated ground station prototype | Dec 2029 | Demo video |
| M3C.2 | Laser power PoC demonstrated | Mar 2030 | Test data + video |
| M3C.3 | BVLOS authorisation obtained | Mar 2030 | CAA letter |
| M3C.4 | Mission engine v1.0 released | Jun 2030 | GitHub release |
| M3C.5 | Revenue exceeds £10K cumulative | Jun 2030 | Accounts |
| M3C.6 | RAEng Enterprise Fellowship applied | Mar 2030 | Application submitted |
| M3C.7 | Degree completed | Jun 2030 | Transcript |
| M3C.8 | Go/no-go decision on full-time company | Jun 2030 | Written decision document |

---

## 6. PHASE 4: STARTUP SCALE (2030-2032)

**Duration:** 2 years
**Budget:** £100K-500K (grants + revenue)

### Prerequisites to Enter This Phase

```
MUST HAVE:
  [x] Proven drone platform with 100+ flights logged
  [x] Paying customers in at least 2 sectors
  [x] BVLOS operational authorisation
  [x] Registered UK Ltd company with revenue
  [x] Team of 3+ people
  [x] Engineering degree completed
  [x] At least one grant awarded

SHOULD HAVE:
  [ ] RAEng Enterprise Fellowship (£75K)
  [ ] International demonstration completed
  [ ] Defence engagement established
  [ ] Mission engine deployed with external users
```

### Year 1 (2030-2031)

```
OPERATIONS
  - Full-time CEO/CTO (you), 2-3 full-time engineers
  - Fleet: 5-8 operational MINI-tier drones
  - Weekly commercial operations across 2-3 sectors
  - Revenue target: £50-100K

PRODUCT
  - MEDIUM tier enters service (25-50kg class)
  - Mission engine as SaaS product (monthly subscription for other operators)
  - Drone-as-a-Service (DaaS) pricing: target 35-50% gross margins
    (accounts for hardware depreciation, insurance, maintenance reserve,
    operator time, and travel — use cost-per-mission spreadsheet from Phase 1)
  - Automated airbase v1 deployed at primary operating site
  - Fleet management dashboard (real-time tracking of all aircraft)

FUNDING
  - Innovate UK Smart Grant (£100-500K for advanced autonomy R&D)
  - DASA competition win (£50-350K for defence applications)
  - Revenue growth from operations
  - Total capital in: £100-300K

REGULATORY
  - Multiple UK SORA authorisations (different areas of operation)
  - Begin CAA Innovation Hub engagement for airship concept
  - Remote ID compliance across all aircraft
```

### Year 2 (2031-2032)

```
OPERATIONS
  - Fleet: 10-15 drones across MINI and MEDIUM tiers
  - 2+ operating bases
  - Revenue target: £100-200K
  - Team: 5-10 people
  - First international commercial operations (Canada, India, or Ghana)

PRODUCT
  - Tethered aerostat prototype (500m-2km altitude, doc 33)
    - Grid-powered via tether
    - Laser power beaming to orbiting drones
    - Communications relay
  - Swarm operations capability (5-10 microdrones coordinated)
  - LARGE tier design and build commences

PARTNERSHIPS
  - University KTP (Knowledge Transfer Partnership) for advanced research
  - Defence prime relationship (BAE, Leonardo, Thales — subcontractor)
  - Conservation organisation partnership (RSPB, Wildlife Trusts, WWF)

MARKET VALIDATION
  - Clear product-market fit in at least one sector
  - Repeat customers with annual contracts
  - Pipeline of £500K+ in qualified opportunities
```

| # | Milestone | Target | Evidence |
|---|-----------|--------|----------|
| M4.1 | Full-time operations launched | Oct 2030 | Payroll records |
| M4.2 | Fleet of 5+ operational drones | Mar 2031 | Asset register |
| M4.3 | £100K cumulative revenue | Dec 2031 | Annual accounts |
| M4.4 | Automated airbase v1 deployed | Jun 2031 | Site photos + demo |
| M4.5 | Tethered aerostat PoC | Dec 2031 | Test data + video |
| M4.6 | First international revenue | Jun 2032 | Invoice/contract |
| M4.7 | Team of 8+ people | Jun 2032 | Org chart |
| M4.8 | DASA or Innovate UK contract won | Dec 2031 | Contract signed |

---

## 7. PHASE 5: INFRASTRUCTURE BUILD (2032-2035)

**Duration:** 3 years
**Budget:** £1-10M (investment + grants + revenue)

### The Logic

This is the phase where the project transitions from "drone operator with clever software" to "infrastructure company building a national network." The airship layer is what makes this vision distinct from every other drone company. But airships are capital-intensive — this requires external investment for the first time.

```
YEAR 1 (2032-2033)
  - Raise seed round: £500K-2M
    - Lead: deep-tech VC (Amadeus Capital, IQ Capital, Octopus Ventures)
    - Or: Entrepreneur First (EF) cohort if earlier stage
    - Pitch: "unified drone infrastructure — one network, every sector"
  - First rigid or semi-rigid airship prototype OR partnership
    - Build vs buy decision (see Decision Points section)
    - If build: 10-20m prototype at 1-3km altitude, 1-5 kW solar
    - If partner: license/contract with Hybrid Air Vehicles, Varialift, or similar
  - Stratospheric balloon experiment
    - High-altitude weather balloon (£200) + telemetry payload
    - Test laser receiver at altitude (proof of concept)
  - UK CAA Innovation Hub: BVLOS corridor proposal
    - Propose first drone corridor between two automated airbases
    - 20-50km corridor with continuous BVLOS operations

YEAR 2 (2033-2034)
  - Airship v1 operational
    - Persistent station-keeping at 1-5 km altitude
    - Communications relay covering 20-50 km radius
    - Laser power beaming to orbiting drones demonstrated
  - Universal Resource Protocol (URP) v1 deployed (doc 34)
    - Any drone can request: power, compute, comms, data, storage
    - Priority tiers: emergency > defence > commercial
    - REST-like API over radio link
  - First BVLOS corridor operational
    - 2 automated airbases connected by airship relay
    - Drones transit corridor autonomously, recharging from airship
  - Revenue: £500K-1M
  - Team: 15-20 people

YEAR 3 (2034-2035)
  - National coverage pilot
    - 2-3 airships covering first regional corridor (e.g., Surrey to Bristol)
    - Multi-sector customers using same infrastructure
  - LARGE tier drone enters service
    - 100+ kg, solar-assisted, 8+ hour endurance
    - Long-range survey, maritime patrol, heavy cargo
  - Cross-sector demonstration
    - Same airship simultaneously supporting:
      - Agricultural survey drones
      - Conservation monitoring drones
      - Emergency response drone on standby
      - Maritime patrol drone
    - Film this. It is the core pitch for Series A.
  - Revenue: £1-2M
  - Team: 20-30 people
```

| # | Milestone | Target | Evidence |
|---|-----------|--------|----------|
| M5.1 | Seed round closed | Dec 2032 | Term sheet signed |
| M5.2 | First airship flight | Jun 2033 | Flight data + video |
| M5.3 | URP v1 deployed | Dec 2033 | Protocol spec + demo |
| M5.4 | BVLOS corridor operational | Jun 2034 | CAA authorisation + ops logs |
| M5.5 | Cross-sector demo filmed | Dec 2034 | Marketing video |
| M5.6 | Revenue exceeds £1M cumulative | Jun 2035 | Accounts |
| M5.7 | Team of 25+ | Jun 2035 | Org chart |

---

## 8. PHASE 6: NATIONAL NETWORK (2035+)

**Duration:** 5+ years
**Budget:** £10-100M+

```
SERIES A (2035-2036)
  - Raise £5-20M
  - Target: 10-35 airships for minimum viable UK coverage
  - Expand to 3-5 regional corridors
  - 50+ drone fleet across all 4 tiers
  - Full commercial operations across 5+ sectors
  - Revenue: £5-10M

SCALE (2036-2038)
  - National BVLOS network operational
  - Government backbone funding (NHS logistics, emergency response)
  - International expansion: 1-2 additional countries
  - Revenue: £10-30M
  - Team: 50-100 people

MATURITY (2038+)
  - Full UK coverage: 30-86 airships, tiered hexagonal grid
  - International operations in 3-5 countries
  - Stratospheric HAPS layer for persistent wide-area coverage
  - Revenue: £30-50M+
  - Team: 100+ people
  - IPO or strategic acquisition possible
```

---

## 9. FUNDING SOURCES — DETAILED TIMELINE

### 9.1 Self-Funded (Savings + Part-Time Work)

| Attribute | Detail |
|-----------|--------|
| Amount | £500-3,000 |
| When | Now through 2027 |
| Eligibility | N/A |
| Likelihood | Certain |
| Funds what | Phase 0-1 hardware, BMFA fees, competition entries |
| Effort | Low (already available) |
| Notes | Part-time job during sixth form or gap period. Even £50/month adds up. Tutoring A-level maths/physics pays £20-30/hr. |

### 9.2 Competition Prizes

| Competition | Prize | Deadline | Likelihood | Notes |
|-------------|-------|----------|------------|-------|
| IMechE UAS Challenge | Up to £1,000 + industry exposure | Autumn (varies) | Medium | University team entry preferred; can enter as independent. Requires flight demonstration. |
| BAE Systems STEM Awards | Up to £500 + mentoring | Check annually | Medium | Portfolio-based. Your project is strong for this. |
| UK Young Engineer of the Year (Royal Academy) | £500-1,000 + trophy | Autumn | Medium | Apply through school or direct. Your project is exactly the right type. |
| IET Young Professionals Awards | £250-500 | Varies | Low-Medium | Engineering innovation category. |
| Raspberry Pi Competition (if applicable) | Varies | Varies | Low | If you use RPi as companion computer. |
| Airbus Fly Your Ideas (university teams) | Up to €30,000 | ~Every 2 years | Low | Requires university team. Worth trying in Phase 3. |
| James Dyson Award | £30,000 (national) / £250,000 (international) | June typically | Low-Medium | Open to current students or recent grads (Phase 3). |
| Shell LiveWIRE / similar enterprise awards | Up to £10,000 | Varies | Medium | When company is registered. |
| **Total realistic prize money (Phases 0-2)** | **£500-3,000** | | | |
| **Total if university competitions included (Phase 3)** | **£2,000-30,000** | | | |

### 9.3 University Grants and Bursaries

| Source | Amount | When | Likelihood | Notes |
|--------|--------|------|------------|-------|
| University enterprise/startup fund | £500-5,000 | Year 1 onwards | High | Most Russell Group universities have these. Imperial has £10K+ available. |
| Department-level project funding | £200-1,000 | Year 1 onwards | High | For individual/group projects using drone platform. |
| Alumni entrepreneur fund | £1,000-10,000 | Year 2-3 | Medium | Competitive, but your project is compelling. |
| University Maker Space / FabLab | £0 (access to equipment worth £50K+) | Day 1 | Certain | 3D printers, CNC, laser cutters, composites lab. |
| **Total realistic** | **£1,000-15,000 over 3 years** | | | |

### 9.4 BMFA Grants

| Attribute | Detail |
|-----------|--------|
| Amount | £100-500 |
| When | When BMFA member, annual application |
| Eligibility | Active BMFA member, youth/development focus |
| Likelihood | Medium |
| Funds what | Equipment, competition entry, club fees |
| Effort | Low (short application form) |

### 9.5 DASA (Defence and Security Accelerator)

| Programme | Amount | When to Apply | Eligibility | Likelihood | Notes |
|-----------|--------|---------------|-------------|------------|-------|
| DASA Open Call | £25K-350K | Rolling (apply anytime) | UK-registered entity, novel defence/security concept | Medium | Your ISR, swarm, and maritime applications are directly relevant. Apply in Phase 3A once company registered. |
| DASA Themed Competition | £50K-1M | When published (2-3/year) | Specific to competition theme | Low-Medium | Watch for UAS, C-UAS, or ISR themed calls. |
| DASA Explorer | Up to £50K | Quarterly | Early-stage, high-risk concepts | Medium-High | Perfect for Phase 3A. Specifically designed for early innovators. |
| **When to apply** | Phase 3A (2027-2028) at earliest | | | | Need registered company + demonstrated capability |
| **Total realistic** | **£25K-100K** | | | | |

### 9.6 Innovate UK Smart Grants

| Attribute | Detail |
|-----------|--------|
| Amount | £25K-500K (covers 45-70% of project costs) |
| When | Rolling quarterly deadlines |
| Eligibility | UK-registered SME; need match funding for remainder |
| Likelihood | Low-Medium (highly competitive, ~10% success rate) |
| Funds what | R&D costs: salaries, equipment, subcontracting, travel |
| Effort | High (3-6 months to write, 10-page application + financials) |
| When to apply | Phase 3B (2028-2029) earliest. Need revenue, team, proven technology. |
| Notes | Needs match funding — you must cover 30-55% of project costs yourself. Best when you have revenue to show commercial viability. |

### 9.7 UKRI Future Flight Challenge (or successor programme)

| Attribute | Detail |
|-----------|--------|
| Amount | £500K-5M (as part of consortium) |
| When | Programme waves published periodically |
| Eligibility | UK entity, usually requires consortium with research partner |
| Likelihood | Low (large, competitive, consortium-based) |
| Funds what | BVLOS infrastructure, urban air mobility, drone integration |
| Effort | Very high (consortium building, multi-month application) |
| When to apply | Phase 4 (2030-2032). Need established company + research partner. |
| Notes | Future Flight Challenge funded £125M total. Successor programmes likely under DSIT. |

### 9.8 Connected Places Catapult

| Attribute | Detail |
|-----------|--------|
| Amount | Varies — often access to testbeds + £10-50K support |
| When | Programme-dependent |
| Eligibility | UK SME working on smart transport/logistics/urban systems |
| Likelihood | Medium |
| Funds what | Testing, validation, regulatory support, market access |
| Effort | Medium (application + pitch) |
| When to apply | Phase 3B onwards (2028+) |
| Notes | They run drone-specific programmes. Good for BVLOS corridor work. |

### 9.9 RAEng Enterprise Fellowship

| Attribute | Detail |
|-----------|--------|
| Amount | £75,000 over 1 year (salary equivalent) |
| When | Annual deadline (usually spring) |
| Eligibility | Recent graduate (within ~4 years), engineering/science background, commercialising research or technology |
| Likelihood | Medium (competitive but your profile fits well) |
| Funds what | Your salary for 1 year to work full-time on the company. No equity taken. |
| Effort | High (detailed application, interview) |
| When to apply | Phase 3C (spring 2030), upon graduation |
| Notes | This is a strong grant for your situation if awarded. £75K, no equity, 1-year runway. The Royal Academy of Engineering actively supports drone/autonomous systems. However, it is competitive (~20% acceptance rate) — do not plan finances around receiving it. Apply the moment you are eligible, but have a backup funding plan. |

### 9.10 Knowledge Transfer Partnerships (KTP)

| Attribute | Detail |
|-----------|--------|
| Amount | £60-120K over 1-3 years (covers a research associate + costs) |
| When | Rolling applications via Innovate UK |
| Eligibility | UK SME + university partner. The KTP associate (a recent grad) is embedded in the company. |
| Likelihood | Medium-High (well-funded programme, good success rates) |
| Funds what | A full-time researcher/engineer working in your company on a defined R&D project |
| Effort | High (need university sponsor + detailed project plan) |
| When to apply | Phase 4 (2030-2031). Need established company. |
| Notes | You could be the KTP associate in someone else's company first to learn — then later host a KTP yourself. |

### 9.11 Horizon Europe (or UK successor)

| Attribute | Detail |
|-----------|--------|
| Amount | €500K-5M (as consortium member) |
| When | Work programme calls published annually |
| Eligibility | UK status post-Brexit: associated country (can apply). Need EU consortium partners. |
| Likelihood | Low (complex, consortium-based, long timelines) |
| Funds what | Large-scale R&D programmes |
| Effort | Very high (9-12 months, consortium management) |
| When to apply | Phase 5 (2032+) if at all. |

### 9.12 Innovate UK Launchpad

| Attribute | Detail |
|-----------|--------|
| Amount | £25K-100K |
| When | Regional/thematic calls |
| Eligibility | UK SME in designated region/sector |
| Likelihood | Medium |
| Funds what | Innovation projects with regional impact |
| Effort | Medium |
| When to apply | Phase 3B-4 (2028-2031) |

### 9.13 British Business Bank Start Up Loans

| Attribute | Detail |
|-----------|--------|
| Amount | Up to £25,000 per person (loan, not grant) |
| When | Anytime (18+) |
| Eligibility | UK resident, viable business plan |
| Likelihood | High (designed to be accessible) |
| Funds what | Equipment, working capital, marketing |
| Effort | Medium (business plan required) |
| When to apply | Phase 3A (2027-2028) when company is registered |
| Notes | This is a LOAN at 6% fixed rate over 1-5 years. Only take this if revenue can service repayment. Comes with 12 months of free mentoring. |

### 9.14 Angel Investment

| Attribute | Detail |
|-----------|--------|
| Amount | £10K-250K (typical angel round) |
| When | Phase 3C or Phase 4 (2029-2031) |
| Eligibility | Registered company, demonstrable traction |
| Likelihood | Medium (depends on traction and market) |
| Funds what | Growth capital — team, equipment, ops |
| Effort | High (pitch deck, due diligence, negotiation) |
| Notes | UK angel networks: AngelList UK, Angel Investment Network, Cambridge Angels, London Business Angels, Syndicate Room. SEIS/EIS tax relief makes UK angels more willing to invest in early-stage deep-tech. |

### 9.15 Seed VC / Accelerators

| Programme | Amount | When | Likelihood | Notes |
|-----------|--------|------|------------|-------|
| Entrepreneur First (EF) | £80K pre-seed + £250K seed | Phase 3C-4 | Medium | London-based. Solo founders welcome. Deep-tech focus. They help you find a co-founder. |
| Techstars (various tracks) | $120K | Phase 4 | Low-Medium | Intense 3-month programme. Would need relocation or remote. |
| Y Combinator | $500K | Phase 4 | Low | Very competitive. US-centric but funds globally. |
| SOSV HAX | $250K hardware accelerator | Phase 4 | Medium | Specifically for hardware/deep-tech. Very relevant. |
| Seraphim Space | £100K-500K | Phase 4-5 | Medium | Space-adjacent tech VC. Airship/HAPS fits their thesis. |
| IQ Capital (Cambridge) | £250K-2M | Phase 4-5 | Medium | Deep-tech VC, specifically drones/autonomy. |
| Amadeus Capital Partners | £500K-5M | Phase 5 | Low-Medium | Deep-tech, later stage. |

### 9.16 Defence Contracts

| Route | Amount | When | Likelihood | Notes |
|-------|--------|------|------------|-------|
| DASA (see 9.5) | £25K-1M | Phase 3+ | Medium | Primary entry point |
| MoD direct procurement (mini-competition) | £100K-1M | Phase 4+ | Low-Medium | Need established DASA relationship first |
| NATO Innovation Fund | €100K-1M | Phase 5+ | Low | Europe's first multi-sovereign VC for deep-tech/defence |
| Defence BattleLab | Access + small funding | Phase 3+ | Medium | Experimentation programme, good for getting on MoD radar |

### 9.17 Revenue from Operations

| Phase | Annual Revenue Target | Sectors |
|-------|----------------------|---------|
| Phase 2 (2026-2027) | £100-500 | Conservation survey, ag mapping |
| Phase 3A (2027-2028) | £500-3,000 | Survey, conservation, university projects |
| Phase 3B (2028-2029) | £3,000-10,000 | Commercial survey, agriculture, construction |
| Phase 3C (2029-2030) | £10,000-30,000 | Multiple sectors, first contracts |
| Phase 4 (2030-2032) | £50,000-200,000 | Commercial ops, defence subcontracts |
| Phase 5 (2032-2035) | £500,000-2,000,000 | Infrastructure + operations |
| Phase 6 (2035+) | £5,000,000+ | National network, SaaS, international |

### 9.18 Crowdfunding

| Attribute | Detail |
|-----------|--------|
| Amount | £5,000-50,000 |
| When | Phase 3B-4 (2028-2031) |
| Platform | Kickstarter (for open-source hardware kit), Crowdcube (equity crowdfunding) |
| Likelihood | Medium (depends on community built) |
| Funds what | Open-source drone hardware kit (sell the platform to hobbyists/researchers) |
| Effort | Very high (video production, marketing, fulfilment logistics) |
| Notes | Only do this if open-source community is significant (1,000+ GitHub stars). The hardware kit becomes a revenue stream and community builder. |

### Funding Timeline Summary

```
PHASE 0-1 (2026)         £0-1K    Self-funded
                          ─────────────────────────────────────
PHASE 2 (2026-2027)      £0.5-3K  Prizes + first revenue
                          ─────────────────────────────────────
PHASE 3A (2027-2028)     £2-15K   University grants + prizes + revenue
                          ─────────────────────────────────────
PHASE 3B (2028-2029)     £25-100K DASA Explorer + revenue + BBB loan
                          ─────────────────────────────────────
PHASE 3C (2029-2030)     £75-200K RAEng Fellowship + Smart Grant + revenue
                          ─────────────────────────────────────
PHASE 4 (2030-2032)      £100-500K Smart Grant + DASA + angels + revenue
                          ─────────────────────────────────────
PHASE 5 (2032-2035)      £1-10M   Seed VC + defence contracts + revenue
                          ─────────────────────────────────────
PHASE 6 (2035+)          £10-100M Series A + gov contracts + revenue
```

---

## 10. MILESTONE MAP

### Master Timeline (ASCII)

```
2026                2027                2028                2029                2030
  |                   |                   |                   |                   |
  |  PHASE 0  | PH 1  |    PHASE 2       |     PHASE 3A      |     PHASE 3B      |
  |  Software | Build  |  Compete+Fly     |   Uni Year 1      |   Uni Year 2      |
  |  + Regs   | + Fly  |  + First Rev     |   Establish        |   Prove           |
  |           |        |                   |                    |                   |
TECH ─────────┼────────┼───────────────────┼────────────────────┼───────────────────
  |           |        |                   |                    |                   |
  * ME v0.1   * First  * Camera module     * Ground station UI  * MEDIUM prototype
  * SITL E2E  | flight * Cargo drop        * ME Phase C         * Microdrone proto
  * SAR plan  * First  * ME v0.2           * Remote ID          * Tube-launch proto
  * ISR plan  | AUTO   * Antenna tracker   *                    * Multi-vehicle
  |           * P/L    * Mesh link         *                    * Swarm demo (3)
  |           | swap   * (Thermal stretch) *                    *
  |           |        |                   |                    |
FUND ─────────┼────────┼───────────────────┼────────────────────┼───────────────────
  |           |        |                   |                    |                   |
  * £0        * £850   * Prizes £0.5-3K    * Uni grants £1-5K   * DASA £25-100K
  |           |        * Revenue £0.1-0.5K * Revenue £0.5-3K    * Revenue £3-10K
  |           |        |                   * BBB loan £10-25K?  * Smart Grant app
  |           |        |                   |                    |
REG ──────────┼────────┼───────────────────┼────────────────────┼───────────────────
  |           |        |                   |                    |                   |
  * Flyer ID  |        * PDRA01 app        * PDRA01 obtained    * UK SORA submitted
  * Op ID     |        |                   * Company registered  *
  * BMFA      |        |                   |                    |
  |           |        |                   |                    |
TEAM ─────────┼────────┼───────────────────┼────────────────────┼───────────────────
  |           |        |                   |                    |                   |
  * Solo      * Solo   * Solo + blog       * 2-3 collaborators  * 3-5 people
  |           |        * readers + forum   * University team    *
  |           |        |                   |                    |
MKT ──────────┼────────┼───────────────────┼────────────────────┼───────────────────
  |           |        |                   |                    |                   |
  * Open src  * Demo   * 1st comp entry    * 5 paid ops         * International PoC
  * Blog      * video  * 1st revenue       * 2 sectors          * Defence contact
  |           |        |                   |                    |


2030                2031                2032                2033                2035+
  |                   |                   |                   |                   |
  |     PHASE 3C      |      PHASE 4 (Startup Scale)         |   PHASE 5-6       |
  |   Uni Year 3      |                                       |   Infrastructure  |
  |   Launch           |                                       |   + National      |
  |                   |                   |                   |                   |
TECH ─────────────────┼───────────────────┼───────────────────┼───────────────────
  |                   |                   |                   |                   |
  * Auto ground stn   * Fleet 5-8 drones  * Aerostat PoC      * Airship v1
  * Laser power PoC   * MEDIUM in service * Swarm ops (10)    * URP deployed
  * ME v1.0           * Airbase v1        * LARGE tier build  * BVLOS corridor
  * LARGE design      * SaaS product      *                   * National pilot
  |                   |                   |                   |
FUND ─────────────────┼───────────────────┼───────────────────┼───────────────────
  |                   |                   |                   |                   |
  * RAEng £75K        * Innovate UK       * Seed round        * Series A
  * Revenue £10-30K   * DASA contract     * £0.5-2M           * £5-20M
  * Graduation        * Revenue £50-100K  * Revenue £100-200K * Revenue £0.5-2M
  |                   |                   |                   |
REG ──────────────────┼───────────────────┼───────────────────┼───────────────────
  |                   |                   |                   |                   |
  * BVLOS obtained    * Multi-area BVLOS  * CAA Innovation    * BVLOS corridor
  * Commercial cert?  * Int'l ops auth    * Hub engagement    * authorised
  |                   |                   |                   |
TEAM ─────────────────┼───────────────────┼───────────────────┼───────────────────
  |                   |                   |                   |                   |
  * 3-5 people        * 5-8 FT employees  * 8-15 people       * 20-30 people
  * First hires       * Office/workshop   *                   * 50-100 (Ph 6)
  |                   |                   |                   |
MKT ──────────────────┼───────────────────┼───────────────────┼───────────────────
  |                   |                   |                   |                   |
  * Multi-sector      * Repeat customers  * 1st international * Multi-corridor
  * customers         * Annual contracts  * revenue           * UK coverage
  * Defence sub       * Pipeline £500K+   *                   * 5+ sectors
```

---

## 11. RISK REGISTER

### R1: Maiden Flight Crash Destroys Airframe + Electronics

| Attribute | Detail |
|-----------|--------|
| Phase | 1 |
| Likelihood | Medium (20-30% for first-time builder) |
| Impact | High — £500+ lost, weeks of delay |
| Mitigation | Follow ArduPilot wiki exactly. CG check before every flight. Glide test first. Mount electronics on vibration-dampened foam. Use sacrificial EPO nose. Fly in calm conditions. Have experienced club member present. |
| Trigger for Plan B | If crash destroys Pixhawk, assess whether to replace (~£150) or pause and focus on more SITL software work until budget recovers. |

### R2: No Flying Club Access (All Nearby Clubs Full or Unfriendly)

| Attribute | Detail |
|-----------|--------|
| Phase | 0-1 |
| Likelihood | Low (ERFC and Caterham both within reach) |
| Impact | High — cannot fly legally without suitable site |
| Mitigation | Contact both clubs early. BMFA membership makes you welcome. Be polite, show up, volunteer. Fallback: BMFA club finder has 750+ clubs and 1000+ sites nationally. |
| Trigger for Plan B | If neither club works, search wider (Horsham, Dorking, Kent clubs). Worst case, find private farmland with landowner permission. |

### R3: Mission Engine Software Has Fundamental Architecture Flaw

| Attribute | Detail |
|-----------|--------|
| Phase | 0-2 |
| Likelihood | Low-Medium |
| Impact | Medium — delay while refactoring |
| Mitigation | TDD approach with 43+ tests catches regressions. SITL validation proves missions actually fly. Architecture based on well-understood patterns (Goal -> Constraint -> Route -> Waypoints). |
| Trigger for Plan B | If Phase B planners cannot fit into Phase A architecture, plan a clean v2 rewrite preserving test fixtures as specification. Budget 4-6 weeks. |

### R4: CAA Tightens Regulations or Delays BVLOS Pathway

| Attribute | Detail |
|-----------|--------|
| Phase | 2-4 |
| Likelihood | Medium (CAA is slow and conservative) |
| Impact | High — commercial operations and infrastructure vision depend on BVLOS |
| Mitigation | Start SORA documentation early (Phase 3A). Engage CAA Innovation Hub proactively. Build evidence base (hours flown, safety record). International operations provide alternative revenue while UK process plays out. |
| Trigger for Plan B | If BVLOS takes 2+ years longer than expected, focus on VLOS commercial ops (survey, mapping — still viable) and international markets where BVLOS is easier (Rwanda, India, Ghana). |

### R5: Grants Rejected — Cannot Fund MEDIUM Tier or Scale-Up

| Attribute | Detail |
|-----------|--------|
| Phase | 3-4 |
| Likelihood | Medium-High (grant success rates are 10-25%) |
| Impact | High — slows progression to larger platforms |
| Mitigation | Apply to multiple grants in parallel. Never depend on a single funding source. Build revenue from MINI-tier operations to self-fund incrementally. Keep burn rate low (university covers living costs during Phase 3). |
| Trigger for Plan B | If no grants by end of Phase 3B, extend Phase 3 and focus on revenue growth. Profitable MINI-tier operations can eventually fund MEDIUM tier development (slower but independent). |

### R6: University Offer Disappointing (Not a Top Aero/Engineering Programme)

| Attribute | Detail |
|-----------|--------|
| Phase | 2 |
| Likelihood | Low-Medium (your profile is strong) |
| Impact | Medium — less access to facilities, weaker network |
| Mitigation | Apply to 5 universities across a range. Your project is a differentiator that most applicants do not have. Practice interview extensively. Even a "lower-ranked" engineering programme provides workshop access and collaborators. |
| Trigger for Plan B | Any accredited engineering degree works. The project matters more than the institution. If no satisfactory offer, consider a gap year (more time for Phase 2 work) and reapply. |

### R7: Revenue Slower Than Expected — No Product-Market Fit

| Attribute | Detail |
|-----------|--------|
| Phase | 3-4 |
| Likelihood | Medium |
| Impact | High — delays everything downstream |
| Mitigation | Start revenue attempts early (Phase 2) to learn what customers actually want. Iterate on service offering. Conservation survey and agricultural mapping are proven markets with existing demand. Talk to 20 potential customers before Phase 3C. |
| Trigger for Plan B | If cumulative revenue is below £5K by end of Phase 3B, reassess target sectors. Consider pivoting to: (a) mission engine SaaS for other drone operators, (b) defence-focused consulting, or (c) open-source hardware kits. |

### R8: Competitors Build the Unified Infrastructure First

| Attribute | Detail |
|-----------|--------|
| Phase | 4-6 |
| Likelihood | Low-Medium |
| Impact | Medium — changes competitive positioning but does not kill the company |
| Mitigation | Your differentiator is not any single technology but the integration of multi-tier drones + mission engine + infrastructure under one unified protocol. No current competitor is building this specific vision. Monitor: Wing, Zipline, Hybrid Air Vehicles, Thales, Airobotics, Skyports. |
| Trigger for Plan B | If a major player (Google Wing, Amazon) builds UK drone infrastructure, pivot to being a best-in-class platform/software provider that operates ON their infrastructure, not competing with it. |

### R9: Technical Failure at Scale (MEDIUM/LARGE Tier Cannot Be Made to Work)

| Attribute | Detail |
|-----------|--------|
| Phase | 3-5 |
| Likelihood | Low-Medium |
| Impact | High — limits platform family vision |
| Mitigation | Each tier is independently viable. MINI tier alone supports a viable survey/mapping business. MEDIUM tier can be partnered or purchased (e.g., Wingcopter, Quantum Systems) rather than built from scratch. |
| Trigger for Plan B | If custom MEDIUM build fails after 2 attempts, buy COTS (commercial off-the-shelf) MEDIUM platform and integrate your mission engine + payload interface. Focus on software and operations, not airframe manufacturing. |

### R10: Key Person Risk (You Get Injured, Burn Out, or Change Direction)

| Attribute | Detail |
|-----------|--------|
| Phase | All |
| Likelihood | Low-Medium |
| Impact | Critical — project stops |
| Mitigation | Document everything obsessively (you are already doing this — 34 documents). Open-source the mission engine so others can continue. Build a team as early as possible (Phase 3A). Maintain work-life balance — this is a marathon, not a sprint. |
| Trigger for Plan B | If you need to step back for 6+ months, the project hibernates. Documentation and open-source code ensure it can resume. If permanent, the open-source community may carry it forward. |

### R11: Airship Technology Does Not Mature Fast Enough

| Attribute | Detail |
|-----------|--------|
| Phase | 5-6 |
| Likelihood | Medium (airships have a long history of "almost ready") |
| Impact | High — infrastructure vision requires airships as nodes |
| Mitigation | Start with tethered aerostats (proven, cheap, available today). Graduate to free-flying airships only when technology is demonstrated. Partner rather than build. Monitor Hybrid Air Vehicles (Bedford, UK), LTA Research, Flying Whales. |
| Trigger for Plan B | If no viable airship partner/technology by 2034, substitute tower-mounted infrastructure (masts with solar + laser + comms) as ground-based network nodes. Less elegant but achievable with current technology. |

### R12: India/International Regulatory Environment More Hostile Than Expected

| Attribute | Detail |
|-----------|--------|
| Phase | 3B-4 |
| Likelihood | Medium |
| Impact | Medium — delays international expansion |
| Mitigation | Research thoroughly before committing (doc 27 already done). Use local partners with regulatory connections. Start with lowest-friction countries (Rwanda, then India). Have UK revenue as fallback. |
| Trigger for Plan B | If first international market fails, try second choice. If 2 fail, defer international expansion until Phase 5 and focus on UK market depth. |

### R13: SEIS/EIS Investment Climate Deteriorates

| Attribute | Detail |
|-----------|--------|
| Phase | 4-5 |
| Likelihood | Low-Medium |
| Impact | Medium — harder to raise angel/seed |
| Mitigation | Do not depend solely on equity investment. Grant-funded path (DASA + Innovate UK + RAEng) can reach Phase 4 without equity. Revenue growth provides alternative funding path. |
| Trigger for Plan B | If equity raise fails twice, continue as a grant + revenue funded company. Growth will be slower but retains 100% ownership. |

### R14: A-Level Results Lower Than Expected

| Attribute | Detail |
|-----------|--------|
| Phase | 1-2 |
| Likelihood | Low (you are on further maths — you are strong) |
| Impact | Medium — affects university options |
| Mitigation | Project itself significantly strengthens any application. Universities value demonstrated capability. Even with lower grades, clearing offers from good engineering programmes are available. |
| Trigger for Plan B | If results are genuinely disappointing, take a gap year. Use the year for Phase 2 work (compete, build, fly, earn). Reapply with stronger portfolio and retake any weak subject. |

### R15: Battery/Power Technology Does Not Improve as Projected

| Attribute | Detail |
|-----------|--------|
| Phase | 4-6 |
| Likelihood | Low (battery tech is improving 5-8% per year consistently) |
| Impact | Medium — limits range/endurance of electric platforms |
| Mitigation | Laser power beaming and airship-based recharging are specifically designed to overcome battery limitations. Hybrid propulsion (generator + electric) is a proven fallback for MEDIUM/LARGE tiers. Hydrogen fuel cells are an emerging option. |
| Trigger for Plan B | If batteries plateau, accelerate laser power and hydrogen fuel cell timelines. Hybrid propulsion for MEDIUM and LARGE tiers. |

---

## 12. KEY DECISION POINTS

### D1: Form a Company (Phase 3A, ~December 2027)

```
TRIGGER: You have paying customers or are applying for grants that require a legal entity.

DECISION: Register a UK Ltd company on Companies House (£12).

GO CRITERIA:
  - At least 1 paying customer or signed LOI
  - Grant application that requires a company
  - £0 cost to register

NO-GO CRITERIA:
  - No reason to delay this. It costs nothing and enables everything.

RECOMMENDATION: Register in December 2027 (first term of university).
               This gives you a company registration date to cite in grants.
```

### D2: Take on Debt (Phase 3A-3B, ~2028)

```
TRIGGER: Need £10-25K for MEDIUM tier prototype or operating capital.

DECISION: Apply for British Business Bank Start Up Loan.

GO CRITERIA:
  - Revenue demonstrably growing (>£2K/year)
  - Clear plan for how the money generates more revenue
  - Can service £400-500/month repayment from operations

NO-GO CRITERIA:
  - Revenue is zero or declining
  - No clear path to repayment
  - University living costs are already stretched

RECOMMENDATION: Only take debt if revenue trajectory is clear. Grants are free money.
               Exhaust grant options first.
```

### D3: Raise External Equity Investment (Phase 4-5, ~2031-2032)

```
TRIGGER: Revenue is growing but capital is needed faster than revenue can fund it.
         Airship development requires £500K+ that grants alone cannot cover.

DECISION: Raise seed round from angels or VC.

GO CRITERIA:
  - Revenue >£100K/year and growing >50% YoY
  - Clear use of funds (e.g., airship prototype, team expansion)
  - Multiple interested investors (don't take the first offer)
  - Reasonable valuation (>£2M pre-money)

NO-GO CRITERIA:
  - Revenue is flat or declining
  - You would give up >30% equity in seed round
  - Investor wants to redirect strategy away from infrastructure vision
  - You can fund the next phase from grants + revenue (slower but owns more)

RECOMMENDATION: Delay equity as long as possible. Every month of revenue and
               progress increases your valuation. RAEng + DASA + Innovate UK
               can fund £200-500K with zero dilution.
```

### D4: Build vs Partner for Airships (Phase 5, ~2032-2033)

```
TRIGGER: Infrastructure vision requires airship layer. Must decide whether to
         design/build airships in-house or partner with existing manufacturer.

OPTION A: BUILD IN-HOUSE
  Pro: Full control, proprietary technology, higher margin
  Con: Massive R&D cost (£5-50M), 3-5 year development, regulatory complexity
  Requires: Dedicated aerospace engineering team (10+ people), large facility

OPTION B: PARTNER/LICENSE
  Pro: Faster to market, lower capital requirement, proven technology
  Con: Dependency on partner, lower margin, less differentiation
  Partners to evaluate: Hybrid Air Vehicles (Bedford, UK), LTA Research (US),
                        Varialift (UK), Flying Whales (France)

OPTION C: START WITH AEROSTATS, DEFER AIRSHIP DECISION
  Pro: Tethered aerostats are proven, cheap (~£50-100K), no BVLOS needed
  Con: Fixed position, limited altitude, not the full vision
  Use case: Proof of concept for laser power + comms relay

RECOMMENDATION: Option C first (Phase 4-5), then Option B (Phase 5-6).
               Only build in-house (Option A) if company reaches £10M+ revenue
               and has 50+ employees. The airship itself is not your competitive
               advantage — the integrated network is.
```

### D5: Choose International Markets (Phase 3B-4, ~2028-2031)

```
TRIGGER: UK operations proven, looking for international expansion.

OPTION A: INDIA (cheapest, largest addressable market)
  Pro: Huge agricultural market, growing drone regulation (DGCA Digital Sky),
       English-speaking, low operating costs
  Con: Bureaucratic, corruption risk, intense local competition (IdeaForge, etc.)
  Estimated cost: £3-5K for initial trip + demo

OPTION B: RWANDA (most permissive regulations)
  Pro: Performance-based RCAA framework, government pro-drone, proven model
  Con: Small market, Zipline dominance, limited local talent pool
  Estimated cost: £5-8K for initial trip + demo

OPTION C: GHANA (regulatory + market size balance)
  Pro: Active drone delivery ops (Zipline), GCAA framework established
  Con: Less developed than Rwanda for drones
  Estimated cost: £5-8K for initial trip + demo

OPTION D: AUSTRALIA (most valuable single market for UK expansion)
  Pro: CASA is progressive, English-speaking, high-value agriculture sector
  Con: Expensive, competitive, far
  Estimated cost: £10-15K for initial trip + demo

RECOMMENDATION: India first (cheapest, largest market, Phase 3B).
               Rwanda second (easiest regulatory, Phase 3C).
               Australia third (highest value, Phase 4).
```

### D6: Pivot Triggers — When the Original Plan Is Not Working

```
TRIGGER                                          PIVOT TO
──────────────────────────────────────           ──────────────────────────────
No revenue by end of Phase 3B (2029)   ────►    Mission engine SaaS for other
                                                 drone operators (sell software,
                                                 not fly drones)

No grants by end of Phase 3C (2030)    ────►    Get a job at a drone company
                                                 (Wing, Zipline, Thales) for
                                                 2-3 years, learn, save, return

Can't build MEDIUM tier (2029)         ────►    Buy COTS platform, integrate
                                                 your software. Become an ops
                                                 + software company, not a
                                                 manufacturer.

Airship layer infeasible (2034)        ────►    Tower-based ground network
                                                 with mast-mounted laser + comms.
                                                 Less dramatic, still valuable.

UK market too small (2032)             ────►    Move to India or US. The tech
                                                 is portable. The market is not.

Full vision fails but revenue grows    ────►    Become a profitable survey/
                                                 mapping drone operator. Not the
                                                 original dream but a good business.
```

---

## 13. HONEST ASSESSMENT

### Probability of Reaching Each Phase

```
Phase 0: Foundation .......... 95%   (almost certain — it is software + paperwork)
Phase 1: First Flight ........ 85%   (high — many people have built Skywalker X8s)
Phase 2: Demonstrate ......... 75%   (good — contingent on time management with A-levels)
Phase 3A: Uni Year 1 ......... 70%   (likely — contingent on university admission)
Phase 3B: Uni Year 2 ......... 50%   (coinflip — depends on grants, team, momentum)
Phase 3C: Uni Year 3 ......... 40%   (less likely — many talented people stall here)
Phase 4: Startup Scale ........ 20%   (hard — full-time company is a different game)
Phase 5: Infrastructure ....... 5-10% (very hard — deep-tech hardware + regulation + capital)
Phase 6: National Network ..... 1-3%  (moonshot — but Zipline was once a grad school idea too)
```

### Most Likely Failure Modes

```
1. ATTRITION (most common, Phase 2-3)
   University, social life, career offers, and the sheer grind of a multi-year
   hardware project cause gradual disengagement. The repo goes quiet. The drone
   sits in a closet. This kills more student projects than any technical failure.

   Antidote: Public accountability (blog, YouTube, open-source community),
   competition deadlines, and early revenue (even £100 from a customer changes
   your psychology from "hobby" to "business").

2. FUNDING GAP (Phase 3B-4)
   Grants are rejected. Revenue is too small to fund next tier. No investor
   interest because the company is "too early." The MEDIUM tier prototype
   requires £10-50K that does not materialise.

   Antidote: Stay lean. The MINI tier alone is a viable business. Do not
   over-invest in hardware you cannot afford. Software is free to develop.

3. REGULATORY WALL (Phase 3-4)
   BVLOS takes longer than expected. CAA requires more documentation, more
   insurance, more evidence than you can produce as a small team. Commercial
   operations are blocked by red tape.

   Antidote: International markets. UK VLOS operations. Sell software/planning
   to operators who already have authorisation.

4. TECHNICAL COMPLEXITY SPIRAL (Phase 3-5)
   Each new tier is harder than the last. MEDIUM tier composites are not like
   EPO foam. LARGE tier solar integration is not like bolting on a panel.
   Airships are not like drones. Each step up requires fundamentally different
   engineering skills.

   Antidote: Partner for what you cannot build. Buy COTS where possible.
   Focus on what you do best: mission engine, payload interface, integration.
```

### What "Success" Looks Like If the Full Vision Does Not Materialise

```
OUTCOME A: "Profitable Drone Operator" (most likely positive outcome)
  - Reached Phase 4. Revenue £50-200K/year. Team of 5-10.
  - Fleet of MINI and maybe MEDIUM drones.
  - Commercial survey, agriculture, conservation clients.
  - Mission engine used by 50-100 other operators (open-source or SaaS).
  - Never built the airship layer.
  - This is a good business and a good life.

OUTCOME B: "Defence Contractor Niche" (plausible)
  - DASA contracts led to MoD relationships.
  - Swarm, ISR, and maritime applications found defence customers.
  - Revenue £200K-1M/year, mostly defence.
  - The infrastructure vision was too ambitious, but the technology
    found a market.

OUTCOME C: "Acqui-hired by Wing/Zipline/BAE" (optimistic partial)
  - Your technology, team, and regulatory know-how attracted a larger player.
  - £1-5M acquisition. You join their team for 2-3 years.
  - The vision lives on inside a bigger organisation.
  - You walk away with capital, experience, and network to try again.

OUTCOME D: "Open-Source Legacy" (minimum viable outcome)
  - The company did not work out commercially.
  - But the mission engine is used by 500+ people worldwide.
  - The research documentation is a reference for the ArduPilot community.
  - You have a world-class portfolio that opens any engineering job.
  - The skills compound forever.
```

### The Minimum Outcome That Makes the Journey Worthwhile

```
Even if you reach only Phase 2 and then stop:

  - You will have designed, built, and flown an autonomous drone
  - You will have written a production-grade mission planning engine
  - You will have open-source software used by others
  - You will have a UCAS application that no other 17-year-old in the country can match
  - You will have learned Python, CAD, electronics, aerodynamics, regulations,
    RF engineering, control theory, and project management
  - You will have a portfolio that gets you into any engineering programme
    and any engineering job

  That alone is worth every hour invested.

  Everything beyond Phase 2 is upside.
```

### A Note on Timelines

The dates in this roadmap are targets, not commitments. Hardware projects always take longer than planned. Grants always take longer to arrive. Regulations always move slower than you hope. Software is the only thing that moves at the speed you type.

The phases are sequential but the durations are flexible. If Phase 3B takes an extra year, that is fine. If Phase 4 starts two years later than projected, that is fine. The vision does not expire. What matters is that each phase builds evidence for the next, and that you never stop making progress — even if progress is one commit, one flight, or one conversation per week.

The 34 documents you have already written are evidence that you know how to make consistent progress. That is the single most important skill for everything that follows.

---

## APPENDIX A: DOCUMENTS INDEX AND PHASE MAPPING

| Doc | Title | Primary Phase |
|-----|-------|---------------|
| 00 | Project Overview | All |
| 01 | Market Research | 3-6 |
| 02 | Technical Specs | 1-2 |
| 03 | Physics and Engineering | 1-3 |
| 04 | Zipline Case Study | 3-6 |
| 05 | African Air Defence Context | 4-6 |
| 06 | Development Roadmap and Test Plan | 0-2 |
| 07 | Mission Engine Architecture | 0-3 |
| 08 | Payload System Design | 1-3 |
| 09 | UK Regulations and Test Sites | 0-4 |
| 10 | Pest Control Applications | 2-4 |
| 11 | Military Applications Research | 3-6 |
| 12 | Naval Maritime Applications | 4-6 |
| 13 | Camera/IR/LiDAR Overview | 2-3 |
| 13 | Sensor Payload Specifications | 2-4 |
| 14 | Deep EO Camera Systems | 2-4 |
| 15 | Deep Thermal IR Imaging | 2-4 |
| 16 | Deep LiDAR Scanning | 3-5 |
| 17 | Deep Loitering Munitions | 4-6 |
| 18 | Deep Counter-UAS | 4-6 |
| 19 | Deep Swarm Deployment | 3-5 |
| 20 | Deep Naval ASW Sonar | 5-6 |
| 21 | Deep Pest Control Systems | 2-4 |
| 22 | Multi-Scale Platform Family | 3-6 |
| 23 | Mesh Network and Directional Comms | 2-4 |
| 24 | Ground Station Software Architecture | 2-4 |
| 25 | AI CAD Tools Research | 3-5 |
| 26 | Automated Drone Bases Research | 4-6 |
| 27 | Regulatory Strategy International | 3-6 |
| 28 | Ground Station Hardware Design | 3-5 |
| 29 | Tileable Microdrone Design | 3-5 |
| 29 | Tube-Packaged Folding Wing Design | 3-5 |
| 30 | Distributed Radar Swarm Research | 4-6 |
| 31 | In-Flight Power Transfer | 4-6 |
| 32 | Persistent Stratospheric Platforms | 5-6 |
| 33 | Aerial Command Base Concept | 5-6 |
| 34 | Unified Airship Infrastructure Network | 5-6 |
| 34 | NotebookLM Airship Infrastructure Research | 5-6 |
| 35 | This Document (Development and Funding Roadmap) | All |

---

*Last updated: 2026-03-26*
*Next review: After Phase 0 completion (June 2026)*
