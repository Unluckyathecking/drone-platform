# In-Flight Power Transfer Technologies for Large Fixed-Wing UAVs

## Comprehensive Research Document — MEDIUM Tier (25–50 kg) and LARGE Tier (100–200 kg)

---

## 1. LASER POWER BEAMING

### 1.1 Operating Principle

A ground-based high-power laser generates a collimated beam directed at a photovoltaic (PV) receiver mounted on the drone. The receiver converts optical energy back to electricity. The system is essentially a wireless extension cord made of light.

The power chain:
```
Wall power → Laser driver → Laser source → Atmosphere → PV receiver → Power conditioning → Drone bus
```

### 1.2 Wavelength Selection

Three primary wavelengths are used in laser power beaming:

- **808–980 nm (near-IR):** Matches silicon and GaAs PV cell peak response. Wall-plug efficiency of diode lasers at 980 nm reaches 50–65%. Atmospheric transmission is good in clear weather (~85–95%/km at sea level). PV conversion efficiency using band-gap-matched cells reaches 50–60%. This is the most commonly used wavelength for drone power beaming demonstrations.

- **1064 nm (Nd:YAG):** Mature laser technology, good atmospheric window. Slightly lower PV conversion efficiency than 980 nm because fewer cell chemistries are optimised for this wavelength. Used in some military and DARPA programs.

- **1550 nm (eye-safe):** The retina does not focus this wavelength, so it is absorbed by the cornea and lens before reaching the retina. This makes it Class 1M eye-safe at much higher power densities than shorter wavelengths. The trade-off is that PV conversion efficiency drops significantly (InGaAs cells at ~30–40% conversion) and suitable high-power laser sources are more expensive. Preferred for any system operating near populated areas.

**Why 980 nm dominates:** The combination of cheap, efficient diode laser arrays and well-matched GaAs PV cells gives the best end-to-end efficiency. Eye safety is managed through beam control interlocks and exclusion zones rather than wavelength choice.

### 1.3 End-to-End Efficiency

The chain of losses is multiplicative:

| Stage | Efficiency | Notes |
|---|---|---|
| Laser wall-plug | 50–65% | Diode arrays at 980 nm |
| Beam forming optics | 90–95% | Collimation and steering |
| Atmospheric transmission (1 km, clear) | 85–95% | Absorption + scattering |
| Atmospheric transmission (5 km, clear) | 50–75% | Cumulative losses |
| Atmospheric transmission (10 km, clear) | 25–55% | Highly variable |
| PV receiver conversion | 50–60% | Band-gap matched GaAs |
| Power conditioning | 90–95% | DC-DC conversion |

**Realistic end-to-end efficiency:**

| Range | End-to-end efficiency | To deliver 500 W, need transmit: |
|---|---|---|
| 1 km, clear | 20–30% | 1.7–2.5 kW electrical input |
| 5 km, clear | 10–18% | 2.8–5 kW |
| 10 km, clear | 5–12% | 4.2–10 kW |
| 1 km, light haze | 12–20% | 2.5–4.2 kW |

### 1.4 Realistic Power Delivery

For a ground-based laser system with 5–10 kW electrical input:

- **At 1 km:** 1,000–3,000 W delivered to drone
- **At 5 km:** 500–1,800 W delivered
- **At 10 km:** 250–1,200 W delivered

For a LARGE tier drone at cruise (200–500 W needed), laser beaming from 1–5 km is plausible. At 10 km the margins get thin. At the target operational altitude of 3,000–5,000 m (slant range), you would need either very high-power lasers (50+ kW class) or accept that laser alone cannot sustain cruise.

### 1.5 Key Players and Demonstrations

**PowerLight Technologies (formerly LaserMotive):**
- Won NASA's 2009 Space Elevator Power Beaming Challenge: powered a robotic climber up a 900 m cable using a ground-based laser, delivering ~500 W at the receiver.
- In 2012, demonstrated a Stalker small UAS flying for 48 hours continuously on laser power. The drone was a Lockheed Martin Stalker (small, ~6 kg) flying at low altitude (~100 m range). This is the most cited successful drone laser power demonstration.
- Acquired by PowerLight Technologies. Has since been working on larger-scale power beaming for defence.

**DARPA SUPER Program (Stand-off Ubiquitous Power/Energy Replenishment):**
- Aimed to deliver 10+ kW over 1+ km to support persistent UAV operations.
- Funded multiple contractors including Lockheed Martin.
- Programme explored adaptive optics, beam control, and high-efficiency PV receivers.

**Lockheed Martin:**
- Partnered with LaserMotive on the Stalker demonstration.
- Has ongoing directed-energy programs relevant to power beaming.

**Chinese Academy of Sciences (2023–2024):**
- Demonstrated laser-powered drone flight of a small quadrotor at several hundred metres range. Published results showing sustained flight for extended periods.

### 1.6 Beam Tracking

Keeping a tight laser beam on a moving drone is a critical engineering challenge:

- **Beam divergence:** A well-collimated 980 nm beam from a 20 cm aperture has a divergence of roughly 6 microradians, giving a spot diameter of ~6 mm at 1 km. In practice, atmospheric turbulence and optics imperfections widen this to 0.1–1 m at 1 km.
- **Tracking accuracy:** The beam must stay on the PV receiver (typically 0.5–2 m across). At 5 km range, this requires pointing accuracy of 0.1–0.4 mrad — achievable with modern gimbal-stabilised tracking systems.
- **Cooperative tracking:** The drone carries a corner reflector or beacon (IR LED or radio) that the ground station tracks. This is far easier than tracking a non-cooperative target.
- **Safety interlock:** If tracking is lost, the beam must shut off within milliseconds (beam wanders = eye safety hazard + wasted power).

**Relevance to FSO laser tracking gimbal (doc 23):** The FSO communication gimbal already has precision pointing (sub-mrad), optical tracking, and a stabilised mount. The receiver optics and tracking algorithms could be adapted. However, the power receiver PV panel is physically much larger than a comms detector, so the gimbal does not need the same extreme precision — tracking to within ±0.5 m at 5 km is sufficient. The control loop architecture (beacon tracking, gimbal stabilisation) transfers directly.

### 1.7 Receiver Weight

- **PV panel:** High-efficiency GaAs cells at ~1 kg/m² for the cells, plus substrate, wiring, bypass diodes. For a 0.5 m² panel (capable of receiving ~500 W in good conditions): 1–2 kg.
- **Power conditioning:** DC-DC converter, MPPT controller, thermal management: 0.5–1.5 kg.
- **Total receiver system for 500 W class:** 2–4 kg.
- **For 2 kW class:** 5–10 kg (larger panel, heavier power electronics).

