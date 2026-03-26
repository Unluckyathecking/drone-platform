# Unified Airship Infrastructure Network: Cross-Sector Resource Sharing Platform

## Executive Summary

This document defines a single, interconnected airship infrastructure network that serves every drone sector simultaneously — agriculture, science, military, marine, conservation, logistics, and emergency services. The core principle: any airship in the network provides power, compute, communications, data, and storage to any authorised drone from any sector, on demand, via a universal resource request protocol.

This is not a collection of parallel networks. It is one infrastructure — like the road network serves cars, trucks, ambulances, buses, and military vehicles on the same tarmac.

The network consists of 30-86 airships positioned across the UK, each performing a primary sector mission while simultaneously serving as infrastructure nodes for all nearby drones. A universal resource request protocol enables any drone to broadcast a need (power, compute, comms, data, storage, resupply) and receive a response from the nearest capable airship within seconds. Priority tiers ensure emergency services always get first access, while a hybrid economic model blends government backbone funding with commercial operation and cooperative sector agreements.

---

## Table of Contents

1. Network Architecture
2. Universal Resource Request Protocol
3. Cross-Sector Scenarios
4. Economic Model
5. Technical Specifications
6. Network Resilience
7. Scaling Calculations
8. Comparison with Existing Infrastructure Models
9. Development Roadmap
10. Integration with Existing Project Architecture

---

## 1. NETWORK ARCHITECTURE

### 1.1 The Four-Layer Model

The network has four physical layers, each with a distinct role:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        LAYER 4: BACKBONE                                     ║
║                                                                              ║
║   LEO Satellites  ◄──────►  GEO Satellites  ◄──────►  Internet Gateways     ║
║   (Starlink/OneWeb)         (SATCOM)                   (fibre landing pts)   ║
║                                                                              ║
║   Role: Long-haul connectivity, GPS, weather data, global reach             ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                        LAYER 3: AIRSHIPS (NODES)                             ║
║                                                                              ║
║   Stratospheric (18-20 km)     Tropospheric (3-8 km)     Low (500m-2 km)   ║
║   ┌───────────────┐            ┌───────────────┐         ┌──────────────┐   ║
║   │ Super-pressure│            │ Semi-rigid     │         │ Tethered     │   ║
║   │ balloon or    │            │ helium airship │         │ aerostats or │   ║
║   │ solar HAPS    │            │ 50-150 m       │         │ small blimps │   ║
║   │               │            │                │         │              │   ║
║   │ Power: solar  │            │ Power: solar + │         │ Power: grid  │   ║
║   │ Comms: SATCOM │            │ fuel cell      │         │ via tether   │   ║
║   │ Compute: edge │            │ Comms: all     │         │ Comms: all   │   ║
║   │ Laser: 4-8    │            │ Compute: heavy │         │ Compute: med │   ║
║   │ Range: 100 km │            │ Laser: 6-12    │         │ Laser: 2-4   │   ║
║   └───────────────┘            │ Range: 50 km   │         │ Range: 20 km │   ║
║                                └───────────────┘         └──────────────┘   ║
║                                                                              ║
║   Role: Resource providers — power, compute, comms, data, storage           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                        LAYER 2: DRONES (CLIENTS)                             ║
║                                                                              ║
║   MICRO     MINI      MEDIUM     LARGE      Cargo     Emergency   Military  ║
║   <1 kg     5-15 kg   25-50 kg   100+ kg    varies    varies      varies    ║
║                                                                              ║
║   All equipped with: standard PV receiver, URP transceiver, identity cert   ║
║                                                                              ║
║   Role: Mission execution — request resources from Layer 3 as needed        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                        LAYER 1: GROUND (HUBS)                                ║
║                                                                              ║
║   Automated airbases     Regional ops centres    Gateway ground stations    ║
║   (doc 26)               (human oversight)       (SATCOM + fibre uplink)    ║
║                                                                              ║
║   Role: Physical maintenance, heavy compute, network management, storage    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 1.2 Network Topology

The airship network uses a **tiered hexagonal grid** with three density levels:

```
  HIGH-DENSITY ZONE (urban corridors, major farming regions)
  Airship spacing: ~30 km — every point covered by 2-3 airships

       ·  30km  ·  30km  ·  30km  ·
      / \      / \      / \      / \
     /   \    /   \    /   \    /   \
    · ─── · ─── · ─── · ─── · ─── ·
     \   /    \   /    \   /    \   /
      \ /      \ /      \ /      \ /
       ·  ─── · ─── · ─── · ─── ·

  MEDIUM-DENSITY ZONE (rural, coastal)
  Airship spacing: ~50 km — every point covered by 1-2 airships

       ·      50km       ·       50km      ·
      / \               / \               / \
     /   \             /   \             /   \
    ·     · ───────── ·     · ───────── ·     ·

  LOW-DENSITY ZONE (remote highlands, open ocean)
  Airship spacing: ~80-100 km — coverage gaps acceptable, satellite backup

       ·              100km               ·
      / \                                / \
     /   \                              /   \
    ·     · ──────────────────────── ·     ·
```

### 1.3 Airship Positioning Strategy

Airships are positioned using three concurrent strategies:

**Fixed station-keeping positions (60% of fleet)**
These airships hold position over strategically valuable locations: above major agricultural regions (East Anglia, Lincolnshire, Welsh Borders), above port cities (Southampton, Liverpool, Felixstowe), above military areas (Salisbury Plain, Lossiemouth corridor), and above emergency service corridors (M1/M6 motorway spine, major conurbations). Each has a station-keeping box of approximately 10 km radius within which it drifts and returns using wind-layer surfing or low-power thrusters.

**Patrol routes (25% of fleet)**
These airships follow repeating circuits. A coastal airship might follow a 400 km figure-eight pattern along the southwest coast, providing rolling coverage that returns to each point every 12-24 hours. Agricultural patrol airships follow seasonal routes — concentrating over arable land during spring/autumn and shifting to upland pastoral areas in summer.

**On-demand repositioning (15% of fleet)**
Reserve airships that the network controller can redirect to surge areas. A major incident, a harvest peak, a military exercise, or a scientific campaign generates a demand spike — the network pulls reserve airships from low-demand areas toward the hot zone. Transit speed of tropospheric airships at 3-8 km altitude: 50-80 km/h, meaning a reserve airship can reposition 200 km in 3-4 hours.

### 1.4 Backbone Connectivity Between Airships

Each airship-to-airship link uses one or more of three technologies:

```
  AIRSHIP A                                              AIRSHIP B
  ┌──────────────────────┐                              ┌──────────────────────┐
  │                      │    ═══ FSO LASER LINK ═══    │                      │
  │  FSO terminal ───────┼──── 1-10 Gbps, 30-80 km ───┼─── FSO terminal      │
  │  (clear weather)     │    atmospheric dependent     │                      │
  │                      │                              │                      │
  │  Directional RF ─────┼──── 50-500 Mbps, 80+ km ───┼─── Directional RF    │
  │  (Ku/Ka-band dish)   │    all-weather backup        │  (Ku/Ka-band dish)   │
  │                      │                              │                      │
  │  SATCOM terminal ────┼──── via LEO relay ──────────┼─── SATCOM terminal   │
  │  (fallback only)     │    10-100 Mbps, any range    │  (fallback only)     │
  └──────────────────────┘                              └──────────────────────┘

  PRIMARY:   FSO laser link — highest bandwidth, lowest latency, but fails in
             fog/rain/cloud. Airships at 3-8 km altitude are often above low
             cloud, so FSO reliability is higher than ground-to-ground.

  SECONDARY: Directional RF — works in all weather, provides sufficient
             bandwidth for most cross-airship traffic. Uses mechanically
             steered parabolic dishes or phased arrays.

  TERTIARY:  SATCOM relay via Starlink/OneWeb — used only when airships are
             beyond RF line-of-sight or both FSO and RF fail. Higher latency
             (~20-40 ms for LEO) but global reach.
```

### 1.5 Coverage Map: UK National Network

```
  ╔══════════════════════════════════════════════════════════╗
  ║               UK AIRSHIP NETWORK COVERAGE                ║
  ║            (Minimum Viable: 35 airships)                 ║
  ╠══════════════════════════════════════════════════════════╣
  ║                                                          ║
  ║            SCOTLAND                                      ║
  ║              ·  Highlands patrol (2 airships)            ║
  ║             · ·                                          ║
  ║            ·   ·  Central Belt fixed (3)                 ║
  ║             · ·   (Glasgow-Edinburgh corridor)           ║
  ║              ·                                           ║
  ║             · ·   East coast patrol (1)                  ║
  ║            ·   ·                                         ║
  ║           ─────── Border ──────                          ║
  ║                                                          ║
  ║            NORTH ENGLAND                                 ║
  ║              ·  · ·   Newcastle-Tees fixed (2)           ║
  ║             ·       ·                                    ║
  ║            ·  · · ·   M62 corridor fixed (3)             ║
  ║           · ·     · ·  (Liverpool-Leeds)                 ║
  ║                                                          ║
  ║            MIDLANDS                                      ║
  ║              · · · ·   Birmingham-Nottingham fixed (3)   ║
  ║             ·       ·                                    ║
  ║            · ·     · ·                                   ║
  ║                                                          ║
  ║            EAST ANGLIA                                   ║
  ║              · · · · ·  Agricultural dense (4)           ║
  ║             ·         ·  (Norfolk/Suffolk/Cambs/Lincs)   ║
  ║                                                          ║
  ║            SOUTH EAST                                    ║
  ║              · · · ·   London periphery fixed (4)        ║
  ║             ·       ·   (no overflight of central        ║
  ║            ·         ·   London — restricted airspace)   ║
  ║              · · · ·                                     ║
  ║                                                          ║
  ║            SOUTH WEST                                    ║
  ║              · · ·     Bristol-Plymouth corridor (2)     ║
  ║             ·     ·                                      ║
  ║                                                          ║
  ║            WALES                                         ║
  ║              · ·       Cardiff fixed (1)                 ║
  ║             ·   ·      North Wales patrol (1)            ║
  ║                                                          ║
  ║            COASTAL                                       ║
  ║              · · · · · · · · · ·                         ║
  ║              Coastal patrol ring (6 airships)            ║
  ║              30 km offshore, figure-eight patterns       ║
  ║              Full coastline coverage on 18-24 hr cycle   ║
  ║                                                          ║
  ║            RESERVE                                       ║
  ║              3 airships on standby at strategic bases    ║
  ║              (Lossiemouth, Brize Norton, Plymouth)       ║
  ║                                                          ║
  ╠══════════════════════════════════════════════════════════╣
  ║  TOTAL: 35 airships for minimum viable national cover    ║
  ║                                                          ║
  ║  FULL NETWORK: 55-70 airships for double-coverage        ║
  ║  everywhere plus dedicated sector airships               ║
  ╚══════════════════════════════════════════════════════════╝
```

---

