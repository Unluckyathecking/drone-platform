# Automated Drone Base/Hub Systems: Comprehensive Research

## 1. Wing (Alphabet/Google)

### How Their Automated Delivery Hubs Work

Wing has evolved from a centralized hub model to a distributed network model called the **Wing Delivery Network**. The system has three core components:

- **Pads**: Landing/charging stations distributed around a city where drones take off, land, and recharge between trips. Pads can be added incrementally to expand coverage.
- **AutoLoaders**: Compact devices (roughly the size of a single parking space) installed at partner stores (e.g., Walmart). Store staff load a package into the AutoLoader, and a Wing drone collects it via its tether without landing. AutoLoaders require no power and no data connection -- they are purely mechanical pickup points.
- **Software/Operations Center**: A centralized control system manages routing, scheduling, and monitoring. One supervising pilot can monitor up to 15 drones simultaneously.

### Operations

- **Logan, Queensland (Australia)**: Crowned "drone delivery capital of the world." Over 50,000 of Wing's first 100,000 deliveries were to Logan customers. Operations scaled to 1,000+ deliveries per day in the region.
- **Dallas-Fort Worth (US)**: First major US metro deployment. Launched from Walmart Supercenter locations in Frisco, with operations at eight+ Walmart stores across Arlington, Frisco, Lewisville, and North Richland Hills.
- **2025-2026 expansion**: Delivery volume tripled in H2 2025 vs H1. 150-store Walmart expansion announced adding Los Angeles, St. Louis, Cincinnati, Miami. Houston went live as first new market of 2026. Bay Area launching March 2026. Over 750,000 total residential deliveries. Service area covers 2+ million customers.

### The Drone

- **Configuration**: Hybrid VTOL -- vertical takeoff/landing with fixed wings for cruise flight. All-electric.
- **Payload**: Original model: 2.5 lbs (1.1 kg). Newer model: 5 lbs (2.3 kg).
- **Range**: 12 statute miles (19.3 km) round trip.
- **Speed**: Up to 65-70 mph (105-113 km/h).
- **Delivery method**: Hovers above the delivery point and lowers the package on a tether/winch line. Does not land at the delivery site.

### Level of Automation

High but not fully autonomous. Remote pilots at a central operations center supervise multiple drones. The flight itself is autonomous (route planning, obstacle avoidance, precision hovering for delivery). Package loading still requires human staff at the store to place items in AutoLoaders. Future plans target fully automated loading.

### Throughput

Up to 1,000+ deliveries per day per delivery region.

### Hub Footprint

No single large facility required. The distributed model uses existing retail stores with AutoLoaders (one parking space each) plus scattered charging Pads. The central operations center size is not publicly specified.

### Charging

Contact charging at Pads. Drones land on Pads and charge between missions. The network software optimizes when and where drones charge.

---

## 2. Zipline

### Platform 1 (P1)

**Launch**: Supercapacitor-powered electric catapult accelerates the drone from 0 to 67 mph (108 km/h) in 0.33 seconds.

**Flight**: Fixed-wing drone cruises at 63 mph (101 km/h) at 80-120m altitude. Range up to 100 km (62 miles) delivery radius. Payload up to 5 lbs.

**Delivery**: The drone descends to 20-35m and drops the package under a paper "drogue" parachute. The drone never lands at the delivery site.

**Recovery**: The drone returns to the distribution center and catches an arresting wire with a tail hook, identical in concept to carrier-based aircraft recovery. This is extremely space-efficient -- no runway needed.

**Hub Design**: Each distribution center has three main operating rooms: a control tower (monitoring airspace), a warehouse (storing medical supplies/blood/products), and a flight operations center. The Kayonza, Rwanda facility has capacity for 150 deliveries per day.

**Robotic Loading**: At P1 hubs, staff manually load packages into the drones before catapult launch. Pharmacists, biotechnologists, and engineers staff the centers (~40+ people at the Rwanda sites).

