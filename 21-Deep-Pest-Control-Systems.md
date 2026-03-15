# Drone-Based Pest Control and Invasive Species Management Systems for Mini Fixed-Wing UAV

## Research Document: Technical Analysis for a 2-4m Wingspan, 4kg Payload, ArduPilot Platform

---

## 1. AERIAL BAIT DELIVERY SYSTEMS

### 1.1 New Zealand Department of Conservation 1080 Bait Drops

**History and Context.** Sodium fluoroacetate (compound 1080) has been New Zealand's primary tool for controlling introduced mammalian predators since the 1950s. It targets possums (*Trichosurus vulpecula*), ship rats (*Rattus rattus*), and Norway rats (*Rattus norvegicus*), with secondary poisoning killing stoats (*Mustela erminea*) that scavenge on poisoned carcasses. Stoats, being obligate carnivores, will not directly consume bait pellets.

In 2024, there were 65 aerial 1080 operations conducted across New Zealand, with 47 pest control research projects ongoing. The New Zealand EPA publishes annual reports on aerial 1080 use, providing transparency on methodology and outcomes.

**Methodology.** Cereal-based pellets containing 0.15% (1500 ppm) sodium fluoroacetate are broadcast from aircraft (historically helicopters) using GPS-guided flight paths. Application rates are typically 1-2 kg of bait per hectare, equating to approximately 3 grams or less of actual 1080 toxin per hectare. At a pellet weight of roughly 6 grams, this translates to 160-830 baits per hectare depending on sowing rate. Dual-application protocols have emerged as a refinement: an initial broadcast targets the majority of the population, followed by a second application 3-4 weeks later to catch juveniles and sub-dominant animals that were excluded from bait by dominant individuals.

**Effectiveness.** Aerial 1080 remains the most effective method for controlling introduced predators over large, remote, and rugged terrain. Possum kill rates regularly exceed 95%, and ship rat populations are suppressed by 90-99% in treatment areas. The key limitation is that 1080 does not achieve permanent eradication on the mainland; populations recover within 2-5 years, necessitating repeated operations.

**Transition to Drones.** The Predator Free 2050 initiative has driven innovation. ZIP (Zero Invasive Predators) has operated in South Westland since 2017, progressively scaling from 2,300 ha to the 100,000 ha Predator Free South Westland Project. Their operations employ a combination of aerial broadcast, "trickle sowing," hand-laying, and drone-laying techniques. ZIP developed the H2Lure, a refillable device with a hydrogen-generating cell that pressurizes bait delivery at a controlled rate for up to 12 months without servicing.

### 1.2 Brodifacoum Bait Drops for Island Rat Eradication

**South Georgia (2011-2015).** The South Georgia Heritage Trust's Habitat Restoration Project represents the largest island rodent eradication ever attempted. Brown rats (*Rattus norvegicus*) and house mice (*Mus musculus*) were targeted across 3,500 km2. The operation was conducted in three phases using helicopters:

- Phase 1 (2011): Initial area equal in size to Macquarie Island
- Phase 2 (2013): Continued coverage
- Phase 3 (2015): Final 940 km2

Bait comprised hard, extruded cereal pellets containing 25 ppm brodifacoum for rats and 50 ppm for mice. The first drop applied 12 kg of bait per hectare; the second drop applied 8 kg/ha. Pellets were approximately 2 grams each (10mm diameter), yielding roughly one bait per two square metres at 12 kg/ha. The operation required almost 450 flying hours. By July 2017, 28 months after baiting concluded, no surviving rodents were detected, and the islands were declared rat-free.

**Macquarie Island (2011).** The Macquarie Island eradication targeted rats, mice, and rabbits simultaneously using brodifacoum bait at similar application rates. At the time of South Georgia's success, the Phase 1 area (comparable to Macquarie Island) confirmed the methodology's validity. These operations used exclusively helicopter-based delivery.

**Application Rates Summary by Target Species:**
- Rats (maintenance/control): 1-2 kg/ha of 1080 cereal bait
- Rats (island eradication, brodifacoum): 12 kg/ha first drop, 8 kg/ha second drop
- Possums + rats combined (NZ aerial 1080): 1-5 kg/ha depending on terrain and target density
- Mice (eradication): Higher concentration bait (50 ppm brodifacoum) at similar weight rates

### 1.3 Bait Pod Designs

**Envico Technologies Precision Bait Deployment System (PBS).** Envico, based in New Zealand, has developed the most advanced drone-specific bait delivery technology. Their Precision Bait Deployment System uses biodegradable bait pods manufactured from wood and bioplastic compound filament. Key specifications:

- Pods break open upon ground impact
- Landing accuracy: 0-2.5 metres of target, even through thick bush canopy
- The system links the drone's autopilot with GNSS-aided GPS positioning and computer-based trajectory calculations
- Can deliver various bait types and quantities to specific locations at programmed densities

**World First Achievement.** In January 2019, Envico conducted the world's first island eradication of vertebrate pests by drone on Seymour Norte (184 ha) in the Galapagos Islands. Using two heavy-lift drones, approximately 1,500 kg of Bell Laboratories conservation bait was dropped across Seymour Norte and Mosquera Islet in just two days. Roughly 48% of North Seymour's area was also hand-baited by 30+ park rangers. The islands were subsequently declared rat-free.

### 1.4 Spreader Mechanisms

**Centrifugal Disc Spreaders.** The dominant mechanism for broadcast bait and seed delivery. Seeds or pellets are deposited from a hopper onto a rotating disc driven by a BLDC motor. A servo motor controls the latch/gate opening via mobile app or autopilot command. Spreading range is adjustable up to 30 metres. The EFT EPS200 Pro offers 12m effective swath width with IP6 rating.

