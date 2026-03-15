# Thermal/Infrared Imaging Payloads for Mini Fixed-Wing UAV

## Technical Specification Document

**Platform Reference:** Mini fixed-wing UAV, 2–4 m wingspan, 4 kg max payload, 200×300×150 mm payload bay, ArduPilot Pixhawk FC

---

## 1. Thermal Sensor Comparison

### 1.1 Sensor Summary Table

| Parameter | FLIR Lepton 2.5 | FLIR Lepton 3.5 | FLIR Boson 320 | FLIR Boson 640 | FLIR Tau 2 640 | InfiRay Tiny1-C | InfiRay T2-S | InfiRay Micro III 640 | Seek CompactPRO |
|---|---|---|---|---|---|---|---|---|---|
| **Resolution** | 80×60 | 160×120 | 320×256 | 640×512 | 640×512 | 256×192 | 256×192 | 640×512 | 320×240 |
| **Pixel pitch** | 17 µm | 12 µm | 12 µm | 12 µm | 17 µm | 12 µm | 12 µm | 12 µm | 12 µm |
| **NETD** | <50 mK | <50 mK | <40 mK (typ. 20) | <40 mK (typ. 20) | <30 mK | <40 mK | <40 mK | <35 mK | <70 mK |
| **Spectral range** | 8–14 µm | 8–14 µm | 7.5–13.5 µm | 7.5–13.5 µm | 7.5–13.5 µm | 8–14 µm | 8–14 µm | 8–14 µm | 7.2–13 µm |
| **Frame rate** | 8.6 Hz (export) | 8.6 Hz (export) | 60 Hz | 60 Hz | 30/60 Hz | 25 Hz | 25 Hz | 30 Hz | <15 Hz |
| **Interface** | SPI / I²C | SPI / I²C | MIPI CSI-2, USB | MIPI CSI-2, USB | Analog (NTSC/PAL), LVDS, USB | USB-C (UVC) | USB-C (UVC) | MIPI CSI-2, USB | USB (proprietary) |
| **Core weight** | 0.9 g | 0.9 g | 7.5 g (w/lens) | 7.5 g (w/lens) | 72 g (w/lens) | 6.3 g | ~8 g | ~12 g | 22.5 g (module) |
| **System weight (est.)** | 15–30 g | 15–30 g | 25–40 g | 25–40 g | 110–160 g | 20–35 g | 25–40 g | 35–55 g | 35–50 g |
| **Power** | <150 mW | <150 mW | <500 mW (typ. 350) | <750 mW (typ. 500) | ~1.2 W | <350 mW | <400 mW | <700 mW | ~500 mW |
| **Price (GBP, approx.)** | £180–220 | £220–280 | £800–1,200 | £2,500–4,000 | £4,000–7,000 | £250–350 | £300–450 | £1,200–1,800 | £350–450 |
| **Startup time** | <5 s to image | <5 s to image | <3 s | <3 s | <4 s | <3 s | <3 s | <3 s | ~1 s |
| **FFC interval** | Manual shutter | Manual shutter | Auto ~3 min or manual | Auto ~3 min or manual | Auto ~3 min or manual | Auto ~5 min | Auto ~5 min | Auto ~3 min | Shutterless (TEC-less) |
| **Radiometric** | No (Lepton 2.5 has limited) | Yes (Lepton 3.5 R) | Optional (Boson+) | Optional (Boson+) | Yes (Tau 2 R) | No (relative) | Limited | Yes (optional) | No |
| **Digital output format** | 14-bit raw | 14-bit raw | 16-bit raw / 8-bit AGC | 16-bit raw / 8-bit AGC | 14-bit raw / CMOS digital | 14-bit via UVC | 14-bit via UVC | 16-bit raw | Proprietary frame |
| **Lens options** | Fixed 51° HFOV | Fixed 57° HFOV | 34°, 50°, 92° | 18°, 24°, 34°, 50°, 95° | 7.5° to 69° (many options) | Fixed 56° | Fixed 56° | Multiple | Fixed 32° |

### 1.2 Detailed Sensor Analysis

#### FLIR Lepton 2.5
The Lepton 2.5 is the entry-level thermal core. At 80×60 pixels, it is fundamentally resolution-limited for aerial work. Each pixel at 100 m AGL with the stock 51-degree HFOV lens covers approximately 1.2 m on the ground; a standing person occupies roughly 1–2 pixels. This is below the Johnson criteria threshold for even detection. The module's primary advantage is cost (under £200) and negligible weight (under 1 g for the bare core). It communicates via SPI at up to 8.6 fps (ITAR/EAR export limited). The 14-bit raw output provides good dynamic range for relative thermal contrast. No shutter is included; flat-field correction relies on a manual or external shutter mechanism, which introduces periodic image disruption. Suitable only for very close-range work or as a supplementary sensor for coarse thermal awareness.

#### FLIR Lepton 3.5
The Lepton 3.5 quadruples the resolution to 160×120 with 12 µm pitch. The radiometric variant (Lepton 3.5 R) provides calibrated temperature output per pixel, a significant capability upgrade. At 100 m AGL with its 57-degree HFOV, ground sample distance (GSD) is approximately 0.50 m/pixel; a person subtends roughly 3–4 pixels vertically. This approaches the detection threshold under Johnson criteria but remains marginal for recognition. The SPI interface at 8.6 fps limits real-time application but is adequate for survey work. The Lepton 3.5 is the strongest low-cost option for payload-constrained platforms. Breakout boards (PureThermal, GroupGets) provide USB UVC output, simplifying integration with companion computers.

#### FLIR Boson 320
The Boson 320 represents the step into professional-grade uncooled cores. At 320×256 with 12 µm pitch and NETD typically around 20 mK, it offers dramatically better thermal sensitivity than the Lepton family. The 60 Hz frame rate (no export restriction on 320 resolution in many jurisdictions, but verify) enables smooth video for real-time operations. Multiple lens options (34° to 92° HFOV) allow mission-tailored field of view. At 100 m AGL with a 34-degree lens, GSD is approximately 0.19 m/pixel; a person subtends roughly 9 pixels vertically — well into the Johnson detection range and approaching recognition. The MIPI CSI-2 interface enables direct connection to Raspberry Pi, Jetson, or other SBCs. The integrated image processing pipeline includes scene-based non-uniformity correction (SBNUC), digital detail enhancement (DDE), and automatic gain control (AGC). FFC occurs automatically every few minutes via an internal shutter; this causes a momentary image freeze (approximately 0.5 s) which must be accounted for in time-critical applications.

#### FLIR Boson 640
The Boson 640 is the highest-resolution uncooled core in the Boson family and represents the sweet spot for UAV thermal imaging. At 640×512 with 12 µm pitch, it provides four times the pixel count of the Boson 320. NETD of approximately 20 mK typical allows detection of subtle thermal signatures. With a 24-degree lens at 100 m AGL, GSD is approximately 0.066 m/pixel; a person subtends roughly 27 pixels vertically — comfortably exceeding Johnson recognition criteria. The Boson+ variant adds radiometric capability for calibrated temperature measurement. Weight remains remarkably low at 7.5 g for the core plus lens module. This is the recommended primary sensor for SAR, wildlife survey, and security applications on the specified platform. Cost is the primary barrier at £2,500–4,000.

#### FLIR Tau 2 640
The Tau 2 is the legacy professional standard for UAV thermal cores. It offers 640×512 resolution with 17 µm pitch and industry-leading NETD below 30 mK. The larger pixel pitch provides better signal-to-noise ratio per pixel compared to 12 µm designs. However, the larger sensor format requires larger optics, resulting in significantly higher system weight (72 g core, 110–160 g with lens and housing). The Tau 2 offers the widest lens selection of any uncooled core, from 7.5-degree telephoto to 69-degree wide angle. It outputs analog video (NTSC/PAL) for simple display and LVDS/CMOS digital for capture. Power consumption is higher (~1.2 W) and the module is physically larger. At the specified 4 kg payload budget this remains viable but consumes more of the weight and volume allocation than the Boson. The Tau 2 is now largely superseded by the Boson for new designs, but remains in wide service. The radiometric variant provides absolute temperature measurement.