**Throughput**: 100-150 deliveries per day per distribution center (Ghana target). New sites in the US have reached 100 deliveries/day within 2 days of opening.

**Countries Operating**: Rwanda (2 distribution centers + third planned), Ghana (6 distribution centers serving 2,300+ health facilities), Kenya, Nigeria, Cote d'Ivoire, Japan, and multiple US cities (Dallas-Fort Worth, Salt Lake City, and expanding to Houston, Phoenix).

**Milestones**: 2+ million commercial deliveries completed. 120+ million autonomous miles flown. Valued at $7.6 billion (2026).

### Platform 2 (P2 "Zip")

**Aircraft**: Hybrid lift+cruise design with both rotors and fixed wings. Much quieter than P1 -- noise described as "rustling leaves."

**Payload/Range**: Up to 8 lbs within a 10-mile delivery radius. Can fly up to 24 miles between docking stations.

**Delivery Method**: The P2 hovers at ~300 feet and deploys a "Droid" -- a small delivery container that descends on a tether. The Droid has its own thrusters and sensors, navigating to a 1-meter diameter landing zone with precision. This is a major innovation: the main aircraft never descends.

**Autonomous Docking**: P2 docks autonomously at compact docking stations that fit in a single parking space or alongside a building. The docks charge the aircraft automatically. No catapult or arresting wire needed -- the P2 is VTOL.

**Energy**: Uses 97% less energy per delivery than P1 (because it serves shorter urban routes).

**Network Model**: Dock-to-dock flying allows a mesh network where drones pick up at one dock and deliver via another, similar to Wing's distributed model.

---

## 3. Amazon Prime Air (MK30)

### Current State (2025-2026)

- Roughly 16,000 total deliveries made as of early 2026.
- Active in 8 US metro areas: Phoenix, Dallas-Fort Worth, Waco, San Antonio, Tampa, Detroit, Kansas City, and Chicago (launching).
- Ambitious target: 500 million deliveries per year by 2030.
- Has experienced setbacks: at least 7 significant incidents since January 2025 including collisions with a crane, apartment building, and internet cable. A two-drone collision in Arizona (October 2025) led to a temporary service pause and FAA/NTSB investigation. Service resumed March 2025.

### MK30 Drone

- Weight: 83 lbs.
- Fully electric VTOL hexagonal design.
- Payload: up to 5 lbs.
- Range: 7.5 miles from fulfillment center.
- Delivery: Descends to ~13 feet above ground, scans for obstacles (pets, cars, people), then releases the package.
- FAA-approved for BVLOS from day one at new locations -- an industry first.
- Designed to operate in light rain and moderate wind.

### Delivery Hub Design

- **"Sub-Same Day" (SSD) fulfillment centers**: 9,000 sq ft facilities including drone launch pads, battery charging stations, and an operations center.
- Located in strategic suburban hubs near population centers.
- Designed to transition a package from shelf to drone in minutes.

### Level of Automation

High automation with human oversight. The drone flies autonomously with onboard detect-and-avoid. An operations center monitors flights. Package loading and facility operations require human staff (numbers not publicly disclosed).

### Regulatory Status

FAA Type Certificate and Part 135 air carrier certificate for MK30. BVLOS approval granted. Under heightened scrutiny after 2025 incidents.

---

## 4. Insitu/Boeing ScanEagle

### SkyHook Recovery System

The SkyHook is a 30-50 foot vertical pole with a hanging rope. The ScanEagle has a hook on the end of its wingtip. Using high-precision differential GPS mounted on both the pole and the UAV, the drone flies into the rope and catches it with the wingtip hook. The rope absorbs the kinetic energy and the drone hangs from the pole for retrieval.

This is mechanically elegant: no runway, no net, no landing gear needed. It works on ships at sea (rolling decks) and in confined spaces.

### Launch System