## 2. UNIVERSAL RESOURCE REQUEST PROTOCOL (URP)

### 2.1 Protocol Overview

The URP is a lightweight, UDP-based discovery protocol layered on top of MAVLink v3 (extending the standard with custom message IDs in the 50000-51000 range). Every drone and airship in the network runs a URP daemon that handles resource discovery, negotiation, allocation, and billing.

The protocol operates in four phases:

```
  PHASE 1: DISCOVERY           PHASE 2: NEGOTIATION
  ┌─────────┐                  ┌─────────┐
  │  DRONE  │── BROADCAST ──►  │ AIRSHIP │
  │         │   ResourceReq    │   (A)   │──► evaluates capacity
  │         │                  └─────────┘    ──► checks priority
  │         │                  ┌─────────┐    ──► calculates cost
  │         │── BROADCAST ──►  │ AIRSHIP │
  │         │   ResourceReq    │   (B)   │──► evaluates capacity
  └─────────┘                  └─────────┘

  ┌─────────┐                  ┌─────────┐
  │  DRONE  │◄── UNICAST ────  │ AIRSHIP │
  │         │   ResourceOffer  │   (A)   │  offer: 800W, 3s wait
  │         │                  └─────────┘
  │         │◄── UNICAST ────  ┌─────────┐
  │         │   ResourceOffer  │ AIRSHIP │  offer: 600W, 12s wait
  └─────────┘                  │   (B)   │
                               └─────────┘

  PHASE 3: ALLOCATION          PHASE 4: SERVICE
  ┌─────────┐                  ┌─────────┐
  │  DRONE  │── UNICAST ────►  │ AIRSHIP │
  │         │  ResourceAccept  │   (A)   │──► allocates resource
  │         │  (picks best     └─────────┘    ──► begins tracking
  │         │   offer)                        ──► starts billing
  │         │                  ┌─────────┐
  │         │── UNICAST ────►  │ AIRSHIP │
  │         │  ResourceDecline │   (B)   │──► frees reservation
  └─────────┘                  └─────────┘

  ┌─────────┐                  ┌─────────┐
  │  DRONE  │◄═══ LASER ═════  │ AIRSHIP │  SERVICE ACTIVE
  │  (PV    │    POWER BEAM    │   (A)   │  ──► tracking drone
  │  panels │                  │         │  ──► monitoring power
  │  receiv)│══► TELEMETRY ══► │         │  ──► logging usage
  └─────────┘                  └─────────┘
```

### 2.2 Message Definitions

**ResourceRequest (Drone to Network — Broadcast)**

```
  ╔═══════════════════════════════════════════════════════════════╗
  ║  RESOURCE REQUEST MESSAGE                                     ║
  ╠═══════════════════════════════════════════════════════════════╣
  ║                                                               ║
  ║  Header                                                       ║
  ║  ├── msg_id:          50001 (URP_RESOURCE_REQUEST)            ║
  ║  ├── timestamp:       uint64 (Unix microseconds)              ║
  ║  ├── sequence:        uint32                                  ║
  ║  └── ttl:             uint8 (hops remaining, default 3)       ║
  ║                                                               ║
  ║  Identity                                                     ║
  ║  ├── drone_id:        uint32 (globally unique)                ║
  ║  ├── drone_class:     enum { MICRO, MINI, MEDIUM, LARGE,     ║
  ║  │                          CARGO, VTOL, HALE }               ║
  ║  ├── sector:          enum { AGRICULTURE, SCIENCE, MILITARY,  ║
  ║  │                          MARINE, CONSERVATION, LOGISTICS,  ║
  ║  │                          EMERGENCY, CIVILIAN, GOV_OTHER }  ║
  ║  ├── operator_id:     uint32 (registered operator)            ║
  ║  └── auth_token:      bytes[32] (signed certificate hash)     ║
  ║                                                               ║
  ║  Position & Kinematics                                        ║
  ║  ├── lat:             int32 (degE7)                           ║
  ║  ├── lon:             int32 (degE7)                           ║
  ║  ├── alt_msl:         int32 (mm)                              ║
  ║  ├── heading:         uint16 (cdeg, 0-35999)                  ║
  ║  ├── groundspeed:     uint16 (cm/s)                           ║
  ║  └── vertical_speed:  int16 (cm/s)                            ║
  ║                                                               ║
  ║  Request                                                      ║
  ║  ├── resource_type:   bitmask uint16                          ║
  ║  │   ├── bit 0: POWER                                         ║
  ║  │   ├── bit 1: COMPUTE                                       ║
  ║  │   ├── bit 2: COMMS                                         ║
  ║  │   ├── bit 3: DATA                                          ║
  ║  │   ├── bit 4: STORAGE                                       ║
  ║  │   └── bit 5: RESUPPLY                                      ║
  ║  ├── priority:        enum { ROUTINE=0, PRIORITY=1,           ║
  ║  │                          URGENT=2, EMERGENCY=3 }           ║
  ║  ├── quantity:        uint32 (resource-specific units)        ║
  ║  │   POWER:   watts requested                                 ║
  ║  │   COMPUTE: GFLOPS requested                                ║
  ║  │   COMMS:   kbps bandwidth                                  ║
  ║  │   DATA:    data_type enum + region bounding box            ║
  ║  │   STORAGE: megabytes                                       ║
  ║  │   RESUPPLY: resupply_type enum + quantity                  ║
  ║  ├── duration:        uint32 (seconds, 0 = until cancelled)   ║
  ║  └── max_cost:        uint32 (cost tokens, 0 = any cost)      ║
  ║                                                               ║
  ╚═══════════════════════════════════════════════════════════════╝
```

**ResourceOffer (Airship to Drone — Unicast)**

```
  ╔═══════════════════════════════════════════════════════════════╗
  ║  RESOURCE OFFER MESSAGE                                       ║
  ╠═══════════════════════════════════════════════════════════════╣
  ║                                                               ║
  ║  Header                                                       ║
  ║  ├── msg_id:          50002 (URP_RESOURCE_OFFER)              ║
  ║  ├── timestamp:       uint64                                  ║
  ║  ├── in_reply_to:     uint32 (sequence of original request)   ║
  ║  └── offer_id:        uint32 (unique for this negotiation)    ║
  ║                                                               ║
  ║  Airship Identity                                             ║
  ║  ├── airship_id:      uint32                                  ║
  ║  ├── airship_class:   enum { STRATO, TROPO, LOW, TETHERED }  ║
  ║  ├── lat/lon/alt:     (same encoding as request)              ║
  ║  └── auth_token:      bytes[32]                               ║
  ║                                                               ║
  ║  Offer Details                                                ║
  ║  ├── available_qty:   uint32 (what can actually be provided)  ║
  ║  ├── service_start:   uint32 (seconds from now)               ║
  ║  │   0 = immediate, >0 = need to reposition/queue             ║
  ║  ├── service_quality: uint8 (0-100 confidence score)          ║
  ║  │   accounts for weather, angle, distance, load              ║
  ║  ├── cost_per_unit:   uint32 (tokens per watt-second,         ║
  ║  │                    per GFLOP, per MB, etc.)                 ║
  ║  ├── estimated_total: uint32 (total cost tokens)              ║
  ║  └── offer_expiry:    uint32 (seconds until offer void)       ║
  ║                                                               ║
  ║  Constraints                                                  ║
  ║  ├── max_duration:    uint32 (seconds, 0 = unlimited)         ║
  ║  ├── drone_must_be:   bitmask {                               ║
  ║  │   IN_RANGE, ABOVE_MIN_ALT, BELOW_MAX_ALT,                 ║
  ║  │   HEADING_TOWARD, SPEED_BELOW }                            ║
  ║  └── notes:           string[64] (human-readable constraint)  ║
  ║                                                               ║
  ╚═══════════════════════════════════════════════════════════════╝
```

**ResourceAccept / ResourceDecline / ResourceRelease (transaction control)**

```
  ResourceAccept   (50003): drone_id, offer_id, auth_token
  ResourceDecline  (50004): drone_id, offer_id, reason_code
  ResourceRelease  (50005): drone_id, offer_id (early termination)
  ResourceStatus   (50006): offer_id, usage_so_far, quality_metric, est_remaining
  ResourceComplete (50007): offer_id, total_usage, total_cost, quality_report
```

### 2.3 Priority and Pre-emption System

The network uses a three-tier priority system:

```
  ╔══════════════════════════════════════════════════════════════════════╗
  ║  PRIORITY TIER 1: MANDATORY (cannot be refused, pre-empts all)     ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║                                                                     ║
  ║  EMERGENCY services in active emergency (SAR, fire, flood)         ║
  ║  Military in declared national defence operations                   ║
  ║  Network integrity (airship-to-airship backbone maintenance)       ║
  ║                                                                     ║
  ║  These requests ALWAYS succeed. If the airship is at capacity,     ║
  ║  it pre-empts lower-priority services. Pre-empted drones receive   ║
  ║  a ResourcePreempt message with 30-second warning to transition    ║
  ║  to battery or find another airship.                               ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║  PRIORITY TIER 2: GUARANTEED (reserved capacity, high reliability) ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║                                                                     ║
  ║  Government operations (environmental monitoring, coast guard)      ║
  ║  Contract holders with SLA (agricultural operators, logistics      ║
  ║  companies that pay for guaranteed capacity)                        ║
  ║  Scientific missions with pre-booked allocations                   ║
  ║                                                                     ║
  ║  These requests succeed if capacity is available within the        ║
  ║  reserved pool. They cannot be pre-empted by Tier 3 but CAN       ║
  ║  be pre-empted by Tier 1.                                         ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║  PRIORITY TIER 3: BEST-EFFORT (market-priced, no guarantees)      ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║                                                                     ║
  ║  All other users: hobby, small commercial, conservation (unless    ║
  ║  subsidised to Tier 2), civilian research                          ║
  ║                                                                     ║
  ║  Priced dynamically based on demand. During low demand: cheap.     ║
  ║  During high demand or capacity crunch: expensive or unavailable.  ║
  ║  Can be pre-empted by Tier 1 or Tier 2 with warning.              ║
  ╚══════════════════════════════════════════════════════════════════════╝
```

Within each tier, requests are ordered by:
1. **Time sensitivity** — a drone at 5% battery beats a drone at 40% battery
2. **First-come-first-served** — equal urgency resolved by arrival time
3. **Cost bid** — in Tier 3 only, higher bidders served first (market mechanism)

### 2.4 Resource Allocation Flow