This is very reasonable for both MEDIUM and LARGE tier drones.

### 1.8 Eye Safety

Class 4 lasers (multi-kW) are extremely dangerous to eyesight and skin at any range within the beam path. Mitigation approaches:

- **Exclusion zone:** No personnel within the beam corridor. Viable for remote/military sites, not for urban areas.
- **Eye-safe wavelength (1550 nm):** Reduces hazard dramatically but with 30–40% lower conversion efficiency.
- **Radar/camera safety system:** Ground station detects aircraft or people entering the beam path and shuts down within milliseconds.
- **Low-power scanning:** Rather than a single high-power beam, scan a lower-power beam rapidly across the receiver. At any instant, the power density is lower. The receiver integrates the energy thermally.

For the comms relay constellation concept, the ground stations would be at fixed sites with controlled perimeters, making exclusion-zone approaches feasible.

### 1.9 Weather Limitations

This is laser beaming's Achilles heel:

| Condition | Transmission at 1 km | Impact |
|---|---|---|
| Clear sky | 85–95% | Full power |
| Light haze | 60–80% | Reduced but usable |
| Heavy haze | 30–50% | Marginal |
| Light rain (2 mm/hr) | 40–70% | Significantly reduced |
| Heavy rain (25 mm/hr) | 10–30% | Unusable |
| Fog (visibility <1 km) | <10% | Beam blocked |
| Cloud (if drone above cloud) | ~0% through cloud | Cannot penetrate |

**UK relevance:** The UK averages 150+ days per year with significant cloud cover. A drone at 3,000–5,000 m altitude would frequently be above cloud with no line of sight to the ground station. This is a fundamental problem for laser beaming in the UK climate.

### 1.10 Summary for This Project

| Parameter | Value |
|---|---|
| TRL | 5–6 (demonstrated on small drones, not at scale for large UAVs) |
| Power to MEDIUM tier | 500–2,000 W at 1–5 km range |
| Power to LARGE tier | 500–3,000 W at 1–5 km range |
| Weight penalty on drone | 2–10 kg (receiver system) |
| Ground infrastructure | 5–50 kW laser, tracking gimbal, cooling, power supply. Cost: £100k–£1M+ |
| Weather limitation | Severe — fog, cloud, heavy rain block the beam |
| Range/altitude | Practical to ~5 km slant range; beyond 10 km very challenging |
| Cost estimate | £200k–£2M per ground station |
| Regulatory | Eye safety regulations, aviation authority approval, exclusion zones |
| Demonstrated on drone? | Yes — LaserMotive/Stalker (2012), 48-hour flight |
| Comms relay relevance | Poor standalone — UK weather makes it unreliable. Useful as supplementary top-up in clear conditions |

---

## 2. MICROWAVE POWER BEAMING

### 2.1 Operating Principle

A ground-based microwave transmitter (klystron, magnetron, or solid-state array) generates a focused microwave beam. The drone carries a rectenna — a rectifying antenna array — that converts the microwave energy directly to DC electricity with very high efficiency.

```
Wall power → Microwave source → Transmit antenna → Atmosphere → Rectenna → DC bus
```

The key advantage: microwaves at ISM band frequencies (2.45 GHz, 5.8 GHz) propagate through cloud, rain, and moderate weather with minimal attenuation — the opposite of laser's weakness.

### 2.2 Frequency Selection

| Frequency | Wavelength | Pros | Cons |
|---|---|---|---|
| 2.45 GHz | 122 mm | Highest rectenna efficiency (85%), ISM band, cheap components | Very large spot size at distance — needs huge transmit antenna |
| 5.8 GHz | 52 mm | Still ISM band, smaller spot, good efficiency (75–80%) | More expensive components than 2.45 GHz |
| 35 GHz | 8.6 mm | Much tighter beam, smaller antennas | Lower rectenna efficiency (~50–60%), expensive, more rain attenuation |
| 94 GHz | 3.2 mm | Very tight beam | Expensive, significant rain attenuation, lower efficiency |

### 2.3 The Beam Spread Problem

This is the fundamental limitation of microwave power beaming. The spot diameter at range R from a transmit antenna of diameter D at wavelength λ:

```
D_spot ≈ 2.44 × λ × R / D_transmit
```

Worked examples at 2.45 GHz (λ = 0.122 m):

| Transmit dish diameter | Range 1 km | Range 5 km | Range 10 km |
|---|---|---|---|
| 3 m | 99 m | 496 m | 993 m |
| 10 m | 30 m | 149 m | 298 m |
| 30 m | 10 m | 50 m | 99 m |

At 5.8 GHz (λ = 0.052 m):

| Transmit dish diameter | Range 1 km | Range 5 km | Range 10 km |
|---|---|---|---|
| 3 m | 42 m | 212 m | 423 m |
| 10 m | 13 m | 63 m | 127 m |
| 30 m | 4.2 m | 21 m | 42 m |

**The problem is clear:** To get a reasonably sized spot at multi-kilometre range at 2.45 GHz, you need a transmit antenna tens of metres in diameter. At 5.8 GHz it is more reasonable but still large. At 35 GHz you get manageable spot sizes from a 3–5 m dish, but efficiency drops and rain attenuation increases.

### 2.4 Power Density and Delivery Calculation

If total transmitted power is P_tx and spot area is A_spot (approximating as uniform over the main lobe, which overstates centre intensity), then:

```
Power density = P_tx / A_spot (W/m²)
Received power = Power density × A_rectenna × η_rectenna
```

**Example:** 5.8 GHz, 10 m transmit dish, 5 km range, 10 kW transmitted:
- Spot diameter: 63 m → Area: ~3,100 m²
- Power density: 10,000 / 3,100 = 3.2 W/m²
- Rectenna area on drone: 5 m² (half of LARGE tier upper wing surface)
- Rectenna efficiency: 75%
- Received power: 3.2 × 5 × 0.75 = **12 W**

That is essentially nothing. To get 500 W at the drone, you would need:
- 500 / (0.75 × 3.2) = 208 m² of rectenna (absurd), OR
- Transmit 417 kW (absurd and dangerous), OR
- Use a much larger transmit dish

**With a 30 m dish at 5.8 GHz, 5 km, 50 kW transmitted:**
- Spot diameter: 21 m → Area: 346 m²
- Power density: 50,000 / 346 = 144 W/m²
- 5 m² rectenna at 75%: **542 W received**

