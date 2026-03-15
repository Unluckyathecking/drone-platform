# Electro-Optical Daylight Camera Payloads for Mini Fixed-Wing UAV: Technical Specification

## Platform Reference Parameters

| Parameter | Value |
|---|---|
| Wingspan | 2–4 m |
| Max payload capacity | 4 kg |
| Payload bay dimensions | 200 × 300 × 150 mm (W × L × H) |
| Autopilot | ArduPilot on Pixhawk (4.x firmware) |
| Propulsion | Pusher propeller configuration |
| Typical cruise speed | 15–25 m/s (54–90 km/h) |
| Typical endurance | 45–90 min (battery-dependent) |
| Operating altitude AGL | 50–150 m |
| Power bus | 4S–6S LiPo (14.8–22.2 V nominal), 5V/12V regulated rails |

The pusher-prop configuration is significant: the camera payload sits in the nose or belly, forward of the CG, with clean airflow and reduced vibration compared to tractor configurations. However, the prop wash over tail surfaces during climb can induce pitch oscillations that the gimbal must compensate for.

---

## 1. Sensor Comparison

### 1.1 Sensor Summary Table

| Parameter | Sony IMX477 (RPi HQ Cam) | Sony RX0 II | Sony A6000 | RunCam 2 | Siyi A8 mini | DJI Zenmuse P1 (ref) |
|---|---|---|---|---|---|---|
| **Sensor format** | 1/2.3" (7.9×6.3 mm) | 1.0" (13.2×8.8 mm) | APS-C (23.5×15.6 mm) | 1/2.3" (~6.2×4.6 mm) | 1/1.8" (~7.4×5.6 mm) | Full-frame (35.9×24.0 mm) |
| **Effective megapixels** | 12.3 MP (4056×3040) | 15.3 MP (4800×3200) | 24.3 MP (6000×4000) | 4.0 MP (1920×1080 native sensor ~16 MP, output 1080p) | 8.0 MP (3840×2160 stills, 4K video) | 45 MP (8192×5460) |
| **Pixel pitch** | 1.55 µm | 2.4 µm | 3.92 µm | ~1.34 µm (effective) | ~1.85 µm | 4.4 µm |
| **Dynamic range** | ~10.5 stops | ~13 stops | ~13.1 stops (at base ISO) | ~8 stops | ~10 stops (est.) | ~14.5 stops |
| **Weight (body only)** | ~50 g (board camera) | 132 g | 344 g (body only) | 49 g | 95 g (integrated gimbal+camera) | 800 g (camera only, no gimbal) |
| **System weight (w/ lens, mount)** | 80–120 g | 132 g (fixed lens) | 500–650 g (w/ pancake lens) | 49 g | 95 g | 1480 g (w/ 35mm lens, no gimbal) |
| **Street price (USD, 2025)** | $50–60 | $650–700 | $450–550 (used) | $60–80 | $250–350 | $5,800+ |
| **Primary interface** | MIPI CSI-2 (2-lane or 4-lane) | Micro HDMI, USB-C | Micro HDMI, USB, WiFi | AV out (analog), micro-USB | Ethernet (IP video), UART | DJI proprietary (SkyPort) |
| **Max still resolution** | 4056×3040 | 4800×3200 | 6000×4000 | 1920×1080 (stills = video frame) | 3840×2160 | 8192×5460 |
| **Max video** | 1080p30 (native ISP), 4K via libcamera raw+encode | 4K 30fps, 1080p 60fps | 1080p 60fps (no 4K) | 1080p 60fps | 4K 30fps, 1080p 60fps | 4K 60fps |
| **Video codecs** | H.264 (via Pi encoder), H.265 (Pi 5) | XAVC-S (H.264) | AVCHD (H.264), XAVC-S | H.264 | H.264, H.265 | H.264, H.265 |
| **Shutter type** | Rolling (electronic) | Rolling (electronic) | Mechanical focal-plane + electronic | Rolling (electronic) | Rolling (electronic) | Mechanical focal-plane shutter |
| **Trigger interface** | Software (libcamera), GPIO | IR remote, USB (limited) | Multi-terminal, IR, USB (PTP/MTP) | Button only (no remote trigger natively) | UART command, Ethernet | DJI SkyPort/PSDK |
| **ArduPilot integration** | Excellent (via companion Pi, MAVLink relay trigger on GPIO) | Poor (manual or IR hack) | Good (servo on multi-terminal connector, or Seagull #MAP2) | Very poor | Good (Siyi SDK over UART/Ethernet, MavLink compatible) | None (DJI ecosystem only) |

### 1.2 Detailed Sensor Analysis

#### Sony IMX477 (Raspberry Pi HQ Camera)

The IMX477 is a back-side-illuminated (BSI) 1/2.3-inch CMOS sensor with 12.3 effective megapixels. Its primary advantage in UAV applications is the direct MIPI CSI-2 interface to a Raspberry Pi companion computer, which provides complete software control over exposure, gain, white balance, and — critically — shutter trigger timing synchronized to ArduPilot waypoints.

The sensor's quantum efficiency peaks around 550 nm at approximately 70%, which is respectable for its class. The small pixel pitch (1.55 µm) means diffraction limiting begins around f/2.8, so lenses should not be stopped down beyond f/4 to preserve resolving power. The rolling shutter readout time is approximately 28 ms for full frame, which at a ground speed of 20 m/s and 100 m AGL produces approximately 0.56 m of image smear — noticeable in photogrammetry but manageable with a fast shutter speed of 1/1000 s or faster (reducing effective smear from the rolling shutter's progressive readout to about 0.4–0.5 pixels).

The C/CS-mount lens interface allows use of high-quality industrial machine-vision lenses, many of which have published distortion curves. This is a significant advantage for photogrammetry.

**Key limitation:** The Pi's hardware ISP can process full-resolution stills at approximately 1 fps for raw capture (DNG) or approximately 2–3 fps for JPEG. For rapid survey triggering at high ground speed, this limits minimum trigger interval. Using `rpicam-still` with the `--immediate` flag and a pre-allocated buffer, achievable rates are roughly 1.5–2 Hz for full-resolution JPEG stills.

#### Sony RX0 II

The RX0 II packs a 1.0-inch Exmor RS sensor into a 59×40.5×35 mm body weighing 132 g. The 1-inch sensor class represents a significant step up from 1/2.3" in terms of per-pixel light gathering (about 2.4× the pixel area). The Zeiss Tessar 7.9 mm f/4.0 fixed lens provides a 24 mm equivalent field of view (approximately 84° diagonal).

Dynamic range at base ISO (125) is approximately 13 stops, competitive with much larger cameras. The fixed wide-angle lens means GSD is determined solely by altitude — there is no option to swap to a longer focal length for higher resolution at a given height.

**Integration challenge:** The camera lacks a wired remote trigger input. The multi-terminal connector supports charging and data but not shutter release. Triggering options are limited to: (a) IR remote emitter aimed at the front of the camera, which is unreliable in a vibrating payload bay; (b) Sony Imaging Edge Mobile app over WiFi, introducing unpredictable latency; or (c) a mechanical servo pressing the physical shutter button, which is crude but functional. None of these provide the sub-10 ms trigger accuracy needed for precision photogrammetry. This camera is better suited as a continuously recording video source from which frames are extracted in post-processing.

#### Sony A6000 (ILCE-6000)

The A6000 remains a workhorse for budget UAV photogrammetry. Its APS-C sensor (23.5×15.6 mm, 24.3 MP) delivers GSD performance that approaches professional mapping cameras at a fraction of the cost. The 3.92 µm pixel pitch provides good signal-to-noise ratio and is well above the diffraction limit for lenses up to approximately f/8.

The mechanical shutter is a crucial feature. It eliminates rolling shutter artifacts entirely at any ground speed, producing geometrically accurate frames essential for photogrammetric bundle adjustment. The shutter is rated to approximately 100,000 actuations.

**Weight is the primary concern.** Body weight is 344 g; add a Sony E 20mm f/2.8 pancake lens (69 g), a Seagull #MAP2 trigger interface (15 g), and a stabilized gimbal (200–400 g), and total system weight approaches 650–850 g before wiring and mounting hardware. This is manageable within the 4 kg payload budget but represents 16–21% of the total allocation.

Triggering is well-proven: the Seagull #MAP2 or Stratosnapper v2 boards convert ArduPilot's PWM camera trigger signal (or MAVLink `DO_DIGICAM_CONTROL` commands) to the Sony multi-terminal protocol. Trigger latency is approximately 50–80 ms, which must be accounted for in trigger distance calculations. Hot-shoe feedback confirms shutter actuation for log synchronization.

The A6000 can sustain approximately 3 fps in continuous shooting mode with auto-exposure, or up to 11 fps in burst mode (but with fixed exposure and focus from the first frame). For survey work at 20 m/s with 80% forward overlap and a 20mm lens at 100 m AGL, trigger interval is approximately 2.5 s — easily within single-shot cadence.

**Power:** The A6000 draws approximately 3–4 W during operation. The internal NP-FW50 battery (7.2 Wh) lasts roughly 90 minutes of continuous shooting. For longer missions, a dummy battery adapter connected to a regulated 7.4 V supply from the aircraft's power bus is recommended.

#### RunCam 2

The RunCam 2 is an action camera designed for FPV racing, not surveying. It is included here because its 49 g weight and compact form factor (38.5×38.5×29.5 mm) make it the lightest option, and it is commonly used as a secondary recording camera on small UAVs.

