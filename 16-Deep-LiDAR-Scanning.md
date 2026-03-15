# Technical Specification: LiDAR Scanning Payloads for Mini Fixed-Wing UAV

**Platform Reference:** 2–4 m wingspan fixed-wing, 4 kg max payload, 200x300x150 mm payload bay, ArduPilot/Pixhawk autopilot

**Document Revision:** 2026-03-15

---

## 1. LiDAR Sensor Comparison

### 1.1 Selection Criteria

Sensors were evaluated against the hard constraints of the platform: maximum mass 4 kg (entire payload assembly including compute, IMU, GPS, wiring, and mount), bay volume 200x300x150 mm, available power from a typical fixed-wing power bus (5V/12V rails, practical ceiling around 60–80 W total for all payloads), and the need for an interface compatible with a companion computer (Ethernet or serial/UART).

### 1.2 Detailed Sensor Specifications

#### 1.2.1 Livox Mid-40

| Parameter | Value |
|---|---|
| Range | 260 m (80% reflectivity), 90 m (10% reflectivity) |
| Points per second | 100,000 |
| Field of View | 38.4° circular |
| Range accuracy | ±2 cm (RMS) |
| Angular accuracy | <0.05° |
| Scan pattern | Non-repetitive, Risley prism (flower/rosette) |
| Weight | 750 g (sensor only), ~880 g with cable |
| Dimensions | 88 x 69 x 76 mm |
| Power consumption | 10 W typical |
| Supply voltage | 10–16 V DC |
| Interface | 100 Mbps Ethernet (UDP) |
| Operating temperature | -20°C to +65°C |
| Laser wavelength | 905 nm |
| Laser class | Class 1 |
| Approximate price | $600–800 USD (discontinued, secondary market) |
| Notes | Excellent price/performance; non-repetitive pattern means coverage density increases with integration time. FOV is relatively narrow — best suited for nadir corridor mapping. Discontinued by Livox but widely available. |

#### 1.2.2 Livox Mid-70

| Parameter | Value |
|---|---|
| Range | 260 m (80%), 90 m (10%) |
| Points per second | 100,000 |
| Field of View | 70.4° circular |
| Range accuracy | ±2 cm |
| Scan pattern | Non-repetitive, Risley prism |
| Weight | 750 g |
| Dimensions | 88 x 69 x 76 mm |
| Power consumption | 10 W |
| Supply voltage | 10–16 V DC |
| Interface | 100 Mbps Ethernet |
| Approximate price | $850–1,000 USD (secondary market) |
| Notes | Same physical package as Mid-40 but nearly double the FOV. The wider FOV reduces point density at any given integration time versus Mid-40 but provides much better cross-track coverage from a fixed-wing. Preferred over Mid-40 for area mapping. |

#### 1.2.3 Livox Mid-360

| Parameter | Value |
|---|---|
| Range | 40 m (10% reflectivity), 70 m (80%) |
| Points per second | 200,000 |
| Field of View | 360° horizontal x 59° vertical |
| Range accuracy | ±3 cm (RMS, 0.2–25 m range) |
| Scan pattern | Non-repetitive, triple Risley prism |
| Weight | 265 g |
| Dimensions | 65 mm diameter x 60 mm height |
| Power consumption | 5.5 W typical |
| Supply voltage | 9–27 V DC |
| Interface | 100 Mbps Ethernet |
| Approximate price | $250–350 USD |
| Notes | Dramatically lighter and cheaper than Mid-40/70. The 360° FOV is unusual for a Livox and makes it attractive for SLAM applications. However, the maximum range is severely limited — 40 m at 10% reflectivity means marginal performance above 30–35 m AGL over dark surfaces (wet soil, asphalt). Best suited for low-altitude (<40 m AGL) missions. The low weight (265 g) makes it the most mass-efficient option on this list. |

#### 1.2.4 Livox Avia

| Parameter | Value |
|---|---|
| Range | 320 m (80%), 190 m (10%) at 100 klx ambient |
| Points per second | 240,000 (triple return mode) |
| Field of View | 70.4° circular |
| Range accuracy | ±2 cm |
| Angular accuracy | <0.05° |
| Scan pattern | Non-repetitive, Risley prism |
| Weight | 498 g |
| Dimensions | 107 x 80 x 62 mm |
| Power consumption | 11 W typical |
| Supply voltage | 9–27 V DC |
| Interface | 1 Gbps Ethernet |
| Laser wavelength | 905 nm |
| Approximate price | $1,200–1,500 USD |
| Notes | Currently Livox's flagship for UAV mapping. Triple return mode is very valuable for vegetation penetration (forestry). Higher point rate than Mid-40/70. Range is excellent. Weight under 500 g is highly attractive. The 1 Gbps Ethernet requirement means the companion computer needs a GbE port (rules out bare RPi 4 without USB-Ethernet adapter). This is the recommended Livox sensor for this platform. |

#### 1.2.5 Livox HAP

| Parameter | Value |
|---|---|
| Range | 150 m (10% reflectivity) |
| Points per second | 450,000 |
| Field of View | 120° x 25° (rectangular) |
| Range accuracy | ±2 cm |
| Scan pattern | Non-repetitive, MEMS-hybrid |
| Weight | 400 g |
| Dimensions | 95 x 74 x 60 mm |
| Power consumption | 9 W |
| Supply voltage | 9–30 V DC |
| Interface | 1 Gbps Ethernet |
| Approximate price | $400–600 USD |
| Notes | Originally designed for automotive ADAS. The rectangular FOV with 120° horizontal is the widest single-sensor coverage here — excellent for cross-track swath in fixed-wing mapping. Very high point rate. However, the 25° vertical aperture is limiting for SLAM applications. Best suited for nadir-mounted corridor or area survey. |

#### 1.2.6 Ouster OS0-32

