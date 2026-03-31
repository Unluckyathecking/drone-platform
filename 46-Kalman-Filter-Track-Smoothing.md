# Kalman Filter Track Smoothing and Prediction
*Research document for mpe-c2 team. Author: INTEROP agent. Date: 2026-03-31.*
*Covers: state vector design, filterpy vs hand-rolled, process/measurement noise tuning, source-specific noise, TrackManager integration, dead reckoning comparison, IMM for maneuvering targets.*
*Status: READ-ONLY reference for CORE to implement against. NO code in this document.*

---

## 1. Why the Current Dead Reckoning Is Insufficient

MPE's existing `predictor.py` implements dead reckoning: given last known position, speed, and heading, project forward in a straight line. This is:

- **Correct for short gaps** (seconds to a few minutes) for straight-moving entities
- **Wrong whenever the entity turns or accelerates** — error grows quadratically with time
- **Noisy** — raw AIS/ADS-B positions contain GPS measurement noise that is propagated directly to alert thresholds. A vessel that GPS-jitters ±50m looks like it is spoofing position if the threshold is too tight.
- **Discontinuous** — each new observation causes a discrete position jump visible in the track history

The Kalman filter solves all three problems simultaneously: it smooths noisy measurements, estimates velocity from position-only observations, and predicts ahead with a principled uncertainty model.

---

## 2. Filter Variant Selection

Four Kalman filter variants are relevant to MPE's use cases. Understanding the differences avoids over-engineering.

### Linear Kalman Filter (KF)

The standard Kalman filter assumes:
- Linear state transition (motion model is linear)
- Linear measurement model (sensor reading is a linear function of state)
- Gaussian noise

**When it applies:** Position tracking in a local Cartesian plane (metres North/East from a reference point). Constant velocity model. Observations are position only (no bearing-only measurements).

**Limitation for MPE:** Latitude/longitude are curvilinear — they are not Cartesian. For short ranges (<50km from a reference point), the flat-Earth approximation (1° lat ≈ 111km, 1° lon ≈ 111km × cos(lat)) is accurate to within 0.3%. For most tactical scenarios (a vessel operating within a 20km × 20km area), a linear KF in local NE (North-East) metres is correct and simple.

### Extended Kalman Filter (EKF)

Handles nonlinear motion or measurement models by linearising them (first-order Taylor expansion) at each time step. Required when:
- Tracking in geodetic coordinates over long distances (>50km)
- Bearing-only measurements (angle to target, not position)
- Coordinated turn model (heading rate is a state variable)

**Limitation:** EKF linearisation introduces error. For geodetic coordinates, requires converting lat/lon → ECEF → local NED → back to lat/lon at every step.

### Unscented Kalman Filter (UKF)

Handles nonlinear models more accurately than EKF by using sigma points (the unscented transform) instead of Jacobian linearisation.

**Specifically validated for AIS vessel tracking in geodetic coordinates** (arxiv.org/abs/2111.13254): A UKF operating directly in geodetic coordinates (lat, lon, speed, course) achieves better accuracy than a plane-Cartesian EKF and reduces computational cost 3× by eliminating coordinate transformations.

**This is the recommended filter for MPE's vessel tracking at any range.**

### IMM (Interacting Multiple Model)

Not a filter variant but a framework: run N Kalman filters (each with a different motion model) in parallel, weight them by likelihood, and output a blended state estimate. Handles entities that switch behaviour (a vessel cruising vs. manoeuvring; an aircraft straight-and-level vs. banking).

Covered in detail in Section 8.

---

## 3. State Vector Design

### Standard 4-State CV (Constant Velocity) Model

For most MPE tracking scenarios, the state vector is:

```
x = [lat, lon, v_lat, v_lon]
```

where:
- `lat`, `lon` are position in decimal degrees (or metres in local NE frame)
- `v_lat`, `v_lon` are velocity in degrees/second (or m/s in local NE frame)

**Why degrees/second and not knots or m/s directly?** When working in geodetic coordinates, velocity must be in the same units as position. The conversion: `v_lat [deg/s] = v_north [m/s] / 111,320`. `v_lon [deg/s] = v_east [m/s] / (111,320 × cos(lat))`.