```
  TIME ──────────────────────────────────────────────────────────►

  DRONE                          NETWORK                    AIRSHIP
  ──────                         ───────                    ───────

  Battery at 30%
  Mission requires 45 more
  minutes of flight
  ─── calculate: need 400W ──►
                                 Broadcast on URP
                                 discovery channel
                                 (915 MHz LoRa or
                                 2.4 GHz mesh)
                                 ────────────────────►
                                                        Airship A: 3 km away
                                                        Current load: 60%
                                                        Laser 3 free
                                                        ── calculate offer ──
                                 ◄────────────────────
                                 Offer: 500W, 2s start
                                 cost: 12 tokens/min
                                                        Airship B: 8 km away
                                                        Current load: 30%
                                                        ── calculate offer ──
                                 ◄────────────────────
                                 Offer: 400W, 8s start
                                 cost: 8 tokens/min

  Compare offers:
  A is faster, more power,
  but costs more.
  Choose A (time-critical).
  ─── ResourceAccept(A) ────►
  ─── ResourceDecline(B) ───►
                                                        Airship A:
                                                        ── slew laser 3 ──
                                                        ── acquire drone PV ──
                                                        ── begin power xfer ──
                                 ◄────────────────────
                                 ResourceStream: ACTIVE
  ◄═══ LASER POWER ════════════════════════════════════
       400-500W received
       Battery charging

  ... 35 minutes later ...

  Battery at 85%
  Mission complete soon
  ─── ResourceRelease ──────►
                                                        ── cease laser ──
                                                        ── log: 35 min,
                                                           420 tokens ──
                                 ◄────────────────────
                                 ResourceComplete
```

---

## 3. CROSS-SECTOR SCENARIOS

### Scenario A: Marine Airship Helps Agricultural Drone

```
  SITUATION:
  ── March, East Anglia. Spring spraying season.
  ── Agricultural drone (MEDIUM class, 35 kg) spraying winter wheat
  ── 28 km from its ground base, battery at 18%
  ── Nearest agricultural airship is 45 km away (serving Norfolk)
  ── BUT: a Marine survey airship is 12 km away, just off the Suffolk coast,
     conducting fisheries survey

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  ····· COAST ·····                                                 │
  │                    ·                                                │
  │  MARINE AIRSHIP     ·        28 km inland                         │
  │  [M] alt: 4 km      ·                                             │
  │  ║                    ·       AG DRONE [D]                         │
  │  ║ 12 km range        ·      alt: 50 m                            │
  │  ║ (laser can reach   ·      battery: 18%                         │
  │  ║  30 km from 4 km    ·     spraying wheat                       │
  │  ║  altitude)           ·                                          │
  │  ║                       ·                                         │
  │  ╚══ laser beam ═════════╗                                         │
  │       slant range: 12 km  ║                                        │
  │       (well within 30 km  ║                                        │
  │        capability)        ▼                                        │
  │                          [D] receives 350W                         │
  │                          continues spraying                        │
  │                          45 more minutes                           │
  │                                                                     │
  │  Without network: drone abandons mission, 8 hectares unsprayed     │
  │  With network:    drone completes mission, marine airship loses    │
  │                   <5% of its power capacity for 45 minutes         │
  └─────────────────────────────────────────────────────────────────────┘

  PROTOCOL EXCHANGE:
  1. Drone broadcasts ResourceRequest(POWER, 400W, ROUTINE, sector=AGRICULTURE)
  2. Marine airship responds: ResourceOffer(350W, 3s start, quality=82%)
     — 82% quality because slant range is 12 km and it is a cross-sector
       service (marine airship's laser is optimised for nadir, not lateral)
  3. Agricultural airship (45 km away) also responds: ResourceOffer(500W,
     180s start, quality=45%) — low quality due to extreme range
  4. Drone accepts marine airship's offer (faster, better quality)
  5. Marine airship slews laser 3 from nadir (fisheries) to lateral (drone)
     — fisheries survey pauses on that one laser, other 5 lasers continue
  6. 45 minutes later: drone releases, marine airship resumes full fisheries
  7. Billing: agricultural operator pays marine operator 420 tokens
```

### Scenario B: Military Drone Uses Civilian Compute Infrastructure

```
  SITUATION:
  ── Military ISR drone on border patrol exercise, Scottish Highlands
  ── Collecting 4K video at 60 fps = ~1.5 GB/min raw
  ── Needs real-time object detection + terrain mapping
  ── Nearest military compute facility: RAF Lossiemouth, 180 km away
  ── Bandwidth to Lossiemouth via satellite: 20 Mbps (too slow for raw video)
  ── BUT: an agricultural survey airship is 15 km away over farmland,
     with 50 TFLOPS of edge compute sitting 80% idle

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  SECURITY MODEL FOR CROSS-SECTOR COMPUTE                        ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Military drone NEVER sends raw classified data to civilian      ║
  ║  infrastructure. Instead:                                        ║
  ║                                                                   ║
  ║  1. Drone encrypts raw video with AES-256-GCM                   ║
  ║  2. Uploads encrypted blob to airship                            ║
  ║  3. Airship receives a SEALED COMPUTE CONTAINER:                 ║
  ║     ┌──────────────────────────────────────┐                     ║
  ║     │  Encrypted container (from MoD)       │                    ║
  ║     │  ├── Encrypted ML model weights       │                    ║
  ║     │  ├── Encrypted input (video frames)   │                    ║
  ║     │  ├── WASM runtime sandbox             │                    ║
  ║     │  └── Signed output channel            │                    ║
  ║     └──────────────────────────────────────┘                     ║
  ║                                                                   ║
  ║  4. The airship's compute runs the container in a hardware-      ║
  ║     isolated enclave (ARM TrustZone or Intel SGX equivalent)     ║
  ║  5. The enclave decrypts, processes, re-encrypts results         ║
  ║  6. Airship receives ONLY encrypted output — cannot inspect      ║
  ║  7. Encrypted results returned to drone or forwarded to MoD     ║
  ║                                                                   ║
  ║  The airship operator sees:                                      ║
  ║  ── "Compute job: 12 TFLOPS for 300 seconds, sealed container"  ║
  ║  ── It does NOT see: what the data is, what the model does,     ║
  ║     or what the output contains                                  ║
  ║                                                                   ║
  ║  This is analogous to how cloud providers run encrypted          ║
  ║  workloads today (AWS Nitro Enclaves, Azure Confidential        ║
  ║  Computing) — proven technology, adapted for airship edge.       ║
  ╚═══════════════════════════════════════════════════════════════════╝

  OUTCOME:
  ── Drone gets real-time object detection with 2-3 second latency
     (vs 15+ seconds via satellite to Lossiemouth)
  ── Agricultural airship earns revenue from idle compute
  ── Military data security maintained via hardware enclaves
  ── MoD saves millions by not deploying dedicated compute airships
     for every exercise
```

### Scenario C: Emergency Services Commandeer the Network

```
  SITUATION:
  ── January. Severe flooding across Somerset Levels.
  ── 200 km² area flooded, 15 villages cut off
  ── Emergency services deploy 40 SAR drones
  ── SAR drones need: continuous power, high-bandwidth comms to
     incident command, real-time mapping, thermal imaging processing

  TIMELINE:
  ═════════════════════════════════════════════════════════════════

  T+0:00  COBRA declares major incident
          Network controller receives EMERGENCY OVERRIDE code
          (signed by Home Office emergency authority)

  T+0:02  All airships within 150 km receive EMERGENCY PRIORITY SHIFT:
          ┌────────────────────────────────────────────────────┐
          │  AFFECTED AIRSHIPS:                                │
          │                                                    │
          │  [AG-1] Agricultural, Taunton Deane — 30 km       │
          │         STATUS: Pause crop survey. Redirect all    │
          │         lasers to SAR drone support.               │
          │         COMMS: Allocate 80% bandwidth to emergency │
          │                                                    │
          │  [AG-2] Agricultural, Bridgwater — 15 km          │
          │         STATUS: Directly overhead flood zone.      │
          │         Full resource allocation to emergency.     │
          │         Becomes PRIMARY RELAY NODE.                │
          │                                                    │
          │  [SC-1] Scientific, Bristol Channel — 45 km       │
          │         STATUS: Pause marine atmospheric study.    │
          │         Provide weather data feed to incident      │
          │         command. Redirect 4 of 6 lasers to SAR.   │
          │                                                    │
          │  [CO-1] Coastal patrol, Severn estuary — 40 km    │
          │         STATUS: Reposition toward flood zone.      │
          │         ETA to optimal position: 45 minutes.       │
          │         Will provide additional power + comms.     │
          │                                                    │
          │  [RES-1] Reserve airship, Brize Norton — 90 km    │
          │          STATUS: Deploying to flood zone.          │
          │          ETA: 2 hours. Heavy compute + storage.    │
          └────────────────────────────────────────────────────┘

  T+0:05  First SAR drones are airborne.
          Each broadcasts ResourceRequest(POWER, EMERGENCY)
          AG-2 (overhead) immediately begins powering 8 drones
          simultaneously via its 8 laser tracking systems

  T+0:10  40 SAR drones airborne. Network allocation:
          ┌──────────────────────────────────────────────┐
          │  AG-2 (overhead):  8 drones powered           │
          │  AG-1 (30 km):    6 drones powered            │
          │  SC-1 (45 km):    4 drones powered (long range)│
          │  Remaining 22:    on battery, queued for      │
          │                   power as airships reposition │
          └──────────────────────────────────────────────┘

  T+0:45  CO-1 arrives at optimal position. Now powering 8 more drones.
          Queue drops to 14 drones on battery.

  T+2:00  RES-1 arrives. Heavy compute processes thermal imagery from
          all 40 drones, building real-time flood map. Storage receives
          all raw sensor data. 6 more drones powered.

  T+2:30  Full network operational:
          ── 32 of 40 drones continuously laser-powered (indefinite endurance)
          ── 8 drones rotating through power queues (20 min powered, 10 min
             battery while transitioning between airship coverage)
          ── Incident command has real-time composite map updated every 30s
          ── All SAR drone video relayed to command via airship backbone
          ── Weather predictions fed to drone autopilots for safety

  T+72:00 Flood recedes. Emergency override released.
          Airships resume primary missions within 2 hours.
          Agricultural operators compensated from emergency fund.

  ═════════════════════════════════════════════════════════════════

  WITHOUT UNIFIED NETWORK:
  ── SAR drones limited to 45-90 min endurance each
  ── Need 3x as many drones to maintain coverage through battery swaps
  ── No persistent aerial communications relay
  ── No real-time composite mapping (each drone sends to separate systems)
  ── Days of reduced capability during the critical 72-hour window
```

### Scenario D: Long-Range Cargo Delivery via Airship Corridor

