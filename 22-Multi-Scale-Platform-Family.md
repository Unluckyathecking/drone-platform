# Multi-Scale Platform Family Concept

## Vision

A family of fixed-wing UAVs sharing the same design philosophy across multiple size classes. Common traits: high-aspect-ratio glider wings, pusher prop configuration, electric propulsion, composite construction, ArduPilot autopilot, and the standardised payload interface (scaled per size class). One mission engine, one training pipeline, one maintenance doctrine — multiple scales.

## Platform Family

### Tier 1: MICRO (~500g, 50-80cm wingspan)

```
  ┌─────────────────────────────────────────┐
  │  MICRO — Disposable / Swarm Member      │
  │                                         │
  │  Wingspan:     50-80 cm                 │
  │  MTOW:         300-800 g               │
  │  Payload:      50-200 g                │
  │  Endurance:    15-25 min               │
  │  Cruise speed: 10-15 m/s              │
  │  Range:        5-15 km                 │
  │  Cost target:  £50-200/unit            │
  │                                         │
  │  Roles:                                 │
  │  ├── Swarm ISR (deployed from MINI+)   │
  │  ├── Expendable sensor node            │
  │  ├── Electronic decoy                  │
  │  ├── Communications relay (short range)│
  │  └── Anti-personnel (loitering munition│
  │      class — Switchblade 300 equiv)    │
  │                                         │
  │  Launch: tube-deployed from carrier    │
  │  Recovery: belly landing or disposable │
  └─────────────────────────────────────────┘
```

### Tier 2: MINI (~5-15kg, 2-4m wingspan) — CURRENT BUILD

```
  ┌─────────────────────────────────────────┐
  │  MINI — Core Multirole Platform         │
  │  ★ THIS IS THE CURRENT PROJECT ★        │
  │                                         │
  │  Wingspan:     2-4 m                    │
  │  MTOW:         5-15 kg                 │
  │  Payload:      1-4 kg                  │
  │  Endurance:    45-90 min               │
  │  Cruise speed: 15-25 m/s              │
  │  Range:        30-80 km                │
  │  Cost target:  £1,000-5,000            │
  │                                         │
  │  Roles:                                 │
  │  ├── ISR / survey / mapping            │
  │  ├── Cargo delivery (1-3 kg)           │
  │  ├── Search and rescue                 │
  │  ├── Comms relay (tactical)            │
  │  ├── Micro-drone carrier (4-8 units)   │
  │  ├── Pest control / conservation       │
  │  └── Light counter-UAS (kamikaze)      │
  │                                         │
  │  Launch: hand-launch or bungee         │
  │  Recovery: belly landing or parachute  │
  │                                         │
  │  Note: MINI tier uses off-the-shelf    │
  │  Skywalker X8 for prototyping only.    │
  │  Production aircraft will be a custom  │
  │  composite airframe optimised for the  │
  │  mission profile.                      │
  └─────────────────────────────────────────┘
```

### Tier 3: MEDIUM (~25-50kg, 4-6m wingspan)

```
  ┌─────────────────────────────────────────┐
  │  MEDIUM — Extended Capability           │
  │                                         │
  │  Wingspan:     4-6 m                    │
  │  MTOW:         25-50 kg                │
  │  Payload:      5-15 kg                 │
  │  Endurance:    2-6 hrs (electric)      │
  │               8-12 hrs (hybrid)        │
  │  Cruise speed: 20-35 m/s              │
  │  Range:        100-300 km              │
  │  Cost target:  £10,000-50,000          │
  │                                         │
  │  Roles:                                 │
  │  ├── Loitering munition carrier        │
  │  │   (can carry Switchblade 600 class) │
  │  ├── Sonar buoy deployment (ASW)       │
  │  ├── Counter-mine surveillance         │
  │  ├── Maritime patrol                   │
  │  ├── Heavy cargo delivery (5-10 kg)    │
  │  ├── Long-range comms relay            │
  │  ├── MINI drone carrier (2-4 units)    │
  │  └── LiDAR survey (heavy sensors)      │
  │                                         │
  │  Launch: catapult or short runway      │
  │  Recovery: belly landing, net, or      │
  │           parachute                    │
  │                                         │
  │  Propulsion options:                    │
  │  ├── Pure electric (large LiPo/Li-ion) │
  │  ├── Hybrid (generator + electric)     │
  │  └── Hydrogen fuel cell (emerging)     │
  └─────────────────────────────────────────┘
```

