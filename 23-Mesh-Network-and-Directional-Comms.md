# Ground Mesh Network with Directional Antenna Tracking

## Project Overview

A ground-based mesh relay network using directional antennas on servo gimbals with hill-climbing signal optimisation algorithms. Two variants: RF (radio frequency) and FSO (free-space optical / laser).

This is a standalone project that:
1. Solves the immediate school network bypass problem
2. Teaches RF engineering, control theory, and embedded systems
3. Transfers directly to the drone comms relay constellation (doc 22)
4. Is legally deployable with zero licensing requirements

## Concept

```
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │  NODE A  │ ◄─RF──► │  NODE B  │ ◄─RF──► │  NODE C  │
  │ (school) │         │ (relay)  │         │ (home)   │
  │          │         │          │         │          │
  │ laptop   │         │ battery  │         │ PC + net │
  │ connects │         │ powered  │         │ exit to  │
  │ via WiFi │         │ on roof/ │         │ internet │
  │          │         │ tree/pole│         │          │
  └──────────┘         └──────────┘         └──────────┘
      │                     │                     │
  ┌───┴───┐            ┌───┴───┐            ┌───┴───┐
  │ANTENNA│            │ANTENNA│            │ANTENNA│
  │on 2-axis           │on 2-axis           │on 2-axis
  │servo   │           │servo   │           │servo   │
  │gimbal  │           │gimbal  │           │gimbal  │
  └───────┘            └───────┘            └───────┘
      ▲                     ▲                     ▲
  Hill-climbing          Hill-climbing          Hill-climbing
  algorithm aims         algorithm aims         algorithm aims
  antenna at             antennas at            antenna at
  strongest signal       both neighbours        strongest signal
```

## Part 1: Hill-Climbing Antenna Tracker

### The Algorithm

Hill climbing (also called gradient ascent) for signal tracking:

```
  HILL-CLIMBING SIGNAL OPTIMISATION
  ══════════════════════════════════

  The antenna sits on a 2-axis gimbal (pan + tilt).
  The algorithm maximises RSSI (Received Signal Strength Indicator).

  PSEUDOCODE:
  ────────────
  1. Read current RSSI at current pan/tilt angles
  2. Nudge pan by +δ degrees → read RSSI
  3. Nudge pan by -δ degrees → read RSSI
  4. Move pan to whichever direction improved RSSI
  5. Nudge tilt by +δ degrees → read RSSI
  6. Nudge tilt by -δ degrees → read RSSI
  7. Move tilt to whichever direction improved RSSI
  8. If improvement < threshold: reduce δ (fine-tune)
  9. If no improvement for N cycles: increase δ (re-scan)
  10. Goto 1

  STATE DIAGRAM:
  ──────────────
                    ┌──────────┐
            ┌──────│  SEARCH   │──────┐
            │      │ (large δ) │      │
            │      └────┬──────┘      │
            │           │ signal      │ no signal
            │           │ found       │ for 30s
            │           ▼             ▼
            │      ┌──────────┐  ┌──────────┐
            │      │  TRACK   │  │  SPIRAL  │
            │      │ (small δ)│  │  SCAN    │
            │      └────┬─────┘  │ (full sky│
            │           │        │  search) │
            │           │ signal └────┬─────┘
            │           │ lost        │ signal
            │           │             │ found
            │           ▼             │
            │      ┌──────────┐       │
            └──────│ REACQUIRE│◄──────┘
                   │(medium δ)│
                   └──────────┘
```

### Why Hill Climbing (Not Just Pointing at Known GPS Coordinates)

You could just calculate the bearing between two known GPS positions and point the antenna there. But hill climbing is better because:

1. **Self-calibrating** — no need to precisely align the gimbal to north or level it
2. **Adapts to multipath** — in urban environments, the strongest signal path may not be the direct line (reflections off buildings can be stronger)
3. **Works with moving targets** — if you later mount this on a drone, it tracks the other drone automatically
4. **Handles antenna imperfections** — real antenna patterns aren't perfectly symmetric; the algorithm finds the true peak
5. **It's the same algorithm used in satellite dish auto-alignment** — industry-proven approach

### Hardware Design

