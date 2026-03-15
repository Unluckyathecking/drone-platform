# Swarm Drone Deployment from Carrier Mini-UAV: Engineering Research

## 1. Existing Swarm Programs (Public Domain)

### PERDIX (MIT Lincoln Laboratory / US DoD SCO)

PERDIX is the most publicly documented micro-drone swarm system. Originated from a MIT Lincoln Laboratory student project, it was transitioned to the Strategic Capabilities Office (SCO) for military development.

**Specifications (from public DoD releases and 2017 demonstration):**
- Wingspan: 290mm (11.4 inches)
- Weight: approximately 290g (0.64 lb)
- Airframe: 3D-printed body, folding wings that deploy post-launch
- Launch method: dispensed from standard aircraft flare/chaff dispensers (e.g., AN/ALE-47 on F/A-18 Super Hornets)
- Propulsion: single electric motor, pusher configuration
- Endurance: approximately 20 minutes (limited by small LiPo battery)
- Speed: 60-70 knots cruise
- Autonomy level: Level 3-4. PERDIX drones do not operate with pre-programmed routes. They share a distributed brain, meaning each drone communicates with every other to make collective decisions. There is no single leader -- if one is lost, the swarm adapts. Demonstrated behaviors include synchronized formation flying, adaptive collective decision-making, and self-healing formations.
- Communication: proprietary mesh network, likely operating in ISM bands
- Key demonstration: January 2017, 103 PERDIX drones launched from three F/A-18s over China Lake, California. They demonstrated collective decision-making, adaptive formation flying, and self-healing.

**Engineering significance:** PERDIX proved that extremely small, inexpensive drones launched from existing aircraft infrastructure can perform cooperative autonomous behaviors. The flare-dispenser launch is a critical design point -- it means no aircraft modification is required.

### LANCA / Mosquito (UK Ministry of Defence / DSTL)

The Lightweight Affordable Novel Combat Aircraft (LANCA) program evolved into what is publicly known as the "Mosquito" project, run by DSTL (Defence Science and Technology Laboratory) in partnership with companies including Blue Bear Systems Research.

**Specifications (from public MoD announcements):**
- Class: small attritable UAS, larger than PERDIX (approximately 3m wingspan for some variants)
- Weight: estimated 30-100 kg depending on variant (significantly larger than micro-drone class)
- Concept: low-cost, attritable (acceptable to lose), swarming drones that can be launched from a larger aircraft
- Endurance: projected 1-2 hours depending on variant
- Autonomy: emphasis on "loyal wingman" concepts with swarming capability
- Communication: mesh-networked, details classified
- Launch: from larger carrier aircraft, potentially wing-mounted pods
- Cost target: low enough to be expendable ("attritable")

LANCA/Mosquito is more relevant as a concept demonstrator for the "carrier launches swarm" architecture at a larger scale. The UK has publicly demonstrated swarm behaviors with 20+ drones in the "Many Drones Make Light Work" trials at Salisbury Plain (2019-2020), where Blue Bear flew autonomous swarm missions with heterogeneous drones performing ISR tasks.

### Shield AI Nova

Shield AI, founded in 2015 in San Diego, developed the Nova quadrotor for autonomous indoor reconnaissance.

**Specifications (from Shield AI public materials):**
- Type: quadrotor VTOL
- Weight: approximately 3-4 kg
- Endurance: 30-40 minutes
- Key technology: "Hivemind" autonomous AI pilot, which enables GPS-denied navigation using SLAM (Simultaneous Localization and Mapping)
- Autonomy level: Level 4-5. Nova can fly building-clearing missions with zero pilot input in GPS-denied, comms-denied environments
- Sensors: LiDAR, cameras, IMU
- Swarming: multi-agent coordination demonstrated, where multiple Novas clear different rooms/floors simultaneously
- Communication: mesh network with the ability to operate autonomously when comms are lost

**Engineering significance:** Nova demonstrates that meaningful autonomous swarming is achievable with current technology. The "Hivemind" software stack has since been adapted for larger platforms (V-BAT, F-16 as announced publicly). The key innovation is resilience -- each drone can complete its mission independently if the mesh is disrupted.

### Coyote Block 2 / Block 3 (Raytheon)

The Coyote family is a tube-launched small UAS originally developed by BAE Systems (Advanced Ceramic Research), now a Raytheon product.

**Specifications (Block 1, from public Raytheon fact sheets):**
- Length: 91 cm (36 inches)
- Wingspan: 147 cm (58 inches) when deployed
- Weight: 5.9 kg (13 lbs)
- Launch: tube-launched from aircraft (e.g., P-3 Orion sonobuoy tubes) or ground-launched
- Propulsion: electric motor, folding propeller
- Endurance: approximately 1 hour (Block 1)
- Speed: 60-70 knots
- Block 2: configured as a counter-UAS effector (kinetic kill)
- Block 3 (HOWLER): longer endurance, enhanced warhead, integrated with KuRFS radar
- Communication: datalink for command and control, details restricted
- Swarming: Coyote was one of the platforms used in DARPA/Navy swarm experimentation (LOCUST program), where 30+ Coyotes were launched in rapid succession from a ground-based multi-tube launcher

**Engineering significance:** The tube-launch mechanism is directly relevant to carrier deployment. Coyote's folding wing design fits inside a standard sonobuoy tube (A-size, 4.875" diameter). This packaging efficiency is a key reference for any carrier-deployed microdrone.

### Comparison Table

