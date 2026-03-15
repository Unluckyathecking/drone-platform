# Drone-Based Pest Control and Invasive Species Management

## Platform Reference: Mini Fixed-Wing UAV (2–4m Wingspan, 4kg Payload)

---

## 1. Aerial Pest Detection and Monitoring

### Overview

Thermal and multispectral imaging from UAVs has become a standard tool for wildlife population surveys. Fixed-wing platforms are particularly suited to this work because they cover large areas efficiently compared to multirotors.

### Payload Modules

| Component | Typical Model | Weight | Power | Notes |
|---|---|---|---|---|
| Thermal/IR camera | FLIR Vue Pro R 640 | 113g | 3.7W | 640x512 resolution, radiometric output |
| RGB high-res camera | Sony A7R IV / Phase One P3 | 580–665g | ~5W | 42–100MP, geotagged stills |
| Dual-sensor gimbal | Gremsy Pixy U | 350–500g | 10W | 2-axis stabilized, accommodates both sensors |
| Onboard compute (AI inference) | NVIDIA Jetson Orin Nano | 60g | 7–15W | Real-time animal detection at edge |
| Data storage | 1TB NVMe SSD | 30g | 2W | Raw thermal + RGB capture |

**Total payload estimate:** 1.1–1.4kg (well within 4kg limit)

### Mission Type

- **Search pattern**: Parallel transect lines (lawnmower pattern) at 80–120m AGL
- **Survey speed**: 15–22 m/s for fixed-wing
- **Overlap**: 70% forward, 50% side for photogrammetric reconstruction
- **Typical coverage**: 200–500 ha per flight (90-minute endurance)

### AI-Based Counting and Tracking

- Convolutional neural networks (YOLO, Faster R-CNN) trained on thermal signatures detect warm-bodied animals against cooler ground
- Population density estimation uses distance sampling or total count methods
- Repeat surveys at intervals build population trend data
- Thermal imaging is most effective at dawn/dusk when thermal contrast between animals and ground is highest

### Feasibility for Mini-UAV

**High feasibility.** This is the most mature drone-based conservation application. The payload is light, power draw is modest, and fixed-wing platforms excel at covering large survey areas. The main constraint is camera resolution vs altitude -- 640x512 thermal sensors require flying at 60–100m AGL to reliably detect rabbit-sized animals.

### Existing Projects and Companies

- **Wildlife Drones (Australia)** -- radio-tracking wildlife from fixed-wing UAVs
- **Conservation Drones** (Lian Pin Koh, Serge Wich) -- open-source platform for tropical wildlife surveys
- **RSPB / Natural England** -- thermal drone surveys for ground-nesting birds and deer census
- **Scion Research (NZ)** -- thermal detection of possums for Department of Conservation
- **University of Adelaide** -- automated kangaroo and feral goat counts from drone thermal imagery
- **PrecisionHawk** -- large-area wildlife surveys using fixed-wing Lancaster platform

---

## 2. Precision Bait Delivery

### Overview

Aerial bait delivery is an established conservation technique. New Zealand's Department of Conservation has conducted aerial 1080 (sodium fluoroacetate) drops from helicopters since the 1950s for possum and rat control, covering over 500,000 ha annually. Transitioning from helicopters to UAVs offers lower cost, higher precision, and reduced human exposure.

### Current Practice: New Zealand Aerial 1080 Program

- Helicopters fitted with underslung bait hoppers drop cereal-based bait pellets containing 1080
- Sow rate: typically 2–4 kg/ha
- Pellet size: 6–12g each
- Used on offshore islands and mainland sanctuaries for rat, possum, and stoat control
- Project Island Song, Antipodes Island, and Whenua Hou (Codfish Island) are notable successes -- restoring populations of native birds like kakapo

### Payload Modules for UAV Bait Delivery

| Component | Specification | Weight | Notes |
|---|---|---|---|
| Bait hopper | 3–4L capacity, servo-actuated gate | 400–600g (empty) | Gravity-fed or auger-driven |
| Bait payload | Cereal pellets, 2–4 kg/ha sow rate | Up to 3kg per sortie | Limits coverage to ~1 ha per sortie at 3kg/ha |
| Spreader mechanism | Spinning disc or venturi tube | 200–400g | Adjustable spread width 5–15m |
| GPS-triggered release | Flight controller integration | Included in autopilot | Activates spreader at waypoints |
| Flow rate sensor | Optical or weight-based | 50g | Verifies actual sow rate |