```
  ANTENNA TRACKER ASSEMBLY
  ════════════════════════

  SIDE VIEW:
  ──────────
       ┌─────────────────┐
       │  PATCH ANTENNA   │  ◄── directional (12-18 dBi)
       │  or YAGI         │      pointed at target node
       └────────┬─────────┘
                │
           ┌────┴────┐
           │  TILT   │  ◄── servo 2 (MG996R or similar)
           │  SERVO  │
           └────┬────┘
                │
           ┌────┴────┐
           │   PAN   │  ◄── servo 1 (continuous rotation or 270°)
           │  SERVO  │
           └────┬────┘
                │
           ┌────┴────────────────────┐
           │      BASE PLATE         │
           │                         │
           │  ┌────────┐  ┌───────┐  │
           │  │ ESP32   │  │ RADIO │  │
           │  │ + RSSI  │  │MODULE │  │
           │  │ reader  │  │       │  │
           │  └────────┘  └───────┘  │
           │                         │
           │  ┌──────────────────┐   │
           │  │  BATTERY (18650) │   │
           │  └──────────────────┘   │
           └─────────────────────────┘

  TOP VIEW (showing pan rotation):
  ─────────────────────────────────

              ╱ antenna
             ╱  beam
            ╱   pattern
           ╱    (~30° wide)
          ╱
    ┌────○────┐  ◄── pan servo rotates 360°
    │  gimbal  │
    └──────────┘
```

### Bill of Materials (Per Node)

| Component | Model | Cost | Weight | Notes |
|-----------|-------|------|--------|-------|
| Microcontroller | ESP32-S3 DevKit | £8 | 10g | WiFi + BLE + ADC for RSSI |
| Pan servo | MG996R (180°) or DS3218 (270°) | £8-12 | 55g | Metal gear, high torque |
| Tilt servo | MG90S or MG996R | £4-8 | 13-55g | Depends on antenna weight |
| RF module (900 MHz) | LoRa SX1262 (Waveshare) | £12 | 8g | RSSI readout built-in, 10km range |
| RF module (2.4 GHz) | nRF24L01+PA+LNA | £5 | 10g | Higher bandwidth, shorter range |
| Directional antenna | 900 MHz Yagi (7-element) | £15-25 | 120g | ~12 dBi gain |
| OR: Patch antenna | 2.4 GHz patch array | £10-15 | 40g | ~14 dBi, flat profile |
| Gimbal frame | 3D printed (PETG) | £3 | 80g | Custom pan-tilt bracket |
| Battery | 2x 18650 Li-ion (3.7V 3000mAh) | £8 | 90g | ~22Wh, runs node for 12-24 hrs |
| Battery holder + BMS | TP4056 + boost converter | £3 | 15g | Charge via USB-C |
| Weatherproof case | IP65 junction box | £5 | 100g | For outdoor relay nodes |
| Solar panel (optional) | 6V 2W mini panel | £6 | 50g | Trickle charge for indefinite runtime |
| **Total per node** | | **£70-100** | **~500g** | |
| **3-node network** | | **£210-300** | | |

### Software Architecture

```
  ESP32-S3 FIRMWARE
  ═════════════════

  ┌─────────────────────────────────────────┐
  │              MAIN LOOP (100 Hz)         │
  │                                         │
  │  ┌─────────────┐  ┌─────────────────┐  │
  │  │ ANTENNA     │  │ MESH ROUTING    │  │
  │  │ TRACKER     │  │                 │  │
  │  │             │  │ Receive packets │  │
  │  │ Read RSSI   │  │ Route/forward   │  │
  │  │ Hill-climb  │  │ Retransmit      │  │
  │  │ Update      │  │                 │  │
  │  │ servos      │  │ Handle:         │  │
  │  │             │  │ - Data packets  │  │
  │  │ States:     │  │ - ACKs          │  │
  │  │ SEARCH      │  │ - Heartbeats    │  │
  │  │ TRACK       │  │ - Route updates │  │
  │  │ REACQUIRE   │  │                 │  │
  │  │ SPIRAL_SCAN │  │                 │  │
  │  └─────────────┘  └─────────────────┘  │
  │                                         │
  │  ┌─────────────┐  ┌─────────────────┐  │
  │  │ WiFi AP     │  │ TELEMETRY       │  │
  │  │             │  │                 │  │
  │  │ Local       │  │ RSSI logging    │  │
  │  │ devices     │  │ Servo angles    │  │
  │  │ connect     │  │ Battery voltage │  │
  │  │ to this     │  │ Link quality    │  │
  │  │ node's AP   │  │ Packet stats    │  │
  │  └─────────────┘  └─────────────────┘  │
  └─────────────────────────────────────────┘
```