This is feasible but requires a 30 m dish transmitting 50 kW — a major installation.

**At 35 GHz with a 5 m dish, 5 km, 10 kW transmitted:**
- Spot diameter: 2.44 × 0.0086 × 5000 / 5 = 21 m → Area: 346 m²
- Power density: 10,000 / 346 = 28.9 W/m²
- 5 m² rectenna at 55%: **79 W**

Still need more power or bigger dish at 35 GHz.

### 2.5 Rectenna Design

A rectenna is an array of small antenna elements, each connected to a rectifying diode (Schottky diode). The antenna captures RF energy, the diode rectifies it to DC, and a combining network sums the DC outputs.

- **2.45 GHz rectenna efficiency:** 80–85% demonstrated in laboratory settings (Brown, 1984; McSpadden, 1998). This is remarkably high.
- **5.8 GHz:** 75–80%.
- **35 GHz:** 50–60%.
- **Conformal rectenna on wing surface:** Yes, this is viable. Rectenna elements are thin, printed-circuit structures. They can be fabricated on flexible substrate and bonded to the wing skin. Weight: ~0.5–2 kg/m² including substrate and wiring. The wing becomes both an aerodynamic surface and a power receiver.
- **Combined with solar cells:** Theoretically, you could have solar cells on top and rectenna elements on the bottom of the wing, or interleave them. This is an active research topic.

### 2.6 Weather Performance

| Condition | 2.45 GHz | 5.8 GHz | 35 GHz |
|---|---|---|---|
| Clear sky | >99% | >99% | >98% |
| Light rain (5 mm/hr) | >99% | >98% | ~90% |
| Heavy rain (25 mm/hr) | >98% | ~95% | ~70% |
| Fog | >99% | >99% | ~95% |
| Cloud | >99% | >99% | ~95% |

This is the massive advantage over laser — 2.45 GHz and 5.8 GHz are essentially all-weather.

### 2.7 Demonstrations

**Mitsubishi Heavy Industries (2015):** Demonstrated 10 kW of microwave power beamed to a small drone at ~50 m distance. The drone hovered on received microwave power. Short range, but proof of concept.

**William C. Brown (1960s–1980s):** Pioneered microwave power beaming. In 1964, demonstrated a helicopter sustained by microwave power. In the 1970s–80s at NASA JPL, demonstrated rectenna efficiencies exceeding 80%.

**NASA/DOE Solar Power Satellite studies (1970s–2000s):** Extensive theoretical work on beaming GW-class power from space to Earth. The rectenna technology is mature; the challenge is the space infrastructure.

**Japan JAXA (2015):** Beamed 1.8 kW over 55 m to a target using microwaves, as part of space-based solar power research.

### 2.8 Regulatory Issues

Transmitting kilowatts or tens of kilowatts of microwave energy into the sky raises serious regulatory concerns:

- **RF exposure limits:** ICNIRP limits for general public at 2.45 GHz: 10 W/m². A beam with 144 W/m² at 5 km range would exceed this at ground level near the transmitter by orders of magnitude.
- **Exclusion zones:** Required around the transmitter and under the beam path.
- **ISM band use:** While 2.45 GHz and 5.8 GHz are ISM bands, high-power directional transmission is regulated differently from omnidirectional low-power use.
- **Aviation safety:** An aircraft flying through a multi-kW microwave beam could experience avionics interference.
- **Ofcom licensing:** Would require special licensing in the UK. No established framework for this application.

### 2.9 Summary for This Project

| Parameter | Value |
|---|---|
| TRL | 4–5 (individual components proven, system-level demonstrations only at short range) |
| Power to MEDIUM tier | 50–300 W feasible with large ground infrastructure |
| Power to LARGE tier | 200–1,000 W feasible with very large ground infrastructure |
| Weight penalty on drone | 1–5 kg (conformal rectenna + power conditioning) |
| Ground infrastructure | 10–30 m dish, 10–100 kW transmitter, tracking system. Cost: £500k–£5M |
| Weather limitation | Minimal at 2.45/5.8 GHz — this is the key advantage |
| Range/altitude | Practical to 5–10 km but needs very large transmit antenna |
| Cost estimate | £1M–£10M per ground station |
| Regulatory | Severe — high-power RF transmission, no established regulatory path |
| Demonstrated on drone? | Yes — MHI (2015) at short range; Brown's helicopter (1964) |
| Comms relay relevance | Theoretically excellent (all-weather) but ground infrastructure is impractical for multiple stations |

---

## 3. TETHERED POWER

### 3.1 Operating Principle

A physical cable (tether) connects the drone to a ground station, delivering electrical power continuously. The ground station houses a power supply and a motorised spool that pays out and reels in the tether as the drone changes altitude or position.

```
Mains power → Ground PSU → High-voltage DC on tether → Drone DC-DC converter → Bus
```

### 3.2 Tether Design

To minimise I²R losses and cable weight, tethered systems use high-voltage DC (200–400 V, some up to 800 V) over thin conductors:

- **Pure copper tether:** Simple, reliable. Weight: 20–50 g/m for conductors carrying 1–5 kW at 400 V. Total tether weight including jacket and strength member: 30–80 g/m.
- **Fibre-optic + copper hybrid:** Adds data link (video, telemetry) to the power cable. Weight: 40–100 g/m.
- **High-strength tether:** Dyneema or Kevlar strength member carries the tensile load; copper conductors are bonded alongside. The strength member weighs 5–15 g/m, so total is dominated by copper.

### 3.3 Altitude vs Cable Weight

This is the fundamental trade-off. The cable must support its own weight plus wind loading.

For a tether at 50 g/m:
- 100 m altitude: 5 kg hanging weight
- 300 m altitude: 15 kg
- 500 m altitude: 25 kg
- 1,000 m altitude: 50 kg

For the MEDIUM tier drone (25–50 kg MTOW), a 15–25 kg tether eats 30–100% of useful payload — only viable to ~200–300 m.

For the LARGE tier drone (100–200 kg MTOW), a 50 kg tether is 25–50% of MTOW — viable to ~500–1,000 m but severely constrains other payload.

**Target altitude of 3,000–5,000 m for comms relay: a tether would weigh 150–250 kg.** This exceeds the LARGE tier MTOW entirely. Tethered operation is categorically incompatible with the comms relay altitude requirement.

### 3.4 Fixed-Wing Tether Complications