**Key Commercial Systems:**
- **CFR-innovations UGS**: Carbon fiber, weight-efficient plastic, and aluminum construction. Adjustable spread range up to 30m. Designed to minimize impact on drone flight stability.
- **EFT EPS250/EPS270**: 50L and 70L capacity respectively, compatible with DJI and other agricultural drone platforms. Centrifugal disc design for uniform distribution.
- **XAG JetSeed**: Centrifugal granule spreading system integrated into XAG agricultural drones.

**Conveyor/Gravity-Fed Hoppers.** Simpler than centrifugal systems; suitable for trickle and cluster baiting rather than broadcast. The Envico system uses a gravity-fed approach with GPS-triggered pod release for precision placement rather than broadcast spreading.

**Fixed-Wing Considerations (4kg payload budget).** For a 2-4m wingspan fixed-wing with 4kg payload, a lightweight centrifugal spreader (approximately 0.5-1.0 kg for the mechanism) leaves 3.0-3.5 kg for bait. At 2 kg/ha application rate, this provides coverage of 1.5-1.75 hectares per sortie. For island eradication rates (12 kg/ha), this is severely limiting at approximately 0.3 ha per sortie, making multiple sorties or a relay system essential. The fixed-wing advantage is speed and endurance for broadcast over linear transects.

### 1.5 GPS-Triggered Release vs Broadcast

**Broadcast Application** remains standard for large-area pest control. GPS-guided flight paths ensure complete coverage with appropriate overlap. The flight management system records all treated areas in real-time.

**Precision/GPS-Triggered Release** is Envico's innovation. The autopilot calculates release timing based on ground speed, altitude, wind conditions, and target coordinates. This enables:
- Cluster baiting: dropping multiple baits at discrete GPS points (e.g., near detected pest sign)
- Trickle sowing: releasing baits at intervals along a flight path
- Targeted delivery: releasing pods at specific coordinates identified from prior survey flights

For a fixed-wing ArduPilot platform, GPS-triggered release is implemented via ArduPilot's servo/relay outputs controlled by mission waypoint commands (DO_SET_SERVO, DO_SET_RELAY). The mission planner defines release points, and the autopilot triggers the mechanism at each waypoint.

---

## 2. TARGET SPECIES DETECTION FROM AIR

### 2.1 Thermal Imaging for Mammal Detection

**Technology Overview.** Thermal (LWIR/MWIR) cameras detect infrared radiation emitted by endothermic animals, producing thermal contrast against the cooler background environment. Standard drone thermal sensors use 640x512 pixel radiometric sensors (e.g., FLIR Vue Pro R, DJI Zenmuse H20T).

**Detection Ranges and Minimum Animal Sizes by Altitude:**

| Altitude | Pixel GSD (640x512, 13mm lens) | Minimum Detectable Animal | Practical Application |
|---|---|---|---|
| 25m | ~3cm | Rabbit (1.5kg+) | Optimal for small mammal surveys; risk of disturbance |
| 40m | ~5cm | Rabbit/hare | Good compromise for lagomorphs |
| 60m | ~8cm | Fox, small deer, feral pig | Standard survey altitude; minimal disturbance |
| 80m | ~10cm | Deer, cattle-sized | High-altitude broad survey |
| 120m | ~15cm | Large ungulates only | Maximum practical altitude for medium mammals |

**Key Findings from Research:**
- Medium-bodied mammals (15-350 kg) are readily identified in automated processes with good image quality
- Small mammals (less than or equal to 15 kg) present significant automated identification challenges even with high-quality thermal imagery
- k-nearest-neighbor classification achieved 93.3% accuracy for wild rabbits at 3-10m altitude (very low)
- European hare population counts have been successfully conducted at 60m altitude with 7 m/s flight speed
- A flight altitude of 25m was identified as optimal for rabbit detection resolution without causing flight disturbance

**Species-Specific Considerations:**
- **Rabbits**: Best detected at 25-40m altitude; warren detection possible through thermal signatures of occupied burrows
- **Feral pigs**: Detectable at 60-80m; strong thermal signature due to body mass
- **Deer**: 40-120m altitude range; morning surveys yield higher detection when animals are in open
- **Foxes**: 40-60m; challenging due to smaller body size and nocturnal habits requiring dawn/dusk surveys

### 2.2 AI Models for Species Classification

**Architectures in Use:**
- **YOLOv8/YOLOv6**: Real-time object detection, with Distant-YOLO (D-YOLO) variant optimized for small, distant targets in thermal imagery
- **EfficientNet/ResNet**: Used by Wildlife Insights platform for camera trap and aerial image classification
- **Deep learning approaches**: F1-score of 0.87 achieved for automated rabbit counting from thermal drone imagery

**Fusion Approaches.** Research published in *Scientific Reports* (2023) demonstrated that fusion of visible and thermal images significantly improves automated detection and classification accuracy compared to either modality alone. Simultaneous thermal + RGB video recording enables thermal detection followed by RGB species confirmation.

**Human-Inspired Deep Learning.** A 2025 paper in *Methods in Ecology and Evolution* presented methods to locate and classify both terrestrial and arboreal animals in thermal drone surveys, addressing the challenge of animals at varying heights and in different canopy structures.

### 2.3 Existing Datasets

- **LILA BC (Labeled Information Library of Alexandria: Biology and Conservation)**: Primary repository for conservation AI training data. Hosts the Conservation Drones dataset with annotated wildlife in drone/aerial images. Also hosts the New Zealand Wildlife Thermal Imaging dataset with 121,190 thermal videos from The Cacophony Project.
- **BIRDSAI**: Long-wave thermal infrared dataset with 48 real and 124 synthetic aerial TIR videos of animals and humans in Southern Africa.
- **iNaturalist/iWildCam**: ~500k labeled photos of ~8k species; primarily handheld camera photos but useful for transfer learning.
- **Aerial Wildlife Image Repository (AWIR)**: Published in *Database* (Oxford Academic, 2024), specifically designed for drone-age AI monitoring.

### 2.4 Population Density Estimation from Transect Flights