In practice, implementing in a local NE plane (metres) is simpler and avoids the longitude scaling factor. Choose a reference point (e.g., the centre of the operational area), convert all positions to North/East offset in metres, run the filter, convert outputs back to lat/lon.

**State vector in local NE metres:**
```
x = [north_m, east_m, v_north_m_s, v_east_m_s]
```

### Extended 6-State CA (Constant Acceleration) Model

For aircraft at cruise (which can manoeuvre quickly), adding acceleration terms improves tracking during turns:

```
x = [north, east, v_north, v_east, a_north, a_east]
```

This is the model to use in the IMM alongside CV for the "maneuvering" sub-filter.

### Coordinated Turn (CT) Model

For entities executing known-rate turns (aircraft in standard-rate turns at 3°/s):

```
x = [north, east, v_north, v_east, ω]
```

where `ω` is the turn rate in rad/s. The state transition is nonlinear (requires EKF or UKF). This model is part of an IMM for aircraft tracking.

### Recommendation per Entity Type

| Entity Type | Primary Model | Notes |
|---|---|---|
| Cargo/tanker vessel | CV 4-state | Slow, rarely manoeuvres abruptly |
| Fishing vessel | IMM: CV + CT | Frequent course changes while fishing |
| Military vessel | IMM: CV + CT + CA | Can manoeuvre rapidly |
| Commercial aircraft (cruise) | CV 4-state | Straight and level most of the time |
| Commercial aircraft (approach/departure) | IMM: CV + CT | Frequent turns in TMA |
| Military aircraft / fast jet | IMM: CV + CA + CT | High acceleration, tight turns |
| Camera-detected ground vehicle | CV 4-state | Constrained to roads, low dynamics |
| Person (on foot) | CV 4-state (low Q) | Very slow, measurement noise dominates |

---

## 4. State Transition Matrix (F) and Process Noise (Q)

### Transition Matrix for CV Model

For time step `dt` seconds, the constant velocity transition matrix is:

```
F = [[1, 0, dt,  0 ],
     [0, 1,  0, dt ],
     [0, 0,  1,  0 ],
     [0, 0,  0,  1 ]]
```

This says: new position = old position + velocity × dt; velocity unchanged.

### Process Noise Covariance Q

Q encodes how much the motion model is wrong — how much the entity's true velocity changes between observations. It is the critical tuning parameter.

**Physical interpretation:** `Q` contains the variance of unmodelled accelerations. For a vessel that can change velocity by ±0.5 m/s between AIS reports (every 2–10 seconds), the process noise standard deviation σ_a ≈ 0.5 m/s.

**Discretised constant-velocity Q matrix (standard form):**

```
Q = σ_a² × [[dt⁴/4, 0,     dt³/2, 0    ],
             [0,     dt⁴/4, 0,     dt³/2],
             [dt³/2, 0,     dt²,   0    ],
             [0,     dt³/2, 0,     dt²  ]]
```

where `σ_a` is the standard deviation of unmodelled acceleration (m/s²).

**Tuned values per entity type:**

| Entity Type | σ_a (m/s²) | Rationale |
|---|---|---|
| Cargo vessel | 0.05 | Very slow to change speed/heading |
| Tanker vessel | 0.03 | Even slower |
| Fishing vessel | 0.3 | Active manoeuvring while working |
| Military vessel | 0.5 | Capable of rapid manoeuvres |
| Commercial aircraft (cruise) | 0.5 | Occasional ATC-directed turns |
| Commercial aircraft (approach) | 1.5 | Frequent turns, speed changes |
| Military aircraft | 5.0–10.0 | High-g manoeuvres |
| Drone / small UAS | 2.0 | Responsive, unpredictable |
| Ground vehicle | 1.0 | Acceleration/braking |
| Person | 0.2 | Walking speed changes |

**Tuning in practice:** Start with these values. If the filter lags badly behind real tracks → Q is too small (filter trusts the model too much). If the filter is jumpy and doesn't smooth well → Q is too large (filter trusts measurements too much). The optimal Q makes the normalised innovation squared (NIS) statistic close to 1.0 — this is the consistency check.

---

## 5. Measurement Model (H) and Measurement Noise (R)

### Measurement Matrix H

AIS, ADS-B, and camera all report position (lat, lon) but NOT velocity directly. The measurement is:

```
z = [north_m, east_m]   (position only)

H = [[1, 0, 0, 0],
     [0, 1, 0, 0]]
```

This 2×4 matrix extracts position from the 4-state vector. Velocity is inferred by the filter from successive position measurements — this is the key capability gain over dead reckoning.

### Measurement Noise Covariance R per Source

R encodes how accurate each sensor is. Larger R = noisier sensor = filter trusts measurements less and relies more on the motion model.

**AIS (Class A transponder):**
- GPS accuracy: typically 10m CEP (Circular Error Probable at 50%) for modern GNSS
- 95% accuracy: 20–30m horizontal
- AIS standard requires < 10m accuracy for Class A under normal conditions
- Reported as: some Class A transponders encode GPS accuracy in the message (RAIMflag + posAcc fields)
- **R_AIS = diag([15², 15²]) m²** — 15m std dev per axis is conservative but realistic

**AIS (Class B transponder — smaller vessels, yachts):**
- Less accurate GPS receiver, lower update rate (every 30s)
- **R_AIS_B = diag([25², 25²]) m²**

**ADS-B:**
- NACp 11 (best): < 3m accuracy (EPU 95%)
- NACp 9 (common commercial aircraft): < 30m
- NACp 7: < 185m (older equipment)
- Most modern commercial aircraft transmit NACp 10 or 11
- ADS-B messages include the NACp value — this should be used to set R dynamically
- **R_ADSB_default = diag([10², 10²]) m²** when NACp is not parsed
- **R_ADSB_NACp11 = diag([3², 3²]) m²** when NACp ≥ 11
- **R_ADSB_NACp9 = diag([20², 20²]) m²** when NACp = 9

**Camera (georegistered detection):**
- Accuracy depends on altitude, camera calibration, gimbal accuracy
- At 100m AGL with 1080p, 90° FOV: ~3m pixel accuracy, but gimbal angle errors add 5–15m
- Conservative estimate: 15–20m for uncalibrated, 5–10m for calibrated
- **R_camera = diag([15², 15²]) m²** (conservative, calibrated system)
- **R_camera_uncal = diag([30², 30²]) m²** (uncalibrated)

**CoT (from allied ATAK users):**
- Highly variable — depends on device GPS
- Smartphone GPS: 3–10m typical outdoors
- **R_CoT = diag([10², 10²]) m²** (smartphone); degrade if source is unknown

**Summary table:**

| Source | σ_pos (m) | R diagonal (m²) | Update rate |
|---|---|---|---|
| AIS Class A | 15 | 225 | 2–10 s (underway) |
| AIS Class B | 25 | 625 | 30 s |
| ADS-B NACp ≥ 10 | 5 | 25 | 0.5–1 s |
| ADS-B NACp 9 | 20 | 400 | 0.5–1 s |
| Camera (calibrated) | 10 | 100 | Per frame (5–10 Hz effective) |
| Camera (uncalibrated) | 30 | 900 | Per frame |
| CoT (smartphone) | 10 | 100 | Variable |

**Critical implementation note:** R should be set per-observation based on the source. `TrackManager` already tags each `Observation` with its `TrackSource`. The filter update step should look up R from a source→R mapping table, not use a single fixed R.

---

## 6. FilterPy vs Hand-Rolled: The Decision

### FilterPy

**What it is:** Open-source Python library by Roger Labbe. Implements KF, EKF, UKF, particle filter, IMM, and more. Companion book: "Kalman and Bayesian Filters in Python" (freely available at `rlabbe.github.io/Kalman-and-Bayesian-Filters-in-Python/`).

**Strengths:**
- Complete implementation of all required filter types (KF, UKF, IMM)
- `IMMEstimator` class directly implements the IMM algorithm with a list of sub-filters and a Markov transition matrix
- Well-tested, used in production systems
- The companion book is the best single reference for understanding the math
- Pure NumPy — no unusual dependencies

**Weaknesses:**
- Prioritises clarity over performance — uses matrix operations where scalar equations would be faster
- Last meaningful commit was 2020 — the library is not actively maintained
- NumPy overhead on small matrices (4×4) is real; a hand-rolled version using scalar equations can be 2–5× faster
- No typing annotations — harder to integrate with modern Python type checkers