- **SuperWedge/Mark 4 pneumatic catapult**: The standard launch system for 20+ years. Pneumatic power accelerates the drone to flying speed.
- **FLARES (Flying Launch and Recovery System)**: A newer approach where a rotary-wing UAV carries the fixed-wing ScanEagle, takes off vertically, clears obstacles, then releases it in flight. Eliminates the need for a catapult entirely -- makes the system truly expeditionary.

### Ground Station Operations

- A complete ScanEagle system comprises: 4 air vehicles, a ground control station (GCS), remote video terminal, SuperWedge launcher, and SkyHook recovery system.
- The GCS has 2 operator consoles and can control up to 8 air vehicles simultaneously.
- A typical 24/7 deployment requires ~7 military personnel + support contractors. Minimum crew for basic operations is approximately 2-3 operators.
- The ICOMC2 (Common Open-mission Management Command and Control) for ScanEagle 2 enables multiple unmanned systems to be managed from a single station.

### STUAS (RQ-21 Blackjack / Integrator)

Uses the same launch and recovery approach as ScanEagle (catapult + SkyHook) but is a larger, more capable platform. The Navy's Small Tactical UAS program, built by Insitu.

---

## 5. Other Automated Drone Systems

### Percepto (Autonomous Inspection Drones)

- **System**: AI-powered drone-in-a-box for industrial inspection (oil & gas, utilities, mining).
- **Launch/Recovery**: VTOL multirotor. Automated takeoff and landing from the Percepto Base.
- **Percepto Base (Air Mobile)**: 100 x 100 x 75 cm, ~100 kg, IP56 rated.
- **Percepto Base (Air Max)**: Heavier at 162 kg. IP65 rated. Withstands 150 mph hurricane-force winds.
- **Autonomy**: Level 5 -- fully autonomous. FAA-approved control centers can manage up to 30 drones from a single location. No pilot on site required.
- **Charging**: Automated contact charging inside the base.
- **Missions/day**: Multiple scheduled and on-demand flights per day.
- **EPA approved** for autonomous OGI (methane leak detection) inspections.
- **Key clients**: Chevron, major utilities.

### Skydio Dock (for X10)

- **Dimensions**: 55.5" x 34.1" x 47.8" (~141 x 87 x 121 cm). Weight: ~229 lbs (104 kg).
- **Launch time**: Airborne in under 20 seconds from alert.
- **Drone (X10)**: Up to 40 min flight time, 12 km range (rural), 1-2 km (dense urban). Visual navigation with AI obstacle avoidance.
- **Environmental**: Built-in HVAC for -4F to 122F. Tested against 160 mph winds. Operates in moderate rain and 28 mph winds.
- **Landing**: Visual fiducial system on Dock landing surface for precision autonomous landing.
- **Scaling**: "Hives" of 2+ Docks for persistent coverage. One operator can command tens to hundreds of drones.
- **Power**: 100-240V AC input. Backup battery for 5 hours.
- **Maintenance**: Biannual.
- **Price**: Not publicly disclosed; early access only through selected partners.
- **Applications**: Public safety (eyes on scene in seconds), infrastructure inspection, construction monitoring.

### DJI Dock 2

- **Footprint**: 0.34 m2 -- the smallest in the market. Weight: 34 kg.
- **Reduction**: 75% smaller volume and 68% lighter than DJI Dock 1.
- **Compatible drones**: Matrice 3D and 3DT.
- **Flight time**: Up to 50 minutes.
- **Range**: 10 km operational.
- **Launch time**: 45 seconds from activation to airborne.
- **Environmental**: IP55, -25C to 45C operating range.
- **Backup battery**: 5 hours in case of power outage.
- **Maintenance**: Biannual.
- **Software**: FlightHub 2 for remote scheduling and management.
- **Price**: ~$21,000-$23,000 (Dock 3 with Matrice 4D/4TD bundle).
- **Autonomy**: High -- scheduled missions, automated RTK landing, but typically requires remote operator oversight.