**Methodology.** Parallel transects spaced 200m apart with 10% side overlap between neighboring frames. Flights at 60m altitude, 7 m/s speed. Distance sampling theory (Buckland et al.) applied to thermal detections to estimate density, corrected for detection probability which varies with altitude, vegetation, and animal behavior.

**Detection Effectiveness.** Thermal drones detected individuals at 0.70 +/- 0.45 individuals/hour compared to ground-based methods at 0.17 +/- 0.22 individuals/hour --- a 4x improvement in detection rate.

**Cost Breakeven.** Drone survey costs were initially 4x higher than traditional methods but had lower operational costs per area (2.7x) and per animal detected (3.2x), with financial return achieved after surveying 740 ha or detecting 38 animals.

### 2.5 Nesting Colony and Warren Detection

**Seabird Colonies.** UAV-mounted thermal sensors can detect occupied burrows through heat signatures of resident chicks. Automated thermal counts were 9.3% higher than manual counts and took approximately 5% of the time. Deep learning applied to RGB imagery can estimate colony size of surface-nesting seabirds.

**Rabbit Warrens.** Satellite-based detection using open-access imagery has been tested for mapping rabbit warrens at landscape scale. Drone thermal surveys at night provide higher resolution detection, with deep learning approaches achieving F1-scores of 0.87 for individual rabbit counting.

### 2.6 Time-of-Day Optimization

- **Dawn/Dusk**: Optimal for thermal contrast (large delta between animal body temperature ~37-39C and cooling ground ~5-15C). Also coincides with crepuscular activity peaks for many target species (rabbits, deer, foxes).
- **Post-Dusk (30-60 minutes after sunset)**: Best for arboreal fauna surveys; ground has cooled but animals retain heat signatures.
- **Morning**: Higher detection rates for deer (most individuals present and active) compared to afternoon.
- **Midday**: Worst conditions; solar heating of ground, rocks, and vegetation creates thermal clutter, dramatically reducing signal-to-noise ratio.

### 2.7 Fixed-Wing Platform Implications

A fixed-wing UAV covers more area per unit time than a multirotor, making it ideal for transect-based population surveys. The ArduPilot mission planner can define parallel survey lines with appropriate spacing. However, fixed-wing minimum speed (typically 15-25 m/s for a 2-4m wingspan aircraft) is higher than the 7 m/s used in many thermal survey studies, reducing pixel dwell time and potentially impacting detection. Mitigations include: higher-resolution thermal sensors, continuous video recording rather than still capture, and AI post-processing of video frames.

---

## 3. SEED BOMBING AND REFORESTATION

### 3.1 Seed Ball Technology

Seed balls (also called seed bombs) consist of seeds encased in a matrix of clay, compost, and nutrients. The clay outer layer protects against predation and desiccation; the compost provides initial nutrition for germination. Typical composition:
- 5 parts dry red or brown clay
- 1 part compost/worm castings
- Seeds appropriate to target ecosystem
- Optional: mycorrhizal inoculant, biochar

Diameter: typically 10-25mm depending on seed size. Weight: 2-10 grams per ball.

### 3.2 Reference Companies and Their Technologies

**Mast Reforestation (formerly DroneSeed, US).** Founded 2015 in Seattle. Uses swarms of 5 drones to reseed 25-50 acres (10-20 ha) per day on fire-ravaged terrain. Payload capacity of 26 kg. Focus on post-wildfire restoration in the western United States.

**AirSeed Technologies (Australia).** Claims to plant 40,000 seed pods per day. Developed proprietary seed pod technology with an engineered mixture designed to maximize germination. Claims to be 25x faster than traditional planting. Trials showed 80% germination success and 75% seed growth success.

**Dendra Systems (UK, Oxford-based).** Achieved 120 seed pods per minute deployment rate. Highly modular drone dispersal systems customizable for different species. Focus on flexibility across diverse reforestation contexts.

**Other Notable Companies:**
- Dronecoria: Open-source 3D-printable design, 8 kg payload, 10 ha/hour coverage rate
- CO2 Revolution: Claims 10x cost-effectiveness vs traditional planting
- Seedcopter: Similar cost-effectiveness claims

### 3.3 Drop Rate and Dispersal Patterns

- Deployment rates: 120 seed pods/minute (Dendra, AirSeed, Lord of the Trees)
- Land coverage: 40-80 ha/day (standard), up to 10 ha/hour (Dronecoria)
- For a fixed-wing with 4 kg payload at ~5g per seed ball: approximately 800 seed balls per sortie
- At 2,500 seed balls per hectare (typical for reforestation): approximately 0.3 ha per sortie
- At 1,000 seed balls per hectare (lower density for hardy species): approximately 0.8 ha per sortie

### 3.4 Germination Rates: Aerial vs Hand-Planted

The evidence is mixed but improving:
- AirSeed/CO2 Revolution trials: 80% germination, 75% growth success (self-reported, limited independent validation)
- Academic review (Australian Plants Society): Drone seeding germination rates are generally lower than hand-planted seedlings, but the cost differential means more seeds can be deployed to compensate
- Key factors affecting germination: seed ball moisture retention, soil contact quality, predator protection, species selection

### 3.5 Cost per Hectare

| Method | Cost per Hectare (approximate) |
|---|---|
| Manual tree planting | $2,000-$8,000/ha |
| Helicopter aerial seeding | $500-$2,000/ha |
| Drone seed bombing | $200-$1,000/ha (claimed) |

Companies claim 10-25x cost reduction, but independent validation is limited. The primary saving is in labor; drone operations require 2-3 operators vs large ground crews.

### 3.6 Hopper Design for 4kg Payload Fixed-Wing

A cylindrical gravity-fed hopper with motor-driven disc release is the most practical design. Open-source designs exist with 50-ball capacity and 9L hopper volume (up to 10 kg). For a 4 kg payload budget:
- Mechanism weight: ~0.5-0.8 kg
- Usable payload: ~3.2-3.5 kg of seed balls
- At 5g per ball: ~640-700 balls per sortie
- A servo-controlled gate with variable opening controls release rate
- ArduPilot integration: PWM-controlled servo on the gate, triggered by mission waypoints or set to continuous release during survey legs

