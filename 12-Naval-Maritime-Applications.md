# Maritime & Naval Applications for Mini Fixed-Wing UAV Platform

**Platform Reference Spec:** 2–4 m wingspan | pusher propeller | electric | 4 kg max payload | ArduPilot autopilot

---

## 1. Maritime Patrol and Surveillance

### Operational Concept

Small fixed-wing UAVs are already the workhorse of maritime surveillance. The mission is straightforward: fly long-duration tracks over coastal waters and relay real-time video and sensor data to a ground station. Targets include illegal fishing vessels, smuggling craft, migrant boats, and general maritime domain awareness.

### Payload Requirements

| Component | Weight | Power | Notes |
|---|---|---|---|
| EO/IR gimbal (e.g., FLIR Vue TZ20, Micro MiniPOP) | 0.5–1.5 kg | 5–15 W | Dual-sensor (visible + LWIR thermal) for day/night vessel detection |
| AIS receiver (e.g., dAISy, Vesper Cortex M1) | 50–150 g | 1–2 W | Receives 161.975/162.025 MHz; correlates radar/visual contacts with ship identity |
| Onboard SBC for processing (Raspberry Pi CM4 or Jetson Orin Nano) | 100–200 g | 5–15 W | Edge detection, target classification, AIS correlation |
| Data link (e.g., Doodle Labs Helix, Microhard pDDL) | 150–300 g | 5–10 W | 50–100+ km range, encrypted video downlink |
| **Total** | **~1.0–2.2 kg** | **~16–42 W** | Well within 4 kg payload budget |

### Mission Profile

- **Patrol route:** Racetrack or lawnmower pattern along a coastline, typically 10–50 km offshore.
- **Altitude:** 300–1000 m AGL for wide-area coverage; lower for identification passes.
- **Endurance target:** 3–6 hours minimum for meaningful maritime patrol. This is the limiting factor for electric platforms — a 2–4 m wingspan electric UAV typically achieves 1.5–3 hours. Solar-assist panels on the wing can extend this to 4–5 hours.
- **ArduPilot modes:** AUTO (waypoint patrol), LOITER (orbit a contact), RTL for recovery.

### Feasibility: HIGH

This is the most mature and realistic application. ScanEagle (3.1 m wingspan, 13 kg fuel-powered) has operated from ships for two decades. Tekever AR5 (now operated by the European Maritime Safety Agency) runs routine coastal patrols. Insitu/Boeing and Textron Aerosonde do the same. Your electric platform is lighter and shorter-ranged but perfectly capable of coastal patrol out to 30–50 km with a relay or mesh network. Many companies already sell systems in this exact class: Penguin C (UAV Factory), Albatross (Applied Aeronautics), and senseFly eBee.

### Key References

- **ScanEagle** — Insitu/Boeing. 3.1 m wingspan, 20+ hour endurance (fuel). Catapult launch, SkyHook recovery. Operated by US Navy, USCG, and dozens of navies.
- **Tekever AR5** — 4.4 m wingspan, 3.8 kg payload, 16-hour endurance (fuel). Operated by EMSA for fisheries and border patrol across the Mediterranean.
- **Penguin C** — UAV Factory. 3.3 m wingspan, EFI gasoline engine, 20+ hours. Widely used for maritime ISR.
- **Insitu Integrator** — Larger (4.9 m) but same mission set.

---

## 2. Anti-Submarine Warfare (ASW) — Sonobuoy Deployment

### What Are Sonobuoys?

Sonobuoys are expendable acoustic sensors dropped from aircraft into the ocean. On hitting the water, they deploy a hydrophone array to a preset depth and begin listening for (passive) or actively pinging (active) submarine noise signatures. Data is transmitted via VHF radio (136–173.5 MHz, 99 standard channels) to the deploying aircraft or a shore station. They are the primary tool for wide-area submarine detection used by P-3 Orion, P-8 Poseidon, and MH-60R helicopters.

### Standard Sonobuoy Specifications

