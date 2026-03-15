# Anti-Submarine Warfare (ASW) and Sonar Systems for Mini Fixed-Wing UAV Deployment

## Comprehensive Engineering Research

---

## 1. SONOBUOY TECHNOLOGY

### 1.1 Standard Military Sonobuoys

Military sonobuoys are the backbone of airborne ASW. They are standardized, expendable, and designed for deployment from aircraft at altitude and speed. The three principal types in the US Navy inventory are:

**AN/SSQ-36B/T Bathythermograph (BT) Buoy**
- Purpose: Measures water temperature as a function of depth to determine the thermal profile (bathythermograph). This data is critical for predicting sonar propagation — thermoclines refract sound and create shadow zones or convergence zones. The BT buoy does not listen for submarines; it characterizes the environment so that the tactical operator can predict where passive and active buoys will perform best.
- Dimensions: A-size — 124 mm (4.88 in) diameter, 914 mm (36 in) length.
- Weight: Approximately 5.0 kg (11 lb).
- Operation: Upon water entry, a sensor probe descends on a wire, measuring temperature at known descent rate (thus inferring depth). Data is transmitted via VHF radio to the deploying aircraft or surface station.
- Depth capability: Typically to 305 m (1,000 ft) or 457 m (1,500 ft) depending on variant.
- Endurance: Single measurement cycle — minutes.
- Cost: Approximately $300–$600 per unit (comparatively cheap, being non-acoustic).

**AN/SSQ-53F DIFAR (Directional Frequency Analysis and Recording) Passive Buoy**
- Purpose: Passive acoustic listening. The hydrophone array detects sound radiated by submarines (machinery noise, propeller cavitation, flow noise) without emitting any energy. DIFAR adds directionality — it uses an omnidirectional hydrophone plus two orthogonal accelerometers to determine the bearing to a sound source.
- Dimensions: A-size — 124 mm diameter, 914 mm length.
- Weight: Approximately 6.8 kg (15 lb).
- Operation: Deploys a surface float with VHF antenna and a hydrophone that descends to a selectable depth (typically 27 m, 61 m, 122 m, or 305 m). The acoustic signal is frequency-modulated onto a VHF carrier (31 selectable channels in the 136–173.5 MHz band) and transmitted to the aircraft. Bearing determination uses the DIFAR technique: the two directional channels are multiplexed with a reference tone.
- Frequency range: Approximately 5 Hz to 2,400 Hz (low-frequency emphasis for submarine detection).
- Endurance: Selectable — 1, 2, 4, or 8 hours (battery life trades with transmit power).
- Detection range: Highly environment-dependent. In good conditions (deep water, quiet environment, convergence zone propagation), a submarine running machinery can be detected at 20–80+ km. In coastal or noisy environments, range drops to single-digit km.
- Cost: Approximately $3,000–$5,000 per unit.

**AN/SSQ-62E DICASS (Directional Command-Activated Sonobuoy System) Active Buoy**
- Purpose: Active sonar — transmits a ping and listens for echoes. Used to confirm and localize a contact initially detected by passive means. Also provides range information (passive buoys give bearing only).
- Dimensions: A-size — 124 mm diameter, 914 mm length.
- Weight: Approximately 8.6 kg (19 lb) — the heaviest of the three, due to the acoustic projector (transmitter).
- Operation: Descends to operating depth. On command from the aircraft (via VHF downlink), it transmits an acoustic pulse. Echo returns are processed and uplinked. Provides range and bearing to target.
- Frequency: Operates in the 6.5–9.5 kHz band (command-selectable), with CW or FM pulse options.
- Ping source level: Approximately 195–200 dB re 1 μPa at 1 m.
- Detection range: Against a submarine-sized target, typically 2–8 km depending on conditions, target aspect, and countermeasures.
- Endurance: 30 minutes to 1 hour active (limited by battery powering the projector).
- Cost: Approximately $6,000–$10,000 per unit.

**Other Notable Types:**
- AN/SSQ-77C VLAD (Vertical Line Array DIFAR): Enhanced passive buoy with a vertical array of hydrophones for improved gain and directionality. A-size, approximately 9 kg. Superior noise rejection.
- AN/SSQ-101 ADAR (Advanced Deployable Acoustic Receiver): Multi-element receive array. Substantially more capable but heavier.
- AN/SSQ-110 Multistatic: Receives pings from DICASS buoys at different positions, enabling multistatic sonar geometry. This dramatically improves detection probability.

### 1.2 Size/Weight Assessment for Mini-UAV

The honest assessment is unambiguous: **standard A-size sonobuoys cannot be carried by the specified mini-UAV platform.**

| Sonobuoy | Weight | vs. 4 kg Payload |
|---|---|---|
| AN/SSQ-36B (BT) | ~5.0 kg | Exceeds by 25% |
| AN/SSQ-53F (DIFAR) | ~6.8 kg | Exceeds by 70% |
| AN/SSQ-62E (DICASS) | ~8.6 kg | Exceeds by 115% |

Even the lightest standard sonobuoy (the BT) exceeds the entire payload capacity. There is no configuration in which a 2–4 m wingspan, 4 kg payload UAV can carry even one standard sonobuoy and still fly safely. Furthermore, the 124 mm diameter, 914 mm length form factor would create significant aerodynamic issues on a small airframe.

The G-size sonobuoy (a smaller NATO standard) at approximately 90 mm diameter and 400 mm length has been explored, but these are not widely fielded and still weigh 2–4 kg with limited capability.

### 1.3 Miniature Sonobuoy Development Programs

Several efforts have aimed at smaller sonobuoys suitable for UAS deployment:

**Ultra Electronics / Sparton (now Elbit Systems of America) Mini Sonobuoys:**
Research programs under DARPA and ONR have explored sonobuoys in the 1–2 kg class. The DARPA "Distributed Agile Submarine Hunting" (DASH) program and the related "Transformational Reliable Acoustic Path System" (TRAPS) explored networks of low-cost, small sensors. However, these programs focused on surface-vessel-deployed or submarine-deployed sensors, not air-dropped miniatures.

**DARPA AOFN (Advanced Off-board Electronic Warfare) and related:**
Not directly sonobuoys, but exploration of small expendable sensors deployed from UAS.

**General Atomics / Northrop Grumman concepts:**
These have focused on MQ-9B or MQ-4C Triton deploying standard sonobuoys from larger platforms (1,000+ kg payload), not mini-UAS.

**Academic / SBIR efforts:**
Several Small Business Innovation Research (SBIR) programs have targeted a "micro-sonobuoy" in the 0.5–1.5 kg range. Key challenges:
- Miniaturizing the VHF transmitter while maintaining range (need 15+ km to be tactically useful)
- Battery energy density limits endurance
- Small hydrophone elements have higher self-noise
- Reduced acoustic aperture means poorer directionality

**Thales / L3Harris:**
Both have explored compact sonobuoy concepts for UAS integration, but published specifications are sparse. The trend is toward buoys in the 1–2 kg range with reduced endurance (1–2 hours) and reduced detection range, intended for deployment from Group 3 UAS (50–600 kg MTOW), not Group 1/2 mini-UAS.

### 1.4 DIY / Research Acoustic Sensors for Similar Function

For a 4 kg payload budget, the most viable approach is to build a custom sensor package from commercial components:

**Basic Passive Listening Buoy (achievable at ~1.5–2.5 kg):**
- Hydrophone: Aquarian Audio H2a or similar (~100 g) — $200
- Preamplifier and ADC: Custom PCB or Teensy/STM32 with audio codec (~50 g) — $50
- GPS module: u-blox MAX-M10S (~5 g) — $30
- Radio uplink: LoRa module (SX1276/SX1262) at 868/915 MHz (~20 g) — $20–40, or 2.4 GHz for higher bandwidth
- Battery: LiPo, 3.7V, 5000 mAh (~100 g) — $15
- Float housing: 3D printed or PVC, with antenna mast (~200–500 g)
- Splash protection / deployment mechanism: parachute, foam, etc. (~200–500 g)
- Total: Approximately 0.7–1.5 kg sensor package + 0.5–1.0 kg housing/deployment

This would not match a military sonobuoy in sensitivity, bandwidth, or endurance, but could detect nearby surface vessel propeller noise, outboard motors, and possibly large marine life. Submarine detection at meaningful range would be extremely challenging.

**Basic Active Sonar Buoy (achievable at ~2.5–3.5 kg):**
- Add a small acoustic projector (piezoelectric transducer) to the above
- Projector: e.g., a modified BlueRobotics Ping transducer or custom PZT element (~200–400 g)
- Driver electronics: H-bridge driver circuit (~50 g)
- Increased battery for transmit power (~200 g additional)
- Total: Approximately 2.5–3.5 kg
- Source level would be very limited — perhaps 170–180 dB re 1 μPa at 1 m, giving detection range of maybe 100–500 m against a submarine target. This is marginal for ASW but potentially useful for diver detection or harbor security.

---

## 2. COMPACT UNDERWATER ACOUSTIC SENSORS

### 2.1 BlueRobotics Ping Sonar (Single-Beam Echosounder)

- **Type:** Single-beam active echosounder (altimeter/depth finder)
- **Frequency:** 115 kHz
- **Beam width:** 30° conical
- **Range:** 0.5 m to 30 m (rated), up to 50 m in good conditions
- **Resolution:** ~1 cm distance resolution
- **Weight:** 150 g (in air, with cable)
- **Dimensions:** 43 mm diameter, 41 mm height (very compact)
- **Power:** 5V, 100–200 mA typical (~0.5–1.0 W)
- **Interface:** UART (TTL serial), 115200 baud
- **Price:** ~$280 USD
- **Assessment for ASW:** This is a bottom-profiling sonar, not designed for target detection. Its 115 kHz frequency attenuates rapidly (approximately 40 dB/km), making it useless beyond a few tens of meters for detecting objects. The narrow 30 m range and single beam make it unsuitable for submarine or vessel detection. However, it could serve as a bathymetric/obstacle-avoidance sensor on a deployed buoy.

### 2.2 BlueRobotics Ping360 (Scanning Sonar)

- **Type:** Mechanically scanning single-beam sonar (rotates 360°)
- **Frequency:** 750 kHz
- **Beam width:** 2° horizontal, 25° vertical
- **Range:** 0.75 m to 50 m (useful range typically 30 m in turbid water)
- **Angular resolution:** 0.9° (400 steps per revolution)
- **Range resolution:** ~5 cm
- **Weight:** 745 g (in air)
- **Dimensions:** 103 mm diameter, 109 mm height
- **Depth rating:** 300 m
- **Power:** 12V, 600 mA typical (~7.2 W) — notably power-hungry
- **Interface:** UART serial or Ethernet (UDP)
- **Price:** ~$2,600 USD
- **Assessment for ASW:** The 750 kHz frequency is extremely high — absorption is approximately 250 dB/km, limiting useful range to 50 m maximum. This is an imaging sonar for ROV navigation, harbor inspection, or structural surveys. It could image a submarine hull at very close range (10–50 m) but has zero utility for detection at ASW-relevant ranges. Too heavy and power-hungry for a disposable buoy, but within the 4 kg payload budget as a single deployable unit. Niche application: close-range harbor security scanning.

### 2.3 Imagenex 831L

- **Type:** Compact mechanically scanning sonar
- **Frequency:** Selectable: 200 kHz, 600 kHz, 1 MHz (model-dependent)
- **Beam width:** 2.4° horizontal at 600 kHz
- **Range:** Up to 100 m (at 200 kHz), 30 m (at higher frequencies)
- **Weight:** ~1.36 kg (3 lb) in air
- **Dimensions:** 122 mm diameter, 64 mm height
- **Depth rating:** 300 m
- **Power:** 12–24V, ~3 W typical
- **Interface:** RS-232 serial
- **Price:** ~$4,000–$6,000 USD
- **Assessment for ASW:** Better range than the Ping360 at 200 kHz, but still limited to ~100 m for meaningful target detection. The 200 kHz frequency has absorption of approximately 50 dB/km, so 500 m is the theoretical maximum (and practically much less). Weight is manageable for a deployed sensor but combined with housing, float, radio, and battery, total deployment weight approaches the 4 kg limit. Not practical for ASW detection but viable for harbor/port security applications.

### 2.4 Teledyne BlueView Micro Sonar

- **Type:** Multi-beam imaging sonar (no moving parts)
- **Frequency:** 900 kHz (M900-90) or 2.25 MHz (P900-45)
- **Field of view:** 45° or 90° sector, 20° vertical
- **Beams:** 256 or 512 beams
- **Range:** Up to 100 m (M900), 30 m practical for imaging
- **Range resolution:** ~2.5 cm
- **Weight:** ~1.1 kg (M900-90 series)
- **Dimensions:** Approximately 178 × 58 × 66 mm
- **Power:** 12–48V, ~12–15 W — high power draw
- **Interface:** Ethernet (10/100)
- **Price:** ~$15,000–$25,000 USD
- **Assessment for ASW:** High-resolution imaging sonar designed for ROV, AUV, and diver operations. Excellent for close-range target identification but the 900 kHz frequency limits range to well under 100 m. The high power consumption (12–15 W) demands a large battery for any endurance. Expensive, power-hungry, and short-ranged — not suitable for the mini-UAV deployment concept. Would be better mounted on a surface vessel or AUV.

### 2.5 Hydrophones

Hydrophones are passive sensors — they listen but do not transmit. This is the most relevant technology for a lightweight, low-power deployable ASW sensor.

**Aquarian Audio H2a-XLR**
- **Type:** Broadband omnidirectional hydrophone
- **Frequency response:** 10 Hz – 100 kHz (±3 dB from 20 Hz to 4 kHz)
- **Sensitivity:** -180 dB re 1V/μPa (requires preamplification)
- **Self-noise:** Not specified by manufacturer, but estimated at equivalent ~sea state 2 noise floor
- **Weight:** ~100 g (with short cable)
- **Dimensions:** 22 mm diameter, 160 mm length (cylindrical)
- **Depth rating:** 80 m
- **Power:** Requires external phantom power or preamp (typically 2–5 mA)
- **Interface:** Analog output (XLR or 3.5 mm, depending on model)
- **Price:** ~$200 USD
- **Assessment for ASW:** This is actually a viable sensor element for a lightweight passive buoy. The frequency range covers the primary acoustic signatures of submarines (tonal machinery at 20–500 Hz, broadband flow/cavitation noise up to several kHz). Self-noise is the main concern — at -180 dB re 1V/μPa, it needs a very low-noise preamplifier to detect quiet targets. It is omnidirectional, so it gives no bearing information (multiple buoys needed for triangulation). Extremely light and inexpensive. The primary limitation is that it is designed for recording, not real-time tactical use, and lacks the signal conditioning of military hydrophones.