### Hill-Climbing Implementation (Python-like pseudocode)

```python
class AntennaTracker:
    def __init__(self, pan_servo, tilt_servo, radio):
        self.pan = 90      # current pan angle (degrees)
        self.tilt = 45      # current tilt angle
        self.delta = 5.0    # step size (degrees)
        self.min_delta = 0.5
        self.max_delta = 15.0
        self.state = "SEARCH"
        self.best_rssi = -120  # dBm
        self.no_improve_count = 0

    def update(self):
        """Called at 10 Hz."""

        if self.state == "SEARCH":
            self._hill_climb_step()
            if self.best_rssi > -80:  # signal found
                self.state = "TRACK"
                self.delta = 2.0

        elif self.state == "TRACK":
            self._hill_climb_step()
            if self.best_rssi < -95:  # signal weakening
                self.state = "REACQUIRE"
                self.delta = 5.0
            elif self.no_improve_count > 20:
                self.delta = max(self.min_delta, self.delta * 0.8)
                self.no_improve_count = 0

        elif self.state == "REACQUIRE":
            self._hill_climb_step()
            if self.best_rssi > -80:
                self.state = "TRACK"
                self.delta = 2.0
            elif self.no_improve_count > 50:
                self.state = "SPIRAL_SCAN"
                self.scan_angle = 0

        elif self.state == "SPIRAL_SCAN":
            self._spiral_step()
            if self.best_rssi > -90:
                self.state = "TRACK"
                self.delta = 2.0

    def _hill_climb_step(self):
        """One iteration of hill climbing on both axes."""
        current_rssi = self.radio.get_rssi()
        improved = False

        # Try pan axis
        for direction in [+self.delta, -self.delta]:
            test_pan = self.pan + direction
            self.pan_servo.write(test_pan)
            time.sleep(0.05)  # settle time
            test_rssi = self.radio.get_rssi()

            if test_rssi > current_rssi + 0.5:  # 0.5 dB hysteresis
                self.pan = test_pan
                current_rssi = test_rssi
                improved = True
                break

        if not improved:
            self.pan_servo.write(self.pan)  # return to best

        # Try tilt axis (same logic)
        for direction in [+self.delta, -self.delta]:
            test_tilt = clamp(self.tilt + direction, 0, 90)
            self.tilt_servo.write(test_tilt)
            time.sleep(0.05)
            test_rssi = self.radio.get_rssi()

            if test_rssi > current_rssi + 0.5:
                self.tilt = test_tilt
                current_rssi = test_rssi
                improved = True
                break

        if not improved:
            self.tilt_servo.write(self.tilt)
            self.no_improve_count += 1
        else:
            self.no_improve_count = 0

        self.best_rssi = current_rssi

    def _spiral_step(self):
        """Expanding spiral scan to find lost signal."""
        self.scan_angle += 10  # degrees per step
        radius = self.scan_angle / 360 * 15  # expanding radius
        self.pan = 90 + radius * math.cos(math.radians(self.scan_angle))
        self.tilt = 45 + radius * math.sin(math.radians(self.scan_angle))
        self.pan_servo.write(self.pan)
        self.tilt_servo.write(self.tilt)
        time.sleep(0.1)
        self.best_rssi = self.radio.get_rssi()
```

### Advanced: Gradient Estimation (Faster Than Hill Climbing)

Hill climbing tests one direction at a time. A smarter approach estimates the gradient using simultaneous perturbation:

```
  SPSA (Simultaneous Perturbation Stochastic Approximation):
  ══════════════════════════════════════════════════════════

  Instead of testing pan and tilt separately (4 measurements per step),
  SPSA perturbs BOTH axes simultaneously with random ±δ:

  1. Generate random direction: Δ = [±1, ±1] (each axis random sign)
  2. Measure RSSI at [pan + δΔ₁, tilt + δΔ₂] → RSSI⁺
  3. Measure RSSI at [pan - δΔ₁, tilt - δΔ₂] → RSSI⁻
  4. Estimate gradient: ∇RSSI ≈ (RSSI⁺ - RSSI⁻) / (2δ) × [1/Δ₁, 1/Δ₂]
  5. Step: [pan, tilt] += α × ∇RSSI

  Only 2 measurements per step instead of 4!
  Converges faster in noisy environments (RSSI fluctuates).

  This is the same algorithm used in adaptive antenna arrays
  and satellite tracking systems.
```