#### InfiRay Tiny1-C
The Tiny1-C is a Chinese-manufactured 256×192 core aimed at the consumer/prosumer drone market. At 12 µm pitch with NETD under 40 mK, it provides respectable performance at a price point (£250–350) significantly below FLIR equivalents of similar resolution. The USB-C UVC interface simplifies integration — the camera appears as a standard USB webcam to any Linux companion computer. Weight is extremely low at 6.3 g. The 56-degree fixed HFOV at 100 m AGL yields GSD of approximately 0.37 m/pixel; a person subtends roughly 5 pixels vertically, which is at the margin of reliable detection. The primary concern is long-term support, documentation quality (often Chinese-language primary), and export control compliance. SDK availability varies; UVC mode provides raw frames without requiring proprietary drivers.

#### InfiRay T2-S
The T2-S is an incremental step from the Tiny1-C with similar 256×192 resolution but improved thermal processing and a slightly more robust mechanical package. It is targeted at integration into OEM products. The USB-C UVC interface is maintained. Weight increases slightly to approximately 8 g. Performance specifications are nearly identical to the Tiny1-C. This module is better suited for applications requiring a more ruggedized connector and improved thermal stability during extended operation. Documentation and support remain the primary integration risk compared to FLIR products.

#### InfiRay Micro III 640
The Micro III 640 is InfiRay's flagship miniature uncooled core, directly competing with the FLIR Boson 640. At 640×512 with 12 µm pitch and NETD under 35 mK, it offers comparable resolution to the Boson at a lower price point (£1,200–1,800 vs £2,500–4,000). The module provides MIPI CSI-2 and USB interfaces. Weight is approximately 12 g — heavier than the Boson core but still very manageable. The Micro III supports multiple lens options and includes onboard image processing with NUC, DDE, and AGC. This is a cost-effective alternative to the Boson 640 for budget-constrained projects, though with less mature ecosystem support, fewer lens options, and potentially more complex export licensing.

#### Seek Thermal CompactPRO
The CompactPRO offers 320×240 resolution with a 32-degree FOV at a consumer price point (£350–450). It uses a proprietary USB interface and requires the Seek SDK for integration. The key distinguishing feature is its shutterless (TEC-less) design, which eliminates the periodic image freeze associated with FFC shutter actuation. However, NETD is significantly worse at approximately 70 mK, meaning subtle thermal contrast is lost. The fixed narrow FOV is advantageous for longer-range detection but limits situational awareness. The proprietary interface and limited SDK complicate custom integration. Weight at 22.5 g for the module is moderate. The CompactPRO is best considered a budget option for applications where periodic image freeze is unacceptable and thermal sensitivity requirements are modest.

### 1.3 Recommendation Matrix by Application

| Application | Primary Recommendation | Budget Alternative |
|---|---|---|
| SAR (person detection) | Boson 640 | InfiRay Micro III 640 |
| Wildlife survey | Boson 640 | Boson 320 |
| Building inspection (radiometric) | Boson 640+ (radiometric) | Lepton 3.5 R |
| Fire detection | Tau 2 640 (radiometric) | Boson 640+ |
| Security/perimeter | Boson 320 | InfiRay Tiny1-C |
| Technology demonstrator | Lepton 3.5 | InfiRay Tiny1-C |

---

## 2. Detection Range Calculations

### 2.1 Johnson Criteria Fundamentals

The Johnson criteria (originally DRI — Detection, Recognition, Identification) define the number of line pairs (or equivalently, pixel pairs) that must span across a target's critical dimension for an observer to achieve a given level of discrimination:

| Task | Line pairs across target | Equivalent pixels across target |
|---|---|---|
| **Detection** | 1.0 ± 0.25 | 2 pixels |
| **Orientation** | 1.4 ± 0.35 | 2.8 pixels |
| **Recognition** | 4.0 ± 0.8 | 8 pixels |
| **Identification** | 6.4 ± 1.5 | 12.8 pixels |

These criteria assume a 50% probability of accomplishing the task by a trained observer. The target's "critical dimension" is typically taken as the minimum dimension (height or width) that distinguishes the target type.

**Critical target dimensions used in calculations:**

- Standing person: 1.8 m (height) × 0.5 m (width); critical dimension = 0.5 m (width, as it is the limiting axis for discrimination)
- Crawling/prone person: 1.8 m × 0.5 m; critical dimension = 0.3 m
- Light vehicle (car): 4.5 m × 1.8 m; critical dimension = 1.8 m
- Heavy vehicle (truck/SUV): 6.0 m × 2.5 m; critical dimension = 2.5 m

### 2.2 Ground Sample Distance (GSD) Calculations

GSD depends on altitude, sensor resolution, pixel pitch, and lens focal length:

```
GSD = (pixel_pitch × altitude) / focal_length
```

Or equivalently using the horizontal field of view (HFOV):

```
GSD = 2 × altitude × tan(HFOV/2) / horizontal_pixels
```

**Reference configurations (lens selected for practical UAV use):**

| Sensor | Resolution | Lens HFOV | GSD @ 50 m | GSD @ 100 m | GSD @ 200 m | GSD @ 300 m |
|---|---|---|---|---|---|---|
| Lepton 2.5 | 80×60 | 51° | 0.60 m | 1.20 m | 2.40 m | 3.59 m |
| Lepton 3.5 | 160×120 | 57° | 0.34 m | 0.68 m | 1.36 m | 2.04 m |
| Boson 320 | 320×256 | 34° | 0.095 m | 0.19 m | 0.38 m | 0.57 m |
| Boson 640 | 640×512 | 24° | 0.033 m | 0.066 m | 0.132 m | 0.198 m |
| Tau 2 640 | 640×512 | 25° | 0.035 m | 0.069 m | 0.138 m | 0.208 m |

### 2.3 Person Detection Range by Resolution

Using Johnson criteria: Detection requires the target's critical dimension to span at least 2 pixels.

For a standing person (critical dimension 0.5 m width):

```
Max detection range = (0.5 m × focal_length) / (2 × pixel_pitch)
```

Or using GSD: range where GSD ≤ critical_dimension / required_pixels.

| Sensor (config) | Detection (2 px, 0.5 m) | Recognition (8 px) | Identification (13 px) |
|---|---|---|---|
| 80×60, 51° HFOV | ~42 m | ~10 m | ~6 m |
| 160×120, 57° HFOV | ~74 m | ~18 m | ~11 m |
| 320×256, 34° HFOV | ~526 m | ~131 m | ~81 m |
| 640×512, 24° HFOV | ~1,515 m | ~379 m | ~233 m |
| 640×512, 50° HFOV | ~670 m | ~168 m | ~103 m |

**Important caveats:** These are geometric limits only. Actual performance is degraded by:
- Atmospheric absorption (see Section 2.5)
- Target thermal contrast relative to NETD
- Platform vibration and motion blur
- Scene clutter and background thermal variation

**Practical rule of thumb:** Multiply Johnson geometric range by 0.5–0.7 for realistic conditions at altitude.

**Realistic person detection ranges for UAV operations:**

| Sensor | Practical detection range | Practical recognition range |
|---|---|---|
| 80×60 | 20–30 m | Not practical |
| 160×120 | 35–55 m | Not practical |
| 320×256 | 260–370 m | 65–95 m |
| 640×512 (24° lens) | 750–1,060 m | 190–265 m |

### 2.4 Vehicle Detection Range

For a light vehicle (critical dimension 1.8 m):