| Parameter | PERDIX | Coyote B1 | Shield AI Nova | LANCA/Mosquito |
|---|---|---|---|---|
| Weight | 290g | 5.9 kg | ~3.5 kg | 30-100 kg |
| Wingspan | 290mm | 1.47m | ~0.5m (rotor) | ~3m |
| Endurance | ~20 min | ~60 min | ~35 min | 1-2 hrs |
| Launch | Flare disp. | Tube | Hand/ground | Carrier aircraft |
| Autonomy | L3-4 | L2-3 | L4-5 | L3-4 |
| Swarm size demo'd | 103 | 30+ | 3-6 | 20+ |
| Disposable? | Yes | Yes | No | Yes (attritable) |

---

## 2. Carrier Aircraft Engineering

### Physical Carriage and Release Architectures

For a mini-UAV carrier (let us define this as approximately 15-25 kg MTOW, 3-4m wingspan, 4 kg payload capacity), there are several fundamental approaches to carrying and releasing sub-drones:

#### A. Tube Launch

The most proven method for deploying folding-wing drones from a carrier platform.

**Mechanism:** Microdrones are packaged in cylindrical tubes mounted either internally in a payload bay or externally under wings/fuselage. Deployment uses one of several ejection methods:
- **Spring-loaded piston:** A compressed spring drives a piston that pushes the drone out of the tube. Reliable, no power required, but the spring force must be carefully calibrated. Too much force damages the drone; too little and it fails to clear the tube in the carrier's slipstream.
- **Pneumatic ejection:** Compressed air (from a small CO2 cartridge or onboard pneumatic reservoir) provides more controllable and consistent ejection force. Allows velocity tuning. More complex but more reliable across temperature ranges.
- **Gravity drop with ram-air deployment:** The tube is oriented downward. The drone slides out under gravity, and a ram-air actuated deployment mechanism (like a spring-loaded catch released by airspeed) opens the wings once clear.

**Design considerations for tube launch:**
- Tube internal diameter determines maximum drone cross-section. For a 40mm tube, the folded drone must fit within a 38mm circle. For 60mm (common for small systems), more packaging options exist.
- Tube length: typically 200-350mm for PERDIX-class drones.
- Tube material: carbon fiber or aluminum for weight savings; 40mm CF tube weighs approximately 15-20g per 100mm length.
- A 4-tube launcher for 40mm drones weighs approximately 200-400g for the structure alone.
- Ejection velocity: needs to be 5-15 m/s to ensure the drone clears the carrier's wake. At carrier speeds of 20-30 m/s, the drone enters a 20-30 m/s airstream immediately, so wing deployment must occur within 0.1-0.3 seconds.

#### B. Drop Deployment (Belly Release)

Drones are carried in a recessed payload bay and released sequentially through a bay door.

**Mechanism:**
- Payload bay with a hinged or sliding door on the ventral surface
- Drones held in cradles with electromagnetic or mechanical latches
- Sequential release: one drone drops, door may close to restore aerodynamics, then reopen for next release
- Or: rapid sequential release through a continuously open bay

**Advantages:** Simpler mechanical interface; drones can be larger/more irregularly shaped than tube-constrained designs. Folding-wing drones deploy wings via spring mechanisms after clearing the carrier.

**Disadvantages:** Open bay door creates significant drag on a small aircraft. Sequential release creates time gaps. If the carrier is at low altitude, the dropped drone needs sufficient height to deploy and stabilize (minimum 15-30m altitude for safe deployment, depending on drone recovery dynamics).

**Design detail:** A belly bay for 4x drones at 500g each requires approximately 200mm x 400mm x 100mm internal volume. The bay door mechanism adds approximately 100-150g. Electromagnetic latches (12V solenoid type) weigh approximately 20-30g each and draw 0.5-1A momentarily.

#### C. Folding-Wing Ejection (Conformal Carriage)

Drones are carried in conformal pods or wing-mounted positions and ejected laterally or rearward.

**Mechanism:** Used by PERDIX (flare dispenser is essentially this). The drone is packaged with wings folded against the body, loaded into a conformal container, and ejected by mechanical force. Wings deploy via spring-loaded hinges once aerodynamic pressure acts on them.

**Wing deployment timing:** Critical engineering parameter. The drone must:
1. Clear the carrier (50-100ms after ejection)
2. Deploy wings (100-300ms, spring-loaded with detent)
3. Stabilize in powered flight (500-1000ms total from ejection)
4. During steps 1-3, the drone is in freefall/ballistic trajectory, losing 5-20m of altitude depending on speed

#### D. Payload Bay Reconfiguration

A modular payload bay is essential for mission flexibility:

**Single munition configuration (4 kg):**
- Entire bay dedicated to one payload
- Simple mounting, single release mechanism
- CG impact is a single step function at release

**4x 1 kg microdrone configuration:**
- Bay divided into 4 stations
- Each station has independent release mechanism
- Drones can be heterogeneous (e.g., 2x ISR + 2x electronic attack)
- Sequential release requires CG management (see below)

**8x 500g microdrone configuration:**
- Maximum swarm density
- Each drone is heavily constrained in size/capability at 500g
- 500g budget: ~150g airframe, ~100g battery (providing ~10-15 min endurance), ~100g avionics/sensors, ~50g motor/prop, ~100g margin
- 8 release mechanisms add weight (~200-300g total for mechanical systems)

### Center of Gravity Management

This is one of the most critical engineering challenges for a carrier-deployed swarm.

**The problem:** A 20 kg carrier aircraft releasing 4 kg of payload experiences a 20% mass reduction. If the payload is distributed across multiple stations, sequential release shifts the CG progressively.

**CG envelope analysis:**
- Typical mini-UAV CG range: 25-35% MAC (Mean Aerodynamic Chord). For a 300mm chord wing, this is a 30mm window.
- 4 drones at 1 kg each, spaced 50mm apart longitudinally, create a CG shift of approximately 2-3mm per release (depending on total aircraft mass and arm lengths).
- For a well-designed system with a 300mm chord, this 2-3mm shift per release is manageable (approximately 1% MAC per release).