### Tier 4: LARGE (~150-200kg, 10-12m wingspan)

```
  ┌─────────────────────────────────────────┐
  │  LARGE — Persistent / Strategic         │
  │                                         │
  │  Wingspan:     10-12 m                  │
  │  MTOW:         150-200 kg              │
  │  Payload:      20-50 kg                │
  │  Endurance:    12-48 hrs               │
  │               (solar-assist / fuel)    │
  │  Cruise speed: 25-40 m/s              │
  │  Range:        500-2000 km             │
  │  Cost target:  £50,000-200,000         │
  │                                         │
  │  Design philosophy:                     │
  │  Custom airframe designed for endurance │
  │  as the primary requirement. High-AR   │
  │  wing (AR 20-30), L/D 26-32, large    │
  │  solar area on upper wing surface.     │
  │                                         │
  │  Roles:                                 │
  │  ├── High-altitude comms relay         │
  │  │   (persistent, constellation mode)  │
  │  ├── Maritime patrol (extended range)  │
  │  ├── ASW sonar field deployment        │
  │  ├── Heavy cargo delivery (20+ kg)     │
  │  ├── SIGINT / ELINT collection         │
  │  ├── MEDIUM/MINI carrier (mothership)  │
  │  └── Pseudo-satellite (stratospheric)  │
  │                                         │
  │  Launch: runway or catapult            │
  │  Recovery: runway, arresting wire, or  │
  │           autonomous landing           │
  │                                         │
  │  Propulsion:                            │
  │  ├── Hybrid electric-combustion        │
  │  ├── Solar + battery (for HALE ops)    │
  │  └── Hydrogen fuel cell                │
  └─────────────────────────────────────────┘
```

## Design Commonality Across Tiers

### What Scales (same across all tiers)

| Feature | How It Scales |
|---------|--------------|
| Wing planform | Same high-AR glider profile, scaled geometrically |
| Pusher prop | Same configuration, different motor/prop sizes |
| Payload interface | Same dovetail concept, scaled rail dimensions per tier |
| Mission engine | Identical software — same goal→waypoint pipeline |
| ArduPilot | Same firmware, different parameter files |
| Composite construction | Same materials (carbon/glass/foam), scaled layup |
| Autonomy level | Identical — fully autonomous waypoint execution |

### What Doesn't Scale (tier-specific)

| Feature | Tier-Specific Reason |
|---------|---------------------|
| Propulsion type | MICRO/MINI: pure electric. MEDIUM: hybrid option. LARGE: fuel/solar |
| Launch/recovery | MICRO: tube. MINI: hand-launch. MEDIUM+: catapult/runway |
| Regulatory category | MINI: Open A3. MEDIUM: Specific. LARGE: Certified |
| Communication range | MICRO: mesh (500m). MINI: telemetry (20km). LARGE: SATCOM |
| Structural certification | MINI: none needed. LARGE: requires design org approval |

## Comms Relay Constellation Concept

### The Problem

Long-range communication over hostile or remote terrain is hard:
- Satellite links are expensive, high-latency, and bandwidth-limited
- Ground-based repeaters are vulnerable, require infrastructure, and can be destroyed
- Manned aircraft are expensive and detectable

### The Solution: Atmospheric Comms Chain

```
  ┌─── 2000-5000m altitude ─────────────────────────────────────┐
  │                                                              │
  │   ○─────────○─────────○─────────○─────────○                 │
  │   relay1    relay2    relay3    relay4    relay5             │
  │   (glide)   (glide)  (glide)   (glide)  (glide)            │
  │                                                              │
  │   Spacing: 50-100 km per link                                │
  │   Total chain: 250-500 km                                    │
  │   Bandwidth: 1-10 Mbps per link (directional antennas)       │
  │   Latency: <50ms end-to-end                                  │
  └──────────────────────────────────────────────────────────────┘
        │                                              │
        ▼                                              ▼
   [GROUND UNIT A]                              [GROUND UNIT B]
   Forward operating base                       Headquarters
   or naval vessel                              250-500 km away
```

### Why This Is Hard to Defeat