| Designator | Type | Function | Weight | Dimensions | Depth | Endurance |
|---|---|---|---|---|---|---|
| AN/SSQ-36 (BT) | Passive | Bathythermograph — measures water temperature profile to calibrate other buoys | 5.0 kg | A-size (124 mm dia × 914 mm) | Variable | Single measurement |
| AN/SSQ-53 (DIFAR) | Passive | Directional frequency analysis and recording — primary passive detection buoy | 4.5 kg | A-size | 27–305 m selectable | 1, 2, 4, or 8 hours |
| AN/SSQ-62 (DICASS) | Active | Directional command-activated sonobuoy system — active ping on command | 5.5 kg | A-size | 27–457 m | 30 min to 8 hours |
| AN/SSQ-101 (ADAR) | Passive | Advanced deployable acoustic receiver — multi-element array | ~15 kg | A-size (×2 length) | Deep | Hours |

### Can a Mini-UAV Carry One?

**The honest answer: barely, and only the lightest variants.**

A standard AN/SSQ-53 at 4.5 kg exceeds the 4 kg payload limit. Even if you shaved to exactly 4 kg, the buoy's A-size form factor (124 mm × 914 mm — nearly a meter long) creates severe integration problems for a 2–4 m wingspan airframe. The buoy would need to be carried externally or in a belly bay, significantly affecting aerodynamics.

**More importantly:** a single sonobuoy is operationally useless for ASW. Submarine localization requires deploying a *pattern* of buoys — typically 6–12 or more in a barrier or cross pattern — so a single-buoy-per-sortie platform has extremely limited tactical value.

### Smaller/Lighter Alternatives

The real opportunity is in miniature acoustic sensors:

| Device | Weight | Notes |
|---|---|---|
| **Ultra Electronics HIDAR miniature sonobuoy** | ~2 kg | Reduced-size passive buoy designed for UAV deployment |
| **Thales Compact Sonobuoy** | ~2.5 kg | Designed for smaller platforms |
| **DARPA DASH (Distributed Agile Submarine Hunting)** | ~1–2 kg | Concept for networked mini-buoys deployed by drones |
| **Custom miniature hydrophone buoy** | 0.5–1.5 kg | Commercial hydrophone (e.g., Cetacean Research C75) + VHF transmitter + float + battery. DIY deployable |
| **RSAqua "Sono.Micro"** concept | ~1 kg | Academic/startup miniature acoustic buoy designs |

With a 4 kg payload, you could carry 2–4 miniature (1 kg) acoustic buoys and deploy them in a pattern across multiple passes or sorties.

### Sonobuoy Data Transmission

- Standard sonobuoys transmit raw acoustic data on VHF channels (136–173.5 MHz).
- The receiving aircraft (or ground station) needs a sonobuoy receiver and acoustic processor (e.g., AN/ARR-78 on P-3, or a modern software-defined radio equivalent).
- For a mini-UAV system, you would either relay the VHF data through the drone's datalink or (more practically) have a ground/ship station with a VHF receiver within line-of-sight of the buoys.

### Mission Profile

1. Fly to search area at 300–500 m altitude.
2. Deploy buoys at calculated spacing (typically 3–10 km apart depending on water conditions and expected detection range).
3. Either orbit overhead to relay VHF data, or return to base while a ship/shore station receives directly.
4. For active buoys: command activation via VHF uplink when a passive detection is made.

### Reference: MQ-8 Fire Scout

The MQ-8B/C Fire Scout (unmanned helicopter, 1400 kg MTOW, ~270 kg payload) has been tested for sonobuoy deployment by the US Navy. It carries a rotary launcher with multiple A-size buoys. This is a platform 100× the size and cost of a mini fixed-wing — which illustrates the scale mismatch. The Navy is also exploring the MQ-9B SeaGuardian (5 tonnes+) for ASW.

### Feasibility: LOW to MODERATE

- **Standard sonobuoys:** Not feasible. Too heavy, too large, and one-per-sortie is tactically useless.
- **Miniature acoustic buoys (1–2 kg):** Moderately feasible. You could carry 2–3 per sortie and deploy a field over multiple flights. This is a research/niche application, not a replacement for P-8 Poseidon ASW.
- **Best use case:** Deploying a network of cheap, lightweight acoustic nodes for harbor defense or chokepoint monitoring (think persistent acoustic tripwire, not open-ocean submarine hunting).
- **DARPA and ONR are actively funding** miniaturized ASW payloads for small UAVs and USVs, so this space may become more viable in the 2027–2030 timeframe.

---

## 3. Miniature Sonar Modules

### Concept

Rather than traditional sonobuoys, deploy compact sonar devices from the UAV — either as floating buoys or tethered sensors lowered to the surface.

### Available Hardware

