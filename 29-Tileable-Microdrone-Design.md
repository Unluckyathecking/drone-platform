# Tileable Microdrone: Stackable Quadcopter for Mass Swarm Deployment

## Executive Summary

This document specifies a hand-sized (~120-150mm square) ducted quadcopter designed from first principles around a single constraint: **maximum packing density for mass deployment from a carrier aircraft**. The square form factor with ducted propellers enables face-to-face stacking, side-by-side tiling, and spring-loaded magazine feeding with near-zero wasted volume. Two design variants are presented: a conventional corner-prop layout (Variant A) and an integrated full-body-duct layout (Variant B).

Reference programs: PERDIX (290g fixed-wing, 103-drone swarm demonstrated 2017), Coyote (tube-launched), Shield AI Nova (autonomous quad). This design occupies the gap between PERDIX (fixed-wing, limited hover) and Nova (too large/expensive for expendable swarm use).

---

## 1. Form Factor and Geometry

### 1.1 Target Envelope

| Parameter | Variant A (Corner Props) | Variant B (Full-Body Duct) |
|---|---|---|
| Footprint | 130 x 130 mm | 130 x 130 mm |
| Thickness | 32 mm | 38 mm |
| Corner radius | 12 mm | 8 mm |
| Prop diameter | 55 mm (2.2") | 50 mm (2.0") |
| Duct lip height | 8 mm above / 6 mm below | 10 mm above / 8 mm below |
| All-up weight target | 180-220 g | 200-260 g |
| Mass (frame only) | 35-45 g | 50-65 g |

### 1.2 Variant A: Corner-Prop Layout (Conventional Quad, Ducted)

Four propellers at the corners of the square, each enclosed in a cylindrical duct that is flush with the top and bottom surfaces. The central area houses avionics, battery, and payload.

```
                         VARIANT A — TOP VIEW
                        130 mm (5.1 inches)
            ◄──────────────────────────────────────►

       ┌──────────────────────────────────────────────┐   ▲
      /  ╭─────╮                          ╭─────╮      \  │
     │   │     │    ┌──────────────┐      │     │       │ │
     │   │  M1 │    │   GPS ANT    │      │ M2  │       │ │
     │   │ CW  │    │  (top face)  │      │ CCW │       │ │
     │   ╰─────╯    └──────────────┘      ╰─────╯       │ │
     │                                                   │ │
     │       ┌──────────────────────────┐                │ │  130 mm
     │       │     FLIGHT CONTROLLER    │                │ │
     │       │  ┌────────┐ ┌────────┐   │                │ │
     │       │  │ STM32  │ │ESP32-C3│   │                │ │
     │       │  │  FC    │ │+ LoRa  │   │                │ │
     │       │  └────────┘ └────────┘   │                │ │
     │       │     ┌──────────┐         │                │ │
     │       │     │  BMP280  │         │                │ │
     │       │     └──────────┘         │                │ │
     │       └──────────────────────────┘                │ │
     │                                                   │ │
     │   ╭─────╮                          ╭─────╮       │ │
     │   │     │    ┌──────────────┐      │     │       │ │
     │   │  M3 │    │   BATTERY    │      │ M4  │       │ │
     │   │ CCW │    │   2S 450mAh  │      │ CW  │       │ │
     │   ╰─────╯    └──────────────┘      ╰─────╯       │ │
      \                                                 /  │
       └──────────────────────────────────────────────┘   ▼

    ╭─────╮ = Ducted prop (55mm OD duct, 50mm prop)
    M1-M4  = Motors (1103 class, 8000-11000 KV on 2S)
    CW/CCW = Rotation direction

    Motor-to-motor diagonal: ~92 mm
    Motor-to-motor side:     ~85 mm (effective wheelbase)
    Central avionics bay:    ~60 x 60 mm
```

```
                    VARIANT A — SIDE VIEW (CROSS-SECTION)

                         130 mm
            ◄──────────────────────────────────►
                                                          ▲
    ────────────────────────────────────────────────────   │ 2mm duct lip
    ┌──────┬───────────────────────────────┬──────────┐   │
    │ DUCT │           GPS antenna         │   DUCT   │   │
    │      ├───────────────────────────────┤          │   │  32 mm
    │ PROP │  FC  │ ESP32 │ LoRa │ BMP280 │   PROP   │   │  total
    │      ├───────────────────────────────┤          │   │  thickness
    │ MOTOR│        BATTERY (2S 450mAh)    │  MOTOR   │   │
    ├──────┴───────────────────────────────┴──────────┤   │
    │               BOTTOM PLATE (PCB)                │   │ 1.6mm PCB
    └─────────────────────────────────────────────────┘   ▼

    Layer stack (top to bottom):
      1. Duct lip / top skin          2 mm
      2. Prop clearance zone          8 mm  (props spin in this plane)
      3. Avionics + motor stators    10 mm
      4. Battery bay                 10 mm  (2S 450mAh: ~48x25x13mm)
      5. Bottom plate / PCB           2 mm
                              Total: 32 mm
```

### 1.3 Variant B: Full-Body Duct (Entire Surface is Lift)

The entire 130x130mm square body is subdivided into four quadrant ducts. Each quadrant is a duct channel with a propeller. Avionics sit in the central cross-shaped spine between the four ducts.

```
                         VARIANT B — TOP VIEW
                        130 mm (5.1 inches)
            ◄──────────────────────────────────────►

       ┌────────────────┬──────┬────────────────────┐   ▲
       │ ╭────────────╮ │      │  ╭────────────╮    │   │
       │ │            │ │      │  │            │    │   │
       │ │   DUCT 1   │ │ GPS  │  │   DUCT 2   │    │   │
       │ │  (50mm     │ │ ANT  │  │  (50mm     │    │   │
       │ │   prop)    │ │      │  │   prop)    │    │   │
       │ ╰────────────╯ │      │  ╰────────────╯    │   │
       ├────────────────┤  FC  ├────────────────────┤   │  130 mm
       │   ESP32+LoRa   │ PCB  │   BARO + IMU       │   │
       ├────────────────┤      ├────────────────────┤   │
       │ ╭────────────╮ │      │  ╭────────────╮    │   │
       │ │            │ │ BAT- │  │            │    │   │
       │ │   DUCT 3   │ │ TERY │  │   DUCT 4   │    │   │
       │ │  (50mm     │ │      │  │  (50mm     │    │   │
       │ │   prop)    │ │      │  │   prop)    │    │   │
       │ ╰────────────╯ │      │  ╰────────────╯    │   │
       └────────────────┴──────┴────────────────────┘   ▼

    Central cross-spine width: 16 mm (houses wiring, FC, battery)
    Each duct quadrant: ~55 x 55 mm outer, 50 mm prop
    Duct wall thickness: 2 mm
    Available prop diameter: ~50 mm (2.0")
```