---

## 4. TARGETED HERBICIDE APPLICATION

### 4.1 Two-Pass Approach: Survey then Treat

**Pass 1 --- Survey Flight.** The aircraft carries a multispectral camera (e.g., MicaSense RedEdge-P with five narrow bands + panchromatic, achieving 2cm GSD at 60m). Images are processed to generate:
- NDVI maps (Normalized Difference Vegetation Index): healthy vegetation appears bright; stressed or different species have distinct signatures
- False-color composites using NIR/Red Edge bands: sensitive to chlorophyll, nitrogen, water content
- Species classification maps using trained AI models

Processing can be completed within 24 hours using Pix4D or similar photogrammetry software, generating a prescription map with georeferenced weed locations and recommended treatment rates.

**Pass 2 --- Treatment Flight.** The prescription map is loaded into the mission planner. The drone (or a different, spray-equipped platform) follows GPS waypoints, activating spray nozzles only over identified invasive plant locations. Three dosage levels (weak, moderate, strong infection density) can be programmed.

### 4.2 Spot-Spraying Technology

Product savings near 50% compared to broadcast spraying, with economic savings of approximately $13.42/acre from reduced chemical use. The "downwash" effect from multirotor rotors enhances deposition on target plants. For a fixed-wing, spray deposition relies on gravity and forward speed; lower altitudes (3-5m above canopy) improve targeting accuracy.

### 4.3 Target Invasive Species and Herbicide Selection

| Species | Detection Method | Herbicide | Notes |
|---|---|---|---|
| Japanese knotweed (*Fallopia japonica*) | RGB + NIR; distinctive large leaves and bamboo-like stems | Glyphosate (foliar spray, late summer) | UK Schedule 9 listed; legal obligation to prevent spread |
| Giant hogweed (*Heracleum mantegazzianum*) | RGB identification of large umbels and deeply lobed leaves | Glyphosate (spring, before flowering) | Phototoxic sap; drone application avoids operator exposure |
| Rhododendron (*R. ponticum*) | Multispectral; evergreen canopy distinct in winter NIR | Glyphosate (stem injection or foliar) | Major UK woodland pest; aerial foliar spray in accessible areas |
| Himalayan balsam (*Impatiens glandulifera*) | RGB; distinctive pink flowers, riparian corridors | Glyphosate (pre-flowering) | Annual; effective if treated before seed set |
| Floating pennywort (*Hydrocotyle ranunculoides*) | NDVI anomaly on water surface | Approved aquatic herbicides (2,4-D amine) | Waterway species; drift management critical |

### 4.4 Spray Drift Management

**Critical Factors:**
- 6% of targeted volume is lost for each 1m increase in application height
- Smaller droplets increase buffer zone distance to >30m
- A three-stage adjustment strategy (nozzle selection, pressure, altitude) can reduce drift ratio by 89.18% and shorten the 90% drift distance to 3.36m

**Nozzle Selection:** Coarser droplets (VMD >250 microns) are mandated for aerial application in most jurisdictions. Flat-fan nozzles are standard on multirotor drones, but larger-orifice nozzles are limited by pump/battery constraints.

**Buffer Zones:** Mandatory around watercourses, hedgerows, and sensitive habitats. UK requirements specify minimum distances based on product label and application method.

**Fixed-Wing Specific Considerations:** Forward speed (15-25 m/s) significantly affects droplet trajectory and drift potential. Lower flight altitudes (2-5m above target) are critical. Spray booms must be designed for the wing's aerodynamic profile to minimize turbulent entrainment of droplets.

### 4.5 NDVI and Spectral Imaging

Sensors with NIR (770-890nm) and Red Edge (670-780nm) bands are more sensitive to physiological and biochemical properties (chlorophyll, nitrogen, water content) and can discriminate between native and invasive species. The MicaSense RedEdge-P achieves 2cm resolution at 60m, sufficient for individual plant identification in many cases.

---

## 5. INSECT PEST MANAGEMENT

### 5.1 Sterile Insect Technique (SIT)

**Principles.** Mass-reared male insects are sterilized using ionizing radiation (gamma or X-ray) and released to mate with wild females. Mated females produce non-viable offspring, causing population decline over successive generations. The technique is species-specific and leaves no chemical residue.

**IAEA/FAO Programs:**
- **Tsetse fly** (*Glossina* spp.): SIT programs across sub-Saharan Africa to combat trypanosomiasis (sleeping sickness). Historically aerial release from light aircraft.
- **Mediterranean fruit fly** (*Ceratitis capitata*): Eradicated from parts of California and Central America. Aerial release at scale from aircraft.
- **Mosquitoes** (*Aedes aegypti*, *Aedes albopictus*): Targets for Zika, dengue, chikungunya control. Mosquitoes are fragile and do not disperse more than 100m in their lifetime, making ground release impractical for large areas and high-altitude aircraft release damaging.

### 5.2 IAEA Drone Release Mechanism

Developed in partnership with WeRobotics (Swiss-American non-profit). Key specifications of the prototype tested in Brazil (April 2018):

- Capacity: 50,000 sterile mosquitoes per flight
- Coverage: 20 hectares in 10 minutes
- Drone weight: less than 10 kg total
- Holding canister height: maximum 5 cm (deeper causes bottom-layer crushing)
- Mortality: less than 10% through chilling, transport, and aerial release
- Temperature management: mosquitoes kept cool during transport to maintain competitiveness
- Development target: increase capacity to 150,000 mosquitoes per flight

The testing confirmed that radiation-sterilized mosquitoes released from drones remained competitive to mate with wild females.

### 5.3 Biological Control Agent Release

