# Technical Specification: Payload Modules for Mini Fixed-Wing UAV

## Document Information

| Field | Value |
|---|---|
| Document ID | PLD-SPEC-001 |
| Version | 1.0 |
| Date | 2026-03-15 |
| Classification | UNCLASSIFIED |

---

## 1. Platform Summary and Interface Specification

### 1.1 Airframe Constraints

| Parameter | Value |
|---|---|
| Wingspan | 2-4 m |
| Configuration | Pusher propeller, fixed-wing |
| Max payload mass | 4.0 kg |
| Payload bay envelope | 200 mm (W) x 300 mm (L) x 150 mm (H) |
| Typical endurance (no payload) | ~90 min |
| Cruise speed | 18-25 m/s |
| Vibration environment | 10-80 Hz dominant, ~2 g peak |

### 1.2 Standard Hotswap Interface (HSI)

**Mechanical:** Dovetail rail (MIL-STD-1913 Picatinny profile adapted), spring-loaded latch with alignment pins. Payload slides in from the rear and locks with a quarter-turn cam.

**Power Connector — Anderson PP45**

| Pin | Rail | Voltage | Max Current | Notes |
|---|---|---|---|---|
| 1 | +5 V | 5.0 V ± 0.25 V | 3 A | BEC-regulated |
| 2 | +12 V | 12.0 V ± 0.5 V | 5 A | Switched BEC |
| 3 | VBATT | 14.8-25.2 V (4-6S) | 8 A | Direct battery, fused |
| 4 | GND | — | — | Common ground |

**Data Connector — JST-GH 8-pin (1.25 mm pitch)**

| Pin | Function | Protocol | Voltage Level |
|---|---|---|---|
| 1 | UART TX (FC→Payload) | MAVLink v2 / Serial | 3.3 V |
| 2 | UART RX (Payload→FC) | MAVLink v2 / Serial | 3.3 V |
| 3 | I2C SDA | I2C | 3.3 V |
| 4 | I2C SCL | I2C | 3.3 V |
| 5 | PWM CH1 | Servo PWM 50-400 Hz | 3.3 V |
| 6 | PWM CH2 | Servo PWM 50-400 Hz | 3.3 V |
| 7 | GPIO ID0 | Digital / ADC | 3.3 V |
| 8 | GPIO ID1 | Digital / ADC | 3.3 V |

**ID Resistor Convention:** Each payload carries a resistor divider on GPIO ID0/ID1 that the flight controller reads at boot via ADC to auto-detect the installed module.

| ID0 (kΩ) | ID1 (kΩ) | Payload Type |
|---|---|---|
| 10 | Open | A — EO Camera |
| 22 | Open | B — IR/Thermal |
| 47 | Open | C — LiDAR |
| 10 | 10 | D — Combined ISR Pod |

**Flight Controller:** Pixhawk 6C / Cube Orange+, running ArduPlane 4.5+.

---

## 2. Payload A — Electro-Optical (EO) Camera Module

### 2.1 Purpose

Daylight survey and mapping camera producing georeferenced imagery suitable for photogrammetric reconstruction (orthomosaics, DSMs, 3D models).

### 2.2 Component Selection

| Component | Model | Mass (g) | Power (W) | Price (GBP) |
|---|---|---|---|---|
| **Camera (Primary)** | Sony RX0 II | 132 | 3.5 | £620 |
| **Camera (Budget Alt)** | Siyi A8 Mini (w/ 3-axis gimbal) | 215 | 6.0 | £340 |
| **Camera (Lightweight Alt)** | RunCam Hybrid 4K | 48 | 2.8 | £75 |
| Companion Computer | Raspberry Pi CM4 (4 GB) on carrier board | 55 | 4.5 | £75 |
| GNSS Receiver (PPK) | u-blox ZED-F9P on SparkFun board | 18 | 0.6 | £190 |
| GNSS Antenna | Tallysman TW4722 L1/L2 patch | 22 | — | £55 |
| MicroSD (camera) | Samsung PRO Plus 256 GB UHS-I | 2 | — | £28 |
| MicroSD (CM4) | Samsung EVO 64 GB | 1 | — | £10 |
| Trigger MOSFET board | Custom PCB (opto-isolated) | 5 | 0.1 | £8 |
| Vibration isolator | 4x silicone grommets M3 | 4 | — | £3 |
| Baseplate + enclosure | 3D-printed PA12/CF | 85 | — | £15 |
| Dovetail adapter | CNC aluminium | 60 | — | £25 |
| **Total (Sony RX0 II build)** | | **384 g** | **8.7 W** | **£1,029** |