**Mitigation strategies:**
1. **Symmetric release:** If drones are arranged symmetrically about the CG, release in pairs (one forward, one aft) to maintain balance. This halves the available sequential release rate but doubles CG stability.
2. **Release order optimization:** Compute the optimal release sequence that minimizes CG excursion. For N drones at known positions, this is a simple optimization problem solved pre-flight.
3. **Active trim compensation:** The carrier's flight controller adjusts elevator trim after each release. Modern autopilots (ArduPilot, PX4) can handle this if programmed with the mass change at each release event. The parameter `TRIM_THROTTLE` and elevator trim are adjusted in a pre-computed schedule.
4. **Lateral CG:** If drones are mounted under the wings, lateral CG must also be managed. Symmetric wing stations released in left-right pairs.

**Quantitative example:** 
- Carrier: 20 kg MTOW, 4 kg payload, wing chord 300mm, CG at 30% MAC (90mm from LE)
- 4 drones at 1 kg, mounted at -50mm, -25mm, +25mm, +50mm from CG
- Release sequence: +50mm first, then -50mm, then +25mm, then -25mm
- After first release: CG shifts forward by ~2.6mm (acceptable)
- After second release: CG returns to near-original (symmetric release)
- This paired-release strategy keeps CG within approximately 1% MAC throughout

### Mechanical Release Mechanisms

**Electromagnetic latch:**
- Weight: 20-40g per station
- Mechanism: 12V solenoid holds a latch pin; when energized, pin retracts, drone drops
- Hold force: 5-20 N (sufficient for 1 kg drone at 3-5g maneuvers)
- Release time: 10-50ms
- Power: 0.5-2A for 50ms (negligible energy, but peak current matters for wiring)
- Reliability: very high (>99.9%) for solenoid mechanisms
- Downside: requires electrical power, wiring to each station

**Spring-loaded mechanical release:**
- Weight: 30-60g per station
- Mechanism: a servo motor actuates a cam or lever that releases a spring-loaded cradle
- Hold force: set by spring preload
- Release time: 50-200ms (servo actuation speed limited)
- Power: servo power only, ~1A for 200ms
- Reliability: high, but more mechanical complexity

**Pneumatic ejection:**
- Weight: 100-200g for entire system (CO2 cartridge + valve + manifold)
- Mechanism: CO2 cartridge feeds a manifold with individual solenoid valves per tube
- Provides positive ejection force (important for tube launch)
- Ejection velocity: 5-20 m/s controllable by orifice sizing and pressure regulation
- CO2 cartridge: 12g cartridge provides approximately 8-12 ejections at low pressure
- Temperature sensitivity: CO2 pressure varies significantly with temperature (50 bar at 20C, 35 bar at 0C). This must be accounted for in ejection velocity calculations.

### Aerodynamic Effects of External Stores

On a mini-UAV (Re ~200,000-500,000), external stores have proportionally much larger effects than on full-scale aircraft:

**Drag increase:**
- A single 40mm diameter tube mounted externally adds approximately 5-15% drag (depending on fairing quality)
- 4 tubes mounted in a pod: 10-25% drag increase with fairing, 20-40% without
- Belly-mounted drones without fairing: each exposed drone adds 3-8% of total aircraft drag
- This directly reduces range/endurance: 20% drag increase means approximately 15-18% range reduction (for propeller aircraft, range scales approximately as 1/D)

**Stability effects:**
- External stores below the CG create a pendulum effect that is actually stabilizing in pitch
- But they add significant wetted area and may create flow separation zones that affect tail effectiveness
- Wing-mounted stores at the tips can change the effective wing aspect ratio and flutter characteristics
- For a mini-UAV at 25-35 m/s, flutter is generally not a concern (too low speed), but vibration from stores in the propwash can be significant

**Interference effects:**
- Drones mounted near the propeller disk experience propwash-induced vibration
- If drones have their own folded propellers, these can create additional parasitic drag
- Post-release, the empty cradles/tubes create cavity resonance and drag -- this should be accounted for in mission planning (the carrier gets progressively "cleaner" and faster as drones are released)

---

## 3. Communication Architecture

### Mesh Networking for Swarm Coordination

A swarm communication network must handle three fundamentally different traffic types, each with different bandwidth and latency requirements:

#### Traffic Types and Requirements

**Command traffic (ground-to-swarm):**
- Content: mission updates, target coordinates, mode changes, abort commands
- Bandwidth: very low, 100-500 bytes per message, 1-10 messages per second to entire swarm
- Latency: moderate, 100-500ms acceptable for mission-level commands
- Reliability: critical -- must use acknowledged delivery with retransmission
- Total bandwidth: <10 kbps for a swarm of 8

**Telemetry (swarm-to-ground and inter-swarm):**
- Content: position, velocity, attitude, battery state, sensor status
- Bandwidth per drone: 200-500 bytes at 5-10 Hz = 8-40 kbps per drone
- For 8-drone swarm: 64-320 kbps total
- Latency: 50-200ms for situational awareness; 10-50ms for coordinated maneuvers
- Reliability: best-effort acceptable (missing one update is not critical)

**Video/sensor data (swarm-to-ground):**
- Content: compressed video (H.264/H.265), imagery, sensor readings
- Bandwidth per drone: 500 kbps (low quality) to 5 Mbps (720p decent quality)
- For 8 drones simultaneously: 4-40 Mbps (impractical for all streams simultaneously)
- Practical approach: only 1-2 drones stream video at a time; others store on-board or transmit compressed keyframes
- Latency: 200-1000ms acceptable for ISR; <100ms for teleoperation

#### Network Topology Options