| Sensor (config) | Detection (2 px) | Recognition (8 px) | Identification (13 px) |
|---|---|---|---|
| 80×60, 51° HFOV | ~150 m | ~38 m | ~23 m |
| 160×120, 57° HFOV | ~265 m | ~66 m | ~41 m |
| 320×256, 34° HFOV | ~1,895 m | ~474 m | ~291 m |
| 640×512, 24° HFOV | ~5,455 m | ~1,364 m | ~838 m |

Again, apply 0.5–0.7 factor for practical ranges.

### 2.5 Effect of Altitude on Thermal Contrast

As altitude increases, the atmospheric path length between sensor and target grows, reducing apparent thermal contrast through two mechanisms:

**Atmospheric absorption in LWIR (8–14 µm):**

The 8–14 µm band is chosen specifically because it corresponds to an atmospheric transmission window. However, absorption is not zero:

- **Primary absorbers:** Water vapour (H₂O), ozone (O₃), CO₂
- **Typical sea-level transmittance over 100 m path:** 95–98% in dry conditions, 85–92% in humid conditions
- **Transmittance over 1 km path:** 70–90% (dry) to 40–70% (humid)

The Beer-Lambert law governs transmission:

```
τ(R) = exp(-α × R)
```

Where α is the extinction coefficient (km⁻¹) and R is the slant range (km).

**Typical LWIR extinction coefficients:**

| Condition | α (km⁻¹) | Transmittance at 100 m | Transmittance at 500 m | Transmittance at 1 km |
|---|---|---|---|---|
| Clear, dry (RH 30%) | 0.1–0.2 | 98–99% | 90–95% | 82–90% |
| Clear, humid (RH 70%) | 0.3–0.6 | 94–97% | 74–86% | 55–74% |
| Light haze | 0.5–1.0 | 90–95% | 61–78% | 37–61% |
| Light rain (2 mm/hr) | 1.0–2.0 | 82–90% | 37–61% | 14–37% |
| Heavy rain (10 mm/hr) | 2.0–5.0 | 61–82% | 8–37% | 1–14% |
| Fog (visibility 500 m) | 3.0–6.0 | 55–74% | 5–22% | <5% |

**Altitude-specific considerations:**

For a UAV at altitude h looking vertically down, the slant range equals h. For off-nadir angles θ, slant range = h / cos(θ). At a 45-degree look angle, slant range is 1.41× the altitude.

The atmosphere is denser (more absorbing) near the surface. For a nadir-looking sensor at 100 m AGL, essentially the entire path is through surface-layer atmosphere. This is actually the worst case compared to a ground-level horizontal path of the same distance, because the surface layer contains the most water vapour.

### 2.6 Minimum Detectable Temperature Difference (MDTD)

The minimum detectable temperature difference at range depends on sensor NETD, atmospheric transmission, optics transmission, and target-to-background spatial frequency:

```
MDTD = NETD / (τ_atm × τ_optics × MTF_system)
```

Where:
- NETD = sensor noise equivalent temperature difference (at the sensor)
- τ_atm = atmospheric transmittance over the slant range
- τ_optics = optics transmittance (typically 0.85–0.95 for germanium lenses)
- MTF_system = modulation transfer function at the target's spatial frequency

**Worked example — Boson 640 detecting a person at 200 m AGL, clear humid conditions:**

```
NETD = 0.020 K (20 mK)
τ_atm at 200 m, RH 70% = exp(-0.4 × 0.2) ≈ 0.923
τ_optics = 0.90
MTF at person spatial frequency ≈ 0.6 (accounting for diffraction, detector sampling)

MDTD = 0.020 / (0.923 × 0.90 × 0.6) = 0.020 / 0.498 = 0.040 K
```

A person typically presents 2–10 K contrast against ambient background (depending on clothing, ambient temperature, wind). At 0.040 K MDTD, person detection is extremely robust. Even at 500 m range in humid conditions, MDTD remains well below typical person thermal contrast.

**The practical limit for person detection is almost always spatial resolution (pixel-on-target), not thermal sensitivity, for modern uncooled cores.**

---

## 3. Dual EO+IR Fusion

### 3.1 Rationale

Visible (EO) and thermal (IR) imagery provide complementary information. EO provides high spatial resolution, colour, and texture for scene understanding and identification. IR provides thermal contrast independent of illumination, enabling detection of concealed or camouflaged targets and operation in darkness. Fusing both into a single display or analysis pipeline significantly enhances situational awareness.

### 3.2 Overlay Alignment Challenges

The fundamental challenge is that EO and IR cameras have different:

- **Optical centres:** Parallax exists unless the sensors are coaxial (rare in compact systems). At close range (under 50 m), parallax causes significant misregistration. At typical UAV altitudes (50–300 m), parallax error is small relative to GSD.
- **Fields of view:** EO cameras typically have wider FOV than IR cameras, or vice versa. The overlap region must be determined.
- **Resolution:** EO typically has 5–50× more pixels than IR. The IR image must be upscaled or the EO downsampled.
- **Distortion models:** Different lens distortion characteristics must be corrected independently.
- **Temporal alignment:** Different frame rates and readout times cause temporal misregistration during platform motion.

### 3.3 Registration Algorithms

#### 3.3.1 Homography-Based Registration (Recommended for UAV)

For a UAV looking at distant ground (all targets approximately coplanar at the ground plane), a single 3×3 homography matrix H maps every pixel from the IR image to the EO image:

```
[x_eo]       [x_ir]
[y_eo] = H × [y_ir]
[ 1  ]       [ 1  ]
```

**Calibration procedure:**

1. Mount both cameras rigidly on the payload platform.
2. Image a calibration target (heated checkerboard pattern visible in both EO and IR) at the expected operating altitude.
3. Detect corresponding points in both images (corner detection or manual selection).
4. Compute H using least-squares fitting (cv2.findHomography with RANSAC).
5. Store H for runtime application.

**Limitations:** H is valid only for a single ground-plane distance. If altitude changes significantly (more than ±30%), H should be recomputed or parameterised by altitude. For nadir-looking cameras over flat terrain, a single H is usually adequate across 50–300 m AGL.

#### 3.3.2 Feature-Based Registration (Dynamic)

For scenes with sufficient shared features, runtime registration can be performed:

1. Extract features from both images using algorithms that work across modalities. Standard feature detectors (SIFT, ORB) often fail across EO/IR because gradient patterns differ fundamentally.
2. **Edge-based matching** is more reliable: apply Canny or Sobel edge detection to both images, then match edge patterns using phase correlation or mutual information.
3. **Mutual information (MI) registration** maximizes the statistical dependence between the two images without requiring explicit feature correspondence. This is the most robust approach but is computationally expensive (~50–200 ms per frame on a Jetson Nano).

#### 3.3.3 IMU/GPS-Aided Registration

If both cameras are geometrically calibrated (intrinsics known) and their relative pose is measured during installation, the homography can be computed analytically from the platform attitude (from Pixhawk IMU) and altitude (from barometer/rangefinder):

```python
# Simplified: compute H from known camera geometry and platform state
R_eo_ir = known_rotation_between_cameras  # from calibration
t_eo_ir = known_translation_between_cameras  # from calibration
n = [0, 0, 1]  # ground plane normal
d = altitude  # from Pixhawk
H = K_eo @ (R_eo_ir + t_eo_ir @ n.T / d) @ np.linalg.inv(K_ir)
```

This approach requires no feature matching and works in featureless terrain (water, desert).

### 3.4 Display Modes

#### Picture-in-Picture (PiP)
The IR image is displayed as a rectangular overlay in one corner of the EO image. No pixel-level registration is required; only a bounding box indicating the IR camera's FOV on the EO image is needed. This is the simplest implementation and the most robust against calibration errors.

**Implementation:** Resize the IR image to the appropriate PiP dimensions. Alpha-blend over the EO image at a fixed position. Overlay a rectangle on the EO image showing the IR FOV boundaries.

#### Side-by-Side
Both images displayed simultaneously at full resolution. Synchronised cursors or zoom regions link the views. No registration required but demands more display real estate.

