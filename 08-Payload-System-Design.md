# Hotswappable Payload System Design

## Interface Specification

### Mechanical — Dovetail Rail with Quick-Release Pins

```
  PAYLOAD BAY CROSS-SECTION (looking forward)
  ════════════════════════════════════════════

        ◄──────── 200mm (bay width) ────────►

        ┌──────────────────────────────────────┐
        │         FUSELAGE UPPER SKIN          │
        │  ┌────────────────────────────────┐  │
        │  │   AVIONICS / FC / BATTERY      │  │
        │  └────────────────────────────────┘  │
        │  ┌────────────────────────────────┐  │
        │  │       PAYLOAD VOLUME           │  │  ▲
        │  │  200mm W × 300mm L × 150mm H  │  │  │ 150mm
        │  │                                │  │  ▼
        │  └────────────────────────────────┘  │
        ╪══ DOVETAIL ══╤═ CONNECTOR ╤══ RAIL ══╪
        └──────────────┴───────────┴───────────┘
                         ▼ opens downward

  Max payload: 4.0 kg (including tray)
  Tray mass budget: 0.3-0.5 kg
  Swap time: 30-60 seconds
```

### Electrical Interface

**Power:** Anderson PowerPole PP45 (4-pole: 5V + 12V + VBATT + GND)
- Pin 1: 5V @ 3A (servos, small cameras)
- Pin 2: 12V @ 5A (gimbals, radios)
- Pin 3: VBATT raw ~22V @ 10A (payload has own regulator)
- Pin 4: GND (common return)
- All three rails available simultaneously; payload draws only what it needs
- Selection: DIP switch on connector plate selects which rails are active, labeled per payload
- Protection: 15A blade fuse inline per rail

**Data:** JST-GH 8-pin (1.25mm pitch)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | UART TX | FC serial → payload |
| 2 | UART RX | Payload → FC serial |
| 3 | I2C SDA | 3.3V logic |
| 4 | I2C SCL | 100/400 kHz |
| 5 | PWM/SERVO 1 | Direct from FC |
| 6 | PWM/SERVO 2 | Direct from FC |
| 7 | GPIO / ID_0 | Payload ID bit 0 |
| 8 | GPIO / ID_1 | Payload ID bit 1 |

**Note:** ID pins (7, 8) require 10kΩ pull-up resistors to 3.3V on the airframe side. Without pull-ups, floating pin reads are unreliable and payload auto-detection will misfire.

**Payload Auto-Detection (ID pins):**

| ID_1 | ID_0 | Payload Type |
|------|------|-------------|
| FLOAT | FLOAT | Empty |
| FLOAT | GND | Cargo pod |
| GND | FLOAT | Camera/ISR |
| GND | GND | Other (read I2C EEPROM) |

### Power Architecture (Isolated)

```
BATTERY ──┬──► FC BEC (5V, 3A) ──► Flight Controller, Servos, Receiver
          │
          └──► PAYLOAD BEC ──► [15A FUSE] ──► Payload Connector
               (separate)
```

Payload fault CANNOT affect flight controller.

## Payload Modules

### A. Cargo Pod (~£30)
- Bomb-bay doors + SG90 servo + latch
- Triggered by DO_SET_SERVO at waypoint
- 5V @ 0.5A, PWM only, no data bus needed
- Parachute variant: replace doors with chute deployment servo

### B. Camera/ISR (~£120-420)
- Budget: RunCam 2 + servo gimbal (~£120)
- Mid: Siyi A8 mini 3-axis integrated (~£350-420)
- Companion computer (RPi) for video streaming
- 12V @ 3A, UART for MAVLink gimbal control
- ArduPilot: MNT_TYPE, DO_SET_ROI, DO_DIGICAM_CONTROL

### C. SAR Sensor Pod (~£340-500)
- FLIR Lepton 3.5 thermal (160×120) on PureThermal board
- Visible light wide-angle camera
- RPi + Google Coral USB for person detection
- Optional: 406MHz PLB scanner, siren
- 12V @ 3A, UART + I2C