Tethered multirotors hover in place — the tether hangs vertically. Fixed-wing aircraft must fly forward to generate lift. This creates severe problems:

- **Tether drag:** The cable cuts through the air at the drone's forward speed, generating enormous aerodynamic drag. A 100 m cable at 20 m/s cruise speed would generate drag comparable to the drone's own airframe drag.
- **Orbit pattern:** The fixed-wing must orbit around the ground station. The tether wraps, tangles, and must spool in/out dynamically. Some concepts use a powered kite approach where the drone flies in circles on a tether like a kite on a string.
- **Ground spool complexity:** Must track the drone's position in 3D and manage tether tension, pay-out, and direction simultaneously.

**Assessment: Tethered power for a fixed-wing is impractical except in very constrained scenarios (powered kite orbiting at low altitude).**

### 3.5 Commercial Systems

**Elistair (France):**
- Orion 2 Tethered Station: powers multirotors to 100 m altitude, 2.5 kW delivered, tether weight ~50 g/m, 10+ hour continuous flight demonstrated. Used by military, law enforcement, and telecom.
- Light-T: lighter system for smaller drones, 60 m altitude, 1.5 kW.
- Customers include French military, US DoD, telecom operators.
- Cost: €30,000–€100,000 per system.

**CyPhy Works (acquired by Shield AI):**
- Developed the PARC tethered drone system using a microfilament tether (extremely thin fibre-optic for data, with a separate power approach). Aimed at persistent surveillance.
- The microfilament was innovative but power delivery over such thin filament was limited.

**Drone Aviation Corp (USA):**
- WATT (Winch Aerostat Tethered Tether) — larger aerostat systems, not directly comparable.

### 3.6 Hybrid Tethered Concept

**Tethered recharging station:** Rather than flying on the tether, the drone lands periodically at a ground station equipped with automated fast-charging or battery swap. This avoids the tether-in-flight problem entirely.

- Drone flies freely for 1–2 hours on battery
- Returns to automated ground station
- Lands, batteries swapped robotically in 2–5 minutes
- Takes off again

This is highly relevant to the airbase/ground station concept in the project. More on this in Section 5.

### 3.7 Summary for This Project

| Parameter | Value |
|---|---|
| TRL | 8–9 for multirotors; 3–4 for fixed-wing |
| Power to MEDIUM tier | 1–3 kW (but altitude limited to ~200 m) |
| Power to LARGE tier | 2–5 kW (altitude limited to ~500 m) |
| Weight penalty on drone | Tether weight is the penalty: 5–50 kg depending on altitude |
| Ground infrastructure | Power supply, spool, tracking system. Cost: £30k–£100k |
| Weather limitation | Wind is the main issue (tether loading). Rain/cloud no problem |
| Range/altitude | 50–300 m practical; 500 m maximum; 3,000–5,000 m impossible |
| Cost estimate | £30k–£100k per station |
| Regulatory | Tethered drones have different (often simpler) regulations than free-flying |
| Demonstrated on drone? | Yes — mature for multirotors (Elistair). Not demonstrated for fixed-wing at scale |
| Comms relay relevance | Incompatible — cannot reach required altitude |

---

## 4. SOLAR POWER (ON-WING)

### 4.1 Solar Cell Technologies and Efficiency

| Technology | Efficiency | Weight (g/m²) | Flexibility | Cost |
|---|---|---|---|---|
| Standard monocrystalline Si | 20–22% | 2,500–4,000 (with glass) | Rigid | Low |
| Thin-film Si (amorphous) | 8–12% | 300–800 | Flexible | Low |
| GaAs (single junction) | 28–30% | 500–1,000 (with substrate) | Semi-flexible | Very high (£200–500/W) |
| Multi-junction (GaInP/GaAs/Ge) | 35–40% | 800–1,500 | Semi-rigid | Extremely high (£500–2,000/W) |
| SunPower IBC cells (Si) | 22–25% | 500–800 (without glass) | Semi-flexible | Moderate |
| Perovskite (emerging) | 25–33% (lab) | 200–500 | Very flexible | Low (projected) |

**For UAV applications**, the relevant metric is W/kg, not just efficiency:

| Technology | W/m² at AM1.5 | Weight (g/m²) | W/kg |
|---|---|---|---|
| Thin-film Si | 80–120 | 500 | 160–240 |
| SunPower IBC | 220–250 | 700 | 314–357 |
| GaAs | 280–300 | 800 | 350–375 |
| Multi-junction | 350–400 | 1,200 | 292–333 |
| Alta Devices GaAs (thin-film) | 260–290 | 300–400 | 650–967 |

**Alta Devices (now Hanergy)** produced thin-film GaAs cells with world-record W/kg ratios: ~1,000 W/kg. These were specifically developed for UAV and satellite applications. Unfortunately, Alta Devices ceased operations around 2020–2021, but similar technology is being pursued by other manufacturers.

### 4.2 Available Wing Area and Power

**LARGE tier drone (6–10 m wingspan, high aspect ratio):**
- Wing area: 4–8 m² (depending on aspect ratio and chord)
- Upper surface available for solar: 60–70% (leading edge curve, control surfaces, structural joints reduce usable area)
- Usable solar area: 2.5–5.5 m²

**Power in direct sun (1,000 W/m² irradiance at optimal angle):**

| Cell technology | 3 m² coverage | 5 m² coverage |
|---|---|---|
| Thin-film Si (10%) | 300 W | 500 W |
| SunPower IBC (23%) | 690 W | 1,150 W |
| GaAs (29%) | 870 W | 1,450 W |
| Multi-junction (38%) | 1,140 W | 1,900 W |

**Weight of solar installation:**

| Cell technology | 5 m² cells weight | + Wiring & encapsulant | Total |
|---|---|---|---|
| Thin-film Si | 2.5 kg | 1 kg | 3.5 kg |
| SunPower IBC | 3.5 kg | 1 kg | 4.5 kg |
| GaAs (thin-film) | 1.5–2 kg | 1 kg | 2.5–3 kg |
| Multi-junction | 6 kg | 1.5 kg | 7.5 kg |

### 4.3 Power Required for Cruise

For a high-aspect-ratio LARGE tier glider/sailplane-type UAV at altitude:

- **Cruise speed:** 15–25 m/s (depending on altitude and wing loading)
- **L/D ratio:** 25–35 (achievable with AR > 20 and clean design)
- **Cruise power = (Weight × g × V_cruise) / (L/D × η_propulsion)**
- For 150 kg drone, L/D = 30, V = 20 m/s, η_prop = 0.7:
  - Power = (150 × 9.81 × 20) / (30 × 0.7) = **1,402 W**