**Recommendation: Use filterpy as the reference and prototype implementation.** Once the filter is validated (covariances tuned, entity types covered), the critical-path filters (those called on every AIS/ADS-B update, potentially at 1 Hz per entity with thousands of entities) can be hand-rolled.

### Hand-Rolled Implementation

A hand-rolled KF for the 4-state CV model requires implementing exactly 5 equations:

1. **Predict state**: `x_pred = F @ x`
2. **Predict covariance**: `P_pred = F @ P @ F.T + Q`
3. **Innovation**: `y = z - H @ x_pred`
4. **Kalman gain**: `K = P_pred @ H.T @ inv(H @ P_pred @ H.T + R)`
5. **Update state + covariance**: `x = x_pred + K @ y`; `P = (I - K @ H) @ P_pred`

For a 4-state, 2-measurement system, these are all small matrices. The speed gain from hand-rolling is significant at scale (thousands of entities updating at 1 Hz). A scalar implementation avoids all matrix allocation overhead.

**For MPE:** Use filterpy for the IMM (complex enough to benefit from the library). Hand-roll the simple CV KF for vessels and aircraft since it is trivial and performance matters at scale.

---

## 7. Integration with TrackManager

### One Filter Per Tracked Entity

Each `TrackedEntity` in `TrackManager` should own a Kalman filter instance. The filter is:
- Created when the entity first appears (initialised with the first observation)
- Updated every time a new `Observation` arrives for that entity
- Queried for the predicted current position (smoothed, interpolated to "now") whenever the entity's state is read

**Filter lifecycle mirroring entity lifecycle:**

```
Observation arrives → TrackManager.update(obs)
  → finds/creates TrackedEntity for obs.uid
  → if new entity: initialise KF with obs position; set P = large initial covariance
  → if existing entity:
      1. predict KF to obs.timestamp (accounts for variable dt between obs)
      2. select R based on obs.source
      3. update KF with obs position (z = [north, east])
  → entity.position = KF.x (smoothed position)
  → entity.velocity = KF.x[2:4] (estimated velocity — not directly observable from single source)
```

### Variable dt Handling

AIS reports every 2–180 seconds. ADS-B reports every 0.5–2 seconds. The prediction step `x_pred = F(dt) @ x` must use the actual time elapsed since the last observation, not a fixed dt. Both F and Q must be recomputed at each prediction step using the actual dt.

This is critical: a fixed-dt filter that receives variable-interval AIS reports will accumulate state errors. FilterPy's `KalmanFilter.predict(u, B, F, Q)` accepts F and Q per call.

### Initial Covariance P

When a filter is created, P (the state error covariance matrix) should be set to:
- Position uncertainty: match the source R (e.g., 225 m² for AIS Class A)
- Velocity uncertainty: large (e.g., 100 m/s² = 10,000 m²/s²) since velocity is unknown at initialisation

```
P_init = diag([225, 225, 10000, 10000])   # for AIS Class A, m² and (m/s)²
```

The filter converges to accurate velocity estimates after 3–5 observations.

### Stale Prediction

When no new observation arrives (e.g., AIS blackout), the engine currently uses dead reckoning from `predictor.py`. With a Kalman filter, the predicted state `x_pred(t_now)` is already the best estimate of current position given the motion model and last known velocity. The filter's `P` matrix grows over time in the absence of updates, correctly representing increasing uncertainty.

This replaces the `predictor.dead_reckoning()` call in the classify loop with `entity.kf.predict(dt=t_now - t_last_obs)`. The engine gets both position and confidence (from diagonal of P) automatically.

---

## 8. Dead Reckoning vs Kalman Filter: The Improvement

### Where Dead Reckoning Fails

Dead reckoning (`predictor.py`) predicts position as:
```
lat_pred = lat_last + v_lat × dt
lon_pred = lon_last + v_lon × dt
```

Issues:
1. **Uses last reported SOG/COG from AIS** — these are themselves noisy (AIS velocity fields have ±0.1 knot resolution for SOG, 0.1° resolution for COG)
2. **No noise filtering** — position jumps from AIS noise are propagated directly
3. **Single-model** — assumes the entity continues at exactly its last reported velocity
4. **No uncertainty quantification** — no way to know how confident the prediction is

### Kalman Filter Improvements