**Reson TC4013 (now Teledyne Marine)**
- **Type:** Precision reference hydrophone
- **Frequency response:** 1 Hz – 170 kHz (usable), resonance at ~250 kHz
- **Sensitivity:** -211 dB re 1V/μPa (open circuit), -199 dB re 1V/μPa with integral preamp
- **Equivalent self-noise:** Approximately sea state 0 (very quiet — this is a high-quality instrument)
- **Weight:** ~56 g (element only, without cable)
- **Dimensions:** 9.5 mm diameter, 40 mm length (very small)
- **Depth rating:** 700 m
- **Power:** Internal preamp requires 2–20 mA DC bias (phantom power)
- **Interface:** BNC coaxial, analog output
- **Price:** ~$1,500–$2,500 USD
- **Assessment for ASW:** This is a substantially better sensor than the H2a for ASW applications. The lower self-noise means better detection sensitivity, and the wider bandwidth covers all frequencies of interest. The TC4013 is used in real naval acoustic research. At 56 g, it is trivially light. The cost is significant but not prohibitive for a research system. The lack of directionality remains (it is omnidirectional), but its sensitivity and noise floor make it the best candidate for a miniature passive sonobuoy hydrophone element.

**Other Relevant Hydrophones:**
- **HTI-96-MIN (High Tech Inc):** -164 dB re 1V/μPa, 2 Hz – 30 kHz, ~60 g, $400. Good balance of sensitivity, bandwidth, and cost. Internal preamp. Widely used in bioacoustics research.
- **Cetacean Research C75 (SoundTrap):** Self-contained recording hydrophone with ADC, memory, and battery. 20 Hz – 150 kHz, 340 g, ~$5,000. Records to internal storage — no real-time output, so not suitable for buoy uplink without modification.

### 2.6 Summary Table: Compact Sensors

| Sensor | Type | Frequency | Range | Weight | Power | Price | ASW Utility |
|---|---|---|---|---|---|---|---|
| BR Ping | Active echo | 115 kHz | 30 m | 150 g | 1 W | $280 | None |
| BR Ping360 | Active scan | 750 kHz | 50 m | 745 g | 7 W | $2,600 | Negligible |
| Imagenex 831L | Active scan | 200–1000 kHz | 100 m | 1,360 g | 3 W | $5,000 | Marginal (port) |
| BlueView M900 | Active imaging | 900 kHz | 100 m | 1,100 g | 15 W | $20,000 | Marginal (port) |
| Aquarian H2a | Passive hydro | 10 Hz–100 kHz | Passive | 100 g | <0.1 W | $200 | Moderate |
| Reson TC4013 | Passive hydro | 1 Hz–170 kHz | Passive | 56 g | <0.1 W | $2,000 | Good |
| HTI-96-MIN | Passive hydro | 2 Hz–30 kHz | Passive | 60 g | <0.1 W | $400 | Moderate |

---

## 3. DEPLOYMENT METHODS FROM AIRCRAFT

### 3.1 Free-Fall Drop of Floating Sensor Buoy

This is the standard military method and the most applicable to fixed-wing UAV.

**Mechanism:** The buoy is held in a tube or rack on the aircraft. A servo-actuated release drops the buoy. It falls under gravity, strikes the water, and begins operating.

**Key engineering considerations for mini-UAV:**

*Impact loading:* A buoy dropped from 50–300 m altitude reaches a terminal velocity determined by its drag coefficient and mass. For a cylindrical buoy of ~1.5 kg, terminal velocity is approximately 25–35 m/s. Water entry at this speed produces deceleration loads of 50–200 g depending on nose shape. Electronics must be ruggedized or potted.

*Water entry protection:* Military sonobuoys use a frangible nose cone that shatters on impact, absorbing energy. For a lightweight custom buoy, options include:
- Foam nose cone (crushable)
- Inflatable/compressible air bladder
- Pointed penetrator nose to reduce slam force
- Parachute to reduce terminal velocity (see 3.2)

*Deployment sequence:*
1. Buoy released from aircraft
2. Free-falls (optionally with drogue/parachute)
3. Enters water — impact braking
4. Flotation deploys: foam collar or sealed buoyancy chamber brings the antenna mast to surface
5. Hydrophone cable deploys: weighted hydrophone descends to operating depth
6. Electronics activate: GPS acquires fix, radio link initiates, acoustic data streaming begins

*Float design:* The buoy must maintain a stable surface attitude with the antenna above water in sea states up to 3–4 (0.5–2.5 m significant wave height). A spar buoy design (tall, thin, ballasted at bottom) is inherently stable. A disc float is lighter but less stable. Military sonobuoys use a spar design with an inflatable float collar.

**Carriage on the aircraft:** For a 2–4 m wingspan UAV, the buoy must be carried externally (underwing or fuselage) or in an internal bay. A 1.5 kg cylindrical buoy of approximately 80 mm diameter and 400 mm length could be carried in a fuselage-conformal pod. Aerodynamic drag penalty: approximately 5–15% increase in drag depending on installation. Release must be clean — the buoy must separate without striking the airframe. A simple gravity-drop with a servo-retracted latch is sufficient at typical UAV speeds (15–25 m/s).

### 3.2 Parachute-Deployed Sensor Pod

A small drogue or parafoil parachute reduces terminal velocity to 3–8 m/s, dramatically reducing water-entry loads.

**Advantages:**
- Electronics need far less ruggedization (10–20 g impact vs. 100+ g)
- Allows more delicate sensors (e.g., MEMS microphones, precision hydrophones)
- More controlled water entry attitude
- Can allow GPS fix during descent for precise splash-point recording

**Disadvantages:**
- Parachute adds weight: a suitable drogue for a 1.5 kg payload weighs 50–150 g
- Parachute adds volume and complexity
- Must separate cleanly after water entry (or remain as surface flag/reflector)
- Wind drift during descent reduces positional accuracy (at 100 m altitude and 5 m/s wind, lateral drift could be 50–150 m)

**Implementation:** A spring-loaded drogue packed behind the buoy deploys on release. A bridle connects to the buoy's center of mass. Upon water entry, a water-soluble link (PVA cord) dissolves and releases the parachute, which drifts away. Alternatively, the parachute becomes the surface float/radar reflector for recovery.

### 3.3 Tethered Deployment

**Not viable for fixed-wing UAV.** A tether requires the aircraft to loiter in a tight circle directly above the sensor. A fixed-wing UAV at minimum airspeed (say 12 m/s) in a banked turn of 30° has a turn radius of approximately 50 m. A tether of this length in water creates enormous drag, and the geometry is unstable — any wind gust changes the load vector. Multirotor UAVs can hover and dip sensors (this is done operationally by some naval forces using larger rotary-wing aircraft), but it is fundamentally incompatible with fixed-wing operations.