For a lighter, more optimised design (100 kg, L/D = 35):
- Power = (100 × 9.81 × 18) / (35 × 0.75) = **673 W**

**Critical insight:** If the airframe is designed specifically for solar endurance (ultra-light, ultra-high L/D), cruise power can be brought below 500 W. With 5 m² of GaAs cells producing 1,450 W in direct sun, **solar power can exceed cruise power by a factor of 2–3 in summer conditions.**

The excess power charges batteries for night flight.

### 4.4 The Day/Night Energy Balance

This is the critical calculation for perpetual flight. The drone must store enough energy during the day to fly through the night.

**UK latitude (51°N) — Summer solstice (June 21):**
- Daylight: ~16.5 hours
- Effective solar hours (>50% peak irradiance, accounting for low sun angles): ~12 hours
- Average irradiance during effective hours: ~700 W/m² (UK is not the Sahara)
- Solar power from 5 m² GaAs: 5 × 0.29 × 700 = **1,015 W average**
- Energy collected in 12 hours: 1,015 × 12 = **12,180 Wh**
- Cruise power needed 24h: 700 W × 24 = **16,800 Wh**
- **Deficit: 4,620 Wh** — perpetual flight NOT achievable at sea level at 51°N even in summer with this design

**But at altitude (above cloud layer, 3,000–5,000 m):**
- Irradiance above clouds: ~1,000–1,100 W/m² (no cloud attenuation)
- Effective solar hours: 14+ hours (higher altitude sees sunrise/sunset earlier/later)
- Average irradiance: 900 W/m²
- Solar power: 5 × 0.29 × 900 = **1,305 W average**
- Energy in 14 hours: **18,270 Wh**
- Night cruise at lower power (cooler air, can slow down): 500 W × 10 h = **5,000 Wh**
- Battery needed: 5,000 Wh at 250 Wh/kg = **20 kg of batteries**
- **Surplus: 18,270 – (700×14 + 500×10) = 18,270 – 14,800 = 3,470 Wh surplus**

**At altitude, in summer, perpetual flight is achievable in the UK.**

**Winter (December, 51°N):**
- Effective solar hours: ~5–6 hours
- Average irradiance above clouds: 600–800 W/m²
- Solar energy: ~4,500–5,200 Wh
- Night is ~17 hours: 500 × 17 = 8,500 Wh
- Day flight: 700 × 7 = 4,900 Wh
- Total needed: 13,400 Wh
- **Deficit: ~8,000 Wh — perpetual flight NOT possible in UK winter**

**Conclusion:** Solar perpetual flight at UK latitude is feasible from roughly April to September at altitude but not in winter. This defines a seasonal operational envelope.

### 4.5 Pseudo-Satellite (HAPS) Programs

**Airbus Zephyr:**
- Wingspan: 25 m. Weight: 75 kg. Altitude: 21,000 m (stratosphere).
- World record: 64 days 18 hours continuous flight (2022, broken from earlier 25-day record).
- Uses amorphous silicon cells and lithium-sulphur batteries.
- Flies above all weather in the stratosphere.
- Powered entirely by solar. Proves the concept works.
- Programme has experienced crashes (2022 crash on a Zephyr S after the record flight, 2023 losses). Ongoing development.

**BAE Systems PHASA-35:**
- Wingspan: 35 m. UK-developed solar HAPS.
- First flight: February 2020 at Woomera, Australia.
- Designed for persistent surveillance and communications relay at 20,000 m.
- Solar cells + batteries for day/night operation.
- Directly relevant to the comms relay constellation concept, but at stratospheric altitude.

**Facebook/Meta Aquila (cancelled):**
- Wingspan: 42 m. Weight: ~400 kg. Aimed for 18,000 m.
- Solar-powered internet relay. Cancelled in 2018 after flight test crashes. Technology transferred to Airbus.

**SoftBank HAPSMobile / Sunglider:**
- Wingspan: 78 m. Solar HAPS for communications relay.
- Partnership with AeroVironment.
- Stratospheric flight tests conducted 2020–2023.

### 4.6 Relevance to MEDIUM Tier

The MEDIUM tier (25–50 kg, 3–5 m wingspan) has less wing area:
- Usable solar area: 1–2.5 m²
- Solar power (GaAs): 290–725 W peak
- Cruise power for 40 kg drone at L/D 25: ~300–450 W
- Marginal — solar might sustain cruise in peak sun but cannot store enough for night
- MEDIUM tier is too heavy per unit wing area for perpetual solar flight

### 4.7 Summary for This Project

| Parameter | Value |
|---|---|
| TRL | 9 for solar cells; 7–8 for solar UAV systems (Zephyr, PHASA-35) |
| Power to MEDIUM tier | 300–700 W peak (marginal for cruise, no night capability) |
| Power to LARGE tier | 700–1,900 W peak (can exceed cruise in summer) |
| Weight penalty on drone | 2.5–7.5 kg (cells + encapsulant + wiring) |
| Ground infrastructure | None during flight (landing/charging station only) |
| Weather limitation | Cloud below drone is fine; above drone blocks sun. UK winter insufficient |
| Range/altitude | Best at high altitude (above weather). No range limit |
| Cost estimate | £5k–£50k for cells depending on technology |
| Regulatory | No additional regulatory burden beyond normal UAV rules |
| Demonstrated on drone? | Yes — Zephyr (64 days), PHASA-35, many others |
| Comms relay relevance | Excellent — the proven approach for persistent airborne platforms |

---

## 5. AERIAL REFUELING / BATTERY SWAP

### 5.1 Mid-Air Battery Swap

Concept: A "tanker" drone rendezvouses with the "mission" drone and transfers a fresh battery pack.

**Status:** This is largely theoretical for practical systems. The challenges are severe:

- **Precision docking in turbulence:** Two aircraft must fly in formation within centimetres of each other and mechanically dock. Military aerial refuelling between manned aircraft with trained pilots and rigid booms is already difficult. Between autonomous UAVs in variable weather, this is extremely challenging.
- **Speed matching:** Both drones must fly at the same speed and altitude while the mechanical transfer occurs.
- **Mechanism weight and complexity:** The docking/transfer mechanism adds weight and failure modes to both aircraft.

**Research:**
- Several academic groups have published concepts (MIT, Georgia Tech).
- No successful demonstration of autonomous mid-air battery swap between fixed-wing UAVs as of 2025.