```
  MISSION: Deliver 3 kg of blood products from London to Edinburgh (530 km)
  DRONE: MEDIUM class, 35 kg MTOW, cruise speed 30 m/s, battery endurance 3 hrs
  PROBLEM: Battery range ~320 km. Edinburgh is 530 km. Drone cannot make it.

  SOLUTION: Airship power corridor

  LONDON ════════════════════════════════════════════════ EDINBURGH
   START                                                    END
    ▼                                                       ▼

    [D]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[D]
    ║         ║         ║         ║         ║         ║
    ▼         ▼         ▼         ▼         ▼         ▼
   [A1]      [A2]      [A3]      [A4]      [A5]      [A6]
  London   Midlands  Nottingham  Leeds   Newcastle  Edinburgh
   SE        M1        corridor   M1       A1      periphery
  airship   airship   airship   airship   airship   airship

  FLIGHT PROFILE:
  ═══════════════════════════════════════════════════════════════

  Segment 1: London to Luton (50 km)
  ── Departs on battery, climbs to 2 km cruise altitude
  ── Airship A1 (London SE) acquires drone, begins laser power
  ── Drone enters "powered cruise" — drawing 200W from laser,
     battery charge maintained at 80%+
  ── Speed: 30 m/s = 28 min

  Segment 2: Luton to Northampton (70 km)
  ── HANDOFF: A1 transfers tracking to A2 (Midlands)
     ┌──────────────────────────────────────────────────┐
     │  HANDOFF PROTOCOL:                                │
     │  1. A1 notifies A2: "Drone D approaching your    │
     │     zone, currently on my laser 4, heading 350°,  │
     │     speed 30 m/s, PV panel orientation 12° pitch" │
     │  2. A2 acquires drone on its laser, begins        │
     │     tracking but does NOT transmit yet             │
     │  3. A2 confirms lock: "Ready to power"            │
     │  4. A1 ceases transmission                        │
     │  5. A2 begins transmission — gap: <500 ms         │
     │  6. Drone reports: "Power transfer nominal"       │
     └──────────────────────────────────────────────────┘
  ── Speed: 30 m/s = 39 min

  Segment 3: Northampton to Nottingham (80 km) — A3 powers
  Segment 4: Nottingham to Leeds (100 km) — A4 powers
  Segment 5: Leeds to Newcastle (100 km) — A5 powers
  Segment 6: Newcastle to Edinburgh (130 km) — A6 powers

  TOTAL:
  ── Distance: 530 km
  ── Time: ~4.9 hours at 30 m/s
  ── Battery on arrival: 75% (the laser kept it topped up throughout)
  ── Number of airship handoffs: 5
  ── Cost: ~2,400 tokens (spread across 6 operators)

  WITHOUT AIRSHIP CORRIDOR:
  ── Drone range: ~320 km
  ── Would need 2 intermediate ground stops for battery swap
  ── Each stop: 20-30 min (landing, swap, takeoff, climb)
  ── Total time: ~7 hours including stops
  ── Requires ground infrastructure at intermediate points
  ── Single point of failure at each ground station
```

### Scenario E: Conservation Drones Piggyback on Farming Infrastructure

```
  SITUATION:
  ── Suffolk Wildlife Trust monitoring breeding bitterns in reedbeds
  ── Budget: £15,000/year for aerial monitoring
  ── Cannot afford: own airship, own ground base, dedicated infrastructure
  ── CAN afford: 2 MINI drones with thermal cameras (£4,000)
  ── Remaining budget: £11,000 for operations

  THE ECONOMICS:

  ┌──────────────────────────────────────────────────────────────┐
  │  WITHOUT UNIFIED NETWORK:                                     │
  │                                                               │
  │  Each drone flight: 45-90 min endurance                      │
  │  Coverage per flight: ~5 km² (slow, methodical thermal scan) │
  │  Battery life: 300 cycles × £80 replacement = £160/yr/drone  │
  │  Flights per week: 3 (limited by volunteer availability)     │
  │  Annual coverage: ~780 km² of survey area                    │
  │  Data processing: manual, on laptop, days of delay           │
  │                                                               │
  │  Limitations: short flights, small area, no real-time data,  │
  │  no persistent monitoring, weather-dependent                  │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  WITH UNIFIED NETWORK:                                        │
  │                                                               │
  │  Suffolk already has 2 agricultural airships overhead         │
  │  (East Anglia is the UK's densest farming region)            │
  │                                                               │
  │  Conservation subscription: Tier 3 (best-effort)             │
  │  Cost: ~8 tokens/min for POWER, ~3 tokens/min for COMPUTE   │
  │  At off-peak rates (conservation flies dawn/dusk when        │
  │  agricultural demand is low): ~6 tokens/min total            │
  │                                                               │
  │  Token pricing (estimated): £0.02/token                      │
  │  Cost per hour of powered flight: £7.20                      │
  │  Cost per hour of compute: £3.60                             │
  │                                                               │
  │  Budget allocation:                                           │
  │  ── Drone hardware: £4,000                                   │
  │  ── Network subscription: £8,000/year                        │
  │  ── Reserve: £3,000                                          │
  │                                                               │
  │  £8,000 at £7.20/hr = 1,111 hours of powered flight/year    │
  │  (vs ~156 hours without network)                             │
  │                                                               │
  │  7x more flight time, plus:                                  │
  │  ── Persistent monitoring (drone stays up 6-8 hrs at a time) │
  │  ── Real-time thermal processing via airship compute         │
  │  ── Automatic bittern detection ML model on airship          │
  │  ── Data stored on airship, downloaded to trust servers daily│
  │  ── Weather data from airship improves flight planning       │
  │                                                               │
  │  The agricultural network was built for farming.             │
  │  Conservation gets world-class infrastructure as a           │
  │  side-effect, at marginal cost to the network.               │
  └──────────────────────────────────────────────────────────────┘

  SUBSIDY MODEL:
  ── DEFRA could subsidise conservation network access (like
     countryside stewardship schemes subsidise hedgerow planting)
  ── Agricultural operators benefit: regulatory goodwill,
     biodiversity credits, ESG reporting
  ── Wildlife trusts benefit: 7x capability for same budget
  ── Network operator benefits: revenue from otherwise idle capacity
  ── Win-win-win-win
```

---

## 4. ECONOMIC MODEL

> **Honest assessment:** The economics of this network do not close without government infrastructure funding. The airship fleet alone costs £200-500M+ in capital, and no single commercial sector generates sufficient revenue to justify that investment. The hybrid model below depends on government willingness to fund the backbone layer as strategic infrastructure — similar to how roads, ATC, and broadband backhaul are publicly funded. Without that public investment, the commercial layer cannot justify deployment.
>
> **Multi-sector revenue assumption caveat:** The revenue projections below assume simultaneous multi-sector use. In practice, certain uses block others — a military mission over an area typically excludes commercial operations in that airspace for security reasons. This reduces achievable simultaneous revenue by 20-40% compared to theoretical maximums.

### 4.1 Analysis of Options

**Option A: Government Infrastructure (like roads)**

Pros: Universal access, no profit motive distorting coverage, emergency access guaranteed by design, long-term investment horizon matches the infrastructure nature of the network.

Cons: Government procurement is slow (15-20 year procurement cycles for major defence/infrastructure projects). Political risk — a change of government could cancel the programme. No market mechanism to efficiently allocate resources. Taxpayer funds a network that primarily benefits commercial operators.

Verdict: Too slow and too politically vulnerable. The technology is moving too fast for government procurement timelines.

**Option B: Commercial Network (like cell towers)**

Pros: Fast deployment (commercial incentive to build coverage quickly). Market pricing efficiently allocates scarce resources. Private investment does not require taxpayer funding. Innovation incentives are strong.

Cons: Coverage gaps in unprofitable areas (remote highlands, open ocean). Emergency access requires regulation (like 999 calls must work on any network). Risk of monopoly — the first mover has enormous advantages. Rural/conservation/scientific users may be priced out.

Verdict: Fast but leaves critical gaps. Rural and emergency access requires regulation.

**Option C: Cooperative Model**

Pros: Each sector retains control of its own airships. Cross-sector sharing is voluntary and mutually beneficial. Lower capital requirement per sector.

Cons: Coordination is hard — who decides airship positioning? Free-rider problem — sectors that invest less still benefit from others' infrastructure. Quality of service varies between sectors. No single entity responsible for network integrity.

Verdict: Works for the mature network but struggles to bootstrap the initial deployment.

**Option D: Hybrid (Recommended for UK)**

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  RECOMMENDED: HYBRID MODEL                                       ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  LAYER 1: Government backbone (funded by MoD + DEFRA + DSIT)    ║
  ║  ────────────────────────────────────────────────────────────    ║
  ║  ── 10-12 strategically positioned airships covering:            ║
  ║     ── Military training areas (Salisbury Plain, Scotland)       ║
  ║     ── Major coastline segments (Channel, North Sea approaches)  ║
  ║     ── Emergency service corridors (M1/M6 spine)                 ║
  ║  ── These airships are government-owned, operated by a           ║
  ║     contracted private company (like NATS operates ATC)          ║
  ║  ── Emergency override authority rests with government           ║
  ║  ── Backbone inter-airship links are government-funded           ║
  ║  ── Cost: £200-500M capital, £50-100M/year operations            ║
  ║  ── Funded via: MoD budget (strategic asset), DEFRA (rural       ║
  ║     coverage), DSIT (digital infrastructure)                     ║
  ║                                                                   ║
  ║  LAYER 2: Commercial operators (market-funded)                   ║
  ║  ────────────────────────────────────────────────────────────    ║
  ║  ── 20-40 additional airships deployed by commercial operators   ║
  ║  ── Focus on profitable areas: East Anglia (agriculture),        ║
  ║     logistics corridors, offshore energy, port cities            ║
  ║  ── Sell resource access to all sectors at market rates           ║
  ║  ── Must comply with URP standard and accept emergency override  ║
  ║  ── Licensed by CAA (like cell operators licensed by Ofcom)      ║
  ║  ── Revenue model: per-use resource fees + subscription tiers    ║
  ║  ── Multiple operators allowed (prevents monopoly)               ║
  ║  ── Government offers spectrum and airspace priority to licensed  ║
  ║     operators (regulatory incentive to build coverage)           ║
  ║                                                                   ║
  ║  LAYER 3: Cooperative sharing (sector-funded)                    ║
  ║  ────────────────────────────────────────────────────────────    ║
  ║  ── Sectors that operate their own airships (e.g., Royal Navy,   ║
  ║     Environment Agency, large agricultural cooperatives)         ║
  ║     register them on the URP network                             ║
  ║  ── Their airships serve their primary mission BUT share idle    ║
  ║     capacity with the network                                    ║
  ║  ── Mutual aid agreements: "I share my spare capacity, you      ║
  ║     share yours when I need it"                                  ║
  ║  ── Token exchange between cooperative members is at cost        ║
  ║     (not market rate) — incentivises participation               ║
  ║                                                                   ║
  ║  LAYER 4: Subsidised access (government grants)                  ║
  ║  ────────────────────────────────────────────────────────────    ║
  ║  ── Conservation, scientific research, and rural community       ║
  ║     drone operations receive subsidised network access           ║
  ║  ── Funded via DEFRA environmental schemes, UKRI research       ║
  ║     grants, and levelling-up funds                               ║
  ║  ── Mechanism: government buys tokens in bulk at market rate,   ║
  ║     distributes to qualifying organisations at reduced rate     ║
  ║  ── Similar to how NHS buys medicines at negotiated prices      ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