---

## Part 2: FSO (Free-Space Optical) Laser Communication

### Why Laser Comms Are Interesting

```
  RF vs FSO COMPARISON
  ════════════════════

  RF (Radio):                    FSO (Laser):
  ├── Detectable by anyone       ├── Point-to-point, nearly invisible
  ├── Subject to jamming         ├── Very hard to jam
  ├── Regulated spectrum         ├── Unregulated (eye-safe lasers)
  ├── Wide beam = easy to aim    ├── Narrow beam = hard to intercept
  ├── Lower bandwidth            ├── VERY high bandwidth (Gbps possible)
  ├── Works in fog/rain          ├── Degrades in fog/rain
  └── Requires antenna gain      └── Requires precise pointing
      for long range                  (THIS IS YOUR SERVO PROJECT)
```

FSO laser comms are used by:
- Starlink (inter-satellite laser links)
- Facebook/Meta Connectivity (Project Aquila used laser backhaul)
- Military (DARPA, various classified programmes)
- ESA (inter-satellite optical links)

At student scale, you can build a working laser comms link for £50-100.

### Design Concept

```
  FSO LASER LINK
  ══════════════

  NODE A                                              NODE B
  ┌─────────────────┐         1-5 km              ┌─────────────────┐
  │  LASER TX       │  ◄──── line of sight ────►  │  LASER TX       │
  │  (650nm diode,  │                              │  (650nm diode,  │
  │   5mW, Class 3R)│                              │   5mW, Class 3R)│
  │                 │                              │                 │
  │  PHOTODIODE RX  │                              │  PHOTODIODE RX  │
  │  (BPW34 or      │                              │  (BPW34 or      │
  │   SFH213, with  │                              │   SFH213, with  │
  │   650nm filter) │                              │   650nm filter) │
  │                 │                              │                 │
  │  ┌───────────┐  │                              │  ┌───────────┐  │
  │  │ 2-AXIS    │  │  Servo gimbal + hill-climb   │  │ 2-AXIS    │  │
  │  │ GIMBAL    │  │  aims laser at receiver       │  │ GIMBAL    │  │
  │  │ (servos)  │  │  on the other end             │  │ (servos)  │  │
  │  └───────────┘  │                              │  └───────────┘  │
  │                 │                              │                 │
  │  ESP32-S3       │                              │  ESP32-S3       │
  │  modulates laser│                              │  modulates laser│
  │  at 1-10 Mbps   │                              │  at 1-10 Mbps   │
  └─────────────────┘                              └─────────────────┘
```

### How It Works

1. **Transmitter:** A laser diode (650nm red, or 850nm IR for less visibility) is modulated by turning it on/off at high speed (OOK — On-Off Keying). The ESP32's RMT peripheral can generate signals at up to 40 MHz, but practical data rates are 1-10 Mbps with simple OOK.

2. **Receiver:** A photodiode (BPW34 silicon PIN diode, or SFH213 for faster response) converts received light to current. A transimpedance amplifier (TIA) converts current to voltage. A comparator or ADC on the ESP32 recovers the digital signal.

3. **Pointing:** This is where the hill-climbing gimbal becomes CRITICAL. The laser beam divergence at 1km with a simple collimating lens is about 1-5 mrad (0.06-0.3°). The gimbal must point within this cone. The tracking algorithm uses the received signal strength on the photodiode as the RSSI equivalent — hill-climb to maximise received optical power.

4. **Acquisition:** Initial alignment uses a wider-divergence beacon (LED or defocused laser) to establish rough pointing, then switches to the narrow-beam laser for data.