### Airobotics (Automated Industrial Drone Stations)

- **System**: Optimus drone + Airbase station + cloud software.
- **Optimus Drone**: 30-minute flight time, 1 kg payload, military-grade avionics.
- **Airbase**: Fully sealed, waterproof, corrosion-resistant enclosure. Contains a **robotic arm** that automatically swaps batteries and payloads between missions -- this is the key differentiator.
- **Autonomy**: Level 5 -- fully autonomous. No pilot required. One-click mission launch from cloud software.
- **Battery/payload swap**: Robotic arm performs automated swap, enabling rapid turnaround and different payloads (visual, thermal, LiDAR, OGI) per mission.
- **Wind tolerance**: Up to 25 knots.
- **Footprint**: Not publicly specified but described as a large industrial enclosure.
- **Applications**: Mining, oil & gas, ports, smart cities.
- **FAA Type Certificate**: Received for Optimus drone.
- **Price**: Enterprise pricing, estimated $250K+ per system.

### American Robotics Scout

- **System**: Scout drone + ScoutBase + ScoutView (cloud portal).
- **Historic first**: First company FAA-approved to operate automated drones without any human operators on site (2021).
- **BVLOS**: Approved for fully autonomous BVLOS up to 10 miles range, under 400 feet altitude.
- **Detect-and-Avoid**: Proprietary acoustic DAA technology -- listens for other aircraft.
- **Throughput**: Up to 20 autonomous missions per day.
- **Autonomy**: Level 5 -- fully autonomous, multi-year unattended operation.
- **Model**: Robotics-as-a-Service (RaaS) -- no capital purchase, subscription-based.
- **ScoutBase**: Weatherproof, autonomous housing/charging/data processing station. Specific dimensions not publicly disclosed.
- **Applications**: Agriculture (precision farming), oil & gas, rail, mining, critical infrastructure.

### UK-Based Automated Drone Companies

- **HEROTECH8**: Connected drone-in-a-box network for border control, airport security, emergency services. Nationwide network enabling on-demand autonomous operations with live feed data.
- **Airvis**: Autonomous drone security systems. IP-rated aircraft with dual day/night cameras, thermal sensor, NIR light. 54 min flight / 47 min hover. Designed for UK security and surveillance market.
- **DroneAg / Agrii**: Deployed one of the first UK agricultural drone-in-a-box systems (Yorkshire, 2025) using Skippy Scout software for autonomous trial plot monitoring.
- **Sky-Drones Technologies**: UK-based manufacturer of drone software and hardware platforms for enterprise autonomous operations.
- **UK market context**: GBP 38.1M invested in UK drone companies in 2025. Regulatory environment progressing but more cautious than US/Australia.

---

## 6. Comparison Table