```
  DETECTION CHALLENGES FOR AN ADVERSARY:
  ═══════════════════════════════════════

  RADAR:
  ├── RCS of a 3-6m composite glider: ~0.01-0.1 m² (bird-sized)
  ├── Slow speed (20-30 m/s) — below most radar velocity filters
  ├── At 3000m+, ground clutter rejection makes detection harder
  └── No metal structure = minimal radar return

  THERMAL / IR:
  ├── Electric motor: negligible heat signature
  ├── Gliding 90% of time: motor off, zero thermal emission
  ├── At altitude: atmospheric absorption masks any signature
  └── Composite skin: low thermal conductivity, blends with sky temp

  ACOUSTIC:
  ├── At 3000m altitude: inaudible from ground
  ├── Slow-turning large prop: low frequency, low amplitude
  └── Ambient wind noise at altitude masks any sound

  VISUAL:
  ├── 3-6m wingspan at 3000m: ~0.1° visual angle
  ├── Unpainted composite blends with sky
  └── No contrails (electric, no combustion)

  ENGAGEMENT CHALLENGES:
  ├── MANPADS (Stinger, Igla): max effective altitude ~3.5km
  │   Range from ground to target: marginal at 3000m+
  │   IR signature too small for seeker lock at range
  ├── AAA (anti-aircraft artillery): can reach altitude but
  │   target is very small and slow (hard to lead)
  ├── Fighter intercept: massive overkill, and the slow
  │   speed makes intercept geometry awkward
  └── Electronic warfare: can jam comms but relay reconfigures
      around lost nodes automatically
```

### Operational Concept

1. **Deployment:** LARGE-tier UAVs (or MEDIUM with solar) launch from a rear area and climb to 3000-5000m. They position themselves in a chain at 50-100km spacing.

2. **Station-keeping:** At altitude, the high-AR wings allow very low power consumption. A 6m wingspan glider at 3000m in calm air needs only 50-100W to maintain altitude. With a 500Wh battery, that's 5-10 hours of powered flight — extended massively by thermal soaring and solar panels.

3. **Communication:** Each relay carries directional antennas (patch or Yagi) pointed at adjacent nodes. Link budget at 50km line-of-sight with 1W transmit power and 12dBi directional antenna: achievable at 1-10 Mbps depending on frequency band.

4. **Resilience:** If a node is lost (shot down, malfunction, battery depletion), adjacent nodes adjust spacing or a replacement is launched. The mission engine handles this automatically — it's a variant of the patrol/loiter mission type with relay-chain topology.

5. **Endurance extension:** Solar panels on the upper wing surface can provide 30-50W for a 6m span aircraft. In summer at mid-latitudes, this nearly matches the power requirement for station-keeping, enabling multi-day operations.

### Link Budget Analysis

```
  RELAY LINK BUDGET (per hop)
  ═══════════════════════════

  Frequency:          2.4 GHz (ISM band for development)
                      or 900 MHz (better propagation)
  Transmit power:     1 W (+30 dBm)
  TX antenna gain:    +12 dBi (patch array, pointed at next node)
  Free-space loss:    -130 dB (at 50 km, 2.4 GHz)
  RX antenna gain:    +12 dBi
  ──────────────────────────────────────
  Received power:     -76 dBm

  Noise floor (BW=5MHz): -101 dBm
  SNR:                    25 dB → supports ~10 Mbps

  For 900 MHz at 100 km:
  Free-space loss:    -132 dB
  Received power:     -60 dBm
  SNR:                41 dB → supports ~50 Mbps (theoretical)
```

### Relevance to Strait of Hormuz / Persian Gulf

```
  COUNTER-MINE / ASW APPLICATION
  ══════════════════════════════

  ┌─── Strait of Hormuz (~55km wide) ──────────────────┐
  │                                                      │
  │  MEDIUM-tier UAVs deploy sonar buoys in barrier      │
  │  pattern across shipping lanes:                      │
  │                                                      │
  │     ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  (sonar buoy line)        │
  │                                                      │
  │  MINI-tier UAVs provide overhead ISR:                │
  │  - Detect mine-laying vessels (thermal + EO)         │
  │  - Track surface contacts (AIS correlation)          │
  │  - Relay sonar data to shore station                 │
  │                                                      │
  │  LARGE-tier UAV at altitude provides comms relay:    │
  │  - Links buoy field to shore HQ                      │
  │  - Persistent (12-24 hr station time)                │
  │  - Difficult to detect / engage                      │
  │                                                      │
  │  MICRO swarm available for close inspection:         │
  │  - Deployed from MINI/MEDIUM to investigate contacts │
  │  - Expendable if investigating suspect mines         │
  └──────────────────────────────────────────────────────┘
```

