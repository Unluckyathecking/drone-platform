# Distributed Radar Swarm: Research Findings

## Overview

This document summarises research conducted via NotebookLM on the feasibility of using a swarm of 45 cheap microdrones (130x130mm tileable quadcopters, ~180g, ~£50 each) as a distributed radar array. The research explored coherent radar, MIMO, multistatic architectures, and practical sensor web design within the strict hardware constraints of the platform.

---

## 1. Three Distributed Radar Architectures

### 1a. Coherent Distributed Radar (Distributed Phased Array)
- All transmitters share a perfectly synchronised master clock and emit the same waveform
- Physical radio waves constructively interfere in the air to form a focused beam
- **Verdict: IMPOSSIBLE with cheap hardware**
- At 77 GHz (TI IWR6843), the wavelength is ~4 mm
- Requires sub-millimeter relative positioning and picosecond clock synchronisation
- The u-blox MAX-M10S GPS on the microdrone only provides 1.5 m accuracy — off by a factor of ~1,000

### 1b. MIMO Radar (Orthogonal Waveforms)
- Each transmitter sends a unique, mathematically orthogonal waveform
- Receivers separate the combined returns to form a "virtual array" in software
- **Verdict: IMPRACTICAL across a swarm**
- The TI IWR6843 uses MIMO internally (on its own chip), but distributed inter-drone MIMO requires sharing raw digitised RF data
- The ESP32-based mesh network supports only ~1-2 Mbps — far too little for raw radar streaming
- The 23-byte TDMA slot per drone is designed for processed telemetry, not raw waveforms

### 1c. Multistatic Radar (Spatial Diversity / Triangulation)
- Transmitters and receivers are dispersed; each processes returns locally
- Targets are localised by combining processed detections from multiple angles
- **Verdict: THE ONLY ACHIEVABLE ARCHITECTURE**
- Each drone detects targets independently within its 50-150 m range
- Shares a compact 23-byte state vector (position, velocity, target data) over the TDMA mesh
- Triangulation from multiple angles defeats stealth shaping and improves spatial coverage

---

## 2. Synchronisation Requirements

| Architecture | Position Accuracy Needed | Clock Sync Needed | Achievable on Microdrone? |
|---|---|---|---|
| Coherent (phased array) | Sub-millimeter | Picoseconds | No |
| MIMO (virtual array) | Centimeter | Nanoseconds | No |
| Multistatic (triangulation) | 1-2 metres | Milliseconds | Yes |

### GPS-Disciplined Clocks
- GPS PPS (Pulse Per Second) output provides ~10-50 nanosecond timing accuracy
- Adequate for LiDAR timestamping and TDMA slot synchronisation
- Thousands of times too slow for coherent beamforming at 77 GHz

### Chip-Scale Atomic Clocks (CSACs)
- Weight: ~35 g; Power: ~120 mW; Cost: ~$3,000-5,000 per unit
- Completely impractical on a 180 g, £50 expendable drone
- The entire avionics stack currently weighs 13.0 g

---

## 3. Self-Calibration via Radar Pings

A theoretically elegant trick: drones ping each other with their radar to measure inter-node distances to sub-millimeter precision, building a floating relative coordinate system that bypasses GPS error.

**Status: Physically valid but computationally impossible on current hardware**

- The ESP32-C3 lacks DSP capability for continuous cross-correlation algorithms
- The 23-byte TDMA slot has zero spare bandwidth for calibration data
- Adding a capable processor (RPi/Jetson) breaks weight, cost, and power budgets

---

## 4. What 77 GHz Radar Can and Cannot Detect

### Can Detect (Above Surface)
- **People**: Walking, running, crawling — each has a distinct micro-Doppler signature
- **Vehicles**: Wheeled vs tracked distinguishable by tire/track micro-Doppler
- **Drones**: Spinning propellers create unique high-frequency Doppler flashes
- **Animals**: Dogs, livestock distinguishable from humans by gait signatures

### Cannot Detect (Below Surface)
- **Buried objects, landmines, tunnels: IMPOSSIBLE at 77 GHz**
- Ground-penetrating radar (GPR) requires frequencies of 10 MHz to 3 GHz
- At 77 GHz (4 mm wavelength), waves bounce off the ground surface with zero penetration
- GPR antennas must be proportional to wavelength — far too large for a 130x130 mm drone

---

## 5. Micro-Doppler Classification

### The Capability
- 77 GHz mmWave radar detects micro-movements of target components (limbs, wheels, propellers)
- By generating time-velocity spectrograms, a machine learning model can classify target type
- A swarm could maintain a signature library: walking person, crawling person, dog, wheeled vehicle, tracked vehicle, drone

### The Processing Bottleneck
- Generating spectrograms requires continuous FFTs — heavy DSP work
- The ESP32-C3 (mesh radio chip) cannot handle this at all
- The TI IWR6843 requires an external RPi/Jetson for classification
- **Solution: Use radar chips with integrated DSP (see Section 7)**

---

## 6. Optimal Practical Mission: Persistent Multistatic Tripwire

Given all hardware constraints, the best achievable mission is a **7-day persistent area saturation sensor web**.

### Grid Geometry
- 45 drones landed in a semi-uniform grid with ~100 m spacing
- Voronoi tessellation algorithm (SPREAD behaviour) ensures even distribution
- Total coverage area: ~1.5 km^2 with overlapping radar fields

### Detection Logic
- TI IWR6843 internally generates a basic point cloud of moving targets
- ESP32-C3 reads a simple threshold trigger via UART (object above minimum RCS and velocity)
- ESP32 calculates approximate global coordinates by adding radar range/angle to GPS position