| Device | Type | Weight | Detection | Price | Notes |
|---|---|---|---|---|---|
| **Blue Robotics Ping Sonar** | Single-beam echosounder | 44 g (in-water) | 30 m range, 300 m depth | ~$280 | Designed for ROVs. Needs waterproof housing + battery + data link for autonomous buoy use |
| **Blue Robotics Ping360** | Scanning sonar (mechanical) | 310 g (in-water) | 50 m range, 360° | ~$2500 | Excellent for sub-surface object detection. Would need float + battery + radio = ~1.5 kg total buoy |
| **Imagenex 852** | Miniature side-scan | ~2 kg (in-air) | 120 m swath | ~$8000 | Compact side-scan head. Designed for small AUVs/ROVs |
| **EchoPilot FLS** | Forward-looking sonar | ~1 kg | 60 m ahead | ~$3000 | Designed for vessel navigation, could be repurposed |
| **Humminbird HELIX (transducer only)** | Chirp sonar | ~0.5 kg | 30–60 m | ~$200 | Consumer fish-finder transducer; cheap, proven, hackable |
| **Kraken Robotics MINSAS** | Synthetic aperture sonar | ~5 kg | High resolution, long range | $$$$ | Too heavy for this platform, but represents the state of the art |

### Deployment Method

1. **Droppable sonar buoy:** Package a Ping360 scanning sonar + battery (18650 pack, ~200 g for 2 hours) + float (foam collar) + LoRa or 900 MHz radio module + GPS. Total package: ~1.5–2.0 kg. Drop from belly bay; it splashes down, self-rights, deploys the transducer below the float, and begins scanning. Data telemetered back via LoRa (low bandwidth: position + detection alerts) or 900 MHz wideband (raw sonar imagery).

2. **Multiple lightweight buoys:** Package a simple Ping single-beam sonar + ESP32 + LoRa + battery + float. Under 500 g each. Carry 4–6 per sortie. Deploy in a grid. Each buoy listens for sub-surface contacts and reports via mesh network.

3. **Towed sonar (not recommended):** Lowering a sonar on a cable from a fixed-wing is operationally impractical — you would need to slow to near-stall, and the drag would be enormous. This approach is viable only for rotorcraft or surface vessels.

### Search Pattern

- Deploy buoys in a grid or barrier pattern.
- Spacing depends on sonar range: for a 50 m range Ping360, space buoys 70–80 m apart for overlapping coverage.
- Best suited for harbor/port security, shallow water mine detection, or monitoring a specific area (bridge piers, anchorage, pipeline route).

### Data Link

- **LoRa (868/915 MHz):** 10–15 km range, but very low bandwidth (~10 kbps). Good for detection alerts and position reports. Not enough for raw sonar imagery.
- **900 MHz wideband (Doodle Labs, Microhard):** 5–20 km, 1–10 Mbps. Can handle sonar imagery.
- **WiFi (2.4/5 GHz):** Short range (~1 km over water), but high bandwidth. Useful if a surface vessel is nearby.

### Feasibility: MODERATE

Deploying miniature sonar buoys is technically achievable. The main challenges are:
- Packaging the sonar + electronics + float into a robust, splash-proof, self-righting buoy.
- Limited sonar range (50–120 m) means many buoys are needed for meaningful coverage.
- Battery life of small buoys: 2–8 hours with 18650 packs.
- Recovery: these are likely expendable at this price point, or require a boat to retrieve.
- Best suited for shallow-water, short-range applications (harbor defense, diver detection, pipeline inspection support).

---

## 4. Water Treatment and Chemical Delivery

### 4.1 Algae Bloom Treatment

**Problem:** Harmful algal blooms (HABs) in lakes, reservoirs, and coastal waters. Common treatments include copper sulfate (CuSO4), hydrogen peroxide, and beneficial bacteria (e.g., *Bacillus* strains).

**Payload:**
- Liquid tank (1.5–3 L at ~1.0–1.3 kg/L depending on solution concentration) = 1.5–3.9 kg
- Spray system: agricultural micro-pump + nozzle array, ~200–500 g
- Total: ~2.0–4.0 kg, at the edge of the payload budget

**Mission profile:**
- Fly lawnmower pattern at 5–15 m altitude over affected water body.
- Dispense liquid treatment in calibrated spray.
- Coverage rate depends on swath width (2–5 m at low altitude) and flight speed.
- For a small lake (1 km²), multiple sorties would be needed.