| System | Launch Method | Recovery Method | Charging/Battery | Autonomy (1-5) | Footprint | Throughput | Cost | Humans Required |
|--------|--------------|-----------------|-------------------|-----------------|-----------|------------|------|-----------------|
| **Wing** | VTOL (rotors) | Precision landing on Pad | Contact charging on Pads | 4 (remote pilot oversight) | Distributed: 1 parking space per AutoLoader/Pad | 1,000+/day per region | Not disclosed | 1 pilot per 15 drones + store staff for loading |
| **Zipline P1** | Electric catapult (0-67mph in 0.3s) | Arresting wire (tail hook) | Battery swap at hub (manual) | 4 (remote pilot monitors) | ~500m2 distribution center | 100-150/day per center | Not disclosed | ~40+ staff per distribution center |
| **Zipline P2** | VTOL (rotors + wing) | Autonomous dock landing | Contact charging in dock | 4.5 (near-autonomous) | 1 parking space per dock | 100+/day per dock | Not disclosed | Minimal -- remote oversight |
| **Amazon MK30** | VTOL (hexarotor) | Precision landing at hub | Battery charging at hub | 4 (remote oversight) | ~830m2 (9,000 sq ft) SSD center | Low currently (~50/day est.) | Not disclosed | Fulfillment center staff + ops center |
| **ScanEagle** | Pneumatic catapult | SkyHook (rope + wingtip hook) | Manual battery swap | 3 (2 operators minimum) | ~100m2 (launcher + SkyHook + GCS) | 3-5 sorties/day (ISR) | ~$3.2M per system | 2-3 minimum, 7+ for 24/7 |
| **Percepto** | VTOL (multirotor) | Autonomous precision landing | Contact charging in base | 5 (fully autonomous) | 1m2 (base footprint) | 5-10 missions/day | $40K-$250K+ | 0 on site; 1 remote per 30 drones |
| **Skydio Dock** | VTOL (multirotor) | Autonomous visual-fiducial landing | Contact charging in dock | 4.5 (near-autonomous) | ~1.2m2 | 10-20 missions/day | Not publicly disclosed | 0 on site; 1 remote per 10s-100s drones |
| **DJI Dock 2** | VTOL (multirotor) | Autonomous RTK landing | Contact charging in dock | 4 (remote operator) | 0.34m2 | 10-15 missions/day | ~$21K-$23K (with drone) | 0 on site; 1 remote operator |
| **Airobotics** | VTOL (multirotor) | Autonomous precision landing | Robotic arm battery swap | 5 (fully autonomous) | ~4m2 (estimated) | 10-15 missions/day | ~$250K+ | 0 on site; cloud-managed |
| **American Robotics Scout** | VTOL (multirotor) | Autonomous landing in ScoutBase | Contact charging in base | 5 (fully autonomous, FAA-certified) | ~2m2 (estimated) | Up to 20 missions/day | RaaS subscription | 0 on site; 0 required (fully automated) |

---

## 7. Key Engineering Principles Extracted

### Pattern 1: VTOL Dominates for Automated Systems
Nearly every modern automated drone base uses VTOL (multirotor or hybrid). The only exceptions are legacy military systems (ScanEagle) and Zipline P1. VTOL eliminates the need for runways, catapults, and recovery systems, dramatically reducing the base station footprint. Zipline's own evolution from P1 (catapult + arresting wire) to P2 (VTOL + dock) confirms this trend.

### Pattern 2: The "Drone-in-a-Box" Form Factor is Converging
DJI Dock 2 (0.34m2), Percepto Base (1m2), Skydio Dock (~1.2m2), and American Robotics ScoutBase all converge on a weatherproof enclosure roughly 0.3-2m2 that handles: housing, charging, environmental control (HVAC), and communications. The enclosure opens its lid, the drone launches vertically, returns, and lands on a precision pad inside. This is the dominant pattern for inspection/monitoring use cases.

### Pattern 3: Precision Landing is the Critical Enabler
Every successful automated system solves the precision landing problem differently but reliably: visual fiducials (Skydio), RTK GPS (DJI), GPS + computer vision (Percepto, Airobotics), or avoids it entirely (Wing's tether pickup from AutoLoaders, ScanEagle's SkyHook). Without reliable, repeatable precision landing, you cannot automate the return-to-base cycle.

### Pattern 4: Battery Strategy Determines Turnaround Time
Three approaches exist:
- **Contact charging in dock** (DJI, Skydio, Percepto, Zipline P2): Simplest mechanically but slowest turnaround (30-60 min charge).
- **Robotic battery swap** (Airobotics): Fastest turnaround (~minutes) but most mechanically complex. Enables different battery sizes and payloads per mission.
- **Distributed charging pads** (Wing): The drone charges opportunistically at the nearest pad, keeping the fleet moving.

For maximum throughput, battery swap or multiple-drone-per-dock strategies are needed.