The sole exception would be a very brief "touch and go" where the fixed-wing UAV descends to just above the water, releases a sensor on a short tether, immediately climbs away, and the tether separates. This is more of a variant on free-fall deployment.

### 3.4 GPS-Tagged Deployment for Recovery

Each buoy should contain a GPS receiver and a radio beacon for post-mission recovery. The GPS coordinates of the splash point are transmitted to the ground station upon activation. After mission completion (battery nearing depletion), the buoy can activate a recovery beacon (e.g., a small LED flasher and a LoRa ping with GPS coordinates) to guide a recovery vessel.

For environmentally sensitive or expensive sensors, recovery is essential. For truly disposable buoys (sub-$100 sensor cost), recovery may not be economical and the buoys should be designed to be environmentally benign (biodegradable housing, non-toxic battery chemistry).

### 3.5 Communication Architecture: Buoy-to-Aircraft-to-Ground

This is a critical system design challenge.

**Link 1: Buoy to Aircraft (Buoy Uplink)**

The buoy floats at sea level with a short antenna mast (10–30 cm above water). The aircraft orbits overhead at 50–300 m altitude. Line-of-sight range is short (a few km at most, limited by the low buoy antenna).

Options:
- **VHF analog FM** (military standard): 136–174 MHz. Excellent propagation, good range, but requires an analog FM receiver on the aircraft and relatively high transmit power (0.5–5 W) from the buoy.
- **UHF digital** (e.g., 915 MHz ISM band): LoRa modulation at 915 MHz can achieve 5–15 km line-of-sight with 100 mW transmit power. Data rate is low (0.3–50 kbps depending on spreading factor). Sufficient for compressed acoustic feature data but not raw audio.
- **2.4 GHz WiFi/digital**: Higher bandwidth (Mbps) but shorter range and more susceptible to multipath from the sea surface.
- **Recommended for mini-UAV system:** LoRa at 868/915 MHz for command/telemetry (GPS, status, detection alerts) and a separate 2.4 GHz link for higher-bandwidth acoustic data if the aircraft is within 1–2 km. Or, process acoustic data on the buoy and transmit only detection reports via LoRa.

**Link 2: Aircraft to Ground Station**

The UAV at 100–300 m altitude has excellent line-of-sight to a ground station or ship. Standard telemetry links (900 MHz, 2.4 GHz, or 5.8 GHz) can relay data to the ground station at 10–50+ km range. ArduPilot supports MAVLink telemetry natively on 900 MHz SiK radios (100 mW, ~20 km range) or RFD900x (1 W, 50+ km).

The aircraft acts as a relay node: it receives buoy data on one radio and retransmits to the ground station on another. This requires a companion computer (e.g., Raspberry Pi) on the UAV to bridge the two links.

**Bandwidth Budget:**

| Data Type | Raw Rate | Compressed/Processed Rate |
|---|---|---|
| Raw hydrophone audio (16-bit, 48 kHz) | 768 kbps | 64–128 kbps (compressed audio) |
| Spectrogram features (1 Hz update) | — | 1–5 kbps |
| Detection alerts (event-based) | — | <0.1 kbps |
| GPS/status telemetry | — | 0.1 kbps |

If processing is done on the buoy (FFT, peak detection, classification), only detection reports and summary spectrograms need to be uplinked — easily within LoRa's capabilities. If raw audio is needed at the ground station, a higher-bandwidth link or on-buoy recording with post-recovery download is required.

---

## 4. ACOUSTIC DETECTION FUNDAMENTALS

### 4.1 Active vs. Passive Sonar Tradeoffs

**Passive Sonar:**
- Listens for sound radiated by the target
- Covert — does not reveal the searcher's presence or position
- Range determined by target radiated noise, ambient noise, and propagation loss
- Provides bearing (with directional sensors) but not range
- Effective against noisy targets (diesel-electric on surface/snorkeling, nuclear submarines at speed)
- Less effective against modern ultra-quiet submarines on battery power at low speed
- Lower power consumption — no transmitter needed
- Primary ASW search mode for initial detection

**Active Sonar:**
- Transmits a pulse and detects reflections from the target
- Non-covert — the target (and everyone else) knows you are searching
- Provides both range and bearing
- Effective against quiet targets (the target cannot "hide" by being silent)
- Range determined by source level, target strength, ambient noise, propagation loss, and reverberation
- Higher power consumption — must drive a projector
- Used primarily for localization and tracking after initial passive detection

**For a mini-UAV deployed sensor, passive sonar is strongly preferred:** it requires less power, less weight (no projector), and is more appropriate for the surveillance/detection phase.

### 4.2 Sound Propagation in Water

Sound propagation in the ocean is complex and profoundly affects sonar performance.

**Sound speed profile:** Sound speed in water depends on temperature, salinity, and pressure (depth). A typical deep-ocean profile:
- Surface: ~1,520 m/s (warm)
- Thermocline (50–500 m): speed decreases with decreasing temperature to ~1,480 m/s
- Deep isothermal layer (below thermocline): speed increases with pressure, ~1,480 m/s rising to ~1,530 m/s at 5,000 m

**Refraction:** Sound bends toward regions of lower speed. In the thermocline, sound from a shallow source refracts downward, creating a "shadow zone" below certain ranges. A submarine sitting below the thermocline may be invisible to a shallow-deployed hydrophone at certain distances.

**Key propagation phenomena:**

*Direct path:* Source and receiver in the same sound-speed layer, short range (<10 km typically). The primary detection mode for shallow-deployed hydrophones.

*Bottom bounce:* Sound reflects off the seafloor and returns to the surface. Effective in moderate depths (100–500 m). Extends detection range but with significant loss at each bounce.

*Convergence zone (CZ):* In deep water, refracted sound re-focuses at the surface at approximately 30–35 nautical mile intervals. Enables very long-range detection (60, 90 nm) but only works in deep ocean (>3,000 m depth) and only at specific ranges (annular zones).

*Sound channel (SOFAR channel):* At the depth of minimum sound speed (~1,000 m in mid-latitudes), sound is trapped by refraction from both above and below. Low-frequency sound can propagate thousands of km with minimal loss. Exploited by deep-moored hydrophone arrays (SOSUS). Not relevant for a shallow-deployed buoy.

*Surface duct:* In some conditions (isothermal surface layer), sound is trapped near the surface. Can extend detection range significantly for both source and receiver near the surface.

**Transmission loss:** For a practical engineering estimate:
- Spherical spreading: 20 log(R) dB, where R is range in meters
- Cylindrical spreading (ducted): 10 log(R) dB
- Absorption: frequency-dependent, adds α(f)·R dB
  - At 100 Hz: α ≈ 0.003 dB/km — negligible
  - At 1 kHz: α ≈ 0.06 dB/km — small
  - At 10 kHz: α ≈ 1 dB/km — significant
  - At 100 kHz: α ≈ 40 dB/km — limits range to hundreds of meters
  - At 750 kHz (Ping360): α ≈ 250 dB/km — range limited to tens of meters

**Critical implication for sensor selection:** ASW requires low frequencies (below ~10 kHz, ideally below 1 kHz). All of the commercial active sonars discussed in Section 2 operate at 100+ kHz, which is useless for ASW detection ranges. Only the passive hydrophones operate at appropriate frequencies.