**Trichogramma Parasitoid Wasps.** The most established drone-deployed biocontrol agent. *Trichogramma* spp. parasitize lepidopteran eggs, controlling European corn borer, spruce budworm, and other moths.

- Deployment rate: 400,000 host eggs per hectare
- Coverage: 20 hectares per hour
- Operation time: 0.5 hours per deployment cycle
- Delivery mechanisms: Biodegradable capsules containing parasitized eggs, released via a fork-and-rotating-hammer mechanism with photoelectric switch counting
- Countries with active programs: Austria, Germany, France, Italy, Canada
- Canadian research: Tested against corn borers in cornfields and spruce budworm in Quebec forests

**Other Biological Control Agents:**
- Codling moth SIT: Successful pilot programs in NZ, Canada, and US
- Pink bollworm SIT: Effective in US cotton
- False codling moth SIT: South African citrus orchards

### 5.4 Pheromone Deployment

A UAV (octocopter) retrofitted with a novel extrusion device delivers pheromone-loaded paraffin at regular intervals during flight. SPLAT (Specialized Pheromone & Lure Application Technology) is an inert matrix infused with pheromones and/or pesticides, applied as dollops from drones. Efficacy is confirmed by measuring mating disruption through reduced male moth trap catches.

### 5.5 Fixed-Wing SIT/Biocontrol Considerations

A fixed-wing platform is well-suited for SIT release due to its ability to cover large areas efficiently. The 4 kg payload could carry a release mechanism plus insect containers. Key challenges:
- Forward speed may affect release uniformity and insect survival
- Container design must prevent insect damage during the vibration and acceleration environment of fixed-wing flight
- ArduPilot DO_SET_SERVO commands can trigger release mechanisms at programmed intervals or GPS points

---

## 6. MARINE AND COASTAL PEST CONTROL

### 6.1 Crown-of-Thorns Starfish (COTS) Detection and Treatment

COTS (*Acanthaster planci*) are responsible for approximately 40% of all coral loss on the Great Barrier Reef over the past 30 years.

**Robotic Detection and Treatment:**
- **COTSbot**: Autonomous underwater vehicle that navigates reefs, detects COTS using computer vision, and delivers lethal bile salt injection. AI detection accuracy: 99.4%.
- **RangerBot**: Smaller (15 kg, 75 cm), cheaper, more versatile successor to COTSbot. 8-hour battery life. Can also monitor coral bleaching, water quality, pollution, and siltation.
- **AI Systems**: YOLOv6 optimized for embedded underwater drone systems achieves Precision 0.927, Recall 0.903, mAP@50 0.938. DCGAN (Deep Convolutional Generative Adversarial Network) augments training data for rare COTS encounters.

**Aerial Drone Role.** Surface-flying drones provide broad-area reef surveillance to identify COTS outbreak hotspots, directing underwater robots or divers to priority treatment areas. Multispectral imaging from altitude can assess coral health indicators across large reef systems.

### 6.2 Kelp Forest Health Assessment

**Mapping Technology.** Kelp-O-Matic is an open-source tool widely adopted for drone-based kelp forest mapping, enabling First Nations, NGOs, and coastal partners to independently monitor kelp canopy extent and area. California has conducted the largest marine resource-focused drone surveys in its history to map kelp dynamics.

**Methodology:** RGB imagery from standard drone cameras, processed with automated classification algorithms to distinguish kelp canopy from water surface. Repeated surveys track changes in canopy area over time.

### 6.3 Drone-Based Water Sampling for eDNA

**Environmental DNA (eDNA)** technology enables detection of invasive aquatic species from water samples. Organisms shed DNA through skin cells, mucus, and excrement; this DNA persists in water and can be extracted and amplified.

**Drone Collection.** UAVs with bleachable collection equipment avoid DNA contamination. The drone descends to the water surface, collects a sample (typically 1-5 litres), and returns to base for laboratory analysis.

**Autonomous Systems.** The DOT-NM Autosampler (developed by NatureMetrics and Dartmouth Ocean Technologies) collects up to 9 consecutive 5-litre eDNA samples per deployment. Configurable timing and volume; depth ratings for 20m, 200m, and 2000m. Can be deployed from vessels, moorings, drones, or AUVs.

**Applications:** Early detection of invasive crab larvae, mussel veligers, and other marine invasive species. High sensitivity for rare and endangered species identification.

### 6.4 Fixed-Wing Coastal Applications

A fixed-wing platform excels at broad-area coastal surveys: reef health mapping, kelp canopy assessment, and identifying locations for targeted water sampling. However, water sampling itself requires hover capability (multirotor or VTOL). A practical concept of operations uses the fixed-wing for survey/detection and a multirotor for intervention.

---

## 7. CASE STUDIES AND ECONOMICS

### 7.1 Cost Comparisons

**Aerial Bait Delivery:**

| Platform | Cost per Operation | Coverage Rate | Limitations |
|---|---|---|---|
| Helicopter (NZ 1080) | $50-150/ha (including bait) | 100-500 ha/hour | Pilot cost, weather windows, minimum area ~100 ha |
| Large drone (Envico ENV50) | $30-100/ha (estimated) | 200 kg bait/hour; 20-40m altitude | Mechanical reliability; battery/fuel limits |
| Small drone (ENV10) | $50-200/ha (estimated) | 13-97 kg bait/hour; 10-15 min flights | Limited payload; frequent reloading |
| Ground crew (bait stations) | $200-500/ha | 2-5 ha/day per worker | Labor-intensive; terrain-limited |

**Agricultural Spraying:**

| Platform | Cost per Hectare | Coverage Rate |
|---|---|---|
| Helicopter | $40-75/ha ($18/acre) | 50-200 ha/hour |
| Agricultural spray drone | $10-20/ha | 4-20 ha/hour |
| Ground-based tractor sprayer | $15-30/ha | 5-15 ha/hour |

**Reforestation:**

| Method | Cost per Hectare |
|---|---|
| Manual planting (seedlings) | $2,000-8,000 |
| Helicopter aerial seeding | $500-2,000 |
| Drone seed bombing | $200-1,000 (claimed) |