The 1/2.3-inch sensor is comparable in size to the IMX477 but has significantly lower effective resolution (the sensor may be 16 MP natively, but output is capped at 1080p). The 120° FOV fixed lens introduces substantial barrel distortion (>5% at edges) that complicates photogrammetric use.

**There is no remote trigger capability.** The camera starts recording when powered on (configurable) and stops when powered off. It is purely a continuous video recorder. Frame extraction from 1080p video yields 2.1 MP effective stills — insufficient for serious mapping work but adequate for situational awareness recording.

The primary role of a RunCam 2 in this airframe is as a dedicated recording camera for flight documentation or as a forward-facing situational awareness camera, not as the primary survey sensor.

#### Siyi A8 mini

The Siyi A8 mini is an integrated camera-gimbal unit designed specifically for small UAVs. It combines an 8 MP 1/1.8-inch sensor with a 3-axis stabilized gimbal in a single unit weighing approximately 95 g. This all-in-one design eliminates the need to source and integrate separate camera, gimbal, and controller components.

The gimbal provides ±150° yaw, -90° to +25° pitch, and ±45° roll stabilization. Stabilization accuracy is specified as ±0.01° (though real-world performance on a vibrating fixed-wing in turbulence is more likely ±0.05–0.1°).

**Interface:** Ethernet output for IP video streaming (H.264/H.265 at up to 4K 30fps or 1080p 60fps), and UART for gimbal control commands. The Siyi SDK provides a MAVLink-compatible command protocol, and ArduPilot has native mount driver support for Siyi gimbals (`MNT_TYPE=8` as of ArduPilot 4.4+). This means the autopilot can directly control gimbal pointing (for tracking, region-of-interest hold, and nadir lock during survey) and can trigger image capture via MAVLink.

The 1/1.8-inch sensor sits between the IMX477's 1/2.3" and the RX0 II's 1.0", offering a reasonable compromise. Pixel pitch of approximately 1.85 µm is small but adequate for daylight operations.

**Key advantage:** Turnkey integration. Mount it, wire Ethernet to a companion computer and UART to the Pixhawk, and the system works. No gimbal tuning, no camera trigger boards, no vibration isolation design.

**Key limitation:** The fixed wide-angle lens (approximately 80° HFOV) cannot be changed. GSD at altitude is determined entirely by flight height. For high-resolution photogrammetry, the A6000 with a suitable lens will significantly outperform it.

#### DJI Zenmuse P1 (Reference Baseline)

The Zenmuse P1 is included as the professional reference against which the practical options are benchmarked. Its full-frame 45 MP sensor with interchangeable lenses (24mm, 35mm, 50mm DJI DL-mount primes) and mechanical global shutter represents the current state-of-the-art for survey-grade aerial photogrammetry.

At 1480 g (with 35mm lens) before gimbal and mounting, it exceeds the weight budget of many payload bays in this UAV class, and its 800 g camera-only weight (without lens) already approaches many complete integrated systems.

It is included to calibrate expectations: when you see GSD numbers for the other sensors at a given altitude, the P1 numbers show what professional survey equipment achieves. The gap informs decisions about acceptable quality levels.

### 1.3 Ground Sample Distance Calculations

GSD is calculated as:

```
GSD = (H × p) / f
```

where:
- H = altitude AGL (m)
- p = pixel pitch (µm)
- f = focal length (mm)

For sensors with fixed lenses, the focal length is determined. For interchangeable lens sensors, a representative lens is chosen.

#### Lens Assignments for GSD Calculation

| Camera | Lens | Focal length (mm) | Notes |
|---|---|---|---|
| IMX477 | 6mm f/1.2 C-mount | 6.0 | Common choice for wide survey |
| IMX477 | 16mm f/1.4 C-mount | 16.0 | Narrow, higher resolution option |
| RX0 II | Built-in Zeiss 7.9mm f/4 | 7.9 | Fixed, not interchangeable |
| A6000 | Sony E 20mm f/2.8 | 20.0 | Compact pancake lens |
| A6000 | Sony E 35mm f/1.8 OSS | 35.0 | Higher GSD option |
| RunCam 2 | Built-in 2.5mm f/2.0 | 2.5 | Fixed wide-angle |
| Siyi A8 mini | Built-in ~4.5mm | 4.5 | Fixed, approximate |
| Zenmuse P1 | DJI DL 35mm f/2.8 | 35.0 | Standard survey lens |

#### GSD Results (cm/pixel)

**At 50 m AGL:**

| Camera + Lens | GSD (cm/px) | Footprint W×H (m) |
|---|---|---|
| IMX477 + 6mm | 1.29 | 52.3 × 39.2 |
| IMX477 + 16mm | 0.48 | 19.6 × 14.7 |
| RX0 II + 7.9mm | 1.52 | 73.0 × 48.6 |
| A6000 + 20mm | 0.98 | 58.8 × 39.2 |
| A6000 + 35mm | 0.56 | 33.6 × 22.4 |
| RunCam 2 | 2.68 | 51.4 × 28.9 |
| Siyi A8 mini + 4.5mm | 2.06 | 79.1 × 59.3 |
| Zenmuse P1 + 35mm | 0.63 | 51.5 × 34.3 |

**At 80 m AGL:**

| Camera + Lens | GSD (cm/px) | Footprint W×H (m) |
|---|---|---|
| IMX477 + 6mm | 2.07 | 83.7 × 62.7 |
| IMX477 + 16mm | 0.78 | 31.3 × 23.5 |
| RX0 II + 7.9mm | 2.43 | 116.8 × 77.8 |
| A6000 + 20mm | 1.57 | 94.1 × 62.7 |
| A6000 + 35mm | 0.90 | 53.7 × 35.8 |
| RunCam 2 | 4.29 | 82.3 × 46.3 |
| Siyi A8 mini + 4.5mm | 3.29 | 126.5 × 94.9 |
| Zenmuse P1 + 35mm | 1.01 | 82.4 × 54.9 |

**At 100 m AGL:**

| Camera + Lens | GSD (cm/px) | Footprint W×H (m) |
|---|---|---|
| IMX477 + 6mm | 2.58 | 104.7 × 78.4 |
| IMX477 + 16mm | 0.97 | 39.2 × 29.3 |
| RX0 II + 7.9mm | 3.04 | 145.9 × 97.3 |
| A6000 + 20mm | 1.96 | 117.6 × 78.4 |
| A6000 + 35mm | 1.12 | 67.1 × 44.7 |
| RunCam 2 | 5.36 | 102.9 × 57.9 |
| Siyi A8 mini + 4.5mm | 4.11 | 158.2 × 118.6 |
| Zenmuse P1 + 35mm | 1.26 | 103.0 × 68.7 |

**At 120 m AGL:**

| Camera + Lens | GSD (cm/px) | Footprint W×H (m) |
|---|---|---|
| IMX477 + 6mm | 3.10 | 125.6 × 94.1 |
| IMX477 + 16mm | 1.16 | 47.0 × 35.2 |
| RX0 II + 7.9mm | 3.65 | 175.1 × 116.7 |
| A6000 + 20mm | 2.35 | 141.1 × 94.1 |
| A6000 + 35mm | 1.34 | 80.6 × 53.7 |
| RunCam 2 | 6.43 | 123.5 × 69.5 |
| Siyi A8 mini + 4.5mm | 4.93 | 189.8 × 142.3 |
| Zenmuse P1 + 35mm | 1.51 | 123.6 × 82.4 |

**Analysis:** The A6000 with a 35mm lens achieves GSD competitive with the Zenmuse P1 at every altitude, at roughly 1/10th the cost and 1/2 the weight. The IMX477 with a 16mm lens achieves the best GSD of any non-reference sensor due to the combination of relatively long focal length and small pixel pitch, but at the cost of a very narrow footprint requiring more flight lines for area coverage.

For general-purpose mapping at 100 m AGL, a GSD target of 2–3 cm/px is achievable with the A6000 + 20mm, IMX477 + 6mm, or RX0 II, which provide the best balance of coverage area and resolution.

### 1.4 Sensor Selection Recommendations by Mission

| Mission Type | Primary Recommendation | Secondary | Rationale |
|---|---|---|---|
| Precision photogrammetry / mapping | A6000 + 20mm f/2.8 | IMX477 + 16mm | Mechanical shutter, high MP, proven calibration |
| SAR / wide-area surveillance | Siyi A8 mini | RX0 II | Wide FOV, real-time video, integrated gimbal |
| Infrastructure inspection | A6000 + 35mm f/1.8 | IMX477 + 16mm | High GSD for detail at safe standoff distance |
| General ISR / video recording | Siyi A8 mini | RunCam 2 (secondary) | Real-time streaming, gimbal stabilization |
| Minimum weight / maximum endurance | IMX477 + 6mm | RunCam 2 | Under 120 g total system |

---

## 2. Lens Selection

### 2.1 Fundamental Tradeoffs

The relationship between focal length, field of view, and GSD forms the central design tension in aerial camera payloads:

**Focal length vs. FOV** (for a given sensor size):

```
HFOV = 2 × arctan(sensor_width / (2 × f))
```

| Equivalent FOV class | Diagonal FOV | Typical use |
|---|---|---|
| Ultra-wide | >100° | SAR, situational awareness |
| Wide | 70–100° | General survey, medium resolution mapping |
| Normal | 40–70° | Precision mapping, inspection |
| Narrow / telephoto | <40° | Detail inspection, target identification |

**The coverage-resolution paradox:** A wider lens covers more ground per image (fewer flight lines, faster survey), but each pixel covers more ground (lower GSD). A narrower lens yields higher GSD but requires more flight lines and more images for the same area, increasing flight time, processing time, and storage requirements.