### 4.2 Revenue and Cost Estimates

```
  CAPITAL COSTS (FULL NATIONAL NETWORK, 55 AIRSHIPS):
  ════════════════════════════════════════════════════

  Government backbone (12 airships):
  ── 4 × stratospheric platforms @ £15M each        = £60M
  ── 8 × tropospheric airships @ £20M each          = £160M
  ── Ground infrastructure (10 hubs) @ £5M each     = £50M
  ── Backbone comms (laser + RF inter-links)         = £30M
  ── Network management system                       = £20M
  ── Contingency (20%)                               = £64M
  ── TOTAL GOVERNMENT CAPITAL:                        £384M

  Commercial operators (35 airships):
  ── 35 × tropospheric airships @ £15-25M each      = £525-875M
  ── Ground infrastructure (20 hubs) @ £3M each     = £60M
  ── TOTAL COMMERCIAL CAPITAL:                        £585-935M

  Cooperative sector airships (8 airships):
  ── Owned by sectors (Navy, Environment Agency, etc.)
  ── Already in their budgets — marginal cost to join network
  ── URP integration per airship: ~£500K              = £4M

  TOTAL NATIONAL NETWORK CAPITAL: £973M - £1.32B

  ANNUAL OPERATING COSTS:
  ════════════════════════

  Per airship:
  ── Helium replenishment: £20-50K/year
  ── Maintenance and inspection: £200-500K/year
  ── Crew / remote operators: £100-200K/year
  ── Insurance: £50-150K/year
  ── Energy (ground systems): £30-80K/year
  ── TOTAL PER AIRSHIP: £400K - £1M/year

  Network total (55 airships): £22-55M/year

  REVENUE STREAMS:
  ════════════════

  Power (laser recharge):
  ── Average drone pays ~£7-15/hour of powered flight
  ── Estimated 50,000 drone-hours/month network-wide (mature network)
  ── Revenue: £4.2-9M/year

  Compute:
  ── £3-8/hour of edge compute
  ── 20,000 compute-hours/month
  ── Revenue: £0.7-1.9M/year

  Communications relay:
  ── £1-3/hour of relayed bandwidth
  ── 100,000 relay-hours/month
  ── Revenue: £1.2-3.6M/year

  Data and storage:
  ── Terrain, weather, map data subscriptions
  ── £500-2,000/month per commercial operator
  ── 200 operators
  ── Revenue: £1.2-4.8M/year

  TOTAL ANNUAL REVENUE: £7.3-19.3M/year (commercial operators only)
  ── Government airships subsidised from defence/DEFRA budgets
  ── Break-even for commercial operators: 8-15 years
  ── Viable with government subsidy for backbone + growing drone market

  The economic case improves dramatically as drone numbers grow.
  At 200,000 drone-hours/month (realistic by 2035-2040):
  ── Revenue: £29-77M/year
  ── Commercial operators profitable within 5-7 years
```

---

## 5. TECHNICAL SPECIFICATIONS

### 5.1 Standard Interfaces

Every drone and airship on the network must implement these standard interfaces:

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  STANDARD INTERFACE: LASER POWER RECEIVER                        ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Wavelength:       980 nm primary, 1550 nm eye-safe secondary    ║
  ║  PV cell type:     GaAs multi-junction, band-gap matched         ║
  ║  Conversion eff:   50-60% at 980 nm, 30-40% at 1550 nm          ║
  ║  Panel sizes:      (scaled by drone class)                       ║
  ║  ├── MICRO:        50 cm² (integrated into wing upper surface)   ║
  ║  ├── MINI:         200-400 cm² (dorsal panel)                    ║
  ║  ├── MEDIUM:       800-1600 cm² (dorsal panel + wing sections)   ║
  ║  └── LARGE:        3000-6000 cm² (dedicated dorsal array)        ║
  ║                                                                   ║
  ║  Beam acquisition: Corner-cube retroreflector (passive) for      ║
  ║                    initial laser tracking, switching to active    ║
  ║                    beacon (940 nm LED) once acquired              ║
  ║                                                                   ║
  ║  Safety:           Onboard power limiter — PV output capped at   ║
  ║                    drone's maximum charge rate. Excess power      ║
  ║                    dumped as heat via wing-surface radiator.      ║
  ║                                                                   ║
  ║  Connector:        Standardised power bus interface:              ║
  ║                    ── 12-52V DC output (class-dependent)          ║
  ║                    ── CAN bus status reporting                    ║
  ║                    ── Automatic MPPT (max power point tracking)   ║
  ║                                                                   ║
  ║  Ref: doc 31 (In-Flight Power Transfer) for detailed physics     ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  STANDARD INTERFACE: COMMUNICATIONS TRANSCEIVER                   ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  URP Discovery Channel:                                          ║
  ║  ├── Frequency:    915 MHz ISM (UK: 868 MHz) — LoRa modulation  ║
  ║  ├── Bandwidth:    125 kHz                                       ║
  ║  ├── Data rate:    ~5 kbps (sufficient for URP messages)         ║
  ║  ├── Range:        30-80 km (airship at altitude to drone)       ║
  ║  └── Purpose:      Resource discovery, negotiation, control      ║
  ║                                                                   ║
  ║  Data Channel (once resource allocated):                         ║
  ║  ├── Primary:      5.8 GHz directional link, 10-100 Mbps        ║
  ║  ├── Secondary:    2.4 GHz omnidirectional, 1-10 Mbps           ║
  ║  └── Tertiary:     UHF (433 MHz), 100 kbps (extreme range)      ║
  ║                                                                   ║
  ║  Protocol Stack:                                                  ║
  ║  ├── Physical:     As above (frequency-dependent)                ║
  ║  ├── Data link:    Custom TDMA (time-division, airship-managed)  ║
  ║  ├── Network:      IPv6 with airship as gateway/router           ║
  ║  ├── Transport:    UDP for telemetry, TCP for data transfer      ║
  ║  ├── Application:  MAVLink v3 + URP extensions (msg 50000+)     ║
  ║  └── Security:     TLS 1.3 for all data channels, WireGuard     ║
  ║                    VPN for military/government traffic            ║
  ║                                                                   ║
  ║  Ref: doc 23 (Mesh Network and Directional Comms) for RF detail  ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  STANDARD INTERFACE: COMPUTE                                      ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Job format:       WebAssembly (WASM) containers                 ║
  ║  ── Why WASM:      Platform-agnostic, sandboxed, fast startup,   ║
  ║                    supports Rust/C/C++/Python compilation         ║
  ║  ── Alternative:   OCI containers (Docker) for heavier workloads ║
  ║                                                                   ║
  ║  Job submission:                                                  ║
  ║  1. Drone uploads WASM binary + input data to airship            ║
  ║  2. Airship validates binary signature (prevent malicious code)  ║
  ║  3. Airship runs in isolated sandbox:                            ║
  ║     ── Memory limit: specified in job manifest                   ║
  ║     ── CPU time limit: specified in job manifest                 ║
  ║     ── Network access: NONE (sandboxed)                          ║
  ║     ── Filesystem: read-only input, write-only output            ║
  ║  4. Airship returns output data to drone                         ║
  ║                                                                   ║
  ║  Sealed compute (military/sensitive):                             ║
  ║  ── Job runs inside hardware enclave (TrustZone/SGX)             ║
  ║  ── Airship cannot inspect input, model, or output               ║
  ║  ── See Scenario B above                                         ║
  ║                                                                   ║
  ║  Typical airship compute hardware:                               ║
  ║  ── 4-8 × NVIDIA Jetson Orin modules (275 TOPS each)            ║
  ║  ── Total: 1,100-2,200 TOPS inference capability                 ║
  ║  ── General compute: ~50-100 TFLOPS FP32                        ║
  ║  ── Power draw: 200-500W (from solar/fuel cell)                  ║
  ║  ── Storage: 4-16 TB NVMe SSD (for data cache + job data)       ║
  ║                                                                   ║
  ║  Common workloads:                                                ║
  ║  ── Object detection on drone video (YOLO, RT-DETR)             ║
  ║  ── Photogrammetry / orthomosaic generation                      ║
  ║  ── Thermal anomaly detection                                    ║
  ║  ── LiDAR point cloud processing                                 ║
  ║  ── Crop health index calculation (NDVI from multispectral)      ║
  ║  ── Maritime vessel tracking and classification                   ║
  ║  ── Weather prediction (local mesoscale model)                   ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  STANDARD INTERFACE: IDENTITY AND AUTHENTICATION                  ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Identity model: Public Key Infrastructure (PKI)                 ║
  ║                                                                   ║
  ║  Root CA:          UK Drone Network Authority (government)       ║
  ║  Intermediate CAs: Sector authorities (MoD, DEFRA, CAA, etc.)   ║
  ║  Leaf certs:       Individual drones and airships                ║
  ║                                                                   ║
  ║  Certificate contents:                                            ║
  ║  ├── Drone/airship unique ID                                     ║
  ║  ├── Operator ID and organisation                                ║
  ║  ├── Sector classification                                       ║
  ║  ├── Priority tier authorisation                                 ║
  ║  ├── Permitted resource types (some drones may not access        ║
  ║  │   compute, some may not access military enclaves, etc.)       ║
  ║  ├── Billing account reference                                   ║
  ║  └── Expiry date (annual renewal required)                       ║
  ║                                                                   ║
  ║  Authentication flow:                                             ║
  ║  1. Drone includes auth_token in ResourceRequest                 ║
  ║     (hash of certificate, signed with private key)               ║
  ║  2. Airship verifies signature against known CA chain            ║
  ║  3. If verification fails: no service (ResourceDeny message)     ║
  ║  4. If verification passes: proceed with offer                   ║
  ║                                                                   ║
  ║  Certificate revocation:                                          ║
  ║  ── Airships cache CRL (certificate revocation list)             ║
  ║  ── Updated via backbone every 15 minutes                        ║
  ║  ── Stolen/compromised drones revoked within 15-30 minutes       ║
  ║  ── Emergency revocation: broadcast via backbone, <60 seconds    ║
  ║                                                                   ║
  ║  Remote ID integration:                                           ║
  ║  ── URP identity system extends CAA Remote ID requirements       ║
  ║  ── Every URP message includes Remote ID data (drone reg,        ║
  ║     operator reg, position, altitude, speed)                     ║
  ║  ── Airships serve as Remote ID relay nodes — forwarding         ║
  ║     drone positions to UTM (Unmanned Traffic Management)         ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  STANDARD INTERFACE: BILLING AND USAGE TRACKING                   ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Unit of account: NETWORK TOKEN (NT)                             ║
  ║  ── 1 NT ≈ £0.02 (pegged, adjusted quarterly)                   ║
  ║  ── Purchased in advance by operators (prepaid account)          ║
  ║  ── Government and emergency accounts: unlimited (post-paid)     ║
  ║                                                                   ║
  ║  Resource pricing (indicative):                                   ║
  ║  ├── POWER:   1 NT per watt-minute (1 kW for 1 hr = 60,000 NT  ║
  ║  │            = ~£1,200 — adjusted by demand multiplier)         ║
  ║  │            Off-peak multiplier: 0.3x                          ║
  ║  │            Peak multiplier: 2-5x                              ║
  ║  ├── COMPUTE: 1 NT per TFLOP-second                             ║
  ║  ├── COMMS:   1 NT per 10 MB transferred                        ║
  ║  ├── DATA:    1 NT per data query                                ║
  ║  ├── STORAGE: 1 NT per GB-hour                                   ║
  ║  └── RESUPPLY: negotiated per item                               ║
  ║                                                                   ║
  ║  Usage logging:                                                   ║
  ║  ── Every ResourceComplete message includes a signed usage       ║
  ║     record (drone_id, airship_id, resource_type, quantity,       ║
  ║     duration, cost, quality metrics)                              ║
  ║  ── Records stored on airship, synced to network billing         ║
  ║     system via backbone every hour                                ║
  ║  ── Monthly settlement between operators                         ║
  ║  ── Disputes resolved via signed records (non-repudiable)        ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 6. NETWORK RESILIENCE