### D. Radar/Scanning (~£500-1,300)
- Realistic options at this scale:
  - mmWave (TI IWR6843): 76-81 GHz, 50-150m range, £40-65
  - LiDAR (Livox Mid-360): 3D point cloud, 200m range, £400-1,200
  - Radar altimeter (Ainstein US-D1): 50m AGL, ArduPilot native, £160
- RPi/Jetson for processing, SSD for data storage
- 12V @ 3A

### E. Comms Relay (~£140-260)
- 2× RFD900x radios as MAVLink relay
- ArduPilot native support (SERIAL2_PROTOCOL = 2)
- Or: store-and-forward with ESP32 controller
- 12V @ 2A

### F. Generic Sensor Bay (~£30)
- Empty tray with perforated M3 mounting plate
- Pre-wired pigtails, power distribution board
- Blank I2C EEPROM for programming payload ID
- For: air quality, magnetometer, multispectral, LoRa mesh, etc.

## CG Management

**Problem:** Payloads range 0.5-4.0 kg in the same bay position.

**Solution:** Sliding payload rail (120mm travel) + battery position adjustment

```
  CG CHART (calculate for YOUR airframe)
  ────────────────────────────────────────
  Payload Mass  │  Rail Position
  0.5 - 1.0 kg  │  +40 to +55mm (aft)
  1.0 - 2.0 kg  │   0 to +40mm (center-aft)
  2.0 - 3.0 kg  │  -20 to +10mm (center-fwd)
  3.0 - 4.0 kg  │  -40 to -20mm (forward)

  + Battery slides fore/aft on Velcro rail (100mm travel)
  + Lead ballast bags (100g, 200g, 500g) for light payloads
```

**Verification:** Balance test before EVERY flight. CG target: 25-33% MAC.

## ArduPilot Per-Payload Parameters

Save as `.param` files on GCS laptop, load when swapping payloads:

- `cargo_pod.param` — SERVO9_FUNCTION, etc.
- `camera_isr.param` — MNT_TYPE, CAM_TRIGG_TYPE, etc.
- `sar_pod.param` — SERIAL protocol, relay pins
- `comms_relay.param` — SERIAL2_PROTOCOL
- `generic.param` — minimal config

**Future:** Lua script auto-detects payload via ID pins, loads params, blocks arming if CG unchecked.

## Safety & Failure Modes

| Failure | Severity | Mitigation |
|---------|----------|-----------|
| Payload detaches in flight | CRITICAL | Safety lanyard: M4 stainless steel through-bolt with aluminium backing plate on fuselage structure (not bare hole in PETG — PETG will creep under sustained load), 2mm steel cable to payload tray, redundant Velcro, pre-flight pull test |
| Electrical short in payload | HIGH | Separate BEC, 15A fuse, MOSFET relay cutoff |
| CG out of limits | CRITICAL | Mandatory balance test, arming check script, in-flight trim monitoring |
| Connector fails mid-flight | MEDIUM | Latching connectors, strain relief, pre-flight continuity check |

**Key principle: Payload failure must NEVER cause aircraft failure.**

## Bill of Materials

### Interface System (airframe side): ~£70

| Item | Cost |
|------|------|
| Dovetail rails (AL 6061-T6, 15×15mm) | £20 |
| Spring detent pins ×2 | £12 |

> **Note:** Detent pin shear load calculations needed — the pins must resist vibration-induced lateral forces without shearing under worst-case flight loads. Flag: needs verification with real hardware testing before relying on calculated margins.

| Anderson PP45 connectors | £7 |
| JST-GH 8-pin ×4 | £10 |
| Fuse, DIP switch, wiring, hardware | £21 |

### Per Tray (blank): ~£16
- 3D-printed body (PETG/nylon), mating connectors, ID resistors

### Build Order
1. Interface system + blank tray (test fit)
2. Cargo pod (simplest, proves the mechanism)
3. Camera module (most useful for testing)
4. Additional modules as missions require