**Quantified example at 100 m AGL with the A6000 (23.5 mm sensor width):**

| Lens | HFOV (°) | Footprint width (m) | GSD (cm/px) | Flight lines for 1 km wide area (60% side overlap) |
|---|---|---|---|---|
| 16mm f/2.8 | 72.5 | 147 | 2.72 | 2 |
| 20mm f/2.8 | 60.8 | 118 | 1.96 | 3 |
| 35mm f/1.8 | 37.1 | 67 | 1.12 | 5 |
| 50mm f/1.8 | 26.4 | 47 | 0.78 | 8 |

The 20mm lens represents the sweet spot for most mapping missions on this platform: 3 flight lines for a 1 km swath at 60% sidelap with sub-2 cm GSD at 100 m.

### 2.2 Specific Lens Recommendations

#### For Sony IMX477 (C/CS-mount)

| Lens | Focal Length | Aperture | HFOV (on 1/2.3") | Weight | Price | Distortion | Notes |
|---|---|---|---|---|---|---|---|
| Arducam 6mm CS-mount | 6 mm | f/1.2 | ~63° | 34 g | $25 | ~3% barrel | Default RPi HQ lens, plastic barrel |
| Arducam 16mm C-mount | 16 mm | f/1.4 | ~27° | 45 g | $30 | <1% barrel | Narrow FOV, high GSD |
| Kowa LM6HC | 6 mm | f/1.4 | ~63° | 52 g | $120 | <0.5% | Industrial grade, metal barrel, calibrated |
| Computar M0814-MP2 | 8 mm | f/1.4 | ~49° | 38 g | $85 | <1% | Good compromise FOV/resolution |
| Edmund Optics 8.5mm | 8.5 mm | f/1.3 | ~46° | 42 g | $150 | <0.3% | Low distortion, excellent MTF |

**Recommendation:** For photogrammetry, the Kowa LM6HC (6mm) or Edmund Optics 8.5mm provides the optical quality needed for consistent calibration. The Arducam lenses are adequate for video/ISR but introduce enough distortion variation unit-to-unit that individual lens calibration is essential for mapping.

#### For Sony A6000 (Sony E-mount)

| Lens | Focal Length | Aperture | HFOV (on APS-C) | Weight | Price | Distortion | Notes |
|---|---|---|---|---|---|---|---|
| Sony E 16mm f/2.8 (SEL16F28) | 16 mm | f/2.8 | 73° | 67 g | $250 | ~2.5% barrel | Widest native E pancake, some softness at corners |
| Sony E 20mm f/2.8 (SEL20F28) | 20 mm | f/2.8 | 61° | 69 g | $350 | ~1.5% barrel | Sharp center, acceptable corners. Best all-rounder |
| Sigma 19mm f/2.8 DN Art | 19 mm | f/2.8 | 63° | 160 g | $170 | ~1% barrel | Sharper than Sony 20mm, but heavier |
| Sony E 35mm f/1.8 OSS (SEL35F18) | 35 mm | f/1.8 | 37° | 154 g | $400 | <0.5% pincushion | Built-in OSS stabilization (can disable for gimbal use) |
| Voigtländer 15mm f/4.5 III | 15 mm | f/4.5 | 77° | 78 g | $500 | ~3% barrel | Manual focus, rectilinear ultra-wide |

**Recommendation:** The Sony 20mm f/2.8 pancake is the standard choice — light, compact (20.4 mm flange-to-tip), sharp enough at f/4, and the most commonly calibrated E-mount lens in OpenDroneMap and Agisoft lens databases. For higher resolution work, the 35mm f/1.8 is excellent but doubles the required flight lines.

#### For Sensors with Fixed Lenses

The RX0 II (7.9mm f/4.0 Zeiss), RunCam 2 (2.5mm f/2.0), and Siyi A8 mini (~4.5mm) have non-interchangeable lenses. Selection is binary: use the camera or don't.

### 2.3 Distortion Characteristics and Calibration

All lenses exhibit geometric distortion that must be modeled and corrected for photogrammetric use. The standard Brown-Conrady distortion model uses:

```
x_distorted = x(1 + k1*r² + k2*r⁴ + k3*r⁶) + 2*p1*x*y + p2*(r² + 2*x²)
y_distorted = y(1 + k1*r² + k2*r⁴ + k3*r⁶) + p1*(r² + 2*y²) + 2*p2*x*y
```

where k1, k2, k3 are radial distortion coefficients and p1, p2 are tangential (decentering) distortion coefficients.

**Calibration methods ranked by accuracy:**

1. **Laboratory calibration with calibration target** (checkerboard or dot grid) using OpenCV `cv2.calibrateCamera()` — achieves sub-pixel reprojection error (<0.3 px). Requires printing a precision target and capturing 20–50 images at various angles. Should be performed once per lens and repeated if the lens is removed/remounted.

2. **Self-calibration during photogrammetric processing** — Agisoft Metashape and OpenDroneMap can estimate lens parameters from the survey images themselves during bundle adjustment. This works well when there is high overlap (>70%) and geometric diversity in the scene. Typical reprojection error: 0.5–1.0 px.

3. **Pre-loaded lens profiles** — Agisoft, Pix4D, and Adobe Camera Raw maintain databases of common lens profiles. The Sony 20mm f/2.8 is well-characterized. Less common lenses (Arducam C-mount, Siyi integrated) may not have profiles available.

**Critical note on the IMX477:** Because C/CS-mount lenses can be rotated and their back-focus distance adjusted, the distortion model changes every time the lens is physically disturbed. For repeatable photogrammetric results, the lens should be locked with thread-locking compound (Loctite 222 or equivalent) after focus is set, and the assembly calibrated as a unit. Mark the rotational alignment of the lens barrel to the sensor board.

**Distortion magnitude by lens class:**

| Lens type | Typical max radial distortion | Calibration necessity |
|---|---|---|
| Ultra-wide (>90° FOV) | 5–15% barrel | Absolutely essential |
| Wide (60–90° FOV) | 1–5% barrel | Required for photogrammetry |
| Normal (40–60° FOV) | 0.5–2% barrel or pincushion | Recommended |
| Narrow (<40° FOV) | <0.5% | Optional but improves results |

---

## 3. Gimbal Engineering

### 3.1 The Case for Stabilization on Fixed-Wing Platforms

Fixed-wing UAVs in the 2–4 m class experience the following in-flight disturbances:

| Source | Frequency range | Amplitude (angular) | Notes |
|---|---|---|---|
| Propeller vibration | 50–200 Hz | 0.5–5° (at sensor, without isolation) | Dominant source. Pusher config helps |
| Wind gust response | 0.1–2 Hz | 2–15° (bank and pitch) | Depends on wing loading |
| Turbulence | 1–10 Hz | 1–5° | Thermal convection, terrain effects |
| Control surface actuation | 2–10 Hz | 0.5–3° | Autopilot corrections |
| Engine torque oscillation | 20–100 Hz | 0.2–1° | Electric motor cogging |

Without stabilization, a nadir-pointing camera at 100 m AGL with 5° pitch deviation shifts the image center by 8.7 m on the ground, creating gaps in coverage that break photogrammetric processing. Even 1° of uncompensated roll at the moment of shutter actuation shifts the footprint by 1.7 m and introduces perspective distortion.

**Stabilization is not optional for survey-grade work.** However, the degree of stabilization needed varies by mission.

### 3.2 2-Axis vs 3-Axis Tradeoffs

| Factor | 2-Axis (Pitch + Roll) | 3-Axis (Pitch + Roll + Yaw) |
|---|---|---|
| Weight (typical) | 80–200 g | 150–400 g |
| Complexity | Moderate | High |
| Power consumption | 2–5 W | 4–10 W |
| Nadir stability | Excellent — compensates the two most critical axes | Excellent + heading hold |
| Yaw compensation | None — accepts aircraft heading changes | Maintains absolute heading |
| Forward oblique pointing | Pitch axis provides this | Full hemisphere pointing |
| Use case fit | Survey/mapping (nadir), fixed forward-look | ISR, tracking, oblique photography |
| Integration difficulty | Simple — two motor axes, rectangular envelope | Complex — nested motor frames, cable routing |
| Payload bay compatibility | Usually fits within 200×300×150 mm | May exceed 150 mm height with camera |

**Recommendation for this platform:** A 2-axis gimbal (pitch + roll) is sufficient for photogrammetric survey missions where the camera points nadir or at a fixed oblique angle. The aircraft's heading is controlled by the autopilot along survey lines, and small yaw deviations are handled by the high overlap between frames.

For ISR/surveillance missions requiring a steerable, pointing camera (e.g., tracking a moving vehicle while the aircraft orbits), a 3-axis gimbal or the integrated Siyi A8 (which is 3-axis) is necessary.

### 3.3 Specific Gimbal Options

#### Siyi A8 mini (Integrated 3-Axis)

- **Type:** Brushless direct-drive, 3-axis
- **Weight:** 95 g (complete with camera)
- **Payload capacity:** N/A (camera is integrated)
- **Stabilization accuracy:** ±0.01° specified, ±0.05° realistic
- **Control input:** UART (Siyi protocol, MAVLink-compatible), Ethernet
- **Power:** 10–26 V input, ~5 W typical
- **Pros:** Turnkey, lightest complete system, ArduPilot native support
- **Cons:** Cannot change camera/lens, 8 MP sensor limits GSD, 1/1.8" sensor

#### Storm32 BGC (Open-Source 3-Axis Controller)

- **Type:** Brushless gimbal controller board (requires separate gimbal mechanics and motors)
- **Board weight:** ~15 g
- **Compatible gimbal frames:** Various 3D-printed or aluminum CNC frames for GoPro/similar sized cameras
- **Typical complete gimbal weight with camera:** 200–400 g
- **Stabilization accuracy:** ±0.05–0.1° (depends heavily on tuning and motor quality)
- **Control input:** UART (MAVLink native), PWM
- **Power:** 2S–6S LiPo direct input, ~6–12 W with motors
- **Firmware:** Open-source STorM32 firmware with active community
- **ArduPilot integration:** Native support (`MNT_TYPE=4`). ArduPilot sends angle commands via MAVLink `MOUNT_CONTROL` messages. Storm32 responds with `MOUNT_STATUS` for camera pointing feedback.
- **Pros:** Highly configurable, open source, community support, MAVLink native
- **Cons:** Requires significant tuning effort (PID loops for each axis), mechanical assembly quality determines performance ceiling, no integrated camera

**To use with the A6000:** A Storm32 controller paired with a 3D-printed or machined aluminum 2-axis frame (pitch + roll) sized for the A6000 + 20mm lens. Total gimbal frame + motors weight: approximately 150–250 g. Complete system (controller + frame + motors + A6000 + 20mm lens + wiring): approximately 600–800 g.

#### SimpleBGC 32-bit (AlexMos)

- **Type:** Commercial brushless gimbal controller, 3-axis (the industry standard for custom gimbal builds)
- **Board weight:** ~20 g (32-bit Extended version with encoder support)
- **Compatible gimbal frames:** Virtually any. Wide ecosystem of commercial frames.
- **Typical complete gimbal weight with A6000:** 300–500 g (frame + motors)
- **Stabilization accuracy:** ±0.01–0.02° (with encoder feedback motors)
- **Control input:** UART (serial API), PWM, analog joystick, CAN bus
- **Power:** 8–26 V, ~8–15 W with motors
- **Software:** SimpleBGC GUI (Windows/Mac) for tuning. Extensive PID, notch filter, and follow mode parameters.
- **ArduPilot integration:** Supported via `MNT_TYPE=6` (AlexMos serial). The integration is less elegant than Storm32 MAVLink — it uses a proprietary serial protocol that ArduPilot translates. Functional but with fewer features exposed.
- **Pros:** Best-in-class stabilization performance, encoder support eliminates drift, extensive tuning tools, commercial support
- **Cons:** More expensive (~$150–250 for controller + encoder board), requires careful PID tuning, proprietary protocol

#### Servo-Based Gimbal (Budget Option)

- **Type:** Two standard or digital servos (e.g., MG90S, MG996R, or Blue Bird BMS-115) in a tilt-pan bracket
- **Weight:** 50–120 g complete (depending on servo size)
- **Stabilization accuracy:** ±0.5–2° (servos lack the bandwidth for vibration rejection)
- **Control input:** PWM directly from Pixhawk servo outputs
- **Power:** 5–6 V from BEC, 0.5–2 W
- **ArduPilot integration:** Native and trivial — `MNT_TYPE=1` (servo). Assign two RC output channels to mount pitch and roll functions. ArduPilot outputs the corrected PWM signal based on the aircraft's IMU data.
- **Pros:** Cheapest option (<$30), simplest integration, lightest
- **Cons:** Cannot reject vibration (servo bandwidth ~10 Hz vs vibration at 50–200 Hz), audible noise, backlash in gears introduces pointing error, limited lifespan under vibration

**Servo gimbals are inadequate for photogrammetry** but acceptable for coarse pointing of a video camera during ISR missions where real-time viewing matters more than geometric precision.

### 3.4 Vibration Isolation

Regardless of gimbal type, the gimbal mounting platform must be vibration-isolated from the airframe. Propeller-induced vibration, even in a pusher configuration, transmits through the fuselage structure and will degrade stabilization performance and cause image blur.

**Vibration isolation design:**

1. **Wire-rope isolators (recommended):** Four AG-1 or AG-2 stainless steel wire rope isolators (e.g., Enidine WR series, or generic equivalents) at the corners of a gimbal mounting plate. These provide 3-axis isolation with a natural frequency that can be tuned by selecting wire diameter and loop geometry. Target natural frequency: 8–15 Hz (below the primary propeller vibration frequency of 50+ Hz, providing >10 dB attenuation). Weight: ~40 g for four isolators + mounting plate.

2. **Silicone ball dampers (common in consumer drones):** Four silicone damping balls press-fit into grommets. Simpler and lighter (~15 g) but less tunable. Natural frequency depends on durometer and ball size. Prone to temperature sensitivity (stiffen in cold, soften in heat).

3. **Sorbothane pads:** 6mm Sorbothane sheet cut to size under a mounting plate. Provides excellent high-frequency damping but limited low-frequency isolation. Best used in combination with mechanical isolators.

**IMU placement for the gimbal controller:** The IMU (accelerometer + gyroscope) for the gimbal controller (Storm32/SimpleBGC) must be mounted on the camera-side of the vibration isolation system — i.e., on the moving part, not the airframe. If mounted on the airframe side, the controller attempts to compensate for vibrations it perceives but that the camera doesn't experience (because the isolators already attenuated them), resulting in induced oscillation.

For the SimpleBGC 32-bit with encoder motors, the encoders provide absolute motor position feedback, reducing reliance on the IMU for position estimation and significantly improving performance in high-vibration environments.

### 3.5 Weight Budget Breakdown

**Configuration A: Minimum Weight ISR System**

| Component | Weight (g) | Notes |
|---|---|---|
| Siyi A8 mini (camera + gimbal) | 95 | Integrated unit |
| Vibration isolator mount | 30 | Wire rope isolators + plate |
| Wiring (Ethernet + power + UART) | 25 | |
| **Total** | **150** | |

**Configuration B: Survey Photogrammetry System**

| Component | Weight (g) | Notes |
|---|---|---|
| Sony A6000 body | 344 | |
| Sony E 20mm f/2.8 lens | 69 | |
| 2-axis brushless gimbal frame + motors | 200 | Custom or adapted |
| SimpleBGC 32-bit controller + IMU | 25 | |
| Seagull #MAP2 trigger | 15 | |
| Vibration isolator mount | 45 | |
| Wiring harness (power, trigger, serial) | 35 | |
| Dummy battery + voltage regulator | 30 | 7.4V regulated supply |
| **Total** | **763** | |

**Configuration C: Lightweight Mapping System**

| Component | Weight (g) | Notes |
|---|---|---|
| Raspberry Pi 4B (2GB) | 46 | Companion computer |
| IMX477 HQ Camera + Kowa 6mm | 102 | |
| 2-axis servo gimbal (MG90S × 2) | 55 | |
| Vibration isolator mount | 25 | |
| Wiring + CSI ribbon cable | 20 | |
| SD card + misc | 5 | |
| **Total** | **253** | |

**Configuration D: Dual System (Survey + Live Video)**

| Component | Weight (g) | Notes |
|---|---|---|
| Configuration B (A6000 survey) | 763 | Primary payload |
| RunCam 2 (fixed forward-facing) | 49 | Secondary video recording |
| Analog VTX (for FPV) | 20 | |
| Mount hardware for RunCam | 15 | |
| **Total** | **847** | |

All configurations fit within the 4 kg payload budget and the 200×300×150 mm bay dimensions (the A6000 configurations are the tightest fit dimensionally and should be verified against the specific airframe's internal geometry with a mockup).

---

## 4. Photogrammetry Pipeline

### 4.1 Image Overlap Requirements

Photogrammetric reconstruction requires that every point on the ground appears in multiple images from different viewing angles. The minimum for stereo reconstruction is two images, but practical structure-from-motion (SfM) pipelines require significantly more redundancy.

**Standard overlap requirements:**

| Overlap type | Minimum | Recommended | Ideal |
|---|---|---|---|
| Forward (along-track / endlap) | 60% | 75–80% | 85% |
| Side (cross-track / sidelap) | 30% | 50–60% | 70% |

Higher overlap provides:
- More tie points for bundle adjustment (improving geometric accuracy)
- Redundancy against cloud shadows, motion blur, or exposure failures
- Better performance in feature-poor areas (water, uniform vegetation, sand)
- Enables multi-view stereo (MVS) dense point cloud generation with lower noise

**The cost of higher overlap:** More images per unit area, which means either slower flight speed (longer mission), more flight lines (more turning time), more storage, and significantly more processing time (SfM bundle adjustment scales roughly O(n²) with image count for feature matching, and MVS scales linearly).

### 4.2 Trigger Spacing Calculation

Given the overlap requirements, the distance between consecutive camera triggers (along-track) and between adjacent flight lines (cross-track) can be calculated:

**Along-track trigger distance:**

```
D_trigger = footprint_along_track × (1 - forward_overlap)
```

**Cross-track line spacing:**

```
D_line = footprint_across_track × (1 - side_overlap)
```

**Where:**

```
footprint_along_track = (H × sensor_height) / f
footprint_across_track = (H × sensor_width) / f
```

**Worked example: A6000 + 20mm lens at 100 m AGL, 20 m/s cruise speed:**

```
sensor_width  = 23.5 mm, sensor_height = 15.6 mm, f = 20 mm
footprint_W   = (100 × 23.5) / 20 = 117.5 m
footprint_H   = (100 × 15.6) / 20 = 78.0 m

(Camera oriented landscape: width = across-track, height = along-track)

D_trigger (80% forward overlap) = 78.0 × (1 - 0.80) = 15.6 m
D_line (60% side overlap)       = 117.5 × (1 - 0.60) = 47.0 m
```

At 20 m/s ground speed:

```
Trigger interval = 15.6 / 20 = 0.78 s → ~1.28 Hz trigger rate
```

This is within the A6000's single-shot capability (~2–3 Hz) but requires fast SD card writes. If the trigger rate exceeds the camera's write capability, increase altitude (larger footprint → larger trigger distance) or reduce speed.

**For the IMX477 + 6mm lens at 100 m AGL, 18 m/s:**

```
footprint_W = (100 × 7.9) / 6 = 131.7 m (across-track, sensor width = 7.9 mm)
footprint_H = (100 × 6.3) / 6 = 105.0 m (along-track)

D_trigger (80%) = 105.0 × 0.20 = 21.0 m
D_line (60%)    = 131.7 × 0.40 = 52.7 m

Trigger interval = 21.0 / 18 = 1.17 s → ~0.86 Hz
```

This is manageable for the IMX477 via the Pi's `rpicam-still` at approximately 1.5 Hz.

### 4.3 ArduPilot Camera Trigger Configuration

ArduPilot provides two primary mechanisms for triggering cameras during survey missions:

#### Method 1: Distance-Based Triggering (DO_SET_CAM_TRIGG_DIST)

The `DO_SET_CAM_TRIGG_DIST` MAVLink command (or mission item) triggers the camera every time the aircraft has traveled a specified horizontal distance. This is the standard method for grid survey missions.

**Configuration:**

```
CAM_TRIGG_DIST = 15.6    (meters, from calculation above)
CAM_TRIGG_TYPE = 0        (servo) or 1 (relay)
CAM1_TYPE = 1             (servo trigger) or appropriate type
```

For servo trigger to a Seagull #MAP2:
```
SERVOx_FUNCTION = 10      (Camera Trigger)
SERVOx_MIN = 1000
SERVOx_MAX = 2000
SERVOx_TRIM = 1500
CAM1_SERVO_ON = 1900      (PWM value to trigger)
CAM1_SERVO_OFF = 1500     (PWM value to reset)
CAM1_DURATION = 3         (servo hold time in 0.1s increments = 300ms)
```

For the IMX477 on a companion Pi, the trigger is received via MAVLink `CAMERA_TRIGGER` messages on the serial link between the Pixhawk and the Pi. A script on the Pi listens for this message and calls `rpicam-still` (or uses the `picamera2` Python library) to capture an image.

**Important nuance:** `DO_SET_CAM_TRIGG_DIST` measures horizontal distance traveled, not along-track distance. In a crosswind, the aircraft's ground track deviates from its heading, and the trigger distance should account for the component of ground speed along the flight line. In practice, for moderate crosswinds (<30% of airspeed), the difference is negligible because overlap margins absorb it.

#### Method 2: Time-Based Triggering (DO_REPEAT_SERVO / DO_REPEAT_RELAY)

For constant-speed flights, a fixed time interval between triggers is simpler:

```
Trigger interval (s) = D_trigger / ground_speed
```

This is set using `DO_REPEAT_SERVO` with the interval calculated for the expected ground speed. However, this method does not adapt to ground speed changes (headwind/tailwind), so distance-based triggering is preferred.

#### Method 3: MAVLink Camera Protocol (V2)

ArduPilot 4.4+ supports the MAVLink Camera Protocol v2, which enables:
- `MAV_CMD_IMAGE_START_CAPTURE` — capture single image or start interval
- `MAV_CMD_IMAGE_STOP_CAPTURE` — stop interval capture
- `MAV_CMD_VIDEO_START_CAPTURE` / `MAV_CMD_VIDEO_STOP_CAPTURE`
- Camera feedback via `CAMERA_IMAGE_CAPTURED` messages (with timestamp, GPS position, attitude quaternion)

This is the preferred method for the Siyi A8 (which responds to MAVLink camera commands natively) and for companion-computer-controlled cameras (IMX477 on Pi, where the Pi acts as a MAVLink camera component).

### 4.4 Trigger Distance Math Summary Table

For 80% forward overlap at various configurations:

| Camera + Lens | Alt (m) | Along-track footprint (m) | Trigger dist (m) | At 18 m/s: interval (s) | At 22 m/s: interval (s) |
|---|---|---|---|---|---|
| A6000 + 20mm | 80 | 62.4 | 12.5 | 0.69 | 0.57 |
| A6000 + 20mm | 100 | 78.0 | 15.6 | 0.87 | 0.71 |
| A6000 + 20mm | 120 | 93.6 | 18.7 | 1.04 | 0.85 |
| A6000 + 35mm | 100 | 44.6 | 8.9 | 0.49 | 0.40 |
| IMX477 + 6mm | 100 | 105.0 | 21.0 | 1.17 | 0.95 |
| IMX477 + 16mm | 100 | 39.4 | 7.9 | 0.44 | 0.36 |
| Siyi A8 + 4.5mm | 100 | 124.4 | 24.9 | 1.38 | 1.13 |

**Critical note on the A6000 + 35mm at 100 m and 22 m/s:** The 0.40 s trigger interval (2.5 Hz) exceeds the A6000's reliable single-shot rate. Either reduce speed, increase altitude, reduce overlap to 75% (trigger dist = 11.1 m, interval = 0.51 s), or use burst mode (but note burst mode locks exposure from the first frame).

### 4.5 Post-Processing Software

#### OpenDroneMap (ODM)

- **Cost:** Free, open source (GPL)
- **Processing:** SfM via OpenSfM, MVS via OpenMVS, mesh generation, orthomosaic, DEM
- **Interface:** CLI (`odm`), web GUI (WebODM), Docker-based
- **Typical processing time:** 500 images at 24 MP: 2–4 hours on a machine with 32 GB RAM, 8-core CPU, and a GPU (CUDA support for MVS). Processing time scales super-linearly with image count.
- **Strengths:** No licensing cost, reproducible pipeline, active development, good for batch/automated processing
- **Weaknesses:** Feature matching can struggle with low-texture scenes (water, uniform pavement). Limited support for multi-spectral sensors. Camera calibration self-refinement less robust than Metashape for unusual lenses.
- **GSD achievable:** Limited by input imagery. With the A6000 + 20mm at 100 m (1.96 cm/px input GSD), expect orthomosaic GSD of approximately 2.0–2.5 cm/px.

**Key ODM parameters for this platform:**

```bash
docker run -ti --rm -v /path/to/images:/datasets/code opendronemap/odm \
  --dsm \
  --dtm \
  --orthophoto-resolution 2.0 \
  --dem-resolution 5.0 \
  --feature-quality high \
  --min-num-features 10000 \
  --matcher-type flann \
  --depthmap-resolution 1000 \
  --mesh-octree-depth 12 \
  --texturing-data-term gmi \
  --gps-accuracy 5 \
  --use-exif
```

#### Agisoft Metashape Professional

- **Cost:** $3,499 (node-locked) or $5,249 (floating license)
- **Processing:** Proprietary SfM + MVS pipeline. Generally considered the quality benchmark for aerial photogrammetry.
- **Strengths:** Superior camera calibration self-refinement. Handles challenging datasets (low texture, repetitive patterns) better than ODM. Built-in GCP workflow. Multi-spectral and thermal processing. Python scripting API for automation. GPU acceleration (CUDA/OpenCL).
- **Weaknesses:** Expensive. Closed source. Processing times comparable to or slightly faster than ODM for similar quality settings.
- **GSD achievable:** Can produce orthomosaics at approximately 1× input GSD when image quality is sufficient. With A6000 + 20mm at 100 m: ~2.0 cm/px orthomosaic.

#### Pix4Dmapper

- **Cost:** $3,490 (perpetual) or subscription ($350/month)
- **Processing:** Proprietary SfM + MVS. Cloud processing option (Pix4Dcloud).
- **Strengths:** Excellent automatic processing (minimal parameter tuning needed). Very robust GCP workflow with sub-centimeter accuracy when combined with RTK/PPK. Industry-standard output formats. rayCloud editor for manual tie-point and classification editing.
- **Weaknesses:** Similar price to Metashape. Slightly less flexible for non-standard camera configurations. Cloud processing requires uploading large datasets.

### 4.6 Output Quality Expectations

#### Orthomosaic

| Input GSD | Expected orthomosaic GSD | Positional accuracy (no GCPs) | Positional accuracy (with 5+ GCPs) |
|---|---|---|---|
| 1–2 cm/px | 1–2.5 cm/px | 1–3 m horizontal, 2–5 m vertical | 2–5 cm horizontal, 3–8 cm vertical |
| 2–4 cm/px | 2–5 cm/px | 1–3 m horizontal, 2–5 m vertical | 3–8 cm horizontal, 5–12 cm vertical |
| 5–8 cm/px | 5–10 cm/px | 2–5 m horizontal, 3–8 m vertical | 5–15 cm horizontal, 8–20 cm vertical |

**Without GCPs:** Positional accuracy is limited by the GPS accuracy of the aircraft's navigation solution. Standard Pixhawk with u-blox M8N GPS provides approximately 2.5 m CEP horizontal, 5 m vertical. This produces orthomosaics with 1–3 m absolute positional error — adequate for visualization and change detection, but insufficient for engineering survey or cadastral mapping.

**With GCPs:** Five or more surveyed ground control points (measured with RTK GNSS to ~2 cm accuracy) distributed across the survey area allow the SfM bundle adjustment to correct systematic errors in the GPS positions. This reduces absolute accuracy to approximately 1–2× GSD horizontally and 1.5–3× GSD vertically. For the A6000 + 20mm at 100 m (GSD 1.96 cm), this means approximately 2–4 cm horizontal and 3–6 cm vertical accuracy — sufficient for volumetric calculations, construction monitoring, and precision agriculture.

**With PPK (Post-Processed Kinematic) GNSS:** If the aircraft carries a survey-grade GNSS receiver (e.g., u-blox ZED-F9P, ~$200, ~15 g) logging raw observations, and a base station logs simultaneously, post-processing can yield camera positions accurate to 2–5 cm. This can eliminate the need for GCPs entirely, or reduce the number needed to 1–2 for verification. The ZED-F9P fits within the payload budget and is supported by ArduPilot's GPS_TYPE parameter.

#### Digital Elevation Model (DEM) / Digital Surface Model (DSM)

- **DSM resolution:** Typically 2–5× GSD. For A6000 + 20mm at 100 m: 4–10 cm/pixel DSM.
- **DTM (bare earth):** Requires classification of the dense point cloud to remove vegetation and structures. Quality depends heavily on ground visibility through vegetation. In dense canopy, DTM accuracy degrades to 0.5–2 m vertical.
- **Vertical noise in DSM:** Typically 2–5× GSD for well-textured surfaces. Smooth, textureless surfaces (e.g., fresh asphalt, calm water) produce significantly higher noise because MVS stereo matching fails.

### 4.7 Georeferencing Workflow

The geotagging pipeline connects each captured image to a geographic position:

1. **ArduPilot logs camera events:** When the camera is triggered (via `CAM_TRIGG_DIST` or MAVLink command), ArduPilot records a `CAM` message in the dataflash log containing: timestamp, GPS lat/lon/alt, roll/pitch/yaw, and the image sequence number.

2. **Image files are stored on the camera's SD card** with sequential filenames (e.g., DSC00001.JPG through DSC01500.JPG).

3. **Post-flight geotagging** matches log entries to image files by sequence number or timestamp and writes GPS coordinates into each image's EXIF data:
   - `GPSLatitude`, `GPSLongitude`, `GPSAltitude`
   - Optionally: `GPSImgDirection` (yaw), camera orientation tags

4. **Tools for geotagging:**
   - **Mission Planner:** Built-in "Geo ref images" function under the Ctrl+F menu. Reads the ArduPilot `.bin` log, correlates timestamps with image files, writes EXIF GPS tags. Handles time offset between camera clock and autopilot clock.
   - **ExifTool (command line):** `exiftool -GPSLatitude=... -GPSLongitude=... -GPSAltitude=... image.jpg` — for scripted/batch workflows.
   - **Custom Python script:** Using `pymavlink` to parse logs and `piexif` or `Pillow` to write EXIF. This is the recommended approach for automated pipelines.

**Time synchronization is critical.** The ArduPilot log timestamps are in microseconds since boot. The camera's file timestamps are in real-world clock time (which may be inaccurate if the camera's clock drifts). The most reliable synchronization method is:

- **For the A6000 with Seagull #MAP2:** The Seagull provides hot-shoe feedback — a signal sent back to the Pixhawk the instant the mechanical shutter fires. ArduPilot logs this as a `CAM` event with the precise autopilot timestamp. This eliminates the need to correlate camera-clock timestamps and provides sub-millisecond timing accuracy.

- **For the IMX477 on a Pi:** The companion computer receives the MAVLink trigger command from the Pixhawk (which includes the autopilot timestamp), captures the image, and can embed the timestamp in the filename or a sidecar file. The Pi's system clock should be synchronized to the Pixhawk's GPS time via the `SYSTEM_TIME` MAVLink message.

---

## 5. Video Downlink

### 5.1 Architecture Overview

A fixed-wing UAV at this scale typically requires two distinct video paths:

1. **FPV / Pilot view:** Low-latency video for the safety pilot or remote operator to maintain situational awareness and visual line-of-sight equivalent. Latency target: <100 ms. Resolution: 720p minimum.

2. **Payload / ISR video:** Higher resolution, potentially stabilized video from the gimbal camera for mission operators. Latency target: <500 ms acceptable, <200 ms preferred. Resolution: 1080p or 4K.

These can be served by separate systems or combined (at the cost of compromises in one direction).

### 5.2 Analog Video

Traditional analog FPV remains relevant due to its near-zero latency and extreme simplicity.

| Parameter | Specification |
|---|---|
| Resolution | NTSC: 480i (720×480 interlaced) / PAL: 576i (720×576) |
| Latency | 1–10 ms (essentially zero — analog RF transmission) |
| Weight | VTX: 5–15 g; antenna: 5–10 g |
| Power | 25 mW–800 mW typical; 1.6 W at max power |
| Frequency | 5.8 GHz (most common), 1.3 GHz (longer range, larger antennas) |
| Range | 5.8 GHz at 600 mW: 2–5 km (with directional RX antenna); 1.3 GHz at 800 mW: 5–15 km |
| Interference | Susceptible to multipath, frequency crowding, and RF noise from ESC/motors |

**Analog is not suitable as the primary payload video link** due to low resolution, but it remains excellent as a secondary pilot FPV feed. A RunCam 2 or similar camera with analog AV output feeding a 5.8 GHz VTX (e.g., TBS Unify Pro32 Nano, 1.5 g) provides a virtually zero-latency pilot view.

### 5.3 Digital FPV Systems

#### DJI O3 Air Unit

| Parameter | Specification |
|---|---|
| Resolution | Up to 1080p 100fps (transmitted), 4K 60fps (onboard recording) |
| Latency | 28–40 ms (measured glass-to-glass) |
| Weight | Air unit: 36.7 g (with antenna); goggles/ground unit: separate |
| Power | 4–9 W (varies with transmit power and resolution) |
| Frequency | 5.8 GHz (auto-channel selection) |
| Range | 10+ km (FCC, clear LOS) |
| Interface | Camera: integrated 1/1.7" sensor; external camera: MIPI input on some variants |
| Video codec | H.264/H.265 encode on-air-unit |
| Ground unit | DJI Goggles 2 or DJI Goggles Integra; HDMI output available for monitor |

**Integration considerations:** The DJI O3 system is designed for DJI's FPV ecosystem but can be used in custom builds. The air unit accepts an external analog video input on some variants, but the primary use case is the built-in camera. For our application, the O3 camera serves as the FPV pilot view, and the HDMI output from the goggles can be captured for ground station display. There is no straightforward way to pipe the Siyi A8's IP video through the DJI O3 link — they are separate video systems.

**Latency at 28–40 ms is exceptional** and suitable for manual piloting in degraded GPS situations.

#### HDZero

| Parameter | Specification |
|---|---|
| Resolution | 720p 60fps (native), 1080p 30fps (Freestyle V2 VTX) |
| Latency | <1 ms (analog-like; HDZero uses a unique approach of transmitting raw pixel data without full-frame encoding) |
| Weight | VTX (Freestyle V2): 20 g; VRX: HDZero goggles |
| Power | 2–5 W |
| Range | 2–10 km (depending on VTX power and antenna) |

HDZero's near-zero latency is achieved by not buffering complete frames — it transmits scan lines as they're read from the sensor. This makes it the best digital system for latency-critical applications. The tradeoff is lower resolution than DJI O3 and more susceptible to signal degradation at range (partial frame corruption rather than DJI's all-or-nothing behavior).

#### Walksnail Avatar

| Parameter | Specification |
|---|---|
| Resolution | Up to 1080p 60fps |
| Latency | 22–35 ms |
| Weight | VTX: ~28 g |
| Power | 3–8 W |
| Range | 5–10 km |

Similar performance to DJI O3 with a more open ecosystem (compatible with multiple goggle brands via their VRX module). Walksnail is a reasonable alternative when DJI lock-in is undesirable.

### 5.4 IP Video over Companion Computer

For the Siyi A8 mini or the IMX477 on a Raspberry Pi, the highest quality and most flexible video downlink uses IP video streaming over a separate data radio.

**Architecture:**

```
[Camera] → [Companion Computer (Pi 4/5)] → [Data Radio TX] ~~~~ [Data Radio RX] → [Ground Station Computer]
   |              |                                                                         |
   MIPI/ETH    GStreamer encode                                                    GStreamer decode
                 H.264/265                                                          + QGroundControl
```

**GStreamer pipeline on the Pi (IMX477 example):**

```bash
# Capture from IMX477, hardware-encode H.264, stream RTP over UDP
gst-launch-1.0 libcamerasrc ! \
  video/x-raw,width=1920,height=1080,framerate=30/1 ! \
  v4l2h264enc extra-controls="controls,repeat_sequence_header=1,h264_profile=1,h264_level=11,video_bitrate=4000000" ! \
  'video/x-h264,level=(string)4.1' ! \
  h264parse ! \
  rtph264pay config-interval=1 pt=96 ! \
  udpsink host=10.0.0.1 port=5600
```

For Pi 5 with H.265 hardware encoder:
```bash
gst-launch-1.0 libcamerasrc ! \
  video/x-raw,width=1920,height=1080,framerate=30/1 ! \
  v4l2h265enc extra-controls="controls,repeat_sequence_header=1" ! \
  h265parse ! \
  rtph265pay config-interval=1 pt=96 ! \
  udpsink host=10.0.0.1 port=5600
```

**For the Siyi A8 mini:** The camera outputs RTSP over Ethernet natively. The companion Pi receives the RTSP stream and can either forward it directly to the data radio (if bandwidth allows) or transcode it to a lower bitrate:

```bash
gst-launch-1.0 rtspsrc location=rtsp://192.168.144.25:8554/main latency=0 ! \
  rtph264depay ! h264parse ! \
  rtph264pay config-interval=1 pt=96 ! \
  udpsink host=10.0.0.1 port=5600
```

**Data radio options:**

| Radio | Bandwidth | Range | Weight | Latency (radio only) | Price |
|---|---|---|---|---|---|
| Microhard pDDL2450 | Up to 8 Mbps | 5–10 km | 60 g | 5–10 ms | $1,500 |
| Doodle Labs Smart Radio Mini | Up to 20 Mbps (MIMO) | 5–15 km | 70 g | 3–8 ms | $800–1,200 |
| Ubiquiti Bullet M2 (2.4 GHz) | Up to 15 Mbps | 3–8 km | 180 g (too heavy for airborne, ground only) | 5–15 ms | $80 |
| RFDesign RFD900x | 0.25 Mbps (telemetry only, not video) | 40+ km | 15 g | 10–50 ms | $200 |
| Generic WiFi (ESP32/RPi built-in) | 5–15 Mbps (2.4 GHz), 20–50 Mbps (5 GHz) | 0.5–2 km | 0 g (integrated) | 10–50 ms | $0 (built-in) |

**For practical video downlink at 1080p 30fps (4 Mbps H.264):** A Doodle Labs Smart Radio Mini provides sufficient bandwidth with margin and a range exceeding typical visual LOS for a 2–4 m wingspan aircraft. Total added weight: ~70 g airborne + ground unit.

**For budget-constrained builds:** The Raspberry Pi's built-in WiFi can stream 1080p to a nearby ground station at ranges of 500 m–1 km with a directional antenna on the ground side. This is suitable for close-range operations but insufficient for extended fixed-wing missions.

### 5.5 Latency Comparison Summary

| System | Glass-to-glass latency | Resolution | Range | Airborne weight |
|---|---|---|---|---|
| Analog 5.8 GHz | 1–10 ms | 480p | 2–5 km | 15 g |
| HDZero | <1 ms | 720p | 2–10 km | 25 g |
| DJI O3 | 28–40 ms | 1080p | 10+ km | 40 g |
| Walksnail | 22–35 ms | 1080p | 5–10 km | 30 g |
| IP video (Pi + Doodle Labs) | 80–200 ms | 1080p–4K | 5–15 km | 120 g |
| IP video (Pi + WiFi) | 100–300 ms | 1080p | 0.5–1 km | 0 g |

**Latency breakdown for IP video path:**

| Stage | Typical latency |
|---|---|
| Camera sensor readout | 10–33 ms (depending on resolution and frame rate) |
| Hardware H.264 encoding (1 frame buffer) | 33 ms (at 30 fps) |
| Network stack (Pi → radio) | 5–10 ms |
| Radio transmission | 3–10 ms |
| Network stack (radio → GCS) | 5–10 ms |
| Software decoding + display | 30–50 ms |
| **Total** | **86–146 ms** |

This can be reduced to 60–100 ms with aggressive tuning: zero-copy pipelines, reduced encoder buffer depth (`tune=zerolatency` in x264, or v4l2 equivalent), and a hardware decoder on the ground station.

### 5.6 Recording vs. Streaming Bandwidth

| Resolution | Frame rate | Codec | Typical bitrate (stream) | Typical bitrate (record) | Data per hour |
|---|---|---|---|---|---|
| 720p | 30 fps | H.264 | 2–3 Mbps | 8–12 Mbps | 3.6–5.4 GB |
| 1080p | 30 fps | H.264 | 4–6 Mbps | 15–25 Mbps | 6.7–11.2 GB |
| 1080p | 60 fps | H.264 | 8–12 Mbps | 25–40 Mbps | 11.2–18 GB |
| 4K | 30 fps | H.264 | 15–25 Mbps | 60–100 Mbps | 27–45 GB |
| 4K | 30 fps | H.265 | 8–15 Mbps | 40–60 Mbps | 18–27 GB |

**Key insight:** Streaming bitrate is typically 1/3 to 1/5 of recording bitrate because streaming quality is limited by the data link bandwidth, while recording quality is limited only by storage write speed. Always record at the highest quality the camera and storage support, and stream a lower-bitrate version over the data link. The high-quality recording is available post-flight for detailed analysis.

---

## 6. Data Storage and Management

### 6.1 SD Card Write Speed Requirements

The SD card must sustain continuous sequential write speeds exceeding the camera's output data rate. Intermittent speed drops (common in cheaper SD cards during garbage collection) cause dropped frames in video or missed triggers in still capture.

| Camera mode | Data rate | Minimum card speed class | Recommended card |
|---|---|---|---|
| A6000 JPEG Fine (24 MP) @ 3 fps | ~30 MB/s burst | UHS-I U3 (V30) | SanDisk Extreme Pro 32 GB |
| A6000 RAW (ARW) @ 3 fps | ~75 MB/s burst | UHS-II U3 (V60) | Sony TOUGH SF-G 32 GB |
| IMX477 DNG (12 MP) @ 1.5 fps | ~36 MB/s burst | UHS-I U3 (V30) | SanDisk Extreme 32 GB |
| 1080p 30 H.264 recording | 3–5 MB/s sustained | UHS-I U1 (V10) | Any Class 10 card |
| 4K 30 H.264 recording | 12–15 MB/s sustained | UHS-I U3 (V30) | SanDisk Extreme 64 GB |
| 4K 30 H.265 recording | 7–10 MB/s sustained | UHS-I U1 (V10) | Any UHS-I card |
| 4K 60 H.264 recording | 25–30 MB/s sustained | UHS-I U3 (V30) | SanDisk Extreme Pro 64 GB |

**For the A6000 in survey mode:** The camera writes JPEG Fine stills of approximately 8–12 MB each. At a 1 Hz trigger rate, sustained write throughput of 10–12 MB/s is needed. A UHS-I U3 card sustains 30 MB/s minimum sequential write, providing ample margin. However, if shooting RAW+JPEG (~35 MB per capture), a UHS-II card is strongly recommended to prevent buffer overflow and missed triggers.

**For the Raspberry Pi + IMX477:** The Pi writes to its own SD card or a USB SSD. The Pi's SD card interface supports up to ~40 MB/s (Pi 4) or ~80 MB/s (Pi 5) in practice. A SanDisk Extreme A2 card provides the needed sustained random write performance. For maximum reliability, write to a USB 3.0 SSD (e.g., Samsung T7, 58 g, 1050 MB/s) rather than the SD card — this eliminates SD card wear and provides virtually unlimited write speed margin.

### 6.2 Storage Capacity Per Flight

| Camera + Mode | File size per image | Images per hour (at 1 Hz trigger) | Storage per hour |
|---|---|---|---|
| A6000 JPEG Fine (24 MP) | 8–12 MB | 3,600 | 29–43 GB |
| A6000 RAW (ARW, 24 MP) | 24–26 MB | 3,600 | 86–94 GB |
| A6000 RAW+JPEG | 32–38 MB | 3,600 | 115–137 GB |
| IMX477 JPEG (12 MP) | 4–6 MB | 3,600 | 14–22 GB |
| IMX477 DNG (12 MP) | 24 MB | 3,600 | 86 GB |
| Siyi A8 4K video | - | - | 27–45 GB (continuous) |
| Siyi A8 1080p video | - | - | 7–11 GB (continuous) |
| RunCam 2 1080p video | - | - | 5–8 GB (continuous) |

**Practical guidance:** A 64 GB SD card supports approximately 1.5 hours of A6000 JPEG survey work at 1 Hz, or approximately 4 hours of IMX477 JPEG capture. For the A6000, carry at least a 128 GB card for missions exceeding 1 hour with margin. For the Pi-based system, a 256 GB USB SSD provides all-day capacity.

**Note on trigger rate:** Survey missions often trigger at 0.5–1.5 Hz depending on altitude and speed. Non-survey video recording is continuous. Budget storage for the worst case: maximum trigger rate for the full mission duration.

### 6.3 Geotagging Workflow (Detailed)

The complete workflow from flight to georeferenced imagery:

#### Step 1: Pre-flight

- Set camera clock to GPS time (if camera supports it; the A6000 can be synced via the Sony Imaging Edge app)
- Verify ArduPilot camera trigger parameters (`CAM_TRIGG_DIST`, `CAM1_TYPE`, servo assignments)
- Format SD card (in-camera format, not computer format, to ensure correct cluster alignment)
- Confirm companion computer scripts are running (if using Pi + IMX477)
- Record GCP coordinates if using ground control (RTK survey of targets before flight)

#### Step 2: In-flight

ArduPilot's camera trigger system creates entries in the dataflash log. Each `CAM` log message contains:

```
CAM {TimeUS, GPSTime, GPSWeek, Lat, Lng, Alt, RelAlt, GPSAlt, Roll, Pitch, Yaw}
```

The `TimeUS` field is microseconds since autopilot boot. `GPSTime` and `GPSWeek` provide absolute UTC time. `Lat/Lng/Alt` are the aircraft's GPS position at the moment of trigger. `Roll/Pitch/Yaw` are the aircraft's attitude (not the camera's — if using a gimbal, the camera attitude must be calculated from gimbal angles).

#### Step 3: Post-flight — Log extraction

Download the `.bin` dataflash log from the Pixhawk's SD card (via Mission Planner, MAVExplorer, or direct SD card read). Extract camera events:

```python
from pymavlink import mavutil

log = mavutil.mavlink_connection('flight.bin')
cam_events = []
while True:
    msg = log.recv_match(type='CAM', blocking=False)
    if msg is None:
        break
    cam_events.append({
        'timestamp': msg.TimeUS,
        'gps_time': msg.GPSTime,
        'gps_week': msg.GPSWeek,
        'lat': msg.Lat,
        'lng': msg.Lng,
        'alt': msg.Alt,
        'rel_alt': msg.RelAlt,
        'roll': msg.Roll,
        'pitch': msg.Pitch,
        'yaw': msg.Yaw
    })
```

#### Step 4: Post-flight — Match images to events

If using hot-shoe feedback (A6000 + Seagull #MAP2), the camera events correspond 1:1 with captured images in sequential order. Image 1 matches event 1, image 2 matches event 2, etc.

If using time-based matching (no hot-shoe), correlate the camera file's EXIF `DateTimeOriginal` with the ArduPilot GPS time, applying a constant offset determined by a calibration exposure at a known time (e.g., photograph a GPS clock display at mission start).

#### Step 5: Write EXIF GPS tags

```python
import piexif
import os

def geotag_image(image_path, lat, lng, alt):
    """Write GPS coordinates to JPEG EXIF data."""
    exif_dict = piexif.load(image_path)
    
    # Convert decimal degrees to degrees/minutes/seconds rational tuples
    def dd_to_dms_rational(dd):
        d = int(abs(dd))
        m = int((abs(dd) - d) * 60)
        s = int(((abs(dd) - d) * 60 - m) * 60 * 10000)
        return ((d, 1), (m, 1), (s, 10000))
    
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: dd_to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: dd_to_dms_rational(lng),
        piexif.GPSIFD.GPSAltitudeRef: 0,  # above sea level
        piexif.GPSIFD.GPSAltitude: (int(alt * 100), 100),
    }
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)
```

#### Step 6: Process in SfM software

Import geotagged images into OpenDroneMap, Metashape, or Pix4D. The GPS tags provide initial camera position estimates for the bundle adjustment. If GCPs are used, mark them in images within the software to refine the solution.

#### Step 7: Export products

- **Orthomosaic:** GeoTIFF with embedded CRS (coordinate reference system, typically WGS84 / UTM zone)
- **DSM/DTM:** GeoTIFF raster
- **Point cloud:** LAS/LAZ format
- **3D mesh:** OBJ or PLY with texture

### 6.4 Data Management Best Practices

1. **Naming convention:** `YYYYMMDD_HHMMSS_SITE_ALTm_CAMERAid/` for each flight dataset folder.

2. **Backup immediately post-flight:** Copy SD card contents to two separate storage devices before reformatting. Flash storage is not archival — a single card failure loses an entire flight's data.

3. **Checksums:** Generate SHA256 checksums for all image files immediately after download. Verify before processing. This catches silent data corruption from SD card errors.

4. **Log association:** Store the ArduPilot `.bin` log in the same folder as the images for that flight. They are inseparable for geotagging.

5. **Storage hierarchy:**
   - **Hot storage (SSD):** Current project, actively processing. 1–4 TB NVMe.
   - **Warm storage (HDD):** Recent projects, may need reprocessing. RAID-1 or ZFS mirror.
   - **Cold storage (archive):** Completed projects. Cloud (S3 Glacier, ~$4/TB/month) or LTO tape.

6. **Processing data multiplier:** SfM processing generates intermediate files (feature databases, depth maps, dense point clouds) that can be 3–10× the size of the input imagery. Budget processing storage accordingly. A 40 GB image set may require 200–400 GB of working space during processing.

---

## Appendix A: System Integration Wiring Diagram (Textual)

```
[Battery 4S-6S]
    |
    ├─→ [PDB / Power Module] ─→ [Pixhawk Power Input]
    |       |
    |       ├─→ [5V BEC 3A] ─→ [Raspberry Pi 5V]
    |       |                    ├─→ [IMX477 via CSI ribbon]
    |       |                    ├─→ [USB SSD (storage)]
    |       |                    └─→ [Data Radio TX (via Ethernet/USB)]
    |       |
    |       ├─→ [12V BEC 2A] ─→ [Siyi A8 mini power]
    |       |
    |       └─→ [7.4V Reg] ──→ [A6000 dummy battery]
    |
    [Pixhawk]
    ├─→ TELEM2 (UART) ──→ [Raspberry Pi UART (MAVLink)]
    ├─→ SERVO9 (PWM) ──→ [Seagull #MAP2 Trigger] ─→ [A6000 Multi-terminal]
    ├─→ SERVO10 (PWM) ──→ [Gimbal Roll Motor (if servo type)]
    ├─→ SERVO11 (PWM) ──→ [Gimbal Pitch Motor (if servo type)]
    ├─→ AUX (UART) ──→ [Siyi A8 UART (gimbal control)]
    └─→ GPS2 ──→ [u-blox ZED-F9P (PPK logging, optional)]
    
    [Seagull #MAP2]
    ├─→ Multi-terminal ──→ [A6000]
    └─→ Hot-shoe ←── [A6000 hot-shoe] (feedback signal)

    [Raspberry Pi]
    ├─→ Ethernet ──→ [Siyi A8 mini (IP video receive)]
    ├─→ GStreamer pipeline ──→ [Data Radio TX (video stream out)]
    └─→ MAVProxy ──→ [Data Radio TX (telemetry multiplex)]
```

## Appendix B: Recommended Configurations by Budget

### Budget Tier 1: <$300 (Minimum Viable Mapping)

- Camera: Raspberry Pi HQ Camera (IMX477) + Arducam 6mm f/1.2 — $55
- Companion computer: Raspberry Pi 4B 2GB — $45
- Gimbal: 2× MG90S servo gimbal, 3D-printed frame — $15
- Vibration isolation: Silicone damper balls — $5
- Video downlink: Pi onboard WiFi (short range) — $0
- Storage: SanDisk 64 GB Extreme microSD — $15
- Trigger: GPIO-triggered via MAVLink script on Pi — $0
- **Total: ~$135**
- **GSD at 100m: 2.58 cm/px, 480p live video at <1 km range**

### Budget Tier 2: $500–$800 (Capable ISR + Basic Mapping)

- Camera + Gimbal: Siyi A8 mini — $300
- Companion computer: Raspberry Pi 4B 4GB — $55
- Video downlink: DJI O3 Air Unit (for pilot FPV) — $200
- Data radio: Doodle Labs Mini (for Siyi A8 IP video) — $900 (or use Pi WiFi for shorter range, $0)
- Storage: 64 GB microSD in Siyi A8 — included
- **Total: ~$555 (without long-range data radio) to ~$1,455 (with data radio)**
- **GSD at 100m: 4.11 cm/px, 1080p stabilized video**

### Budget Tier 3: $1,000–$2,000 (Survey-Grade Photogrammetry)

- Camera: Sony A6000 (used) — $450
- Lens: Sony E 20mm f/2.8 — $350
- Trigger: Seagull #MAP2 — $90
- Gimbal: SimpleBGC 32-bit + custom 2-axis frame + motors — $250
- Vibration isolation: Wire rope isolators — $30
- Power: Dummy battery + 7.4V regulator — $25
- Secondary FPV: RunCam Nano + analog VTX — $40
- Companion computer: Raspberry Pi 4B (for geotagging/telemetry) — $55
- Storage: 128 GB UHS-I U3 SD card — $25
- GNSS upgrade: u-blox ZED-F9P (for PPK) — $200 (optional)
- **Total: ~$1,315 (without PPK) to ~$1,515 (with PPK)**
- **GSD at 100m: 1.96 cm/px, survey-grade orthomosaics with GCPs or PPK**

---

## Appendix C: Key ArduPilot Parameters Reference

| Parameter | Value | Description |
|---|---|---|
| `CAM1_TYPE` | 1 (Servo) or 4 (MAVLink) | Camera trigger mechanism |
| `CAM_TRIGG_DIST` | 15.6 (example) | Distance between triggers in meters |
| `SERVOx_FUNCTION` | 10 | Assign servo output to Camera Trigger |
| `CAM1_SERVO_ON` | 1900 | PWM value to trigger camera |
| `CAM1_SERVO_OFF` | 1500 | PWM value for idle state |
| `CAM1_DURATION` | 3 | Trigger pulse duration (×100 ms) |
| `MNT1_TYPE` | 8 (Siyi) / 4 (Storm32 MAVLink) / 6 (AlexMos) / 1 (Servo) | Mount/gimbal driver |
| `MNT1_PITCH_MIN` | -90 | Gimbal minimum pitch angle (nadir) |
| `MNT1_PITCH_MAX` | 0 | Gimbal maximum pitch angle (horizon) |
| `MNT1_DEFLT_MODE` | 3 | Default mount mode (3 = GPS point) |
| `MNT1_RC_RATE` | 30 | RC control angular rate (deg/s) |
| `SERIALx_PROTOCOL` | 2 (MAVLink2) | Serial port for companion computer |
| `SERIALx_BAUD` | 921 | Baud rate (921600) for companion link |
| `GPS_TYPE2` | 2 | Second GPS for ZED-F9P PPK module |
| `LOG_BITMASK` | 0xFFFF | Enable all logging including CAM events |

---

This specification covers the complete electro-optical payload design space for a mini fixed-wing UAV in the 2–4 m class. The optimal configuration depends on the primary mission: the Siyi A8 mini for ISR/surveillance with minimal integration effort, the Sony A6000 + 20mm f/2.8 for photogrammetric mapping, or the Raspberry Pi HQ Camera for maximum flexibility and the tightest budgets. All configurations fit within the 4 kg payload and 200×300×150 mm bay constraints with substantial margin.