### Pattern 5: The "Zero Humans On Site" Threshold
The regulatory and engineering frontier is removing humans from the field entirely. American Robotics was first to achieve FAA approval for zero-human-on-site operations. Percepto manages 30 drones from one remote operator. This requires: acoustic or electronic detect-and-avoid, weatherproof enclosures, self-diagnostic health monitoring, and redundant communications. This is the standard your system should target.

### Pattern 6: Distributed Network vs. Centralized Hub
Two architecture models are emerging:
- **Centralized hub** (Zipline P1, Amazon): A single facility with many drones, staff, and inventory. Higher throughput per location but expensive and inflexible.
- **Distributed network** (Wing, Zipline P2, DJI/Skydio/Percepto docks): Many small, cheap nodes spread across the area. Each node is simple (one dock, one drone). Scale by adding nodes. More resilient, lower per-node cost, easier regulatory approval.

The industry is clearly trending toward distributed.

### Pattern 7: Environmental Hardening is Non-Negotiable
Every operational system is designed for extreme conditions: Percepto Base survives 150 mph winds, Skydio Dock tested to 160 mph, DJI Dock 2 operates -25C to 45C. IP55-IP65 ratings are standard. Built-in HVAC is common. Systems that cannot operate in rain, wind, and temperature extremes do not get deployed.

### Pattern 8: Remote Operations Center Model
Wing (1 pilot : 15 drones), Percepto (1 operator : 30 drones), Skydio (1 operator : 100s of drones) all use a centralized remote operations center. This is far more efficient than on-site pilots. The ratio of operators to drones keeps improving as autonomy software matures.

### Pattern 9: The Delivery Mechanism Matters
For delivery drones specifically, three approaches:
- **Tether/winch lowering** (Wing, Zipline P2 Droid): Aircraft hovers and lowers package. Avoids ground-level obstacles. More precise.
- **Parachute drop** (Zipline P1): Simplest but least precise. Works for medical supplies to known landing zones.
- **Descend-and-release** (Amazon MK30): Drone descends close to ground (~4m) then releases. Simpler than tether but requires clear landing zone.

Tether/winch is emerging as the preferred method for residential delivery.

### Pattern 10: Regulatory Approval is the Hardest Part
Every system's deployment timeline was gated by regulation, not technology. American Robotics spent years getting zero-human-on-site approval. Amazon's program has been in development since 2013 and has only completed ~16,000 deliveries. Wing succeeded partly by starting in Australia (more permissive) and building a regulatory track record. Any drone base system must be designed with regulatory compliance (detect-and-avoid, logging, redundancy, fail-safes) as a core requirement from day one.

---

## Sources

