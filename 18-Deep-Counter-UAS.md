# Counter-UAS Systems for Mini Fixed-Wing UAV Platforms: Engineering Research

## Platform Reference Specifications

- **Wingspan:** 2–4 m (typical examples: Penguin C, ScanEagle-class, or custom composite airframe)
- **MTOW:** ~15–25 kg (airframe 8–12 kg, fuel/battery 3–6 kg, payload 4 kg)
- **Payload volume:** roughly 2–4 liters in a fuselage bay or underwing pod
- **Electrical power available:** 30–80 W continuous from a dedicated BEC/generator tap; burst up to 150 W from a secondary battery
- **Endurance:** 2–6 hours (gas/hybrid), 45–90 min (electric)
- **Cruise speed:** 18–30 m/s (65–108 km/h)
- **Autopilot:** ArduPilot (Plane firmware) on Cube Orange+ or similar, with MAVLink telemetry
- **Companion computer:** Raspberry Pi 5, Jetson Orin Nano, or Radxa Rock 5B — all under 100 g, 15–25 W

---

## 1. Detection Methods Deployable from a Drone

### 1.1 RF Detection / Direction Finding

**Principle:** Hostile drones maintain a control link (typically 2.4 GHz, 5.8 GHz, or 900 MHz) and often a video downlink. An airborne RF sensor scans these bands for characteristic signals — frequency-hopping patterns, known protocol signatures (DJI OcuSync, Crossfire, ExpressLRS, etc.), or raw energy above a noise floor.

**Specific Hardware:**

| System / Component | Weight | Power | Notes |
|---|---|---|---|
| CRFS RFeye Node 40-8 | ~1.2 kg | 15 W | 9 kHz–8 GHz, real-time spectrum monitoring, designed for integration |
| Ettus USRP B205mini-i | 28 g (board only) | 5 W | 70 MHz–6 GHz, 56 MHz bandwidth, requires companion computer for DSP |
| RTL-SDR v4 + LNA | 15 g total | 0.5 W | 24 MHz–1.766 GHz, extremely cheap but limited bandwidth and dynamic range |
| KerberosSDR (4-channel coherent) | 120 g | 3 W | Direction finding via phase interferometry across 4 RTL-SDR tuners |
| Custom: HackRF One + 4-element patch array | ~200 g total | 2.5 W | 1 MHz–6 GHz, can do crude DF with MUSIC/ESPRIT algorithms on companion computer |

**Detection Range:** Highly dependent on the target's transmit power and the antenna gain. A DJI controller at 26 dBm (400 mW) EIRP on 2.4 GHz is detectable at:
- Omnidirectional whip on the interceptor: 1–3 km (signal above noise floor, SNR >10 dB)
- Small directional antenna (8 dBi patch): 3–8 km
- For direction finding with phase interferometry (KerberosSDR-style 4-channel): angular accuracy of ~5–15 degrees at 1 km, degrading with range. Baseline separation on a 3 m wingspan gives roughly λ/2 spacing at 2.4 GHz (6.25 cm), which is tight — you want elements at wingtips for maximum baseline (~3 m = 24λ), giving sub-degree DF accuracy in theory, but vibration and airframe flexing degrade this to ~2–5 degrees practically.

**False Positive Rate:** In an urban RF environment, raw energy detection is nearly useless (massive false positives from WiFi, Bluetooth, etc.). Protocol-aware detection — identifying DJI OcuSync headers, ELRS FHSS patterns, or MAVLink heartbeats — dramatically reduces false positives to <1% in testing. Libraries like DroneID decoders (DJI broadcasts RemoteID-like frames) make this practical. In a rural/battlefield environment, false positive rates drop further.

**Integration Notes:**
- Antenna placement is critical: mount DF elements on wingtips or in a ventral array with known phase centers
- Airframe carbon fiber is RF-opaque — fiberglass or Kevlar radomes needed over antenna locations
- The companion computer runs GNU Radio or custom SDR pipeline; latency for detection is ~50–200 ms per sweep
- Weight budget: realistically 150–400 g for a useful RF detection payload including antennas
- Power budget: 3–8 W continuous

**Assessment:** RF detection is the lightest, lowest-power detection method and is **highly feasible** at this scale. It is the recommended primary detection layer. Limitation: it cannot detect drones operating autonomously with no active RF link (pre-programmed GPS waypoint missions with radio silence).

---

### 1.2 Compact FMCW Radar

**Principle:** Frequency-Modulated Continuous Wave radar transmits a chirp and measures the beat frequency of returns to determine range. Modern mmWave radar-on-chip devices operate at 60–77 GHz and can detect micro-Doppler signatures from spinning propellers, which is a strong discriminator for drones vs. birds.

**Specific Hardware:**

| System | Frequency | Weight | Power | Max Detection Range (0.01 m² RCS) |
|---|---|---|---|---|
| TI IWR6843AOP (antenna-on-package) | 60–64 GHz | 8 g (board) | 2.5 W | ~50–80 m |
| TI AWR2944 (77 GHz, 4TX/4RX) | 76–81 GHz | ~15 g (module) | 4 W | ~150–200 m |
| Ainstein USD-19 | 24 GHz | 55 g | 2 W | ~200 m (for small drones) |
| Ainstein USD-26 | 77 GHz | 42 g | 3 W | ~150 m |
| Echodyne EchoGuard (phased array) | X-band (9.4 GHz) | 1.8 kg | 35 W | ~3 km for small drones |
| Robin Radar Elvira | X-band | 12 kg | 100 W | ~5 km | Not airborne feasible |

**Critical Analysis — Can compact radar detect a small drone at useful range?**

The radar range equation governs this:

R_max = [ (P_t × G² × λ² × σ) / ((4π)³ × k × T × B × SNR_min × F × L) ]^(1/4)

For a small drone target (RCS σ ≈ 0.01 m² = −20 dBsm):

- **TI IWR6843AOP:** P_t = 12 dBm, G = 10 dBi (on-package antennas), λ = 5 mm, B = 4 GHz bandwidth. Calculated max range for SNR = 13 dB: approximately **40–80 m** depending on integration time. This is essentially useless for early warning but potentially useful for terminal guidance in the final approach phase.

- **TI AWR2944 with external antenna array (20 dBi horn/lens):** Range extends to ~300–500 m. Board + antenna + radome: ~100 g, 6 W. This becomes marginally useful for detection but requires mechanical or electronic scanning to cover a useful field of regard.

- **Ainstein USD-19/26:** Purpose-built for UAV detect-and-avoid. Specified at ~200 m for cooperative targets; for a 0.01 m² RCS non-cooperative target, realistic range is 80–150 m. Weight and power are very feasible.