### 4.3 Detection Range Estimates

Using the passive sonar equation: SE = SL - TL - NL + DI + AG - DT

Where: SE = signal excess (>0 for detection), SL = source level (target radiated noise), TL = transmission loss, NL = ambient noise level, DI = directional index of hydrophone, AG = array gain, DT = detection threshold

**Target source levels (approximate):**
- Modern SSN (nuclear submarine) at 5 knots: 110–120 dB re 1 μPa at 1 m (broadband, 50–500 Hz)
- Older SSN at 10 knots: 130–140 dB
- Diesel-electric on battery at 3 knots: 100–115 dB
- Diesel-electric snorkeling: 140–160 dB
- Small surface vessel (fishing boat): 150–170 dB
- Large merchant ship: 175–190 dB

**Ambient noise levels (broadband, 50–500 Hz):**
- Deep ocean, calm (sea state 0): 55–65 dB
- Deep ocean, moderate (sea state 3): 70–80 dB
- Coastal waters: 75–90 dB
- Busy shipping lane: 80–95 dB
- Harbor: 90–110 dB

**Achievable detection range with a single omnidirectional hydrophone (DI=0, AG=0) and DT=10 dB:**

| Target | Environment | Estimated Range |
|---|---|---|
| Snorkeling diesel sub | Deep ocean, calm | 10–50 km |
| Modern SSN at 5 kt | Deep ocean, calm | 1–5 km |
| Modern SSN at 5 kt | Coastal | 0.1–1 km |
| Quiet diesel on battery | Deep ocean, calm | 0.5–3 km |
| Quiet diesel on battery | Coastal | 50–500 m |
| Fishing boat | Any | 5–20 km |
| Large merchant | Any | 20–100 km |

These are rough estimates and highly sensitive to actual propagation conditions. The key takeaway: **a single omnidirectional hydrophone can detect noisy targets at useful ranges, but detecting modern quiet submarines requires either very favorable conditions, multiple sensors, or sophisticated processing.**

### 4.4 What a Small Sensor Can Realistically Detect

Given a Reson TC4013 or comparable hydrophone deployed at 10–50 m depth:

**Reliably detectable (>90% probability in moderate conditions):**
- Surface vessels of all sizes within 5–20 km (propeller tonals, engine harmonics)
- Outboard motors within 2–10 km
- Divers with open-circuit SCUBA within 100–500 m (bubble noise)
- Marine mammals (whales, dolphins) within 5–50 km (biological sounds are often very loud)

**Potentially detectable (50–90% probability, good conditions):**
- Diesel-electric submarine snorkeling within 5–20 km
- AUV/UUV within 200–2,000 m (electric motor whine, propeller)

**Difficult to detect (<50% probability):**
- Modern nuclear submarine at low speed: requires convergence zone propagation or very quiet environment, neither of which is guaranteed
- Diesel-electric on battery at low speed: may be quieter than ambient noise at ranges beyond 1–2 km
- Diver propulsion vehicles (DPVs): very quiet, detectable only at close range (<200 m)

---

## 5. SEARCH PATTERNS FOR ASW

### 5.1 Barrier Search

**Concept:** Deploy a line of buoys across a strait, channel, or expected transit route. The target must pass through the barrier to reach its objective.

**Geometry:** N buoys spaced at distance D along a line of length L = N × D. Each buoy has a detection radius R (approximation — actually a probability-of-detection function of range).

**Spacing:** For high probability of detection, overlap between adjacent buoys is needed: D ≤ 2R for >90% detection probability. For R = 2 km (optimistic for a quiet target with a small sensor), spacing D = 3–4 km, and a 20 km strait requires 5–7 buoys.

**Mini-UAV application:** A UAV carrying one buoy at a time would need 5–7 sorties to establish this barrier, which is feasible if each sortie is 30–60 minutes. The buoys must have sufficient endurance to remain operational until all are deployed and the target transit window has passed.

### 5.2 Area Search (Grid Pattern)

**Concept:** Cover an area with a regular grid of buoys. Used when the target location is unknown within a broad area.

**Geometry:** For an area A with buoys of detection radius R, the number of buoys needed for full coverage is approximately A / (π R²). For A = 100 km² and R = 2 km, this requires approximately 8 buoys. For R = 500 m (more realistic for a small sensor against a quiet target), this requires approximately 127 buoys — not feasible from a mini-UAV.

**Mini-UAV application:** Area search is only practical if the detection radius is large enough that a manageable number of buoys covers the area. With small sensors, area search is impractical for open-ocean ASW. It may be viable for:
- Lake or harbor surveillance (small area)
- Searching a localized area after initial cueing from other intelligence

### 5.3 Cross-Fix Triangulation

**Concept:** Multiple passive buoys detect the same target. Each buoy provides a bearing line (if directional) or a time-of-arrival. The intersection of bearing lines or the time-difference-of-arrival (TDOA) computation gives the target position.

**For omnidirectional hydrophones (our case):** TDOA is the primary method. If three or more buoys detect the same acoustic event (e.g., a transient or a continuous tonal), the time differences between arrivals at different buoys can be used to compute the source location. This requires:
- Synchronized clocks (GPS-disciplined oscillators on each buoy — achievable with ~100 ns accuracy from GPS PPS)
- Sufficient SNR at each buoy
- Known sound speed (or estimated from BT data)
- Buoy positions known (GPS)

**Minimum configuration:** Three buoys for 2D localization, four for 3D. Buoy baseline (separation) should be comparable to or larger than the distance to the target for good geometric dilution of precision (GDOP).

**Accuracy:** For buoys separated by 2 km, a target at 5 km range, sound speed uncertainty of ±5 m/s, and time-measurement accuracy of ±1 ms: position uncertainty is approximately 100–500 m. Adequate for cueing further investigation, not for weapons targeting.

### 5.4 Datum Search

**Concept:** When a target is detected or its position is estimated from other intelligence (e.g., periscope sighting, ESM intercept, satellite detection), establish a datum point and expand the search from there. The target could be anywhere within a circle of radius V × T, where V is the target's maximum speed and T is the time since the datum.

**Procedure:**
1. Deploy buoys at the datum point
2. Expand outward in concentric rings or sectors
3. Priority deployment along likely escape routes (e.g., toward deep water, away from shore)

**Mini-UAV application:** This is the most promising scenario for mini-UAV ASW. The UAV is scrambled from a forward base or ship, flies to the datum, and deploys buoys in an expanding pattern. Multiple sorties may be needed as the datum expands. Speed is essential — the datum grows at 10–20 km/hr for a submarine at 5–10 knots.

### 5.5 Optimal Buoy Spacing

The optimal spacing depends on the detection probability function, which is modeled as:

P(detect | range R) = P₀ × exp(-(R/R₅₀)²)

Where R₅₀ is the range at which detection probability is 50%. For a "cookie cutter" model (detect with certainty within radius R, not at all beyond R), spacing D = √3 × R gives full hexagonal coverage with minimum buoys.

For probabilistic detection, the cumulative detection probability across a field of buoys depends on the number of independent detection opportunities. More buoys, more closely spaced, gives higher probability.

### 5.6 ArduPilot Mission Integration

ArduPilot supports custom mission scripting via Lua or MAVLink. An automated deployment pattern could be implemented as:

**Approach 1: Pre-planned waypoint mission**
- Ground station software (e.g., QGroundControl with custom plugin or Mission Planner script) generates a waypoint pattern based on:
  - Search area geometry
  - Desired buoy spacing
  - Wind/drift corrections
  - UAV performance (endurance, speed, payload configuration)
- At each deployment waypoint, a servo command (DO_SET_SERVO) triggers the release mechanism
- The UAV confirms release via a payload sensor (e.g., microswitch on the release latch)

**Approach 2: Lua scripting on ArduPilot**
- ArduPilot 4.1+ supports Lua scripting for custom automation
- A Lua script could:
  - Accept a search pattern type (barrier, grid, datum) and parameters
  - Generate waypoints dynamically
  - Trigger deployment at computed positions
  - Adjust spacing based on real-time buoy feedback (adaptive search)

**Approach 3: Companion computer**
- A Raspberry Pi or similar running ROS/MAVROS interfaces with ArduPilot via MAVLink
- Higher-level planning algorithms (Python, C++) generate missions
- Can incorporate buoy feedback in real-time (e.g., move next deployment closer to a buoy reporting a contact)

---

## 6. DATA PROCESSING AND CLASSIFICATION

### 6.1 Acoustic Signal Processing

**Fast Fourier Transform (FFT):** The fundamental tool. Converts time-domain hydrophone data into frequency-domain spectra. Typical parameters:
- Sample rate: 48 kHz (covers 0–24 kHz Nyquist)
- FFT size: 4,096 points (frequency resolution: 48000/4096 = 11.7 Hz)
- Window: Hanning or Blackman-Harris to reduce spectral leakage
- Overlap: 50–75% for temporal resolution
- Output: Power spectral density (PSD) in dB re 1 μPa²/Hz

**Spectrogram (LOFAR display):** A time-frequency plot (frequency on Y-axis, time on X-axis, intensity as color). This is the primary display for passive sonar operators. Submarine tonals appear as persistent horizontal lines. Machinery harmonics appear as sets of equally-spaced lines. Broadband noise appears as a raised noise floor across frequencies.

**DEMON (Demodulation of Envelope Modulation of Noise):** A technique for extracting propeller blade-rate information from broadband cavitation noise. The broadband noise radiated by a cavitating propeller is amplitude-modulated at the blade rate (shaft RPM × number of blades). DEMON analysis:
1. Bandpass filter the hydrophone signal in a frequency band where cavitation noise dominates (typically 1–20 kHz)
2. Envelope-detect (rectify and low-pass filter) — this extracts the modulation
3. FFT the envelope — peaks appear at the blade rate and harmonics
4. Blade rate gives shaft RPM; harmonics reveal number of blades

**DEMON is extremely valuable** for classification: different vessel types have characteristic blade rates. A submarine with a 7-blade propeller at 2 RPM (typical low-speed) has a blade rate of 14 Hz — very difficult to detect but distinctive if found.

**Narrowband analysis:** Zoom FFT or high-resolution spectral estimation (MUSIC, ESPRIT algorithms) for detecting narrow tonal lines buried in noise. Tonals from rotating machinery (turbines, generators, pumps) are the primary passive detection cue for submarines.

**Broadband energy detection:** Simple integration of spectral energy across a frequency band. Useful for detecting transients (torpedoes, active sonar pings from other sources, marine mammal clicks, hull popping from depth changes).

### 6.2 Target Classification

The acoustic signature of a contact must be classified to distinguish threats from non-threats.

**Surface vessel characteristics:**
- Strong broadband cavitation noise (cavitation is nearly continuous at typical speeds)
- High blade rate (merchant props: 80–120 RPM, 3–5 blades = 240–600 Hz blade rate)
- Engine harmonics: diesels at 15–30 Hz per cylinder, multiples
- Hull/wake noise: broadband, 100 Hz–10 kHz
- Generally loud (SL 150–190 dB)

**Submarine characteristics:**
- Much quieter than surface vessels at low speed
- Tonal signatures: machinery at discrete frequencies (often 50/60 Hz from electrical systems, plus specific machinery tonals)
- Very low blade rate at patrol speed (10–30 Hz)
- Broadband flow noise dominates at higher speeds
- Periodic transients: valve operations, hull popping during depth changes

**Marine life:**
- Whales: very specific frequency bands (blue whale: 10–30 Hz moans; humpback: 100–4,000 Hz songs; sperm whale: broadband clicks)
- Dolphins: echolocation clicks at 20–130 kHz, whistles at 2–20 kHz
- Snapping shrimp: broadband crackling at 2–200 kHz (dominant noise source in tropical shallow water)

**Classification features:**
1. Spectral content: frequency of tonals, bandwidth of broadband components
2. Modulation: blade rate, shaft rate from DEMON
3. Source level: estimated by measuring received level and compensating for range (if known)
4. Temporal behavior: constant (transiting vessel), intermittent (machinery cycling), Doppler shift (approaching/receding)
5. Speed estimation: from Doppler shift or DEMON blade rate

### 6.3 Machine Learning for Acoustic Classification

This is an active area of research with increasing maturity.

**Feature-based approaches:**
- Extract hand-designed features (spectral centroid, bandwidth, DEMON peaks, Mel-frequency cepstral coefficients) from audio segments
- Feed into traditional ML classifiers: SVM, Random Forest, Gradient Boosted Trees
- Advantages: interpretable, works with small training sets, low computation
- Training data: NOAA acoustic datasets, ShipEar database, DeepShip dataset

**Deep learning approaches:**
- Convert audio to spectrograms (Mel-spectrogram or CQT)
- Feed into CNN (ResNet, VGG) or audio-specific architectures (SoundNet, PANNs)
- End-to-end learning: raw audio to classification via 1D-CNN or Transformer
- Advantages: can discover features humans miss, excellent performance with large training data
- Disadvantages: requires substantial training data, computationally expensive, "black box"

**Edge deployment considerations:**
- Buoy processor: a low-power microcontroller (STM32H7, ESP32-S3) can run a small CNN (~100K parameters) for basic classification at 5–20 inferences/second. TensorFlow Lite Micro or TinyML frameworks.
- Aircraft companion computer: a Raspberry Pi 4 or Coral TPU can run larger models (~10M parameters) in real-time.
- Ground station: full workstation with GPU can run state-of-the-art models on all buoy data simultaneously.

**Recommended architecture for mini-UAV system:**
1. On-buoy: simple energy detection and threshold-based screening (is there anything worth reporting?). Transmit compressed audio snippets and feature vectors only when threshold is exceeded.
2. On-aircraft or ground station: run CNN classifier on received data to categorize contacts.
3. Human operator at ground station: final decision authority, with ML recommendations displayed.

### 6.4 Bandwidth Requirements for Acoustic Data Uplink

| Processing Level | Data Transmitted | Bandwidth Required |
|---|---|---|
| Raw audio (16-bit, 48 kHz, mono) | PCM samples | 768 kbps |
| Compressed audio (Opus @ 64 kbps) | Encoded audio stream | 64 kbps |
| Spectrogram snapshots (1/sec, 256 bins, 8-bit) | 256 B/sec | 2 kbps |
| Feature vectors (1/sec, 20 features, 32-bit) | 80 B/sec | 0.6 kbps |
| Detection reports (event-triggered) | Short messages | <0.1 kbps |