**Total payload estimate:** 3.5–4.0kg (at payload capacity limit)

### Mission Type

- **Delivery route**: Pre-planned parallel lines with GPS-triggered spreader activation
- **Altitude**: 20–40m AGL for accurate placement
- **Speed**: 10–15 m/s (slower than survey for even distribution)
- **Coverage per sortie**: 0.75–1.5 ha at 3kg/ha sow rate (limited by payload capacity)
- **Operational model**: Multiple short sorties from a base station with rapid reload

### Precision Targeting vs Broadcast Spreading

The key advantage of UAV delivery over helicopter broadcast is precision:

- **Geofenced exclusion zones** around waterways, non-target habitat, and human areas
- **Variable rate application** -- higher density in known pest hotspots (informed by prior thermal survey)
- **Reduced bait wastage** -- potentially 40–60% less bait required compared to broadcast
- **Closed-loop feedback** -- combine with prior survey data to target only occupied areas

### Regulatory Requirements

- **Pesticide application license**: Required in most jurisdictions. In the UK, this falls under the Plant Protection Products Regulations. In NZ, the Resource Management Act governs aerial 1080 use.
- **Aerial application permit**: Separate from the drone flight authorization. Operators need certification equivalent to manned aerial applicator licenses.
- **Environmental impact assessment**: Usually required for toxin-based bait programs
- **Buffer zones**: Mandated distances from waterways, dwellings, and non-target areas
- **Bait dye and biomarkers**: Required in many jurisdictions to identify treated bait

### Feasibility for Mini-UAV

**Moderate feasibility, with caveats.** The 4kg payload limit severely restricts per-sortie coverage. A helicopter can carry 500–1000kg of bait; the UAV carries 3kg. This makes the platform suitable for:
- Small island eradications (under 50 ha)
- Precision top-up drops in specific zones after helicopter broadcast
- Urban-adjacent or sensitive areas where helicopter operations are impractical
- Research trials and proof-of-concept

For large-area operations (thousands of hectares), this platform would serve as a complement to, not a replacement for, helicopter operations.

### Existing Projects and Companies

- **ZIP (Zero Invasive Predators), NZ** -- developing drone-based bait and trap delivery for Predator Free 2050
- **Department of Conservation, NZ** -- trialing drone delivery of brodifacoum bait on small islands
- **Island Conservation (US)** -- drone-based rodenticide delivery on tropical islands
- **Boffa Miskell (NZ)** -- environmental consulting firm integrating drone bait delivery into eradication planning
- **University of Auckland** -- research into optimal bait sow rates from UAV platforms

---

## 3. Seed Bombing / Habitat Restoration

### Overview

After invasive species removal, rapid revegetation prevents reinvasion and erosion. Drone-based seed dispersal is a fast-growing sector, with several well-funded companies operating at scale.

### Seed Ball Technology

Seed balls (or seed pods) encapsulate native seeds in a clay/nutrient matrix:
- Diameter: 10–25mm
- Weight: 5–15g each
- Composition: seeds + clay + biochar + mycorrhizal inoculant + nutrients
- Survival advantage: protection from predation, moisture retention, nutrient provision

### Payload Modules

| Component | Specification | Weight | Notes |
|---|---|---|---|
| Seed pod hopper | 4–6L capacity, pneumatic or gravity feed | 300–500g (empty) | Similar to bait hopper design |
| Seed pod payload | 10–25mm diameter pods | Up to 3.5kg per sortie | ~230–700 pods per load |
| Dispersal mechanism | Pneumatic launcher or gravity drop | 200–400g | Pneumatic gives better spacing |
| GPS-triggered release | Waypoint-based dispensing | Included in autopilot | Species-specific planting zones |
| Species-sorting hopper | Multi-compartment hopper | 500–800g | Plant right species in right microhabitat |

**Total payload estimate:** 3.5–4.0kg at capacity

### Mission Type

- **Delivery route**: Waypoint-based with species-specific drop zones
- **Altitude**: 10–30m AGL
- **Speed**: 8–12 m/s
- **Density**: 1,000–10,000 seeds/ha depending on species and restoration goals
- **Coverage**: 0.5–2 ha per sortie at typical densities

### Feasibility for Mini-UAV

**High feasibility for targeted restoration; low for broadscale reforestation.** The mini-UAV is well-suited to:
- Post-eradication revegetation of small islands
- Riparian corridor planting
- Steep terrain inaccessible to ground crews
- Targeted infill planting in gaps

For large-scale reforestation (thousands of hectares), the commercial operators listed below use much larger platforms.