- **Echodyne EchoGuard:** The only radar in this list with genuinely useful counter-UAS range (3+ km for small drones), but at 1.8 kg and 35 W, it consumes nearly half the payload capacity and a huge fraction of available power. Marginally feasible on a 4 kg payload platform but leaves almost nothing for other systems.

**Micro-Doppler Advantage:** The key value of radar from an airborne platform is micro-Doppler classification. Spinning propellers create distinctive spectral signatures at blade-pass frequencies (typically 200–800 Hz for multirotor props). TI's radar toolbox includes embedded micro-Doppler classifiers that can distinguish drones from birds with >90% accuracy at ranges where SNR is adequate.

**Airborne Challenges:**
- Platform vibration creates clutter returns and phase noise — need vibration isolation (Sorbothane mounts, ~20 g)
- Ground clutter from look-down geometry is severe; need either pulse-Doppler processing (complex for FMCW) or careful antenna beamforming to avoid ground returns
- The interceptor's own ground speed (20–30 m/s) creates a large Doppler offset that must be compensated using INS/GPS data
- Atmospheric attenuation at 60/77 GHz is ~0.5–1 dB/km in clear air, ~5–10 dB/km in moderate rain — limited in bad weather

**Assessment:** Compact mmWave radar is **feasible but of limited utility** for early detection (ranges too short). It becomes valuable as a **terminal sensor** for the final 100–500 m of intercept, providing precise range, range-rate, and angle data for guidance. The TI AWR2944 with a small external antenna or an Ainstein module is the sweet spot: 50–100 g, 3–6 W, and provides terminal-phase tracking data. For long-range detection, radar at this scale class is insufficient — you need ground-based radar cueing.

---

### 1.3 Acoustic Detection

**Principle:** Multirotor drones produce distinctive acoustic signatures from propeller blade-passing frequencies and their harmonics (typically fundamental at 100–400 Hz, harmonics up to several kHz). A microphone array can detect and localize these sounds.

**Hardware:**
- MEMS microphone arrays: 4–8 × InvenSense ICS-43434 or Knowles SPH0645, each <0.1 g, on a small PCB
- Array geometry: distributed across the airframe (wingtips + nose + tail gives ~3 m baseline)
- Weight: 20–50 g for the array + ADC + processing
- Power: 1–3 W