**Option 1: Carrier as Central Relay**
```
Ground Station <--long range link--> Carrier <--short range mesh--> Swarm Members
```
- Carrier maintains the long-range link to ground station (higher power radio, directional antenna)
- Swarm members use low-power short-range links to communicate with carrier and each other
- Advantages: swarm members can be simpler/lighter (smaller radio), carrier provides range extension
- Disadvantages: single point of failure at carrier; carrier must remain in communication range of all swarm members
- Range budget: carrier-to-ground 5-20 km (depending on power/frequency); carrier-to-swarm 500m-2km

**Option 2: Flat Peer-to-Peer Mesh**
```
Ground Station <--link--> Any Swarm Member <--mesh--> All Swarm Members
```
- Every drone is equal; any drone can relay to ground station
- Messages hop through the mesh to reach all members
- Advantages: no single point of failure; self-healing network
- Disadvantages: every drone needs a capable radio; latency increases with hop count; bandwidth decreases with mesh size
- Practical mesh limit: 8-16 nodes before bandwidth/latency degrades significantly

**Option 3: Hybrid (Recommended)**
```
Ground Station <--long range--> Carrier + designated relay drones
Carrier <--short range mesh--> Swarm Members
Swarm Members <--peer-to-peer--> Adjacent Swarm Members
```
- Carrier serves as primary relay but is not a single point of failure
- Swarm members can communicate peer-to-peer for time-critical coordination (collision avoidance, formation adjustments)
- One or two swarm members designated as backup relays to ground
- Best balance of resilience, bandwidth, and weight

#### Specific Hardware Options

**ESP32 (Espressif ESP-NOW / WiFi Mesh):**
- Frequency: 2.4 GHz
- Range: 200-500m open air (with PCB antenna), up to 1km with external antenna
- Bandwidth: up to 1 Mbps (ESP-NOW), 20+ Mbps (WiFi)
- Latency: 1-5ms (ESP-NOW point-to-point)
- Weight: 3-5g for bare module (ESP32-C3 Mini)
- Power: 80-240mA transmit, 10-30mA idle
- Cost: $2-4 per module
- Mesh support: ESP-MDF (Mesh Development Framework) supports up to 1000 nodes theoretically; practically tested to ~50
- Pros: dirt cheap, excellent SDK, WiFi allows video streaming, very lightweight
- Cons: 2.4 GHz is crowded; range is limited; not suitable for carrier-to-ground long range link
- **Best for:** inter-swarm short-range coordination

**XBee (Digi International) -- XBee 900HP or XBee SX 868:**
- Frequency: 900 MHz (or 868 MHz for EU)
- Range: 2-5 km (900HP with wire antenna), up to 14 km (XBee SX with high-gain antenna)
- Bandwidth: 10-200 kbps
- Latency: 5-30ms
- Weight: 5-8g for module; 15-30g with antenna and interface board
- Power: 200-500mA transmit at 3.3V
- Cost: $30-50 per module
- Mesh support: DigiMesh protocol, up to 64 nodes
- Pros: excellent range, sub-GHz penetrates obstacles better, proven mesh protocol
- Cons: low bandwidth (no video), relatively expensive, moderate weight
- **Best for:** command/telemetry links, carrier-to-swarm

**RFD900x (RFDesign):**
- Frequency: 902-928 MHz
- Range: up to 40 km with appropriate antennas
- Bandwidth: up to 750 kbps (raw), ~500 kbps usable
- Latency: 5-20ms
- Weight: 15g module + antenna
- Power: 1W transmit (1A at 5V peak)
- Cost: $80-120 per unit
- Mesh support: point-to-point and multipoint (up to 4 nodes natively; mesh requires custom firmware)
- Pros: longest range, well-supported by ArduPilot/PX4, reliable
- Cons: not natively mesh; heavy for microdrones; high power draw
- **Best for:** carrier-to-ground long-range link

**LoRa SX1276/SX1262 (Semtech):**
- Frequency: 433 MHz, 868 MHz, or 915 MHz
- Range: 5-15 km (depending on spreading factor and antenna)
- Bandwidth: 0.3-37.5 kbps (LoRa modulation), up to 300 kbps (FSK mode on SX1262)
- Latency: 30-200ms (LoRa modulation is inherently slow due to chirp spreading)
- Weight: 2-5g for bare module; 8-15g with antenna and breakout
- Power: 40-120mA transmit
- Cost: $5-15 per module
- Mesh support: custom mesh implementations available (e.g., Meshtastic); no native mesh
- Pros: exceptional range-to-power ratio, very lightweight, cheap
- Cons: very low bandwidth (telemetry only, forget video), high latency
- **Best for:** emergency/backup link, low-rate telemetry, long-range heartbeat

#### Recommended Architecture for 8-Drone Swarm from Carrier

**Primary inter-swarm link: ESP32 (ESP-NOW)**
- Each microdrone carries an ESP32-C3 Mini (3g, $3)
- ESP-NOW provides <5ms latency for formation coordination
- 200-500m range sufficient for swarm spacing of 20-100m
- Bandwidth sufficient for telemetry sharing at 10 Hz among all 8 drones

**Carrier-to-swarm command link: LoRa SX1262 at 915 MHz**
- Carrier carries a LoRa transceiver (10g)
- Each microdrone carries a LoRa transceiver (8g)
- Provides 2-5 km range for mission commands even when swarm disperses
- Low bandwidth (sufficient for commands and compressed telemetry)
- Serves as backup if ESP-NOW mesh fails

**Carrier-to-ground link: RFD900x**
- Carrier carries RFD900x (15g + antenna)
- Provides 10-40 km range to ground station
- 500 kbps sufficient for carrier telemetry + aggregated swarm status
- Video from carrier's own camera if equipped