## Engineering Communication Systems — Design Considerations

### Antenna Design Per Tier

| Tier | Primary Link | Antenna Type | Weight | Gain |
|------|-------------|-------------|--------|------|
| MICRO | Mesh (ESP32) | PCB trace antenna | <1g | 2 dBi |
| MINI | Telemetry (SiK/RFD900x) | Dipole or sleeve | 10-20g | 2-5 dBi |
| MEDIUM | Data link (Doodle Labs) | Patch antenna | 30-80g | 8-12 dBi |
| LARGE | Relay (custom) | Directional array | 200-500g | 12-18 dBi |

### Frequency Selection

| Band | Range | Bandwidth | Pros | Cons |
|------|-------|-----------|------|------|
| 433 MHz | 20+ km | Low (kbps) | Excellent propagation, penetrates foliage | Narrow band, low data rate |
| 868/915 MHz | 15+ km | Low-medium | Good propagation, LoRa available | ISM band congestion |
| 2.4 GHz | 5-50 km | High (Mbps) | WiFi ecosystem, cheap hardware | Shorter range, rain attenuation |
| 5.8 GHz | 2-20 km | Very high | Video-capable bandwidth | Rain fade, line-of-sight only |

### Protocol Stack for Relay Network

```
  APPLICATION LAYER
  ├── MAVLink v2 (telemetry, commands)
  ├── RTP/RTSP (video streaming)
  └── Custom (sonar data, sensor fusion)

  TRANSPORT LAYER
  ├── UDP (low-latency telemetry and video)
  └── TCP (reliable command delivery)

  NETWORK LAYER
  ├── Mesh routing (BATMAN-adv or custom)
  ├── Dynamic topology management
  └── Node discovery and failover

  LINK LAYER
  ├── 802.11 (WiFi — high bandwidth, short range)
  ├── LoRa (long range, low bandwidth backup)
  └── Custom TDMA (relay chain optimised)

  PHYSICAL LAYER
  ├── 900 MHz band (primary relay link)
  ├── 2.4 GHz band (local mesh / high bandwidth)
  └── Directional antennas with tracking
```

### Connection to Electrical Engineering

This project directly exercises:

| EE Topic | Where It Appears |
|----------|-----------------|
| RF circuit design | Antenna matching, LNA, PA, filter design |
| Signal processing (DSP) | Sonar processing, DEMON analysis, spectral analysis |
| Information theory | Shannon capacity, link budget, coding gain, modulation |
| Antenna theory | Patch arrays, phased arrays, beam steering |
| Power electronics | BEC design, solar MPPT, battery management |
| Embedded systems | STM32/ESP32 firmware, real-time control loops |
| Control theory | PID loops (autopilot), Kalman filtering (navigation) |
| Electromagnetic compatibility | EMI from motors affecting radios, shielding |
| PCB design | Custom flight controllers, payload interface boards |
| Sensor physics | Thermal detectors (bolometers), acoustic transducers |

These map directly to modules in EE / Electronic Engineering degrees at:
- Imperial (EEE), Southampton (ECS), Bristol (EE), Bath (Electronic Engineering), UCL (EEE), Edinburgh, Manchester, Surrey
- And dual-track programmes: Cambridge Engineering, Oxford Engineering Science

## Development Sequence

The multi-scale family develops bottom-up:

```
  PHASE 1 (Current - Summer 2026):  Build MINI tier (Skywalker X8)
  PHASE 2 (2026-2027):              Design MICRO tier (swarm member)
  PHASE 3 (2027-2028):              Design MEDIUM tier (extended capability)
  PHASE 4 (2028+):                  Design LARGE tier (persistent comms relay)

  Each tier reuses:
  ├── Mission engine (same software, scaled parameters)
  ├── Payload interface concept (scaled dovetail dimensions)
  ├── ArduPilot configuration methodology
  ├── Ground station and operations procedures
  └── Manufacturing approach (composite layup, 3D printed components)
```

The MINI tier being built now is the proof of concept for the entire family. Every lesson learned — software architecture, payload integration, flight testing methodology — transfers directly to subsequent tiers.