### 6.1 Failure Modes and Mitigations

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  FAILURE: SINGLE AIRSHIP LOSS                                    ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Cause: Mechanical failure, weather damage, controlled descent   ║
  ║                                                                   ║
  ║  Impact:                                                          ║
  ║  ── Coverage gap of 30-50 km radius (depending on density zone)  ║
  ║  ── All drones currently serviced by that airship lose resource   ║
  ║  ── Backbone link broken between two network segments            ║
  ║                                                                   ║
  ║  Mitigation (automatic, within seconds):                         ║
  ║  1. GRACEFUL HANDOFF: If airship detects impending failure       ║
  ║     (gas leak, power loss, structural alert), it sends           ║
  ║     ResourcePreempt to all serviced drones with 60-second        ║
  ║     warning and the ID of nearest alternative airship            ║
  ║  2. DRONE AUTONOMY: Drones switch to battery power immediately.  ║
  ║     URP daemon re-broadcasts ResourceRequest. Neighbouring       ║
  ║     airships expand service radius to cover gap.                 ║
  ║  3. BACKBONE REROUTE: Backbone traffic routes around the lost    ║
  ║     node via alternative paths (mesh topology — every airship    ║
  ║     has 2-4 backbone links to neighbours)                        ║
  ║  4. NETWORK REBALANCE: Within 1-4 hours, reserve airship        ║
  ║     repositioned to fill gap. Neighbouring airships adjust       ║
  ║     station-keeping to partially close the hole.                 ║
  ║                                                                   ║
  ║  Design principle: No single airship is a single point of        ║
  ║  failure for any critical function. Every area within high-      ║
  ║  density zones is covered by at least 2 airships.                ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  FAILURE: MULTIPLE AIRSHIP LOSS (correlated failure)             ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Cause: Severe weather event (storm takes out 3-5 airships),     ║
  ║  coordinated attack, common-mode software fault                  ║
  ║                                                                   ║
  ║  Impact: Regional network collapse — large coverage gap          ║
  ║                                                                   ║
  ║  Mitigation:                                                      ║
  ║  1. GRACEFUL DEGRADATION: Network enters "degraded mode"         ║
  ║     ── Emergency services get ALL remaining capacity              ║
  ║     ── Tier 2 and 3 services suspended in affected region        ║
  ║     ── Drones revert to battery-only operation                   ║
  ║  2. SATELLITE FALLBACK: Drones switch comms to direct satellite  ║
  ║     (Starlink/Iridium terminals on MEDIUM+ drones)               ║
  ║  3. GROUND RELAY: Ground bases activate backup relay stations    ║
  ║     (lower bandwidth, shorter range, but available immediately)  ║
  ║  4. RAPID REDEPLOY: Reserve fleet + airships from unaffected     ║
  ║     regions reposition. ETA: 4-12 hours for partial restoration. ║
  ║  5. WEATHER AVOIDANCE: Airships receive weather forecasts 6-24   ║
  ║     hours ahead. If severe weather approaching, airships         ║
  ║     pre-emptively reposition or descend to shelter. The          ║
  ║     correlated-failure scenario is reduced by proactive action.  ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  FAILURE: BACKBONE LINK BREAK                                    ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Cause: Weather (fog breaks FSO), equipment failure, jamming     ║
  ║                                                                   ║
  ║  Impact: Network partitions — some airships cannot reach         ║
  ║  network management system or billing servers                    ║
  ║                                                                   ║
  ║  Mitigation:                                                      ║
  ║  1. MULTI-PATH ROUTING: Each airship maintains 2-4 backbone     ║
  ║     links. Traffic routes around broken links automatically      ║
  ║     (OSPF-like routing protocol adapted for airship network)     ║
  ║  2. AUTONOMOUS OPERATION: Each airship can operate independently ║
  ║     for 24-72 hours using cached data:                           ║
  ║     ── Cached CRL (certificate revocation list)                  ║
  ║     ── Cached terrain/weather data                               ║
  ║     ── Local billing ledger (settled when connectivity returns)  ║
  ║     ── Autonomous resource allocation (no central coordinator)   ║
  ║  3. SATELLITE BRIDGE: Any airship can bridge via SATCOM to       ║
  ║     reach the rest of the network (higher latency, lower         ║
  ║     bandwidth, but maintains connectivity)                       ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  FAILURE: CYBER ATTACK                                           ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Attack vectors:                                                  ║
  ║  ── Spoofed ResourceRequests (fake drones requesting resources)  ║
  ║  ── Man-in-the-middle on drone-airship link                     ║
  ║  ── Compromised drone certificate used to access network        ║
  ║  ── DDoS on URP discovery channel                                ║
  ║  ── Malicious compute job attempting to escape sandbox           ║
  ║                                                                   ║
  ║  Defences:                                                        ║
  ║  1. PKI AUTHENTICATION: Every message cryptographically signed.  ║
  ║     Spoofed requests fail signature verification. No valid cert  ║
  ║     = no service.                                                ║
  ║  2. TLS 1.3: All data channels encrypted end-to-end. MITM       ║
  ║     attacks defeated by certificate pinning.                     ║
  ║  3. RAPID REVOCATION: Compromised certificates revoked within    ║
  ║     15 minutes via backbone-distributed CRL. Emergency           ║
  ║     revocation in <60 seconds.                                   ║
  ║  4. RATE LIMITING: URP discovery channel rate-limited per        ║
  ║     certificate. DDoS from single source: blocked after 10       ║
  ║     requests/minute. DDoS from many sources: requires many       ║
  ║     compromised certificates (hard to obtain at scale).          ║
  ║  5. SANDBOX ISOLATION: Compute jobs run in WASM sandbox with     ║
  ║     no network access, limited memory, limited CPU time.         ║
  ║     Escape requires exploiting WASM runtime vulnerability        ║
  ║     (possible but difficult — WASM designed for this).           ║
  ║  6. INTRUSION DETECTION: Each airship runs anomaly detection     ║
  ║     on URP traffic patterns. Unusual request patterns (e.g.,     ║
  ║     100 drones requesting service from same location within      ║
  ║     10 seconds) trigger alert and temporary lockdown.            ║
  ║  7. NETWORK SEGMENTATION: Military traffic runs on separate      ║
  ║     virtual network (VLAN equivalent) within the same physical   ║
  ║     infrastructure. Compromise of civilian segment does not      ║
  ║     expose military traffic.                                     ║
  ╚═══════════════════════════════════════════════════════════════════╝

  ╔═══════════════════════════════════════════════════════════════════╗
  ║  FAILURE: DELIBERATE ADVERSARY TARGETING AIRSHIPS                ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  This is the fundamental vulnerability of the airship concept:   ║
  ║  airships are large, slow, and visible. They are easier to       ║
  ║  target than satellites but harder to replace.                   ║
  ║                                                                   ║
  ║  Mitigations (layered defence):                                  ║
  ║                                                                   ║
  ║  1. ALTITUDE: Tropospheric airships at 3-8 km are above most    ║
  ║     small arms, most small drones, and most MANPADS effective    ║
  ║     range. Stratospheric platforms at 18-20 km are above ALL     ║
  ║     conventional threats except dedicated SAM systems and        ║
  ║     military aircraft.                                           ║
  ║                                                                   ║
  ║  2. ESCORT DRONES: Government backbone airships carry 4-8       ║
  ║     counter-UAS drones (doc 18) that patrol a defensive         ║
  ║     perimeter. These intercept approaching hostile drones        ║
  ║     before they reach the airship.                               ║
  ║                                                                   ║
  ║  3. DISPERSAL: Rather than one large airship, the network uses  ║
  ║     many smaller airships spread across a wide area. Destroying  ║
  ║     one degrades the network 2-3%; destroying enough to          ║
  ║     collapse it requires attacking 10+ geographically dispersed  ║
  ║     targets simultaneously — a much harder military problem.     ║
  ║                                                                   ║
  ║  4. RAPID REPLACEMENT: Tropospheric airships can be deployed     ║
  ║     from ground storage in 4-12 hours. The network maintains a  ║
  ║     reserve of deflated airship envelopes and gondolas at        ║
  ║     strategic bases. A destroyed airship is replaced within      ║
  ║     24-48 hours (vs months for a satellite).                     ║
  ║                                                                   ║
  ║  5. MOBILITY: Under threat, airships can reposition at 50-80    ║
  ║     km/h — not fast enough to evade a missile, but fast enough  ║
  ║     to move away from a ground-based threat zone within hours.   ║
  ║                                                                   ║
  ║  6. DECEPTION: Cheap decoy balloons (£500-2,000 each) deployed  ║
  ║     near real airships. Radar cross-section and IR signature     ║
  ║     mimic real airships. Forces adversary to expend expensive    ║
  ║     weapons on cheap targets.                                    ║
  ║                                                                   ║
  ║  7. HARDENING: Airship envelopes designed with self-sealing     ║
  ║     inner layers and compartmentalised gas cells. Small          ║
  ║     punctures do not cause rapid deflation — helium leaks       ║
  ║     slowly through small holes. Airship can lose 10-20% of     ║
  ║     gas volume and still maintain altitude (at reduced payload). ║
  ║                                                                   ║
  ║  Honest assessment: In a peer-to-peer military conflict,        ║
  ║  airships are vulnerable. The network is designed for peacetime  ║
  ║  and asymmetric threat environments. In a full-scale conflict,  ║
  ║  the network degrades to satellite-only backbone and ground-    ║
  ║  based relay stations.                                           ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 7. SCALING CALCULATIONS

### 7.1 UK Coverage Analysis