LoRa at SF7/BW125 delivers approximately 5.5 kbps — sufficient for feature vectors and detection reports, but not for audio streaming. For compressed audio, a 2.4 GHz link (or LoRa at very low SF with close range) is needed.

---

## 7. MARITIME PATROL INTEGRATION

### 7.1 Combined EO/IR Surveillance + Sonar Deployment

The mini-UAV can serve dual roles:
1. **Visual/thermal surface surveillance:** Camera (EO) and thermal imager (IR) for detecting and tracking surface vessels, periscopes, snorkels, wakes.
2. **Acoustic subsurface surveillance:** Deploying sonar buoys.

**Operational concept:** The UAV flies a maritime patrol route with EO/IR sensors. When the mission requires acoustic coverage of a specific area (e.g., a chokepoint, a datum from intelligence), it deploys one or more buoys and then continues its patrol, orbiting within radio range of the deployed buoys to relay data.

**Sensor suite within 4 kg payload budget (if carrying one buoy):**
- EO camera (gimbal-mounted): ~200–400 g
- Thermal camera: ~100–200 g
- Sonar buoy: ~1,500–2,500 g
- Buoy relay radio: ~50–100 g (if separate from telemetry radio)
- Total: ~1,850–3,200 g — within 4 kg budget

If more buoys are needed, the EO/IR payload may need to be sacrificed on some sorties, or a multi-sortie approach used where one sortie carries the camera and subsequent sorties carry buoys.

### 7.2 Surface Vessel Tracking and Exclusion

A critical problem in ASW is distinguishing submarine contacts from surface vessels. If you can identify and track all surface vessels in the area, any remaining acoustic contact is potentially a submarine.

**AIS (Automatic Identification System):** All commercial vessels >300 GT, and all passenger vessels, must transmit AIS. A lightweight AIS receiver (~30 g, e.g., dAISy HAT, ~$50) on the UAV or ground station provides identity, position, course, and speed for all cooperative vessels. Correlating AIS tracks with acoustic contacts allows immediate exclusion of known surface vessels.

**Visual/thermal identification:** The UAV's EO/IR sensors can identify vessels that are not transmitting AIS (small boats, military vessels, vessels with AIS disabled). Image recognition can estimate vessel type and size.

**Exclusion workflow:**
1. Buoy detects acoustic contact on bearing X at estimated range Y
2. Cross-reference with AIS tracks: is there a known vessel at that bearing/range? If yes, classify as "surface vessel, identified" and exclude
3. Cross-reference with EO/IR: is there a visible vessel? If yes, classify and exclude
4. Remaining unidentified contacts: potential subsurface targets — escalate

### 7.3 Multi-Sortie Search Operations

A single mini-UAV sortie might deploy 1–2 buoys (given payload constraints). Building an effective search requires multiple sorties:

**Operational timeline example:**
- Sortie 1 (T+0 to T+45 min): Deploy buoy 1 at position A. Transit back.
- Sortie 2 (T+60 to T+105 min): Deploy buoy 2 at position B. Transit back.
- Sortie 3 (T+120 to T+165 min): Deploy buoy 3 at position C. Orbit to relay data from all three buoys.
- Sortie 4+: Continue deployment or transition to relay/surveillance.

**Battery swap time:** With pre-charged batteries, turnaround can be 5–10 minutes (land, swap battery and buoy payload, relaunch). Field crew of 2–3 people.

**Buoy endurance constraint:** If buoys have 4–8 hours of battery life, the first buoy deployed will expire before a large field is fully established. This limits the effective search to areas that can be seeded within the buoy lifetime.

**Concept of operations:** A practical mini-UAV ASW system would use a team of 2–3 UAVs operating in relay, with a total inventory of 10–20 buoys for a single search operation.

### 7.4 Coordination with Surface Vessels and Other Aircraft

**With a surface vessel (mothership):**
- UAV launches and recovers from the vessel's deck
- Buoy data is relayed to the vessel's combat information center
- The vessel can deploy its own sonar (hull-mounted or towed array) for correlation
- The vessel can investigate contacts and recover buoys
- The UAV extends the vessel's search perimeter beyond its own sonar range

**With other aircraft:**
- A larger ASW aircraft (P-8A, MQ-9B) may be deploying standard sonobuoys in the same area
- Data fusion between mini-UAV buoys and military sonobuoys improves detection
- The mini-UAV can fill gaps in the larger aircraft's pattern or provide persistent coverage after the larger aircraft departs

**With shore-based infrastructure:**
- Fixed hydrophone arrays (SOSUS legacy, or newer distributed systems) may provide initial detection
- The mini-UAV is cued to investigate specific contacts, deploying buoys for localization

---

## 8. FEASIBILITY ASSESSMENT FOR MINI-UAV ASW

### 8.1 Standard Sonobuoys: Definitively Not Feasible

There is no configuration in which a 2–4 m wingspan, 4 kg payload electric UAV can carry a standard A-size sonobuoy. The lightest standard sonobuoy (AN/SSQ-36B BT, ~5 kg) exceeds the entire payload capacity. This is a hard physical constraint, not an engineering challenge to be overcome. Military sonobuoys are deployed from P-3C/P-8A patrol aircraft, SH-60 helicopters, and MQ-9B Triton — all with payload capacities of 100+ kg.

### 8.2 Minimum Viable Custom Sonar Buoy

**The lightest useful passive acoustic buoy can be built at approximately 1.0–1.8 kg:**

| Component | Weight | Cost |
|---|---|---|
| Hydrophone (TC4013 or HTI-96-MIN) | 60 g | $400–2,000 |
| Preamplifier + ADC (custom PCB) | 30 g | $50 |
| Microcontroller (STM32H7 or similar) | 15 g | $20 |
| GPS module (u-blox) | 5 g | $30 |
| LoRa radio module + antenna | 25 g | $30 |
| Battery (3.7V 6000 mAh LiPo) | 120 g | $20 |
| Hydrophone cable (10 m, thin) | 100 g | $20 |
| Ballast weight for hydrophone depth | 50 g | — |
| Float body (PVC/3D-printed, sealed) | 200 g | $30 |
| Antenna mast + VHF whip | 50 g | $10 |
| Splash protection (foam nose) | 50 g | $5 |
| Parachute (small drogue) | 80 g | $20 |
| Wiring, connectors, potting | 50 g | $20 |
| **Total** | **~835 g – 1,200 g** | **~$655–$2,255** |

This buoy would:
- Listen passively across 5 Hz – 30 kHz
- Deploy the hydrophone to ~10 m depth
- Perform on-board FFT and basic detection
- Transmit detection reports and feature data via LoRa at 2–5 km range to the orbiting UAV
- Operate for approximately 4–8 hours on battery
- Provide GPS position for mapping and recovery

It would NOT:
- Match the sensitivity of a military DIFAR sonobuoy (no directional capability)
- Detect quiet submarines at ranges beyond a few km
- Operate in heavy sea states (small float is unstable in >SS3)
- Provide the bandwidth for raw audio streaming

### 8.3 Can Useful Acoustic Detection Be Done with Sub-1 kg Sensors?