| Metric | Dead Reckoning | Kalman Filter |
|---|---|---|
| Position smoothing | None — raw GPS noise visible | Filters noise; track appears smooth |
| Velocity estimate | From last AIS SOG/COG field | Estimated from position history; more accurate for vessels that underreport SOG |
| 60s-ahead position error | Grows linearly with velocity noise | Grows with uncertainty from Q; physically bounded |
| 5-minute prediction (AIS blackout) | Drifts if last velocity was noisy | Estimate + explicit uncertainty interval |
| Anomaly detection | Position jump detection uses raw Δposition | Can use innovation (measurement - prediction) — a normalised innovation > threshold signals anomaly |

**Validated improvement from research:** The Extended Kalman Filter for AIS ship tracking demonstrated real-time track prediction and smoothing in Trondheim harbour (Fossen & Fossen, Semantic Scholar). The UKF in geodetic coordinates achieves 3× computational reduction vs EKF while improving accuracy (arXiv 2111.13254).

**The most important new capability:** The Kalman filter's **innovation** (the difference between what the filter predicted and what the sensor measured) is a powerful anomaly detector. An entity that AIS-spoofs its position will produce an abnormally large innovation because its claimed position is inconsistent with its recent track. This improves on MPE's current `classifier.py` spoofing detection (which uses a raw haversine jump check) with a physically-principled, velocity-aware check.

---

## 9. IMM for Maneuvering Entities

### What IMM Solves

A cargo vessel cruising at 12 knots rarely manoeuvres — a CV filter works well. The same vessel entering port turns, slows, and stops in sequences that break the CV model. Running a single CV filter produces large innovations and sluggish track updates during port manoeuvres.

IMM solves this by running multiple filters in parallel:
- Filter 1: CV (straight-line cruise)
- Filter 2: CT (coordinated turn, constant turn rate)
- Filter 3: CA (acceleration/deceleration)

At each time step, IMM:
1. Computes the likelihood of the current observation under each filter's prediction
2. Updates filter weights (mode probabilities) via Bayes' rule
3. Mixes the filter states according to a Markov transition matrix
4. Updates all filters with the current observation
5. Outputs a blended state estimate: `x_combined = Σ μᵢ × xᵢ`

### Markov Transition Matrix

The Markov matrix M encodes how likely a model switch is between time steps. For a vessel:

```
         CV    CT    CA
CV  [ [0.90, 0.05, 0.05],   ← likely to stay in cruise
CT  [  0.10, 0.85, 0.05],   ← manoeuvring often continues
CA  [  0.10, 0.05, 0.85] ]  ← acceleration phase often continues
```

For an aircraft (faster model switching):

```
         CV    CT    CA
CV  [ [0.80, 0.10, 0.10],
CT  [  0.15, 0.80, 0.05],
CA  [  0.15, 0.05, 0.80] ]
```

### FilterPy IMM Implementation

FilterPy provides `IMMEstimator` (in `filterpy.kalman`):
- Takes a list of `KalmanFilter` (or EKF/UKF) objects as sub-filters
- Takes `mu` (initial mode probabilities, e.g. `[0.33, 0.33, 0.34]`)
- Takes `M` (Markov transition matrix, N×N)
- `imm.predict()` and `imm.update(z)` work identically to a single KF

GitHub references for standalone Python IMM implementations:
- `github.com/azimuth-san/IMM-Filter` — clean Python 3 IMM
- `github.com/ludvigls/IMM-PDA` — IMM with probabilistic data association for radar

### When to Use IMM vs Simple KF

**Use simple CV KF:**
- Cargo vessels, tankers in open ocean
- Commercial aircraft in cruise (>FL200)
- Ground vehicles on known road network (add road-snapping instead of IMM)

**Use IMM (CV + CT):**
- Fishing vessels (active manoeuvring)
- Aircraft in terminal areas (approach/departure)
- Military vessels (unpredictable manoeuvring)

**Use IMM (CV + CT + CA):**
- Military aircraft / fast jets
- Vessels in distress (erratic behaviour)

**Pragmatic recommendation for MPE MVP:** Implement CV KF first for all entities. Add IMM only for military vessel and military aircraft entity types in a second pass. The innovation-based anomaly detection improvement is available from the simple CV filter already.

---

## 10. Summary: What CORE Needs to Build

### New Module: `track_filter.py`

One module containing:

| Component | Implementation | Notes |
|---|---|---|
| `EntityFilter` base class | Interface: `initialise(obs)`, `predict(dt)`, `update(z, R)`, `state → (lat, lon, v_north, v_east)` | |
| `CVKalmanFilter` | Hand-rolled 4-state CV filter | For vessels and commercial aircraft |
| `UKFVesselFilter` | filterpy UKF in geodetic coordinates | For vessels tracked over long distances |
| `IMMFilter` | filterpy IMMEstimator wrapping CV + CT | For fishing vessels, military entities |
| `R_TABLE` | Dict mapping `TrackSource → R matrix` | Source-specific measurement noise |
| `Q_TABLE` | Dict mapping `EntityType → σ_a` | Entity-specific process noise |

### Changes to `TrackManager`

`TrackedEntity` needs one new field: `filter: EntityFilter`. On first observation: initialise filter. On subsequent observations: call `filter.predict(dt)` then `filter.update(z, R)`. Entity position read from `filter.state` rather than last raw observation.

### Changes to `c2_models.py`

No changes to data structures. The filter is an implementation detail of `TrackedEntity` — the external interface (`.lat`, `.lon`, `.speed`, `.heading`) stays the same.

### Changes to `predictor.py`

The `dead_reckoning()` method should be replaced with a call to `entity.filter.predict(dt)`. The result is the same (projected future position) but from the filter's smoothed velocity estimate rather than the last raw AIS velocity field.

### Innovation as Anomaly Signal

The `classifier.py` spoofing detection (currently: `haversine(pos_now, pos_last) > threshold`) should be augmented to use the Kalman innovation: `innovation = z - H @ x_pred`. A normalised innovation squared (NIS) exceeding a chi-squared threshold (chi2 with 2 degrees of freedom, 99.9% threshold ≈ 13.8) is a statistically sound AIS spoofing flag. This replaces the ad-hoc haversine jump check with a principled, velocity-aware test.

---

## 11. Key References

- FilterPy library: [github.com/rlabbe/filterpy](https://github.com/rlabbe/filterpy)
- FilterPy IMMEstimator: [filterpy.readthedocs.io/en/latest/kalman/IMMEstimator.html](https://filterpy.readthedocs.io/en/latest/kalman/IMMEstimator.html)
- Kalman and Bayesian Filters in Python (book): [rlabbe.github.io/Kalman-and-Bayesian-Filters-in-Python](https://rlabbe.github.io/Kalman-and-Bayesian-Filters-in-Python/)
- UKF for vessel tracking in geodetic coordinates: [arxiv.org/abs/2111.13254](https://arxiv.org/abs/2111.13254)
- Kalman filter for AIS ship tracking (EKF): [Semantic Scholar — Fossen & Fossen](https://www.semanticscholar.org/paper/Extended-Kalman-Filter-Design-and-Motion-Prediction-Fossen-Fossen/e9cdde18bdd35a1615126c5203a1c2d8823cddd8)
- IMM algorithm reference (JHU APL): [jhuapl.edu/Content/techdigest V22-N04](https://www.jhuapl.edu/Content/techdigest/pdf/V22-N04/22-04-Genovese.pdf)
- IMM for maneuvering aircraft: [MDPI Algorithms 2024](https://www.mdpi.com/1999-4893/17/9/399)
- Passive ADS-B tracking with UKF: [ACM DL 10.1145/3673277.3673380](https://dl.acm.org/doi/fullHtml/10.1145/3673277.3673380)
- ADS-B NACp accuracy table: [ResearchGate table](https://www.researchgate.net/figure/Navigation-Accuracy-Category-for-Position-NACp_tbl9_331033102)
- AIS reporting intervals: [arundaleais.github.io](https://arundaleais.github.io/docs/ais/ais_reporting_rates.html)
- AIS Class A position report spec: [navcen.uscg.gov](https://www.navcen.uscg.gov/ais-class-a-reports)
- Kalman filter constant velocity model tutorial: [balzer82.github.io/Kalman](https://balzer82.github.io/Kalman/)
- Standalone Python IMM: [github.com/azimuth-san/IMM-Filter](https://github.com/azimuth-san/IMM-Filter)
- Kalman filter explained: [kalmanfilter.net](https://kalmanfilter.net/)