**Thermal Wildlife Survey:**

Drone surveys have initial costs 4x higher than traditional methods but lower per-area operational costs (2.7x) and per-animal-detected costs (3.2x). Financial return after 740 ha surveyed or 38 animals detected.

### 7.2 Coverage Rates by Mission Type

| Mission Type | Fixed-Wing Coverage | Multirotor Coverage |
|---|---|---|
| Thermal wildlife survey (60m AGL) | 50-100 ha/hour | 10-30 ha/hour |
| Multispectral vegetation mapping | 80-200 ha/hour | 15-40 ha/hour |
| Broadcast bait delivery | Limited by payload (3-4 kg) | 5-20 ha/hour (depending on rate) |
| Precision bait pod delivery | 10-30 ha/hour (GPS-triggered) | 5-15 ha/hour |
| Seed ball dispersal | 20-50 ha/hour | 10-20 ha/hour |
| Herbicide spot-spraying | Not ideal (forward speed) | 4-20 ha/hour |

### 7.3 Success Rates of Drone-Based Programs

- **Galapagos Seymour Norte (2019)**: 100% rat eradication confirmed. World's first drone-based island eradication.
- **Pacific Island Conservation**: Drone technologies are "expediting Pacific island conservation, eradicating invasive rats at speed" (2024 report).
- **SIT Mosquito Programs**: Less than 10% mortality through drone release process; competitive mating confirmed.
- **Trichogramma Programs**: Operational across multiple European countries with proven efficacy in corn borer suppression.
- **FitoStinger (EU H2020)**: Drone-based pest control for European trees using 75% less pesticide than other drones and 90% less than spray cannons.

### 7.4 ROI Calculations

For a small fixed-wing platform (estimated $5,000-15,000 build cost with ArduPilot):
- **Survey missions**: ROI positive after ~740 ha of thermal surveys vs hiring traditional survey teams
- **Bait delivery**: ROI depends on comparison platform; replaces ground crew work in steep/remote terrain where helicopters are prohibitively expensive for small areas (<100 ha)
- **Seed bombing**: At $200-1,000/ha drone vs $2,000-8,000/ha manual, ROI is rapid if the platform operates regularly
- **For farms >2.27 ha**: The cost-benefit ratio favors drone adoption over traditional methods

---

## 8. REGULATORY FRAMEWORK (UK FOCUS)

### 8.1 Wildlife and Countryside Act 1981

The Wildlife and Countryside Act 1981 is the primary legislation for wildlife protection in Great Britain. Key provisions relevant to drone-based pest control:
- **Section 1**: Protection of wild birds --- any pest control operation must avoid non-target bird species
- **Section 9**: Protection of certain wild animals --- operations near protected species require licensing
- **Schedule 9**: Lists non-native species that are illegal to release or allow to escape (includes many target invasive plants)
- The Act requires the Health and Safety Executive (HSE) to consult relevant nature conservation authorities when permitting pesticide application "in" or "close to" conservation areas

### 8.2 Control of Pesticides Regulations 1986

Made under Part III of the Food and Environment Protection Act 1985 (FEPA). These regulations:
- Prescribe approvals required before any pesticide may be sold, stored, supplied, used, or advertised
- Control aerial application of pesticides (which legally includes drone application)
- Require that aerial application operators obtain consent from the water authority if applying pesticide for aquatic weed control or near watercourses

### 8.3 Natural England Licensing

Natural England issues wildlife licenses for activities that would otherwise be offenses under the Wildlife and Countryside Act. For drone-based pest control:
- **General Licenses**: Cover routine pest control of listed species (certain corvids, wood pigeons, etc.) without individual application
- **Individual/Project Licenses**: Required for operations that may disturb protected species (e.g., drone flights near Schedule 1 bird nesting sites, bat roosts)
- **Class Licenses**: For specific categories of work by authorized persons

### 8.4 CAA Regulations for Agricultural Drone Operations

**Key Requirements (as of 2025-2026):**
- An **Aerial Spraying Permit** is required every time pesticide is applied from the air, including all drone applications
- Operators must obtain CAA authorization to fly (Operational Authorization under the Open, Specific, or Certified category depending on operation risk)
- The drone must be fitted with "best available technology" to reduce spray drift
- Maps and grid references of treatment areas must be submitted
- Processing time: approximately 10 days if not near a conservation area
- Equipment must be inspected by the National Sprayer Testing Scheme (NSTS) before the fifth anniversary of purchase, then every 3 years

**Operational Constraints:**
- Wind velocity must not exceed 10 knots during application (unless product approval permits higher)
- Warning signs required within 60m of treatment area
- Ground markers must be provided where they assist the pilot
- Appropriate vertical and horizontal distances must be maintained from people, livestock, and buildings

**Drone Category Considerations for a 2-4m Wingspan Fixed-Wing:**
- A 2-4m wingspan aircraft with 4kg payload likely has an MTOW of 8-15 kg, placing it in the **Specific Category** under UK drone regulations
- Requires an **Operational Authorization** from the CAA based on a risk assessment (SORA methodology or equivalent)
- If carrying and releasing pesticides, chemicals, or biological agents, additional HSE/DEFRA approvals apply
- Beyond Visual Line of Sight (BVLOS) operations require specific CAA approval and may require detect-and-avoid systems

### 8.5 Environmental Permits

- **Environmental Permitting Regulations 2016**: May apply if operations involve discharge of substances near controlled waters
- **DEFRA approvals**: Required for release of biological control agents (e.g., parasitoid wasps) that are not native to the UK
- **Invasive Alien Species (Enforcement and Permitting) Order 2019**: Regulates management activities for listed invasive species
- **Biocidal Products Regulation (retained EU law)**: Applies to rodenticides (e.g., brodifacoum) used outside of agricultural settings