#### Alpha-Blended Overlay
The IR image is warped to align with the EO image (using H), colourised (applying a colour palette such as iron, rainbow, or white-hot), and blended with the EO image:

```python
fused = cv2.addWeighted(eo_aligned, alpha, ir_colourised_warped, 1-alpha, 0)
```

Typical alpha = 0.5–0.7 (biased toward EO for spatial detail). This provides the richest combined view but requires accurate registration and is visually confusing if alignment is poor.

#### Thermal Highlighting
The EO image is displayed normally, with thermal detections (regions above a threshold or detected by an algorithm) overlaid as coloured regions or contours. This preserves EO spatial detail while drawing attention to thermally significant features.

### 3.5 Companion Computer Requirements

| Fusion Mode | Processing Load | Minimum Platform | Recommended Platform |
|---|---|---|---|
| PiP (no registration) | Trivial | Raspberry Pi Zero 2W | Raspberry Pi 4 |
| Homography warp + blend | Light (~5 ms/frame) | Raspberry Pi 4 | Raspberry Pi 4 |
| Feature-based registration | Moderate (~50–200 ms) | Raspberry Pi 4 | Jetson Nano |
| MI-based registration | Heavy (~200–500 ms) | Jetson Nano | Jetson Xavier NX |
| Fusion + AI detection | Heavy | Jetson Nano + Coral | Jetson Xavier NX |

**Companion computer comparison for this UAV platform:**

| Computer | Weight | Power | GPU/NPU | Suitability |
|---|---|---|---|---|
| Raspberry Pi 4 (4 GB) | 46 g | 3–6 W | VideoCore VI (limited) | Basic fusion, recording |
| Raspberry Pi 5 (8 GB) | 47 g | 5–10 W | VideoCore VII | Moderate fusion + light ML |
| Jetson Nano (4 GB) | 140 g | 5–10 W | 128-core Maxwell GPU | Fusion + ML inference |
| Jetson Xavier NX | 180 g | 10–15 W | 384-core Volta + 2× NVDLA | Full pipeline + AI |
| Jetson Orin Nano | 200 g | 7–15 W | 1024-core Ampere | Overkill but future-proof |
| Google Coral Dev Board Mini | 60 g | 2–3 W | Edge TPU (4 TOPS) | ML inference only, no GPU for fusion |

### 3.6 OpenCV Thermal Fusion Pipeline

A complete pipeline for the recommended Boson 640 (IR) + Raspberry Pi Camera Module 3 (EO) on a Raspberry Pi 4 or Jetson Nano:

```python
import cv2
import numpy as np

class ThermalFusionPipeline:
    def __init__(self, homography_matrix, ir_colormap=cv2.COLORMAP_INFERNO):
        """
        homography_matrix: 3x3 numpy array mapping IR pixels to EO pixels
        """
        self.H = homography_matrix
        self.colormap = ir_colormap
        self.alpha = 0.6  # EO weight in blend

    def preprocess_ir(self, ir_raw_16bit):
        """
        Convert 16-bit raw thermal to 8-bit with histogram equalization.
        ir_raw_16bit: 640x512 uint16 array (raw radiometric or AGC output)
        """
        # Normalize to 8-bit using min-max scaling
        ir_min = np.percentile(ir_raw_16bit, 1)
        ir_max = np.percentile(ir_raw_16bit, 99)
        ir_norm = np.clip((ir_raw_16bit - ir_min) / (ir_max - ir_min) * 255, 0, 255)
        ir_8bit = ir_norm.astype(np.uint8)

        # Apply CLAHE for local contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        ir_enhanced = clahe.apply(ir_8bit)

        return ir_enhanced

    def colorize_ir(self, ir_8bit):
        """Apply false color palette to thermal image."""
        return cv2.applyColorMap(ir_8bit, self.colormap)

    def warp_ir_to_eo(self, ir_color, eo_shape):
        """Warp IR image to EO image coordinate frame using homography."""
        h, w = eo_shape[:2]
        ir_warped = cv2.warpPerspective(ir_color, self.H, (w, h),
                                         flags=cv2.INTER_LINEAR,
                                         borderMode=cv2.BORDER_CONSTANT,
                                         borderValue=(0, 0, 0))
        return ir_warped

    def blend(self, eo_frame, ir_warped):
        """Alpha blend EO and warped IR."""
        # Create mask of valid (non-zero) IR pixels
        ir_gray = cv2.cvtColor(ir_warped, cv2.COLOR_BGR2GRAY)
        mask = (ir_gray > 0).astype(np.float32)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)  # feather edges
        mask = np.stack([mask] * 3, axis=-1)

        # Blend only where IR data exists
        fused = (eo_frame * self.alpha + ir_warped * (1 - self.alpha)) * mask
        fused += eo_frame * (1 - mask)

        return fused.astype(np.uint8)

    def thermal_highlight(self, eo_frame, ir_warped, ir_8bit_warped, threshold=200):
        """
        Overlay only hot regions from IR onto EO.
        Useful for SAR — highlights people/animals against background.
        """
        # Warp the 8-bit IR to get temperature proxy in EO coords
        h, w = eo_frame.shape[:2]
        ir_8bit_eo = cv2.warpPerspective(ir_8bit_warped, self.H, (w, h))

        # Create hot-region mask
        _, hot_mask = cv2.threshold(ir_8bit_eo, threshold, 255, cv2.THRESH_BINARY)
        hot_mask_3ch = cv2.merge([hot_mask, hot_mask, hot_mask])

        # Overlay coloured IR only in hot regions
        result = eo_frame.copy()
        result = np.where(hot_mask_3ch > 0, ir_warped, result)

        return result

    def process_frame(self, eo_frame, ir_raw_16bit, mode='blend'):
        """
        Main processing loop. Call once per synchronized frame pair.
        mode: 'blend', 'highlight', 'pip', 'ir_only'
        """
        ir_8bit = self.preprocess_ir(ir_raw_16bit)
        ir_color = self.colorize_ir(ir_8bit)

        if mode == 'ir_only':
            return cv2.resize(ir_color, (eo_frame.shape[1], eo_frame.shape[0]))

        if mode == 'pip':
            pip_size = (eo_frame.shape[1] // 4, eo_frame.shape[0] // 4)
            ir_pip = cv2.resize(ir_color, pip_size)
            result = eo_frame.copy()
            result[10:10+pip_size[1], 10:10+pip_size[0]] = ir_pip
            return result

        ir_warped = self.warp_ir_to_eo(ir_color, eo_frame.shape)

        if mode == 'blend':
            return self.blend(eo_frame, ir_warped)
        elif mode == 'highlight':
            ir_8bit_warped = cv2.warpPerspective(ir_8bit, self.H,
                                (eo_frame.shape[1], eo_frame.shape[0]))
            return self.thermal_highlight(eo_frame, ir_warped, ir_8bit_warped)
```

**Calibration script for computing H:**

```python
def calibrate_eo_ir(eo_image, ir_image, num_points=8):
    """
    Interactive calibration: user clicks corresponding points
    in EO and IR images of a heated checkerboard target.
    """
    eo_points = []
    ir_points = []

    # ... (interactive point selection GUI) ...

    eo_pts = np.array(eo_points, dtype=np.float32)
    ir_pts = np.array(ir_points, dtype=np.float32)

    H, mask = cv2.findHomography(ir_pts, eo_pts, cv2.RANSAC, 5.0)
    return H
```

---

## 4. Radiometric vs Non-Radiometric

### 4.1 Fundamental Distinction

**Non-radiometric (relative):** The sensor outputs a signal proportional to incident infrared radiation, but the mapping from signal to absolute temperature is not calibrated or maintained. The output shows relative thermal contrast — hotter objects appear brighter (or darker in black-hot palette) than cooler objects. The exact temperature of any pixel is unknown.