| Parameter | Value |
|---|---|
| Range | 50 m (Lambertian target), 35 m at 10% reflectivity |
| Points per second | 655,360 (32 channels x 2048 azimuth x 10 Hz) |
| Field of View | 360° x 90° (+45° to -45°) |
| Range accuracy | ±1.5–5 cm (range dependent) |
| Angular resolution | 0.18° horizontal (2048 mode), 2.8° vertical |
| Scan pattern | Spinning, 32 channels |
| Weight | 447 g |
| Dimensions | 73 x 73 x 54 mm |
| Power consumption | 14–20 W |
| Supply voltage | 12–24 V DC |
| Interface | 1 Gbps Ethernet |
| Laser wavelength | 865 nm |
| Approximate price | $4,000–6,000 USD |
| Notes | Ultra-wide 90° vertical FOV is unique. Short-range sensor optimized for robotics/indoor — 50 m max range makes it marginal for UAV mapping above 30 m AGL. High power draw is a concern. The 360° mechanical spinning introduces gyroscopic effects in a fixed-wing (though minor at the sensor's small mass). Also outputs near-infrared imagery and ambient imagery per revolution — potentially useful for colorized point clouds. |

#### 1.2.7 Ouster OS0-64

| Parameter | Value |
|---|---|
| Range | 50 m (same optics as OS0-32) |
| Points per second | 1,310,720 (64 channels x 2048 x 10 Hz) |
| Field of View | 360° x 90° |
| Range accuracy | ±1.5–5 cm |
| Angular resolution | 0.18° horizontal, 1.4° vertical |
| Scan pattern | Spinning, 64 channels |
| Weight | 447 g |
| Dimensions | 73 x 73 x 54 mm |
| Power consumption | 14–20 W |
| Interface | 1 Gbps Ethernet |
| Approximate price | $8,000–12,000 USD |
| Notes | Double the vertical resolution of OS0-32 in the same package. Same range limitation. The 1.3 million points/sec at 10 Hz produces enormous data volumes (approximately 100+ MB/s raw). For fixed-wing use, the short range is the primary limitation. Only suitable for very low altitude (sub-30 m) passes. |

#### 1.2.8 Ouster OS1-32

| Parameter | Value |
|---|---|
| Range | 120 m (Lambertian), 80 m at 10% reflectivity |
| Points per second | 655,360 (at 10 Hz, 2048 mode) |
| Field of View | 360° x 45° (+22.5° to -22.5°) |
| Range accuracy | ±1–3 cm |
| Angular resolution | 0.18° horizontal, 1.4° vertical |
| Scan pattern | Spinning, 32 channels |
| Weight | 447 g |
| Dimensions | 73 x 73 x 74 mm |
| Power consumption | 14–20 W |
| Interface | 1 Gbps Ethernet |
| Approximate price | $4,500–7,000 USD |
| Notes | The mid-range Ouster option. 120 m range is adequate for UAV mapping at 50–80 m AGL. The 45° vertical FOV is more appropriate than the OS0's 90° for airborne use (less wasted energy pointing at the sky). Digital spinning LiDAR with built-in IMU (used for internal compensation, not navigation-grade). Solid choice if budget allows — well-characterized, widely used in research. |

#### 1.2.9 Velodyne Puck Lite (VLP-16 Lite)

| Parameter | Value |
|---|---|
| Range | 100 m |
| Points per second | 300,000 (single return), 600,000 (dual return) |
| Field of View | 360° x 30° (+15° to -15°) |
| Range accuracy | ±3 cm |
| Angular resolution | 0.1–0.4° horizontal (RPM dependent), 2° vertical |
| Scan pattern | Spinning, 16 channels |
| Weight | 590 g |
| Dimensions | 72 mm diameter x 72 mm height |
| Power consumption | 8 W |
| Supply voltage | 9–32 V DC |
| Interface | 100 Mbps Ethernet |
| Approximate price | $4,000–6,000 USD (used/refurbished) |
| Notes | The original UAV LiDAR workhorse. Lighter than standard VLP-16 (590 g vs 830 g). Low power draw (8 W) is very favorable. 16 channels with 2° vertical spacing means relatively coarse vertical resolution — but 100 m range is reliable. The spinning design is proven in thousands of UAV deployments. Now largely superseded by Ouster and Livox options but has the most mature software ecosystem. Dual return mode is valuable for vegetation penetration. Currently being phased out by Velodyne/Ouster (post-merger). |

#### 1.2.10 Cygbot CYG-D1

| Parameter | Value |
|---|---|
| Range | 15 m (indoor), 8 m (outdoor, high ambient) |
| Points per second | 23,040 (at 15 Hz frame rate) |
| Field of View | 80° x 60° (ToF camera-style) |
| Range accuracy | ±1–2 cm (close range) |
| Scan pattern | Solid-state ToF array (no scanning) |
| Weight | ~150 g |
| Dimensions | ~70 x 50 x 40 mm |
| Power consumption | 5 W |
| Interface | USB 2.0 |
| Approximate price | $200–400 USD |
| Notes | This is a time-of-flight depth camera, not a traditional LiDAR scanner. The extremely short outdoor range (8 m) makes it unsuitable for any meaningful UAV mapping. Included here for completeness. Could theoretically be used for very close-range inspection (sub-5 m) such as bridge underside inspection with a slow pass, but this is not a practical mapping sensor. Not recommended. |

#### 1.2.11 YDLiDAR G4

| Parameter | Value |
|---|---|
| Range | 16 m (indoors), 10 m (outdoors, typical) |
| Points per second | 9,000 (at 9 Hz rotation) |
| Field of View | 360° x ~0.5° (2D scanner) |
| Range accuracy | ±1–2 cm |
| Scan pattern | Spinning, single beam (2D) |
| Weight | 167 g |
| Dimensions | 56 mm diameter x 72 mm height |
| Power consumption | 2.5 W |
| Interface | UART (serial) |
| Approximate price | $100–150 USD |
| Notes | 2D LiDAR scanner only — produces a single scan plane, not a 3D point cloud. To generate 3D data from a fixed-wing, the aircraft's forward motion sweeps the scan line across the terrain (push-broom style), but with only ~9,000 pts/sec and 10 m outdoor range, the resulting point cloud is extremely sparse and short-range. Useful only as a budget altimeter or obstacle detector, not for mapping. Not recommended for survey work. |

#### 1.2.12 Benewake TF-Luna

| Parameter | Value |
|---|---|
| Range | 8 m (default), up to 12 m in favorable conditions |
| Points per second | N/A — single point measurement at 250 Hz |
| Field of View | ~2° (single beam) |
| Range accuracy | ±6 cm at 6 m |
| Scan pattern | None (single-point rangefinder) |
| Weight | 5 g |
| Dimensions | 35 x 21 x 13.5 mm |
| Power consumption | 0.35 W |
| Interface | UART, I2C |
| Approximate price | $15–25 USD |
| Notes | Single-point ToF rangefinder — not a scanner. Used as a laser altimeter in ArduPilot (RNGFND parameter class). Excellent for terrain-following altitude hold but produces zero mapping data. Can be paired with a servo-driven pan mechanism to create a crude 2D scanner, but the 250 Hz sample rate and 8 m range make this impractical. Useful as a supplementary altimeter alongside a real mapping LiDAR. |

### 1.3 Summary Comparison Table

| Sensor | Weight (g) | Range (m) @ 10% | Pts/sec (k) | FOV | Power (W) | Price (USD) | Recommended |
|---|---|---|---|---|---|---|---|
| Livox Mid-40 | 750 | 90 | 100 | 38.4° circ | 10 | $700 | Corridor only |
| Livox Mid-70 | 750 | 90 | 100 | 70.4° circ | 10 | $900 | Area mapping |
| Livox Mid-360 | 265 | 40 | 200 | 360° x 59° | 5.5 | $300 | Low-alt SLAM |
| **Livox Avia** | **498** | **190** | **240** | **70.4° circ** | **11** | **$1,400** | **Best overall** |
| Livox HAP | 400 | 150 | 450 | 120° x 25° | 9 | $500 | Wide corridor |
| Ouster OS0-32 | 447 | 35 | 655 | 360° x 90° | 17 | $5,000 | Low-alt only |
| Ouster OS0-64 | 447 | 35 | 1,310 | 360° x 90° | 17 | $10,000 | Low-alt only |
| Ouster OS1-32 | 447 | 80 | 655 | 360° x 45° | 17 | $6,000 | Good mid-range |
| Velodyne Puck Lite | 590 | ~80 | 300 | 360° x 30° | 8 | $5,000 | Proven legacy |
| Cygbot CYG-D1 | 150 | 8 | 23 | 80° x 60° | 5 | $300 | Not suitable |
| YDLiDAR G4 | 167 | 10 | 9 | 360° x 0° (2D) | 2.5 | $125 | Not suitable |
| TF-Luna | 5 | 8 | 0.25 | ~2° (1D) | 0.35 | $20 | Altimeter only |

### 1.4 Sensor Recommendations by Application

**Primary recommendation: Livox Avia.** At 498 g with 240,000 pts/sec, 190 m range at 10% reflectivity, triple-return capability, and 70.4° FOV, it offers the best combination of performance, weight, and cost for this platform. Total payload assembly (Avia + Jetson Orin Nano + RTK GPS + IMU + NVMe + mount + wiring) comes in under 1.8 kg, well within the 4 kg budget.

**Budget option: Livox Mid-360.** At 265 g and $300, it enables a sub-$1,500 total payload build. The 40 m range limitation restricts operations to low-altitude passes (20–30 m AGL), which is acceptable for forestry understory and small-area terrain mapping.

**Maximum point density: Livox HAP.** 450,000 pts/sec with 120° horizontal coverage. Best for corridor mapping where cross-track swath width matters more than vertical FOV.

**Research/flexibility: Ouster OS1-32.** 360° scanning with calibrated intensity and near-IR imagery. Best software ecosystem for SLAM research. High power draw (17 W) and cost ($6,000+) are the drawbacks.

---

## 2. Point Cloud Density Mathematics

### 2.1 Fundamental Relationships

The ground-level point density is the critical metric for all survey applications. It depends on the sensor's point rate, the aircraft's ground speed and altitude, the sensor's FOV, and the scan pattern geometry.

**Basic point density for a nadir-pointing sensor:**

```
ρ = R / (v × W)
```

Where:
- ρ = point density (points/m²)
- R = sensor point rate (points/sec)
- v = ground speed (m/s)
- W = swath width on ground (m)

**Swath width from FOV and altitude:**

```
W = 2 × h × tan(θ/2)
```

Where:
- h = altitude AGL (m)
- θ = sensor FOV (full angle)

### 2.2 Worked Examples: Livox Avia

The Livox Avia has a 70.4° circular FOV and 240,000 pts/sec (triple return). For a fixed-wing at typical survey speeds:

**At 50 m AGL, 20 m/s ground speed:**

```
W = 2 × 50 × tan(35.2°) = 2 × 50 × 0.707 = 70.7 m
ρ = 240,000 / (20 × 70.7) = 240,000 / 1,414 = 169.7 pts/m²
```

**At 80 m AGL, 25 m/s ground speed:**

```
W = 2 × 80 × tan(35.2°) = 113.1 m
ρ = 240,000 / (25 × 113.1) = 240,000 / 2,827.5 = 84.9 pts/m²
```

**At 100 m AGL, 25 m/s ground speed:**

```
W = 2 × 100 × tan(35.2°) = 141.4 m
ρ = 240,000 / (25 × 141.4) = 240,000 / 3,535 = 67.9 pts/m²
```

**At 30 m AGL, 15 m/s ground speed (slow survey):**

```
W = 2 × 30 × tan(35.2°) = 42.4 m
ρ = 240,000 / (15 × 42.4) = 240,000 / 636 = 377.4 pts/m²
```

### 2.3 Livox Non-Repetitive Pattern Consideration

Livox sensors use a Risley prism (or triple-prism) mechanism that creates a non-repetitive scan pattern. Unlike spinning LiDAR where the same angular positions are revisited every revolution, Livox patterns fill the FOV progressively. This means:

- At short integration times (0.1 s), the pattern covers only a fraction of the FOV area
- At 1 second integration, approximately 80% of the FOV is covered
- At 2+ seconds integration, coverage asymptotically approaches 100%

For a fixed-wing moving at 20 m/s, any given ground point is within the sensor's FOV for approximately:

```
t_dwell = W_along_track / v
```

Where `W_along_track` is the effective along-track footprint, which for a circular FOV equals the swath width:

```
t_dwell = 70.7 / 20 = 3.54 seconds (at 50 m AGL)
```

This is excellent — 3.5 seconds of integration means the non-repetitive pattern achieves near-complete coverage. The effective density is very close to the theoretical maximum.

At higher speeds or altitudes, dwell time decreases, but even at 25 m/s and 100 m AGL:

```
t_dwell = 141.4 / 25 = 5.66 seconds
```

The longer range (larger footprint) compensates for higher speed, maintaining long dwell times.

### 2.4 Spinning LiDAR Point Density (Ouster OS1-32)

For spinning sensors, the geometry differs. The horizontal scan is 360°, but only a portion illuminates the ground (the rest points at the sky or horizontally). For a nadir-mounted spinning sensor on a fixed-wing, the useful vertical FOV (ground-illuminating portion) is approximately:

```
θ_useful ≈ θ_vertical / 2  (for nadir mount, only the downward-facing half)
```

For OS1-32 with 45° vertical FOV, the useful cross-track coverage is approximately:

```
W = 2 × h × tan(22.5°) = 2 × 50 × 0.414 = 41.4 m (at 50 m AGL)
```

Point rate for the useful hemisphere at 10 Hz rotation, 2048 azimuth mode:

```
Useful points ≈ 655,360 × (45°/360°) = 81,920 pts/rev × 10 rev/s
But only half the vertical channels point down: ~40,960 × 10 = 409,600 useful pts/sec
```

Actually, in practice the geometry is more complex. For a horizontal aircraft, the spin axis is vertical, and channels at different elevation angles illuminate different cross-track distances. The effective ground point rate is approximately 50–60% of the total:

```
ρ = 0.55 × 655,360 / (20 × 41.4) = 360,448 / 828 = 435 pts/m² (at 50 m AGL, 20 m/s)
```

This is higher than the Avia at the same conditions, but the OS1-32's 80 m range at 10% reflectivity limits the maximum altitude more than the Avia's 190 m.

### 2.5 Swath Width and Flight Line Spacing

For area mapping, parallel flight lines must overlap to ensure complete coverage. The required overlap depends on:

1. **Navigation accuracy** — GPS drift between lines
2. **Scan pattern edge effects** — point density falls off at swath edges
3. **Classification requirements** — multiple viewing angles improve classification

Standard overlap requirements:

| Application | Minimum sidelap | Typical sidelap |
|---|---|---|
| Terrain mapping (basic) | 20% | 30% |
| Forestry (canopy penetration) | 30% | 50% |
| Corridor mapping | N/A (single strip) | N/A |
| Urban/building modeling | 30% | 40% |
| Archaeology | 40% | 60% |

**Flight line spacing calculation:**

```
S = W × (1 - overlap_fraction)
```

For Livox Avia at 50 m AGL with 30% overlap:

```
S = 70.7 × 0.7 = 49.5 m line spacing
```

**Number of flight lines for an area:**

```
N = ceil(A_width / S) + 1  (plus 1 for edge coverage)
```

For a 500 m × 500 m survey area:

```
N = ceil(500 / 49.5) + 1 = 11 + 1 = 12 lines
Total flight distance = 12 × 500 = 6,000 m
Flight time (at 20 m/s, ignoring turns) = 300 s = 5 minutes
With turns (~30 s each): 5 + 11 × 0.5 = 10.5 minutes
```

### 2.6 Point Density Requirements by Application

| Application | Minimum pts/m² | Recommended pts/m² | Achievable altitude (Avia, 20 m/s) |
|---|---|---|---|
| Topographic survey (USGS QL2) | 2 | 8 | Up to 190 m AGL |
| Topographic survey (USGS QL1) | 8 | 16 | Up to 130 m AGL |
| Topographic survey (USGS QL0) | 24 | 40+ | Up to 70 m AGL |
| Forestry canopy height model | 4 | 15 | Up to 120 m AGL |
| Individual tree detection | 15 | 40+ | Up to 60 m AGL |
| Biomass estimation | 8 | 20 | Up to 90 m AGL |
| Power line detection | 20 | 50+ | Up to 55 m AGL |
| Building roof modeling | 10 | 25 | Up to 75 m AGL |
| Archaeology under canopy | 15 | 30+ | Up to 65 m AGL |
| Flood modeling DEM | 4 | 10 | Up to 140 m AGL |
| Mining stockpile volumes | 10 | 30+ | Up to 65 m AGL |

### 2.7 Beam Divergence and Footprint Size

At range, the laser beam expands. Beam divergence determines the minimum resolvable feature size:

| Sensor | Beam divergence | Footprint at 50 m | Footprint at 100 m |
|---|---|---|---|
| Livox Avia | 0.28° × 0.03° (elliptical) | 24.4 cm × 2.6 cm | 48.9 cm × 5.2 cm |
| Ouster OS1-32 | 0.18° × ~1.4° (channel specific) | 15.7 cm | 31.4 cm |
| Velodyne Puck Lite | 0.18° (vertical emitter specific) | 15.7 cm | 31.4 cm |
| Livox Mid-360 | 0.2° | 17.5 cm | 34.9 cm |

The footprint size sets the lower bound on spatial resolution regardless of point density. Even at 1,000 pts/m², if each footprint is 25 cm across, you cannot resolve features smaller than ~25 cm.

---

## 3. SLAM and Real-Time Mapping

### 3.1 LiDAR SLAM Algorithms

SLAM (Simultaneous Localization and Mapping) is relevant for two scenarios on this platform: (1) GPS-denied or GPS-degraded environments where the LiDAR must provide position estimates, and (2) real-time motion compensation and map building for immediate situational awareness.

#### 3.1.1 LOAM (LiDAR Odometry and Mapping)

- **Reference:** Ji Zhang and Sanjiv Singh, RSS 2014
- **Architecture:** Two-module system — high-frequency odometry (10 Hz) for motion estimation using edge and planar feature extraction, and low-frequency mapping (1 Hz) for global map refinement
- **Feature extraction:** Computes local surface curvature; high-curvature points are edges, low-curvature points are planes
- **Strengths:** Low computational cost, works on single-core CPU, foundational algorithm that many successors build upon
- **Weaknesses:** No loop closure, drift accumulates over long flights, no IMU integration in original formulation, assumes structured environments (struggles over featureless terrain like water or flat desert)
- **Suitability for fixed-wing:** Moderate. The high speed (20+ m/s) and large scan areas stress the feature matching. Works best for corridor mapping over structured terrain.

#### 3.1.2 LeGO-LOAM (Lightweight and Ground-Optimized LOAM)

- **Reference:** Tixiao Shan and Brendan Englot, IROS 2018
- **Architecture:** Extends LOAM with ground segmentation, point cloud clustering, and loop closure via pose graph optimization (using GTSAM)
- **Ground segmentation:** Uses the ring structure of spinning LiDAR (assumes organized point cloud with known channel angles) to segment ground points. This is problematic for Livox sensors which produce unorganized clouds.
- **Loop closure:** Integrates ICP-based loop closure with scan context descriptors
- **Strengths:** More robust than LOAM, lower drift, ground plane constraint improves vertical accuracy
- **Weaknesses:** Tightly coupled to spinning LiDAR data format (16/32/64 channel organized clouds). Requires porting/adaptation for Livox non-repetitive patterns. Not designed for airborne use — ground segmentation assumes the sensor is near ground level.
- **Suitability for fixed-wing:** Poor without significant modification. Ground segmentation heuristics fail at altitude. The organized point cloud assumption requires adaptation for Livox.

#### 3.1.3 FAST-LIO2 (Fast LiDAR-Inertial Odometry 2)

- **Reference:** Wei Xu et al., IEEE T-RO 2022 (University of Hong Kong MARS Lab)
- **Architecture:** Tightly coupled iterated extended Kalman filter (iEKF) fusing IMU propagation with direct point-to-map registration (no feature extraction). Uses incremental kd-tree (ikd-Tree) for map management.
- **Key innovation:** Eliminates feature extraction entirely — registers raw points directly to the map using point-to-plane ICP within the iEKF update step. The ikd-Tree allows O(log n) insertion and deletion, enabling real-time map updates.
- **IMU integration:** Tightly coupled IMU preintegration provides motion prior between LiDAR frames. This is critical for fixed-wing applications where inter-frame motion is large (2 m between frames at 20 m/s and 10 Hz).
- **Computational cost:** Demonstrated real-time on ARM processors (tested on Khadas VIM3 with 4-core A73). Runs comfortably on Jetson Nano.
- **Strengths:** Extremely robust, works with any LiDAR (spinning, solid-state, Livox), handles aggressive motion, very low drift (<0.1% of travel distance in structured environments), lightweight computation
- **Weaknesses:** No loop closure (odometry-only), map size limited by available RAM (ikd-Tree grows indefinitely without pruning), no global localization
- **Suitability for fixed-wing:** Excellent. This is the recommended algorithm for this platform. Native Livox support, tight IMU coupling handles high-speed motion, and the computational efficiency allows real-time operation on Jetson Orin Nano. The lack of loop closure is mitigated by the RTK GPS providing global position — FAST-LIO2 provides the high-frequency (100+ Hz via IMU propagation) pose estimate between GPS updates.

#### 3.1.4 LIO-SAM (LiDAR Inertial Odometry via Smoothing and Mapping)

- **Reference:** Tixiao Shan et al., IROS 2020
- **Architecture:** Factor graph optimization (using GTSAM) with four types of factors: IMU preintegration factors, LiDAR odometry factors, GPS factors, and loop closure factors
- **IMU integration:** Preintegration theory provides motion prior; IMU bias is estimated online
- **GPS integration:** GPS position measurements are directly incorporated as factors in the graph — this is extremely valuable for airborne use where GPS is generally available and loop closure is rare (straight flight lines)
- **Loop closure:** Scan context descriptors + ICP verification
- **Strengths:** The factor graph formulation naturally handles heterogeneous sensor fusion. GPS integration means global position accuracy is maintained. IMU provides motion compensation. Can operate with degraded GPS (uses LiDAR odometry to bridge gaps).
- **Weaknesses:** Higher computational cost than FAST-LIO2 (factor graph optimization is more expensive than EKF). Requires organized point cloud from spinning LiDAR in the original implementation (though community forks exist for Livox). Graph grows over long flights — needs marginalization or sliding window.
- **Suitability for fixed-wing:** Good, especially when GPS factors are used. The GPS-aided mode means drift is bounded even on long flights. Community forks (e.g., LIO-SAM with Livox support, "LIO-SAM-6AXIS") adapt it for Livox sensors. The computational cost is manageable on Jetson Orin Nano. Recommended as an alternative to FAST-LIO2 when GPS integration in the SLAM loop is desired.

### 3.2 IMU Integration for Motion Compensation

Fixed-wing aircraft at 20 m/s move approximately 2 m between consecutive LiDAR frames (at 10 Hz). Within a single scan frame, the aircraft translates 0.2 m at 100 Hz point acquisition (typical for Livox accumulation period of 100 ms). This intra-frame motion causes scan distortion ("skewing") that must be corrected.

**Motion compensation pipeline:**

1. **IMU data at 200–400 Hz** provides angular rate (gyroscope) and specific force (accelerometer)
2. **IMU preintegration** between LiDAR frame timestamps computes relative rotation, velocity, and position change
3. **Per-point de-skewing:** Each point's timestamp is used to interpolate the IMU-derived pose at that instant. The point is then transformed from the sensor frame at its measurement time to the sensor frame at the frame's reference time.
4. **The de-skewed frame** is then registered to the map (or used for SLAM)

**IMU requirements:**

| Parameter | Minimum | Recommended |
|---|---|---|
| Update rate | 200 Hz | 400 Hz |
| Gyro bias stability | <10°/hr | <1°/hr |
| Accelerometer bias stability | <0.5 mg | <0.1 mg |
| Noise density (gyro) | <0.01°/s/√Hz | <0.005°/s/√Hz |
| Noise density (accel) | <100 µg/√Hz | <50 µg/√Hz |

**Recommended IMU units:**

- **VectorNav VN-100 (MEMS):** 400 Hz, gyro bias 10°/hr, 15 g, $500 — minimum viable
- **VectorNav VN-200 (MEMS + GPS):** Integrated GPS/INS, 400 Hz, $3,000 — integrated solution
- **Xsens MTi-30 (MEMS):** 400 Hz, gyro bias 10°/hr, AHRS onboard, $1,500
- **SBG Ellipse-A:** Industrial-grade MEMS AHRS, 200 Hz, gyro bias 8°/hr, $2,000
- **Pixhawk internal IMU (ICM-42688-P):** 8 kHz capable, gyro bias ~10°/hr, noise density adequate for SLAM but not survey-grade — usable as a secondary source

For survey-grade results, a dedicated external IMU is necessary. The Pixhawk's IMU can serve as a backup and for real-time SLAM, while the external IMU provides the precision needed for post-processed georeferencing.

### 3.3 Real-Time vs Post-Processing Tradeoffs

| Aspect | Real-time (onboard SLAM) | Post-processing |
|---|---|---|
| Position accuracy | 0.1–0.5 m (SLAM) | 0.02–0.05 m (PPK GPS + boresight) |
| Point cloud accuracy | 0.05–0.2 m relative | 0.02–0.05 m absolute |
| Computation | Must run on companion computer | Desktop/workstation |
| Storage | Must record raw data AND poses | Raw data only (reprocessable) |
| Latency | Immediate | Hours to days |
| Use case | Situational awareness, obstacle avoidance, coverage verification | Final deliverable, survey-grade mapping |

**Recommendation:** Always record raw sensor data (LiDAR + IMU + GPS) for post-processing. Run FAST-LIO2 in real-time for coverage verification and immediate situational awareness, but produce final deliverables through post-processing with PPK GPS corrections.

### 3.4 Companion Computer Selection

| Computer | CPU | GPU | RAM | Storage I/F | Weight | Power | Price | Assessment |
|---|---|---|---|---|---|---|---|---|
| Raspberry Pi 4 (8 GB) | 4× A72 @ 1.8 GHz | VideoCore VI (no CUDA) | 8 GB | microSD / USB 3.0 | 46 g | 5–7 W | $75 | Marginal. Can run FAST-LIO2 in degraded mode (10 Hz with frame dropping). No CUDA for GPU-accelerated processing. USB 3.0 NVMe via adapter is unreliable for sustained writes. Not recommended. |
| Raspberry Pi 5 (8 GB) | 4× A76 @ 2.4 GHz | VideoCore VII | 8 GB | PCIe 2.0 x1 (via HAT) | 47 g | 5–10 W | $80 | Better than RPi 4. Native PCIe for NVMe. Runs FAST-LIO2 at 10 Hz with Livox Avia. Still no CUDA. Viable for budget builds. |
| NVIDIA Jetson Nano (4 GB) | 4× A57 @ 1.43 GHz | 128-core Maxwell | 4 GB | microSD / USB 3.0 | 136 g (module + carrier) | 5–10 W | $149 | Runs FAST-LIO2 comfortably. CUDA available for point cloud processing. 4 GB RAM is limiting for large maps. USB 3.0 storage bottleneck. Legacy product — difficult to source. |
| **NVIDIA Jetson Orin Nano (8 GB)** | **6× A78AE @ 1.5 GHz** | **1024-core Ampere, 32 Tensor cores** | **8 GB** | **PCIe Gen3, NVMe native** | **~200 g (with carrier board)** | **7–15 W** | **$249** | **Recommended.** Substantial CPU and GPU upgrade. Native NVMe support solves the storage write speed problem. 8 GB RAM is adequate for SLAM with map pruning. 40 TOPS AI performance enables potential real-time classification. Runs FAST-LIO2 and LIO-SAM simultaneously if needed. |
| NVIDIA Jetson Orin NX (16 GB) | 8× A78AE @ 2.0 GHz | 1024-core Ampere, 32 Tensor cores | 16 GB | PCIe Gen4, NVMe native | ~200 g | 10–25 W | $399 | Overkill for SLAM but useful if real-time classification or mesh generation is required. 16 GB RAM allows larger maps. Higher power draw. Consider if the mission profile includes real-time DEM generation. |

**Recommended configuration: Jetson Orin Nano (8 GB)** with a compact carrier board (e.g., Seeed Studio reComputer carrier at ~100 g, or a custom carrier at 50–80 g).

### 3.5 Processing Pipeline

```
[LiDAR sensor] → UDP/Ethernet → [Companion computer]
[IMU] → UART/SPI → [Companion computer]
[GPS receiver] → UART → [Companion computer]
[ArduPilot/Pixhawk] → MAVLink/UART → [Companion computer]

Real-time pipeline (onboard):
1. Raw point cloud frames (10 Hz) + IMU (400 Hz) + GPS (10 Hz)
2. Per-point timestamp synchronization (PTP or hardware trigger)
3. IMU preintegration for motion model
4. Per-point de-skewing using interpolated IMU poses
5. FAST-LIO2: de-skewed frame → iEKF update → pose estimate + map update
6. Pose output at IMU rate (400 Hz) via ROS topic
7. Map visualization (optional, downsampled for bandwidth)
8. All raw data simultaneously logged to NVMe SSD

Post-processing pipeline (ground station):
1. PPK: raw GPS observables + base station data → cm-level trajectory (RTKLIB)
2. INS/GPS fusion: PPK positions + raw IMU → smoothed trajectory (forward-backward Kalman)
3. Boresight calibration application: trajectory + lever arm + rotation offsets
4. Point cloud georeferencing: each raw point transformed to global coordinates using the
   calibrated trajectory + sensor extrinsics
5. Strip adjustment: minimize discrepancy between overlapping flight lines
6. Ground classification: progressive morphological filter, cloth simulation filter (CSF),
   or deep learning classifier
7. Product generation: DEM, DSM, DTM, contours, intensity raster
8. Quality assessment: comparison against ground control points
```

---

## 4. Georeferencing and Accuracy

### 4.1 Direct Georeferencing

Direct georeferencing computes each point's global coordinates using:

```
P_global = P_GPS(t) + R_body_to_global(t) × (L_lever + R_sensor_to_body × P_sensor)
```

Where:
- `P_GPS(t)` = GPS antenna position in global frame at time t
- `R_body_to_global(t)` = rotation matrix from body (IMU) frame to global frame (from INS)
- `L_lever` = lever arm vector from GPS antenna to IMU center (measured, constant)
- `R_sensor_to_body` = rotation matrix from LiDAR sensor frame to body (IMU) frame (boresight)
- `P_sensor` = point coordinates in sensor frame (raw LiDAR measurement)

Every term in this equation introduces error. The total error budget is approximately:

```
σ_total² = σ_GPS² + σ_INS_position² + σ_INS_attitude² × h² + σ_boresight² × h² + σ_LiDAR²
```

Where h is the range (approximately AGL altitude for nadir points).

### 4.2 GPS/GNSS Options

#### 4.2.1 Single-Frequency RTK

- **Receiver:** u-blox F9P (L1/L2 dual-frequency, despite the section name)
- **Weight:** 15–25 g (module + antenna)
- **Power:** 0.5–1 W
- **Real-time accuracy:** 1–2 cm horizontal, 2–3 cm vertical (with RTK fix via base station radio link)
- **Limitation:** Requires continuous radio link to base station (or NTRIP via cellular). Radio link may be unreliable from a fixed-wing at distance.
- **Price:** $200 (F9P module + antenna)

#### 4.2.2 PPK (Post-Processed Kinematic)

- **Receiver:** Same u-blox F9P, logging raw observables (RAWX messages) at 5–10 Hz
- **Post-processing:** RTKLIB or Emlid Studio, using RINEX data from a nearby base station (own base, or CORS network)
- **Accuracy:** 1–2 cm horizontal, 2–3 cm vertical (same as RTK, but achieved in post-processing without real-time radio link)
- **Baseline constraint:** Accuracy degrades above ~10 km baseline to base station. <5 km is preferred.
- **Recommendation:** PPK is strongly preferred over real-time RTK for fixed-wing mapping because it eliminates the radio link requirement and allows reprocessing. Log raw GNSS observables alongside LiDAR data.

#### 4.2.3 PPP (Precise Point Positioning)

- **No base station required** — uses precise satellite clock and orbit products
- **Convergence time:** 20–30 minutes to reach cm-level (problematic for short flights)
- **Accuracy (converged):** 3–5 cm horizontal, 5–8 cm vertical
- **Useful as a backup** when no base station or CORS network is available

### 4.3 Boresight Calibration

Boresight calibration determines the rotation matrix `R_sensor_to_body` and the lever arm vector `L_lever` between the LiDAR sensor frame and the IMU/navigation frame. Errors in boresight propagate linearly with range:

```
Positional error from 0.1° boresight error at range h:
ε = h × tan(0.1°) = h × 0.00175
At 50 m: ε = 8.7 cm
At 100 m: ε = 17.5 cm
```

This makes boresight calibration the single most critical accuracy parameter after GPS quality.

**Calibration procedure:**

1. Fly over a calibration site with clearly defined geometric features (building edges, road markings, or dedicated targets)
2. Fly at least 4 lines: 2 opposing directions + 2 cross-lines at 90°
3. Fly at 2 different altitudes (e.g., 40 m and 80 m) to separate boresight angles from lever arm
4. In post-processing, adjust the three boresight angles (roll, pitch, heading offsets) and three lever arm components to minimize discrepancy between overlapping strips and known control points
5. Software: typically done in the LiDAR processing suite (e.g., LiDAR360, DJI Terra, or custom scripts using PDAL + optimization)

**Expected boresight accuracy:** 0.01–0.05° after proper calibration, contributing 1–4 cm error at 50 m range.

**Lever arm measurement:** Physically measure the 3D vector from GPS antenna phase center to IMU center and from IMU center to LiDAR optical center. Accuracy of 1–2 mm is achievable with careful measurement. The lever arm must be measured in the IMU body frame (not the aircraft frame if they differ).

### 4.4 Expected Absolute Accuracy

Combining all error sources for a well-calibrated system:

| Component | Horizontal σ (cm) | Vertical σ (cm) |
|---|---|---|
| PPK GPS | 1.5 | 2.5 |
| INS attitude (MEMS, 0.05° RMS) | 4.4 at 50m AGL | 1.0 |
| Boresight calibration (0.02°) | 1.7 at 50m AGL | 0.5 |
| Lever arm (2 mm accuracy) | 0.2 | 0.2 |
| LiDAR ranging (2 cm) | 0.5 | 2.0 |
| **RSS total at 50 m AGL** | **5.1** | **3.4** |
| **RSS total at 80 m AGL** | **7.8** | **4.2** |
| **RSS total at 100 m AGL** | **9.6** | **4.8** |

These are 1-sigma (68% confidence) values. For 95% confidence, multiply by 1.96.

**At 50 m AGL, expected absolute accuracy is approximately 5 cm horizontal, 3.5 cm vertical (1σ).** This meets or exceeds ASPRS accuracy class requirements for 10 cm vertical accuracy surveys.

With a navigation-grade IMU (fiber optic gyro, ~0.01°/hr bias stability, $15,000+), the attitude contribution shrinks dramatically, but this exceeds the budget and weight constraints of this platform.

### 4.5 Ground Control Points (GCPs)

GCPs provide independent accuracy verification and can be used for datum transformation or residual error correction.

**When GCPs are required:**
- When PPK baseline exceeds 15 km
- When no CORS station is available for PPK processing
- For projects requiring certified accuracy (e.g., legal surveys)
- For boresight calibration flights

**GCP specifications:**
- Minimum 3 GCPs for a basic check, 5+ for statistical validation
- GCPs should be outside the flight area perimeter (for block adjustment)
- Surveyed to 1–2 cm accuracy using static GNSS or total station
- Physical targets: 30–60 cm white or reflective panels (LiDAR reflective targets for easy identification in point cloud)
- LiDAR GCPs can be flat elevated surfaces (e.g., building roofs with known survey marks) to enable both horizontal and vertical checking

**Without GCPs:** Absolute accuracy depends entirely on the PPK/INS solution. For most practical applications of this platform (forestry, terrain mapping, volume measurement), the 5–10 cm accuracy from direct georeferencing without GCPs is sufficient.

---

## 5. Data Management

### 5.1 Data Rates

| Sensor | Points/sec | Bytes per point (raw) | Raw data rate | With overhead (Ethernet headers, timestamps) |
|---|---|---|---|---|
| Livox Avia | 240,000 | 18 bytes (XYZ float16 + intensity + timestamp) | 4.3 MB/s | ~6 MB/s |
| Livox Mid-360 | 200,000 | 18 bytes | 3.6 MB/s | ~5 MB/s |
| Livox HAP | 450,000 | 18 bytes | 8.1 MB/s | ~11 MB/s |
| Ouster OS1-32 | 655,360 | 12–24 bytes (configurable) | 7.9–15.7 MB/s | ~12–20 MB/s |
| Velodyne Puck Lite | 300,000 | 7 bytes (in packet format) | 2.1 MB/s | ~3 MB/s (with packet headers) |

**Additional data streams:**

| Source | Data rate |
|---|---|
| IMU (400 Hz, 6-axis float32) | 9.6 KB/s |
| GPS raw observables (10 Hz) | ~5 KB/s |
| SLAM output poses (100 Hz) | 4.8 KB/s |
| ArduPilot MAVLink telemetry | ~2 KB/s |
| **Total ancillary** | **~22 KB/s (negligible)** |

### 5.2 Storage Requirements

For the recommended Livox Avia at ~6 MB/s total:

| Mission duration | Raw data | With 1.5× safety margin |
|---|---|---|
| 15 minutes | 5.4 GB | 8.1 GB |
| 30 minutes | 10.8 GB | 16.2 GB |
| 1 hour | 21.6 GB | 32.4 GB |
| 2 hours | 43.2 GB | 64.8 GB |

For Ouster OS1-32 at ~15 MB/s:

| Mission duration | Raw data | With 1.5× safety margin |
|---|---|---|
| 30 minutes | 27 GB | 40.5 GB |
| 1 hour | 54 GB | 81 GB |
| 2 hours | 108 GB | 162 GB |

### 5.3 NVMe SSD Requirements

The sustained sequential write speed must exceed the peak data rate with margin for filesystem overhead, SLAM computation spikes, and buffer management:

**Minimum sustained write speed:** 2× peak data rate = 12 MB/s for Avia, 40 MB/s for OS1-32. Even the slowest NVMe SSDs sustain 500+ MB/s sequential writes, so write speed is not a bottleneck.

**Key concern: Random write performance during buffer flushes.** When the ROS bag writer (or custom logger) flushes buffers, random 4K writes occur. Even budget NVMe SSDs handle 50+ MB/s random writes, which is far above the requirement.

**Recommended storage hardware:**

| Option | Capacity | Weight | Interface | Notes |
|---|---|---|---|---|
| Samsung 980 (M.2 2280) | 250 GB / 500 GB / 1 TB | 8 g | PCIe Gen3 x4 | Standard desktop NVMe. Requires M.2 slot on carrier board. |
| WD SN740 (M.2 2230) | 256 GB / 512 GB / 1 TB / 2 TB | 2.5 g | PCIe Gen4 x4 | Shorter form factor (2230) fits compact carrier boards. Steam Deck SSD. |
| Samsung PM991a (M.2 2230) | 256 GB / 512 GB | 2.5 g | PCIe Gen3 x4 | OEM drive, widely available. |

**Recommendation:** 512 GB WD SN740 (M.2 2230). At 2.5 g, it adds negligible weight. 512 GB supports over 20 hours of Livox Avia recording — far more than any single flight. The 2230 form factor is compatible with the Jetson Orin Nano carrier boards.

### 5.4 Point Cloud File Formats

| Format | Extension | Compression | Metadata | Typical use | Software support |
|---|---|---|---|---|---|
| LAS 1.4 | .las | None | Extensive (CRS, classification, GPS time, return number, intensity, color) | Industry standard for airborne LiDAR | Universal |
| LAZ | .laz | Lossless (typically 7–15× compression vs LAS) | Same as LAS | Archival and distribution | LAStools, PDAL, most GIS |
| PLY | .ply | Optional (binary packing) | Minimal (vertex properties only) | Research, 3D visualization | CloudCompare, MeshLab, Open3D |
| PCD | .pcd | Optional | Minimal | ROS/PCL ecosystem | PCL, ROS, Open3D |
| E57 | .e57 | Lossless | Extensive (images, structured scans) | Terrestrial laser scanning, BIM | Most commercial software |
| ROS bag | .bag / .db3 | None (raw message serialization) | ROS message metadata | Raw recording during flight | ROS/ROS2 |
| Custom binary | .bin | None | Custom header | Livox/Ouster native recording | Vendor tools |

**Recommended workflow:**
1. Record during flight as ROS2 bag (.db3) — contains all raw sensor messages with precise timestamps
2. Convert ROS bag to LAS 1.4 during post-processing (after georeferencing)
3. Archive as LAZ for 7–15× size reduction
4. Export PLY/PCD for specific processing tools as needed

### 5.5 Post-Processing Software

#### 5.5.1 Open Source

**CloudCompare:**
- Interactive 3D point cloud viewer and editor
- Supports LAS, LAZ, PLY, PCD, E57, ASCII, and dozens more
- Manual and semi-automatic classification, segmentation, mesh generation
- ICP registration for strip alignment
- Volume computation (2.5D grid and convex hull)
- Cross-section extraction
- Rasterization (point cloud to DEM/DSM GeoTIFF)
- Runs on Windows, macOS, Linux
- Limitation: single-threaded for many operations, struggles with >500 M points

**PDAL (Point Data Abstraction Library):**
- Command-line and pipeline-based point cloud processing
- Readers/writers for all major formats
- Filters: ground classification (SMRF, PMF), noise removal, decimation, colorization, height above ground, reprojection
- Pipeline JSON/YAML allows reproducible, scriptable workflows
- Python bindings for custom processing
- Example pipeline for DEM generation:
  ```json
  {
    "pipeline": [
      {"type": "readers.las", "filename": "input.laz"},
      {"type": "filters.smrf"},
      {"type": "filters.range", "limits": "Classification[2:2]"},
      {"type": "writers.gdal", "filename": "dem.tif", "resolution": 0.5, "output_type": "idw"}
    ]
  }
  ```

**LAStools:**
- Suite of command-line tools (partially open source; some tools require license)
- lasground, lasclassify, las2dem, lasgrid, lasmerge, lassort, etc.
- Extremely fast and memory-efficient
- Industry-standard ground classification (lasground_new)
- The most performance-optimized point cloud tools available
- License: open source for laszip, lasinfo, lasmerge; licensed for lasground, las2dem, etc. ($2,000–5,000 for commercial use)

**RTKLIB:**
- Open-source GNSS processing suite
- PPK processing: rtkpost (GUI) or rnx2rtkp (CLI)
- Reads RINEX observation files and produces kinematic solutions
- Outputs position + velocity + clock at each epoch
- Critical for the PPK workflow

#### 5.5.2 Commercial

| Software | Purpose | Price | Notes |
|---|---|---|---|
| LiDAR360 (GreenValley) | Full LiDAR processing suite | $5,000–15,000/yr | Strip adjustment, boresight calibration, classification, forestry tools |
| Terrasolid (TerraScan/TerraMatch) | Gold standard for airborne LiDAR | $10,000+ | Used by professional survey firms, runs inside MicroStation |
| DJI Terra | DJI ecosystem LiDAR processing | $2,500–5,000 | Works with Livox sensors (DJI subsidiary) |
| Pix4Dmatic | Photogrammetry + LiDAR fusion | $3,500/yr | Newer entrant, good for combined camera + LiDAR |
| Global Mapper | GIS + LiDAR | $500–900/yr | Excellent for visualization and basic processing |

---

## 6. Specific Applications

### 6.1 Terrain Mapping and DEM Generation

**Objective:** Generate a bare-earth Digital Elevation Model (DEM) by classifying and removing above-ground objects (vegetation, buildings, vehicles).

**Flight parameters (Livox Avia):**
- Altitude: 50–80 m AGL
- Speed: 18–22 m/s
- Sidelap: 30%
- Expected ground point density: 20–50 pts/m² (before ground classification)
- After ground classification: 5–20 pts/m² ground points (terrain-dependent)

**Processing pipeline:**
1. Georeference raw point cloud (PPK + INS + boresight)
2. Strip adjustment to minimize inter-strip discrepancies
3. Noise filtering (statistical outlier removal)
4. Ground classification using progressive morphological filter (SMRF in PDAL) or cloth simulation filter (CSF in CloudCompare)
5. Interpolate ground points to regular grid (IDW, TIN, or kriging)
6. Output: GeoTIFF DEM at 0.25–1.0 m resolution

**Expected DEM accuracy:** 5–10 cm vertical RMSE in open terrain, 10–20 cm in vegetated areas (dependent on vegetation density and penetration).

**Contour generation:** From DEM, contour intervals of 0.25 m are achievable in open terrain; 0.5–1.0 m in forested areas.

### 6.2 Forestry

**Applications:**

**Canopy Height Model (CHM):**
- CHM = DSM - DEM (first return surface minus bare earth)
- Resolution: 0.5–1.0 m
- Accuracy: ±0.5 m for canopy height
- Requires: adequate ground returns through canopy gaps (Livox Avia triple return is valuable here)

**Individual Tree Detection:**
- Requires 15+ pts/m² on canopy
- Algorithms: local maxima filtering on CHM, watershed segmentation, deep learning (PointNet++, RandLA-Net)
- Accuracy: 70–95% detection rate depending on forest structure (higher in plantations, lower in dense natural forest)
- Fly at 30–50 m AGL for maximum canopy detail

**Biomass Estimation:**
- Allometric models relate tree height and crown diameter to above-ground biomass (AGB)
- LiDAR metrics: mean height, height percentiles (P50, P75, P95), canopy cover fraction, gap fraction
- Area-based approach: compute metrics in 20×20 m grid cells, calibrate against field plots
- Expected accuracy: R² > 0.7 for AGB prediction in most forest types

**Timber Volume:**
- Requires individual tree segmentation + species classification (often from co-registered camera imagery)
- Volume tables or taper models applied per tree
- Accuracy: ±15–25% per tree, ±5–10% at stand level

**Flight planning for forestry:**
- Fly at 40–60 m AGL for balance between penetration and coverage
- Multiple passes at different times of day (morning/evening for lower sun angle reducing ambient noise)
- Leaf-off season flights provide dramatically better ground returns in deciduous forests
- 50% sidelap recommended to maximize multi-angle canopy penetration

### 6.3 Corridor Mapping

**Applications:** Power line inspection, road/highway survey, railway monitoring, pipeline right-of-way.

**Flight planning:**
- Single or double flight line along the corridor
- Altitude: 40–60 m AGL (power lines), 50–80 m AGL (roads)
- Speed: 15–25 m/s
- Livox HAP (120° horizontal FOV) is particularly effective here — provides 80–140 m swath width at 40–60 m AGL

**Power line specific:**
- Wire detection requires 50+ pts/m² on conductors — achieved at 40 m AGL with Avia
- Catenary modeling: fit catenary curves to classified wire points
- Clearance analysis: measure wire-to-ground, wire-to-vegetation distances
- Pylon/tower extraction: classify returns on structures, fit geometric primitives
- Temperature-normalized sag calculation using survey time ambient temperature

**Road survey:**
- Cross-section extraction every 0.5–5 m along centerline
- Surface roughness analysis (IRI proxy from LiDAR)
- Drainage analysis: slope and crown detection
- Sign and marking inventory (from intensity returns)

### 6.4 Archaeology

**Objective:** Detect anthropogenic features (walls, terraces, mounds, ditches, roads) beneath vegetation canopy.

**Why LiDAR:** The ability to penetrate forest canopy and produce a bare-earth model reveals subtle topographic features invisible to cameras, radar, or even ground survey in dense vegetation.

**Flight parameters:**
- Altitude: 30–50 m AGL (maximize ground penetration)
- Speed: 12–18 m/s (lower speed = higher density)
- Sidelap: 50–60% (multiple viewing angles improve ground classification under canopy)
- Target: 25+ ground pts/m²

**Processing for archaeology:**
- Ground classification with aggressive settings (keep subtle terrain features that standard forestry ground filters might smooth away)
- Multiple ground classification passes with varying parameters, manual editing of results
- DEM at 0.25 m resolution (or finer)
- Visualization techniques: hillshade (multi-directional), slope, sky-view factor (SVF), local relief model (LRM), positive/negative openness
- SVF and LRM are particularly effective for revealing subtle archaeological features

**Notable capabilities:**
- Detection of features as subtle as 10–20 cm elevation change over 2–5 m horizontal distance
- Mapping under triple-canopy tropical forest (demonstrated in Maya archaeology in Guatemala and Mesoamerica)
- The Livox Avia triple return mode is essential for maximizing ground return percentage in dense canopy

### 6.5 Mining: Stockpile Volume Measurement

**Objective:** Compute volume of material stockpiles (gravel, ore, coal, etc.) with survey-grade accuracy.

**Flight parameters:**
- Altitude: 30–50 m AGL
- Speed: 15 m/s
- Single or double pass per stockpile (small area)
- Target: 50+ pts/m² for detailed surface modeling

**Volume computation methods:**
1. **2.5D grid method:** Rasterize point cloud to grid, compute volume between surface and reference plane (pit floor or geoid)
2. **TIN method:** Triangulate surface points, compute volume of prisms between TIN and base plane
3. **Cross-section method:** Extract parallel cross-sections, compute area of each, integrate along stockpile axis

**Expected accuracy:**
- For a 10,000 m³ stockpile: ±1–2% volume accuracy (±100–200 m³)
- Limiting factors: edge definition (where does the pile end?), surface roughness, reference surface definition
- LiDAR advantage over photogrammetry: works on textureless surfaces (uniform material color), works in shadow/overcast, faster processing

**Repeat surveys:** Monthly or weekly flyovers with identical flight plans enable change detection — volume added/removed between surveys. Point cloud differencing (M3C2 algorithm in CloudCompare) provides per-point distance measurements between surveys.

### 6.6 Flood Modelling

**Objective:** Generate high-resolution terrain models for hydrological simulation (flood extent, depth, flow routing).

**Requirements:**
- Bare-earth DEM at 0.5–1.0 m resolution
- Vertical accuracy ±10 cm or better (RMSE)
- Complete coverage of floodplain, channels, levees, bridges, culverts
- Hydro-enforcement: ensure DEM respects drainage connectivity (remove bridges over waterways, enforce channel connectivity)

**Flight parameters:**
- Altitude: 50–80 m AGL
- Sidelap: 30–40%
- Ensure coverage extends well beyond expected flood extent (inundation boundaries are sensitive to terrain at floodplain margins)

**LiDAR-specific considerations for hydrology:**
- LiDAR does not penetrate water — water surface returns are unreliable (specular reflection, absorption). Bathymetric data must come from other sources or green-wavelength (532 nm) bathymetric LiDAR (not applicable to sensors in this spec).
- Bridge decks appear as ground in the point cloud — must be classified and removed, then channel bed interpolated beneath
- Levees and embankments must be captured with high point density — a narrow 1 m levee crest requires 4+ points across its width to accurately model the crown elevation
- Culverts are invisible to LiDAR — must be manually encoded in the DEM or obtained from asset databases

**Hydrological software integration:**
- Export DEM as GeoTIFF, import to HEC-RAS (1D/2D), TUFLOW, MIKE FLOOD, or Flood Modeller
- LiDAR-derived DEMs at 1 m resolution have been shown to reduce flood extent prediction error by 30–50% compared to 5 m photogrammetric DEMs

---

## 7. Integration with the Platform

### 7.1 Mechanical Mounting

**Payload bay constraints:** 200 × 300 × 150 mm (W × L × H). All components must fit within this volume or be distributed across available mounting points.

**Vibration isolation:**
- Fixed-wing vibration sources: engine (IC or electric motor), propeller harmonics, airframe buffeting
- LiDAR sensors are generally vibration-tolerant (solid-state types more than spinning types)
- Spinning LiDAR (Ouster, Velodyne): the spinning mechanism itself is precision-balanced; external vibration can induce bearing wear and measurement noise. Mount on vibration isolators.
- Solid-state (Livox): no moving parts exposed to damage, but vibration-induced motion corrupts the point cloud if not compensated by IMU. Mount rigidly to the IMU bracket (not isolated) so that IMU and LiDAR experience identical motion.

**Critical mounting principle:** The LiDAR sensor and the IMU must be rigidly coupled. Any relative motion between them cannot be compensated and directly corrupts the point cloud. Mount both on a single machined aluminum plate (6061-T6, 3–4 mm thick), which is then mounted to the airframe via vibration isolators (if needed for airframe-induced vibration).

**Recommended mounting arrangement (top-down view of 200×300 mm bay):**

```
+--------------------------------------------------+
|                                                  |
|  [GPS antenna above fuselage, cable down]        |
|                                                  |
|  +----------+    +----------+    +--------+      |
|  | Livox    |    | Jetson   |    | NVMe   |      |
|  | Avia     |    | Orin     |    | SSD    |      |
|  | 107x80   |    | Nano     |    | (on    |      |
|  | mm       |    | carrier  |    | carrier|      |
|  +----------+    | 100x80   |    | board) |      |
|                  | mm       |    +--------+      |
|  +----------+    +----------+                    |
|  | IMU      |                                    |
|  | VN-100   |    +----------+                    |
|  | 36x33    |    | F9P GPS  |                    |
|  | mm       |    | module   |                    |
|  +----------+    +----------+                    |
|                                                  |
+--------------------------------------------------+
       (nadir opening below for LiDAR FOV)
```

The LiDAR must have an unobstructed nadir view. A cutout in the fuselage belly provides the FOV window. For the Avia's 70.4° circular FOV at a setback of ~20 mm from the skin, the opening must be at least:

```
Opening diameter = 2 × 20 × tan(35.2°) + sensor_aperture = 2 × 20 × 0.707 + 50 ≈ 78 mm
```

A 100 mm circular or 100×100 mm square opening provides margin. The opening should be covered with an optically transparent window (polycarbonate, anti-reflection coated) or left open (with appropriate aerodynamic fairing to prevent turbulent flow into the bay).

### 7.2 Power Budget

**Available power:** Typical fixed-wing UAV with ArduPilot carries a 4S–6S LiPo (14.8–22.2 V). A dedicated payload battery (4S, 5000 mAh = 74 Wh) can power the entire LiDAR payload for extended missions.

| Component | Voltage | Power (W) | Current from 14.8V bus |
|---|---|---|---|
| Livox Avia | 9–27 V (direct) | 11 | 0.74 A |
| Jetson Orin Nano | 5V via regulator | 15 (peak) | 1.01 A |
| u-blox F9P GPS | 3.3V via regulator | 0.5 | 0.03 A |
| VectorNav VN-100 IMU | 3.3–5V | 0.5 | 0.03 A |
| NVMe SSD | 3.3V (from Jetson) | 3 (peak) | (included in Jetson) |
| Ethernet switch/cable losses | — | 1 | 0.07 A |
| Voltage regulators (efficiency loss ~15%) | — | 4.7 | 0.32 A |
| **Total** | | **~35.7 W peak** | **2.41 A** |

**Endurance on dedicated 4S 5000 mAh battery:**

```
Energy = 14.8 V × 5.0 Ah = 74 Wh
Endurance = 74 / 35.7 = 2.07 hours
```

With 80% usable capacity (LiPo safe discharge): ~1.66 hours. This exceeds typical fixed-wing endurance (30–90 minutes depending on aircraft).

**Recommendation:** Use a separate 4S 2200–3000 mAh LiPo (44–60 g per 1000 mAh) dedicated to the payload. A 3000 mAh pack (180 g, 44.4 Wh) provides ~1 hour of payload operation, which matches typical aircraft endurance.

**Power distribution:**
- BEC/regulator: 14.8 V → 5 V, 5 A (for Jetson Orin Nano) — use a high-efficiency synchronous buck converter (e.g., Pololu D36V28F5, 93% efficiency)
- Livox Avia accepts 9–27 V directly — connect to the 14.8 V bus through a filtered input (LC filter for motor noise suppression)
- GPS and IMU powered from Jetson's 3.3V/5V rails

### 7.3 GPS/IMU Synchronization with ArduPilot

**Time synchronization is critical.** All data streams (LiDAR, IMU, GPS) must share a common time base for accurate georeferencing. A 1 ms timing error at 20 m/s ground speed produces 2 cm positional error.

**Synchronization methods:**

1. **PPS (Pulse Per Second) from GPS:** The u-blox F9P outputs a hardware PPS signal (rising edge synchronized to GPS time within ±30 ns). This PPS is connected to:
   - The Livox Avia (has a dedicated sync/PPS input pin) for timestamping point cloud frames
   - The companion computer (GPIO interrupt) for correlating system clock to GPS time
   - The IMU (if it has a sync input) for correlating IMU timestamps

2. **IEEE 1588 PTP (Precision Time Protocol):** Ouster sensors support PTP for network-based time synchronization. If using an Ouster sensor, the Jetson runs a PTP master, and the LiDAR synchronizes its clock via Ethernet. Accuracy: <1 µs.

3. **Hardware trigger line:** Some configurations use a shared trigger line where the GPS PPS triggers simultaneous capture across all sensors. This is the most reliable method.

**ArduPilot integration:**
- ArduPilot on the Pixhawk has its own time reference (GPS-disciplined system clock)
- The companion computer communicates with ArduPilot via MAVLink (UART or USB) using the MAVROS or pymavlink libraries
- ArduPilot provides: aircraft attitude, GPS position, airspeed, altitude, waypoint progress
- The companion computer can send MAVLink `CAMERA_TRIGGER` or custom messages to log events
- For survey-grade work, ArduPilot's GPS/IMU data is used for flight management only — the payload's independent GPS and IMU provide the mapping-grade trajectory

**ArduPilot survey mission planning:**
- Use ArduPilot's `SURVEY` or `DO_SET_CAM_TRIGG_DIST` mission items for regular triggering
- For LiDAR (continuous scanning, not frame-based), the survey grid is defined as a series of waypoints with appropriate line spacing
- ArduPilot's `NAV_WAYPOINT` items define the flight lines; `DO_CHANGE_SPEED` sets the survey speed
- Mission Planner or QGroundControl have built-in survey grid generators

### 7.4 System Architecture Diagram

```
                    +-------------------+
                    |   GPS Antenna     |
                    |  (L1/L2, patch)   |
                    +--------+----------+
                             |
                    +--------+----------+
                    |   u-blox F9P      |
                    |   (PPK logging)   |
                    +--------+----------+
                             | UART (NMEA + RAWX)
                             | PPS (GPIO)
+---------------+   +--------+----------+   +----------------+
|   Livox Avia  +---+  Jetson Orin Nano  +---+ ArduPilot      |
|   (Ethernet)  |   |                    |   | Pixhawk        |
+-------+-------+   |  - ROS2 Humble    |   | (MAVLink/UART) |
        |            |  - FAST-LIO2      |   +----------------+
        |            |  - Data logger    |
+-------+-------+   |  - Mission mgmt   |   +----------------+
|   Livox Avia  |   |                    +---+ NVMe SSD       |
|   PPS input   +---+  GPIO (PPS in)    |   | (M.2 2230)     |
+---------------+   +--------+----------+   +----------------+
                             |
                    +--------+----------+
                    |  VectorNav VN-100  |
                    |  IMU (UART/SPI)    |
                    +-------------------+

Power distribution:
    [4S LiPo] → [LC filter] → Livox Avia (14.8V direct)
    [4S LiPo] → [5V Buck regulator] → Jetson Orin Nano
    Jetson → 3.3V/5V rails → GPS module, IMU
```

### 7.5 Weight Budget

| Component | Weight (g) | Notes |
|---|---|---|
| Livox Avia sensor | 498 | Including cable |
| Jetson Orin Nano (module) | 60 | SoM only |
| Carrier board (compact) | 80–120 | Seeed Studio or custom |
| NVMe SSD (M.2 2230, 512 GB) | 2.5 | WD SN740 |
| u-blox F9P module | 5 | Module only |
| L1/L2 GNSS antenna (patch) | 30–50 | Tallysman TW4721 or similar |
| VectorNav VN-100 IMU | 15 | With connector |
| Mounting plate (aluminum, 3 mm) | 80–120 | 6061-T6, machined |
| Vibration isolators (4×) | 20 | Silicone or wire rope |
| Wiring harness | 40–60 | Ethernet, power, UART cables |
| Voltage regulator (5V buck) | 15 | Pololu D36V28F5 or similar |
| LC filter for LiDAR power | 10 | Inductor + capacitor |
| Payload battery (4S 2200 mAh) | 200 | If separate from main battery |
| Miscellaneous (connectors, standoffs, thermal pads) | 30–50 | |
| **Total (with dedicated battery)** | **1,085–1,220 g** | |
| **Total (shared power from main battery)** | **885–1,020 g** | |

**Margin against 4 kg payload limit:** The complete LiDAR payload assembly at ~1.0–1.2 kg leaves 2.8–3.0 kg of margin. This margin can accommodate:
- A heavier sensor (e.g., Ouster OS1-32 at 447 g instead of Avia at 498 g — similar)
- Additional sensors (RGB camera for colorized point clouds: ~50–150 g)
- Larger battery for extended missions
- Structural reinforcement for the payload bay

The platform's 4 kg payload capacity is generous for a LiDAR mapping payload. Even with a dual-sensor configuration (LiDAR + camera + heavier compute), the total would remain under 2 kg.

---

## Appendix A: Quick-Start Configuration Recommendations

### Budget Build (~$1,500 total payload hardware)

| Component | Cost |
|---|---|
| Livox Mid-360 | $300 |
| Raspberry Pi 5 (8 GB) + NVMe HAT | $110 |
| 256 GB NVMe SSD | $30 |
| u-blox F9P (SparkFun GPS-RTK board) | $220 |
| L1/L2 antenna | $50 |
| ICM-42688 IMU breakout (or use Pixhawk IMU data) | $30 |
| Mounting hardware, wiring, regulators | $100 |
| **Total** | **~$840** |

Limitations: 40 m max range, marginal processing power, no dedicated survey-grade IMU. Suitable for low-altitude terrain mapping, research, and proof-of-concept.

### Professional Build (~$4,000 total payload hardware)

| Component | Cost |
|---|---|
| Livox Avia | $1,400 |
| Jetson Orin Nano (8 GB) + carrier board | $350 |
| 512 GB NVMe SSD | $50 |
| u-blox F9P + antenna | $270 |
| VectorNav VN-100 IMU | $500 |
| Mounting plate (custom machined) | $150 |
| Wiring, regulators, connectors | $150 |
| **Total** | **~$2,870** |

This configuration delivers survey-grade performance: 5 cm horizontal, 3.5 cm vertical accuracy, 240,000 pts/sec, 190 m range, real-time SLAM capability, and all for under 1.2 kg total weight.

### High-End Research Build (~$10,000+)

| Component | Cost |
|---|---|
| Ouster OS1-32 | $6,000 |
| Jetson Orin NX (16 GB) + carrier | $500 |
| 1 TB NVMe SSD | $80 |
| u-blox F9P + antenna | $270 |
| SBG Ellipse-A AHRS/IMU | $2,000 |
| Mounting, wiring, thermal management | $300 |
| **Total** | **~$9,150** |

360° scanning, maximum point density, calibrated intensity and NIR imagery, navigation-grade AHRS. Suitable for research in SLAM, autonomous navigation, and high-density survey applications below 60 m AGL.

---

## Appendix B: Software Stack Summary

**Onboard (Jetson Orin Nano):**
- Ubuntu 22.04 (JetPack 6.x)
- ROS2 Humble
- Livox SDK2 / Livox ROS2 driver
- FAST-LIO2 (ROS2 port)
- rosbag2 for data recording
- MAVROS for ArduPilot communication
- gpsd + str2str (RTKLIB) for GPS data management
- Custom mission management node (monitors ArduPilot mission state, starts/stops recording)

**Ground Station (Post-Processing):**
- RTKLIB (rtkpost): PPK GPS processing
- Custom or commercial INS/GNSS processor: trajectory smoothing
- PDAL: point cloud pipeline (georeferencing, ground classification, DEM generation)
- LAStools: format conversion, tiling, optimization
- CloudCompare: visualization, quality control, manual editing
- QGIS: GIS integration, DEM visualization, product delivery

---

This specification covers the complete LiDAR payload design space for the described platform. The Livox Avia on a Jetson Orin Nano with PPK GPS represents the optimal balance of capability, weight, power, and cost for a 2–4 m wingspan fixed-wing UAV, delivering survey-grade point clouds at under 1.2 kg total payload mass.