### Existing Companies and Projects

- **DroneSeed (US)** -- now part of **Mast Reforestation**. Used heavy-lift multirotors for post-wildfire reseeding. First FAA-approved company for drone swarm reforestation.
- **AirSeed Technology (Australia)** -- proprietary seed pods with 25+ species. Claims 40,000 pods per day per drone. Operates in Australia and internationally.
- **BioCarbon Engineering / Dendra Systems (UK)** -- AI-mapped planting using fixed-wing survey drones paired with multirotor seed delivery drones. Has planted in Australia, UK, and Southeast Asia.
- **Flash Forest (Canada)** -- pneumatic seed pod delivery, targeting 1 billion trees by 2028
- **Lord Howe Island Board (Australia)** -- post-rat-eradication revegetation using drone seed dispersal
- **Parihaka Restoration Project (NZ)** -- small-scale drone seeding trial after possum control

---

## 4. Invasive Plant Detection

### Overview

Multispectral and hyperspectral imaging can identify invasive plant species by their unique spectral signatures -- different chlorophyll content, leaf structure, and water content produce distinct reflectance profiles that cameras can detect even when species look similar in visible light.

### Payload Modules

| Component | Typical Model | Weight | Power | Notes |
|---|---|---|---|---|
| Multispectral camera | MicaSense RedEdge-P | 174g | 4.5W | 5 discrete bands (blue, green, red, red edge, NIR) |
| Hyperspectral sensor | Headwall Nano-Hyperspec | 680g | 9W | 270 bands, 400–1000nm |
| Downwelling light sensor | MicaSense DLS 2 | 35g | 0.5W | Calibrates for ambient light changes |
| LiDAR (optional) | Livox Mid-360 | 265g | 9W | Canopy structure, biomass estimation |
| Onboard processing | Jetson Orin Nano | 60g | 15W | Real-time NDVI computation |

**Total payload estimate (multispectral):** 0.5–0.8kg
**Total payload estimate (hyperspectral + LiDAR):** 1.0–1.5kg

### Key Analyses

- **NDVI (Normalized Difference Vegetation Index)**: Basic vegetation health. Invasives often have different NDVI values from native species.
- **Red Edge Position**: Sensitive to chlorophyll concentration differences between species
- **Spectral Unmixing**: Separates mixed pixels into component species
- **Object-Based Image Analysis (OBIA)**: Classifies species by texture, shape, and spectral properties combined
- **Machine Learning Classification**: Random forest, SVM, or deep learning on spectral data achieves 85–95% accuracy for many invasive species

### Targeted Herbicide Application

Crossing over from precision agriculture, drone-based spot-spraying of herbicides on detected invasive plants is now operational:

| Component | Specification | Weight | Notes |
|---|---|---|---|
| Spray tank | 2–3L capacity | 200g (empty) + 2–3kg liquid | Herbicide solution |
| Spray nozzles | 2–4 flat-fan nozzles | 100g | Variable rate, drift-reducing |
| Pump | 12V diaphragm pump | 150g | 2–4 L/min flow rate |
| Spray controller | PWM-based, GPS-triggered | 80g | Activates only over identified targets |

**Note:** Spray application from fixed-wing aircraft requires careful nozzle design to manage airspeed-induced drift. Multirotor platforms are generally preferred for precision spot-spraying, but fixed-wing can work for strip application.

### Mission Type

- **Survey (detection)**: Parallel transects at 60–120m AGL, same as ecological survey
- **Spot-spray (treatment)**: Low-altitude passes at 5–15m AGL over identified targets (better suited to multirotor)
- **Two-phase workflow**: Fixed-wing surveys to map invasive stands, then targeted ground or multirotor treatment

### Feasibility for Mini-UAV

**High feasibility for detection, moderate for treatment.** The fixed-wing platform excels at large-area invasive plant mapping. Spray application is more challenging because:
- Fixed-wing speed increases drift risk
- Low-altitude flying at 5–15m AGL over vegetation is higher risk
- Treatment is better suited to multirotor or ground-based follow-up

The optimal workflow is: fixed-wing survey to detect and map invasive stands, then export target coordinates to ground crews or multirotor spray drones.

### Existing Companies and Projects