**Assessment:** TRL 2–3. Not viable for the near term.

### 5.2 DARPA Gremlins

DARPA's Gremlins program demonstrated airborne launch and recovery of small UAVs (Dynetics X-61A) from a C-130 aircraft:

- A mechanical arm extends from the C-130's cargo ramp.
- The X-61A drone flies into the capture mechanism.
- Once captured, it is reeled into the aircraft for maintenance and relaunch.
- Successful demonstrations in 2021.

This is not power transfer but rather full recovery and relaunch. The principle could be adapted: a large "mothership" drone carries batteries and recovers/relaunches small drones. However, the mothership would need to be much larger than the mission drones and would itself have endurance limits.

### 5.3 Automated Ground-Based Battery Swap

This is far more practical and directly relevant to the project's airbase/ground station concept:

**How it works:**
1. Drone approaches ground station autonomously (precision landing using RTK GPS + vision).
2. Lands on a platform or cradle.
3. Robotic mechanism removes spent battery pack and inserts fresh one.
4. Drone takes off again.
5. Spent battery charges at the station (from mains, solar, or generator).

**Swap time:** 2–5 minutes achievable with purpose-built mechanism.

**Companies and systems:**
- **Skycharge:** Automated drone charging pads (contact charging, not swap).
- **WiBotic:** Wireless inductive charging for drones (land on pad, charge wirelessly). 300 W–1.5 kW. Takes 30–60 minutes to charge — too slow for persistent operations.
- **Skysense (acquired by Asylon):** Autonomous landing pad with contact charging.
- **H3 Dynamics (DRONEBOX):** Autonomous drone nest with battery swap. Demonstrated commercial operations.
- **Airobotics (Optimus):** Fully autonomous drone-in-a-box with automatic battery swap. Used commercially in mining, oil and gas. Swap time: ~3 minutes.

For the project, designing the ground station with automated fast-charging or battery swap is highly practical. With a 5-minute swap and 1-hour flight endurance, the drone is on-station 92% of the time. With two drones alternating, 100% coverage is maintained.

### 5.4 Relay System

Rather than powering one drone indefinitely, use a relay approach:

- Drone A provides comms relay coverage.
- When Drone A's battery is low, Drone B launches from the ground station.
- Drone B climbs to altitude and takes over relay duty.
- Drone A returns, lands, and gets battery swapped/recharged.
- Repeat indefinitely.

**Handover time:** 10–20 minutes (Drone B climbing to altitude while Drone A descends). During handover, both drones can relay simultaneously (no coverage gap if network protocol handles handover gracefully).

**Minimum fleet for continuous coverage:** 2 drones per station (one flying, one charging). 3 drones provides redundancy for maintenance.

This is the approach used by most commercial persistent surveillance companies.

### 5.5 Summary for This Project

| Parameter | Mid-Air Swap | Ground Battery Swap | Relay System |
|---|---|---|---|
| TRL | 2–3 | 7–8 (Airobotics operational) | 8–9 (proven concept) |
| Complexity | Extreme | Moderate | Low |
| Coverage gap | None (in theory) | 5–20 min per swap | 0 (with 2+ drones) |
| Weight penalty | 5–10 kg mechanism | 0 (mechanism on ground) | 0 |
| Ground infrastructure | None | Automated swap station | Swap station + spare drone |
| Weather limitation | Severe (precision flying) | Landing in wind is the limit | Same as single drone ops |
| Cost estimate | R&D phase | £20k–£100k per station | Station + extra drone(s) |
| Comms relay relevance | Not practical | Good for lower altitude ops | Excellent — proven approach |

---

## 6. HYBRID APPROACHES

### 6.1 Solar + Battery (Day/Night Cycle) — The Zephyr Model

As analysed in Section 4.4, this is the proven approach for perpetual flight:

- Solar charges batteries during the day while simultaneously powering flight.
- Batteries sustain flight at night.
- Works at UK latitude from April to September at altitude.
- Requires ultra-light, high-AR airframe designed around the energy balance.

**For the LARGE tier concept:** Designing a purpose-built solar-endurance variant of the LARGE tier airframe, with lower wing loading and higher aspect ratio, could achieve multi-day flights in summer. This would be a specialised variant, not the general-purpose LARGE tier platform.

### 6.2 Solar + Laser (Night Top-Up)

Concept: Solar sustains daytime flight. At night (or in winter), ground-based laser beaming supplements battery power.

- Addresses the winter gap where solar alone cannot sustain 24-hour flight.
- The laser system only needs to provide the deficit (~500 W for a few hours), not the full cruise power.
- Ground station with laser beaming would serve as a "recharging zone" the drone orbits over periodically during the night.

**Challenges:** The same weather limitations apply — laser cannot penetrate cloud, and nights in UK winter are often cloudy. The drone at 3,000–5,000 m is likely above the cloud layer, but the ground station is below it.

**Assessment:** The weather limitation undermines the value proposition. If you could guarantee clear skies at night, this would be excellent. In the UK, you cannot.

### 6.3 Solar + Ground Station Relay

The most practical hybrid:

- Solar-equipped LARGE tier drones fly extended missions (6–24 hours depending on season).
- Automated ground stations with battery swap enable indefinite relay coverage.
- Solar extends each sortie, reducing the number of landing/swap cycles.
- In summer, a single drone might fly 2–3 days before needing to land.
- In winter, the relay system maintains coverage when solar is insufficient.

### 6.4 Hydrogen Fuel Cell

Not power transfer per se, but dramatically extends endurance by replacing battery energy storage:

**Energy density comparison:**
| Technology | Wh/kg (system level, including tank/BOP) |
|---|---|
| Li-ion battery | 200–270 |
| Li-S battery (emerging) | 350–500 (projected) |
| H2 fuel cell + compressed H2 (350 bar) | 500–800 |
| H2 fuel cell + compressed H2 (700 bar) | 800–1,200 |
| H2 fuel cell + liquid H2 | 1,500–2,500 (but cryogenic) |

**3–5x the energy density of lithium batteries** at system level for compressed H2.

**Companies:**
- **Intelligent Energy (UK, Loughborough):** Market leader in UAV fuel cells. 650 W, 800 W, 2.4 kW modules. Powers several commercial and military drones. Flight times of 2–3 hours on small drones demonstrated repeatedly.
- **HES Energy (Singapore):** Develops H2 fuel cells for drones. Claims 3.5-hour flight time on multi-rotor drones.
- **Doosan Mobility Innovation (South Korea):** DS30 fuel cell drone — 2-hour flight time with 5 kg payload. Commercially available. DM30 fuel cell powerpack: 2.6 kW.
- **Honeywell (formerly Ballard UAV):** Developing fuel cells for Group 2/3 UAVs.
- **MMC UAV (China):** HyDrone — hydrogen-powered industrial drone, 4+ hour flight time claimed.