```
  UK METRICS:
  ══════════
  Total land area:           242,495 km²
  Total coastline length:    31,368 km (including islands)
  Exclusive Economic Zone:   ~773,676 km² (sea area)
  Agricultural land:         ~171,000 km² (71% of land)
  Major urban areas:         ~15,000 km² (6% of land)
  Population:                ~67 million

  COVERAGE GEOMETRY:
  ══════════════════

  Airship coverage radius depends on altitude and resource type:

  ┌─────────────────────────────────────────────────────────────────┐
  │  COVERAGE RADIUS BY ALTITUDE AND RESOURCE                       │
  │                                                                  │
  │  Altitude   Laser Power    Comms Relay    Compute (via comms)  │
  │  ────────   ───────────    ───────────    ──────────────────   │
  │  500 m      5-10 km        15-25 km       15-25 km             │
  │  2 km       10-20 km       40-60 km       40-60 km             │
  │  5 km       15-30 km       80-120 km      80-120 km            │
  │  8 km       20-40 km       120-160 km     120-160 km           │
  │  20 km      30-60 km       300-500 km     300-500 km           │
  │                                                                  │
  │  Laser limited by: atmospheric absorption, beam divergence,    │
  │  receiver size, tracking accuracy                               │
  │  Comms limited by: line-of-sight horizon, frequency, power     │
  │  Compute limited by: comms bandwidth (same as comms range)     │
  └─────────────────────────────────────────────────────────────────┘

  SCENARIO 1: MINIMUM VIABLE NETWORK (power focus, 30 km radius)
  ═══════════════════════════════════════════════════════════════

  Coverage per airship (power): pi × 30² = 2,827 km²
  UK land coverage needed:      242,495 km²
  Raw count:                    242,495 / 2,827 = 86 airships

  BUT: hexagonal tiling is ~90.7% efficient (vs circles):
  Adjusted:                     86 / 0.907 = 95 airships

  This is FULL national coverage, every square metre.
  Not needed — most of Scotland's highlands have no drones.

  SCENARIO 2: PRAGMATIC NATIONAL NETWORK (coverage where needed)
  ═══════════════════════════════════════════════════════════════

  High-density zones (agricultural + urban corridors):
  ── Area: ~100,000 km² at 30 km radius spacing
  ── Airships: 100,000 / 2,827 = 36 airships

  Coastal coverage (30 km offshore strip):
  ── Strip area: 31,368 km × 30 km = ~940,000 km²
  ── But most coastline only needs one line of coverage
  ── Effective area: ~200,000 km² (major shipping lanes + fishing)
  ── At 50 km radius (comms-focused, not power):
     200,000 / (pi × 50²) = 26 airships
  ── But coastal airships overlap with land coverage
  ── Net additional coastal: ~15 airships

  Reserve and strategic:
  ── 3-5 reserve airships

  TOTAL PRAGMATIC: 36 + 15 + 5 = 56 airships

  SCENARIO 3: MINIMUM BOOTSTRAP (proof of viability)
  ═══════════════════════════════════════════════════

  East Anglia agricultural corridor only:
  ── Area: ~20,000 km²
  ── At 30 km radius: 8 airships
  ── Plus 2 coastal: 10 airships total
  ── Serves the UK's most intensive farming region
  ── Proves the concept, generates revenue, attracts investment

  SUMMARY:
  ┌──────────────────────────────────────────────────┐
  │  Network Scale     Airships    Coverage           │
  │  ──────────────    ────────    ────────           │
  │  Bootstrap         10          East Anglia only   │
  │  Regional          20-25       2-3 UK regions     │
  │  National (min)    35          Major corridors    │
  │  National (full)   55-70       Double coverage    │
  │  Total (inc sea)   70-95       Land + coastal     │
  └──────────────────────────────────────────────────┘
```

### 7.2 Capacity Calculations

```
  PER-AIRSHIP CAPACITY (tropospheric, 50-100 m class):
  ════════════════════════════════════════════════════

  Power generation:
  ── Solar array: 200-500 m² at 20-25% efficiency
  ── Peak solar power: 40-125 kW (midday, summer, UK latitude)
  ── Average solar power (annualised, UK): 15-50 kW
  ── Fuel cell backup: 10-20 kW continuous
  ── Total average available: 25-70 kW

  Power allocation:
  ── Propulsion + station-keeping: 5-15 kW
  ── Onboard systems (compute, comms, sensors): 3-8 kW
  ── Available for laser power beaming: 12-47 kW

  Laser power beaming capacity:
  ── Per laser: 1-5 kW output (electrical equivalent at receiver)
  ── Lasers per airship: 6-12 tracking systems
  ── Simultaneous drones powered: 6-12
  ── Power delivered per drone: 200-2,000 W (depending on range/class)
  ── At average 500W/drone: 12-24 drones simultaneously

  Compute capacity:
  ── 4-8 Jetson Orin modules: 50-100 TFLOPS
  ── Simultaneous compute jobs: 4-8 (one per module)
  ── Average job: 3-5 minutes (e.g., process 100 drone video frames)
  ── Throughput: ~100 jobs/hour

  Comms capacity:
  ── Backbone: 1-10 Gbps (FSO) + 50-500 Mbps (RF)
  ── Drone downlinks: 50-200 simultaneous connections
  ── Total drone bandwidth: 500 Mbps - 2 Gbps aggregate
  ── Per-drone average: 2.5-40 Mbps (sufficient for video streaming)

  Storage:
  ── 4-16 TB onboard NVMe
  ── Serves as local cache (terrain, weather, maps)
  ── Temporary storage for drone data offload
  ── Synced to ground storage via backbone

  NETWORK-WIDE CAPACITY (55 airships):
  ═════════════════════════════════════

  ── Simultaneous drones powered: 660-1,320
  ── Total laser power delivered: 330-660 kW (network-wide)
  ── Compute throughput: ~5,500 jobs/hour
  ── Aggregate drone comms: 27-110 Gbps
  ── Storage: 220-880 TB distributed cache
```

---

## 8. COMPARISON WITH EXISTING INFRASTRUCTURE MODELS

### 8.1 Analogous Systems

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  MODEL            SIMILARITY    KEY LESSON FOR AIRSHIP NETWORK   ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  CELL PHONE       ★★★★★        Closest analogy. Towers (airships)║
  ║  NETWORKS         (closest)    provide service to phones (drones) ║
  ║                                that roam between coverage areas.  ║
  ║                                Handoff between towers is seamless.║
  ║                                Multiple operators share spectrum. ║
  ║                                Emergency calls (999) work on any ║
  ║                                network. Regulated by Ofcom.       ║
  ║                                                                   ║
  ║                                Lesson: The cell network model     ║
  ║                                WORKS for multi-operator, multi-   ║
  ║                                user shared infrastructure. Copy   ║
  ║                                the regulatory framework (Ofcom    ║
  ║                                equivalent for airship network),   ║
  ║                                the roaming agreements, and the    ║
  ║                                emergency access mandates.         ║
  ║                                                                   ║
  ║  ─────────────────────────────────────────────────────────────── ║
  ║                                                                   ║
  ║  POWER GRID       ★★★★         Generation (solar on airships)    ║
  ║                                distributed to consumers (drones)  ║
  ║                                via transmission (laser beams).    ║
  ║                                Grid balancing = resource alloc.   ║
  ║                                Base load + peak demand pricing.   ║
  ║                                                                   ║
  ║                                Lesson: Power grid uses real-time  ║
  ║                                demand/supply matching and dynamic ║
  ║                                pricing. The airship network's     ║
  ║                                token pricing should follow this   ║
  ║                                model. Also: grid resilience via   ║
  ║                                redundant interconnections is      ║
  ║                                directly applicable.               ║
  ║                                                                   ║
  ║  ─────────────────────────────────────────────────────────────── ║
  ║                                                                   ║
  ║  INTERNET          ★★★★        Packet routing between nodes.     ║
  ║                                Airship backbone is essentially    ║
  ║                                an aerial internet with routers    ║
  ║                                (airships) forwarding packets.     ║
  ║                                BGP-like routing, OSPF-like link  ║
  ║                                state within the network.          ║
  ║                                                                   ║
  ║                                Lesson: The internet's layered     ║
  ║                                protocol stack (physical → data    ║
  ║                                link → network → transport →       ║
  ║                                application) is the right model    ║
  ║                                for URP. Also: net neutrality      ║
  ║                                debates are directly relevant to   ║
  ║                                cross-sector priority/pricing.     ║
  ║                                                                   ║
  ║  ─────────────────────────────────────────────────────────────── ║
  ║                                                                   ║
  ║  AIR TRAFFIC       ★★★         Central authority managing shared ║
  ║  CONTROL                       airspace between diverse users.    ║
  ║                                Flight plans, separation, priority ║
  ║                                (emergency > scheduled > general). ║
  ║                                                                   ║
  ║                                Lesson: ATC's priority system      ║
  ║                                (emergency > military > commercial)║
  ║                                maps directly to URP tiers.        ║
  ║                                ATC's concept of "flow control"    ║
  ║                                (limiting entries to congested     ║
  ║                                areas) is useful for managing      ║
  ║                                airship capacity during peaks.     ║
  ║                                                                   ║
  ║  ─────────────────────────────────────────────────────────────── ║
  ║                                                                   ║
  ║  GPS                ★★         Satellites provide service to any  ║
  ║                                receiver, any user, for free.      ║
  ║                                Government-funded, universally     ║
  ║                                available. No authentication       ║
  ║                                required (for civilian signal).    ║
  ║                                                                   ║
  ║                                Lesson: GPS shows that government- ║
  ║                                funded infrastructure can enable   ║
  ║                                massive commercial ecosystems.     ║
  ║                                The airship backbone (government-  ║
  ║                                funded) could catalyse a drone     ║
  ║                                economy worth billions, just as    ║
  ║                                GPS enabled the navigation and     ║
  ║                                logistics industries.              ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

### 8.2 The Best Analogy: Cellular Network + Power Grid Hybrid

The airship infrastructure network is most accurately described as **a cellular network that also transmits power**. The cell network analogy captures the coverage model, handoffs, multi-operator structure, and regulatory framework. The power grid analogy captures the energy distribution, demand matching, and pricing model.

No existing infrastructure does both simultaneously — this is the novel element. The closest precedent is Nikola Tesla's vision of wireless power transmission via a network of towers, now finally practical thanks to laser power beaming technology that did not exist in Tesla's era.

---

## 9. DEVELOPMENT ROADMAP