**Total radio weight per microdrone:** approximately 11-15g (ESP32 + LoRa module + antennas)
**Total radio weight on carrier:** approximately 30-40g (ESP32 + LoRa + RFD900x + antennas)

#### Frequency Management

With 8 drones plus a carrier all transmitting, frequency management is critical:

- **2.4 GHz band (ESP-NOW):** Use channel hopping across WiFi channels 1, 6, 11 to avoid self-interference. ESP-NOW supports this natively. Time-Division Multiple Access (TDMA) allocation: each drone gets a 1ms slot in a 10ms frame, leaving 2ms for carrier commands.
- **915 MHz band (LoRa):** Single channel with TDMA. Carrier transmits commands in first 100ms of each second; drones respond in assigned 100ms slots. With 8 drones, full round-robin in 1 second.
- **900 MHz (RFD900x):** Frequency-hopping spread spectrum (FHSS) built into the RFD900x, automatically avoids the LoRa channel.

---

## 4. Autonomous Swarm Behaviors

### Consensus Algorithms for Formation Flying

Formation flying requires all swarm members to agree on a shared reference frame and their positions within it. Several algorithm families address this:

#### Reynolds Flocking Rules (1987)

The foundational model for emergent swarm behavior, using three simple rules applied to each agent:

1. **Separation:** Steer to avoid crowding local flockmates. Each drone computes a repulsive vector from all neighbors within a "separation radius" (typically 2-5 body lengths, so 1-3m for microdrones).
2. **Alignment:** Steer toward the average heading of local flockmates. Each drone adjusts its heading toward the mean heading of neighbors within an "alignment radius" (typically 5-20m).
3. **Cohesion:** Steer toward the average position of local flockmates. Each drone moves toward the centroid of neighbors within a "cohesion radius" (typically 10-50m).

**Implementation for real drones:**
- Each drone broadcasts its position and velocity at 5-10 Hz via ESP-NOW
- Local computation: for each received neighbor state, compute separation, alignment, and cohesion vectors
- Weight the three vectors (tuning parameters: w_sep, w_align, w_coh)
- Sum with mission-level waypoint attraction vector
- Convert to velocity command for flight controller
- Computational cost: O(N) per drone per timestep, trivially handled by any modern microcontroller

**Limitations:** Reynolds rules produce organic, fluid formations but not precise geometric patterns. For structured formations (V-formation, line abreast, etc.), additional position assignment is needed.

#### Olfati-Saber Consensus Protocol (2006)

A mathematically rigorous framework for multi-agent consensus with guaranteed convergence:

The protocol defines potential functions between agents:
- **Attractive potential** at long range (pulls agents toward desired inter-agent distance)
- **Repulsive potential** at short range (prevents collision)
- **The combination** creates a virtual spring-damper system between each pair of agents

**Key equations (simplified):**
- Each agent i updates its velocity based on: u_i = Σ_j [∇φ(||q_j - q_i||)] + Σ_j [a_ij(p_j - p_i)] + f_i^γ
  - First term: gradient of pairwise potential function (formation shape)
  - Second term: velocity consensus (alignment), where a_ij is the adjacency weight
  - Third term: navigational feedback (move toward goal)

**Properties:**
- Provably converges to desired formation if the communication graph is connected
- Handles dynamic topology (drones entering/leaving communication range)
- Can enforce specific inter-agent distances (unlike Reynolds)
- Requires each drone to know its own state accurately (GPS + IMU)

**Practical implementation:**
- Each drone maintains a neighbor table updated at 5-10 Hz
- Potential function computation: ~100 floating-point operations per neighbor per timestep
- For 8 neighbors: ~800 FLOPS per timestep at 10 Hz = 8 KFLOPS (negligible computational load)
- Tuning the potential function shape and damping parameters is the main engineering challenge

#### Hungarian Algorithm (for Task/Position Assignment)

When drones must be assigned to specific positions in a formation (or specific tasks), the Hungarian algorithm solves the optimal assignment problem:

- Input: an N×M cost matrix where entry (i,j) is the cost (usually distance) for drone i to take position j
- Output: the minimum-cost one-to-one assignment
- Complexity: O(N³) -- for 8 drones, this is 512 operations, computed in <1ms on any microcontroller
- Used when the formation shape changes: reassign drones to new positions to minimize total travel distance
- Also used for task allocation: assign drones to search zones, targets, etc.

### Task Allocation Algorithms

#### Auction-Based (Market-Based) Allocation

Each task is "auctioned" among drones. Drones "bid" based on their suitability (distance to task, remaining battery, sensor capability). The highest bidder wins the task.

**Consensus-Based Bundle Algorithm (CBBA):**
- Each drone maintains a list of tasks and bids
- Drones exchange bid information via mesh network
- Through iterative bidding and consensus, tasks are allocated without a central auctioneer
- Handles task dependencies, diminishing returns, timing constraints
- Converges in O(N_t × N_d) message rounds where N_t = tasks, N_d = drones
- For 8 drones and 16 tasks: convergence in <2 seconds with 10 Hz communication

**Advantages:** Decentralized, robust to drone loss, handles heterogeneous capabilities
**Disadvantages:** May not find globally optimal solution; convergence time increases with swarm size

#### Centralized Planning (on Carrier or Ground Station)