**Existing operators:**
- **Rantizo** — agricultural drone spraying (primarily multirotor).
- **DJI Agras** series — multirotor chemical application. Fixed-wing is less common for spraying due to the need for slow, precise flight.
- **Leading Edge Associates** — algae treatment using drones in Florida.

**Feasibility: MODERATE.** Fixed-wing platforms are not ideal for spraying (too fast, too high). Multirotors dominate this niche because they can hover and fly slowly. A fixed-wing could work for dispersant delivery over large areas where precision is less critical.

### 4.2 Oil Spill Dispersant Application

**Concept:** Spray chemical dispersant (e.g., Corexit, Finasol) over oil slicks to break them into smaller droplets that biodegrade faster.

**Payload:** Same as above — liquid tank + spray system, 2–4 kg.

**Advantage of fixed-wing:** Oil slicks can cover large areas. A fixed-wing's speed and endurance are actually beneficial here compared to multirotors. You can cover a long, thin slick quickly.

**Limitation:** 2–4 kg of dispersant is a tiny amount. A meaningful oil spill response requires thousands of liters. A mini-UAV would be useful for targeted application on small, isolated slicks or for initial rapid response before larger assets arrive.

**Reference:** The US Coast Guard and NOAA have tested drone-based dispersant spraying. Textron's Aerosonde has been proposed for this role.

**Feasibility: LOW to MODERATE.** Useful for small-scale or rapid-response situations. Not a substitute for C-130 Hercules aerial spraying on major spills.

### 4.3 Water Quality Sampling

**Concept:** Drop sensor pods into water bodies, let them collect data (pH, dissolved oxygen, turbidity, temperature, conductivity, chlorophyll), then retrieve later.

**Payload:**
- Sensor pod: water quality sonde (e.g., YSI EXO2, In-Situ Aqua TROLL) or custom package = 0.5–2.0 kg per pod
- Carry 2–4 pods per sortie
- Drop via servo-actuated release mechanism

**Mission profile:** Fly to predetermined GPS coordinates over a lake/reservoir, release pods at each location, pods float and log data or transmit via LoRa/cellular. Retrieve by boat later, or make them expendable with cellular uplink.

**Reference:** **Winfield Solutions** and **Cana** have developed drone-deployed water samplers. **FluidLytix** and **WaterBit** offer IoT water monitoring sensors suitable for aerial deployment.

**Feasibility: HIGH.** This is straightforward — you are essentially dropping small packages at GPS coordinates, which is trivially achievable with ArduPilot's DO_GRIPPER or servo release commands.

### 4.4 Invasive Species Treatment

**Application:** Treating lakes for invasive mussels (zebra/quagga), aquatic weeds (hydrilla, Eurasian milfoil), or invasive fish.

**Method:** Same as algae treatment — chemical dispensing via spray or drop.

**Feasibility: MODERATE.** Same constraints as algae treatment. Fixed-wing is workable for broad-area application.

### Regulatory Requirements

- **USA:** EPA regulates pesticide/chemical application over water under FIFRA (Federal Insecticide, Fungicide, and Rodenticide Act). Need NPDES permit under Clean Water Act for any discharge to navigable waters. FAA Part 107 waiver needed for beyond-visual-line-of-sight (BVLOS). Agricultural exemption under Part 137 may apply.
- **EU:** REACH regulations for chemical substances. National aviation authority approval for BVLOS drone operations.
- **Key point:** The chemical application itself is typically more heavily regulated than the drone flight. You need a licensed applicator (often requiring a commercial pesticide applicator license) and environmental impact assessment.

---

## 5. Marine Wildlife Monitoring

### 5.1 Whale and Dolphin Surveys

**Concept:** Replace manned survey aircraft (historically the standard) with UAVs for cetacean population counts, behavioral studies, and photo-ID.

**Payload:**
- High-resolution camera (Sony A7R or similar mirrorless, ~650 g + gimbal) for photo-ID
- Thermal camera (FLIR Boson 640) for detecting whale blows at distance, ~50 g
- Total: ~1.0–1.5 kg

**Mission profile:**
- Systematic transect survey (line-transect distance sampling methodology).
- Altitude: 200–500 m to avoid disturbance (most permit conditions require minimum altitude).
- Speed: 60–100 km/h, similar to manned survey aircraft.
- A fixed-wing platform is ideal — it covers large areas efficiently and is less disturbing to wildlife than hovering multirotors.