**Radiometric (absolute):** The sensor includes factory calibration data that maps the raw detector signal to absolute object temperature (in °C or K) for each pixel. This calibration accounts for sensor gain, offset, lens transmission, and internal sensor temperature. The output includes a per-pixel temperature value (typically in centikelvins or tenths of degrees in the raw data stream).

### 4.2 Radiometric Accuracy at Altitude

Factory radiometric accuracy for uncooled microbolometer cores is typically ±2°C or ±2% of reading (whichever is larger) for blackbody targets under laboratory conditions. At altitude, additional error sources include:

**Atmospheric transmission:** The atmosphere between sensor and target absorbs and emits IR radiation. Without atmospheric correction, a 100°C target at 200 m range in humid conditions might read 94–97°C. The correction requires knowledge of:
- Air temperature (from Pixhawk barometer/thermometer)
- Relative humidity (requires a humidity sensor; not standard on Pixhawk)
- Path length (from altitude + look angle)

**Reflected ambient radiation:** Objects are not perfect blackbodies. The measured apparent temperature includes reflected ambient radiation (sky, surroundings). For high-emissivity targets (skin ε ≈ 0.98, vegetation ε ≈ 0.95), this effect is small. For low-emissivity targets (metal ε ≈ 0.1–0.5), the error can be enormous.

**Downwelling sky radiation:** The sky radiates at an effective temperature of approximately -40°C to -60°C in the LWIR (clear sky). When looking down at a target, the target reflects some of this cold sky radiation, causing it to appear cooler than its true temperature. The magnitude depends on target emissivity and sky conditions.

**Practical radiometric accuracy at typical UAV operating conditions (100 m AGL, temperate climate):**

| Condition | Accuracy (uncorrected) | Accuracy (atm. corrected) |
|---|---|---|
| Clear, dry, ε > 0.95 | ±3–5°C | ±2–3°C |
| Clear, humid, ε > 0.95 | ±5–8°C | ±2–4°C |
| Clear, any, ε < 0.5 | ±10–30°C | ±5–15°C |
| Light rain/haze | ±10–20°C | ±5–10°C |

### 4.3 When Radiometric Is Required

| Application | Radiometric Required? | Reason |
|---|---|---|
| SAR person detection | **No** | Person-background contrast (2–10 K) far exceeds NETD; only relative contrast matters |
| Wildlife counting | **No** | Animal-background contrast is sufficient for detection; absolute temperature unnecessary |
| Fire detection (presence) | **No** | Fire/hotspot contrast is extreme (hundreds of degrees); relative imaging detects easily |
| Fire detection (temperature mapping) | **Yes** | Determining fire intensity, mapping temperature contours for fire behaviour prediction |
| Building thermal inspection | **Yes** | Must quantify heat loss in W/m², compare to standards; requires calibrated temperature |
| Electrical/industrial inspection | **Yes** | Must measure component temperatures to assess failure risk against rated limits |
| Agricultural crop stress | **Depends** | Canopy temperature relative to air temperature (crop water stress index) requires radiometric; simple stress detection does not |
| Volcanic/geothermal monitoring | **Yes** | Absolute temperature measurement for hazard assessment |
| Roof moisture detection | **Marginal** | Wet areas are detectable by relative contrast (higher thermal mass = slower cooling); radiometric adds quantitative analysis |

### 4.4 Radiometric Sensors Available for This Platform

| Sensor | Radiometric Output | Accuracy | Notes |
|---|---|---|---|
| FLIR Lepton 3.5 R | Per-pixel, °C×100 in raw | ±5°C (lab) | Limited by 160×120 resolution |
| FLIR Boson+ 640 | Per-pixel telemetry | ±5°C or ±5% | Requires Boson+ variant; adds ~£500 premium |
| FLIR Tau 2 R | Per-pixel via digital interface | ±2°C or ±2% | Best accuracy but heaviest/most expensive |
| InfiRay Micro III (radiometric variant) | Per-pixel | ±2°C (claimed) | Availability and documentation uncertain |

### 4.5 Practical Recommendation

For most UAV applications on this platform, a non-radiometric Boson 640 is sufficient and preferred. The Boson 640 in standard (non-radiometric) mode still outputs 16-bit data that is monotonically related to scene temperature; this is perfectly adequate for detection, relative comparison, and thresholding. If building/industrial inspection is a planned mission, select the Boson+ variant or add a separate radiometric payload for those specific missions.

---

## 5. AI-Based Detection on Thermal Imagery

### 5.1 Person Detection Models

#### 5.1.1 Architecture Selection

**YOLOv5/YOLOv8 (Recommended):**
The YOLO family provides the best balance of accuracy and inference speed for edge deployment. YOLOv8-nano achieves real-time performance (>30 fps) on Jetson Nano at 640×640 input resolution. YOLOv5s is well-supported with extensive documentation for custom training.

Key consideration: thermal images have fundamentally different characteristics from visible images. Pre-trained weights (on COCO, ImageNet, etc.) provide only marginal benefit for thermal transfer learning because feature distributions differ. Fine-tuning or training from scratch on thermal data is essential.

**SSD (Single Shot Detector):**
MobileNet-SSD provides faster inference than YOLO at the cost of lower accuracy, particularly for small targets. On a Coral Edge TPU, MobileNet-SSD-v2 runs at approximately 70 fps at 300×300 input. However, the 300×300 input resolution is limiting for aerial thermal imagery where targets are small.

**EfficientDet:**
EfficientDet-D0 provides good accuracy at moderate computational cost. The TensorFlow Lite version runs efficiently on Coral Edge TPU. Better small-object detection than SSD due to BiFPN feature pyramid.

#### 5.1.2 Training Data Sources

**Public aerial thermal person detection datasets:**

| Dataset | Size | Resolution | Altitude Range | Annotations | Access |
|---|---|---|---|---|---|
| **FLIR ADAS** | ~14,000 images | 640×512 | Ground level (vehicle) | Bbox (person, car, bicycle) | Free (FLIR website) |
| **KAIST Multispectral** | ~95,000 frame pairs | 640×480 (visible + LWIR) | Ground level | Bbox (person) | Free (academic) |
| **BIRDSAI** | Aerial drone thermal video | 640×512 | 50–120 m | Bbox (person, animal) | Request-based |
| **HOTSPOT** | Aerial thermal wildlife | Various | Various | Bbox (animal) | NOAA, free |
| **DroneVehicle** | ~56,000 images | Various | 30–100 m | Bbox (vehicle, person) | Request-based |
| **VisDrone** (thermal subset) | Limited | Various | 10–100 m | Bbox (multi-class) | Free |
| **AU-AIR** | Aerial multi-modal | Including thermal | Various | Bbox | Free |
| **VEDAI** | Aerial EO (no thermal) | — | — | — | Useful for data augmentation |

**Critical issue:** There is a significant gap in publicly available aerial thermal datasets specifically for SAR scenarios (person lying in field/forest, at 50–200 m AGL). Most available datasets are ground-level automotive. The most effective approach is to collect a custom dataset using the actual sensor (Boson 640) on the actual platform at the planned operating altitudes.

**Data augmentation for thermal:**
- Random brightness/contrast shifts (simulating ambient temperature variation)
- Horizontal flip
- Random crop/zoom (simulating altitude variation)
- Gaussian noise injection (simulating sensor noise)
- Do NOT use colour jitter or hue shifts (thermal images are single-channel)

#### 5.1.3 Edge Inference Hardware Comparison