- [Wing Launches the Automated Wing Delivery Network, with Autoloader](https://dronelife.com/2023/03/09/wing-launches-the-automated-wing-delivery-network-with-autoloader-for-curbside-pickup-videos/)
- [Wing shows off AutoLoaders](https://newatlas.com/drones/wing-autoloaders/)
- [Wing Technology](https://wing.com/technology)
- [Wing Finally Brings Drone Delivery To Bay Area](https://dronexl.co/2026/03/24/wing-brings-drone-delivery-to-bay-area/)
- [Wing Introduces New Delivery Drone with Double the Payload](https://www.flyingmag.com/googles-wing-introduces-new-delivery-drone-with-double-the-payload/)
- [Zipline Wikipedia](https://en.wikipedia.org/wiki/Zipline_(drone_delivery_company))
- [Zipline and the Network Design Behind the Most Advanced Autonomous Delivery System](https://www.logisticsnavigators.com/startup-corner/zipline-and-the-network-design-behind-the-most-advanced-autonomous-delivery-system-in-the-world)
- [Zipline unveils P2 delivery drones that dock and recharge autonomously](https://www.cnbc.com/2023/03/15/zipline-unveils-p2-delivery-drones-that-dock-and-recharge-autonomously.html)
- [Zipline Platform 2 Droid Drone Delivery - IEEE Spectrum](https://spectrum.ieee.org/delivery-drone-zipline-design)
- [Zipline Completes First Customer Delivery With P2](https://dronexl.co/2025/01/16/zipline-completes-first-customer-delivery-p2-drone/)
- [Zipline raises over $600M, surpasses 2M deliveries](https://www.therobotreport.com/zipline-raises-over-600m-in-funding-surpasses-2m-commercial-drone-deliveries/)
- [Zipline snaps up another $200M](https://techcrunch.com/2026/03/23/zipline-snaps-up-another-200m-to-fuel-its-drone-delivery-expansion/)
- [Inside Zipline's New Rwandan Distribution Centre](https://www.uasvision.com/2019/03/21/inside-ziplines-new-rwandan-distribution-centre/)
- [Amazon Prime Air Wikipedia](https://en.wikipedia.org/wiki/Amazon_Prime_Air)
- [Amazon Prime Air Hosts Community Meet-and-greet In Tinley Park](https://dronexl.co/2026/02/26/amazon-prime-chicago-drone-delivery-launch/)
- [Amazon Prime Air Launches In Kansas City](https://dronexl.co/2026/02/09/amazon-prime-air-kansas-city/)
- [Amazon resumes drone deliveries after two-month pause](https://www.cnbc.com/2025/03/31/amazon-resumes-drone-deliveries-after-two-month-pause.html)
- [Meet the MK30, Amazon's most advanced delivery drone](https://www.aboutamazon.com/news/operations/mk30-drone-amazon-delivery-packages)
- [Boeing Insitu MQ-27 ScanEagle Wikipedia](https://en.wikipedia.org/wiki/Boeing_Insitu_MQ-27_ScanEagle)
- [ScanEagle - Naval Technology](https://www.naval-technology.com/projects/scaneagle-uav/)
- [Insitu FLARES launch system](https://www.flightglobal.com/civil-uavs/insitu-pressing-forward-with-flares-as-scaneagle-launch-system/120504.article)
- [Percepto Autonomous Drone Solutions](https://percepto.co/)
- [Percepto Base Specifications](https://percepto.co/drone-in-a-box/percepto-base/)
- [Chevron's Autonomous Drone Inspections with Percepto](https://dronelife.com/2025/03/14/the-inside-story-on-chevrons-autonomous-drone-inspections-with-percepto/)
- [Skydio Dock for X10](https://www.skydio.com/dock)
- [Skydio Dock Technical Specs](https://www.skydio.com/dock/technical-specs)
- [DJI Dock 2 Guide](https://www.flytbase.com/blog/dji-dock-2-guide)
- [DJI Dock 2 Pricing and Specs](https://candrone.com/blogs/news/dji-dock-2)
- [Airobotics Automated Drone Platform](https://www.airoboticsdrones.com/press-releases/airobotics-unveils-completely-automated-drone-platform-will-revolutionize-industrial-enterprises/)
- [Airobotics battery-swapping platform](https://newatlas.com/airobotics-system-drones/43985/)
- [American Robotics FAA approval](https://www.auvsi.org/news/american-robotics-receives-approval-to-operate-automated-drones-without-human-operators-on-site/)
- [American Robotics BVLOS Waiver](https://www.american-robotics.com/post/new-bvlos-waiver-secured-by-american-robotics-defines-a-framework-for-bvlos-operations-under-part-10)
- [Drone-in-the-Box Systems in 2025: Deep Dive](https://www.thedroneu.com/blog/drone-in-the-box-systems/)
- [UK Drone Companies - Beauhurst](https://www.beauhurst.com/blog/top-drone-companies-uk/)
- [Airvis Autonomous Drone Security UK](https://airvis.co.uk/autonomous-drone-security/)
- [HEROTECH8 / UK autonomous drone companies](https://ensun.io/search/autonomous-drone/united-kingdom)