**For the LARGE tier:**
- A 2–5 kW fuel cell system would weigh 5–15 kg.
- 5 kg of compressed H2 at 350 bar: ~1,700 Wh/kg at cell level, but system overhead brings it to ~800 Wh/kg → 4,000 Wh usable.
- At 700 W cruise: **5.7 hours of flight** from 5 kg of H2.
- With 10 kg of H2: **11.4 hours**.
- Combined with solar: In summer, the fuel cell provides baseload + night power, solar covers daytime. Flight times of 24–48+ hours become feasible.

**H2 Infrastructure:**
- Green hydrogen from electrolysis is increasingly available.
- Compressed gas storage at the ground station.
- Refuelling takes 5–10 minutes (much faster than battery charging).
- Safety: H2 is flammable but dissipates rapidly in open air. Outdoor operations are manageable.

### 6.5 Solar + Hydrogen Fuel Cell

This is potentially the optimal combination for the comms relay constellation:

- **Solar cells on wing** (3–5 m², GaAs): 700–1,450 W in direct sun.
- **H2 fuel cell** (2–5 kW capacity): Provides power during night, cloud cover, and supplemental power during high-demand phases (climb, heavy payload operation).
- **Small Li-ion battery** (2–5 kg): Buffer for transients, peak loads, and as backup.
- **Daytime:** Solar powers cruise + charges battery + fuel cell idles.
- **Night/cloud:** Fuel cell takes over.

**Endurance estimate:**
- 10 kg H2 provides ~8,000 Wh at system level.
- Night cruise: 500 W × 10 hours (summer) = 5,000 Wh from fuel cell.
- Day cruise from solar: ~12 hours at zero fuel cell consumption.
- **Total endurance: 2–3 days in summer**, limited by H2 supply.
- With a ground station for H2 refuel and relay: **indefinite coverage**.

### 6.6 Summary of Hybrid Approaches

| Approach | Endurance | Complexity | Best Season | Comms Relay Suitability |
|---|---|---|---|---|
| Solar + battery | 12h–multi-day (summer) | Low | Apr–Sep | Good in summer, poor in winter |
| Solar + laser | 24h+ (clear nights) | High | Year-round (clear weather) | Poor (UK weather) |
| Solar + ground relay | Indefinite (with fleet) | Moderate | Year-round | Excellent |
| H2 fuel cell only | 4–12 hours | Moderate | Year-round | Good (needs ground station) |
| Solar + H2 + ground relay | Indefinite | Moderate-High | Year-round | Optimal |

---

## 7. TECHNOLOGY COMPARISON TABLE

| Technology | TRL | Power to MEDIUM (W) | Power to LARGE (W) | Drone Weight Penalty (kg) | Ground Infrastructure | Weather Limit | Max Range/Alt | Cost per Station | Regulatory Burden | Demonstrated? | Comms Relay Score (1-10) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Laser beaming | 5–6 | 500–2,000 | 500–3,000 | 2–10 | Major (£200k–£2M) | Severe | 5–10 km | £200k–£2M | High | Yes (LaserMotive 2012) | 3 |
| Microwave beaming | 4–5 | 50–300 | 200–1,000 | 1–5 | Very major (£1M–£10M) | Minimal | 5–10 km | £1M–£10M | Very high | Yes (MHI 2015, short range) | 2 |
| Tethered power | 8–9 (multi) / 3 (FW) | 1,000–3,000 | 2,000–5,000 | 5–50 (cable) | Moderate (£30k–£100k) | Wind | 50–500 m | £30k–£100k | Lower | Yes (Elistair) | 1 |
| Solar on-wing | 7–8 | 300–700 peak | 700–1,900 peak | 2.5–7.5 | None in flight | Cloud above drone | No limit | £5k–£50k | None additional | Yes (Zephyr 64 days) | 8 |
| Ground battery swap | 7–8 | N/A (relay) | N/A (relay) | 0 | Station (£20k–£100k) | Landing weather | No limit | £20k–£100k | Standard | Yes (Airobotics) | 7 |
| Relay fleet | 8–9 | N/A | N/A | 0 | Station + spare drones | Standard | No limit | £50k–£200k | Standard | Yes (commercial ops) | 8 |
| H2 fuel cell | 6–7 | 500–2,500 | 1,000–5,000 | 5–15 (cell + H2) | H2 storage + refuel | None | No limit | £20k–£80k | Moderate (H2 safety) | Yes (Intelligent Energy, Doosan) | 7 |
| Solar + H2 + relay | 5–6 (integrated) | 800–3,000 | 1,500–6,000 | 8–20 | Station + H2 | Cloud limits solar only | No limit | £50k–£150k | Moderate | Partial (subsystems proven) | 9 |

---

## 8. COMPARISON ANALYSIS

### Power Beaming (Laser and Microwave) — Verdict: Not Primary Approach

Both laser and microwave power beaming are technically fascinating but face fundamental obstacles for the comms relay constellation:

**Laser:** UK weather kills reliability. A drone at 3,000–5,000 m altitude will frequently be above cloud that blocks line-of-sight to the ground laser. Even in clear conditions, atmospheric losses at the slant ranges involved (5–10 km) reduce efficiency significantly. The technology is proven at short range on small drones but has not been demonstrated at the scale and range needed.

**Microwave:** All-weather capability is the right characteristic for the UK, but the physics of beam spread make it impractical. Delivering meaningful power (>500 W) to a drone at 5 km altitude requires a transmit antenna 10–30 m in diameter transmitting tens of kilowatts. The ground infrastructure cost and regulatory challenges are extreme. Additionally, conformal rectennas on the wing surface would conflict with solar cell coverage.

Both technologies may have niche roles — laser for clear-weather top-up, microwave for short-range high-power scenarios — but neither is suitable as the primary endurance extension approach.

### Tethered Power — Verdict: Wrong Application

Tethered systems are proven and effective for low-altitude multirotor operations (surveillance, temporary comms). They are categorically incompatible with fixed-wing flight at 3,000–5,000 m. The cable weight alone exceeds the drone's maximum takeoff weight. This technology is irrelevant for the comms relay constellation.