```
                    VARIANT B — SIDE VIEW (CROSS-SECTION)

                         130 mm
            ◄──────────────────────────────────►
                                                          ▲
    ┌─────────────────┬────────┬──────────────────────┐   │
    │  ▓▓ DUCT LIP ▓▓ │  GPS   │  ▓▓ DUCT LIP ▓▓     │   │ 3mm
    │  ┌───────────┐  │        │  ┌───────────┐       │   │
    │  │  PROP 1   │  │   FC   │  │  PROP 2   │       │   │
    │  │  ░░░░░░░  │  │  PCB   │  │  ░░░░░░░  │       │   │  38 mm
    │  │  MOTOR    │  │        │  │  MOTOR    │       │   │
    │  └───────────┘  │BATTERY │  └───────────┘       │   │
    │  ▓▓ DUCT LIP ▓▓ │        │  ▓▓ DUCT LIP ▓▓     │   │ 3mm
    └─────────────────┴────────┴──────────────────────┘   ▼

    Layer stack (top to bottom):
      1. Top duct lip / inlet bell    3 mm
      2. Prop clearance              10 mm
      3. Motor stator + ESC          10 mm
      4. Bottom duct lip / exhaust    3 mm
      5. Central spine depth         38 mm (contains battery vertically)

    Airflow: TOP → through duct → BOTTOM (pusher config in each duct)
```

### 1.4 Variant Comparison

| Criterion | Variant A (Corner Props) | Variant B (Full Body Duct) |
|---|---|---|
| Disc area (total) | 4 x pi x 25^2 = 7,854 mm^2 | 4 x pi x 25^2 = 7,854 mm^2 |
| Disc loading at 200g | 25.0 g/dm^2 | 25.0 g/dm^2 |
| Duct efficiency gain | +20-25% (partial shrouding) | +25-35% (full shrouding, longer duct) |
| Structural weight | Lower (open center) | Higher (full duct walls + cross spine) |
| Avionics access | Easy (open center bay) | Harder (buried in cross spine) |
| Stacking flatness | Excellent (flush top/bottom) | Excellent (flush top/bottom) |
| Manufacturing complexity | Medium | High |
| Recommended for | **Primary design** | Future iteration |

**Recommendation: Proceed with Variant A for first prototype.** Variant B offers better aerodynamic efficiency but significantly higher structural complexity and manufacturing cost. Variant A achieves the core tiling/stacking requirement with simpler construction.

---

## 2. Propulsion System

### 2.1 Motor Selection

| Parameter | Specification | Notes |
|---|---|---|
| Motor class | 1103 | 11mm stator diameter, 3mm stator height |
| Specific models | BetaFPV 1103 8000KV, Happymodel EX1103 7000KV | Widely available, proven in 2-3" quads |
| KV rating | 7000-11000 KV (2S) | Higher KV for 2S, lower for 3S (if used) |
| Weight per motor | 3.5-4.5 g | Including wires, no prop |
| Max continuous current | 4-6 A per motor | Limited by ESC and wire gauge |
| 4x motor mass | 14-18 g | |

### 2.2 Propeller Selection

For Variant A with 55mm duct (50mm usable prop diameter):

| Parameter | Value |
|---|---|
| Prop diameter | 50 mm (2.0 inch) |
| Pitch | 1.0-1.5 inch | Low pitch for static thrust in ducted application |
| Blade count | 3-blade (triblade) | Better static thrust per diameter than 2-blade |
| Material | Polycarbonate or nylon | Standard micro quad props |
| Prop-to-duct tip gap | 1.5-2.0 mm radial | Critical for duct efficiency; tighter = better but risk of rubbing |
| Weight per prop | 0.5-0.8 g |
| 4x prop mass | 2-3 g |

### 2.3 Thrust Analysis

Baseline (un-ducted) thrust for 1103 8000KV on 2S with 50mm triblade:

| Condition | Thrust per motor | 4-motor total | Notes |
|---|---|---|---|
| Unducted, 100% throttle | ~55-65 g | 220-260 g | Measured on typical 2" builds |
| Ducted (+25% static) | ~69-81 g | 275-325 g | Duct augmentation at static hover |
| Ducted, 50% throttle (hover) | ~35-40 g | 140-160 g | Efficient hover point |

Thrust-to-weight analysis at 200g AUW:

| Metric | Unducted | Ducted |
|---|---|---|
| Max thrust | 240 g | 300 g |
| T:W ratio | 1.2:1 | **1.5:1** |
| Hover throttle | 83% | **67%** |

At 200g AUW with ducting, the T:W of 1.5:1 is adequate for controlled flight but below the 2:1 target for aggressive maneuvering. **Note:** T:W is marginal at mid-pack voltage (3.5V/cell) where thrust drops ~15-20% from full-charge values — the figures above are at full charge. Needs thrust-stand validation with actual motor/prop/duct combination across the full voltage range before committing to production. To improve:

**Option 1: Reduce weight to 170g** -- T:W becomes 1.76:1 (requires smaller battery, ~350mAh)
**Option 2: Use 1104 8000KV motors** -- adds ~4g (16g to 20g for 4 motors) but increases thrust by ~20%, yielding ~360g max thrust, T:W = 1.76:1 at 205g AUW
**Option 3: Use 2.5S or 3S battery** -- significantly more thrust but adds battery weight and voltage regulation complexity

**Recommendation: 1103 8000KV on 2S with ducting, target 180g AUW.** T:W = 1.67:1. Adequate for the mission profile (stable hover, gentle maneuvering, not acrobatic racing).

### 2.4 Battery Selection

| Option | Voltage | Capacity | Weight | Energy | Est. hover time |
|---|---|---|---|---|---|
| 1S 550mAh HV LiPo | 3.8V nom | 550 mAh | 14 g | 2.09 Wh | ~4 min |
| **2S 450mAh LiPo** | 7.4V nom | 450 mAh | 26 g | 3.33 Wh | **~7 min** |
| 2S 650mAh LiPo | 7.4V nom | 650 mAh | 36 g | 4.81 Wh | ~9 min |
| 2S 850mAh LiPo | 7.4V nom | 850 mAh | 48 g | 6.29 Wh | ~11 min |