### 8.6 Practical Compliance Pathway for a UK Drone Pest Control Operation

1. Obtain CAA Operational Authorization (Specific Category) with BVLOS approval if needed
2. Obtain Aerial Spraying Permit from HSE for each pesticide application
3. Ensure all pesticide products have UK registration and approval for aerial use
4. Consult Natural England if operating in or near SSSIs, SACs, SPAs, or other designated conservation areas
5. Obtain water authority consent if operating near watercourses
6. Ensure NSTS inspection of spray/dispersal equipment
7. Maintain operational logs, GPS flight records, and pesticide application records
8. For biological control agent release: consult DEFRA and obtain any necessary permits under the Wildlife and Countryside Act

---

## 9. ARDUPILOT INTEGRATION NOTES

### 9.1 Mission Planning for Pest Control

ArduPilot Plane supports hundreds of 3D waypoints, automatic takeoff/landing, and sophisticated mission planning. Key features for pest control:

- **DO_SET_SERVO**: Triggers spreader/release mechanism at specific waypoints
- **DO_SET_RELAY**: On/off control for spray pumps
- **DO_CHANGE_SPEED**: Adjusts speed for different mission phases (faster for transit, slower for delivery)
- **Survey Grid**: Mission Planner and QGroundControl can generate parallel survey/treatment lines with configurable spacing, altitude, and overlap

### 9.2 Crop Sprayer Integration

ArduPilot Copter includes native crop sprayer support: PWM-controlled pump and optional spinner, with flow rate automatically adjusted based on vehicle speed. For Plane (fixed-wing), this functionality can be adapted using the same servo/relay outputs, though native Plane support is less mature. Custom Lua scripting on ArduPilot can implement variable-rate application logic.

### 9.3 Sensor Integration

ArduPilot supports companion computers (Raspberry Pi, Nvidia Jetson) via MAVLink for real-time AI processing of thermal/multispectral imagery. This enables:
- Real-time thermal animal detection with waypoint logging for subsequent targeted treatment
- NDVI computation and invasive species detection during survey flights
- Adaptive mission modification based on in-flight detections

---

## SUMMARY OF KEY FINDINGS

For a 2-4m wingspan, 4kg payload, ArduPilot fixed-wing UAV, the most viable applications in approximate order of feasibility are:

1. **Thermal/multispectral survey and detection** --- The platform's primary strength. Long endurance and high speed make it ideal for transect-based population surveys and invasive plant mapping. Hardware: thermal camera + RGB/multispectral sensor.

2. **Broadcast bait delivery** --- Viable but payload-limited. At 2 kg/ha, each sortie covers ~1.5-2 ha. Best for supplementary operations in terrain inaccessible to helicopters but too small for helicopter economics. Hardware: lightweight centrifugal spreader.

3. **Seed ball dispersal** --- Similar payload constraints but good alignment with fixed-wing characteristics. Continuous release along flight lines suits the platform well. Hardware: gravity-fed hopper with servo gate.

4. **Precision bait pod delivery** --- GPS-triggered release of individual pods is well-suited to ArduPilot mission scripting. Lower throughput than broadcast but higher precision.

5. **SIT/biocontrol agent release** --- Forward speed and endurance make fixed-wing suitable for area-wide sterile insect or Trichogramma release. Requires careful container design to manage insect survival at speed.

6. **Herbicide spot-spraying** --- Least suited to fixed-wing due to forward speed, spray drift, and need for precise targeting. Better delegated to a multirotor partner platform using maps generated by the fixed-wing survey.

The optimal concept of operations is a **two-platform system**: the fixed-wing conducts survey and detection missions, generating target maps, while a multirotor (or the same fixed-wing with a different payload) conducts precision treatment missions guided by those maps.

---