**Data processing:** Images analyzed post-flight or with onboard AI (Jetson-based species detection models exist, e.g., from NOAA's VIAME project).

**Reference:**
- **NOAA** uses ScanEagle-class UAVs for marine mammal surveys.
- **Duke University Marine Lab** operates fixed-wing drones for cetacean surveys.
- **Murdoch University (Australia)** pioneered drone-based whale population monitoring.

**Feasibility: HIGH.** This is a proven application. Fixed-wing UAVs are arguably the best platform for large-area wildlife surveys.

### 5.2 Coral Reef Health Assessment

**Payload:**
- Multispectral camera (MicaSense RedEdge-P, ~170 g) for coral bleaching detection
- RGB camera for photogrammetric mapping
- Total: ~0.5–1.0 kg

**Mission profile:** Fly grid pattern at 50–120 m altitude over reef. Generate orthomosaic maps. Spectral analysis identifies bleached vs. healthy coral.

**Limitation:** Water column absorption limits optical depth to ~10 m in clear water. Only shallow reefs are visible.

**Feasibility: HIGH** for shallow reefs. The platform is well-suited.

### 5.3 Biopsy Sampling

**Reference: Ocean Alliance SnotBot** — a multirotor drone that flies through a whale's blow (exhalation plume) to collect mucus samples containing DNA, hormones, and microbiome data.

**Feasibility for fixed-wing: VERY LOW.** SnotBot requires hovering at low altitude directly above a whale and precisely timing passage through the blow. A fixed-wing cannot hover. This application is exclusively for multirotors.

### 5.4 Floating Sensor Network Deployment

**Concept:** Deploy small floating sensor packages (GPS + temperature + salinity + accelerometer + satellite or LoRa uplink) to track ocean currents, monitor marine protected areas, or create virtual fences.

**Payload:** 200–500 g per sensor pod × 4–8 pods = 1.0–4.0 kg.

**Reference:** Pacific Gyre "SPOT" drifters, Sofar Ocean "Spotter" buoys (though these are larger). Custom lightweight drifters can be built for ~$100–200 each using ESP32 + GPS + LoRa + solar cell + waterproof housing.

**Feasibility: HIGH.** Simple drop deployment. Fixed-wing covers large area efficiently.

---

## 6. Search and Rescue at Sea

### Detection Payload

| Component | Weight | Function |
|---|---|---|
| Thermal camera (FLIR Boson 640 or DJI Zenmuse H20N) | 50–350 g | Detect body heat of person in water. Effective range: 500–1000 m altitude |
| Visible camera (4K, stabilized) | 300–600 g | Visual confirmation and identification |
| AI detection software (onboard Jetson) | 150 g | Real-time person-in-water detection. Models available from USCG research |
| AIS/PLB receiver | 50–100 g | Detect personal locator beacons (406 MHz or AIS SART) |
| **Total** | **~0.5–1.2 kg** | Leaves significant margin for other payloads |

### Emergency Supply Drop

With remaining payload capacity (2.5–3.5 kg after sensors), the UAV could carry and drop:

| Item | Weight | Notes |
|---|---|---|
| Inflatable life jacket (manual) | ~0.5 kg | Compact when packed |
| Personal locator beacon (PLB) | ~0.2 kg | ACR ResQLink or similar |
| Waterproof VHF radio | ~0.3 kg | Standard marine handheld |
| Chemical light sticks (×4) | ~0.2 kg | Visibility at night |
| Survival blanket | ~0.1 kg | Space blanket type |
| **Total supply package** | **~1.3 kg** | Easily within budget |

A servo-released drop container with a small drogue chute for accuracy is straightforward to implement.

### Mission Profile

1. **Alert:** Coast guard receives distress call with approximate position.
2. **Launch:** UAV launched from shore station, vessel, or vehicle within 5 minutes.
3. **Transit:** Fly to search area at max speed (100–140 km/h).
4. **Search:** Fly expanding square or sector search pattern. ArduPilot supports DO_SET_CAM_TRIGG_DIST for systematic photo coverage.
5. **Detect:** Thermal/AI identifies person in water.
6. **Mark:** Transmit GPS coordinates to rescue coordination center.
7. **Drop:** Release supply package near survivor.
8. **Orbit:** Remain on station, guiding rescue vessel via real-time video downlink.

### Reference

- **USCG** has tested Puma AE and ScanEagle for maritime SAR.
- **ICARUS project (EU)** developed UAV-based SAR systems.
- **Australian Maritime Safety Authority** operates fixed-wing drones for coastal SAR.
- **Helper Drone (France)** — drops life preservers to drowning swimmers (multirotor, but the concept transfers).

### Feasibility: HIGH

This is one of the strongest use cases for the platform. A fixed-wing UAV can cover vastly more search area per hour than a multirotor, and the payload requirements are modest. The main gap is: the UAV cannot physically recover the survivor, so it is a force multiplier for crewed rescue assets, not a replacement.

---

## 7. Overwater Flight Challenges

### 7.1 Navigation

**Problem:** Over open water, there are no terrain features for visual odometry or optical flow. The horizon is featureless.

**Mitigations:**
- **GPS is the primary nav source** and is generally reliable over water (no multipath from buildings or terrain). Dual-GPS (e.g., Here3 + Here4) provides redundancy.
- **ArduPilot EKF3** fuses GPS, IMU, magnetometer, and barometer. Over water, barometric altitude is reliable (no terrain-induced pressure variations), but sea-level pressure changes with weather — ensure QNH is updated.
- **Magnetometer interference** is lower over water (no ferrous structures), but compass calibration should account for the vehicle's own interference.
- **Radar altimeter** (e.g., Ainstein US-D1, 48 g) provides reliable AGL altitude over water, unlike barometric altitude.
- **No ADSB terrain following** needed, but maintain safe altitude to avoid ship masts and offshore structures.

**ArduPilot parameters of note:**
- `TERRAIN_ENABLE = 0` (no terrain data over open ocean)
- `GPS_TYPE` and `GPS_TYPE2` for dual GPS
- `RNGFND_TYPE` for radar altimeter integration

### 7.2 Salt Spray and Corrosion

**Threats:** Salt air corrodes electronics, connectors, and metal fasteners. Salt deposits on propeller reduce efficiency. Salt on pitot tube causes airspeed errors.

**Mitigations:**
- **Conformal coating** (e.g., MG Chemicals 419D silicone conformal coat) on all PCBs — flight controller, ESC, GPS, radio.
- **Stainless steel or titanium fasteners** instead of plain steel.
- **Marine-grade connectors** (gold-plated, sealed) or liberally applied dielectric grease on all connectors.
- **Pitot tube cover** deployed when not in flight; consider heated pitot to prevent salt/moisture buildup.
- **Post-flight wash** with fresh water after every maritime sortie — this is standard practice for naval aircraft of all sizes.
- **Carbon fiber or fiberglass airframe** — inherently corrosion-resistant. Avoid aluminum structural components or treat with ACF-50 anti-corrosion fluid.

### 7.3 Waterproofing

**Levels of protection:**
- **IP54 minimum** for electronics bays (splash/spray protection).
- **IP67 for critical components** if the aircraft might ditch.
- **Methods:** Sealed electronics bays with gaskets, conformal coating on boards, drain holes (counterintuitively — let water OUT rather than trying to keep it completely sealed), silicone sealing of cable penetrations.
- **Motor/ESC:** Brushless motors are inherently somewhat water-resistant. Use marine-rated ESCs or conformal-coat standard ones.

### 7.4 Engine Failure and Recovery

**The fundamental problem:** If the electric motor fails over water with no landing options, the aircraft will ditch. For an expendable surveillance platform, this may be acceptable. For an expensive sensor package, you need mitigation.

**Options:**

| Recovery Method | Weight | Pros | Cons |
|---|---|---|---|
| **Parachute (ballistic)** | 300–500 g | Proven technology (MARS parachute systems). ArduPilot supports parachute deployment (`CHUTE_ENABLED`). Slows descent to ~5 m/s | Aircraft still lands in water. Payload must be waterproof or you lose it |
| **Inflatable floats** | 200–400 g | Keep airframe on surface for boat recovery. CO2 cartridge inflation | Adds complexity. Must deploy reliably. Works only in calm seas |
| **Parachute + float combo** | 500–800 g | Best of both: slow descent + stays on surface | Weight penalty eats into payload budget |
| **Waterproof airframe** | 0 g (design choice) | Inherently floatable if airframe is sealed foam/composite with positive buoyancy | Doesn't protect electronics from immersion unless fully sealed |
| **Transponder/locator beacon** | 50–100 g | Doesn't prevent ditching but enables recovery. GPS position transmitted on splash-down | Need a boat to go retrieve it |

**ArduPilot water-relevant parameters:**
- `CHUTE_ENABLED = 1` — enables parachute release
- `CHUTE_ALT_MIN` — minimum altitude for parachute deployment
- `CHUTE_CRT_SINK` — critical sink rate to trigger auto-deploy
- `FS_SHORT_ACTN` and `FS_LONG_ACTN` — failsafe actions (can be set to deploy chute or spiral down)
- `BATT_FS_CRT_ACT` — critical battery failsafe action
- Custom Lua script can monitor motor RPM (if using telemetry ESC) and deploy chute if motor stops unexpectedly

**Recommendation:** For maritime operations, design the airframe with positive buoyancy (closed-cell foam core, sealed compartments) and carry a 50 g GPS locator beacon (e.g., Spot Trace, $100). Accept that ditching will happen eventually and plan for recovery rather than trying to prevent water contact.

### 7.5 Additional Overwater Considerations

**Weather:**
- Overwater weather changes rapidly. Wind over open water is typically stronger and more consistent than overland.
- ArduPilot's wind estimation (via EKF groundspeed vs. airspeed) works well over water.
- Set conservative wind limits: if headwind exceeds 50% of cruise airspeed, abort and return.

**Communications:**
- Radio line-of-sight over water is excellent (no terrain blockage), but range is limited by Earth curvature: ~40 km at 100 m altitude, ~65 km at 300 m altitude.
- For longer range: use a relay on a ship, cellular (if near coast with coverage), or satellite (Iridium SBD for telemetry, ~200 g).

**Regulatory:**
- Overwater BVLOS operations require specific waivers in most jurisdictions.
- Maritime airspace is generally less restricted than overland, but coordination with maritime authorities (coast guard, port authority) is essential.
- ICAO and national regulations on unmanned aircraft over international waters are still evolving.

---

## Summary Feasibility Matrix

| Application | Payload Fit | Mission Fit | Technical Readiness | Overall Feasibility |
|---|---|---|---|---|
| **Maritime Patrol / Surveillance** | Excellent | Excellent | High (proven) | **HIGH** |
| **ASW — Standard Sonobuoys** | Over weight | Poor (single buoy useless) | Low | **LOW** |
| **ASW — Miniature Acoustic Buoys** | Good (2–3 per sortie) | Moderate (niche) | Medium (R&D needed) | **MODERATE** |
| **Miniature Sonar Buoy Deployment** | Good | Moderate (short range) | Medium | **MODERATE** |
| **Water Treatment / Spraying** | Marginal (2–4 L capacity) | Poor (fixed-wing too fast) | Medium | **LOW-MODERATE** |
| **Water Quality Sampling** | Excellent (multiple pods) | Good | High (simple drop) | **HIGH** |
| **Oil Spill Dispersant** | Marginal (small volume) | Moderate (good for small slicks) | Medium | **LOW-MODERATE** |
| **Whale/Dolphin Surveys** | Excellent | Excellent | High (proven) | **HIGH** |
| **Coral Reef Mapping** | Excellent | Good (shallow only) | High | **HIGH** |
| **Biopsy Sampling** | N/A | Impossible (needs hover) | N/A | **NOT FEASIBLE** |
| **Floating Sensor Deployment** | Excellent | Excellent | High | **HIGH** |
| **SAR Detection** | Excellent | Excellent | High | **HIGH** |
| **SAR Supply Drop** | Good | Good | Medium (needs testing) | **HIGH** |

---

## Top 5 Recommended Applications (in priority order)

1. **Maritime surveillance / coastal patrol** — Proven, high demand, well-suited to fixed-wing. Start here.
2. **Search and rescue detection** — High social value, modest payload, strong platform fit.
3. **Marine wildlife surveys** — Growing market, well-funded research customers, perfect for fixed-wing transects.
4. **Water quality sensor deployment** — Simple mechanically, clear commercial need, easy to demonstrate.
5. **Floating sensor network deployment** — Emerging market in ocean monitoring, IoT integration, good fit for fixed-wing range.

---

*Note: All weights and specifications are approximate and should be verified against current manufacturer datasheets. Payload integration always requires flight testing to confirm CG, aerodynamic impact, and power budget.*