| Feature | Google Coral USB Accelerator | Jetson Nano (4 GB) | Jetson Orin Nano |
|---|---|---|---|
| **Compute** | 4 TOPS (int8 only) | 472 GFLOPS (FP16) | 40 TOPS (int8), 20 TFLOPS (FP16) |
| **Framework** | TensorFlow Lite only | TensorRT, PyTorch, TF | TensorRT, PyTorch, TF |
| **Supported models** | Edge TPU-compiled TFLite | Any (ONNX, TensorRT optimized) | Any |
| **YOLOv8-nano fps** | ~15–25 fps (300×300) | ~20–30 fps (640×640) | ~60–100 fps (640×640) |
| **Power** | 2–4 W (+ host computer) | 5–10 W | 7–15 W |
| **Weight** | 10 g (+ host RPi4: 46 g) | 140 g (with carrier) | 200 g |
| **Flexibility** | Limited (int8 quantized only) | Full (custom layers, dynamic models) | Full |
| **Total system weight** | ~56 g (Coral + RPi4) | 140 g | 200 g |

**Recommendation:**

- **Budget/weight-constrained:** Raspberry Pi 4 + Coral USB. Run MobileNet-SSD or EfficientDet-Lite on Coral for detection, use RPi CPU for fusion/recording. Total ~56 g, ~5–8 W.
- **Performance-focused:** Jetson Nano. Run YOLOv8-nano with TensorRT optimization. Single board handles fusion, detection, recording, and MAVLink communication. 140 g, 5–10 W.
- **Future-proof:** Jetson Orin Nano. Massive headroom for multi-model pipelines (detection + tracking + classification). 200 g, 7–15 W.

### 5.2 Detection Accuracy vs Altitude and Conditions

Based on published literature and practical testing:

| Altitude | Target pixels (Boson 640, 24° lens) | YOLOv8-nano mAP50 (estimate) | Notes |
|---|---|---|---|
| 30 m | ~90 pixels (person height) | 85–92% | Large target, high confidence |
| 60 m | ~45 pixels | 75–85% | Good detection, reliable recognition |
| 100 m | ~27 pixels | 60–75% | Detection reliable, recognition challenging |
| 150 m | ~18 pixels | 45–60% | Detection marginal, small object regime |
| 200 m | ~14 pixels | 30–45% | Below reliable detection for most models |
| 300 m | ~9 pixels | 15–25% | Sub-pixel regime approaching; detection unreliable |

**Environmental effects on detection accuracy:**

| Condition | Impact on Detection | Mitigation |
|---|---|---|
| Night, calm, clear | **Best case** — maximum thermal contrast | None needed |
| Day, overcast | **Good** — moderate contrast, no solar loading | None needed |
| Day, sunny | **Degraded** — solar-heated surfaces mimic body temp | Increase detection threshold; use motion cues |
| Rain | **Variable** — rain cools targets but also cools background | Retrain model on wet-condition data |
| High wind | **Degraded** — convective cooling reduces target temperature | Lower detection threshold |
| After sunset (1–2 hr) | **Excellent** — thermal crossover eliminates solar clutter | Optimal survey window |

### 5.3 False Positive Management

False positives are the primary operational challenge for thermal person detection. Common false positive sources:

| Source | Thermal Signature | Mitigation Strategy |
|---|---|---|
| Animals (deer, dogs, etc.) | Similar temperature to humans | Train classifier to distinguish body shape; use size estimation from altitude |
| Sun-heated rocks/metal | Can match body temperature | Use temporal filtering (rocks cool/heat slowly vs. people moving); shape analysis |
| Vehicle engines | Hot, compact | Size and shape classification; GPS-based road masking |
| Exhaust vents/chimneys | Hot point sources | Geographic masking using maps; persistence filtering |
| Water reflections | Variable, can appear hot | Polarimetric analysis (if available); geographic masking |
| Recently occupied surfaces | Residual heat | Temporal filtering (heat dissipates quickly vs. persistent occupancy) |

**Multi-stage detection pipeline (recommended):**

1. **Stage 1: Thermal anomaly detection** — simple threshold or blob detection on the thermal image to identify all regions warmer than background by a configurable margin. Fast, high recall, high false positive rate.
2. **Stage 2: CNN classification** — crop each anomaly region, resize to model input, classify as person/animal/vehicle/other using a trained classifier. Moderate speed, reduces false positives by 80–90%.
3. **Stage 3: Temporal tracking** — use a tracker (SORT, DeepSORT, ByteTrack) to maintain object identity across frames. Reject detections that appear for only 1–2 frames (transient noise). Confirm detections that persist across multiple frames.
4. **Stage 4: Geometric validation** — estimate object size from pixel extent and altitude; reject detections inconsistent with expected target size (e.g., a "person" detection covering 50 m² is clearly a heated surface).

---

## 6. Specific Applications

### 6.1 Search and Rescue (SAR)

#### 6.1.1 Detection Probability vs Search Speed vs Altitude

The fundamental SAR trade-off: higher altitude means wider ground coverage (faster search) but lower spatial resolution (reduced detection probability per pass).

**Swath width calculation:**

```
Swath width = 2 × altitude × tan(HFOV / 2)
```

For Boson 640 with 24° HFOV:

| Altitude (m) | Swath Width (m) | GSD (m/px) | Person pixels (height) | Coverage rate at 20 m/s (km²/hr) |
|---|---|---|---|---|
| 50 | 21.3 | 0.033 | 54 | 1.53 |
| 80 | 34.1 | 0.053 | 34 | 2.45 |
| 100 | 42.6 | 0.066 | 27 | 3.07 |
| 150 | 63.9 | 0.100 | 18 | 4.60 |
| 200 | 85.2 | 0.133 | 14 | 6.13 |

**Detection probability per pass (estimated for person, Boson 640, trained operator or AI):**

| Altitude | Pd per pass (still person) | Pd per pass (moving person) | Notes |
|---|---|---|---|
| 50 m | 95% | 98% | Very high; person is large and obvious |
| 80 m | 88% | 95% | High; comfortable detection |
| 100 m | 78% | 90% | Good; recommended operational altitude |
| 150 m | 55% | 75% | Marginal; second pass recommended |
| 200 m | 35% | 55% | Unreliable; use only for wide-area cueing |

**Cumulative detection probability over N passes:**

```
Pd_cumulative = 1 - (1 - Pd_per_pass)^N
```

At 100 m altitude with Pd = 0.78 per pass:
- 1 pass: 78%
- 2 passes: 95.2%
- 3 passes: 98.9%

**Optimal SAR strategy for this platform (assuming 30–45 min endurance):**

1. **Phase 1 — Wide area cueing (150 m AGL):** Fly a grid pattern covering the maximum probable area. Use AI detection to flag thermal anomalies. Coverage rate ~4.6 km²/hr. Accept high false positive rate.
2. **Phase 2 — Targeted verification (80 m AGL):** Re-fly over each flagged anomaly at lower altitude. Verify or dismiss each detection. AI + operator confirmation.
3. **Phase 3 — Identification pass (50 m AGL, if needed):** Orbit confirmed detections for visual/thermal identification. Switch to EO camera if daylight.

#### 6.1.2 Night Operations

Thermal imaging is most effective for SAR at night:
- Maximum thermal contrast between person (~33°C skin, ~25–30°C clothed) and environment (~5–15°C vegetation/ground)
- No solar loading clutter
- Detection probability increases by 15–25% compared to daytime

**Best window:** 2–4 hours after sunset (ground has cooled, person has not).

#### 6.1.3 Person in Water Detection

Water surface temperature is relatively uniform. A person's head (the only exposed surface) presents approximately 0.01–0.02 m² of thermal signature. At 100 m AGL with Boson 640, a head subtends approximately 2–3 pixels — at the Johnson detection limit. Detection in water is significantly more challenging than on land. Recommended altitude: 50 m or below for water SAR. A person's thermal wake (disturbed water) may be visible for several minutes and can aid detection.

### 6.2 Wildlife Survey

#### 6.2.1 Animal Counting

Thermal imaging enables automated animal counting that is:
- Independent of camouflage and vegetation cover
- Effective at night when many species are active
- Less disturbing to wildlife than low-altitude visible-light survey

**Detection capability by animal size (Boson 640, 100 m AGL):**