**Fundamental Problem — Self-Noise:**
This is the showstopper. A fixed-wing UAV in flight generates massive aerodynamic noise (boundary layer turbulence over the microphones, propeller noise from the interceptor's own motor/engine, wind noise). Typical self-noise levels:
- Fixed-wing UAV at cruise: 85–100 dB SPL at the airframe surface
- Target drone at 100 m: ~50–60 dB SPL (a typical DJI Mavic 3 is ~75 dB at 1 m, falling at 6 dB per distance doubling)

The target signal is **buried 30–40 dB below self-noise**. Even with:
- Aerodynamic microphone fairings (reduce wind noise by 10–15 dB)
- Beamforming with an 8-element array (gain ~9 dB)
- Spectral subtraction of known self-noise profile (~5–10 dB improvement)

You still have negative SNR at any useful range. Ground-based acoustic detection systems (like Squarehead DISCOVAIR) work because they are stationary with minimal self-noise, achieving 500 m–1 km detection. Airborne acoustic detection has been demonstrated only from hovering multirotor platforms in very controlled conditions.

**Assessment:** Acoustic detection from a fixed-wing platform is **not feasible** with current technology. The self-noise problem is fundamental. This approach is only viable for ground-based or stationary hover-platform deployment.

---

### 1.4 Visual / IR Detection with AI

**Principle:** Use a gimballed or fixed camera (visible or thermal IR) with onboard neural network inference to detect and track drones in the visual field.

**Hardware Options:**

| Camera | Type | Weight | Resolution | FoV | Notes |
|---|---|---|---|---|---|
| Sony Alpha 7C (stripped) | Visible, full-frame | ~350 g | 24 MP | Lens-dependent | Overkill, too heavy |
| Arducam IMX477 (RPi HQ Cam) | Visible, 1/2.3" | 45 g | 12 MP | 70° with 6mm lens | Good balance, cheap |
| FLIR Boson 640 | LWIR thermal | 30 g | 640×512 | 24°–95° | Detects motor/battery heat |
| FLIR Lepton 3.5 | LWIR thermal | 1 g | 160×120 | 57° | Too low resolution for drone detection at range |
| DJI Zenmuse H20N (not standalone) | Multi-sensor | 800 g | Visible + thermal + laser rangefinder | Various | Too heavy, proprietary |
| See3CAM_CU135 (e-con Systems) | Visible, 1/3.2" | 25 g | 13 MP | USB3 | Good for integration |

**Detection Range Analysis:**

For a small drone (0.3 m across) to be detectable, it needs to subtend at least ~10 pixels in the image (for a CNN detector like YOLOv8-nano):

- 12 MP camera (4000×3000), 70° FoV: angular resolution = 0.0175°/pixel = 0.3 mrad/pixel
- 10 pixels = 3 mrad subtended angle
- Range for 0.3 m target at 3 mrad: R = 0.3/0.003 = **100 m**

To detect at 500 m, you need the target to subtend 0.6 mrad, which with a 0.3 m drone requires angular resolution of 0.06 mrad/pixel. This implies a narrow FoV telephoto setup:
- 12 MP sensor with a 200 mm lens: FoV ~6° × 4°, 0.015 mrad/pixel → drone detectable at **~500–800 m** but with a tiny search area

**This creates a search-vs-resolution tradeoff.** Solutions:
1. **Two-camera system:** Wide-angle (70°) for search + narrow telephoto (6°) for identification/tracking. Weight: ~120 g. This is the standard approach.
2. **Gimballed camera:** Scan the telephoto camera across the search area. Weight: 200–400 g with a small gimbal (e.g., SimpleBGC-based 2-axis). Slow scan rate limits effectiveness.
3. **AI detection on wide-angle, then crop-and-zoom in software:** Works if target is detectable at all in the wide image (limited to ~100–200 m).

**Onboard AI Processing:**
- YOLOv8-nano on Jetson Orin Nano: ~200 FPS at 640×640 input, 1.5 W incremental power
- Custom drone-detection model trained on UAV-vs-bird datasets (e.g., Anti-UAV Challenge dataset, DroneVsBird dataset): achievable mAP ~0.75–0.85 at 100 m ranges
- Thermal detection is more robust (drones have hot motors and batteries that stand out against sky background), works at night, less affected by clouds/contrast. FLIR Boson 640 with a 50 mm lens can detect a drone's thermal signature at 300–500 m.

**Thermal IR Advantage:**
Against a cold sky background, a drone's motor heat (50–80°C above ambient) creates 5–15°C apparent temperature difference at the sensor. FLIR Boson 640 NETD is <40 mK, so even at ranges where the drone subtends only a few pixels, the thermal contrast makes detection possible. This is particularly effective at night and in low-visibility conditions.

**Assessment:** Visual/IR detection is **feasible and recommended** as a secondary detection layer. The optimal configuration is:
- FLIR Boson 640 (thermal, 30 g, 1 W) for primary detection — robust day/night
- Arducam IMX477 with 16 mm lens (visible, 45 g, 2 W) for identification and fine tracking
- Both processed on Jetson Orin Nano (60 g, 15 W)
- Total: ~135 g, 18 W
- Effective detection range: 200–500 m (thermal), 100–300 m (visible, conditions-dependent)
- False positive rate: <5% with a well-trained model in open airspace; higher in urban environments with birds

---

## 2. Kinetic Interception

### 2.1 Reference Systems

**Anduril Roadrunner:** A vertically-launched autonomous interceptor, roughly 1.8 m long, jet-powered, capable of high-speed intercept. It is designed to loiter and then dash to intercept. It is a purpose-built system in the 10–20 kg class — significantly larger and more capable than our platform. Key lesson: it uses a combination of radar cueing from ground systems and onboard electro-optical terminal guidance.

**Fortem DroneHunter F700:** A large multirotor (~25 kg) that carries a tethered net launcher. It uses its own radar (TrueView R20, a proprietary X-band) for autonomous tracking and fires a net at ranges of 15–40 m. Intercept speed is limited (~15 m/s) because it's a multirotor. Key lesson: net capture works but requires close approach and relatively slow closure rates.

**DRONECATCHER (Delft Dynamics):** A multirotor that fires a net-carrying projectile (compressed gas launcher) at ranges up to 20 m. Net deploys and tangles target propellers. Has been operationally deployed.

**Common theme:** All existing airborne intercept systems use multirotor platforms, not fixed-wing, because of the maneuverability requirements for close-approach engagement. This is a critical consideration.

### 2.2 Net-Based Capture

**Trailing Net:**
- Concept: Fixed-wing tows a net (2–3 m across) on a 10–20 m line and flies through the target drone
- Weight: net + line + deployment mechanism = 200–500 g
- Aerodynamic drag of a deployed trailing net at 25 m/s: substantial, roughly 5–15 N depending on net size and mesh, which translates to ~10–30% cruise power increase
- Targeting accuracy required: need to pass within ±1.5 m of target → very challenging at 25 m/s closing speed against a maneuvering target
- Risk: net tangles in own propeller or control surfaces

**Launched Net:**
- Concept: Compressed gas or spring-loaded net launcher fires forward or downward at the target from 10–20 m range
- Weight: launcher mechanism 300–600 g, net + projectile 100–200 g per shot, gas cartridge 50–100 g
- Single-shot system (no reload in flight) unless carrying multiple launchers
- Launch velocity needed: ~15–30 m/s to reach target at 10–20 m range
- Net must deploy to 2–3 m diameter in flight — requires weighted corners (bolas-style) or deployment vanes
- Total system weight: 500–1000 g for a single-shot system — feasible within 4 kg payload
- **Key problem:** timing. At 25 m/s closing speed, the engagement window at 15 m range is 0.6 seconds. The fire decision, motor actuation, and net flight time must all fit in this window. Requires very precise terminal guidance data.

**Tangle Devices (Streamers/Filaments):**
- Concept: Release Kevlar streamers or monofilament lines designed to tangle in target propellers
- Weight: 10–50 g per device, can carry many
- Deployment: released from a dispenser as the interceptor passes near the target
- Effective radius: very small (must contact propellers directly)
- Probability of kill per pass: very low (<10%)
- Assessment: novelty with low effectiveness

### 2.3 Direct Collision (Kamikaze Intercept)

**Concept:** The interceptor dives into the target drone at high speed, destroying both.

**Physics:**
- Interceptor mass: ~15 kg at intercept. Target mass: 1–5 kg (typical commercial drone).
- At 30 m/s closing speed, kinetic energy = 0.5 × 15 × 30² = 6,750 J — more than sufficient to destroy a small multirotor
- Even a glancing blow that damages one arm or motor will destabilize a quadcopter
- Hit probability: at 30 m/s closing speed, the interceptor needs to be within ~0.5 m of the target center. With a 3 m wingspan, the effective cross-section for a wing strike is much larger — need to pass within ±1.5 m laterally.

**This is the most feasible kinetic approach for a fixed-wing platform.** Cost per interceptor is low if using a simple airframe. The interceptor becomes an expendable munition.

### 2.4 Fixed-Wing vs. Multirotor: Intercept Feasibility

**Speed advantage — fixed-wing:** Cruise 25 m/s, dash 35–45 m/s (can dive at 50+ m/s). Typical commercial multirotor: max speed 15–20 m/s. The fixed-wing has a significant speed advantage and will catch the target.

**Maneuverability disadvantage — fixed-wing:**
- Minimum turn radius at 25 m/s and 45° bank: R = v²/(g × tan(45°)) = 625/9.81 ≈ **64 m**
- At 60° bank: R ≈ 37 m
- A multirotor target can change direction nearly instantaneously (decelerate at 5–8 m/s², turn, accelerate in new direction)
- If the target executes a hard turn when the interceptor is 100 m away (4 seconds at 25 m/s closing), the interceptor arrives at the target's previous position and must execute a turn-around, losing 200–400 m of distance

**Intercept Geometry:**
The solution is **proportional navigation (PN)**, not pure pursuit:
- In pure pursuit, the interceptor always points at the target — this leads to tail-chase curves with very long intercept times against a maneuvering target
- In PN, the interceptor steers to keep the line-of-sight (LOS) rotation rate at zero (or a commanded value): heading change rate = N × LOS rate, where N (navigation constant) is typically 3–5
- PN is optimal against non-maneuvering targets and near-optimal against moderately maneuvering ones
- For a fixed-wing with a 2:1 speed advantage over the target, PN produces intercept in most geometries within 1–2 turns

**Augmented Proportional Navigation (APN):** Adds a term proportional to estimated target acceleration. Required against maneuvering targets. The guidance law becomes:

a_commanded = N × V_c × LOS_rate + (N × N_t) / 2

where V_c is closing velocity and N_t is estimated target acceleration normal to LOS.

**Terminal Guidance Sequence:**
1. Initial cueing: RF direction finding gives bearing to target (±5°)
2. Approach phase: thermal/visual camera acquires target, provides LOS angles at 10 Hz
3. Mid-course: PN guidance steers interceptor, radar (if fitted) provides range/range-rate
4. Terminal (final 200 m): high-update-rate visual tracking (30+ Hz) with APN guidance
5. Final 50 m: open-loop or bang-bang control to impact point

**Required Guidance Hardware:**
- IMU: already in ArduPilot's flight controller (ICM-42688-P or similar), 200+ Hz update rate
- Target tracker: visual/IR camera + Jetson Orin Nano running tracker (KCF, CSRT, or learned tracker) at 30 FPS
- Range measurement: without radar, use image-based size estimation (if target type is known) or triangulation during approach
- Guidance law runs on companion computer, sends roll/pitch commands to ArduPilot via MAVLink COMMAND_LONG or SET_ATTITUDE_TARGET

**Assessment:** A fixed-wing can intercept a multirotor in most scenarios, but **requires multiple passes** if the target maneuvers aggressively. Kamikaze intercept is the highest-probability kinetic method. Net capture from a fixed-wing is very challenging due to the high closure rates and limited engagement window. The recommended kinetic approach is expendable interceptor with PN guidance, treating the airframe as a munition.

---

## 3. Electronic Warfare / Jamming

### 3.1 GPS Spoofing and Denial

**Principle:** Transmit fake GPS signals that cause the target drone's GPS receiver to report an incorrect position. The target either drifts off course, enters failsafe (RTH to wrong location), or loses position hold and becomes uncontrollable.

**Implementation:**
- Requires a software-defined radio capable of transmitting GPS L1 (1575.42 MHz): HackRF One (1 W output) or LimeSDR Mini (10 mW output, needs amplifier)
- GPS signal simulator software: GPS-SDR-SIM (open source) generates fake GPS baseband signals
- Effective spoofing requires overpowering the real GPS signal by ~3–10 dB at the target
- Real GPS signal at ground level: approximately −130 dBm
- With 1 W EIRP from a directional antenna at 100 m range, received power at target: approximately −50 dBm — overwhelmingly stronger than real GPS
- Weight: HackRF + amplifier + antenna + companion computer = 200–400 g
- Power: 5–15 W (mostly the RF amplifier)

**Legal Framework:**
- **HIGHLY ILLEGAL** in virtually all jurisdictions without explicit military/government authorization
- UK: Wireless Telegraphy Act 2006, Section 68 — imprisonment up to 2 years for intentional interference with any wireless telegraphy. The Ofcom enforcement regime is strict.
- US: 47 USC § 333 — interference with licensed radio communications. GPS spoofing additionally violates 18 USC § 32 (destruction of aircraft).
- NATO countries: generally prohibited except by authorized military units under specific ROE
- Even military use requires careful coordination to avoid affecting friendly forces' GPS

**Countermeasures the target may employ:**
- Multi-constellation GNSS (GPS + GLONASS + Galileo + BeiDou) makes single-constellation spoofing less effective
- IMU-based dead reckoning during GPS anomalies (DJI drones do this)
- Anti-spoofing via signal authentication (Galileo OSNMA, GPS III)
- Frequency diversity and spatial filtering (military receivers)

**Assessment:** Technically feasible at this scale (lightweight, low power), but **legally prohibited** in almost all non-military contexts. For military applications, it's a viable lightweight effector but requires careful coordination.

---

### 3.2 RF Control Link Jamming

**Principle:** Overpower the drone-to-controller communication link, causing loss of control signal. Most drones will then enter a failsafe mode (typically hover, descend, or RTH).

**Target Frequencies:**
| Band | Typical Use | Bandwidth | Notes |
|---|---|---|---|
| 2.4 GHz | Primary control (DJI, FrSky, etc.) | 80 MHz (2400–2483 MHz) | WiFi coexists here |
| 5.8 GHz | Video downlink, some control | 150 MHz (5725–5875 MHz) | |
| 900 MHz | Long-range control (Crossfire, ELRS 900) | 26 MHz (902–928 MHz) | Regional, US/AU |
| 433 MHz | EU long-range links | 1.7 MHz | Very narrow band |
| 1.2 GHz | Legacy video links | Variable | Less common now |

**Jammer Architecture:**

**Broadband (barrage) jamming:**
- Noise or swept-CW across the entire band
- Simple but requires high power to cover the full bandwidth
- Power requirement: to achieve J/S (jammer-to-signal ratio) of 10 dB at 500 m range against a 1 W controller at 1 km from target:
  - Free-space path loss from jammer at 500 m: ~80 dB at 2.4 GHz
  - Controller signal at target: ~−80 dBm (1 W EIRP at 1 km)
  - Required jammer power at target: −70 dBm = jammer EIRP − 80 dB → jammer EIRP = +10 dBm (10 mW) minimum
  - In practice, need 1–10 W EIRP due to frequency-hopping processing gain, antenna orientation uncertainty, and multipath
- Weight: RF amplifier (MPA-24-40, 40 dBm at 2.4 GHz, 300 g, 30 W DC power) + SDR source + antenna = 500–800 g
- Power consumption: 20–50 W — this is a major constraint; needs a dedicated battery

**Protocol-aware (smart) jamming:**
- Detects the specific frequency-hopping pattern of the control link and jams only the current hop frequency
- Requires: fast-scanning receiver (USR B205mini) to detect hops + fast-switching transmitter
- Hop time for typical protocols: DJI OcuSync = ~1 ms hops; ELRS = 5 ms hops; FrSky = ~9 ms hops
- Reaction time to detect hop and switch jammer frequency must be <0.5 ms — very challenging
- If achieved, jamming power can be reduced by 10–20 dB because energy is concentrated on the active channel
- Requires sophisticated FPGA-based processing (not feasible on companion computer alone)
- Weight: 300–600 g if using a small FPGA board (Xilinx Zynq-based)
- Power: 10–25 W
- Significantly more effective against frequency-hopping protocols but much harder to implement

**Directional vs. Omnidirectional Antennas:**

For an airborne jammer, directionality matters enormously:
- **Omnidirectional (dipole):** 2 dBi gain, radiates in all directions, most power wasted. Also jams friendly communications. Weight: 10 g.
- **Patch antenna:** 8–12 dBi gain, 60–90° beamwidth. Must be pointed at the target. Weight: 30–80 g.
- **Phased array (e.g., 2×2 patch):** 12–15 dBi, electronically steerable over ±45°. Weight: 100–200 g. This is the optimal choice for an airborne platform — it can track the target and concentrate energy.
- **Key advantage of directional:** reduces required transmit power by 10–13 dB (factor of 10–20), bringing total system power into the feasible range (5–15 W)

**Legal Restrictions:**
- **UK:** Ofcom strictly prohibits all RF jamming by non-government entities. The Wireless Telegraphy Act 2006 makes it a criminal offense. Even the police cannot jam without Home Office authorization. Military jamming requires MOD authorization.
- **US:** FCC prohibits all jamming (47 USC § 333). Even federal agencies need specific authorization.
- **NATO:** Military operations permit jamming under ROE, but require frequency deconfliction to avoid fratricidal interference
- **EU:** Framework Decision 2005/222/JHA covers interference with information systems; national implementations vary but universally prohibit civilian jamming

**Assessment:** RF jamming is **technically feasible** at mini-UAV scale with careful antenna design (directional, 500–800 g total system, 15–40 W). The primary constraint is **legal, not technical**. For authorized military/government use, this is one of the most effective C-UAS effectors deployable from a small platform. Broadband jamming of 2.4 GHz is the easiest; protocol-aware jamming is significantly more effective but requires FPGA development. The power requirement (15–40 W) is the main engineering challenge — likely requires a dedicated LiPo pack (3S 2200 mAh = 180 g, provides ~25 minutes of jamming at 30 W).

---

## 4. Drone Swarm vs. Drone Defense

### 4.1 Multiple Interceptors Against a Swarm

**Scenario:** A hostile swarm of N_a attacking drones approaches a defended area. A swarm of N_d defender drones must intercept them.

**Force Ratio:** Lanchester's Square Law suggests that in a many-vs-many engagement where each unit can engage one opponent at a time, the combat power scales with the square of numbers. However, drone-vs-drone combat more closely follows Lanchester's Linear Law (each engagement is essentially 1v1, outcomes are somewhat random), so numerical advantage matters linearly, and what dominates is the **exchange ratio** — how many attackers each defender can neutralize.

For expendable (kamikaze) interceptors: exchange ratio = 1:1 at best. You need as many defenders as attackers, plus margin for misses. Probability of kill per engagement is perhaps 0.5–0.8 depending on guidance quality and target maneuverability. So you need N_d ≈ 1.3–2.0 × N_a defenders.

For re-usable interceptors (net-based, or jammers that can engage multiple targets): exchange ratio improves. A jammer drone can suppress multiple targets simultaneously. A net-carrier with 3 nets can potentially engage 3 targets in sequence.

### 4.2 Autonomous Target Assignment

**The Weapon-Target Assignment (WTA) Problem:**

Given N_d defenders and N_a attackers, assign defenders to targets to maximize the number of attackers neutralized while minimizing defensive gaps.

This is NP-hard in the general case. Practical approaches:

**Auction-based algorithms (CBBA — Consensus-Based Bundle Algorithm):**
- Each defender "bids" on targets based on its capability to engage (proximity, sensor quality, fuel remaining, closure geometry)
- Targets are assigned to highest bidders through a distributed consensus protocol
- Communication requirement: each defender broadcasts its bid list; convergence in O(N_d × N_a) message rounds
- Robust to communication delays and single-node failures
- Used in real multi-UAV research (MIT ACL, Georgia Tech IMDL)
- Computational load: trivial (runs on ArduPilot companion computer)

**Market-based task allocation:**
- Extension of auction algorithms with dynamic re-assignment as situation evolves
- Defenders can "trade" targets if circumstances change (e.g., one defender damaged, another has better geometry)

**Hungarian algorithm:**
- Optimal for static assignment (minimize total engagement distance/time)
- O(n³) complexity — feasible for swarms up to ~100 units in real-time
- Not robust to dynamic changes; needs re-running as situation evolves

**Closest-first heuristic:**
- Each defender engages the nearest unassigned target
- Distributed, requires minimal communication (just "target X claimed")
- Suboptimal but very fast and robust
- Works well when the defender count significantly exceeds attacker count

### 4.3 Communication Architecture

**Requirements:**
- Low latency (<100 ms) for coordination decisions
- Moderate bandwidth (each node needs to share: position, velocity, target assignments, sensor data summaries)
- Per-node data rate: ~1–5 kbps for coordination data; 50–500 kbps if sharing compressed target imagery
- Mesh networking: no single point of failure

**Implementation Options:**

| Technology | Range | Bandwidth | Weight | Latency | Notes |
|---|---|---|---|---|---|
| LoRa mesh (915/868 MHz) | 5–15 km | 0.3–50 kbps | 15 g | 50–500 ms | Low bandwidth limits to coordination data only |
| 2.4 GHz WiFi mesh (802.11s) | 0.5–2 km | 1–10 Mbps | 10 g | 5–20 ms | Interference with targets' control links |
| 5.8 GHz WiFi mesh | 0.5–1.5 km | 1–50 Mbps | 10 g | 5–20 ms | Better separation from 2.4 GHz control bands |
| Silvus StreamCaster 4200 | 5–15 km | 20–100 Mbps MANET | 230 g | <10 ms | Military-grade, expensive, robust |
| Doodle Labs Helix MANET | 5–10 km | 10–80 Mbps | 90 g | <10 ms | Popular in defense UAV applications |

For a mini-UAV swarm defense system, the recommended architecture is:
- **Primary:** Doodle Labs Helix or similar MANET radio (90 g, 5 W) for low-latency coordination and compressed video sharing
- **Backup:** LoRa mesh for coordination data if primary link is lost or jammed
- **Protocol:** ROS2 DDS (Data Distribution Service) over the mesh network, with custom message types for target tracks and assignments

### 4.4 Game Theory: Attacker Swarm vs. Defender Swarm

**The problem maps to a pursuit-evasion differential game.**

Key insights from game-theoretic analysis:

**Attacker strategy (minimax):** Distribute attackers to maximize the probability that at least one reaches the target. Optimal: spread attack across multiple approach vectors to force defenders to split. If attackers are expendable, send sacrificial elements to draw defenders, then exploit gaps.

**Defender strategy (maximin):** Position defenders to minimize the maximum probability of any attacker reaching the defended area. Optimal: maintain a layered defense with reserves. Inner layer covers high-value areas; outer layer engages early to thin the attack.

**Nash equilibrium in simple cases:** For equal-capability drones with kamikaze engagement, the Nash equilibrium tends toward defenders maintaining a patrol line perpendicular to expected attack vectors, with allocation proportional to threat density.

**Attacker advantage:** The attacker has the initiative (chooses when, where, and how to attack). A 3:1 defender-to-attacker ratio is typically needed to ensure high probability of defense, accounting for coordination overhead, sensor gaps, and engagement failures. This is consistent with historical air defense force ratios.

**Defender advantage:** Interior lines — defenders can concentrate faster if positioned centrally. Also, defenders can potentially employ area-effect weapons (jammers) that engage multiple attackers simultaneously.

---

## 5. Sensor Fusion for Tracking

### 5.1 Multi-Sensor Architecture

The optimal sensor suite for an airborne C-UAS platform combines:

1. **RF detection** (primary search sensor): provides bearing to target at long range (1–8 km), low weight/power
2. **Thermal IR camera** (secondary search + tracking): provides bearing + elevation at 200–500 m, works day/night
3. **Visual camera** (identification + fine tracking): provides bearing + elevation + target classification at 100–300 m
4. **mmWave radar** (terminal sensor): provides range + range-rate at 50–300 m, critical for intercept guidance

Each sensor provides different measurement types and has different error characteristics:

| Sensor | Measurements | Update Rate | Angular Accuracy | Range Accuracy | Range |
|---|---|---|---|---|---|
| RF DF (4-ch SDR) | Azimuth only | 1–5 Hz | ±2–10° | None (requires triangulation) | 1–8 km |
| Thermal IR | Azimuth + Elevation | 30 Hz | ±0.5° | None (angular only) | 200–500 m |
| Visual camera | Az + El + classification | 30 Hz | ±0.2° | Estimated from target size | 100–300 m |
| mmWave radar (AWR2944) | Range + Range-rate + Az + El | 10–20 Hz | ±1–2° | ±0.1 m | 50–300 m |

### 5.2 Kalman Filter Tracking Architecture

**State Vector:** The target state to be estimated:
x = [x, y, z, vx, vy, vz, ax, ay, az]

Nine states: 3D position, velocity, and acceleration in a local NED frame.

**Process Model:** Constant-acceleration model with process noise to account for target maneuvers:
x(k+1) = F × x(k) + w(k)

where F is the standard kinematic state transition matrix and w is process noise with covariance Q tuned to expected target maneuver levels (σ_a ≈ 3–8 m/s² for a maneuvering multirotor).

**Measurement Models:**

For bearing-only sensors (RF, camera):
z_bearing = [atan2(y_target - y_platform, x_target - x_platform), atan2(z_target - z_platform, range_horizontal)]

This is nonlinear → requires Extended Kalman Filter (EKF) or Unscented Kalman Filter (UKF).

For radar:
z_radar = [range, range_rate, azimuth, elevation]

Also nonlinear due to the polar-to-Cartesian conversion.

**Recommended: UKF or EKF with sequential measurement update.**

Each sensor's measurements are processed independently in the measurement update step, with appropriate measurement noise covariance R for each sensor. This naturally handles different update rates (asynchronous fusion) and sensor dropouts.

**Initialization Problem:** Bearing-only sensors cannot initialize range. Solutions:
1. Triangulation from two bearing measurements at different positions (requires platform motion, ~10 s baseline)
2. Assume target is at a fixed altitude (e.g., ground-based intelligence says target is at 100 m AGL) — constrains the problem
3. Wait for radar acquisition to provide range
4. Use rate of bearing change + known platform motion to estimate range (observability requires maneuvering)

### 5.3 Track-While-Scan (TWS) for Multiple Targets

**Architecture:**
- Detection layer: each sensor produces detection reports (bearing, strength, classification)
- Association layer: Global Nearest Neighbor (GNN) or Joint Probabilistic Data Association (JPDA) associates detections with existing tracks
- Track management: new detections not associated with existing tracks initiate tentative tracks; tracks confirmed after N detections in M scans (e.g., 3/5); tracks dropped after T_max time without update

**GNN vs. JPDA:**
- GNN: computationally simple, assigns each detection to the nearest existing track. Fails when tracks are closely spaced.
- JPDA: computes probabilistic weights for all possible detection-to-track assignments. Better in clutter and closely-spaced targets. Computational cost: O(m^n) for m detections and n tracks — practical up to ~10 targets with pruning.
- For airborne C-UAS with <10 simultaneous targets, JPDA is feasible on a companion computer.

**Multi-sensor handoff:** When a target transitions from RF-detection range to visual-detection range:
1. RF track provides predicted bearing to target
2. Camera search is biased to the predicted bearing (±uncertainty)
3. When camera detects a candidate, its bearing is compared with the RF track prediction
4. If consistent (within 3σ), the camera measurement is associated with the RF track
5. The track now has both RF and camera updates, improving accuracy
6. When radar acquires (shorter range), range/range-rate measurements are added to the same track

### 5.4 Companion Computer Requirements

**Computational Load Estimate:**

| Function | Compute | Memory | Framework |
|---|---|---|---|
| RF SDR processing (spectrum scanning) | 1 CPU core, ~30% | 200 MB | GNU Radio |
| YOLOv8-nano inference (640×640, 30 FPS) | GPU (Orin Nano: 1024 CUDA cores) | 500 MB | TensorRT |
| Thermal processing + detection | 0.5 CPU core | 100 MB | OpenCV |
| UKF tracker (10 targets) | 0.1 CPU core | 10 MB | Custom C++ |
| TWS track management + JPDA | 0.2 CPU core | 50 MB | Custom C++ |
| Guidance law computation | 0.05 CPU core | 10 MB | Custom C++ |
| ROS2 middleware + communications | 0.5 CPU core | 300 MB | ROS2 Humble |

**Total:** Requires ~2 CPU cores + GPU + 1.2 GB RAM.

**Recommended Hardware:**
- **Jetson Orin Nano 8GB:** 6 ARM Cortex-A78AE cores, 1024 CUDA cores, 8 GB unified memory. 7–15 W. 60 g (module + carrier board). Handles all of the above with headroom. This is the clear winner.
- **Raspberry Pi 5 (8GB):** 4 Cortex-A76 cores, no GPU for inference. Would need a Hailo-8 AI accelerator add-on for YOLO inference. Total: 80 g, 10 W. Viable but less elegant.
- **Radxa Rock 5B:** Decent but less software support than Jetson ecosystem.

---

## 6. Mission Engine Requirements

### 6.1 Patrol/Loiter Patterns for Defensive Coverage

**Racetrack/Hippodrome Pattern:**
- Standard loiter: elongated oval with straight legs and semicircular turns
- Coverage: long axis oriented perpendicular to expected threat axis
- Altitude: 100–300 m AGL for optimal sensor coverage
- Speed: minimum sustainable airspeed (~15–18 m/s for a 3 m wingspan aircraft) to maximize endurance
- Pattern size: 500 m × 200 m gives ~2 minute orbit time
- ArduPilot implementation: DO_SET_MODE(LOITER) with a custom Lua script for racetrack geometry, or use a series of DO_LAND_START-style waypoints defining the pattern

**Expanding Square Search:**
- For searching an area when a threat has been detected but not localized
- ArduPilot implementation: generate waypoints dynamically from companion computer via MAVLink MISSION_ITEM_INT messages

**Barrier Patrol:**
- For defending a linear feature (perimeter, border)
- Multiple drones patrol overlapping segments
- Segment length: determined by sensor detection range and required coverage overlap (typically 30–50% overlap)

### 6.2 Alert and Intercept Mission Generation

**Alert Workflow:**

1. **Detection Alert:** Sensor fusion system detects and confirms a target track (confidence > threshold)
2. **Threat Assessment:** Companion computer evaluates:
   - Target classification (multirotor, fixed-wing, bird, false alarm)
   - Target trajectory prediction (heading toward defended area?)
   - Threat level assignment (based on size, speed, heading, behavior)
3. **Engagement Decision:** If threat level exceeds threshold AND operator authorizes (or autonomous ROE permits):
4. **Intercept Path Generation:**
   - Compute intercept point using proportional navigation geometry
   - Generate a waypoint sequence: departure from patrol → transit to intercept area → terminal approach
   - Account for wind (ArduPilot provides wind estimate via EKF)
   - Time-to-intercept estimate shared with operator
5. **Handoff to Guidance:** When within sensor acquisition range of target, transition from waypoint navigation to closed-loop guidance (PN law driving ArduPilot via SET_ATTITUDE_TARGET or guided mode overrides)
6. **Post-Engagement:** If non-expendable, assess engagement success and either re-engage or return to patrol

**ArduPilot Integration:**

ArduPilot Plane supports several relevant features:
- **Guided Mode:** Accepts position/velocity/acceleration targets from companion computer via MAVLink
- **Follow Mode:** Can follow a target position provided via MAVLink FOLLOW_TARGET messages
- **Lua Scripting:** Onboard scripts can implement custom guidance laws, mode transitions, and mission logic
- **Offboard Control:** SET_POSITION_TARGET_LOCAL_NED and SET_ATTITUDE_TARGET provide direct control from companion computer

The recommended architecture:
- Mission engine runs on companion computer (Python/C++ ROS2 node)
- Communicates with ArduPilot via MAVLink over serial (UART, 921600 baud)
- Normal operations: sends waypoints and mode commands
- Intercept operations: sends SET_ATTITUDE_TARGET at 50 Hz for direct guidance control
- ArduPilot maintains safety limits (geofence, max bank angle, min altitude) even during offboard control

### 6.3 Autonomous vs. Operator-in-the-Loop Engagement

**Levels of Autonomy (adapted from US DoD OODA framework):**

| Level | Description | Latency | Applicability |
|---|---|---|---|
| 1 — Human in the loop | Operator authorizes each engagement | 5–30 s | Peacetime, permissive environments |
| 2 — Human on the loop | System engages autonomously; operator can abort | 1–5 s | Active defense zones |
| 3 — Human out of the loop | Fully autonomous engagement | 0 s | Denied-comms environments, swarm defense |

**For counter-UAS, Level 2 is the most practical starting point.** The system detects, tracks, and proposes engagement. The operator sees the target classification (camera image, track data) and presses a button to authorize. The latency constraint is that the engagement window may be short (30–120 seconds from detection to target reaching the defended area).

**Level 3 is necessary for swarm defense** where the engagement tempo exceeds human decision-making capacity. This requires very high confidence in target classification (to avoid engaging friendly or civilian drones) and clear ROE encoded in software.

### 6.4 Integration with Ground-Based Air Defense

**Data Links:**
- Defender drone receives target tracks from ground-based radar/EO systems via STANAG 4586 (NATO standard for UAV interoperability) or a simplified MAVLink-based protocol
- Ground radar provides long-range cueing (track position, velocity) that the airborne platform cannot achieve with its own sensors
- The airborne platform provides terminal tracking and engagement, complementing ground sensors

**Command and Control Architecture:**
- Ground station runs a C2 application (e.g., based on TAK — Team Awareness Kit, or a custom Qt/web application)
- Tracks from all sensors (ground radar, ground EO, airborne sensors) are fused in the ground station
- Ground station issues engagement commands to specific interceptor drones
- Each interceptor acknowledges and executes semi-autonomously

### 6.5 ROE Enforcement in Software

**Implementation as a state machine:**

```
STATES:
  PATROL → DETECT → TRACK → CLASSIFY → AUTHORIZE → ENGAGE → ASSESS

TRANSITIONS:
  PATROL → DETECT: sensor detection above threshold
  DETECT → TRACK: track confirmed (3/5 detections)
  TRACK → CLASSIFY: target within classification sensor range
  CLASSIFY → AUTHORIZE: target classified as hostile (confidence > 0.9)
  AUTHORIZE → ENGAGE: operator authorization received (Level 2) OR autonomous ROE met (Level 3)
  ENGAGE → ASSESS: engagement complete (impact, net deployed, or jammer activated)
  ASSESS → TRACK: target still active, re-engage
  ASSESS → PATROL: target neutralized

SAFETY CONSTRAINTS (checked every cycle):
  - Geofence: engagement must occur within defined volume
  - Altitude floor: no engagement below X meters AGL
  - Civilian airspace: check ADS-B receiver for nearby manned aircraft
  - Friendly drone deconfliction: check IFF (pre-shared encryption keys on friendly drones)
  - Weapon hold: operator can freeze all engagements at any time
  - Bingo fuel/battery: if below threshold, disengage and RTH
```

This state machine runs on the companion computer and gates all engagement decisions. The software cannot be overridden except by the operator's explicit authority.

---

## 7. Feasibility Assessment

### 7.1 What's Realistic at Mini-UAV Scale

**Tier 1 — Feasible and Practical Today:**

| Capability | Weight | Power | TRL | Notes |
|---|---|---|---|---|
| RF detection & direction finding | 200–400 g | 5–8 W | 7–8 | Best detection method for airborne platform |
| Visual/thermal detection with AI | 135 g | 18 W | 6–7 | Requires good training data and Jetson processing |
| Kamikaze intercept with PN guidance | ~0 g (it IS the airframe) | ~0 W extra | 5–6 | Makes the platform expendable; proven guidance algorithms |
| Sensor fusion tracker (EKF/UKF) | Software only | 2 W (compute) | 7 | Well-understood algorithms |
| Patrol/intercept mission engine | Software only | 2 W (compute) | 5–6 | ArduPilot + companion computer |
| Communication with ground C2 | 90–230 g (MANET radio) | 5–10 W | 8 | COTS radios available |

**Tier 2 — Feasible with Significant Engineering Effort:**

| Capability | Weight | Power | TRL | Notes |
|---|---|---|---|---|
| RF jamming (2.4 GHz) | 500–800 g | 20–40 W | 5–6 | Legal restrictions; power budget is tight |
| mmWave radar terminal guidance | 80–150 g | 4–6 W | 5 | Airborne clutter rejection needs work |
| Net launcher (single-shot) | 500–1000 g | Pneumatic | 4 | Very challenging engagement geometry from fixed-wing |
| Multi-drone coordination (2–4 units) | Software + radio | 5 W | 4–5 | Demonstrated in research, not in C-UAS ops |

**Tier 3 — Not Feasible or Impractical at This Scale:**

| Capability | Why Not |
|---|---|
| Acoustic detection from fixed-wing | Self-noise overwhelms target signal by 30+ dB |
| Long-range radar detection (>1 km) | Requires X-band radar too heavy/power-hungry (1.8+ kg, 35+ W) |
| GPS spoofing | Legal prohibition; countermeasures making it less effective |
| Net capture from fixed-wing at cruise speed | Engagement window too short (<1 s); miss probability too high |
| Large swarm coordination (>10 units) | Communication and assignment complexity; not enough engineering maturity |
| Directed energy (laser) | Power requirements (kW-class) utterly infeasible at this scale |

### 7.2 Platform-Specific Considerations for Fixed-Wing

**Advantages of fixed-wing for C-UAS:**
- Speed: can chase down any commercial multirotor
- Endurance: 2–6 hours of patrol vs. 30 minutes for a multirotor interceptor
- Range: can cover a large defensive area from a single launch point
- Altitude: can loiter at 200–500 m for optimal sensor coverage
- Payload capacity: 4 kg is meaningful for sensor + effector packages

**Disadvantages of fixed-wing for C-UAS:**
- Cannot hover: cannot match a stationary or slow-moving multirotor's position
- Large turn radius: 40–70 m minimum, cannot follow rapid target maneuvers
- Stall risk: aggressive maneuvering near stall speed during intercept
- Forward-firing limitation: sensors and effectors must deal with the platform's forward velocity
- Landing/launch: needs runway or catapult, limiting rapid deployment

**Best Role for a Fixed-Wing C-UAS Platform:**
The optimal role is **persistent wide-area surveillance and detection with cueing to other assets,** with kamikaze intercept as a secondary capability. The fixed-wing provides:
1. Long-endurance patrol with RF + thermal sensors scanning for threats
2. Track generation and classification
3. Cueing ground-based C-UAS systems or multirotor interceptors
4. If no other interceptor is available: autonomous kamikaze engagement using PN guidance

### 7.3 Power and Weight Budget — Recommended Configuration

**Detection-Focused Configuration (Non-Expendable):**

| Component | Weight | Power |
|---|---|---|
| RF SDR + antennas (USRP B205mini + 4-element array) | 200 g | 6 W |
| FLIR Boson 640 (thermal camera) | 30 g | 1 W |
| Arducam IMX477 + 16 mm lens (visual camera) | 60 g | 2 W |
| Jetson Orin Nano + carrier board | 80 g | 15 W |
| Doodle Labs Helix MANET radio | 90 g | 8 W |
| Dedicated sensor battery (6S 3000 mAh) | 450 g | — |
| Wiring, mounts, vibration isolation, radomes | 150 g | — |
| **Total** | **1,060 g** | **32 W** |

This leaves 2,940 g of the 4 kg payload budget for fuel/propulsion margin, additional batteries, or a single-shot net launcher.

Sensor battery endurance at 32 W draw: 6S × 3.7V × 3Ah / 32W ≈ **2.1 hours** — well-matched to platform endurance.

**Interceptor Configuration (Expendable):**

| Component | Weight | Power |
|---|---|---|
| FLIR Boson 640 (thermal, terminal guidance) | 30 g | 1 W |
| Arducam IMX477 + 6 mm lens (visual, terminal guidance) | 45 g | 2 W |
| TI AWR2944 radar module + lens antenna (terminal ranging) | 100 g | 6 W |
| Raspberry Pi 5 + Hailo-8 (guidance computer) | 90 g | 12 W |
| Dedicated sensor battery (4S 1500 mAh) | 180 g | — |
| Fragmentation/weight ring for lethality enhancement | 500 g | — |
| **Total** | **945 g** | **21 W** |

This is a much lighter configuration — the interceptor doesn't need RF detection or comms (it receives its initial target track from a separate detection platform or ground station and goes autonomous for terminal guidance).

### 7.4 Existing Systems in This Size Class

**Operational or near-operational systems in the mini-UAV C-UAS space:**

1. **Anduril Anvil:** A small quad-copter interceptor (~3 kg), kamikaze engagement, guided by Anduril's Lattice AI platform with cueing from ground sensors. Closest existing analog to what we're discussing, but it's a multirotor.

2. **Elbit Systems LAHAT-derived interceptor drones:** Israeli development of small fixed-wing interceptors with seeker heads for drone intercept. Details are classified but the concept is validated.

3. **L3Harris / Dynetics Interceptor:** Part of the US Army's counter-small UAS program. Small expendable interceptor with autonomous guidance.

4. **MARSS NiDAR + interceptor drone:** MARSS provides the detection layer (ground radar + cameras) and cues commercial interceptor drones. Demonstrated at airports.

5. **Fortem SkyDome:** Integrates TrueView radar (ground-based) with DroneHunter interceptors. The most mature commercial C-UAS system.

None of these use a mini fixed-wing as the primary interceptor platform. The fixed-wing role in existing systems is either as a detection/surveillance asset (e.g., ScanEagle in military C-UAS) or as a long-range interceptor in larger size classes (Roadrunner). A mini fixed-wing C-UAS platform as described here would be novel.

---

## Summary of Recommendations

For a 2–4 m wingspan, 4 kg payload ArduPilot platform:

1. **Primary mission: Persistent Detection and Tracking.** Equip with RF SDR + thermal/visual cameras + Jetson Orin Nano. This is entirely feasible at ~1 kg, provides 2+ hours of coverage, and generates target tracks that can be shared with ground-based or multirotor interceptor assets.

2. **Secondary mission: Expendable Intercept.** If the platform is expendable, strip the payload to thermal camera + radar + guidance computer (~950 g) and use PN guidance for kamikaze intercept. This is the most feasible kinetic approach from a fixed-wing.

3. **Do not attempt** net capture from a fixed-wing (engagement geometry is impractical), acoustic detection (self-noise), or long-range radar detection (too heavy/power-hungry).

4. **RF jamming** is technically feasible as an effector (~800 g, 30 W) but legally restricted to military applications. If authorized, it's the highest-probability-of-success non-kinetic effector.

5. **Multi-drone coordination** is the force multiplier: dedicated detection platforms cueing dedicated interceptors, with a ground station fusing all data. This architecture is more effective than trying to make one platform do everything.