### FSO Bill of Materials (Per End)

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Laser diode | 650nm 5mW (Class 3R) | £3 | Red, visible for alignment. Or 850nm IR for covert |
| Collimating lens | Glass lens, 10mm focal length | £2 | Narrows beam to ~1 mrad divergence |
| Photodiode | BPW34 (silicon PIN) | £1 | Sensitive at 650nm, fast response |
| Optical bandpass filter | 650nm ±10nm | £5 | Rejects ambient light (critical for daytime) |
| Focusing lens (RX) | 25mm diameter, 50mm focal | £3 | Collects light onto photodiode |
| Transimpedance amplifier | OPA380 or LTC6268 | £4 | Converts photodiode current to voltage |
| Comparator | LM393 or TLV3501 | £1 | Recovers digital signal |
| Pan servo | MG996R | £8 | Same as RF tracker |
| Tilt servo | MG996R | £8 | |
| ESP32-S3 | DevKit | £8 | Modulation + demodulation + tracking |
| 3D printed gimbal + mount | PETG | £3 | Holds optics and servos |
| Power supply | 2x 18650 + BMS | £8 | |
| PCB / protoboard | Custom or perfboard | £5 | TIA + comparator circuit |
| **Total per end** | | **~£60** | |
| **Complete link (2 ends)** | | **~£120** | |

### Pointing Accuracy Requirement

```
  BEAM DIVERGENCE vs RANGE
  ════════════════════════

  With a 10mm collimating lens and 650nm laser:
  Beam divergence ≈ 1.2 × λ / D = 1.2 × 0.00065 / 0.01 = 0.078 rad

  Wait — that's the diffraction limit for a 10mm aperture.
  In practice with a cheap laser diode + lens: ~1-3 mrad (0.06-0.17°)

  At 1 km range with 2 mrad divergence:
  Beam diameter = 1000 × 0.002 = 2 metres

  So the gimbal needs to point within ±1 metre at 1 km = ±1 mrad = ±0.06°

  Servo resolution:
  - MG996R: ~0.1° per step (with PWM at 1µs resolution)
  - With 16-bit PWM on ESP32: ~0.005° per step
  - 0.005° = 0.087 mrad → MORE than enough precision

  Conclusion: standard hobby servos CAN achieve the pointing accuracy
  needed for a 1km laser link. The hill-climbing algorithm handles
  the fine alignment.
```

### Data Rates Achievable

| Modulation | Rate | Complexity | Notes |
|------------|------|-----------|-------|
| OOK (On-Off Keying) | 1-10 Mbps | Low | ESP32 RMT peripheral, simple comparator |
| PPM (Pulse Position) | 1-5 Mbps | Medium | Better power efficiency, more complex timing |
| OFDM (optical) | 10-100 Mbps | High | Requires fast ADC + DSP, beyond ESP32 |

**1-10 Mbps OOK is achievable with £60 of components.** That's enough for SSH, web browsing, and even compressed video streaming.

### Weather Limitations

```
  ATMOSPHERIC EFFECTS ON FSO
  ══════════════════════════

  Condition              Attenuation (dB/km)    Link at 1km?
  ──────────────────────────────────────────────────────────
  Clear air              0.2-0.5                YES ✓
  Light haze             1-3                    YES ✓
  Light rain (2mm/hr)    3-6                    YES (reduced margin)
  Moderate rain (10mm)   6-10                   MARGINAL
  Heavy rain (25mm)      10-20                  NO ✗
  Light fog (vis 1km)    10-15                  NO ✗
  Dense fog (vis 200m)   50+                    NO ✗
  Snow (moderate)        5-15                   MARGINAL

  MITIGATION: Have RF backup link (LoRa) for when FSO fails.
  The system automatically falls back to RF in bad weather.
```

### Why This Is a Brilliant Project

```
  SKILLS DEVELOPED                      UNI/CAREER RELEVANCE
  ════════════════                      ════════════════════
  Control theory (hill climbing,        Core EE module at every uni
  PID, gradient estimation)

  RF engineering (link budget,          Telecoms, satellite, defence
  antenna gain, path loss)

  Optical engineering (laser            Photonics, fibre optics,
  divergence, photodetector             satellite laser comms
  physics, TIA design)

  Embedded systems (ESP32,              Every EE/CS job
  real-time control, PWM, ADC)

  PCB design (TIA circuit,              Hardware engineering
  analogue + digital mixed signal)

  Signal processing (OOK                DSP, communications
  demodulation, noise filtering,
  clock recovery)

  Mesh networking (routing,             Network engineering,
  topology management)                  distributed systems

  3D CAD (gimbal design)                Mechanical/systems engineering

  ALL of this goes in your UCAS personal statement.
  ALL of it transfers to the drone comms relay project.
```