| Animal | Body size (m) | Pixels at 100 m | Detectable? | Countable? |
|---|---|---|---|---|
| Elephant | 3.5 × 2.0 | 53 × 30 | Yes | Yes, individually |
| Deer/large ungulate | 1.5 × 1.0 | 23 × 15 | Yes | Yes |
| Sheep/goat | 0.7 × 0.5 | 11 × 8 | Yes | Yes (groups may merge) |
| Fox/hare | 0.4 × 0.2 | 6 × 3 | Marginal | No (insufficient resolution) |
| Bird (large, grouse) | 0.3 × 0.2 | 5 × 3 | Marginal | No |
| Rodent | 0.1 × 0.05 | 1.5 × 0.8 | No | No |

**Thermal contrast considerations for wildlife:**
- Fur/feather insulation reduces apparent surface temperature compared to skin temperature
- Animals in sun-heated environments may have reduced contrast during day
- Resting animals (curled, lower metabolic rate) have lower contrast than active animals
- Wet animals have significantly different thermal signatures (higher emissivity, evaporative cooling)

#### 6.2.2 Anti-Poaching

Thermal imaging for poacher detection is functionally identical to SAR person detection, with additional requirements:
- Extended loiter time (patrol rather than search)
- Real-time alerting to ground teams
- Recording with GPS coordinates for evidence
- Detection of vehicles (engine heat) at greater range than persons
- Discrimination of authorized personnel (rangers) from intruders (requires communication/tracking integration)

### 6.3 Fire Detection

#### 6.3.1 Hotspot Identification

Fire presents an extreme thermal signature. Even the Lepton 2.5 (80×60) can detect active fire at significant range. The challenge is not detection but characterisation:

**Temperature ranges and sensor saturation:**

| Scene Element | Temperature | Notes |
|---|---|---|
| Background vegetation | 10–30°C | Normal ambient |
| Sun-heated ground | 40–70°C | Daytime solar loading |
| Smouldering embers | 200–400°C | Sub-surface combustion |
| Active flame front | 600–1,200°C | Open combustion |

Standard uncooled microbolometers saturate above approximately 120–150°C (scene temperature) in their default configuration. Most cores offer a "high-gain" and "low-gain" mode:

- **High gain (default):** Optimized for -40°C to +120°C scene. Best NETD. Saturates on fire.
- **Low gain:** Extended to +400°C or even +600°C. Higher NETD (~2× worse). Required for fire characterisation.
- **Dual-gain (Boson 640):** Automatically switches or captures both; provides full dynamic range.

For fire detection (presence/absence), high-gain mode is fine — saturation simply confirms "very hot." For fire temperature mapping, low-gain or dual-gain mode is required, and radiometric calibration is essential.

#### 6.3.2 Fire Line Mapping

A fixed-wing UAV provides efficient fire perimeter mapping:
- Fly at 150–200 m AGL along the fire perimeter
- Record geotagged thermal video
- Post-process to generate orthorectified thermal mosaic
- Overlay on GIS map for incident command

At 150 m AGL with Boson 640 (50° HFOV lens for wider coverage), swath width is approximately 140 m. At 25 m/s airspeed, a 10 km fire perimeter can be mapped in approximately 7 minutes.

**Smoke penetration:** LWIR (8–14 µm) penetrates thin to moderate smoke effectively. Thick, optically dense smoke blocks LWIR. MWIR (3–5 µm) cores provide better smoke penetration but are cooled sensors (heavy, expensive, not suitable for this platform). In practice, the UAV should fly upwind of the fire to minimize smoke between sensor and target.

### 6.4 Building Inspection

#### 6.4.1 Heat Loss Assessment

Building thermal inspection from UAV requires:
- **Radiometric sensor** (mandatory for quantitative assessment)
- **Known emissivity** of building materials (brick ε ≈ 0.93, glass ε ≈ 0.92, metal cladding ε ≈ 0.2–0.7)
- **Indoor-outdoor temperature differential** of at least 10°C (ideally >15°C)
- **Low wind conditions** (<5 m/s) to minimize convective heat transfer masking
- **Overcast sky or night** to eliminate solar loading artifacts
- **Flight altitude** 20–50 m for facades, 30–80 m for rooftops

**Common defects detectable:**

| Defect | Thermal Signature | Minimum ΔT Required | Sensor Requirement |
|---|---|---|---|
| Missing insulation | Hot patch on exterior wall | 2–5°C | Radiometric, ≥320×256 |
| Thermal bridge (lintel, slab edge) | Linear hot feature | 1–3°C | Radiometric, ≥320×256 |
| Air leakage | Hot spot near windows/doors | 2–8°C | Radiometric, ≥320×256 |
| Moisture in flat roof | Warm patch at night (thermal mass) | 1–3°C | Radiometric, ≥640×512 recommended |
| Underfloor heating failure | Cold patch in heated zone | 3–10°C | Radiometric |
| Solar panel defect (hot cell) | Hot spot on panel | 5–20°C | Radiometric, ≥320×256 |

#### 6.4.2 Moisture Detection

Moisture detection exploits the high thermal mass of water. After sunset, dry building materials cool rapidly; wet areas retain heat longer due to water's specific heat capacity (4.18 kJ/kg·K vs ~0.8–1.0 for dry building materials). The optimal survey window is 2–4 hours after sunset on a clear, calm evening following a warm day.

At dawn (pre-sunrise), the effect reverses: wet areas are cooler because they absorbed less heat during the night. Both windows are usable; the post-sunset window typically provides stronger contrast.

### 6.5 Security and Perimeter Monitoring

For persistent perimeter monitoring, the fixed-wing UAV provides:

- **Area coverage rate:** 3–5 km²/hr at 100 m AGL
- **Intruder detection range:** 200–500 m (Boson 640, depends on background)
- **Endurance-limited patrol radius:** At 30 min endurance and 20 m/s, total path length ~36 km; perimeter length of ~10 km can be re-surveyed every ~10 minutes

**Integration with ground systems:**
- MAVLink telemetry to ground station includes UAV position and attitude
- Detection algorithm outputs target GPS coordinates (derived from UAV position + gimbal angle + altitude)
- Coordinates transmitted to ground patrol for intercept
- Target tracking across multiple passes enables velocity/heading estimation

---

## 7. Environmental Factors

### 7.1 Performance in Rain, Fog, and Cloud

#### Rain

| Rain Intensity | Rate (mm/hr) | LWIR Transmission (100 m) | Effect on Detection |
|---|---|---|---|
| Drizzle | 0.5 | 95% | Negligible impact |
| Light rain | 2 | 90% | Minor degradation; person detection reliable |
| Moderate rain | 5 | 78% | Noticeable degradation; reduce altitude |
| Heavy rain | 15 | 55% | Significant; detection range halved |
| Torrential | 50 | 20% | Thermal imaging largely ineffective |

Rain on the target also changes its thermal signature: wet clothing and wet skin have different emissivity and temperature (evaporative cooling reduces apparent temperature by 2–8°C). In rain, a person may present less thermal contrast against wet surroundings.

Rain on the sensor window is a critical practical problem. Water droplets on the germanium lens dramatically degrade image quality. The payload bay must include a lens wiper or hydrophobic coating, and the lens should be recessed or shielded from direct rain impingement.

#### Fog

Fog is composed of water droplets 1–50 µm in diameter. LWIR radiation (8–14 µm wavelength) is scattered by droplets of similar size, making fog highly attenuating:

| Fog Type | Visibility | LWIR Transmission (100 m) | Usable? |
|---|---|---|---|
| Thin haze | 2–5 km | 90–95% | Yes, full performance |
| Light fog | 500 m–1 km | 50–70% | Yes, reduced range |
| Moderate fog | 200–500 m | 20–40% | Marginal; fly below fog layer |
| Dense fog | <200 m | <10% | No; thermal imaging ineffective |