### Data Flow (23-Byte TDMA Slot)
| Field | Bytes | Content |
|---|---|---|
| Drone ID | 1 | Node identifier |
| GPS Position | 8 | Target lat/lon as int32 offsets |
| Altitude | 2 | cm resolution |
| Velocity Vector | 6 | vx/vy/vz in cm/s |
| Battery Voltage | 1 | 0.1V resolution |
| Status Flags | 1 | Target detected flag |
| Sensor Data | 4 | Target size/RCS estimate |

### Operator Display
- Satellite map with 45 green dots (landed swarm nodes)
- Red target icon appears when any node detects movement
- Track line shows target path through the grid with heading arrow
- Multiple overlapping detections provide sensor-fused tracking

### Tracking Accuracy
- Individual node: ~3-5 m (limited by 1.5 m GPS error + radar angle uncertainty)
- Sensor-fused (3-4 overlapping nodes): ~2-3 m
- Sub-meter tracking requires RTK GPS (u-blox ZED-F9P, ~£190) — breaks budget

---

## 7. The Key Insight: Edge-AI Radar Chips

The single most impactful upgrade is replacing the standard TI IWR6843 with a radar chip that has **integrated DSP and on-chip machine learning inference**.

### Candidate Chips
| Chip | Key Feature | Approx. Cost |
|---|---|---|
| TI AWR2544 | Integrated DSP, on-chip processing | £25-40 |
| Infineon BGT60TR13C | Gesture-resolution micro-movement detection | £20-35 |
| Standard TI IWR6843 | External processing required | £40-65 |

### Why This Matters
- The radar chip itself runs FFTs and neural network inference on-chip
- Outputs a simple serial message to ESP32: `{"target": "TRACKED_VEHICLE", "confidence": 0.92}`
- ESP32 packs a 1-byte classification code into the 23-byte TDMA slot
- **No weight, power, or cost penalty** — the chip swap adds zero grams
- Maintains 7-day landed persistence (no power-hungry companion computer)
- Potentially cheaper than the baseline IWR6843

### What This Unlocks
- On-chip micro-Doppler classification (person/vehicle/drone/animal)
- Confidence scores per detection
- The swarm becomes an intelligent classified sensor web, not just a tripwire

---

## 8. Existing Programs and State of the Art

### Demonstrated
- **PERDIX**: 103-drone swarm demonstrated in 2017 (fixed-wing, 290 g)
- **MIT Lincoln Laboratory**: Flight-tested distributed coherent apertures using defence-grade payloads with proprietary wireless microwave time-transfer (picosecond sync achieved)
- **Multistatic networks**: Academic and commercial flight tests using drones as scattered independent receivers with geometric triangulation

### Theoretical / Simulated Only
- Most academic MIMO distributed radar papers are simulation-only
- Coherent beamforming on small UAVs remains confined to tier-one defence labs
- DARPA OFFSET program explores swarm tactics but not specifically distributed radar arrays

### Key Gap
- Nobody has demonstrated distributed coherent radar on expendable, COTS-based drone swarms
- The gap between MIT Lincoln Lab's defence-grade flight tests and a £50 microdrone is enormous
- Multistatic (non-coherent) approaches are the realistic path forward

---

## 9. Five Engineering Takeaways (Ranked by Actionability)

1. **Exploit "Land and Listen" persistence** — Transform 4-minute flyers into 7-day ground sensors by landing the swarm and cutting motor power (50 W to 0.3 W)

2. **Compress all data to 23 bytes** — Design every detection algorithm around the 23-byte TDMA slot constraint; process locally, transmit only conclusions

3. **Shift DSP to the radar chip** — Source smart radar modules with integrated hardware DSP; avoid adding companion computers that break weight/cost/power budgets

4. **Abandon coherent beamforming** — Embrace multistatic spatial diversity; scatter drones for overlapping coverage and use network-level sensor fusion for tracking

5. **Ruthlessly hold the £50 per-node cost** — The swarm's tactical value is expendability and area saturation; resist upgrading individual nodes at the expense of swarm scale

---

## 10. Implications for Platform Design

### For the Tileable Microdrone (29-Tileable-Microdrone-Design.md)
- The 130x130mm form factor is well-suited for ground-based radar sensor web deployment
- The 45-drone packing in a 500x500x200mm bay maps perfectly to the optimal grid geometry
- The TDMA mesh protocol (Section 7.2 of that document) is already designed for exactly this data flow
- Consider adding a radar chip with integrated DSP to the optional sensor payload list (alongside OV2640, MLX90640, etc.)

### For the Tube-Packaged Design (29-Tube-Packaged-Folding-Wing-Design.md)
- Fixed-wing variants are less suited for landed radar web missions (cannot hover to precise landing points)
- However, the MICRO tube variant could deploy radar-equipped tileable microdrones from sonobuoy tubes
- The MINI tube variant (with its heavier payload budget) could carry an IWR6843 + Jetson for airborne radar processing during transit, then the tileable microdrones handle persistent ground coverage

### Recommended Next Steps
1. Prototype a single-node radar detection system: ESP32-C3 + TI IWR6843 eval board, test detection range and basic target classification
2. Evaluate the TI AWR2544 for on-chip classification capability vs the standard IWR6843
3. Build a 3-node multistatic triangulation demonstrator to validate tracking accuracy
4. Design the 23-byte detection message format and integrate with the existing TDMA protocol
5. Simulate the full 45-node grid in software before committing to hardware

---

*Research conducted 2026-03-25 via NotebookLM deep conversation with the "Drone Platform - Engineering Specifications" notebook. Conversation saved as notebook note.*