---

## Part 3: Hybrid System — RF + FSO with Automatic Fallback

The optimal design combines both:

```
  HYBRID NODE
  ═══════════

  ┌────────────────────────────────────────────┐
  │                                            │
  │  ┌──────────────┐    ┌──────────────────┐  │
  │  │ FSO LASER    │    │ RF (LoRa 900MHz) │  │
  │  │ TX + RX      │    │ with Yagi        │  │
  │  │ on gimbal    │    │ on same gimbal   │  │
  │  └──────┬───────┘    └────────┬─────────┘  │
  │         │                     │             │
  │         └────────┬────────────┘             │
  │                  │                          │
  │            ┌─────┴──────┐                   │
  │            │  2-AXIS    │                   │
  │            │  GIMBAL    │                   │
  │            │  (servos)  │                   │
  │            └─────┬──────┘                   │
  │                  │                          │
  │            ┌─────┴──────┐                   │
  │            │  ESP32-S3  │                   │
  │            │            │                   │
  │            │ Hill-climb │                   │
  │            │ tracker    │                   │
  │            │            │                   │
  │            │ Auto mode: │                   │
  │            │ FSO clear  │                   │
  │            │  weather   │                   │
  │            │ RF in fog/ │                   │
  │            │  rain      │                   │
  │            └────────────┘                   │
  │                                            │
  │  Battery: 2x 18650 (22 Wh)                │
  │  Solar: 6V 2W panel (outdoor nodes)        │
  │  WiFi AP: connect local devices            │
  │                                            │
  └────────────────────────────────────────────┘

  AUTOMATIC FALLBACK:
  ═══════════════════

  if fso_link_quality > threshold:
      use FSO (1-10 Mbps, covert, undetectable)
  else:
      fall back to RF (50 kbps LoRa, works in any weather)

  Both links share the same gimbal — same tracking algorithm.
  FSO uses photodiode RSSI. RF uses LoRa RSSI.
```

## Development Sequence

```
  PHASE 1 (£30, 1-2 weeks):
  ├── Buy 2x ESP32-S3 + 2x LoRa SX1262 modules
  ├── Build basic point-to-point LoRa link (omnidirectional)
  ├── Verify bidirectional data transfer + RSSI readout
  └── Test range with stock antennas (should get 2-5km line of sight)

  PHASE 2 (£40, 1-2 weeks):
  ├── 3D print pan-tilt gimbal
  ├── Mount directional antenna (Yagi or patch)
  ├── Implement hill-climbing tracker in ESP32 firmware
  ├── Test: does the gimbal track and improve signal?
  └── Measure gain improvement: omni vs tracked directional

  PHASE 3 (£60, 2-3 weeks):
  ├── Build FSO laser TX/RX circuit (TIA + comparator)
  ├── Bench test: laser → photodiode → data recovery at 1m
  ├── Mount on gimbal, test at 10m, 100m, 1km
  ├── Implement OOK modulation/demodulation on ESP32
  └── Measure data rate and BER at distance

  PHASE 4 (£30, 1-2 weeks):
  ├── Build 3rd node (relay)
  ├── Implement mesh routing (store-and-forward)
  ├── Deploy: school → relay → home
  ├── Test end-to-end latency and throughput
  └── Add automatic FSO/RF fallback

  TOTAL: ~£160 and 6-8 weeks of weekend work
```

## Connection to Drone Comms Relay

Everything built here transfers directly:

| Ground Mesh Component | Drone Relay Equivalent |
|----------------------|----------------------|
| Hill-climbing servo tracker | Air-to-ground antenna tracking on drone |
| LoRa RF link | Drone-to-drone relay link |
| FSO laser link | Drone-to-ground high-bandwidth downlink |
| Mesh routing firmware | Multi-drone relay chain routing |
| ESP32 node | Drone companion computer comms subsystem |
| Auto RF/FSO fallback | Weather-adaptive link management |

The ground mesh is the drone comms relay without the flying part. Master it on the ground, then put it in the air.