**Recommended primary:** Sony RX0 II — 15.3 MP (1" Exmor RS), mechanical-like electronic shutter, excellent low-light, Zeiss 24 mm eq. f/4.0 lens. Well proven for UAV photogrammetry.

### 2.3 Performance Specifications

| Parameter | Sony RX0 II | Siyi A8 Mini | RunCam Hybrid |
|---|---|---|---|
| Sensor | 1" 15.3 MP | 1/2.7" 4K | 1/3" 8 MP |
| Still resolution | 4800 x 3200 | 3840 x 2160 (video frame grab) | 3840 x 2160 |
| GSD at 100 m AGL | 2.1 cm/px | 3.8 cm/px | 4.2 cm/px |
| GSD at 60 m AGL | 1.3 cm/px | 2.3 cm/px | 2.5 cm/px |
| FOV (diagonal) | 84° | 88° | 79° |
| Min trigger interval | 1.0 s (burst mode) | 2.0 s | 0.5 s (video) |
| Stabilisation | Electronic (EIS) | 3-axis mechanical gimbal | None |
| Video | 4K 30 fps | 4K 30 fps | 4K 30 fps |
| Hot shoe / trigger input | Multi-terminal (2.5 mm) | UART command | USB trigger |

**Mapping Coverage at 100 m AGL, 20 m/s cruise, 70% forward overlap:**
- Strip width: ~168 m (Sony RX0 II)
- Photo interval: ~2.5 s (50 m along-track spacing)
- Coverage rate: ~12 ha/min (single strip)

### 2.4 Mechanical Layout

```
           200 mm
    ┌──────────────────────┐
    │  ┌──────────────────┐│ ▲
    │  │   GNSS Antenna   ││ │
    │  │  (Tallysman)     ││ │
    │  │  [60x60x12mm]    ││ │
    │  └──────────────────┘│ │
    │                      │ │
    │  ┌────────┐ ┌──────┐│ │
    │  │ CM4 +  │ │ZED-  ││ │ 300 mm
    │  │Carrier │ │F9P   ││ │ (Length)
    │  │[85x56] │ │[25x  ││ │
    │  │        │ │ 35]  ││ │
    │  └────────┘ └──────┘│ │
    │                      │ │
    │  ┌──────────────────┐│ │
    │  │   Sony RX0 II    ││ │
    │  │   [59x41x35mm]   ││ │
    │  │  ↓ lens down ↓   ││ │
    │  │  [on vib mount]  ││ ▼
    │  └──────────────────┘│
    │ ════════════════════ │ ← Dovetail rail
    └──────────────────────┘

    Side view (150 mm height):
    ┌──────────────────────────┐ ▲
    │ GNSS ant.  CM4   F9P    │ │ 40 mm upper deck
    ├──────────────────────────┤ │
    │                          │ │ 75 mm camera zone
    │   Sony RX0 II            │ │ (lens pointing down
    │   on silicone mounts     │ │  through window)
    ├──────────────────────────┤ │
    │ ▓▓ optical window ▓▓    │ │ 20 mm floor
    │ ═══ dovetail rail ═══   │ ▼ 15 mm rail
    └──────────────────────────┘
      Total: ~150 mm
```

Camera lens faces nadir (straight down) through a flat BK7 optical window (anti-reflection coated) flush with the fuselage belly.

### 2.5 Wiring Diagram

```
                    ANDERSON PP45                JST-GH 8-PIN
                   ┌───────────┐               ┌───────────────┐
                   │ +5V  (1)──┼──────────────→│ CM4 +5V       │
                   │           │    ┌─────────→│ ZED-F9P +5V   │
                   │ +12V (2)──┼────┘          │               │
                   │           │  (not used     │               │
                   │ VBATT(3)──┼── by EO mod)  │               │
                   │ GND  (4)──┼──────────────→│ Common GND    │
                   └───────────┘               └───────────────┘

    JST-GH Pin 1 (UART TX from FC) ──→ CM4 UART RX (GPIO 15)
    JST-GH Pin 2 (UART RX to FC)  ←── CM4 UART TX (GPIO 14)
                                        ↕ MAVLink v2 @ 921600 baud

    JST-GH Pin 3 (I2C SDA) ──→ (Reserved, not used in EO module)
    JST-GH Pin 4 (I2C SCL) ──→ (Reserved)

    JST-GH Pin 5 (PWM CH1) ──→ Trigger MOSFET gate
                                   │
                                   └──→ Sony RX0 II Multi-terminal
                                        (opto-coupled, active-low pulse)

    JST-GH Pin 6 (PWM CH2) ──→ (Spare / gimbal tilt if Siyi)

    JST-GH Pin 7 (GPIO ID0) ──┤ 10 kΩ to 3.3 V (ID = EO Camera)
    JST-GH Pin 8 (GPIO ID1) ──┤ Open

    CM4 Internal Connections:
    ┌──────────────────────────────────────────────┐
    │ CM4 USB ──→ Sony RX0 II (USB-C, PTP/MTP)    │
    │ CM4 USB ──→ ZED-F9P (USB, UBX protocol)     │
    │ CM4 GPIO 17 ──→ Hot-shoe feedback (rising    │
    │                  edge = shutter confirmed)    │
    │ CM4 SPI ──→ microSD (OS + logs)              │
    └──────────────────────────────────────────────┘
```

### 2.6 ArduPilot Configuration

**Parameters (ArduPlane):**

```
# Camera trigger on AUX5 (SERVO13)
CAM1_TYPE = 1              ; Servo/Relay trigger
CAM1_SERVO_ON = 1100       ; PWM value for shutter press
CAM1_SERVO_OFF = 1500      ; PWM value for idle
CAM1_DURATION = 3          ; Trigger pulse 300 ms (unit = 0.1s)
CAM1_TRIGG_DIST = 50       ; Distance-based trigger every 50 m
SERVO13_FUNCTION = 10      ; Camera trigger
SERVO13_MIN = 1000
SERVO13_MAX = 2000

# MAVLink companion computer on SERIAL2
SERIAL2_PROTOCOL = 2       ; MAVLink2
SERIAL2_BAUD = 921         ; 921600 baud

# Camera feedback
CAM1_FEEDBAK_PIN = 54      ; AUX6 input — hot-shoe feedback
CAM1_FEEDBAK_POL = 1       ; Active high

# GPS for PPK — ZED-F9P raw data logged on CM4, not via FC
# FC uses its own GNSS for navigation

# Mission planner camera grid
WP_YAW_BEHAVIOR = 0        ; Fixed yaw in AUTO
```

**MAVLink Commands Used:**

| Command | MAV_CMD ID | Purpose |
|---|---|---|
| `MAV_CMD_DO_DIGICAM_CONTROL` | 203 | Trigger single image |
| `MAV_CMD_DO_SET_CAM_TRIGG_DIST` | 206 | Set distance-based triggering |
| `MAV_CMD_DO_DIGICAM_CONFIGURE` | 202 | Set camera mode |
| `CAMERA_IMAGE_CAPTURED` | #263 | Feedback message with lat/lon/alt/q |
| `CAMERA_TRIGGER` | #112 | Timestamp of trigger event |

### 2.7 Data Storage and Transmission

| Aspect | Specification |
|---|---|
| Image format | JPEG (8-10 MB each) or RAW DNG (30 MB each) |
| Storage per flight (60 min) | ~14 GB JPEG / ~42 GB RAW at 2 s interval |
| On-camera storage | 256 GB microSD (Samsung PRO Plus) |
| PPK GNSS log | ~200 MB/hr (RINEX observation) |
| Real-time downlink | Compressed JPEG preview (640x480) via MAVLink `ENCAPSULATED_DATA` at 1 fps, or dedicated video TX (separate from payload spec) |
| Post-flight transfer | USB 3.0 from CM4 or card removal |
| Georeferencing | EXIF tags written by CM4 using interpolated PPK position + FC attitude quaternion |

### 2.8 Processing Pipeline

**On-board (CM4, in-flight):**
- Receive MAVLink `CAMERA_TRIGGER` timestamp
- Log ZED-F9P raw GNSS observations
- Write EXIF geotags to JPEG files via `libgphoto2` PTP interface
- Generate low-res preview stream

**Post-flight (ground station):**
- PPK correction: `RTKLIB` / `Emlid Studio` using base station RINEX
- Photogrammetry: `OpenDroneMap` or `Agisoft Metashape`
- Output: Orthomosaic (GeoTIFF), DSM, 3D point cloud

### 2.9 Companion Computer Software Stack

```
Raspberry Pi CM4 (4 GB RAM, 32 GB eMMC + 64 GB SD)
├── OS: Raspberry Pi OS Lite (64-bit, Bookworm)
├── mavlink-router (FC ↔ CM4 ↔ GCS bridge)
├── dronekit-python or pymavlink (mission awareness)
├── libgphoto2 (Sony PTP camera control)
├── gpsd + str2str (ZED-F9P GNSS stream)
├── Python trigger daemon:
│   ├── Listens for CAMERA_TRIGGER MAVLink message
│   ├── Records ZED-F9P timestamp + raw measurement
│   └── Tags image EXIF via PTP
└── (Optional) GStreamer pipeline for video preview
```

---

## 3. Payload B — Infrared / Thermal Imaging Module

### 3.1 Purpose

Thermal imaging for search-and-rescue (SAR), infrastructure inspection, wildlife survey, and agricultural NDVI-proxy work. Optional EO+IR overlay (picture-in-picture or fused).

### 3.2 Component Selection

| Component | Model | Resolution | Mass (g) | Power (W) | Price (GBP) | NETD |
|---|---|---|---|---|---|---|
| **Thermal (Primary)** | FLIR Boson 320 (9 mm lens) | 320x256 | 30 | 1.0 | £1,650 | <50 mK |
| **Thermal (High-Res)** | FLIR Boson 640 (14 mm lens) | 640x512 | 36 | 1.5 | £3,800 | <40 mK |
| **Thermal (Budget)** | FLIR Lepton 3.5 (on PureThermal) | 160x120 | 12 | 0.5 | £280 | <50 mK |
| **Thermal (Budget Hi-Res)** | InfiRay Tiny1-C (384) | 384x288 | 25 | 1.2 | £750 | <40 mK |
| EO Overlay Camera | RunCam Thumb Pro 4K | 3840x2160 | 18 | 2.5 | £85 |
| Companion Computer | Raspberry Pi CM4 (4 GB) | — | 55 | 4.5 | £75 |
| Frame Grabber / Interface | GroupGets PureThermal 3 (USB-C) | — | 8 | 0.3 | £95 |
| Baseplate + enclosure | 3D-printed PA12/CF | 65 | — | £12 |
| Dovetail adapter | CNC aluminium | 60 | — | £25 |
| Germanium window (IR-pass) | 25 mm dia, AR-coated | 12 | — | £85 |
| **Total (Boson 320 + EO overlay)** | | **248 g** | **8.3 W** | **£2,027** |

**Recommended primary:** FLIR Boson 320 with 9 mm lens — excellent sensitivity, radiometric output, proven airborne sensor. For budget builds, the Lepton 3.5 on PureThermal 3 is viable but resolution-limited.

### 3.3 Performance Specifications

| Parameter | Boson 320 (9 mm) | Boson 640 (14 mm) | Lepton 3.5 | InfiRay Tiny1-C |
|---|---|---|---|---|
| Resolution | 320x256 | 640x512 | 160x120 | 384x288 |
| Pixel pitch | 12 µm | 12 µm | 12 µm | 12 µm |
| HFOV | 24° | 26° | 56° | 30° |
| Frame rate | 60 fps (ITAR: 9 fps export) | 60 / 9 fps | 8.7 fps | 25 fps |
| Spectral band | 8-14 µm (LWIR) | 8-14 µm | 8-14 µm | 8-14 µm |
| NETD | <50 mK | <40 mK | <50 mK | <40 mK |
| Radiometric | Yes (via CMOS output) | Yes | Yes (Lepton 3.5 only) | Yes |
| Temp accuracy | ±5°C (±3°C w/ cal) | ±5°C | ±5°C | ±2°C |
| Temp range | -40 to 500°C | -40 to 500°C | -10 to 140°C | -20 to 550°C |

**Detection Range Estimates (FLIR Boson 320, 9 mm lens):**

Johnson criteria: Detection = 1.5 px across target, Recognition = 6 px, Identification = 12 px.

| Target | Size | Detection | Recognition | Identification |
|---|---|---|---|---|
| Person (standing) | 0.5 x 1.8 m | 800 m | 200 m | 100 m |
| Person (prone) | 0.5 x 0.5 m | 220 m | 55 m | 28 m |
| Vehicle (car) | 2.0 x 4.5 m | 2,000 m | 500 m | 250 m |
| Vehicle (truck) | 2.5 x 8.0 m | 3,500 m | 900 m | 450 m |

*Note: Ranges assume FLIR standard atmospheric model, 50% relative humidity, sea level. Actual performance varies with atmospheric conditions, target-to-background contrast, and clutter.*

### 3.4 Mechanical Layout

```
           200 mm
    ┌──────────────────────┐
    │                      │ ▲
    │  ┌────────┐ ┌──────┐│ │
    │  │  CM4 + │ │Pure- ││ │
    │  │Carrier │ │Thrml ││ │ 300 mm
    │  │Board   │ │3     ││ │
    │  └────────┘ └──────┘│ │
    │                      │ │
    │  ┌────────┐ ┌──────┐│ │
    │  │ Boson  │ │RunCam││ │
    │  │ 320    │ │Thumb ││ │
    │  │ [21x   │ │[28x  ││ │
    │  │  21mm] │ │ 22]  ││ │
    │  │  ↓↓↓   │ │ ↓↓↓  ││ ▼
    │  └────────┘ └──────┘│
    │ [Ge window] [glass] │
    │ ════════════════════ │ ← Dovetail
    └──────────────────────┘

    Side view:
    ┌──────────────────────────┐ ▲
    │ CM4    PureThermal 3     │ 45 mm
    ├──────────────────────────┤
    │                          │
    │ Boson 320   RunCam Thumb │ 60 mm
    │ (nadir)     (nadir,      │
    │              30° offset) │
    ├──────────────────────────┤
    │ [Ge] [glass] windows     │ 25 mm
    │ ═══ dovetail rail ═══    │ 20 mm
    └──────────────────────────┘
     Total: ~150 mm
```

Boson and RunCam are mounted side-by-side, both nadir-pointing. The Germanium window (8-14 µm passband) covers the Boson aperture; a standard optical glass window covers the EO camera.

### 3.5 Wiring Diagram

```
    ANDERSON PP45                    JST-GH 8-PIN
   ┌───────────┐                   ┌────────────────┐
   │ +5V  (1)──┼──→ CM4 5V        │                │
   │           │──→ PureThermal 5V │                │
   │ +12V (2)──┼──  (not used)     │                │
   │ VBATT(3)──┼──  (not used)     │                │
   │ GND  (4)──┼──→ Common GND    │                │
   └───────────┘                   └────────────────┘

   JST-GH Pin 1 (UART TX) ──→ CM4 UART RX (MAVLink v2 @ 921600)
   JST-GH Pin 2 (UART RX) ←── CM4 UART TX
   JST-GH Pin 3 (I2C SDA) ──→ Boson I2C SDA (CCI interface)
   JST-GH Pin 4 (I2C SCL) ──→ Boson I2C SCL (CCI, addr 0x50)
   JST-GH Pin 5 (PWM CH1) ──→ (unused)
   JST-GH Pin 6 (PWM CH2) ──→ (unused)
   JST-GH Pin 7 (GPIO ID0) ──┤ 22 kΩ to 3.3V
   JST-GH Pin 8 (GPIO ID1) ──┤ Open

   CM4 Internal:
   ┌──────────────────────────────────────────────┐
   │ CM4 USB-A  ──→ PureThermal 3 (UVC + raw)    │
   │                  └──→ Boson 320 (CMOS video) │
   │ CM4 USB-C  ──→ RunCam Thumb (UVC 4K)        │
   │ CM4 GPIO 4 ──→ RunCam record trigger         │
   └──────────────────────────────────────────────┘
```

### 3.6 ArduPilot Configuration

```
# Thermal payload on SERIAL2
SERIAL2_PROTOCOL = 2       ; MAVLink2
SERIAL2_BAUD = 921

# I2C external bus for Boson CCI commands (NUC, FFC, palette)
# Accessed via companion computer's I2C passthrough, not FC directly

# No camera trigger needed — thermal streams continuously
# Optional: CAM1 for RunCam EO stills
CAM1_TYPE = 1
CAM1_TRIGG_DIST = 30       ; EO stills for overlay registration
SERVO13_FUNCTION = 10
```

**MAVLink Commands:**

| Command / Message | ID | Purpose |
|---|---|---|
| `MAV_CMD_VIDEO_START_STREAMING` | 2502 | Begin thermal stream relay to GCS |
| `MAV_CMD_VIDEO_STOP_STREAMING` | 2503 | Stop stream |
| `VIDEO_STREAM_INFORMATION` | #269 | Advertise thermal + EO streams |
| `CAMERA_IMAGE_CAPTURED` | #263 | EO overlay frame geotag |
| Custom MAVLink message (via `NAMED_VALUE_FLOAT`) | #251 | Relay spot temperature to GCS |

### 3.7 Data Storage and Transmission

| Aspect | Specification |
|---|---|
| Thermal video format | 16-bit radiometric TIFF sequence or RJPEG (Boson native) |
| Thermal data rate | 320x256 x 16-bit x 9 fps = 14.1 Mbit/s raw; ~3 MB/s compressed |
| Storage per hour (thermal) | ~11 GB/hr (16-bit TIFF); ~4 GB/hr (RJPEG) |
| EO overlay video | H.265 1080p 30 fps, ~15 Mbit/s = ~6.5 GB/hr |
| Total storage per hour | ~10-17 GB/hr (both streams) |
| On-board storage | 256 GB microSD on CM4 carrier |
| Real-time downlink | H.264 compressed thermal (320x256 or upscaled 640x480) at <2 Mbit/s via MAVLink or dedicated video TX on 5.8 GHz |
| Fusion output | Software overlay on CM4 using OpenCV: thermal colourmap alpha-blended onto EO frame |

### 3.8 Processing Pipeline

**On-board (CM4, real-time):**
- `v4l2` capture from PureThermal 3 (UVC + raw16)
- OpenCV: apply colourmap (Ironbow/White-Hot), overlay geolocation HUD
- Person/vehicle detection: lightweight TFLite model (MobileNet-SSD trained on FLIR ADAS dataset), ~5 fps on CM4 CPU
- Temperature spot measurement: read radiometric pixel values, apply Planck calibration
- GStreamer pipeline for encoded downlink stream

**Post-flight:**
- Radiometric analysis in FLIR Thermal Studio or `thermitas`
- Orthomosaic-registered thermal map via OpenDroneMap (thermal band)

---

## 4. Payload C — LiDAR Scanning Module

### 4.1 Purpose

Airborne LiDAR scanning for topographic mapping, forestry canopy analysis, corridor survey (power lines, pipelines), and 3D scene reconstruction. Generates georeferenced point clouds with centimetre-level accuracy when fused with IMU/GNSS.

### 4.2 Component Selection

| Component | Model | Mass (g) | Power (W) | Price (GBP) | Notes |
|---|---|---|---|---|---|
| **LiDAR (Primary)** | Livox Mid-360 | 265 | 9.0 | £850 | Non-repetitive, 360° coverage |
| **LiDAR (High-Perf)** | Ouster OS0-32 (Rev D) | 447 | 14.0 | £3,200 | 32-ch, 360° mechanical spin |
| **LiDAR (Legacy)** | Velodyne Puck Lite (VLP-16) | 590 | 8.0 | £4,800 | 16-ch, 360° spinning, proven |
| **LiDAR (Ultra-Light)** | Livox Avia | 498 | 10.0 | £1,200 | Non-repetitive, triangular scan |
| IMU | Xsens MTi-630 AHRS | 12 | 0.6 | £650 | ±0.3° roll/pitch, ±1° heading |
| GNSS (PPK) | u-blox ZED-F9P | 18 | 0.6 | £190 | L1/L2 multi-band |
| GNSS Antenna | Tallysman TW4722 | 22 | — | £55 | |
| Companion Computer | Raspberry Pi 5 (8 GB) | 50 | 7.0 | £80 | or Jetson Orin Nano for SLAM |
| SSD Storage | Samsung T7 500 GB (USB 3.2) | 58 | 2.5 | £55 | |
| Ethernet interface | USB-C to Ethernet adapter | 15 | 0.3 | £12 | For Livox/Ouster Ethernet |
| Power regulator | 12 V to Livox voltage reg | 20 | — | £15 | |
| Baseplate + enclosure | 3D-printed PA12/CF + Al frame | 120 | — | £30 | |
| Dovetail adapter | CNC aluminium | 60 | — | £25 | |
| **Total (Livox Mid-360 build)** | | **640 g** | **20.0 W** | **£1,962** |
| **Total (Ouster OS0-32 build)** | | **822 g** | **25.0 W** | **£4,312** |

**Recommended:** Livox Mid-360 — best mass/cost/performance ratio for the 4 kg payload limit. Non-repetitive scan pattern gives increasingly uniform coverage with dwell time. The Ouster OS0-32 is superior for corridor mapping but heavier and more expensive.

> **Warning:** The Velodyne Puck Lite at 590 g sensor-only approaches the practical limit. With all support electronics the total LiDAR module reaches ~1.1 kg, leaving 2.9 kg for other payloads or fuel. The Livox Mid-360 at 640 g total module is strongly preferred.

### 4.3 Performance Specifications

| Parameter | Livox Mid-360 | Ouster OS0-32 | Velodyne Puck Lite |
|---|---|---|---|
| Range (90% refl.) | 40 m | 35 m (wide FOV mode) | 100 m |
| Range (10% refl.) | 15 m | 20 m | 50 m |
| Points/sec | 200,000 | 655,360 | 300,000 |
| Channels | Non-repetitive pattern | 32 | 16 |
| HFOV | 360° | 360° | 360° |
| VFOV | 59° (-7° to +52°) | 90° (±45°) | 30° (±15°) |
| Angular resolution | 0.2° (non-rep. avg) | 0.35° V, configurable H | 2.0° V, 0.1-0.4° H |
| Wavelength | 905 nm | 865 nm | 903 nm |
| Point cloud format | Livox custom + PCD | OSF / PCAP / PCD | PCAP / PCD |
| Interface | 100 Mbps Ethernet | 1 Gbps Ethernet | 100 Mbps Ethernet |
| Eye safety | Class 1 | Class 1 | Class 1 |

**Point Cloud Density at 100 m AGL, 20 m/s cruise (Livox Mid-360):**
- Along-track: ~20 m/s → 200,000 pts/s → ~10 pts/m² (nadir, single pass)
- Cross-track swath: ~40 m effective (limited by range at oblique angles)
- With 50% overlap: ~15-20 pts/m² merged density

### 4.4 Mechanical Layout

```
           200 mm
    ┌──────────────────────┐
    │  ┌──────────────────┐│ ▲
    │  │   GNSS Antenna   ││ │
    │  │   [60x60x12]     ││ │
    │  └──────────────────┘│ │
    │                      │ │
    │  ┌───────┐ ┌───────┐│ │
    │  │ RPi 5 │ │ F9P + ││ │ 300 mm
    │  │ + SSD │ │ MTi-  ││ │
    │  │       │ │ 630   ││ │
    │  └───────┘ └───────┘│ │
    │                      │ │
    │  ┌──────────────────┐│ │
    │  │  Livox Mid-360   ││ │
    │  │  [φ65 x 60 mm]  ││ │
    │  │  ↓ nadir scan ↓  ││ ▼
    │  └──────────────────┘│
    │ ════════════════════ │ ← Dovetail
    └──────────────────────┘

    Side view:
    ┌──────────────────────────┐ ▲
    │ GNSS ant  RPi5  F9P MTi │ 40 mm
    ├──────────────────────────┤
    │                          │
    │     Livox Mid-360        │ 65 mm
    │  (on anti-vib plate)     │
    │                          │
    ├──────────────────────────┤
    │  ▓▓ open aperture ▓▓    │ 25 mm
    │  ═══ dovetail  ═══      │ 20 mm
    └──────────────────────────┘
     Total: ~150 mm
```

The Livox Mid-360 is mounted nadir-pointing with a clear aperture cut-out in the belly. The 360° HFOV is partially occluded by the fuselage; effective usable HFOV is approximately 200° (nadir ±100°), which is sufficient for corridor and area mapping.

**CRITICAL:** The IMU (Xsens MTi-630) must be rigidly co-mounted with the LiDAR sensor on the same anti-vibration plate. The lever arm offset between IMU, LiDAR, and GNSS antenna must be measured to ±1 mm and entered into the post-processing software.

### 4.5 Wiring Diagram

```
    ANDERSON PP45
   ┌───────────┐
   │ +5V  (1)──┼──→ RPi 5 +5V (via USB-C PD shim)
   │           │──→ ZED-F9P +5V
   │ +12V (2)──┼──→ Livox Mid-360 (10-16V input)
   │           │──→ Xsens MTi-630 (5-30V, uses 12V)
   │ VBATT(3)──┼──  (not used)
   │ GND  (4)──┼──→ Common GND (star ground at baseplate)
   └───────────┘

   JST-GH 8-PIN
   ┌────────────────┐
   │ Pin 1 (UART TX)│──→ RPi 5 UART RX (MAVLink @ 921600)
   │ Pin 2 (UART RX)│←── RPi 5 UART TX
   │ Pin 3 (I2C SDA)│──→ (unused)
   │ Pin 4 (I2C SCL)│──→ (unused)
   │ Pin 5 (PWM CH1)│──→ (unused)
   │ Pin 6 (PWM CH2)│──→ (unused)
   │ Pin 7 (ID0)    │──┤ 47 kΩ to 3.3V
   │ Pin 8 (ID1)    │──┤ Open
   └────────────────┘

   RPi 5 Internal:
   ┌──────────────────────────────────────────────────────┐
   │ RPi 5 Ethernet (via USB-C adapter) ──→ Livox Mid-360│
   │   Static IP: RPi=192.168.1.50, Livox=192.168.1.1    │
   │                                                      │
   │ RPi 5 USB  ──→ Xsens MTi-630 (USB, 400 Hz IMU)     │
   │ RPi 5 USB  ──→ ZED-F9P (USB, UBX raw + NMEA)       │
   │ RPi 5 USB  ──→ Samsung T7 SSD (point cloud storage) │
   └──────────────────────────────────────────────────────┘
```

### 4.6 ArduPilot Configuration

```
# MAVLink to companion on SERIAL2
SERIAL2_PROTOCOL = 2
SERIAL2_BAUD = 921

# LiDAR does not require direct FC control — companion handles all
# FC provides attitude/position via MAVLink for real-time georeferencing

# Optional: rangefinder from LiDAR for terrain following
RNGFND1_TYPE = 10          ; MAVLink rangefinder
RNGFND1_MIN_CM = 50
RNGFND1_MAX_CM = 4000      ; 40 m max
RNGFND1_ORIENT = 25        ; Down
TERRAIN_FOLLOW = 1         ; Enable terrain following in AUTO
```

**MAVLink Messages Used:**

| Message | ID | Direction | Purpose |
|---|---|---|---|
| `ATTITUDE_QUATERNION` | #61 | FC → CM | Vehicle attitude for point cloud registration |
| `GLOBAL_POSITION_INT` | #33 | FC → CM | Vehicle position (coarse, for real-time preview) |
| `GPS_RAW_INT` | #24 | FC → CM | Raw GNSS for monitoring |
| `DISTANCE_SENSOR` | #132 | CM → FC | Nadir distance for terrain following |
| `STATUSTEXT` | #253 | CM → FC | LiDAR health/status messages |

### 4.7 Data Storage and Transmission

| Aspect | Specification |
|---|---|
| Raw point cloud rate | 200,000 pts/s x (3x float32 xyz + uint8 intensity + uint16 timestamp) = ~3.2 MB/s |
| IMU data rate | 400 Hz x 24 bytes = ~10 KB/s |
| GNSS raw data rate | ~100 KB/s (UBX RAW + SFRBX) |
| **Total data rate** | ~3.3 MB/s = ~12 GB/hr |
| Storage medium | Samsung T7 500 GB SSD (USB 3.2 Gen 2) |
| Flight time per fill | ~40 hrs (500 GB ÷ 12 GB/hr) — storage is not the constraint |
| Real-time downlink | Not practical for full point cloud. Downlink: summary statistics, coverage map (low-res raster), and LiDAR health via MAVLink. |
| Point cloud format | PCD (binary) or LAS 1.4 (with GPS time, intensity, return number) |
| Post-flight transfer | USB 3.2 from SSD, or remove SSD for direct connection |

### 4.8 Processing Pipeline

**On-board (RPi 5, real-time):**
- Livox SDK 2.0: receive point cloud via Ethernet UDP
- Time synchronization: PTP (IEEE 1588) between RPi, Livox, and GNSS PPS
- Raw data logging: write timestamped PCD chunks to SSD
- Optional real-time SLAM: `FAST-LIO2` on RPi 5 (feasible at ~5 Hz, resource-intensive)
- Nadir range extraction → feed to FC as `DISTANCE_SENSOR` for terrain following

**Post-flight (ground workstation):**
1. PPK GNSS correction (RTKLIB / Emlid Studio)
2. IMU/GNSS fusion: compute precise trajectory (POSPac, NovAtel Inertial Explorer, or open-source `ins_nav`)
3. Point cloud georeferencing: apply trajectory to raw LiDAR timestamps → global coordinates
4. Strip adjustment: align overlapping strips (CloudCompare, LAStools)
5. Classification: ground/vegetation/building (PDAL, `lasground_new`)
6. Output: LAS 1.4 / LAZ compressed, DSM/DTM rasters

**Recommended Ground Workstation:**
- CPU: AMD Ryzen 7 or better
- RAM: 32 GB minimum (64 GB for large datasets)
- GPU: NVIDIA RTX 3060+ (for CloudCompare, Potree rendering)
- Software: CloudCompare, PDAL, LAStools, QGIS

---

## 5. Payload D — Combined ISR Pod (EO + IR + Laser Rangefinder)

### 5.1 Purpose

All-in-one Intelligence, Surveillance, and Reconnaissance (ISR) pod providing real-time EO/IR video with target geolocation via integrated laser rangefinder. Designed for observation, tracking, and target coordinate generation.

### 5.2 Component Selection

| Component | Model | Mass (g) | Power (W) | Price (GBP) |
|---|---|---|---|---|
| **EO Camera** | Sony IMX577 (12 MP, on Arducam USB) | 15 | 1.5 | £45 |
| **EO Lens** | M12 8 mm f/1.4 (42° HFOV) | 8 | — | £18 |
| **Thermal Camera** | FLIR Boson 320 (9 mm) | 30 | 1.0 | £1,650 |
| **Laser Rangefinder** | JRT M88B (905 nm, 1500 m, eye-safe) | 45 | 2.0 (peak) | £280 |
| **2-Axis Gimbal** | Custom (2x Dynamixel XL330) | 110 | 3.0 (peak) | £120 |
| Gimbal Controller | Dynamixel U2D2 + OpenCR | 25 | 0.5 | £55 |
| Companion Computer | NVIDIA Jetson Orin Nano (8 GB) | 60 | 15.0 (max) | £450 |
| GNSS Receiver | u-blox ZED-F9P | 18 | 0.6 | £190 |
| GNSS Antenna | Tallysman TW4722 | 22 | — | £55 |
| Video TX | Herelink Air Unit (or DJI O3) | 65 | 5.0 | £320 |
| MicroSD (Jetson) | Samsung PRO Plus 256 GB | 2 | — | £28 |
| Power regulation board | Custom (5V/12V from VBATT) | 25 | — | £20 |
| Baseplate + enclosure | 3D-printed PA12/CF + Al gimbal frame | 130 | — | £35 |
| Dovetail adapter | CNC aluminium | 60 | — | £25 |
| Germanium window | 25 mm, AR-coated | 12 | — | £85 |
| Optical dome (EO) | BK7 hemisphere 30 mm | 10 | — | £15 |
| **Total** | | **637 g** | **28.6 W (peak)** | **£3,391** |

**Power Budget Note:** 28.6 W peak draw requires careful power management. Typical sustained draw is ~22 W (LRF pulsing intermittently, gimbal not continuously slewing, Jetson at moderate load). The VBATT rail (8 A max at 14.8 V = 118 W capacity) supports this with margin.

### 5.3 Performance Specifications

**EO Channel:**

| Parameter | Value |
|---|---|
| Sensor | Sony IMX577, 1/2.3", 12.3 MP |
| Video output | 4K 30 fps / 1080p 60 fps |
| Lens | 8 mm M12, f/1.4, 42° HFOV |
| GSD at 100 m | 5.2 cm/px |
| Zoom | Digital 4x (via Jetson ISP) |

**IR Channel:**

| Parameter | Value |
|---|---|
| Sensor | FLIR Boson 320 |
| Resolution | 320x256 |
| HFOV | 24° (9 mm lens) |
| Frame rate | 9 fps (export-compliant) |
| NETD | <50 mK |

**Laser Rangefinder:**

| Parameter | Value |
|---|---|
| Model | JRT M88B |
| Range | 5-1500 m (cooperative target); 5-800 m (non-cooperative, natural surfaces) |
| Accuracy | ±1.0 m |
| Wavelength | 905 nm (eye-safe Class 1M) |
| Measurement rate | 1 Hz (continuous) or single-shot |
| Beam divergence | 3 mrad |

**Gimbal:**

| Parameter | Value |
|---|---|
| Axes | 2 (pan/tilt) |
| Pan range | ±90° (limited by fuselage) |
| Tilt range | +10° (horizon) to -90° (nadir) |
| Slew rate | 60°/s max |
| Stabilisation | Rate gyro feedback via Dynamixel PID + Jetson IMU compensation |
| Pointing accuracy | ±0.5° (stabilised) |

**Target Geolocation Accuracy:**

Geolocation uses the intersection of the LRF range vector with the WGS84 ellipsoid, refined by:
- Vehicle GNSS position (PPK-corrected to ±0.02 m)
- Vehicle attitude (FC INS, ±0.5° roll/pitch, ±1.5° heading)
- Gimbal angle (encoder, ±0.3°)
- LRF range (±1.0 m)

| Altitude (AGL) | Slant Range | Geolocation CEP (m) |
|---|---|---|
| 60 m | 85 m (45° depress) | ~2.5 m |
| 100 m | 141 m (45° depress) | ~4.0 m |
| 100 m | 100 m (nadir) | ~2.0 m |
| 200 m | 283 m (45° depress) | ~7.5 m |

*CEP = Circular Error Probable (50% of measurements within this radius). Dominated by heading error and LRF range uncertainty at long slant range.*

### 5.4 Mechanical Layout

```
           200 mm
    ┌──────────────────────┐
    │  ┌──────────────────┐│ ▲
    │  │   GNSS Antenna   ││ │
    │  └──────────────────┘│ │
    │                      │ │
    │  ┌──────────────────┐│ │
    │  │  Jetson Orin Nano││ │
    │  │  [100x79x21mm]   ││ │ 300 mm
    │  │  + carrier board ││ │
    │  └──────────────────┘│ │
    │  ┌────────┐ ┌──────┐│ │
    │  │ Video  │ │ F9P  ││ │
    │  │  TX    │ │      ││ │
    │  └────────┘ └──────┘│ │
    │       ┌──────────┐   │ │
    │       │ 2-AXIS   │   │ │
    │       │ GIMBAL   │   │ ▼
    │       │EO|IR|LRF │   │
    │       └──────────┘   │
    │ ════════════════════ │ ← Dovetail
    └──────────────────────┘

    Side view:
    ┌──────────────────────────┐ ▲
    │ GNSS   Jetson   VidTX   │ 50 mm
    │        F9P              │
    ├──────────────────────────┤
    │                          │
    │    Gimbal assembly       │ 70 mm
    │  ┌──────────────────┐    │
    │  │ EO cam │ Boson │LRF│  │
    │  │ (fwd)  │(centre)│  │  │
    │  └──────────────────┘    │
    ├──────────────────────────┤
    │  ▓▓ dome/window ▓▓      │ 15 mm
    │  ═══ dovetail ═══       │ 15 mm
    └──────────────────────────┘
     Total: ~150 mm
```

The gimbal hangs below the electronics deck. The three sensors (EO camera, Boson 320, LRF) are co-mounted on the gimbal tilt plate, boresighted in the factory/workshop to a common optical axis. The belly of the fuselage has a cut-out or dome for the gimbal's range of motion.

### 5.5 Wiring Diagram

```
    ANDERSON PP45
   ┌───────────┐
   │ +5V  (1)──┼──→ F9P +5V
   │           │──→ Gimbal controller (U2D2) +5V
   │ +12V (2)──┼──→ Boson 320 (via internal reg to 3.3V)
   │           │──→ LRF JRT M88B (12V input)
   │           │──→ Video TX 12V
   │ VBATT(3)──┼──→ Jetson Orin Nano (12-20V input via barrel)
   │ GND  (4)──┼──→ Common GND (star topology)
   └───────────┘

   JST-GH 8-PIN
   ┌────────────────┐
   │ Pin 1 (UART TX)│──→ Jetson UART RX (MAVLink v2 @ 921600)
   │ Pin 2 (UART RX)│←── Jetson UART TX
   │ Pin 3 (I2C SDA)│──→ (unused — Boson CCI via Jetson GPIO)
   │ Pin 4 (I2C SCL)│──→ (unused)
   │ Pin 5 (PWM CH1)│──→ Gimbal pan override (emergency centre)
   │ Pin 6 (PWM CH2)│──→ Gimbal tilt override (emergency stow)
   │ Pin 7 (ID0)    │──┤ 10 kΩ to 3.3V
   │ Pin 8 (ID1)    │──┤ 10 kΩ to 3.3V
   └────────────────┘

   Jetson Orin Nano Internal:
   ┌───────────────────────────────────────────────────────┐
   │ USB 3.0 port 1 ──→ Arducam IMX577 (UVC 4K)          │
   │ USB 3.0 port 2 ──→ PureThermal 3 ──→ Boson 320      │
   │ USB 2.0         ──→ Dynamixel U2D2 (gimbal servos)   │
   │ USB 2.0         ──→ ZED-F9P (UBX GNSS)               │
   │ UART (40-pin)   ──→ JRT M88B LRF (UART 19200 baud)  │
   │ GPIO (40-pin)   ──→ LRF trigger (active high pulse)  │
   │ I2C (40-pin)    ──→ Boson CCI (0x50, FFC/NUC ctrl)   │
   │ HDMI/CSI        ──→ (unused, or debug monitor)        │
   │                                                       │
   │ Ethernet (internal) ──→ Video TX (Herelink Air Unit)  │
   │   GStreamer H.264 RTP stream @ 1080p 30fps            │
   └───────────────────────────────────────────────────────┘
```

### 5.6 ArduPilot Configuration

```
# MAVLink to ISR companion on SERIAL2
SERIAL2_PROTOCOL = 2
SERIAL2_BAUD = 921

# Gimbal control (Jetson acts as gimbal manager)
MNT1_TYPE = 6              ; Gimbal via MAVLink (GIMBAL_MANAGER protocol)
MNT1_RC_RATE = 30          ; 30°/s from RC sticks
MNT1_DEFLT_MODE = 3        ; MAVLink targeting (GCS or companion)
RC6_OPTION = 213           ; Mount tilt (operator stick)
RC7_OPTION = 214           ; Mount pan (operator stick)

# Camera trigger
CAM1_TYPE = 4              ; MAVLink camera (companion handles trigger)

# Emergency gimbal stow via PWM failsafe
SERVO13_FUNCTION = 6       ; Mount pan (backup)
SERVO14_FUNCTION = 7       ; Mount tilt (backup)
```

**MAVLink Commands and Messages:**

| Command / Message | ID | Purpose |
|---|---|---|
| `GIMBAL_MANAGER_SET_PITCHYAW` | #287 | Point gimbal at target angle |
| `MAV_CMD_DO_SET_ROI_LOCATION` | 195 | Lock gimbal onto GPS coordinate |
| `MAV_CMD_DO_SET_ROI_NONE` | 197 | Release gimbal lock |
| `MAV_CMD_DO_DIGICAM_CONTROL` | 203 | Trigger EO snapshot |
| `MAV_CMD_REQUEST_VIDEO_STREAM_INFORMATION` | 2504 | Query available streams |
| `CAMERA_IMAGE_CAPTURED` | #263 | Georeferenced image metadata |
| `CAMERA_TRACKING_IMAGE_STATUS` | #275 | Object tracking box coordinates |
| `GIMBAL_DEVICE_ATTITUDE_STATUS` | #285 | Current gimbal orientation |
| `DISTANCE_SENSOR` | #132 | LRF range measurement (ISR→FC) |
| `DEBUG_FLOAT_ARRAY` | #350 | Target geolocation lat/lon/alt |
| Custom `NAMED_VALUE_FLOAT` | #251 | IR spot temp, LRF range readout |

### 5.7 Data Storage and Transmission

| Aspect | Specification |
|---|---|
| EO video recording | H.265 4K 30 fps on Jetson NVEnc, ~45 Mbit/s, ~20 GB/hr |
| IR video recording | 16-bit radiometric + 8-bit colourmap, ~4 GB/hr |
| LRF log | Text CSV (timestamp, range, azimuth, elevation), negligible |
| Geolocation log | JSON with target coords, CEP estimate, ~1 MB/hr |
| Total on-board storage | 256 GB microSD (~10 hr recording) |
| **Real-time downlink** | |
| Video TX system | Herelink Air Unit (or DJI O3 Air Unit) |
| Downlink frequency | 2.4 GHz (Herelink) or 5.8 GHz (DJI O3) |
| Downlink video | H.264 1080p 30 fps, 8-12 Mbit/s |
| Downlink range | 10-20 km (Herelink, clear LOS) |
| Downlink latency | 150-200 ms (glass-to-glass) |
| Selectable streams | EO only, IR only, PiP (EO+IR overlay), side-by-side |
| Telemetry overlay | OSD with lat/lon, alt, heading, gimbal angles, LRF range, target coords |
| MAVLink tunnel | Herelink carries MAVLink alongside video for full GCS control |

### 5.8 Processing Pipeline (Jetson Orin Nano)

The Jetson Orin Nano (40 TOPS AI performance, 8 GB RAM) runs the full ISR software stack:

```
Jetson Orin Nano (JetPack 6.x, Ubuntu 22.04)
├── GStreamer Master Pipeline
│   ├── EO: v4l2src → nvvidconv → nvv4l2h265enc → filesink (record)
│   │                           └→ nvv4l2h264enc → rtph264pay → udpsink (downlink)
│   ├── IR: v4l2src (raw16) → custom colormap (CUDA) → overlay compositor
│   └── Compositor: EO + IR → PiP or blend → encoder → downlink
│
├── Gimbal Manager (C++ / ROS2 node)
│   ├── MAVLink GIMBAL_MANAGER protocol handler
│   ├── Dynamixel SDK: PID control loop at 100 Hz
│   ├── FC attitude feed-forward for stabilisation
│   └── ROI geo-pointing: lat/lon → gimbal angles via geodetic math
│
├── Target Geolocator (Python)
│   ├── Inputs: vehicle lat/lon/alt, attitude quat, gimbal angles, LRF range
│   ├── Algorithm: ray-casting from sensor through WGS84 ellipsoid
│   ├── Output: target lat/lon/alt/CEP → MAVLink + OSD overlay + log
│   └── MGRS/UTM grid reference generation
│
├── Object Tracker (TensorRT)
│   ├── Detection: YOLOv8-nano (person/vehicle), ~30 fps on Orin Nano
│   ├── Tracking: ByteTrack (centroid + IoU association)
│   ├── Output: bounding box → gimbal auto-track feedback loop
│   └── IR detection: fine-tuned on FLIR ADAS thermal dataset
│
├── LRF Driver (Python, serial)
│   ├── JRT M88B UART protocol handler
│   ├── Trigger: single-shot on operator command or auto (1 Hz)
│   └── Output: range → geolocator + MAVLink DISTANCE_SENSOR
│
├── MAVLink Router (mavlink-routerd)
│   ├── FC UART ↔ Jetson (all vehicle telemetry)
│   ├── Jetson apps (multiple endpoints)
│   └── GCS via Herelink tunnel
│
└── GNSS Logger (gpsd + custom)
    ├── ZED-F9P UBX raw observations → file (for PPK post-mission)
    └── Real-time NMEA → geolocator
```

---

## 6. Comparative Summary

| Parameter | A: EO Camera | B: IR/Thermal | C: LiDAR | D: ISR Pod |
|---|---|---|---|---|
| Total mass | 384 g | 248 g | 640 g | 637 g |
| Peak power | 8.7 W | 8.3 W | 20.0 W | 28.6 W |
| Typical power | 8.0 W | 7.5 W | 18.0 W | 22.0 W |
| Estimated cost | £1,029 | £2,027 | £1,962 | £3,391 |
| Data rate | ~5 MB/s (stills) | ~3 MB/s | ~3.3 MB/s | ~8 MB/s |
| Storage/hr | 14 GB (JPEG) | 11 GB | 12 GB | 24 GB |
| Real-time downlink | 1 fps preview | Yes (320x256 thermal) | No (stats only) | Yes (1080p 30fps) |
| Companion computer | RPi CM4 (4 GB) | RPi CM4 (4 GB) | RPi 5 (8 GB) | Jetson Orin Nano |
| Endurance impact* | ~5% reduction | ~4% reduction | ~12% reduction | ~18% reduction |

*Endurance impact estimated from power draw relative to propulsion system. Assumes ~150 W propulsion at cruise.*

---

## 7. Standard Integration Procedures

### 7.1 Pre-Flight Checklist (All Payloads)

1. Slide payload module into dovetail rail until latch clicks
2. Verify Anderson PP45 seated (check 5V/12V LEDs on payload PCB)
3. Verify JST-GH data cable connected (check MAVLink heartbeat on GCS)
4. Verify GPIO ID0/ID1 read correctly (GCS displays detected payload type)
5. Payload-specific power-on self-test (see individual module checklists)
6. Verify data storage media inserted and writable
7. Verify companion computer boot complete (MAVLink STATUSTEXT: "PLDx READY")
8. For Payload C/D: verify GNSS lock on ZED-F9P (min 6 satellites, PDOP < 3.0)

### 7.2 ArduPilot Auto-Detection Script

On boot, the FC reads GPIO ID0/ID1 ADC values and runs a Lua script:

```lua
-- payload_detect.lua (runs on Pixhawk)
local ID0_PIN = 54  -- AUX6
local ID1_PIN = 55  -- AUX7

function update()
    local v0 = analogRead(ID0_PIN)  -- 0-3.3V mapped to 0-1023
    local v1 = analogRead(ID1_PIN)

    if v0 > 200 and v0 < 400 and v1 < 100 then
        -- 10k divider = ~1.65V → ADC ~512... (simplified)
        gcs:send_text(6, "Payload A (EO Camera) detected")
        param:set("CAM1_TYPE", 1)
        param:set("CAM1_TRIGG_DIST", 50)
    elseif v0 > 600 and v0 < 800 and v1 < 100 then
        gcs:send_text(6, "Payload B (IR/Thermal) detected")
    elseif v0 > 900 and v1 < 100 then
        gcs:send_text(6, "Payload C (LiDAR) detected")
        param:set("RNGFND1_TYPE", 10)
    elseif v0 > 200 and v0 < 400 and v1 > 200 and v1 < 400 then
        gcs:send_text(6, "Payload D (ISR Pod) detected")
        param:set("MNT1_TYPE", 6)
    else
        gcs:send_text(4, "WARNING: Unknown payload or no payload")
    end

    return update, 5000  -- re-check every 5 seconds
end

return update()
```

### 7.3 Vibration Isolation

All payloads use a common vibration isolation strategy:
- 4x M3 silicone grommets (Shore 30A) between sensor plate and baseplate
- Natural frequency target: 8-12 Hz (below dominant airframe vibration band)
- Critical for LiDAR (point cloud noise) and EO camera (image blur)
- IMU-equipped payloads (C, D) must have IMU rigidly attached to sensor plate (not isolated separately)

---

## 8. Regulatory and Compliance Notes

| Aspect | Requirement |
|---|---|
| ITAR/EAR | FLIR Boson: 9 fps frame rate limit on export variants. Verify EAR99 classification for destination country. |
| Eye safety | LRF JRT M88B: Class 1M at 905 nm. Complies with IEC 60825-1. Must be labelled. |
| LiDAR | Livox Mid-360: Class 1 eye-safe (905 nm). No restrictions. |
| RF emissions | Video TX (Herelink/DJI): requires spectrum allocation per local authority. UK: Ofcom WT licence for airborne use above 2W EIRP. |
| UAV operations | All payloads must be declared in operating mass. Combined UAV+payload MTOW determines CAA category (UK: Open <25 kg, Specific >25 kg). |
| Data protection | IR/EO capable of identifying individuals. GDPR (UK GDPR) applies if operating over populated areas. Data processing impact assessment required. |

---

## 9. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-03-15 | UAV Systems Engineering | Initial release — all four payload modules |

---

*End of document PLD-SPEC-001 v1.0*