**Important:** LWIR does NOT "see through fog" as is commonly claimed. It performs somewhat better than visible light in haze and very light fog, but dense fog defeats both modalities. The advantage of thermal in fog is that it does not require illumination — a person's thermal emission penetrates thin fog better than reflected light from a searchlight.

#### Cloud

For a UAV operating below cloud base, cloud is irrelevant. The UAV must remain VFR or within BVLOS regulatory clearance below the cloud layer. If operating within cloud (unlikely for this platform class), thermal imaging is completely defeated.

### 7.2 Crosswind Cooling Effects

Wind causes convective cooling of exposed surfaces, reducing the apparent thermal signature:

```
Heat loss ∝ h_conv × (T_surface - T_air)
h_conv ∝ √(wind_speed)  (for forced convection over a flat plate)
```

**Quantitative effect on person signature:**

| Wind Speed | Apparent Temperature Reduction (exposed skin) | Effect on Detection |
|---|---|---|
| Calm (0–2 m/s) | 0°C (reference) | Best thermal contrast |
| Light (2–5 m/s) | -1 to -2°C | Negligible impact |
| Moderate (5–10 m/s) | -2 to -5°C | Minor reduction; still detectable |
| Strong (10–15 m/s) | -5 to -10°C | Significant; target approaches background |
| Gale (>15 m/s) | -8 to -15°C | Thermal signature may be lost; also, fixed-wing UAV operations become challenging |

Wind also cools background surfaces, but differentially: exposed surfaces cool more than sheltered ones. This can actually improve detection in some cases (person sheltered behind a wall stands out more as the wall's windward face cools).

**Wind also affects the UAV platform:**
- Fixed-wing in headwind: reduced ground speed, reduced coverage rate, but improved resolution (more time per pixel)
- Fixed-wing in crosswind: image smear if frame rate is too low relative to cross-track velocity; 60 fps Boson mitigates this
- Gusts cause gimbal disturbance: servo-stabilised gimbals required above 5 m/s; platform vibration increases

### 7.3 Time of Day Effects

#### Thermal Crossover

"Thermal crossover" occurs when objects that were warmer than their surroundings become the same temperature, then cooler. This happens twice daily:

1. **Morning crossover (30–90 min after sunrise):** Objects that were cooler overnight (low thermal mass items, thin metal) heat rapidly in sunlight and pass through ambient temperature. Objects with high thermal mass (concrete, soil) are still cool.
2. **Evening crossover (30–90 min after sunset):** Reverse of morning. Low thermal mass objects cool rapidly below ambient; high thermal mass objects remain warm.

During crossover periods, thermal contrast is minimized and detection performance is worst. The duration depends on material properties and weather conditions but typically lasts 15–45 minutes.

#### Optimal Survey Windows

| Time Window | Thermal Contrast (person) | Background Clutter | Overall Detection Quality |
|---|---|---|---|
| Pre-dawn (3–5 AM) | **Excellent** (8–15 K) | **Low** | **Best** |
| Morning crossover (sunrise +30–60 min) | **Poor** (0–3 K) | **High** (rapidly changing) | **Worst** |
| Mid-morning (sunrise +2–4 hr) | **Fair** (3–6 K) | **Moderate** (solar loading building) | **Fair** |
| Solar noon | **Variable** (2–8 K) | **High** (many false positives) | **Poor** |
| Afternoon | **Variable** (2–5 K) | **High** | **Poor** |
| Evening crossover (sunset +30–60 min) | **Poor** (0–3 K) | **High** | **Worst** |
| Post-sunset (sunset +2–4 hr) | **Excellent** (8–12 K) | **Low** (cooling) | **Best** |
| Night (midnight) | **Excellent** (10–15 K) | **Very low** | **Best** |

#### Solar Loading

During daytime, the sun heats surfaces to well above ambient air temperature:

- Dark asphalt: 50–70°C (20–40 K above ambient)
- Concrete: 40–55°C
- Metal roofing: 50–80°C
- Vegetation: 25–35°C (transpiration limits heating)
- Soil: 35–50°C

A person at 33°C (clothed surface ~28–30°C) can appear **cooler** than sun-heated ground during peak solar hours. This is the primary cause of missed detections and false positives during daytime thermal survey.

**Mitigation strategies for daytime operation:**
- Fly higher to blur small hot features; rely on person-sized thermal anomalies
- Use AI models trained specifically on daytime thermal data
- Combine thermal with EO; use thermal for cueing, EO for confirmation
- Use relative contrast (hot-relative-to-local-background) rather than absolute threshold
- Prefer shadows and vegetated areas for initial search priority

### 7.4 Optimal Flight Conditions Summary

**Ideal conditions for thermal imaging survey:**

| Parameter | Ideal Value | Acceptable Range | Avoid |
|---|---|---|---|
| Time of day | 2–4 hr after sunset; pre-dawn | Any night; overcast day | Sunrise/sunset crossover; clear midday |
| Wind | Calm (<3 m/s) | <8 m/s | >12 m/s |
| Cloud cover | Overcast (day) / Clear (night) | Any (day); clear-scattered (night) | Fog, low cloud |
| Rain | None | Light drizzle | Moderate+ rain |
| Humidity | <60% RH | <80% RH | >90% RH (condensation risk) |
| Temperature differential | >10 K between target and background | >5 K | <3 K (crossover) |
| ΔT (indoor-outdoor for buildings) | >15°C | >10°C | <5°C |

---

## Appendix A: System Integration Summary

### Recommended Configuration for This Platform

**Primary configuration (performance):**
- Sensor: FLIR Boson 640, 24° HFOV lens (non-radiometric unless building inspection required)
- Companion computer: Jetson Nano 4 GB
- EO camera: Raspberry Pi Camera Module 3 (wide)
- Recording: 256 GB microSD for dual-stream recording
- MAVLink: UART to Pixhawk for telemetry + trigger synchronization
- Total payload weight: ~250 g (sensor + computer + cameras + mounting)
- Total power: ~12 W (from dedicated BEC off main battery)

**Budget configuration:**
- Sensor: InfiRay Micro III 640 or Boson 320
- Companion computer: Raspberry Pi 4 (4 GB) + Google Coral USB
- EO camera: Raspberry Pi Camera Module 3
- Total payload weight: ~150 g
- Total power: ~8 W

**Minimum viable configuration:**
- Sensor: FLIR Lepton 3.5 on PureThermal Mini breakout
- Companion computer: Raspberry Pi Zero 2W
- No EO fusion
- Total payload weight: ~50 g
- Total power: ~3 W

### Payload Bay Compliance

All configurations fit within the specified 200×300×150 mm payload bay with margin. The primary configuration (250 g) is well within the 4 kg payload limit, leaving substantial capacity for gimbal (200–400 g), additional sensors, or extended battery. Even the heaviest conceivable configuration (Tau 2 + Jetson Xavier NX + 2-axis gimbal + recording system) totals approximately 800 g — 20% of the payload budget.

### ArduPilot Integration Points

- **MAVLink camera trigger:** Pixhawk sends DO_DIGICAM_CONTROL or DO_SET_CAM_TRIGG_DIST commands; companion computer captures synchronized frame + GPS/attitude metadata
- **Gimbal control:** MAVLink gimbal protocol (v2) for stabilization commands; or direct PWM from Pixhawk auxiliary outputs to servo-driven gimbal
- **Telemetry relay:** Companion computer receives detection alerts, encodes GPS coordinates, sends via MAVLink STATUSTEXT or custom message to ground station
- **Autonomous search patterns:** ArduPilot AUTO mode with grid/survey waypoint missions; camera trigger at calculated intervals for complete ground coverage

---

This specification covers the critical technical dimensions for thermal payload integration on the described platform. The FLIR Boson 640 with a Jetson Nano companion computer represents the optimal configuration for most applications, providing 640×512 resolution at 60 Hz with onboard AI inference capability, all within approximately 250 g and 12 W — a fraction of the platform's capacity.