- **Dendra Systems (UK)** -- end-to-end invasive plant detection and management from drones
- **Aerobuoy (NZ)** -- wilding pine detection in New Zealand using multispectral drone imagery
- **Environmental Mapping and Surveying (Australia)** -- lantana and rubber vine detection from UAV multispectral
- **XAG (China)** -- agricultural spray drones adapted for invasive plant management
- **Rantizo (US)** -- precision herbicide application from UAV, licensed in 22 US states
- **CSIRO (Australia)** -- research into hyperspectral detection of invasive grasses (buffel grass, gamba grass)
- **Landcare Research / Manaaki Whenua (NZ)** -- wilding conifer detection and mapping across Canterbury high country

---

## 5. Marine Invasive Species

### Overview

Aerial surveys of shallow marine environments detect invasive species that are visible through clear water. The most prominent example is the Crown-of-Thorns Starfish (COTS) on the Great Barrier Reef, where drone surveys have supplemented diver-based monitoring programs.

### Crown-of-Thorns Starfish (COTS)

- COTS are large (25–80cm diameter) and distinctly colored (purple-blue), making them visible from altitude in clear water
- Outbreaks can kill 40–90% of coral in affected reefs
- Traditional monitoring relies on manta-tow diver surveys, which are slow and expensive

### Payload Modules

| Component | Typical Model | Weight | Power | Notes |
|---|---|---|---|---|
| RGB camera (high-res) | Sony A7R IV | 580g | 5W | Polarizing filter to reduce surface glare |
| Circular polarizer filter | Custom 77mm filter | 20g | -- | Critical for cutting water surface reflection |
| Multispectral camera | MicaSense RedEdge-P | 174g | 4.5W | Water-penetrating bands (blue, green) |
| Bathymetric LiDAR (emerging) | Miniaturized green-wavelength LiDAR | 800g–1.5kg | 15W | Penetrates 1–3m water depth |
| Onboard AI | Jetson Orin Nano | 60g | 15W | Real-time COTS/lionfish detection |

**Total payload estimate:** 0.8–2.3kg depending on configuration

### Detection Techniques

- **Polarized imaging**: Circular polarizing filters reduce surface glare, allowing imaging of shallow reef (0.5–5m depth in clear water)
- **Blue/green channel analysis**: Water absorbs red light rapidly; blue and green channels penetrate deepest
- **AI object detection**: CNN models trained on COTS images achieve 80–90% detection rates at 10–30m altitude over clear water
- **Temporal differencing**: Repeat surveys reveal COTS movement patterns and outbreak front progression

### Mission Type

- **Search pattern**: Reef-following transects at 10–30m AGL
- **Timing**: Calm conditions essential (Beaufort 0–2), low sun angle preferred for water penetration
- **Speed**: 8–15 m/s
- **Coverage**: 50–200 ha per flight depending on reef geometry
- **Challenge for fixed-wing**: Reef surveys require slow flight and tight turns around reef features. A high-aspect-ratio fixed-wing may struggle with this compared to a multirotor.

### Feasibility for Mini-UAV

**Moderate feasibility.** Fixed-wing platforms can cover large reef areas efficiently for broad survey work, but the requirement for slow, maneuverable flight over complex reef structures favors multirotors for detailed survey. A practical workflow:
- Fixed-wing for large-area screening (identifying which reef sections have COTS)
- Multirotor or diver follow-up for detailed assessment and treatment
- Fixed-wing for monitoring outbreak fronts across tens of kilometers of reef

Additional constraint: operations over water require either floatation recovery systems or water-resistant airframes in case of ditching.

### Existing Projects and Companies

- **QUT (Queensland University of Technology)** -- COTSBot autonomous underwater vehicle and complementary drone surveys on the Great Barrier Reef
- **AIMS (Australian Institute of Marine Science)** -- integrating drone aerial surveys into the Long-Term Monitoring Program
- **Great Barrier Reef Marine Park Authority** -- trialing drone surveys for COTS early detection
- **NOAA / University of Miami** -- drone surveys for lionfish density in Caribbean reefs
- **Reef Ecologic** -- commercial drone reef survey services in Townsville, QLD
- **Allen Coral Atlas** -- satellite + drone remote sensing for global reef monitoring (not species-specific but related)

---

## 6. Regulatory Framework

### UK Environment Agency Regulations

#### Drone Flight Authorization
- **CAA (Civil Aviation Authority)** governs all drone flight in the UK
- Operations require an **Operational Authorization** for BVLOS (Beyond Visual Line of Sight) -- essential for fixed-wing survey/delivery missions
- The **Open Category** (under 25kg, VLOS only) is too restrictive for most conservation missions
- The **Specific Category** (SORA risk assessment) is the typical pathway for conservation UAV operations
- The **Certified Category** may apply for autonomous operations in populated areas