However, the automated ground station concepts from tethered system companies (Elistair's expertise in persistent operations) are informative for the relay station design.

### Solar — Verdict: Primary Power Source

Solar is the only technology demonstrated to enable multi-week continuous flight (Zephyr, 64 days). The physics work for the LARGE tier: with 5 m² of GaAs cells, peak power exceeds cruise requirements. The weight penalty is modest (3–7 kg). No ground infrastructure is needed during flight.

The limitation is seasonal and geographic — UK winter does not provide enough solar energy for 24-hour flight. This is a hard physical constraint that cannot be engineered around; it must be designed around.

### Hydrogen Fuel Cell — Verdict: Key Enabler for All-Season Operation

H2 fuel cells bridge the gap that solar cannot fill: night hours, winter months, cloudy days. With 3–5x the energy density of batteries, a 10 kg H2 supply extends flight time from hours to days. UK-based Intelligent Energy is a global leader, making supply chain access straightforward.

The combination of solar + H2 fuel cell gives the best single-drone endurance across all seasons.

### Relay Fleet — Verdict: Essential for True Indefinite Coverage

No single power technology guarantees indefinite flight in all conditions. A relay fleet with automated ground stations provides the operational guarantee: if a drone must land (weather, mechanical issue, fuel exhaustion), another takes over. This is how real-world persistent surveillance systems operate.

---

## 9. RECOMMENDATION FOR THE PERSISTENT COMMS RELAY CONSTELLATION

### Primary Approach: Solar + Hydrogen Fuel Cell + Relay Fleet

The recommended architecture layers three technologies:

**Layer 1 — Solar (primary daytime power):**
- 4–5 m² of high-efficiency GaAs or advanced silicon cells on the LARGE tier upper wing surface.
- Provides 800–1,500 W in direct sun (above cloud at altitude).
- Sustains cruise + charges buffer battery during the day.
- Weight: 3–5 kg. Cost: £10k–£30k per airframe.

**Layer 2 — Hydrogen fuel cell (night/winter/cloud power):**
- 1.5–3 kW PEM fuel cell (Intelligent Energy or similar).
- 5–10 kg compressed H2 at 350 bar.
- Provides 5–12 hours of non-solar flight.
- Combined with solar: 2–4 day endurance per sortie in summer; 8–16 hours in winter.
- Weight: 8–15 kg (cell + H2 + tank). Cost: £15k–£40k per airframe.

**Layer 3 — Relay fleet with automated ground stations:**
- Minimum 3 LARGE tier drones per coverage zone (1 flying, 1 on standby, 1 in maintenance).
- Automated ground station with H2 refuelling and battery top-up.
- Seamless handover protocol: replacement drone climbs to altitude before on-station drone descends.
- Provides indefinite coverage guarantee regardless of season or weather.
- Ground station cost: £50k–£150k.

### Operational Concept — Seasonal Modes

**Summer mode (April–September):**
- Single drone flies 2–4 days continuously (solar + H2).
- Ground station refuels H2 during brief landing (~15 minutes).
- Drone relay only needed every 2–4 days.
- High availability with minimal fleet usage.

**Winter mode (October–March):**
- Drone flies 8–16 hours per sortie (H2 dominant, solar supplementary).
- Relay fleet rotates every 8–12 hours.
- All 3 drones in the fleet cycle through: fly → refuel → standby → fly.
- 100% coverage maintained.

### Why Not Power Beaming?

For this specific application — persistent comms relay over the UK at 3,000–5,000 m — power beaming is not recommended as a primary technology because:

1. UK weather makes laser unreliable (cloud between ground and drone).
2. Microwave requires impractical ground infrastructure at the required range.
3. Solar + H2 + relay achieves the goal with proven subsystems at reasonable cost.
4. The FSO laser tracking capability from the comms system could potentially support a laser power top-up as a future enhancement, but this should not be relied upon for the baseline design.

### Development Roadmap

| Phase | Milestone | Technologies |
|---|---|---|
| Phase 1 | Battery-only LARGE tier flights, 1–2 hours | Li-ion battery |
| Phase 2 | Solar integration, extend to 4–8 hour flights | Solar + Li-ion |
| Phase 3 | H2 fuel cell integration, extend to 24+ hours | Solar + H2 + Li-ion buffer |
| Phase 4 | Automated ground station, relay operations | Full system |
| Phase 5 | Persistent constellation (3+ drones, indefinite) | Fleet operations |

### Key Supplier Contacts

- **Solar cells:** SunPower (IBC cells), MicroLink Devices (thin-film GaAs, successor to Alta Devices technology), Oxford PV (perovskite-silicon tandem — UK based, emerging)
- **H2 fuel cells:** Intelligent Energy (Loughborough, UK — 20 minutes from project area by road), Doosan Mobility Innovation
- **Ground station automation:** Custom design drawing on Airobotics and Elistair concepts
- **H2 supply:** BOC (UK industrial gas supplier), green H2 from electrolysis at ground station (long-term)

### Cost Summary for Initial Persistent Constellation (1 coverage zone)

| Item | Quantity | Cost Estimate |
|---|---|---|
| LARGE tier airframe (solar-optimised variant) | 3 | £15k–£30k each |
| Solar cell installation per airframe | 3 | £10k–£30k each |
| H2 fuel cell system per airframe | 3 | £15k–£40k each |
| Automated ground station with H2 storage | 1 | £50k–£150k |
| Comms relay payload per airframe | 3 | £5k–£15k each |
| **Total** | | **£140k–£495k** |

This is a significant investment but within range of a serious development programme. The costs decrease with subsequent coverage zones as the airframe and ground station designs are proven.

---

### Key References and Further Reading

1. PowerLight Technologies (formerly LaserMotive) — laser power beaming demonstrations
2. W. C. Brown, "The History of Power Transmission by Radio Waves," IEEE Trans. MTT, 1984 — foundational microwave power beaming work
3. Airbus Zephyr programme — zephyr.airbus.com — solar HAPS world record
4. BAE Systems PHASA-35 — UK solar HAPS development
5. Intelligent Energy — intelligent-energy.com — UK fuel cell manufacturer
6. Elistair — elistair.com — tethered drone systems
7. DARPA Gremlins programme — aerial recovery demonstrations
8. Mitsubishi Heavy Industries microwave power beaming demonstration (2015)
9. Airobotics Optimus — automated drone-in-a-box with battery swap
10. J. McSpadden and J. Mankins, "Space Solar Power Programs and Microwave Wireless Power Transmission Technology," IEEE Microwave Magazine, 2002
