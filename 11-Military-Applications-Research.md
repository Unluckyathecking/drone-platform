# Engineering Requirements for Munition Payloads on Small Fixed-Wing UAV Platforms

## Platform Reference Class: 2–4m Wingspan, 4kg Maximum Payload

### Research Scope and Disclaimer

This document examines the engineering requirements that military munition payloads impose on small UAV airframes and mission planning systems. All data is drawn from publicly available defense publications, manufacturer datasheets, Congressional Research Service reports, and open-source defense journalism. The purpose is understanding platform integration requirements — structural, electrical, computational, and regulatory — not weapons development.

---

## 1. Anti-Personnel Loitering Munition

### Reference System: AeroVironment Switchblade 300

**Published Specifications (from AeroVironment public materials, CRS Report R47838):**

- Total system weight: approximately 2.5 kg (5.5 lbs), including the launch tube
- Munition flyweight (in flight): approximately 1.3–1.5 kg
- Wingspan: approximately 60 cm (foldable)
- Endurance: approximately 15 minutes powered flight
- Range: approximately 10 km from launch point
- Warhead: approximately 40mm grenade equivalent fragmentation charge (estimated 200–300g warhead mass)
- Guidance: GPS-aided inertial navigation with electro-optical terminal seeker (daylight and IR variants)
- Terminal approach: steep dive, operator-in-the-loop or semi-autonomous

**Carrier Aircraft Requirements:**

| Requirement | Specification |
|---|---|
| Payload bay volume | Minimum 65cm x 12cm x 12cm per munition (folded configuration) |
| Release mechanism | Pneumatic or spring-ejection tube, or underwing trapeze release |
| Ejection force | 15–30N sustained over 0.2s to ensure clean separation at flight speed |
| Electrical interface | Power for munition electronics keep-alive prior to release (5V/12V, <5W) |
| Data link | Wideband datalink handoff — carrier must relay target coordinates and terminal seeker initialization data |
| Structural reinforcement | Hard points rated to 2x payload weight for maneuvering loads (so 3 kg per station minimum) |
| CG management | Release of 1.5 kg from a 4 kg payload budget shifts CG significantly — requires either symmetric carriage (2 munitions) or active trim compensation |

**Mission Engine Requirements:**

- **Target designation:** Onboard EO/IR sensor must be able to geolocate targets to <10m CEP for GPS handoff, or provide a continuous track for the munition's seeker to slave to
- **Loiter patterns:** Racetrack or orbit patterns at 300–600m AGL over the target area; the mission engine must calculate fuel/energy reserves for loiter time plus egress
- **Abort capability:** Critical requirement — the Switchblade 300 has a wave-off mode allowing the operator to abort a terminal dive and re-enter loiter. The carrier's mission engine must support this by maintaining the datalink and providing re-engagement planning
- **Release envelope:** The mission engine must enforce minimum/maximum airspeed, altitude, and dive angle constraints for clean separation. Typical release: 60–100 km/h, level flight or shallow dive, >150m AGL
- **Battle damage assessment:** Post-release, the carrier should loiter to provide BDA via its own sensors

**Platform Modifications vs Standard Payload Bay:**

- Standard survey/ISR payload bays are designed for static, rigidly mounted sensors. Munition carriage requires:
  - A release mechanism (mechanical actuator, pyrotechnic bolt, or pneumatic piston)
  - Umbilical connector for pre-release power and data
  - Blast/exhaust clearance if the munition has a booster motor at separation
  - Modified payload bay doors or underwing pylons
- Structural analysis required for asymmetric release loads and flutter analysis with external stores

**Feasibility Assessment: HIGH**

A single Switchblade 300-class munition at 1.3–1.5 kg is well within the 4 kg payload budget. Two munitions (approximately 3 kg) are feasible with symmetric mounting. The primary challenges are integration engineering (release mechanism, datalink handoff) rather than weight.

---

## 2. Anti-Armor Munition

### Reference Systems: Switchblade 600, UVision HERO-120, WB Electronics Warmate

**Published Specifications:**