#### Pesticide and Bait Application
- **The Plant Protection Products Regulations 2012** govern pesticide use in the UK
- Aerial application of pesticides is **banned by default** under Regulation (EC) No 1107/2009 (retained in UK law post-Brexit), with exemptions available where:
  - No viable alternative exists
  - The pesticide is specifically approved for aerial application
  - A specific exemption is granted by the relevant authority (HSE in England)
- The **Health and Safety Executive (HSE)** issues the exemptions and maintains the approved product list
- Operators need a **PA1/PA6** (or equivalent) certificate for pesticide application
- Additional **aerial application endorsement** may be required

#### 1080 and Other Vertebrate Toxins
- **1080 (sodium fluoroacetate) is not approved for use in the UK** -- unlike NZ and Australia
- Anticoagulant rodenticides (brodifacoum, bromadiolone) are regulated under UK Biocidal Products Regulation
- Aerial delivery of rodenticides would require special authorization from HSE and likely DEFRA

#### Wildlife Protection
- **Wildlife and Countryside Act 1981** protects non-target species
- Operations must avoid disturbance to Schedule 1 protected species (e.g., certain raptors, red squirrels)
- **Natural England / NatureScot / NRW** issue licenses for operations that might disturb protected species
- Seasonal restrictions apply near nesting sites (typically March–August)
- An **Ecological Impact Assessment** is typically required

### Regulatory Requirements by Application

| Application | Key Regulations | Licenses Needed | Lead Authority |
|---|---|---|---|
| Wildlife survey (imaging only) | ANO 2016, CAA Operational Authorization | BVLOS authorization, landowner permission | CAA, Natural England |
| Bait delivery (rodenticide) | BPR, HSE authorization | Aerial application exemption, pest control license | HSE, DEFRA |
| Seed dispersal | Minimal pesticide regulation | BVLOS authorization only | CAA |
| Herbicide spraying | PPP Regulations, aerial spray ban | Aerial application exemption, PA1/PA6 | HSE, CAA |
| Marine survey | ANO 2016, Marine and Coastal Access Act 2009 | BVLOS over water, marine license if deploying anything | CAA, MMO |

### General Best Practices for Regulatory Compliance

1. **Pre-operational environmental assessment** for all pesticide/bait operations
2. **Non-target species mitigation plan** -- detailing how non-target animals will be protected
3. **Buffer zones** -- minimum distances from water bodies, dwellings, public rights of way
4. **Spill containment** -- protocols for payload failure or crash during bait/spray operations
5. **Traceability** -- GPS logging of all dispensed materials (bait, seed, herbicide) for regulatory audit
6. **Insurance** -- public liability and environmental liability coverage specific to aerial application
7. **Community consultation** -- often a planning requirement for aerial toxin operations

---

## Summary: Application Feasibility Matrix

| Application | Payload Weight | Feasibility | Coverage/Sortie | Maturity |
|---|---|---|---|---|
| Thermal/IR wildlife survey | 1.1–1.4kg | **High** | 200–500 ha | Operational |
| Precision bait delivery | 3.5–4.0kg | **Moderate** (small areas) | 0.75–1.5 ha | Trialing |
| Seed pod dispersal | 3.5–4.0kg | **High** (small areas) | 0.5–2 ha | Operational |
| Invasive plant detection | 0.5–1.5kg | **High** | 100–400 ha | Operational |
| Herbicide spot-spray | 2.5–3.5kg | **Low** (fixed-wing) | 0.5–1 ha | Prefer multirotor |
| Marine species survey | 0.8–2.3kg | **Moderate** | 50–200 ha | Research/Trial |

### Recommended Multi-Mission Approach

The greatest value from a single fixed-wing platform comes from a **modular payload bay** supporting rapid swap between:

1. **Survey configuration** (thermal + multispectral + RGB) -- 1.0–1.5kg -- for detection and monitoring
2. **Delivery configuration** (hopper + spreader) -- up to 4.0kg -- for bait or seed dispensing

This allows a two-phase operational model:
- **Phase 1**: Survey flights to detect, count, and map pest populations or invasive plant stands
- **Phase 2**: Targeted delivery flights to the identified hotspots only

This detect-then-treat approach minimizes bait/herbicide usage, reduces non-target impacts, and produces the data trail regulators require.

---

*Sources and references current to early 2025. Regulatory frameworks may have been updated since. Always verify current regulations with the relevant authority before operational deployment.*