- A single planner (running on the carrier's computer or ground station) computes the optimal task allocation
- Uses full knowledge of all drone states and all tasks
- Can use integer linear programming (ILP) or mixed-integer programming for optimal solutions
- For 8 drones: ILP solves in milliseconds on modern hardware
- Broadcasts assignments to all drones

**Advantages:** Globally optimal, simple to implement
**Disadvantages:** Single point of failure; requires reliable communication to all drones

**Recommendation for 8-drone mini-UAV swarm:** Use centralized planning on the carrier as the primary method, with CBBA as a fallback when communication to the carrier is lost. The swarm is small enough that centralized planning is computationally trivial and communication bandwidth is sufficient.

### Collision Avoidance Within the Swarm

**Layered approach:**

1. **Strategic layer (mission planning):** Assign non-overlapping areas or altitudes to drones. Simplest: altitude deconfliction with 5-10m vertical separation.

2. **Tactical layer (formation control):** The consensus/flocking algorithms inherently maintain inter-agent spacing. Olfati-Saber's repulsive potential function prevents agents from getting closer than a minimum distance.

3. **Reactive layer (emergency avoidance):** Each drone runs a reactive collision avoidance algorithm:
   - **Velocity Obstacles (VO):** Given a neighbor's position and velocity, compute the set of own-velocities that would lead to collision within a time horizon. Choose a velocity outside this set.
   - **ORCA (Optimal Reciprocal Collision Avoidance):** Extension of VO where each drone takes responsibility for half the avoidance maneuver. Guarantees collision-free trajectories if all drones run ORCA.
   - **Time horizon:** Typically 2-5 seconds. For drones at 10-20 m/s, this means reacting to threats 20-100m away.
   - **Update rate:** Reactive avoidance must run at 10-20 Hz minimum.

4. **Last-resort layer:** If an imminent collision is detected (<1 second, <5m), execute a hard avoidance maneuver (maximum climb for one drone, maximum descent for the other, based on deterministic priority rules like "lower ID number climbs").

### Degraded Mode Operations

**When swarm members are lost:**

1. **Detection:** Heartbeat monitoring. Each drone broadcasts a heartbeat at 2-5 Hz. If 3 consecutive heartbeats are missed (0.6-1.5 seconds), the drone is declared lost by its neighbors.

2. **Formation adaptation:**
   - Remaining drones re-run the Hungarian algorithm to fill gaps
   - Formation may scale down (e.g., from 8-point to 7-point pattern)
   - Or remaining drones spread out to maintain coverage area (increase inter-agent distance)

3. **Task reallocation:**
   - Lost drone's tasks are re-auctioned among remaining drones via CBBA
   - Priority-based: critical tasks (e.g., target tracking) are reallocated immediately; low-priority tasks (e.g., mapping the last 10% of an area) may be dropped

4. **Communication topology repair:**
   - If the lost drone was a critical relay node, remaining drones adjust positions to maintain mesh connectivity
   - Graph connectivity algorithms (e.g., algebraic connectivity / Fiedler value monitoring) run continuously
   - If the Fiedler value drops below a threshold, drones move to increase connectivity

5. **Graceful degradation thresholds:**
   - 8 → 6 drones: full mission capability with reduced coverage rate
   - 6 → 4 drones: mission continues with reduced area or reduced sensor coverage
   - 4 → 2 drones: switch to paired operation mode
   - 2 → 1 drone: single drone continues independently or returns to carrier
   - 0 drones: carrier operates independently or returns to base

### Emergent vs. Scripted Coordination

**Emergent behavior** (Reynolds-type rules): Each drone follows simple local rules. Complex global patterns emerge from local interactions. Advantages: robust, scalable, handles unexpected situations. Disadvantages: difficult to predict exact behavior; hard to guarantee specific coverage or timing.

**Scripted coordination** (pre-planned waypoints/formations): Each drone follows a pre-computed trajectory. Advantages: predictable, verifiable, meets specific mission requirements. Disadvantages: brittle when conditions change; requires re-planning for any deviation.

**Recommended hybrid approach:** Use scripted coordination for the mission-level plan (area assignments, search patterns, timing) and emergent behavior for the tactical level (formation maintenance, obstacle avoidance, dynamic spacing). The carrier computes and distributes the mission plan; individual drones execute it using local autonomous behaviors.

---

## 5. Mission Planning for Swarms

### Multi-Agent Mission Planning Architecture

Traditional single-drone mission planning (waypoint lists) is insufficient for swarms. The mission engine must handle:

**Temporal coordination:** Drones must arrive at positions at coordinated times. A simple waypoint list has no concept of "arrive at waypoint 3 at the same time as drone B arrives at its waypoint 3." The mission planner must compute velocity profiles for each drone to achieve synchronized arrivals.

**Spatial deconfliction:** Routes must not intersect at the same time. For 8 drones operating in a shared area, this requires 4D (x, y, z, t) trajectory planning.

**Contingency planning:** For each possible drone failure, the mission planner should have a pre-computed reallocation plan (or the ability to compute one in real time).

### Area Decomposition

For a search or surveillance mission, the swarm must divide a target area among N drones:

#### Voronoi Partitioning
- Compute the Voronoi tessellation of the area based on drone positions
- Each drone is responsible for the region closest to it
- Dynamically updates as drones move
- Handles non-convex areas with constrained Voronoi
- Computational cost: O(N log N) for N drones -- trivial for 8

#### Grid-Based Decomposition
- Divide the area into a grid of cells
- Assign cells to drones using the Hungarian algorithm or auction-based allocation
- Each drone plans a coverage path within its assigned cells
- Simple to implement; works well for regular areas
- Cell size determined by sensor footprint (e.g., camera field of view at operating altitude)

#### Example: 1 km² search area, 8 drones
- Each drone responsible for 125,000 m² (approximately 354m × 354m)
- At 50m swath width (camera FOV at 100m altitude) and 15 m/s speed:
  - Lawnmower path length: 354m × (354/50) ≈ 2,500m
  - Time to cover: 2,500/15 ≈ 167 seconds ≈ 2.8 minutes
- Compare single drone: 8× longer = 22 minutes
- With 20-minute microdrone endurance, the swarm can cover the area while a single drone cannot

### Cooperative Coverage Path Planning

**Boustrophedon (lawnmower) decomposition:**
- Standard approach: decompose area into cells, plan lawnmower path in each cell
- Multi-agent: assign cells to drones, each plans own lawnmower path
- Overlap handling: ensure sensor footprints overlap slightly at cell boundaries (5-10% overlap)

**Spiral coverage:**
- Drones start at the perimeter and spiral inward
- Better for circular or irregular areas
- Multiple drones can spiral from different starting points

**Frontier-based exploration:**
- Originally from robotics (Yamauchi 1997)
- Drones are attracted to unexplored frontiers (boundaries between explored and unexplored areas)
- Each drone selects the nearest unassigned frontier
- Naturally distributes drones across the area
- Handles dynamic environments where new areas of interest are discovered

### Dynamic Retasking

When a drone fails mid-mission:

1. **Immediate response (0-2 seconds):** Collision avoidance by neighbors; heartbeat timeout detection
2. **Task recovery (2-5 seconds):** Failed drone's remaining area is identified; CBBA re-auction among surviving drones
3. **Path replanning (5-10 seconds):** Affected drones recompute their coverage paths to include the orphaned area
4. **Mission timeline update (10-30 seconds):** Overall mission completion estimate updated; if mission cannot be completed with remaining drones, prioritize high-value areas

**Implementation:** Each drone maintains not just its own task list but a shared task board (replicated via mesh). When a drone is detected as lost, any drone can initiate re-auction of orphaned tasks without waiting for a central coordinator.

### Data Fusion

Combining observations from multiple drones:

**Position-based fusion:**
- Each drone tags observations with GPS coordinates and timestamps
- Ground station (or carrier) maintains a composite map
- Overlapping observations are merged using weighted averaging (weights based on sensor quality, range, viewing angle)

**Track fusion (for moving targets):**
- Multiple drones may observe the same target from different angles
- Covariance intersection or federated Kalman filtering merges tracks
- Cross-correlation is a challenge: if two drones see a moving object, is it the same object?
- Solution: gating (only fuse if observations are within spatial and temporal gates)

**Distributed detection:**
- Binary decision fusion: each drone sends a detection/no-detection bit for a grid cell
- Fusion center applies optimal decision rule (e.g., k-out-of-N rule: declare target present if at least k of N drones detected it)
- Significantly improves detection probability and reduces false alarm rate compared to single sensor

---

## 6. Applications

### Area Surveillance (Distributed Sensor Network)

Deploy 8 microdrones in a persistent surveillance pattern over a 1-2 km² area. Each drone orbits a designated station point, providing overlapping sensor coverage. With 20-minute endurance, the carrier can cycle: deploy set 1, loiter for 15 minutes, deploy set 2 to replace, recover or abandon set 1. The mesh network provides real-time data aggregation. Change detection algorithms identify new activity across the distributed sensor network.

### Search and Rescue

Parallel search with 8 drones covers area 8× faster than a single drone. In the critical "golden hour" after a disaster, this speed multiplication is the primary value. Drones carry optical cameras and thermal imagers (FLIR Lepton at 1g, $200). Frontier-based exploration is ideal: drones naturally spread out and are attracted to unsearched areas. When a potential detection occurs, neighboring drones converge for multi-angle confirmation, reducing false positives.

### Agricultural Pest Monitoring

Distributed sampling across a large field. Each microdrone carries a miniature spectrometer or multispectral camera (available at <50g). The swarm provides simultaneous sampling across the field, capturing a temporal snapshot that a single slow-moving drone cannot. Critical for detecting pest outbreaks that spread rapidly -- the spatiotemporal resolution of 8 simultaneous samples catches spreading patterns that sequential sampling misses.

### Environmental Monitoring

Distributed air/water quality sampling. Each drone carries a gas sensor array (e.g., Sensirion SGP40 VOC sensor, 2g) or descends to collect water samples. The swarm maps concentration gradients in real time, enabling plume tracking (following a chemical plume to its source using cooperative gradient ascent algorithms). This requires at least 3-4 spatially separated measurements to estimate gradient direction -- perfect for a swarm.

### Electronic Warfare / Decoy Applications

**Distributed jamming:** Each microdrone carries a small RF emitter. Spatial distribution makes the jamming source difficult to locate and defeat. 8 drones at 500mW each provide 4W total radiated power from 8 different directions.

**Decoy/saturation:** Microdrones equipped with radar reflectors (corner reflectors or Luneberg lenses) can simulate the radar cross-section of a larger aircraft. 8 decoys overwhelm air defense tracking capacity. At approximately $50-200 per disposable drone, this is vastly cheaper than any air defense missile.

---

## 7. Feasibility Assessment for Mini-UAV Carrier

### Realistic Swarm Size Given 4 kg Payload

**Budget analysis for 4 kg total payload:**

The 4 kg must cover: drone mass × N + launcher mechanism + wiring/structural integration.

Launcher system overhead:
- 8-tube launcher structure: ~300g (carbon fiber tubes + mounting frame)
- Pneumatic system (CO2 + valves): ~150g
- Wiring and connectors: ~100g
- Total overhead: ~550g

Available for drones: 4000g - 550g = 3450g

**Drone size options:**

| Config | Drone mass | Number | Mass budget | Drone endurance | Capability |
|---|---|---|---|---|---|
| Large | 800g | 4 | 3200g | 25-35 min | Camera + compute |
| Medium | 430g | 8 | 3440g | 15-20 min | Camera, basic |
| Small | 250g | 12 | 3000g | 8-12 min | Minimal sensor |
| Micro | 150g | 16+ | 2400g+ | 5-8 min | Beacon/decoy only |

**Recommended configuration:** 8 drones at approximately 430g each provides the best balance of swarm size and individual capability. This is close to the PERDIX class (290g) but with slightly more capability.

### Minimum Viable Microdrone

**What is the smallest drone that can perform useful work?**

At the absolute minimum for a fixed-wing microdrone:
- Airframe (3D-printed or foam): 40-60g
- Motor + propeller (brushless outrunner, 1806 class): 25-35g
- ESC (micro, 6-10A): 5-8g
- Flight controller (STM32-based micro FC): 5-10g
- GPS (uBlox MAX-M10S): 2-3g
- IMU (integrated on FC): 0g additional
- Radio (ESP32-C3 + LoRa): 10-15g
- Battery (1S 600mAh LiPo for ~8 min, or 2S 450mAh for ~10 min): 20-35g
- Camera (OV2640 or similar, 0.3MP minimum): 2-5g
- Structural (fasteners, wires, connectors): 10-20g

**Total minimum: approximately 120-190g**

At 150g, with a 30g battery (1S 700mAh), endurance is approximately 8-12 minutes at 12-15 m/s cruise speed, giving a range of 6-10 km. This is marginally useful for ISR but effective for decoy, communication relay, or sensor deployment roles.

**At 430g (recommended):**
- Higher capacity battery: 2S 1000mAh (55g) → 15-20 min endurance
- Better camera: 2MP with video (5g)
- Full dual-radio stack: ESP32 + LoRa (15g)
- More capable flight controller with onboard logging
- Stronger airframe for higher wind tolerance
- Range: 15-20 km at 15 m/s

### Power and Endurance Tradeoffs

For a micro fixed-wing at 430g:
- Wing loading: approximately 30-40 g/dm² (for 100-140 dm² wing area, i.e., ~33cm span × 3.5cm chord × 2 panels)
- Actually, let me recalculate: 430g at 35 g/dm² needs 12.3 dm² wing area → ~35cm × 35cm wing area is impractical for a tube-launched drone
- More realistic: 430g at 50-60 g/dm² needs 7-8.6 dm² → wingspan 50-60cm with 14-15cm chord
- Cruise power: approximately 10-15W for level flight at 12-15 m/s
- Battery: 2S 1000mAh = 7.4 Wh
- Available energy (80% usable): 5.9 Wh
- Endurance at 12W: 5.9/12 = 0.49 hours ≈ 30 minutes
- Endurance at 15W (with payload power + radio): 5.9/15 = 0.39 hours ≈ 24 minutes
- Real-world derating (wind, maneuvering, 20%): approximately 18-20 minutes

### Recovery vs. Disposable

**Can microdrones return to the carrier?**

This is extremely challenging for several reasons:
1. **Mid-air recovery:** Requires precise rendezvous (sub-meter accuracy) at relative speeds of 5-15 m/s. Mechanisms like trailing nets or magnetic capture cones have been demonstrated at larger scales (DARPA Gremlins program with C-130) but are impractical at mini-UAV scale.
2. **Landing and retrieval:** Microdrones could land at a designated point for manual collection. This is feasible but defeats the purpose of the carrier concept.
3. **Net recovery by carrier:** The carrier trails a net or line; microdrones fly into it. Attempted in research but reliability is very low (<50% success rate in benign conditions).

**Recommendation: Design for disposable operation.** This simplifies the microdrone design (no landing gear, simpler structure), reduces weight, and avoids the immense complexity of autonomous mid-air recovery. The economic model must support this.

### Cost Per Unit for Disposable Swarm Members

**Bill of Materials for 430g microdrone (production quantity 100):**

| Component | Cost |
|---|---|
| Airframe (injection-molded EPP foam + 3D-printed parts) | $15-25 |
| Motor (1806 brushless) | $8-12 |
| ESC (micro 10A) | $5-8 |
| Propeller (folding, 5") | $3-5 |
| Flight controller (custom STM32 PCB) | $15-25 |
| GPS module (uBlox) | $10-15 |
| Radio stack (ESP32 + LoRa) | $8-12 |
| Camera module | $5-10 |
| Battery (2S 1000mAh) | $8-12 |
| Wiring, connectors, structural | $5-10 |
| Assembly labor | $15-25 |
| **Total per unit** | **$97-159** |

At scale (quantity 1000+), costs drop to approximately $60-100 per unit through PCB integration (combine FC + radio + camera on single board), bulk component purchasing, and automated assembly.

**The $100 disposable drone is achievable today.** This compares favorably with the cost of alternatives: a single precision munition costs $20,000+; a Javelin missile costs $175,000. Even in civilian applications, 8 × $100 drones ($800 total) covering an area in 3 minutes vs. one $5,000 drone covering it in 24 minutes is compelling.

### Feasibility Summary

| Parameter | Assessment |
|---|---|
| Swarm size from 4kg payload | 8 drones at 430g: feasible |
| Microdrone endurance | 18-20 minutes: adequate for most missions |
| Communication | Dual-radio (ESP32 + LoRa): proven technology, 15g per drone |
| Autonomous coordination | Olfati-Saber consensus + CBBA: well-studied, implementable on STM32 |
| Carrier CG management | Paired symmetric release: straightforward |
| Release mechanism | Pneumatic tube launch: proven (PERDIX heritage) |
| Recovery | Not feasible at this scale; design for disposable |
| Cost per swarm member | $100-150 in moderate quantity |
| Total swarm cost | $800-1,200 for 8 disposable drones |
| Technical readiness | TRL 4-5: all subsystems demonstrated individually; system integration is the remaining challenge |

The primary engineering risks are: (1) reliable tube deployment at mini-UAV scale and speed, requiring extensive flight testing; (2) mesh network reliability in dynamic RF environments; and (3) autonomous coordination software maturity for field operations. All three are engineering challenges with known solution paths, not fundamental research problems.