**Yes, but with significant limitations.** A sub-1 kg sensor can detect:
- Surface vessels at useful range (5–20 km) — but AIS and radar do this better
- Loud submarines (snorkeling, transiting at speed) at 2–10 km — useful for chokepoint monitoring
- Divers and small underwater vehicles at 100–500 m — useful for harbor security
- Marine mammals — useful for environmental monitoring (a commercial application that helps fund development)

**It cannot reliably detect modern quiet submarines** operating on battery at low speed. This requires either:
- Much larger sensors with lower self-noise and directional capability (i.e., military sonobuoys)
- Many sensors in a dense network (feasible but requires dozens of buoys)
- Favorable propagation conditions (which cannot be guaranteed)

### 8.4 Range Limitations of Small Acoustic Sensors

The fundamental physics limitation is the noise floor. A small hydrophone element (even a good one like the TC4013) in a lightweight, imperfectly isolated float housing will have a higher effective noise floor than a military sonobuoy with vibration isolation, electromagnetic shielding, and optimized preamplifier design. Realistically, the noise floor of a custom buoy will be 10–20 dB worse than a military sonobuoy, which directly translates to a factor of 3–10 reduction in detection range for the same target.

Additionally, the lack of directional capability (which requires either multiple hydrophones in a known geometry, or specialized sensors like DIFAR accelerometers) means that a single buoy can detect but not localize. Multiple buoys with TDOA processing partially compensate, but require precise time synchronization and sufficient signal-to-noise ratio at all buoys simultaneously.

### 8.5 Comparison with Alternative Platforms

**Is ASW better done by surface vessels?**
Surface vessels can carry large, powerful hull-mounted sonar and towed arrays with detection ranges of 20–100+ km. They can deploy standard sonobuoys. They are clearly superior for ASW capability. However, they are slow to reposition (15–30 knots vs. 60–100 knots for a UAV), expensive to operate, and detectable by the submarine. Mini-UAVs do not replace surface vessels but can complement them.

**Is ASW better done by larger aircraft?**
Yes, for capability. A P-8A Poseidon carries 120+ sonobuoys and sophisticated processing. An MQ-9B can carry 40+. But these are multi-million dollar platforms with multi-thousand dollar per hour operating costs. A mini-UAV system costing $5,000–$20,000 total (UAV + buoys + ground station) offers a capability that is many orders of magnitude cheaper, even if many orders of magnitude less capable.

### 8.6 Niches Where Mini-UAV ASW Adds Value

**1. Rapid response to intelligence cues in remote locations**
A man-portable mini-UAV system can be deployed from a beach, small boat, or remote airstrip within minutes. It can seed an area with acoustic sensors far faster than waiting for a ship or large aircraft. For island nations, coast guards, and special operations forces operating from austere bases, this may be the only ASW capability available.

**2. Disposable/expendable sensor deployment in contested environments**
In an environment where enemy air defenses make large aircraft operations dangerous, a small, low-RCS UAV deploying cheap buoys is expendable. The loss of a $1,000 UAV and $500 buoy is acceptable; the loss of a $250M P-8A is not.

**3. Harbor and port security**
Detecting divers, UUVs, and small submarines in harbors and approaches does not require long-range ASW sonar. Small sensors deployed by UAV can establish a perimeter around a port, anchorage, or critical infrastructure. Detection ranges of 100–500 m are sufficient in this context. This is arguably the most immediately practical application.

**4. Chokepoint monitoring**
Narrow straits (1–5 km width) can be covered by a few buoys. Even with modest detection range, a barrier across a chokepoint forces a submarine to pass within detection range of at least one sensor. Combined with surface surveillance (AIS, radar, EO/IR), this can provide a basic subsurface awareness capability.

**5. Environmental and research applications**
Monitoring marine mammal activity, measuring ambient noise for environmental impact assessments, and conducting acoustic surveys. These applications are commercially viable and do not require military-grade sensitivity. The mini-UAV enables rapid, wide-area sensor deployment for researchers.

**6. Training and concept development**
Military forces can use mini-UAV-deployed buoys for ASW training exercises at a fraction of the cost of real sonobuoys. The acoustic data quality need not be military-grade for training purposes.

### 8.7 Recommended System Architecture

For the specified platform (2–4 m wingspan, 4 kg payload, electric, ArduPilot):

**UAV Configuration:**
- Primary payload: 1 custom passive acoustic buoy (~1.2 kg) + EO camera (~300 g)
- Alternatively: 2 buoys (no camera) at ~1.0 kg each for dedicated ASW sorties
- Buoy release mechanism: Servo-actuated belly latch, spring-assisted ejection
- Relay radio: LoRa 868/915 MHz module connected to companion computer
- Companion computer: Raspberry Pi Zero 2W (~15 g) running relay software and basic acoustic processing

**Buoy Design:**
- Hydrophone: HTI-96-MIN (best cost/performance) or TC4013 (best performance)
- Deployment depth: 10 m (wire-guided, ballast-weighted)
- Processing: STM32H7 running FFT, DEMON, and simple threshold detection
- Communications: LoRa uplink (feature data + detection alerts), 2.4 GHz backup for audio snippets
- Endurance: 6 hours target
- Splash protection: Foam nose cone + small drogue parachute
- Recovery: GPS beacon activated on low battery

**Ground Station:**
- Laptop running custom software (Python/C++ with Qt or web GUI)
- LoRa receiver (backup direct link from buoys at short range)
- MAVLink telemetry receiver for UAV data
- Display: map with buoy positions, contact tracks, spectrogram displays
- AIS receiver for surface vessel correlation

**Estimated Total System Cost:**
- UAV airframe + autopilot + radios: $2,000–$5,000
- 10 buoys: $6,500–$22,500 (depending on hydrophone choice)
- Ground station hardware: $1,500–$3,000
- Software development: substantial (person-months of effort)
- **Total hardware: $10,000–$30,000** for a research/prototype system

---

## SUMMARY OF KEY CONCLUSIONS

1. **Standard military sonobuoys are incompatible** with the specified mini-UAV. This is a hard weight constraint with no workaround.

2. **A custom passive acoustic buoy at 1.0–1.8 kg is feasible** and can fit within the 4 kg payload alongside a small EO camera.

3. **Passive sonar is the only viable modality** for UAV-deployable ASW sensors. All commercial active sonars operate at frequencies far too high for ASW-relevant ranges. A passive hydrophone at low frequencies (10 Hz – 10 kHz) can detect surface vessels reliably and loud submarines at modest range.

4. **Detection of modern quiet submarines is not realistic** with this class of sensor. The system's ASW value lies in detecting noisier targets (snorkeling submarines, transit-speed submarines), monitoring chokepoints, and providing harbor/port security against divers and UUVs.

5. **The strongest use case is harbor security and chokepoint monitoring**, where detection ranges of 100 m – 5 km are tactically useful and achievable with small sensors.

6. **Multi-buoy TDOA processing** can provide localization without directional hydrophones, but requires precise GPS-disciplined time synchronization across all buoys.

7. **On-buoy processing with LoRa uplink** is the right architecture — transmit detections and features, not raw audio, to stay within the bandwidth of low-power radio links.

8. **The system is best viewed as a complement** to conventional ASW assets, not a replacement. Its value is in rapid deployment, low cost, expendability, and access to austere environments where larger platforms cannot operate.