| Parameter | Switchblade 600 | HERO-120 | Warmate |
|---|---|---|---|
| Total weight | 23 kg (50 lbs) | 12.5 kg | 5.3 kg (with warhead) |
| Warhead weight | ~5 kg (Javelin-derived) | ~3.5 kg | ~1.4 kg |
| Warhead type | Shaped charge (anti-armor) | Multipurpose shaped charge | HEAT or thermobaric |
| Penetration | >300mm RHA (estimated, Javelin-class) | ~200mm RHA (published) | ~80–100mm RHA (estimated) |
| Wingspan | ~1.3 m | ~2.4 m | ~1.6 m |
| Guidance | GPS/INS + EO/IR seeker | GPS/INS + EO seeker | GPS/INS + EO seeker |
| Range | 40+ km | 60+ km | 30 km |

**Critical Weight Analysis:**

The fundamental challenge is the physics of shaped charges. Armor penetration is roughly proportional to charge diameter and liner geometry. Published data from open ordnance engineering references (e.g., Paul Cooper's "Explosives Engineering") establishes:

- A shaped charge penetrates approximately 1.5–6x its diameter in rolled homogeneous armor (RHA), depending on liner material, standoff, and precision
- To penetrate 200mm RHA (enough for APCs, light armor, top-attack on MBTs), you need roughly a 60–80mm diameter charge
- A 60mm shaped charge warhead with casing weighs approximately 1.5–2.5 kg
- A minimal HEAT warhead capable of defeating light armored vehicles (80–100mm penetration): approximately 1.0–1.5 kg

**Does Anti-Armor Exceed 4 kg?**

- **Full anti-armor (Switchblade 600 class):** Yes, dramatically. At 23 kg system weight and 5 kg warhead, this is completely impossible for the reference platform class.
- **Medium anti-armor (HERO-120 class):** Yes. 12.5 kg system weight is 3x the payload budget.
- **Light anti-armor (Warmate class):** Marginal. The Warmate's 5.3 kg total weight exceeds 4 kg, but its warhead alone (1.4 kg) fits. However, the Warmate IS its own airframe — to carry a Warmate-equivalent warhead as a deployable payload, you need the warhead (1.4 kg) plus guidance section (0.5–1 kg) plus release mechanism (0.3–0.5 kg), totaling 2.2–2.9 kg. This is within budget but leaves little margin.

**Terminal Guidance Requirements:**

All effective anti-armor munitions require precise terminal guidance because shaped charges must impact within narrow cone angles (typically <15 degrees from perpendicular) to achieve rated penetration:

- **EO seeker:** Requires stabilized camera, image processor, and tracking algorithm. Minimum additional mass approximately 300–500g. Power draw approximately 10–20W.
- **IR seeker (uncooled):** Similar mass, works at night, but lower resolution. Approximately 400–600g.
- **Semi-active laser (SAL):** Requires external designator but simplifies the munition. Seeker head approximately 200–400g.
- **GPS-only:** Adequate for stationary targets only (CEP 3–10m). Not sufficient for moving armor.

**Honest Assessment for Mini-UAV Class:**

- **Against main battle tanks:** NOT FEASIBLE. Top-attack on an MBT requires penetration of 300+ mm RHA through ERA. The required warhead exceeds the entire payload budget.
- **Against APCs/IFVs (top attack):** MARGINALLY FEASIBLE. A 60mm shaped charge (approximately 1.5 kg warhead) could achieve 100–150mm penetration in top-attack mode, sufficient against BTR/BMP class vehicles. Total deployed munition weight approximately 2.5–3.5 kg.
- **Against soft-skinned vehicles and technicals:** FEASIBLE. An EFP (explosively formed penetrator) warhead of 0.8–1.2 kg can penetrate 20–40mm of steel, sufficient for unarmored vehicles.
- **Against stationary armor (with top-attack):** FEASIBLE with GPS guidance if the target is pre-located.

**Platform Requirements for Anti-Armor Payload:**

- Significantly reinforced hardpoints (the warhead is dense — high point-loading)
- Steep terminal dive capability if the carrier IS the munition (loitering munition mode) — requires structural integrity at high dive speeds (>200 km/h)
- If deploying a separate munition: the munition needs its own guidance and flight surfaces, consuming weight budget
- Mission engine must compute terminal attack geometry, particularly top-attack dive angles (typically 45–70 degrees from horizontal)
- Safety-critical arming logic: the warhead must have environmental sensing (acceleration, spin, altitude gates) to prevent premature detonation

---

## 3. Counter-UAS / Anti-Drone

### Reference Concepts: Anduril Roadrunner, Fortem DroneHunter, various interceptor programs

**Published System References:**

| System | Approach | Weight | Platform Class |
|---|---|---|---|
| Anduril Roadrunner | Kinetic (reusable VTOL interceptor) | ~25 kg | Dedicated platform, NOT a payload |
| Fortem DroneHunter | Net capture | ~7 kg (drone) | Dedicated multirotor |
| MARSS Interceptor | Kinetic/net | ~5 kg | Dedicated platform |
| Drone-mounted jammers | RF jamming payload | 1–3 kg | Payload on carrier |

**Detection Methods at Mini-UAV Scale:**

- **Radar:** NOT FEASIBLE as a payload. Even compact AESA arrays (e.g., Echodyne metamaterial radar) weigh 1–2 kg and draw 30–60W, but they detect targets at limited range (1–3 km for small drones). The entire payload and power budget would be consumed.
- **RF detection:** FEASIBLE. An SDR-based RF detector (listening for control links and video downlinks) weighs 200–500g and draws 5–10W. Range 1–5 km depending on target emissions. Cannot detect autonomous drones operating without RF emissions.
- **Visual (EO/IR):** FEASIBLE. A camera with onboard AI processing for drone detection. Weight 300–800g. Range limited to 500m–2km depending on target size and optics. Requires significant onboard compute (e.g., NVIDIA Jetson class, 10–20W).
- **Acoustic:** MARGINAL. Microphone arrays can detect drone motor noise but have extremely limited range in flight due to wind noise on the carrier platform. Not practical for air-to-air.

**Interception Approaches — Feasibility at Mini-UAV Scale:**

**Kinetic (direct collision):**
- The carrier aircraft IS the interceptor. No payload required beyond guidance.
- Requires: high-speed terminal maneuverability (the target drone may be small and agile), robust terminal seeker, and sufficient structural mass to cause damage on impact.
- Mission engine must solve a 3D intercept geometry problem in real time, with the target potentially maneuvering.
- FEASIBLE in concept, but the carrier is expended. Essentially a purpose-built loitering munition targeting drones instead of ground targets.

**Net capture:**
- A deployable net (0.5–1.5 kg) with a deployment mechanism (pyrotechnic or spring-loaded).
- Range: must be deployed within 5–20m of the target, requiring precise close approach.
- Challenge: a fixed-wing aircraft approaching a hovering multirotor has an enormous speed differential. The intercept window is milliseconds.
- MARGINAL for fixed-wing. Better suited to multirotor interceptors that can match the target's flight regime.

**RF Jamming:**
- A broadband jammer payload (1–2 kg, 20–50W RF output, requiring 50–100W electrical input) that overwhelms the target's control link.
- Effective range: 100–500m with a directional antenna.
- Challenge: power budget. 50–100W is substantial for a mini-UAV — may require a dedicated generator or large battery.
- Legality: RF jamming is heavily regulated even for military use (fratricide risk to friendly communications).
- MARGINAL. Power is the limiting factor.

**Directed Energy (laser, HPM):**
- NOT FEASIBLE. Even the smallest counter-drone lasers (e.g., Raytheon HELWS) are vehicle-mounted systems weighing hundreds of kilograms. Miniaturization to mini-UAV scale does not exist in any publicly documented program.

**Mission Engine Requirements for Counter-UAS:**

This is the most computationally demanding mission type:

- **Autonomous target tracking:** Must maintain track on a small, fast, potentially maneuvering target in 3D space using onboard sensors only (datalink latency is too high for human-in-the-loop intercept)
- **Intercept planning:** Real-time proportional navigation or augmented proportional navigation guidance law. Update rate >10 Hz. This is fundamentally the same problem as missile guidance.
- **Classification:** Must distinguish hostile drones from birds, debris, friendly aircraft. Requires trained ML models.
- **Cooperative intercept:** If multiple interceptors are available, the mission engine should assign targets and deconflict flight paths.
- **Compute requirements:** A modern embedded GPU (Jetson Orin class: 275 TOPS, 15–60W) is the minimum for real-time visual tracking and intercept computation. Weight approximately 200–500g plus cooling.

**Honest Feasibility Assessment:**

Counter-UAS from a mini fixed-wing platform is feasible ONLY in the kinetic kamikaze interceptor role, where the carrier IS the weapon. Carrying a separate C-UAS payload (jammer, net, etc.) is marginal to infeasible given the weight and power constraints. The most realistic concept of operations is a loitering interceptor that uses onboard EO/IR and AI to detect, classify, track, and intercept hostile drones autonomously.

---

## 4. Swarm / Microdrone Deployment

### Reference Programs: PERDIX (US DoD/SCO), LANCA (UK), Coyote Block 1 (Raytheon)

**Published Program Details:**

**PERDIX (Strategic Capabilities Office / MIT Lincoln Labs):**
- Published in DoD press releases and SCO demonstrations (2017 Naval Air Weapons Station China Lake test)
- Individual drone weight: approximately 290g (publicly reported)
- Wingspan: approximately 30 cm
- Endurance: approximately 20 minutes
- Deployed from flare dispensers on fighter aircraft (F/A-18) — 103 units in the public demonstration
- No warhead — ISR and electronic warfare roles
- Communication: mesh network, distributed consensus algorithms (no central controller)
- Each unit runs identical software; swarm behavior is emergent from shared decision rules

**LANCA (Lightweight Affordable Novel Combat Aircraft, UK DSTL/Spirit AeroSystems):**
- Larger class: 3m+ wingspan, jet-powered
- NOT a microdrone — this is a loyal wingman program
- Not directly relevant to sub-munition deployment from a mini-UAV

**Coyote Block 1 (Raytheon / US Navy):**
- Weight: approximately 5.9 kg per unit
- Launched from sonobuoy tubes (SONOBUOY-A size launchers)
- Tube-launched, folding wing
- Too heavy for carriage on a mini-UAV (one unit exceeds the entire payload budget)

**Carrier Aircraft Requirements for Microdrone Deployment:**

Given the 4 kg payload limit, only PERDIX-class microdrones are relevant:

| Parameter | Calculation |
|---|---|
| Individual microdrone mass | ~300g |
| Dispensing mechanism per drone | ~50g (tube, spring, retainer) |
| Total per unit (deployed) | ~350g |
| Maximum units at 4 kg | 11 units (with margin for dispenser structure) |
| Realistic count (with shared dispenser housing, wiring, controller) | 6–8 units |

**Dispenser Design Requirements:**

- **Sequential ejection:** Drones must be released one at a time or in controlled salvos to avoid collision. The dispenser needs individual retention and release mechanisms (solenoid latches or pyrotechnic bolts).
- **Separation dynamics:** At carrier speeds of 60–100 km/h, the released microdrone enters the airstream in a folded configuration and must deploy wings and stabilize within 2–3 seconds. This requires careful aerodynamic design of the microdrone and release sequencing.
- **Power and data:** Each microdrone needs its battery topped off and its mission data loaded via umbilical before release. The dispenser needs a shared power bus and data bus.
- **CG shift:** Releasing 6–8 drones sequentially from a total of ~2.5 kg shifts the carrier's CG progressively. The mission engine must compensate with trim adjustments. Symmetric release (alternating left/right) is preferred if the dispenser geometry allows it.

**Communication Architecture for Swarm Coordination:**

This is the most technically challenging aspect. Publicly documented approaches include:

- **Mesh networking:** Each drone communicates with neighbors within RF range (typically 500m–2km for low-power 900 MHz or 2.4 GHz links). Information propagates through the mesh. Latency increases with swarm size.
- **Protocols:** The PERDIX program reportedly uses a custom protocol derived from academic swarm research. Open-source analogs include MAVLink-based mesh (used in ArduPilot swarm research) and DDS (Data Distribution Service) for real-time pub/sub.
- **Bandwidth requirements:** Each drone needs to share position, sensor data, and intent. Minimum approximately 1–10 kbps per node for position/intent; 100+ kbps if sharing imagery.
- **Resilience:** The swarm must tolerate loss of individual nodes without mission failure. This requires distributed consensus (no single point of failure) — algorithms like Raft or PBFT adapted for mobile ad-hoc networks.

**Autonomous Target Assignment Algorithms:**

Publicly documented approaches from academic and defense research:

- **Auction-based assignment:** Each drone "bids" on targets based on proximity, sensor capability, and fuel state. The highest bidder is assigned. This is computationally light and decentralized. (Reference: CBBA — Consensus-Based Bundle Algorithm, MIT)
- **Potential field methods:** Targets are attractors, threats are repellers, other swarm members are weak repellers (for spacing). Each drone follows the gradient. Simple but can get trapped in local minima.
- **Task decomposition:** A surveillance mission is decomposed into cells; drones claim cells using distributed negotiation. This is the approach most consistent with PERDIX-type operations.
- **Compute requirements per drone:** These algorithms are lightweight — a microcontroller-class processor (ARM Cortex-M4/M7, <1W) is sufficient for swarm coordination. The carrier's mission engine needs more power to plan the deployment and initialize the swarm mission.

**Mission Engine Requirements on the Carrier:**

- **Swarm initialization:** Load mission parameters (area of interest, target descriptions, communication keys, ROE) into each microdrone before release
- **Deployment planning:** Calculate optimal release points (altitude, spacing, formation) based on wind, target area geometry, and desired coverage
- **Relay capability:** After deployment, the carrier may serve as a communication relay between the swarm and the ground station, requiring a dual-radio setup (one for GCS link, one for swarm mesh)
- **Recovery planning (if applicable):** Some microdrone concepts include recovery. The carrier's mission engine would need to plan collection orbits.

**Feasibility Assessment: MODERATE**

Deploying 6–8 PERDIX-class microdrones (ISR/EW role) from a mini-UAV is physically feasible within the 4 kg budget. The engineering challenges are primarily in the dispenser mechanism, clean separation aerodynamics, and communication architecture. The microdrones themselves are too small to carry meaningful munitions — at 300g, they are limited to ISR sensors, RF payloads (jammers/spoofers weighing 50–100g), or serving as decoys.

Deploying munition-carrying sub-drones is NOT feasible — even a minimal munition (small fragmentation charge plus guidance) would weigh 500g+, limiting the swarm to approximately 6 units and raising severe safety and arming concerns.

---

## Cross-Cutting Requirements Summary

### Structural and Mechanical

| Requirement | Anti-Personnel | Anti-Armor | Counter-UAS | Swarm Deploy |
|---|---|---|---|---|
| Payload mass | 1.5–3 kg | 2.5–4 kg | 0–4 kg (kinetic: 0) | 2.5–3.5 kg |
| Hardpoint rating | 3 kg per station | 8 kg per station | N/A | Distributed load |
| Release mechanism | Ejection tube/trapeze | Trapeze/pylon | N/A | Sequential dispenser |
| CG shift management | Moderate | Severe | N/A | Progressive (worst case) |
| Structural modification | Moderate | Significant | Minimal | Significant |

### Electrical and Computational

| Requirement | Anti-Personnel | Anti-Armor | Counter-UAS | Swarm Deploy |
|---|---|---|---|---|
| Pre-release power | 5–10W | 5–10W | N/A | 10–20W (charging) |
| Datalink bandwidth | 1–5 Mbps (video handoff) | 1–5 Mbps | N/A (autonomous) | 100 kbps (init) |
| Onboard compute | Standard FCS + GCS relay | Standard + terminal guidance | GPU-class (Jetson Orin) | Standard + swarm planner |
| Sensor requirements | EO/IR gimbal | EO/IR gimbal + laser designator | EO/IR + AI classification | EO/IR for BDA |

### Mission Engine Software Requirements

All munition-capable missions require these capabilities beyond standard ISR:

1. **Weapons release envelope computation** — airspeed, altitude, attitude, and g-loading constraints
2. **Target geolocation** — converting pixel coordinates to WGS84 with error estimates
3. **Munition datalink management** — separate from the GCS link
4. **Abort/wave-off logic** — the ability to cancel an engagement at any point before terminal
5. **Battle damage assessment** — post-strike ISR pass planning
6. **Safety interlocks** — software-enforced arming gates (minimum altitude, minimum distance from friendlies, operator confirmation)
7. **Collateral damage estimation** — weapon effects modeling to predict blast/fragmentation radius

### Regulatory and Legal Framework

**All categories require military authorization. There is no civilian pathway for any of these capabilities.**

| Framework | Applicability |
|---|---|
| ITAR (US International Traffic in Arms Regulations) | All munition-related components, guidance systems, and integration documentation are ITAR-controlled under USML Categories IV (Launch Vehicles, Guided Missiles, Ballistic Missiles, Rockets, Torpedoes, Bombs, and Mines) and XI (Military Electronics) |
| EAR (Export Administration Regulations) | Dual-use components (cameras, IMUs, compute modules) may fall under EAR Category 7 (Navigation and Avionics) |
| MTCR (Missile Technology Control Regime) | Systems capable of delivering >500g payload to >300km range are Category I restricted. Mini-UAVs typically fall below this threshold but may be captured under Category II |
| CCW Protocol (Convention on Certain Conventional Weapons) | Ongoing international discussions on Lethal Autonomous Weapons Systems (LAWS). No binding treaty yet, but "meaningful human control" is an emerging norm |
| DoD Directive 3000.09 | US policy on autonomy in weapon systems. Requires senior-level review for systems that select and engage targets without human authorization |
| NATO STANAG 4586 | Interoperability standard for UAV control. Munition-capable UAVs integrated into NATO C2 must comply |
| National aviation authority (FAA in US, CAA in UK) | Airworthiness certification for weapons-carrying UAVs is a military-only process, typically handled through MIL-HDBK-516C (Airworthiness Certification Criteria) |

**Key Legal Distinction:** The platform itself (airframe, autopilot, mission engine) may be developed as dual-use. The moment a weapons release mechanism, arming circuit, or terminal guidance algorithm is integrated, the entire system becomes a munition under ITAR and equivalent frameworks. This applies to software as well — a mission engine with weapons release logic is export-controlled even without hardware.

---

## Summary Feasibility Matrix

| Mission Type | Weight Feasibility | Technical Feasibility | Realistic for Mini-UAV? |
|---|---|---|---|
| Anti-personnel loitering munition | HIGH (1.5 kg, well within budget) | HIGH (proven concept) | YES — most natural fit |
| Anti-armor (light vehicles, top-attack) | MARGINAL (2.5–3.5 kg, tight) | MODERATE (guidance is challenging) | CONDITIONAL — light armor only |
| Anti-armor (MBT-class) | NOT FEASIBLE (warhead alone >4 kg) | NOT FEASIBLE | NO |
| Counter-UAS (kinetic interceptor) | HIGH (carrier IS weapon) | MODERATE (intercept guidance is hard) | YES — as dedicated interceptor |
| Counter-UAS (payload-based) | MARGINAL to LOW | LOW (power constraints) | MARGINAL at best |
| Swarm ISR/EW deployment | MODERATE (6–8 units) | MODERATE (dispenser + comms) | YES — ISR/EW roles only |
| Swarm munition deployment | LOW (limited count, tiny warheads) | LOW (arming safety concerns) | NOT PRACTICAL |

---

## Key References (Open Source)

1. AeroVironment Switchblade product literature (avinc.com)
2. UVision HERO series product brochures (uvisionuav.com)
3. Congressional Research Service, "Loitering Munitions" (R47838, updated 2024)
4. DoD Strategic Capabilities Office, PERDIX demonstration press release (January 2017)
5. Cooper, Paul W., "Explosives Engineering," Wiley-VCH (shaped charge physics)
6. DoD Directive 3000.09, "Autonomy in Weapon Systems" (updated 2023)
7. MTCR Equipment, Software and Technology Annex
8. Echodyne EchoGuard radar specifications (echodyne.com)
9. NVIDIA Jetson Orin module specifications (nvidia.com)
10. MIT CBBA algorithm publications (Jonathan How et al., MIT ACL)
11. MIL-HDBK-516C, Airworthiness Certification Criteria
12. STANAG 4586, Standard Interfaces of UAV Control System for NATO UAV Interoperability