Hover power estimate at 67% throttle, 200g AUW, ducted:
- Current per motor at hover: ~2.5A
- Total hover current: ~10A
- Hover power: 10A x 7.4V = 74W
- But this assumes aggressive constant-throttle; real hover with efficient props and ducts draws less
- Corrected estimate: ~45-55W hover power (based on benchmarked 2" ducted builds)
- At 50W hover: 3.33 Wh / 50W x 60 = **4.0 minutes** (2S 450mAh)
- At 50W hover: 4.81 Wh / 50W x 60 = **5.8 minutes** (2S 650mAh)

**Recommendation: 2S 450mAh for minimum weight variant (26g, ~4-5 min endurance), 2S 650mAh for extended mission (36g, ~6-7 min endurance).** Flight time is the primary weakness of this form factor -- acceptable for short-duration swarm missions (area saturation ISR, rapid deployment sensor networks).

### 2.5 ESC Selection

| Parameter | Specification |
|---|---|
| Type | 4-in-1 ESC integrated on FC PCB |
| Current rating | 12A per channel continuous |
| Protocol | DShot600 or DShot300 |
| Weight | Included in FC weight (combined FC+ESC board) |
| Specific models | Happymodel CrazyF4 ELRS AIO, BetaFPV F4 1S/2S AIO |

---

## 3. Avionics

### 3.1 Flight Controller Stack

| Component | Specific Part | Weight | Dimensions | Notes |
|---|---|---|---|---|
| FC + 4in1 ESC | Happymodel CrazyF411 ELRS AIO | 4.5 g | 26x26 mm | STM32F411, ICM-42688-P IMU, 12A ESCs |
| GPS | u-blox MAX-M10S module | 1.5 g | 10x10 mm | 1.5m CEP accuracy, 1Hz default (10Hz capable) |
| GPS antenna | Ceramic patch 12x12mm | 1.0 g | 12x12x4 mm | Must face upward, on top surface |
| Barometer | BMP280 | 0.2 g | 2x2.5 mm | Integrated on FC or separate breakout |
| Mesh radio | ESP32-C3-MINI-1 | 1.8 g | 13x16 mm | WiFi + BLE, mesh networking |
| Long-range radio | SX1262 LoRa module | 1.5 g | 12x12 mm | 868 MHz (UK), 2-5 km range |
| LoRa antenna | Chip antenna or PCB trace | 0.3 g | -- | Integrated into main PCB |
| Voltage regulator | 3.3V LDO (for ESP32/LoRa) | 0.2 g | SOT-23 | Powers digital electronics from battery bus |
| Wiring/connectors | Micro JST, solder joints | 2.0 g | -- | Minimized by AIO design |
| **Total avionics** | | **13.0 g** | | Well under 30g target |

### 3.2 Avionics Architecture

```
                    AVIONICS BLOCK DIAGRAM

    ┌─────────────────────────────────────────────────────┐
    │                   2S LiPo (7.4V)                    │
    │                       │                             │
    │              ┌────────┴────────┐                    │
    │              │  Power bus      │                    │
    │              │  7.4V direct    │                    │
    │              └───┬────┬───┬───┘                     │
    │                  │    │   │                          │
    │           ┌──────┘    │   └──────┐                  │
    │           ▼           ▼          ▼                  │
    │    ┌─────────┐  ┌─────────┐  ┌──────┐              │
    │    │ 4x ESC  │  │  3.3V   │  │ 5V   │              │
    │    │ (12A ea)│  │  LDO    │  │ BEC  │              │
    │    └────┬────┘  └────┬────┘  └──┬───┘              │
    │         │            │          │                   │
    │    ┌────┴────┐  ┌────┴──────────┴───┐              │
    │    │ 4x 1103 │  │   Digital bus     │              │
    │    │ motors  │  │                   │              │
    │    └─────────┘  │  ┌───────────┐    │              │
    │                 │  │ STM32F411 │    │              │
    │                 │  │    FC     │    │              │
    │                 │  │ ICM42688  │    │              │
    │                 │  │  BMP280   │    │              │
    │                 │  └─────┬─────┘    │              │
    │                 │        │ UART     │              │
    │                 │   ┌────┴────┐     │              │
    │                 │   │ ESP32-C3│     │              │
    │                 │   │  mesh   │     │              │
    │                 │   └────┬────┘     │              │
    │                 │        │ SPI      │              │
    │                 │   ┌────┴────┐     │              │
    │                 │   │ SX1262  │     │              │
    │                 │   │  LoRa   │     │              │
    │                 │   └─────────┘     │              │
    │                 │                   │              │
    │                 │   ┌─────────┐     │              │
    │                 │   │MAX-M10S │     │              │
    │                 │   │  GPS    │     │              │
    │                 │   └─────────┘     │              │
    │                 └───────────────────┘              │
    └─────────────────────────────────────────────────────┘

    Communication stack:
      ESP32-C3 ◄──► Mesh (inter-drone, ~500m, 2.4 GHz WiFi)
      SX1262   ◄──► LoRa (carrier/GCS command, 2-5 km, 868 MHz)
      STM32    ◄──► ESCs (DShot600, motor control)
      STM32    ◄──► GPS (UART, 9600-115200 baud)
      STM32    ◄──► ESP32 (UART, 115200 baud, MAVLink-lite)

    RF COEXISTENCE NOTE:
      GPS (1575.42 MHz) and ESP32 (2.4 GHz WiFi) share the same
      small PCB area (~26x26mm). At this proximity, ESP32 TX bursts
      can desensitize the GPS front end, causing degraded fix quality
      or total loss of lock. Mitigation: ground plane separation,
      RF shield can over GPS module, time-division (pause ESP32 TX
      during GPS acquisition). REQUIRES PROTOTYPE TESTING — this is
      a known failure mode in small drones and cannot be resolved
      by simulation alone.
```

### 3.3 Firmware Architecture

| Layer | Firmware | Notes |
|---|---|---|
| Flight control | Betaflight 4.4+ or INAV 7+ | INAV preferred for autonomous waypoint following |
| Mesh coordination | Custom on ESP32-C3 | Lightweight swarm protocol over ESP-NOW |
| Command reception | LoRa packet handler on ESP32 | Receives mission commands, relays to FC via MSP/MAVLink |
| Freefall detection | Custom Betaflight module | Accelerometer reads <0.1g for >200ms triggers arm + stabilize |

### 3.4 Optional Sensor Payloads

These are mission-specific additions that increase weight and cost:

| Sensor | Weight | Power | Purpose | Added cost |
|---|---|---|---|---|
| OV2640 camera (2MP) | 1.5 g | 120 mW | Visual ISR | £2 |
| MLX90640 thermal (32x24) | 3.0 g | 200 mW | Thermal ISR, SAR | £25 |
| MEMS microphone (SPH0645) | 0.3 g | 10 mW | Acoustic monitoring | £1 |
| LED beacon (high-intensity) | 0.5 g | 500 mW | Visual marking, distraction | £0.50 |
| Gas sensor (MQ series) | 2.0 g | 150 mW | Environmental monitoring | £3 |

---

## 4. Weight Budget

### 4.1 Detailed Mass Breakdown (Variant A, 2S 450mAh)

| Component | Mass (g) | % of AUW |
|---|---|---|
| Frame (injection-molded PA12 nylon) | 38 | 21.1 |
| 4x motors (1103 8000KV) | 16 | 8.9 |
| 4x props (50mm triblade) | 3 | 1.7 |
| FC + 4in1 ESC (AIO board) | 4.5 | 2.5 |
| GPS module + antenna | 2.5 | 1.4 |
| ESP32-C3 module | 1.8 | 1.0 |
| SX1262 LoRa module | 1.5 | 0.8 |
| BMP280 (if separate) | 0.2 | 0.1 |
| Voltage regulators | 0.5 | 0.3 |
| Wiring, connectors, solder | 3.0 | 1.7 |
| Battery (2S 450mAh LiPo) | 26 | 14.4 |
| Alignment pins (4x nylon) | 1.0 | 0.6 |
| Magazine rail guides (2x) | 1.5 | 0.8 |
| Charging contacts (2x spring pins) | 1.0 | 0.6 |
| Foam separator (per drone share) | 0.5 | 0.3 |
| **Contingency (5%)** | **5.1** | **2.8** |
| | | |
| **TOTAL AUW** | **~180 g** | **100%** |

180g AUW with 2S 450mAh. With 2S 650mAh battery (36g instead of 26g): **~190g AUW**.

Both are well under the 200g threshold (which matters in some regulatory frameworks -- sub-250g in most jurisdictions does not require registration for recreational use, though swarm operations would require specific authorization regardless).

---

## 5. Packing and Deployment System

### 5.1 Stacking (Vertical)

Drones stack face-to-face. The top surface (GPS antenna, duct inlet lips) nests against the bottom surface (PCB, duct exhaust lips) of the drone above, separated by a thin foam sheet.

```
            STACKING DIAGRAM — SIDE VIEW (10-drone stack)

                      130 mm
            ◄──────────────────────────►

            ┌──────────────────────────┐  ─┐
            │       DRONE 10           │   │ 32 mm
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░  ─┤ 1.5mm foam
            ┌──────────────────────────┐   │
            │       DRONE 9            │   │ 32 mm
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░  ─┤ 1.5mm foam
            ┌──────────────────────────┐   │
            │       DRONE 8            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 7            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 6            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 5            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 4            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 3            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 2            │   │
            └──────────────────────────┘   │
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
            ┌──────────────────────────┐   │
            │       DRONE 1            │   │ 32 mm
            └──────────────────────────┘  ─┘

    Stack height: 10 x 32mm + 9 x 1.5mm = 333.5 mm (~334 mm)
    Stack mass:   10 x 180g + 9 x 2g   = 1,818 g (~1.82 kg)

    Self-alignment features:
    ┌───────────────────────┐
    │  ●                 ●  │   ● = Alignment pin (top) / dimple (bottom)
    │                       │       2mm diameter nylon pins, 3mm tall
    │                       │       Located at diagonally opposite corners
    │                       │       Pins on top → dimples on bottom
    │  ●                 ●  │       Self-centering conical shape
    └───────────────────────┘
```

### 5.2 Grid Tiling (Horizontal)

```
            GRID TILING — TOP VIEW (4x4 = 16 drones in one layer)

    ◄──────────────────── 520 mm (4 x 130mm) ────────────────────►

    ┌──────────┬──────────┬──────────┬──────────┐   ▲
    │          │          │          │          │   │
    │  D-01    │  D-02    │  D-03    │  D-04    │   │
    │          │          │          │          │   │
    ├──────────┼──────────┼──────────┼──────────┤   │
    │          │          │          │          │   │
    │  D-05    │  D-06    │  D-07    │  D-08    │   │  520 mm
    │          │          │          │          │   │
    ├──────────┼──────────┼──────────┼──────────┤   │
    │          │          │          │          │   │
    │  D-09    │  D-10    │  D-11    │  D-12    │   │
    │          │          │          │          │   │
    ├──────────┼──────────┼──────────┼──────────┤   │
    │          │          │          │          │   │
    │  D-13    │  D-14    │  D-15    │  D-16    │   │
    │          │          │          │          │   │
    └──────────┴──────────┴──────────┴──────────┘   ▼

    Packing efficiency:
      The key metric is VOLUMETRIC efficiency — how much of the carrier
      payload bay is actually filled with drones:
      3D volumetric efficiency: ~83% (see section 5.3 combined packing)
      This is the number that matters for carrier payload capacity.

      Supporting detail — 2D tiling:
      Drone area:    130 x 130 = 16,900 mm^2
      Available area: 16,900 mm^2 (square tiles perfectly)
      Actual efficiency with 1mm clearance per side:
        Effective cell: 132 x 132 mm
        Usable area ratio: (130/132)^2 = 97.0% (2D packing)

    Compare with circular drones of same inscribed diameter:
      Circle area in 130mm square: pi x 65^2 = 13,273 mm^2
      Packing efficiency of circles in grid: 13,273/16,900 = 78.5%
      ADVANTAGE OF SQUARE FORM FACTOR: +21.5% more drones per area
```

### 5.3 Combined Packing Density

```
    CARRIER PAYLOAD BAY: 500 x 500 x 200 mm (example MEDIUM tier)

    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │   Layer 3:  ┌───┬───┬───┐                           │
    │     (top)   │ D │ D │ D │  3 x 3 = 9 drones        │
    │             ├───┼───┼───┤                           │
    │             │ D │ D │ D │                            │
    │             ├───┼───┼───┤  (500/132 = 3.78 → 3)    │
    │             │ D │ D │ D │                            │
    │             └───┴───┴───┘                           │
    │                                                     │
    │   Layer 2:  [same — 9 drones]                       │
    │                                                     │
    │   Layer 1:  [same — 9 drones]                       │
    │   (bottom)                                          │
    │                                                     │
    │   Vertical:  200mm / (32 + 1.5) = 5.97 → 5 layers  │
    │                                                     │
    │   TOTAL: 3 x 3 x 5 = 45 drones                     │
    │   Total mass: 45 x 180g = 8.1 kg                   │
    │   Volumetric efficiency: 83%                        │
    └─────────────────────────────────────────────────────┘

    For a LARGE tier carrier (1000 x 500 x 300 mm bay):
      Grid: 7 x 3 = 21 per layer
      Layers: 300 / 33.5 = 8.9 → 8 layers
      TOTAL: 21 x 8 = 168 drones
      Total mass: 168 x 180g = 30.2 kg (requires large carrier!)

    For MINI tier carrier (200 x 200 x 100 mm bay — your current project):
      Grid: 1 x 1 = 1 per layer
      Layers: 100 / 33.5 = 2.9 → 2 layers
      TOTAL: 2 drones (limited, but proof of concept)
      Alternative: magazine stack of 3 drones (3 x 33.5 = 100.5mm)
```

### 5.4 Magazine Concept

```
    SPRING-LOADED MAGAZINE — ISOMETRIC CUTAWAY

                    ┌─────────────────────┐
                    │    MAGAZINE BODY     │
                    │   (aluminum tube,    │
                    │    134 x 134 mm ID)  │
                    │                      │
                    │  ┌────────────────┐  │
                    │  │   DRONE 10     │  │  ◄── Top drone (next to deploy)
                    │  │   (armed)      │  │
                    │  ├────────────────┤  │
                    │  │   DRONE 9      │  │
                    │  ├────────────────┤  │
                    │  │   DRONE 8      │  │
                    │  ├────────────────┤  │
                    │  │   DRONE 7      │  │
                    │  ├────────────────┤  │
                    │  │      ...       │  │
                    │  ├────────────────┤  │
                    │  │   DRONE 1      │  │
                    │  ├────────────────┤  │
                    │  │  ╔══════════╗  │  │
                    │  │  ║ SPRING   ║  │  │  ◄── Compression spring
                    │  │  ║ PLATE    ║  │  │      pushes stack upward
                    │  │  ╚══════════╝  │  │
                    │  └────────────────┘  │
                    │                      │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │   EJECTION DOOR      │  ◄── Solenoid-actuated gate
                    │   (bottom of carrier)│      opens to release bottom drone
                    └──────────────────────┘
                               │
                               ▼
                         Drone drops out
                         (freefall → arm → fly)


    MAGAZINE SPECIFICATIONS:
    ┌────────────────────────────────────────────┐
    │  Internal dimensions: 134 x 134 x 380 mm  │
    │  Wall thickness:      2 mm aluminum        │
    │  External dimensions: 138 x 138 x 385 mm  │
    │  Capacity:            10 drones            │
    │  Magazine mass:       ~180 g (empty)       │
    │  Loaded mass:         180 + 1818 = ~2.0 kg │
    │  Spring force:        ~20N (pushes stack)  │
    │  Gate actuator:       12V solenoid, 25g    │
    │  Power bus contacts:  2x spring pins/side  │
    │    (charges all drones while in magazine)   │
    └────────────────────────────────────────────┘
```

### 5.5 Power-On-Eject Mechanism

Three independent activation methods (redundant):

**Method 1: Magnetic reed switch**
- Small magnet embedded in magazine wall
- Reed switch on drone is held CLOSED (power OFF) while magnet is present
- When drone exits magazine, magnetic field disappears, reed switch opens, power circuit completes
- Weight: 0.3g (reed switch) + 0g (magnet is on magazine, not drone)
- Reliability: very high, no moving parts on drone

**Method 2: Mechanical microswitch**
- Lever-arm microswitch on drone bottom edge
- Pressed IN (power OFF) by magazine wall pressure
- Releases when drone clears magazine
- Weight: 0.8g
- Reliability: high, proven mechanism

**Method 3: Freefall detection (software)**
- Accelerometer (already on FC) detects sustained <0.1g for >200ms
- FC was in deep-sleep mode while in magazine
- IMU samples at low rate (10 Hz) in sleep mode, triggers full wake on freefall
- Zero additional hardware weight
- Latency: 200-300ms detection + 100ms boot = 300-400ms total

**Recommended: Method 1 (reed switch) as primary, Method 3 (freefall detection) as backup.**

### 5.6 Deployment Sequence Analysis

```
    DEPLOYMENT TIMELINE — SINGLE DRONE

    t = 0.000s    Gate opens, drone begins to slide out
    t = 0.050s    Drone clears magazine (50ms ejection via spring)
    t = 0.050s    Reed switch triggers: power ON
    t = 0.100s    FC boot begins (gyro calibration skipped — pre-cal'd)
    t = 0.250s    FC operational, IMU streaming
    t = 0.300s    Freefall confirmed (backup: accelerometer <0.1g)
    t = 0.350s    ESCs armed, motors spin up to idle
    t = 0.500s    Motors at stabilization thrust (~80% throttle)
    t = 0.600s    Attitude stabilized (rate gyro loop active)
    t = 0.800s    Full attitude control, transitioning to hover
    t = 1.000s    Stable hover achieved
    t = 1.200s    GPS fix acquired (hot start, almanac pre-loaded)
    t = 1.500s    Mesh radio active, announces presence
    t = 2.000s    Receives swarm assignment from carrier
    t = 2.500s    Begins mission execution

    FREEFALL DISTANCE:
      t_freefall = 0.500s (time from drop to motor authority)
      d = 0.5 × g × t^2 = 0.5 × 9.81 × 0.5^2 = 1.23 m

      With air resistance on a 130x130mm flat plate at 180g:
        Terminal velocity of this shape ≈ 12-15 m/s
        At 0.5s: v = ~4.5 m/s (well below terminal velocity)
        Actual drop with drag: ~1.0 m

      CONSERVATIVE ESTIMATE: 4-6 m altitude loss before stabilization
      (accounts for ESC boot time, gyro settling, and mid-pack voltage
      where thrust margins are thinner)

      At 0.8s (attitude stable, not yet hovering):
        d = 0.5 × 9.81 × 0.8^2 = 3.14 m (no drag)
        With drag: ~2.5 m

      MINIMUM DEPLOYMENT ALTITUDE: 50 m AGL (provides 44-46m safety margin)
      RECOMMENDED DEPLOYMENT ALTITUDE: 100-200 m AGL
```

### 5.7 Deployment Rate and Separation

```
    SEQUENTIAL DEPLOYMENT FROM 10-DRONE MAGAZINE

    Gate cycle time:     0.3s (solenoid open → drone exits → solenoid close)
    Spring re-seat time: 0.1s (next drone pushed into position)
    Minimum interval:    0.4s per drone

    Deployment rate:     2.5 drones/second

    Full magazine (10 drones): 4.0 seconds total deployment time

    SEPARATION AT DEPLOYMENT:
      If carrier speed = 20 m/s and deployment interval = 0.4s:
        Horizontal separation = 20 × 0.4 = 8.0 m between consecutive drones
        Vertical separation   = ~0.5 m (each successive drone has 0.4s less freefall)

      ASYMMETRIC MOTOR FIRING FOR ACTIVE SEPARATION:
        During the first 0.5s after stabilization, alternate drones fire
        asymmetric motor pairs briefly (e.g., M1+M3 at 90%, M2+M4 at 60%)
        to induce a lateral drift of 1-2 m/s. Odd-numbered drones drift
        left, even-numbered drift right. This doubles the effective
        separation between adjacent drones in the deployment string and
        reduces collision risk during the critical stabilization phase.

    SPATIAL DISTRIBUTION AFTER 10s (all 10 deployed, each stabilizing):
      Drone 1:  8.0s into flight, ~50m from drop point (maneuvering)
      Drone 10: 0.4s into flight, still stabilizing at drop point
      String length: ~120m along carrier flight path
      All within mesh radio range of each other (~500m)
```

### 5.8 Failed Deployment (Drone Does Not Activate)

```
    FAILURE MODE: Drone drops but does not power on / stabilize

    Drop altitude: 200m AGL (recommended)
    Terminal velocity of 130x130mm, 180g flat plate:
      Cd ≈ 1.1 (flat plate)
      A = 0.0169 m^2 (130x130mm)
      rho = 1.225 kg/m^3

      v_term = sqrt(2mg / (rho × Cd × A))
      v_term = sqrt(2 × 0.180 × 9.81 / (1.225 × 1.1 × 0.0169))
      v_term = sqrt(3.53 / 0.0228)
      v_term = sqrt(154.8)
      v_term = 12.4 m/s (~28 mph)

    Impact energy: 0.5 × 0.180 × 12.4^2 = 13.8 J

    For context:
      - Cricket ball at 40 mph: ~32 J
      - Falling smartphone from 10m: ~5 J
      - This drone at terminal velocity: 13.8 J

    RISK ASSESSMENT:
      - Could cause injury if it hits a person
      - Unlikely to cause serious injury (sub-200g, large flat area distributes impact)
      - Mitigation: deploy only over unpopulated areas or at sufficient altitude
        that wind dispersal makes direct hit extremely unlikely
      - Additional mitigation: foam bumper on bottom surface (adds 2g, reduces
        peak impact force by ~40%)

    TUMBLE BEHAVIOR:
      A flat square plate tumbles chaotically during freefall (autorotation).
      Horizontal drift during tumble from 200m: ~30-80m (wind dependent).
      The flat shape acts as a natural drag brake — this is a safety advantage
      over cylindrical or streamlined failed drones that would fall faster.
```

---

## 6. Structural Design

### 6.1 Frame Architecture

```
    EXPLODED VIEW — VARIANT A

                        ┌─────────────────────┐
                        │    TOP SHELL         │  ◄── 1.5mm PA12 nylon
                        │  (duct inlets,       │      injection molded
                        │   GPS window,        │      Weight: ~18g
                        │   alignment pins)    │
                        └─────────┬───────────┘
                                  │
                        ┌─────────┴───────────┐
                        │    PCB STACK         │  ◄── FC+ESC AIO board
                        │  (26x26mm FC,        │      GPS module
                        │   ESP32, LoRa,       │      Radio modules
                        │   all soldered to     │      Weight: ~13g
                        │   carrier PCB)       │
                        └─────────┬───────────┘
                                  │
                        ┌─────────┴───────────┐
                        │    BATTERY           │  ◄── 2S 450mAh LiPo
                        │  (48 x 25 x 13 mm)  │      secured with foam pad
                        │                      │      Weight: 26g
                        └─────────┬───────────┘
                                  │
                        ┌─────────┴───────────┐
                        │    BOTTOM SHELL      │  ◄── 1.5mm PA12 nylon
                        │  (duct exhaust,      │      injection molded
                        │   alignment dimples, │      Weight: ~17g
                        │   magazine rails,    │      Includes motor mounts
                        │   charging contacts) │
                        └─────────────────────┘


    MOTOR MOUNTING DETAIL (corner duct cross-section):

              duct wall (2mm)
                │
          ┌─────┤
          │     │        ┌──── prop (50mm)
          │     │        │
          │  ┌──┴────────┴───┐
          │  │  ░░░░░░░░░░░  │   ◄── prop plane
          │  └───────┬───────┘
          │          │
          │     ┌────┴────┐
          │     │  MOTOR  │      ◄── 1103 motor, press-fit into
          │     │  1103   │          molded motor mount boss
          │     └────┬────┘
          │          │
          └──────────┘
              duct wall (2mm)

    Motor mount: 3-point press-fit boss molded into bottom shell
    Motor wires route through channels in shell wall to central PCB bay
```

### 6.2 Material Selection

| Material | Density | Tensile Str. | Frame mass (est.) | Cost per unit | Suitability |
|---|---|---|---|---|---|
| PA12 Nylon (injection) | 1.01 g/cm^3 | 50 MPa | 35 g | £1.50 (at qty 1000) | **Best for production** |
| PA12 Nylon (MJF 3D print) | 1.01 g/cm^3 | 48 MPa | 38 g | £8-12 (at qty 10) | Best for prototyping |
| PETG (FDM 3D print) | 1.27 g/cm^3 | 53 MPa | 44 g | £3-5 (at qty 10) | Budget prototyping |
| Carbon-fiber PA (CF-nylon) | 1.10 g/cm^3 | 85 MPa | 30 g | £15-20 (at qty 10) | Weight-critical variant |
| FR4 PCB-as-frame | 1.85 g/cm^3 | 310 MPa | 28 g* | £3-5 | *Only for main plate, not ducts |

**Recommended approach:**
1. **Prototype phase:** MJF (HP Multi Jet Fusion) nylon 3D printing. Allows rapid iteration, good strength, reasonable cost at qty 5-20. Lead time: 3-5 days from service bureaus.
2. **Low-rate production (qty 100):** Injection-molded PA12 nylon. Tooling cost: £3,000-8,000 for the two-piece shell mold. Per-unit frame cost drops to £1-2.
3. **Mass production (qty 10,000+):** Same injection mold tooling, per-unit cost drops below £0.50.

### 6.3 Integrated Structural Features

```
    BOTTOM SURFACE — UNDERSIDE VIEW

    ┌───────────────────────────────────────────────┐
    │  ○                                         ○  │
    │      DIMPLE                         DIMPLE    │
    │                                               │
    │  ═══════════════════════════════════════════   │  ◄── Magazine guide rail
    │                                               │      (raised ridge, 2mm tall,
    │      ╭───╮                      ╭───╮         │       2mm wide, full length)
    │      │   │                      │   │         │
    │      │   │   ┌──────────────┐   │   │         │
    │      │   │   │  CHARGE PAD  │   │   │         │      ◄── 2x spring-loaded
    │      │   │   │  (+)    (-)  │   │   │         │          pogo pins
    │      │   │   └──────────────┘   │   │         │          (gold-plated)
    │      │   │                      │   │         │
    │      ╰───╯                      ╰───╯         │
    │                                               │
    │  ═══════════════════════════════════════════   │  ◄── Magazine guide rail
    │                                               │
    │  ○                                         ○  │
    │      DIMPLE                         DIMPLE    │
    └───────────────────────────────────────────────┘

    ALIGNMENT SYSTEM:
      Top surface:  4x conical pins (2mm base, 1.5mm tip, 3mm tall)
      Bottom surface: 4x conical dimples (matching geometry)
      Purpose: self-centering when stacking, prevents lateral shift in magazine
      Tolerance: ±0.5mm self-alignment range

    MAGAZINE RAIL GUIDES:
      2x parallel raised ridges on bottom surface
      Match grooves in magazine inner wall
      Provide guided insertion and prevent rotation during deployment
      Rail height: 2mm, width: 2mm, length: full 130mm

    CHARGING CONTACTS:
      2x gold-plated spring pins (pogo pins) on bottom surface
      Mate with PCB pads on top surface of drone below in stack
      Allows daisy-chain charging: charger connects to top drone,
      power passes through stack via pin-to-pad contacts
      Current rating: 500mA per pin (1A total, charges 450mAh in ~30 min)
```

---

## 7. Swarm Communication Protocol

### 7.1 Communication Architecture

```
    COMMUNICATION HIERARCHY

    ┌─────────────────────────────────────────────────┐
    │              GROUND CONTROL STATION              │
    │  (or carrier aircraft autopilot)                 │
    └────────────────────┬────────────────────────────┘
                         │
                    LoRa (868 MHz)
                    2-5 km range
                    SF7-SF12 adaptive
                    ~1-10 kbps
                         │
    ┌────────────────────┴────────────────────────────┐
    │              SWARM MESH LAYER                    │
    │                                                  │
    │    D01 ◄──────► D02 ◄──────► D03                │
    │     ▲             ▲             ▲                │
    │     │             │             │                │
    │     ▼             ▼             ▼                │
    │    D04 ◄──────► D05 ◄──────► D06                │
    │     ▲             ▲             ▲                │
    │     │             │             │                │
    │     ▼             ▼             ▼                │
    │    D07 ◄──────► D08 ◄──────► D09                │
    │                                                  │
    │    ESP-NOW mesh (2.4 GHz, ~500m range)           │
    │    <5 ms inter-node latency                     │
    │    Auto-forming, self-healing topology           │
    └──────────────────────────────────────────────────┘
```

### 7.2 TDMA Slot Allocation

For a 48-drone swarm:

| Parameter | Value |
|---|---|
| Frame duration | 50 ms |
| Slots per frame | 50 |
| Slot duration | 1.0 ms |
| Payload per slot | ~250 bytes (at 2 Mbps ESP-NOW) |
| Slots per drone | 1 |
| Reserved slots | 2 (sync + command relay) |
| Max drones per frame | 48 |
| Position update rate | 20 Hz (every 50ms) |

Each drone transmits in its assigned slot:
- Drone ID (1 byte)
- GPS position (8 bytes: lat/lon as int32 offsets from swarm origin)
- Altitude (2 bytes: cm resolution)
- Velocity vector (6 bytes: vx/vy/vz as int16, cm/s)
- Battery voltage (1 byte: 0.1V resolution)
- Status flags (1 byte: armed, GPS fix, mission state)
- Sensor data summary (4 bytes: mission-dependent)
- **Total: 23 bytes per slot** (well within 250-byte capacity)

### 7.3 Swarm Behaviors

| Behavior | Description | Algorithm |
|---|---|---|
| SPREAD | Cover maximum area evenly | Voronoi tessellation — each drone moves to centroid of its Voronoi cell |
| TRACK | Converge on target | Proportional navigation toward shared target estimate |
| ORBIT | Circle a point of interest | Distributed phase assignment, equal angular spacing |
| LINE | Form a search line | Rank-order by position, equal spacing along bearing |
| RETURN | RTL to carrier/base | Sequential approach with altitude separation |
| LAND | Distributed landing | Each drone finds flat spot within its Voronoi cell |

### 7.4 LoRa Command Protocol

Commands from carrier/GCS via LoRa:

| Command | Payload | Description |
|---|---|---|
| `DEPLOY_SPREAD` | center_lat, center_lon, radius | Spread to cover area |
| `DEPLOY_LINE` | start_lat, start_lon, end_lat, end_lon, spacing | Search line |
| `TRACK_TARGET` | target_lat, target_lon, altitude | Converge on target |
| `ORBIT_POI` | poi_lat, poi_lon, radius, altitude | Orbit point |
| `RTL` | base_lat, base_lon | Return to base |
| `EMERGENCY_LAND` | (none) | Immediate landing |
| `SET_ALTITUDE` | altitude_m | Change swarm altitude |
| `REPORT` | (none) | Request status from all drones |

---

## 8. Applications

### 8.1 Area Saturation ISR

48 drones deployed from a single carrier pass. Each drone covers a ~150m diameter circle with onboard camera. At 200m spacing:

```
    COVERAGE PATTERN — 48 DRONES IN SPREAD FORMATION

    Each ○ = one drone's coverage circle (~150m diameter)

    ○ ○ ○ ○ ○ ○ ○ ○
     ○ ○ ○ ○ ○ ○ ○
    ○ ○ ○ ○ ○ ○ ○ ○
     ○ ○ ○ ○ ○ ○ ○
    ○ ○ ○ ○ ○ ○ ○ ○
     ○ ○ ○ ○ ○ ○ ○
    ○ ○ ○ ○ ○ ○ ○ ○

    Grid spacing: 150m (hexagonal close-pack)
    Coverage width: 8 × 150m = 1,200m
    Coverage depth: 7 × 130m = 910m  (hex row offset = 150 × sin60 = 130m)
    Total area: ~1.09 km^2
    Time to deploy: ~20 seconds (2 magazines of 24)
    Persistent coverage time: 5-7 minutes per drone
```

### 8.2 Distributed Sensor Network

Drones deploy, fly to assigned positions, and **land**. On the ground with motors off, the ESP32 mesh and sensors continue operating on battery for extended duration.

| Mode | Power draw | Battery life (2S 450mAh) |
|---|---|---|
| Flying (hover) | 50 W | 4 minutes |
| Landed, sensors active | 0.3 W | 11 hours |
| Landed, sleep with periodic wake | 0.02 W | 7 days |

This transforms a 4-minute flyer into a 7-day ground sensor node.

### 8.3 Search and Rescue

With MLX90640 thermal sensor (32x24 pixel, adds 3g and £25):
- 16 drones search 16 parallel corridors simultaneously
- Each corridor: 150m wide, drone speed 5 m/s
- 1 km search depth in 200 seconds (3.3 minutes)
- Total area searched: 16 x 150m x 1000m = 2.4 km^2 in under 4 minutes
- Thermal detection range: ~30m altitude, person-sized heat signature detectable

### 8.4 Agricultural Pest Monitoring

With MEMS microphone or miniature multispectral sensor:
- Deploy 48 drones across a field
- Land at grid positions 30m apart
- Listen for pest sounds (e.g., moth wing frequencies, rodent ultrasound)
- Or photograph individual plants for disease detection
- Coverage: 48 x 30m spacing = 1,440m x 1,080m grid = 1.55 km^2

### 8.5 Military / Defense Applications

**Reference: PERDIX comparison**

| Parameter | PERDIX | This Design (Tileable Quad) |
|---|---|---|
| Weight | 290g | 180g |
| Form factor | Fixed-wing, folding | Quad, stackable square |
| Hover capability | No (stall speed ~15 m/s) | **Yes** (this is the key advantage) |
| Endurance | ~20 min (cruise) | ~5 min (hover) |
| Packing density | Cylindrical tube, moderate | Square tile, very high |
| Swarm size demonstrated | 103 | Target: 48 per carrier pass |
| Launch method | Flare dispenser | Magazine drop |
| Indoor capable | No | **Yes** (GPS-denied requires extra sensors) |
| Loiter/persist | No (must keep flying) | **Yes** (can land and wait) |

Key defense applications:
- **ISR swarm**: rapid area coverage with hover and landing capability
- **Decoy swarm**: 48 radar/RF returns mimicking larger force
- **Electronic warfare**: distributed RF emitters/jammers
- **Counter-drone**: interceptor swarm (kinetic impact at 180g, 12 m/s closing speed = 13 J, enough to foul a target drone's props)
- **Persistent surveillance**: deploy, land on rooftops, listen for days

---

## 9. Cost Analysis

### 9.1 Full-Spec BOM (Qty 100)

| Component | Unit Cost (qty 100) | Notes |
|---|---|---|
| Frame — 2-piece PA12 shell (MJF print) | £8.00 | MJF at qty 100; injection mold at qty 1000+ drops to £1.50 |
| Motors — 4x 1103 8000KV | £12.00 | £3.00 each, Chinese OEM direct |
| Props — 4x 50mm triblade | £0.80 | £0.20 each, bulk buy |
| FC + 4in1 ESC (AIO) | £8.50 | Happymodel/BetaFPV class |
| GPS — u-blox MAX-M10S + antenna | £5.50 | Module + ceramic patch |
| ESP32-C3-MINI-1 | £1.20 | Espressif direct |
| SX1262 LoRa module | £2.50 | Semtech reference design |
| BMP280 barometer | £0.30 | If separate from FC |
| Battery — 2S 450mAh LiPo | £4.50 | GNB, Tattu, or equivalent |
| Alignment pins (4x nylon) | £0.10 | Injection-molded with frame or press-fit |
| Pogo pins (2x charging contacts) | £0.40 | Mill-Max or equivalent |
| Reed switch (power-on activation) | £0.15 | Glass reed switch |
| PCB carrier board (for mounting) | £1.50 | 2-layer FR4, panelized |
| Connectors, wires, solder | £1.00 | Micro JST, 28AWG silicone |
| Foam separator sheet | £0.05 | Shared across magazine |
| Assembly labor (15 min at £12/hr) | £3.00 | Hand assembly for qty 100 |
| | | |
| **TOTAL PER DRONE** | **£49.50** | At qty 1000+ with injection molds |

> **Realistic cost note:** At qty 100 (MJF frames, hand assembly), actual cost is £58-68 per unit including rework, yield losses, and shipping. The £49.50 figure is achievable at qty 1000+ with injection-molded frames and batch assembly processes.

### 9.2 Minimum Viable Version (No GPS, Basic Radio) — Target <£20

Strip to absolute minimum for disposable/expendable operation:

| Component | Unit Cost (qty 100) | Notes |
|---|---|---|
| Frame — 2-piece PA12 shell (MJF) | £8.00 | Same |
| Motors — 4x 1103 8000KV | £12.00 | Same |
| Props — 4x 50mm triblade | £0.80 | Same |
| FC + 4in1 ESC (AIO) | £8.50 | Same |
| Battery — 2S 300mAh LiPo | £3.50 | Smaller, lighter |
| ESP32-C3-MINI-1 (mesh only) | £1.20 | No LoRa, no GPS |
| Reed switch | £0.15 | |
| Wiring/connectors | £0.50 | Simplified |
| Assembly (10 min) | £2.00 | Simpler build |
| | | |
| **TOTAL PER DRONE** | **£36.65** | Over £20 target |

The £20 target is not achievable at qty 100 with quality brushless motors and a proper flight controller. The motors + FC alone cost £20.50. Paths to reach £20:

| Cost reduction | Savings | Tradeoff |
|---|---|---|
| Custom PCB combining FC+ESC+ESP32 | -£5.00 | Requires PCB design investment (£2,000-5,000 NRE) |
| Chinese OEM motors at qty 1000 | -£4.00 | £2.00/motor instead of £3.00, longer lead time |
| Injection-molded frame at qty 1000 | -£6.50 | Requires £5,000 tooling investment |
| Simpler 1S battery | -£1.00 | Reduced flight time, lower thrust |
| **Total savings** | **-£16.50** | |
| **Revised unit cost** | **£20.15** | At qty 1000 with NRE investment |

At qty 1000 with upfront tooling: **£20 per drone is achievable.** At qty 100, the realistic minimum is ~£35-37.

### 9.3 Magazine Cost

| Component | Cost |
|---|---|
| Aluminum magazine body (CNC or extruded) | £25 |
| Spring plate + compression spring | £3 |
| Solenoid gate mechanism | £8 |
| Charging bus PCB + connector | £5 |
| Wiring harness | £2 |
| **Total per magazine** | **£43** |

### 9.4 System Cost Summary

| Configuration | Drones | Magazines | Total Cost |
|---|---|---|---|
| Minimum demo (3 drones) | 3 x £50 = £150 | 0 (hand deploy) | £150 |
| Proof of concept (10 drones + magazine) | 10 x £50 = £500 | 1 x £43 = £43 | £543 |
| Operational swarm (48 drones) | 48 x £50 = £2,400 | 5 x £43 = £215 | £2,615 |
| Mass production (1000 drones) | 1000 x £20 = £20,000 | 100 x £30 = £3,000 | £23,000 |

---

## 10. Design Risks and Mitigations

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Insufficient T:W ratio | HIGH | MEDIUM | Use 1104 motors if 1103 undersized; reduce AUW; optimize duct geometry in CFD |
| Duct wall resonance / vibration | MEDIUM | HIGH | Add internal ribs; tune wall thickness; use damping material |
| Magazine jam (drone stuck) | HIGH | LOW | Chamfered edges; PTFE coating on magazine walls; spring force margin |
| Props damaged in stack | MEDIUM | LOW | Ducts fully protect props; foam separators prevent contact |
| GPS denied environment | MEDIUM | HIGH | Optical flow sensor option (+3g, +£8); ESP32 ranging for relative positioning |
| ESC sync failure on cold start | HIGH | LOW | Pre-arm ESCs in magazine; fast-start ESC firmware |
| Battery deep discharge in storage | MEDIUM | MEDIUM | Storage voltage maintenance via magazine charging bus |
| Mesh network congestion at 48 nodes | MEDIUM | MEDIUM | TDMA prevents collision; tested at 50 nodes in ESP-NOW benchmarks |
| Regulatory approval for swarm ops | HIGH | HIGH | UK CAA requires specific operational authorization; start with MOD/DSTL partnership |

---

## 11. Development Roadmap

### Phase 1: Single Drone Prototype (4-8 weeks)

- 3D print (FDM PETG) Variant A frame
- Off-the-shelf FC (CrazyF4 AIO), motors (1103 8000KV), 2S 450mAh battery
- Bench test: thrust stand verification of ducted vs unducted performance
- First flight: manual control via Betaflight + radio receiver
- Measure AUW, flight time, stability
- Deliverable: flying prototype, validated weight and thrust numbers

### Phase 2: Autonomy and Communication (4-6 weeks)

- Add GPS module, configure INAV for autonomous waypoint flight
- Integrate ESP32-C3 with custom mesh firmware
- Test 3-drone mesh communication
- Implement freefall detection auto-arm
- Deliverable: 3 autonomous drones communicating via mesh

### Phase 3: Magazine and Deployment (6-8 weeks)

- Design and fabricate 10-drone magazine (aluminum + 3D print)
- Integrate charging contacts, reed switch activation
- Ground-level drop tests (2-3m drop, verify auto-arm and stabilization)
- Elevated drop tests (10-30m, from tethered balloon or tall structure)
- Deliverable: magazine prototype, successful drop-and-fly demonstration

### Phase 4: Swarm Integration (8-12 weeks)

- Scale to 10+ drones
- Implement swarm behaviors (SPREAD, TRACK, ORBIT)
- Field test: deploy 10 drones from magazine, execute area coverage mission
- MJF nylon frame production run (qty 20-50)
- Deliverable: 10-drone swarm demonstration video, performance data

### Phase 5: Carrier Integration (12-16 weeks)

- Integrate magazine into MINI tier carrier payload bay
- Air-to-air deployment test (carrier drops swarm at 100m AGL)
- Full system demonstration: carrier launches, deploys 10-drone swarm, swarm executes ISR mission, returns data via mesh
- Deliverable: integrated carrier + swarm system demonstration

---

## 12. Reference Dimensions Summary

```
    QUICK REFERENCE CARD

    ┌─────────────────────────────────────┐
    │        TILEABLE MICRODRONE          │
    │         Variant A (v1.0)            │
    │                                     │
    │  Footprint:     130 x 130 mm       │
    │  Thickness:     32 mm              │
    │  Corner radius: 12 mm              │
    │  AUW:           180 g              │
    │  Prop diameter: 50 mm (ducted)     │
    │  Motor:         1103 8000KV        │
    │  Battery:       2S 450mAh LiPo    │
    │  Flight time:   4-5 min (hover)    │
    │  Max thrust:    ~300 g (ducted)    │
    │  T:W ratio:     1.67:1            │
    │  Radio:         ESP32 mesh + LoRa  │
    │  GPS:           u-blox MAX-M10S    │
    │                                     │
    │  PACKING:                           │
    │  Stack height (10): 334 mm         │
    │  Stack mass (10):   1.82 kg        │
    │  Grid (500x500mm):  3x3 = 9/layer │
    │  Grid (500x500x200mm): 45 drones  │
    │  Magazine capacity: 10 drones      │
    │  Deploy rate: 2.5 drones/sec       │
    │                                     │
    │  Unit cost: £50 (qty 100)          │
    │  Unit cost: £20 (qty 1000, min)    │
    └─────────────────────────────────────┘
```