### Phase 1: Proof of Concept (2-3 years, £15-30M)

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  PHASE 1: SINGLE CORRIDOR DEMONSTRATOR                          ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Scope:                                                           ║
  ║  ── 2 tropospheric airships (prototype, 30-50 m class)           ║
  ║  ── 1 corridor: 60-80 km along East Anglia coast                ║
  ║  ── 1 automated ground base                                      ║
  ║  ── 10-20 test drones from 2-3 sectors (agriculture + science)  ║
  ║  ── Single-sector then cross-sector testing                      ║
  ║                                                                   ║
  ║  Key milestones:                                                  ║
  ║  Year 1:                                                          ║
  ║  ├── Airship 1 operational (single-sector, agriculture)          ║
  ║  ├── Laser power beaming to 5 drones simultaneously             ║
  ║  ├── Basic URP protocol: power + comms only                      ║
  ║  ├── Demonstrate 4-hour drone endurance (vs 90 min on battery)  ║
  ║  └── Cost: £8-15M                                                ║
  ║                                                                   ║
  ║  Year 2:                                                          ║
  ║  ├── Airship 2 operational — demonstrates HANDOFF between A1/A2 ║
  ║  ├── Cross-sector test: science drones use agricultural airship  ║
  ║  ├── URP v2: add compute and storage                             ║
  ║  ├── Demonstrate sealed compute (military-grade encryption test) ║
  ║  ├── Demonstrate emergency priority override                     ║
  ║  └── Cost: £5-10M                                                ║
  ║                                                                   ║
  ║  Year 3:                                                          ║
  ║  ├── Long-duration test: 30-day continuous network operation     ║
  ║  ├── Full URP v3: all 6 resource types operational               ║
  ║  ├── Billing system prototype: tokens, metering, settlement     ║
  ║  ├── Regulatory engagement: CAA, Ofcom, MoD                     ║
  ║  ├── Publish results, attract Phase 2 investment                 ║
  ║  └── Cost: £2-5M                                                 ║
  ║                                                                   ║
  ║  What Phase 1 proves:                                             ║
  ║  ── Laser power handoff between airships works in real weather   ║
  ║  ── Cross-sector resource sharing is technically feasible         ║
  ║  ── URP protocol is robust enough for multi-drone operations     ║
  ║  ── The economics pencil out (cost per drone-hour established)   ║
  ║  ── Regulatory pathway is viable                                 ║
  ║                                                                   ║
  ║  What Phase 1 does NOT prove:                                    ║
  ║  ── National-scale operations                                    ║
  ║  ── Full multi-operator commercial viability                     ║
  ║  ── Military-grade security at scale                             ║
  ║  ── Adversarial resilience                                       ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

### Phase 2: Regional Network (3-5 years from Phase 1 start, £100-250M)

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  PHASE 2: MULTI-REGION, MULTI-SECTOR NETWORK                    ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Scope:                                                           ║
  ║  ── 10-15 airships across 2-3 UK regions:                       ║
  ║     ── East Anglia (agriculture-focused, 4-5 airships)           ║
  ║     ── Southwest coast (marine + emergency, 3-4 airships)        ║
  ║     ── Central Scotland (military + science, 3-4 airships)       ║
  ║  ── 3-5 automated ground bases                                   ║
  ║  ── 50-200 operational drones across 5+ sectors                  ║
  ║  ── 2-3 network operators (commercial + government)              ║
  ║  ── Full URP with billing, authentication, priority system       ║
  ║                                                                   ║
  ║  Key milestones:                                                  ║
  ║  Year 3-4:                                                        ║
  ║  ├── East Anglia corridor expanded to full regional coverage     ║
  ║  ├── First commercial agricultural operator paying for service   ║
  ║  ├── First government airship (MoD) operational in Scotland     ║
  ║  ├── Cross-region backbone link: East Anglia ↔ Scotland         ║
  ║  ├── First conservation organisation on network (subsidised)     ║
  ║  └── Cost: £40-100M                                              ║
  ║                                                                   ║
  ║  Year 5:                                                          ║
  ║  ├── Southwest coastal network operational                       ║
  ║  ├── First emergency services exercise using network             ║
  ║  ├── Multi-operator URP interoperability demonstrated            ║
  ║  ├── Regulatory framework published (CAA + Ofcom + MoD)          ║
  ║  ├── 300+ km cargo corridor demonstrated (London ↔ Birmingham)  ║
  ║  ├── International interest: demos for NATO, EU partners         ║
  ║  └── Cost: £60-150M                                              ║
  ║                                                                   ║
  ║  What Phase 2 proves:                                             ║
  ║  ── Multi-region backbone connectivity                           ║
  ║  ── Multi-operator commercial model                              ║
  ║  ── Cross-sector resource sharing at scale                       ║
  ║  ── Emergency override system in realistic exercise              ║
  ║  ── Long-range corridor delivery viability                       ║
  ║  ── Regulatory compliance pathway proven                         ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

### Phase 3: National Network (5-10 years from start, £500M-1.3B cumulative)

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  PHASE 3: UK NATIONAL INFRASTRUCTURE                             ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  Scope:                                                           ║
  ║  ── 35-70 airships, full UK coverage (land + coastal)            ║
  ║  ── 10-20 automated ground bases                                  ║
  ║  ── 1,000+ operational drones across all sectors                 ║
  ║  ── 5+ commercial operators                                      ║
  ║  ── Government backbone fully operational                        ║
  ║  ── International interconnection (to European networks)         ║
  ║                                                                   ║
  ║  Target capabilities (mature network):                            ║
  ║  ── Any drone, anywhere in UK, within 30 km of an airship       ║
  ║  ── Laser power available to extend any drone's endurance 3-10x ║
  ║  ── Edge compute within 5 seconds of any drone                  ║
  ║  ── High-bandwidth comms relay to any remote area               ║
  ║  ── Emergency pivot: entire regional network redirected within   ║
  ║     5 minutes of COBRA declaration                               ║
  ║  ── Cargo corridor: any two points in UK connected via airship  ║
  ║     power chain — drones no longer range-limited                 ║
  ║                                                                   ║
  ║  Economic target:                                                 ║
  ║  ── Network serves 500,000+ drone-hours/year                    ║
  ║  ── Revenue: £50-100M/year (commercial operations)               ║
  ║  ── Government subsidy: £30-50M/year (backbone + emergency)     ║
  ║  ── Conservation/science subsidy: £5-10M/year                   ║
  ║  ── Commercial operators profitable by year 7-10                 ║
  ║                                                                   ║
  ║  Vision:                                                          ║
  ║  ── The airship network becomes invisible infrastructure —       ║
  ║     like cell towers or the power grid. Drone operators don't   ║
  ║     think about power or comms; they just fly. The network      ║
  ║     handles it, like WiFi handles your internet connection      ║
  ║     without you thinking about cables and routers.               ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 10. INTEGRATION WITH EXISTING PROJECT ARCHITECTURE

### 10.1 How This Connects to Existing Documents

```
  THIS DOCUMENT (34) INTEGRATES:
  ═══════════════════════════════

  Doc 22 (Multi-Scale Platform Family)
  ── Every platform tier (MICRO through LARGE) becomes a network client
  ── Standard PV receiver and URP transceiver added to each tier's spec
  ── The platform family gains effectively unlimited range and endurance
     when operating within network coverage

  Doc 31 (In-Flight Power Transfer)
  ── Laser power beaming is the primary power resource in the network
  ── Specifications from doc 31 (wavelength, efficiency, range) apply
     directly to airship-to-drone power transfer
  ── The network is the deployment model for the power transfer tech

  Doc 32 (Persistent Stratospheric Platforms)
  ── Stratospheric platforms become the high-altitude tier of the network
  ── Their comms relay capability becomes a network backbone resource
  ── Their 300-500 km comms range provides wide-area network management

  Doc 33 (Aerial Command Base)
  ── The mobile forward command airship (Variant 2) is a network node
  ── The home base balloon (Variant 1) is a fixed network node
  ── Both variants gain cross-sector capability via URP

  Doc 23 (Mesh Network and Directional Comms)
  ── Ground mesh network becomes Layer 1 (ground hubs) of this network
  ── Directional antenna tracking transfers to airship FSO terminals
  ── Hill-climbing algorithm applies to airship laser tracking

  Doc 26 (Automated Drone Bases)
  ── Ground bases become network hubs (Layer 1)
  ── Physical maintenance stays at ground bases
  ── Power and comms shift to airship network (reducing ground base
     complexity and increasing drone operational radius)

  Doc 12 (Naval/Maritime Applications)
  ── Maritime drones become network clients
  ── Coastal airships serve as maritime infrastructure
  ── ASW, fisheries, and coast guard drones share the same airships

  Doc 10/21 (Pest Control/Conservation)
  ── Conservation and pest control drones become network clients
  ── Piggyback on agricultural airship infrastructure (Scenario E)
  ── Dramatically lower cost of aerial conservation monitoring
```

### 10.2 What Changes in the Platform Design

For the MINI tier (current build target, doc 22), adding network compatibility requires:

```
  HARDWARE ADDITIONS TO MINI PLATFORM:
  ════════════════════════════════════

  1. Dorsal PV receiver panel (200-400 cm², ~50-100 g)
     ── GaAs cells optimised for 980 nm
     ── Mounted on upper fuselage or wing root
     ── Connected to battery charge controller via MPPT

  2. URP transceiver module (~30 g)
     ── 868 MHz LoRa (URP discovery channel)
     ── 5.8 GHz directional link (data channel)
     ── Integrated into existing comms bay

  3. Corner-cube retroreflector (5 g)
     ── Passive, no power required
     ── Mounted dorsal, visible from above
     ── Enables airship laser acquisition

  4. URP software daemon on ArduPilot companion computer
     ── Runs alongside mission engine (doc 07)
     ── Monitors battery state → triggers resource requests
     ── Handles offer comparison and acceptance
     ── Reports to mission engine: "network power available" or
        "network power unavailable — plan for battery-only"

  TOTAL ADDED MASS: ~85-135 g
  TOTAL ADDED COST: ~£150-300
  TOTAL ADDED POWER DRAW: ~1.5 W (transceiver)

  These additions are trivial relative to the MINI platform's
  5-15 kg MTOW and £1,000-5,000 cost target. The capability
  gain — potentially unlimited endurance within network coverage —
  is transformative.
```

---

## Conclusion

The unified airship infrastructure network transforms every drone from an isolated battery-limited platform into a node in a national resource grid. The key insight is that infrastructure shared across sectors is dramatically cheaper per user than infrastructure built for each sector independently — the same principle that makes roads, cell networks, and the power grid economically viable.

The technology for every component exists today: laser power beaming (doc 31), stratospheric platforms (doc 32), tropospheric airships (doc 33), mesh networking (doc 23), edge compute (commodity NVIDIA hardware), PKI authentication (standard internet technology). What does not yet exist is the integration — the URP protocol, the cross-sector sharing model, the regulatory framework, and the economic structure that ties it all together.

Phase 1 requires two airships, one corridor, and £15-30M to prove the concept. If it works, the path to a national network serving every sector is a scaling challenge, not a research challenge. The physics work. The economics work at scale. The question is whether the UK has the institutional will to build shared infrastructure for a drone economy that does not yet fully exist — the same leap of faith that justified building motorways before most people owned cars, or cell towers before most people owned mobile phones.

The airship network is the missing infrastructure layer between satellites (too far, too expensive, too slow) and ground stations (too short-range, too many needed). It is the drone equivalent of the cellular network — and just as transformative.