Sources:
- [EPA Annual Report on Aerial 1080 Use in NZ 2024](https://www.epa.govt.nz/assets/RecordsAPI/EPA-annual-report-on-aerial-1080-use-in-New-Zealand-2024.pdf)
- [Precision Pest Control Using UAS and Novel Bait Pod System](https://cdnsciencepub.com/doi/abs/10.1139/dsa-2023-0104)
- [Envico Drone Baiting](https://www.envicotech.co.nz/drone-baiting)
- [NZ DOC - Why We Use 1080](https://www.doc.govt.nz/nature/pests-and-threats/methods-of-control/1080/why-we-use-1080/)
- [Predator Free NZ - Taking Flight](https://predatorfreenz.org/stories/taking-flight-saving-nature-from-the-sky/)
- [South Georgia Rodent Eradication - Cambridge Core](https://www.cambridge.org/core/journals/oryx/article/rodent-eradication-scaled-up-clearing-rats-and-mice-from-south-georgia/BC3E2CDA08575456EA235D0E92A41FB4)
- [NZ DOC - Rat Eradication Using Aerial Baiting Best Practice](https://www.doc.govt.nz/Documents/conservation/threats-and-impacts/pest-control/other-technical-documents/rat-eradication-using-aerial-baiting.pdf)
- [South Georgia Heritage Trust - Habitat Restoration Project](https://sght.org/habitat-restoration-project/)
- [Island Conservation - Seymour Norte Press Release](https://www.islandconservation.org/invasive-rodents-no-longer-threaten-wildlife-seymour-norte-island-mosquera-islet/)
- [Drones: Emergence of a Transformative Technology for Island Rodent Eradications](https://conbio.onlinelibrary.wiley.com/doi/full/10.1111/csp2.70139)
- [Five Years of Progress: Drone-Based Rodenticide Delivery](https://escholarship.org/uc/item/68r593zz)
- [CFR-Innovations Granule Spreader](https://www.cfr-innovations.com/)
- [AI-Powered Animal Recognition via Drone Thermal Imaging](https://dl.acm.org/doi/10.1145/3687272.3694716)
- [Automated Detection of Animals in Low-Resolution Airborne Thermal Imagery](https://www.mdpi.com/2072-4292/13/16/3276)
- [Fusion of Visible and Thermal Images for Wildlife Detection - Nature](https://www.nature.com/articles/s41598-023-37295-7)
- [European Hare Population Counts Using Thermal Drones](https://www.mdpi.com/2504-446X/7/1/5)
- [Human-Inspired Deep Learning for Thermal Drone Surveys (2025)](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.70006)
- [LILA BC Conservation Drones Dataset](https://lila.science/datasets/conservationdrones/)
- [NZ Wildlife Thermal Imaging Dataset - LILA BC](https://lila.science/datasets/new-zealand-wildlife-thermal-imaging/)
- [Aerial Wildlife Image Repository - Oxford Academic](https://academic.oup.com/database/article/doi/10.1093/database/baae070/7718812)
- [Thermal Drone Surveys for Population Density Estimation](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/eap.70091)
- [Method Matters: Thermal Drones and Density Estimation](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/eap.70164)
- [UAV-Assisted Seeding and Monitoring of Reforestation Sites Review](https://www.tandfonline.com/doi/full/10.1080/00049158.2024.2343516)
- [AirSeed Technologies](https://www.airseedtech.com/)
- [Dendra Systems Aerial Seeding](https://www.dendra.io/aerial-seeding)
- [Drone Reforestation - Mongabay](https://news.mongabay.com/2023/07/new-tree-tech-cutting-edge-drones-give-reforestation-a-helping-hand/)
- [Design of a Seed Dispenser for UAVs - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2405896325024668)
- [Seed Ball Sowing with Fixed Wing UAVs](https://www.academia.edu/44301537/IRJET_AFFORESTATION_USING_FIXED_WING_UAV)
- [Pix4D - Mapping and Spot Spraying Invasive Weeds](https://www.pix4d.com/blog/drone-mapping-spraying-invasive-species)
- [Herbicide Spraying and Weed ID Using Drone Technology Review](https://www.sciencedirect.com/science/article/pii/S2590123024001233)
- [Systematic Review of Drone Remote Sensing of Invasive Plants (2024)](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.14330)
- [Spray Drift Characteristics of Unmanned Aerial Spraying Systems](https://pmc.ncbi.nlm.nih.gov/articles/PMC9395147/)
- [Agricultural Spray Drone Deposition: Height and Nozzle Influence](https://www.cambridge.org/core/journals/weed-science/article/agricultural-spray-drone-deposition-part-2-operational-height-and-nozzle-influence-pattern-uniformity-drift-and-weed-control/BC63228D24C1D1EC3761C02F74E2B747)
- [IAEA Drone Test for Sterile Mosquito Release](https://www.iaea.org/newscenter/pressreleases/drone-test-yields-breakthrough-for-use-of-nuclear-technique-to-fight-mosquitoes-iaea-study)
- [Field Performance of Sterile Male Mosquitoes from UAV - Science Robotics](https://www.science.org/doi/10.1126/scirobotics.aba6251)
- [WeRobotics Drone Aerial Release Mechanism for Mosquitoes](https://werobotics.org/assets/blog/2018/04/WeRobotics-Drone-based-Aerial-Release-Mechanism-for-Mosquitoes-v1.1.pdf)
- [Trichogramma UAS Release in Canada - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8513577/)
- [Trichogramma Ball Delivery System for Agricultural Drone](https://www.mdpi.com/2504-446X/7/10/632)
- [Drones: Innovative Technology for Precision Pest Management](https://academic.oup.com/jee/article/113/1/1/5666881)
- [Burrow-Nesting Seabird Survey Using UAV Thermal Sensor](https://www.mdpi.com/2504-446X/7/11/674)
- [COTSbot - Underwater Drone for COTS](https://www.asme.org/topics-resources/content/underwater-drone-hunts-coraleating-crownofthorns)
- [RangerBot - New Atlas](https://newatlas.com/rangerbot-reef-underwater-drone/56173/)
- [COTS Detection with YOLOv6 - Frontiers](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2025.1658205/full)
- [Kelp Mapping Guidebook - Hakai Institute](https://hakai.org/kelp-mapping-guidebook/)
- [Drone eDNA Water Sampling - Limnology and Oceanography Methods](https://aslopubs.onlinelibrary.wiley.com/doi/10.1002/lom3.10214)
- [NatureMetrics Autonomous eDNA Autosampler](https://www.naturemetrics.com/news/autonomous-aquatic-edna-sampling-solution)
- [UK HSE Aerial Spraying Permit Arrangements](https://www.hse.gov.uk/pesticides/using-pesticides/general/aerial-spraying.htm)
- [Control of Pesticides Regulations 1986 - UK Legislation](https://www.legislation.gov.uk/uksi/1986/1510/made)
- [UK CAA Approves Agricultural Drone Spraying (2023)](https://dronedj.com/2023/01/20/uk-caa-agricultural-drone-spraying/)
- [UK CAA Introduction to Drone Flying Rules](https://www.caa.co.uk/drones/rules-and-categories-of-drone-flying/introduction-to-drone-flying-and-the-uk-rules/)
- [Zero Invasive Predators (ZIP)](https://zip.org.nz/)
- [Predator Free 2050 Science and Innovation - NZ DOC](https://www.doc.govt.nz/nature/pests-and-threats/predator-free-2050/innovative-tools-and-technology/)
- [ArduPilot Plane Documentation](https://ardupilot.org/plane/)
- [ArduPilot Crop Sprayer Documentation](https://ardupilot.org/copter/docs/sprayer.html)
- [FitoStinger Drone Pest Control - EU CORDIS](https://cordis.europa.eu/article/id/418469-drone-based-pest-control-system-protects-europe-s-trees)
- [Spray Drone ROI Cost Analysis](https://dronespraypro.com/blogs/news/spray-drone-roi-cost-analysis-for-modern-farming)
- [Economics of Drone Ownership for Agricultural Spray - MU Extension](https://extension.missouri.edu/publications/g1274)
