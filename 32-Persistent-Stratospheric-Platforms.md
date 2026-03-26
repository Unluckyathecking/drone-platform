# Persistent High-Altitude Platforms: Comprehensive Research Document

## 1. Solar HAPS (High Altitude Pseudo-Satellites)

### Operating Principle

Solar HAPS are fixed-wing or flying-wing UAVs that fly in the stratosphere (18-25 km / 60,000-80,000 ft), powered by solar cells during the day and batteries at night. They fill the gap between terrestrial systems and satellites — offering satellite-like coverage with drone-like flexibility and cost.

The fundamental engineering challenge is the **overnight power problem**: the aircraft must carry enough battery to sustain flight through 14+ hours of darkness at winter solstice latitudes, while remaining light enough to fly in air that is only ~5% of sea-level density.

### Airbus Zephyr

**The current benchmark for solar HAPS.**

- **Zephyr S**: 25m wingspan, ~75 kg total mass, flies at ~21 km (70,000 ft)
- **Record flight**: 64 days, 18 hours, 26 minutes (June-August 2022, launched from Yuma, Arizona). This smashed the previous 25-day record.
- **What happened after the record**: The aircraft was lost on its next flight attempt in late 2022 — it encountered unexpected stratospheric turbulence and broke up. A second aircraft was also lost in 2023 during testing.
- **Current status (2025-2026)**: Airbus has continued development despite the losses. The Zephyr T (next generation) is a larger variant (~33m wingspan) intended to carry heavier payloads (up to 20 kg vs ~5 kg for Zephyr S). Airbus secured contracts with the UK Ministry of Defence (under Project Obsidian/FCAS-adjacent programmes) and has been conducting flight campaigns from various locations. The programme has been somewhat quiet publicly after the crash losses, with Airbus reportedly focusing on improving structural resilience to stratospheric weather phenomena (gravity waves, turbulence layers at the tropopause).
- **Key lesson from Zephyr**: Even at 21 km, the atmosphere is not benign. Gravity waves, wind shear, and tropopause turbulence can destroy ultralight structures. The 64-day flight proved the energy system works; structural robustness is the remaining challenge.
- **Built in Farnborough, UK** (relevant for UK section below).

### BAE Systems PHASA-35

- **UK-developed** solar HAPS, 35m wingspan
- Originated from Prismatic Ltd (a small UK company BAE acquired in 2019)
- First flight of a subscale demonstrator in 2020 at Woomera, Australia
- **Current status**: BAE has been relatively quiet about PHASA-35 since 2022-2023. It appears to be in continued development, with BAE positioning it as part of a broader "layered sensing" capability alongside conventional satellites and lower-altitude drones. No public 64-day-class endurance demonstrations yet.
- **Target applications**: Persistent ISR (intelligence, surveillance, reconnaissance), communications relay, border monitoring
- **Key differentiator**: BAE is integrating it with wider defence systems rather than marketing it as a standalone product

### SoftBank HAPSMobile / Sunglider

- Joint venture between SoftBank and AeroVironment
- **Sunglider**: 78m wingspan — one of the largest solar HAPS ever built
- Designed specifically for **telecommunications** — acting as a stratospheric cell tower
- First stratospheric test flight in 2020 from Spaceport America, New Mexico
- The aircraft achieved stratospheric altitude but experienced a landing incident
- **Current status**: SoftBank has invested heavily (~$200M+) but progress has been slow. AeroVironment (the partner providing aerospace expertise) has been doing the engineering. The massive wingspan creates structural challenges. SoftBank's core interest is using these as floating cell towers for connectivity in developing nations and disaster response.
- **Key insight**: The telecom business case is compelling — a single HAPS at 20 km can cover a ~200 km diameter cell, replacing hundreds of terrestrial towers. But the engineering is brutally hard.

### Facebook Aquila (Cancelled)

- **Cancelled in 2018** after ~3 years of development
- 42m wingspan, ~400 kg, designed to fly at 18-27 km for 90 days
- **Why it failed**:
  1. **Structural failures**: First full-scale test flight in June 2016 ended with a crash landing — the right wing broke during approach. An NTSB investigation found structural divergence (the wing bent beyond limits in a gust).
  2. **Facebook's strategic pivot**: Mark Zuckerberg decided it was more efficient to partner with existing aerospace companies and satellite operators rather than build aircraft in-house. Facebook (Meta) pivoted to investing in subsea cables, terrestrial wireless, and LEO satellites instead.
  3. **Engineering underestimation**: Facebook's software engineers underestimated the aerospace challenge. Building an ultralight, ultra-efficient aircraft is an aerospace-specific discipline — it doesn't transfer from software engineering culture.
- **Legacy**: The Aquila team's work on laser communication (free-space optical links) between HAPS and ground stations was genuinely innovative and has influenced the field.

### XSun SolarXOne (French)

- Smaller-scale French solar drone company
- Not stratospheric — operates at lower altitudes (few hundred to few thousand metres)
- Focused on agricultural and industrial inspection applications
- Relevant as a commercial solar drone but **not a HAPS competitor**

### KARI EAV-3 (South Korean)

- Developed by the Korea Aerospace Research Institute
- 20m wingspan, ~53 kg
- Achieved 18.5 km altitude in test flights (2016, 2020)
- One of the few government-funded HAPS programmes outside Europe/US
- **Current status**: Continued development with the Korean government for maritime surveillance over the Korean peninsula. South Korea's geography (peninsula surrounded by sea) makes HAPS attractive for persistent maritime domain awareness.

### Aurora/Boeing Odysseus (Cancelled)

- Developed by Aurora Flight Sciences (acquired by Boeing in 2017)
- 74m wingspan — massive flying wing with three fuselage pods
- Used a unique "perpetual flight" concept with solar cells covering the entire upper wing surface
- **Why it was cancelled**:
  1. Aurora was acquired by Boeing, and Boeing's priorities shifted
  2. The programme competed internally with Boeing's satellite business
  3. First outdoor structural test in 2019 — the aircraft was damaged by ground winds before it even flew. The ultralight structure (carbon fibre and thin film) was too fragile for real-world handling
  4. Boeing subsequently deprioritised it in favour of other programmes
- **Key lesson**: Ground handling of ultralight stratospheric aircraft is a serious operational challenge. These things are essentially giant kites — any ground wind can destroy them.

### Current State of the Solar HAPS Industry (2025-2026)

The industry is in a **"trough of disillusionment"** phase:
- Multiple high-profile cancellations (Aquila, Odysseus)
- Crash losses (Zephyr)
- No system has yet achieved routine, operational, months-long persistence
- **But**: Zephyr's 64-day flight proved the physics works. The problems are engineering, not fundamental.
- **Who's still actively flying**: Airbus Zephyr (cautiously), BAE PHASA-35 (development), HAPSMobile (slowly)
- **Investment continues**: Defence ministries (UK MoD, US DoD, Korean military) continue funding because the capability is genuinely transformative
- **Key remaining challenges**: Winter-night energy storage, structural resilience, operational logistics (launch/recovery), regulatory frameworks

---

## 2. Stratospheric Balloons

### Operating Principle

Large balloons filled with helium (or hydrogen) that float at a target altitude in the stratosphere (18-25 km). Unlike HAPS planes, they are **lighter-than-air** — they don't need to generate lift, so they can carry much heavier payloads with much less complexity.

### Google Loon (Cancelled January 2021)

- **The most ambitious stratospheric balloon programme ever attempted**
- Used super-pressure balloons at ~20 km altitude to provide LTE cellular connectivity
- Each balloon covered ~5,000 km² (40 km radius)
- Achieved remarkable results:
  - 312 days aloft (single balloon endurance record)
  - Provided emergency connectivity after Hurricane Maria in Puerto Rico (2017)
  - Launched commercial service in Kenya (2020) with Telkom Kenya
- **Why it was cancelled**:
  1. **Unit economics never closed**: Each balloon lasted ~150 days on average (not the 312-day record). Manufacturing cost was reportedly $50,000-100,000 per balloon. Replacing balloons every 5 months was too expensive compared to terrestrial alternatives.
  2. **Station-keeping was imperfect**: Balloons can ride wind layers but cannot hold a precise position. You need a *constellation* of balloons cycling through to maintain coverage over one area, which multiplies the cost.
  3. **The telecom business case shifted**: By 2020, SpaceX Starlink and other LEO satellite constellations were progressing rapidly, offering a more scalable path to global connectivity.
  4. **Alphabet X prioritisation**: As an "X moonshot," Loon needed a path to becoming a self-sustaining business. After 10 years and reportedly $600M+ invested, the path wasn't clear.
- **Key lessons learned**:
  - Super-pressure balloon technology works — multi-month flights are achievable
  - Autonomous station-keeping via altitude adjustment (riding different wind layers) is feasible but imprecise
  - The machine learning system for predicting and exploiting wind patterns was genuinely innovative
  - Manufacturing at scale (thousands of balloons) drove costs down significantly
  - Loon's technology was not lost — it was transferred to other Alphabet projects and Loon alumni started companies (see Aerostar partnerships)

### Raven Aerostar

- **The leading operational stratospheric balloon provider today**
- Subsidiary of Raven Industries (acquired by CNH Industrial in 2021)
- Based in Sioux Falls, South Dakota
- **Thunderhead balloon system**: Super-pressure balloons for persistent stratospheric flight
- **Key capabilities**:
  - Flights of 30-90+ days routinely
  - Payloads up to ~30 kg (standard) or larger with bigger balloons
  - Station-keeping via altitude-layered wind riding (similar to Loon's approach)
  - Operational for US military and government customers (ISR, communications)
- **Notable contracts**: US Southern Command (SOUTHCOM) for counter-narcotics surveillance, various DoD programmes
- **Cost**: Significantly cheaper than satellites — estimated $1,000-5,000 per day of operation vs millions for satellite time
- **Current status (2025-2026)**: Actively flying operational missions. Probably the most mature and operational stratospheric persistence platform in existence today.

### World View

- Based in Tucson, Arizona
- **Two business lines**:
  1. **Stratollite**: Stratospheric balloon platform for remote sensing and communications (their original business)
  2. **Space tourism**: Pressurised capsule carried to ~30 km by a balloon for ~$125,000 per ticket (the higher-profile business)
- Stratollite has demonstrated multi-week flights with station-keeping
- **Current status**: Focused primarily on the tourism business (first commercial flights targeted for 2025-2026), but the Stratollite technology remains available for commercial/government customers

### Zero-Pressure vs Super-Pressure Balloons

| Characteristic | Zero-Pressure | Super-Pressure |
|---|---|---|
| **Envelope** | Open at bottom, vents gas | Sealed, pressurised |
| **Altitude control** | Ballast drop (go up) / gas vent (go down) | Differential heating/cooling |
| **Endurance** | Days to weeks (limited by ballast) | Months (no ballast needed) |
| **Diurnal cycle** | Large altitude swings day/night (~5 km) | Maintains altitude (~1 km swing) |
| **Cost** | Cheaper | More expensive (stronger envelope) |
| **Use case** | Scientific campaigns, short missions | Long-endurance persistence |
| **Material** | Polyethylene film | Polyethylene with reinforcement (biaxially oriented) |

Super-pressure balloons are the key technology for persistent stratospheric presence. The envelope must withstand internal pressure changes as solar heating warms the gas during the day. NASA's super-pressure balloon programme has flown balloons of 18M cubic feet volume carrying ~2,700 kg payloads for scientific missions.

### Station-Keeping: Wind Layer Surfing

The stratosphere has multiple wind layers moving in different directions and speeds at different altitudes. By changing altitude (typically ±1-2 km), a balloon can move between these layers to navigate:

- **How it works**: At 18 km, wind may blow east at 15 m/s. At 20 km, wind may blow west at 8 m/s. By adjusting buoyancy to change altitude, the balloon effectively "sails" between wind layers.
- **Altitude adjustment methods**: Pumping air into/out of an internal ballonet (air ballast), or using differential solar heating
- **Machine learning**: Loon pioneered using reinforcement learning to optimise altitude decisions given wind forecast data. Their system could keep a balloon within ~50 km of a target point for weeks.
- **Limitations**: You're always at the mercy of available winds. Some days/locations, all wind layers go the same direction. You cannot hover precisely — you orbit around the target area.
- **Constellation approach**: To ensure continuous coverage, you fly multiple balloons that cycle through the coverage area. When one drifts too far, another takes over. This requires 3-5x the number of balloons compared to "one balloon per spot."

### Endurance and Payload Capacity

- **Endurance**: Super-pressure balloons routinely achieve 30-100 days. Loon's record was 312 days. Multi-month flights are the norm for well-designed systems.
- **Payload capacity**: This is where balloons massively outperform HAPS planes:
  - Small stratospheric balloon: 5-30 kg payload
  - Medium: 30-200 kg
  - Large (NASA-class): up to 2,700 kg
  - Compare to Zephyr: ~5 kg payload
- **Cost estimates**:
  - Balloon manufacturing: $10,000-100,000 depending on size and type
  - Launch operations: $5,000-20,000 per launch
  - Daily operating cost: $1,000-5,000
  - Compare to satellite: $50M-500M+ to build and launch; $5,000-50,000/day to operate

---

## 3. Stratospheric Airships

### Operating Principle

Combine buoyancy (like balloons) with propulsion and solar power (like HAPS planes). The airship's helium provides most or all of the lift, while solar-powered propellers provide station-keeping thrust. The large surface area of the envelope provides ample space for solar cells.

### Thales Stratobus

- **French programme** by Thales Alenia Space
- 115m long, 34m diameter — enormous
- Target altitude: 20 km
- Design payload: 250 kg (massive compared to HAPS planes)
- Endurance target: 1 year continuous
- Solar cells on upper surface, batteries + regenerative fuel cells for night
- **Current status**: Has been in development since ~2014. Progress has been slow. As of 2024-2025, Thales was still in prototype/demonstrator phase. The programme has not been cancelled but has not achieved stratospheric flight. Schedule has slipped multiple times.
- **Key challenges**: The sheer size creates enormous structural and manufacturing challenges. Operating a 115m airship in the stratosphere where wind speeds can reach 30+ m/s is extremely demanding.

### Sceye

- Based in Roswell, New Mexico (formerly known as StratXX, then rebranded)
- Building large stratospheric airships for connectivity and Earth observation
- Backed by significant venture funding
- **Key claims**: 60m+ length, payloads of 100+ kg, endurance of months
- Successfully flew a prototype to stratospheric altitude in 2023
- **Current status (2025-2026)**: One of the more active stratospheric airship companies. Has been conducting test flights from New Mexico. Focused on providing broadband connectivity to underserved areas and environmental monitoring.
- **Business model**: Sell "stratospheric-as-a-service" — customers buy connectivity or observation data, not the airship itself.

### Why Haven't Stratospheric Airships Worked Yet?

They are, on paper, the ideal platform — but several factors have prevented success:

1. **Size and structural challenge**: To carry useful payload at 20 km (where air density is ~7% of sea level), you need enormous volume for buoyancy. A 200 kg payload requires roughly 2,800 m³ of helium at 20 km. The envelope must be ultralight yet strong enough to withstand pressure differentials, UV radiation, and wind loads.

2. **Wind resistance**: Unlike a balloon (which drifts with the wind and has no drag), an airship trying to hold station must fight the wind. At 20 km, winds can average 10-30 m/s. The drag on a 100m+ airship at even 10 m/s requires substantial power — which requires more solar cells and batteries — which requires more lift — which requires a bigger envelope. This is a viscious scaling loop.

3. **Thermal management**: During the day, solar heating can overpressure the envelope. At night, cooling causes the helium to contract, reducing lift. Managing this diurnal cycle for a structure the size of a football field is a serious engineering challenge.

4. **Launch and recovery**: Getting a 100m+ airship through the troposphere (where weather happens — rain, turbulence, icing, strong winds) is extremely risky. The tropopause crossing is the most dangerous phase.

5. **Helium**: Helium is expensive and a non-renewable resource. A large stratospheric airship requires thousands of cubic metres. Hydrogen would be cheaper and more buoyant but introduces flammability concerns (though at stratospheric altitude with minimal oxygen, the risk is much lower than at ground level).

### Advantages Over HAPS Planes

Despite the challenges, the theoretical advantages are significant:
- **Payload**: 100-500 kg vs 5-20 kg for solar planes
- **Power**: Much more surface area for solar cells
- **Hovering**: Can hold position rather than circling
- **Endurance**: No structural fatigue from continuous flight manoeuvres
- **Radar cross-section**: Large surface for antenna integration

---

## 4. Tethered Aerostats

### Operating Principle

Helium-filled balloons or blimps tethered to the ground by a cable. The cable provides both a physical anchor (station-keeping) and can carry power and data (fibre optic + electrical conductors). This solves the station-keeping and power problems simultaneously — at the cost of altitude and mobility.

### TCOM / Lockheed Martin PTDS

- **Persistent Threat Detection System** — the workhorse military aerostat
- 74m (243 ft) long tethered aerostat
- Operational altitude: ~3 km (10,000 ft)
- **Operational history**: Extensively used in Iraq and Afghanistan from 2004 onwards. At peak, over 60 aerostats were deployed across Afghanistan for persistent wide-area surveillance.
- Carries sophisticated radar and electro-optical/infrared (EO/IR) sensor payloads
- Payload capacity: 1,000+ kg (enormous)
- Endurance: **Weeks to months** continuously. Limited by weather (must be winched down in extreme winds/storms) and helium replenishment
- Cost: ~$15-20M per system (including ground station and sensors). Operating cost ~$10,000-20,000/day including crew.
- **Still operational**: Used along the US southern border and at various military installations

### JLENS (Joint Land Attack Cruise Missile Defense)

- Raytheon system using two tethered aerostats with radar
- 74m aerostats at ~3 km altitude
- One aerostat carried surveillance radar, the other carried fire-control radar
- **Infamous incident (2015)**: During a test deployment at Aberdeen Proving Ground, Maryland, one JLENS aerostat broke free of its tether and drifted across Pennsylvania, dragging its cable across power lines and causing widespread blackouts. It was eventually brought down.
- **Programme status**: Effectively dead after the incident and cost overruns (~$2.7B spent). The embarrassment of a runaway military blimp was a public relations disaster.
- **Lesson**: Tether reliability is critical. A broken tether turns an asset into a hazard.

### Altaeros BAT (Buoyant Airborne Turbine)

- Novel concept: a tethered aerostat carrying a wind turbine
- Flies at ~600m (2,000 ft) to access stronger, more consistent winds
- Originally developed at MIT
- Also designed to carry telecom equipment — combining power generation with communications relay
- **Current status**: Pivoted more toward the telecom relay application (brand name "SuperTower"). Concept is sound but commercialisation has been slow.

### Tethered Aerostat Summary

| Parameter | Typical Value |
|---|---|
| Altitude | 1-5 km (tropospheric, NOT stratospheric) |
| Endurance | Weeks to months (weather-limited) |
| Payload | 100-2,000+ kg |
| Station-keeping | Perfect (tethered) |
| Coverage radius | 50-100 km (for radar/comms at 3 km altitude) |
| Key limitation | Altitude (limited by tether weight and wind loads) |
| Weather vulnerability | Must winch down in storms (>60 kt winds) |
| Cost | $5-20M per system, $10-20K/day operations |

**Relevance**: Tethered aerostats are the most mature and operationally proven persistent airborne platform. They are not stratospheric, but they provide genuine weeks-to-months persistence with heavy payloads. For many applications (border surveillance, base protection, local communications), they are more practical than stratospheric solutions.

---

## 5. Thermal Soaring and Dynamic Soaring

### Autonomous Thermal Soaring

- **Concept**: Unpowered or minimally-powered gliders that detect and exploit thermals (columns of rising warm air) to stay aloft indefinitely, like soaring birds.
- **Research**: Significant academic work at MIT, Stanford, and Microsoft Research. Microsoft's "AI for Earth" project flew autonomous sailplanes in Nevada that used machine learning to find and exploit thermals.
- **How it works**: Onboard sensors (variometer, temperature, machine learning) detect thermals. The autopilot circles within the thermal to gain altitude, then glides to the next thermal. Net energy gain over a flight can be positive.
- **Limitations for persistence**:
  - Thermals are **daytime-only** (solar heating of ground creates thermals). No thermals at night means you must land or have battery reserves.
  - Thermals are **weather-dependent** — overcast days, rain, and winter reduce thermal activity dramatically.
  - **Altitude ceiling**: Thermals in the troposphere typically top out at 2-5 km. This is NOT stratospheric.
  - Works well for extending endurance from hours to a full day, but not for weeks/months.

### Dynamic Soaring

- **Concept**: Exploiting wind speed gradients (wind shear) to extract energy. Albatrosses do this — they fly patterns through the boundary layer where wind speed changes rapidly with altitude, gaining kinetic energy from the gradient.
- **Record**: Model aircraft using dynamic soaring in ridge lift have exceeded 800 km/h (500 mph). The technique works spectacularly when conditions are right.
- **Limitations for persistent platforms**:
  - Requires strong, consistent wind shear (typically found near ocean surfaces, ridgelines, or specific atmospheric layers)
  - The flight path is dictated by the wind pattern — you cannot hover or hold a station
  - Not applicable at stratospheric altitudes (the boundary layer shear that dynamic soaring exploits is a tropospheric phenomenon)
  - Extremely demanding on airframe structures (high g-loads in the manoeuvres)

### Practical Assessment

Thermal and dynamic soaring are **endurance extenders**, not persistence solutions:
- Useful for extending a drone's mission from 2 hours to 8-12 hours
- Not useful for weeks/months of continuous flight
- Not applicable at stratospheric altitudes
- Could complement a solar-powered system at lower altitudes (using thermals during the day reduces battery drain)
- **Not practical for a communications relay** that needs to be in a known position 24/7

---

## 6. Space-Based Alternatives (For Comparison)

### LEO Satellites (Starlink Model)

- Altitude: 340-550 km
- Orbital period: ~90 minutes
- **Coverage**: Global (with enough satellites). Starlink has 5,000+ satellites as of 2025.
- **Cost per satellite**: ~$250,000-500,000 (SpaceX has driven costs down dramatically)
- **Cost to launch**: ~$1,100/kg to LEO on Falcon 9 ($2,700/kg retail, but SpaceX internal cost is much lower)
- **Latency**: 20-40 ms (much better than GEO)
- **Bandwidth**: 100-300 Mbps per terminal
- **Lifetime**: 5-7 years per satellite
- **Key advantage**: Once in orbit, no weather concerns, no station-keeping fuel for years
- **Key disadvantage**: Requires massive constellation (hundreds to thousands) for continuous coverage; space debris concerns; cannot be easily updated or serviced

### GEO Satellites (Traditional Comms)

- Altitude: 35,786 km
- **Coverage**: ~1/3 of Earth's surface per satellite (3 satellites = global minus poles)
- **Cost**: $150M-400M per satellite + $50-100M launch
- **Latency**: 600 ms round-trip (problematic for interactive applications)
- **Bandwidth**: Very high (modern HTS satellites: 100+ Gbps total)
- **Lifetime**: 15-20 years
- **Key advantage**: One satellite covers a huge area for a very long time
- **Key disadvantage**: Enormous upfront cost, high latency, 3+ year build time

### Why Choose Stratospheric Over Space?

| Factor | Stratospheric | LEO Satellite | GEO Satellite |
|---|---|---|---|
| **Latency** | <1 ms | 20-40 ms | 600 ms |
| **Deployment time** | Hours to days | Months to years | 3-5 years |
| **Update/service** | Land and modify | Impossible | Impossible |
| **Regional focus** | Perfect — one platform over one area | Wasteful — constellation orbits entire Earth | Good — but expensive |
| **Resolution (imaging)** | Very high (20 km vs 500+ km) | Moderate | Poor |
| **Cost for one area** | $100K-$10M | $100M+ (need whole constellation) | $200M+ |
| **Regulatory** | Aviation rules (complex but known) | Space licensing (ITU, national) | Space licensing |
| **Recovery** | Can land and relaunch | Deorbits and burns up | Cannot recover |

**The strategic niche for stratospheric platforms**: When you need persistent coverage over a *specific region* (a country, a disaster zone, a border area, a maritime chokepoint), and you need it deployed quickly, with the ability to change the payload, at a fraction of satellite cost. The latency advantage is also significant for real-time applications.

---

## 7. Comprehensive Comparison Table

| Platform | Altitude | Endurance | Payload | Station-keeping | Approx. Cost | TRL | Weather Tolerance | Key Pros | Key Cons |
|---|---|---|---|---|---|---|---|---|---|
| **Solar HAPS (Zephyr)** | 18-25 km | 2 months (record 64 days) | 5-20 kg | Circles over area (~50 km orbit) | $5-20M/unit | 7-8 | Poor (fragile in turbulence) | Precise positioning, recoverable | Tiny payload, fragile, winter problem |
| **Super-pressure balloon** | 18-22 km | 1-10 months | 5-200 kg | Wind-layer surfing (~50 km accuracy) | $50-150K/unit | 8-9 | Moderate (rides above weather) | Cheap, proven, good payload | Cannot hover precisely, consumable |
| **Stratospheric airship** | 18-22 km | Months to 1 year (target) | 100-500 kg | Active propulsion (good) | $20-100M/unit | 4-6 | Moderate | Large payload, hovers, big solar area | Unproven, enormous, hard to launch |
| **Tethered aerostat** | 1-5 km | Weeks to months | 100-2,000 kg | Perfect (tethered) | $5-20M/system | 9 | Poor (must winch down in storms) | Proven, huge payload, powered via tether | Low altitude, immobile, weather-limited |
| **Thermal soaring drone** | 0.5-5 km | Hours to 1 day | 1-10 kg | Very poor (follows thermals) | $10-100K | 5-6 | Poor (needs thermals = fair weather) | No fuel needed, elegant | Daytime only, cannot hold station |
| **Dynamic soaring drone** | 0-0.5 km | Hours | 1-5 kg | None (follows wind gradient) | $10-50K | 3-4 | Needs specific wind conditions | Extreme speed, no fuel | Not for persistence, very niche |
| **LEO satellite** | 340-2,000 km | 5-7 years | N/A (is the payload) | Orbital mechanics | $0.3-5M/sat + launch | 9 | Immune | Long life, global, no weather issues | Needs constellation, can't service |
| **GEO satellite** | 35,786 km | 15-20 years | N/A | Stationkeeping fuel | $200-500M | 9 | Immune | Huge coverage, decades of life | Enormous cost, high latency, slow to deploy |

**TRL scale**: 1-3 = research, 4-6 = prototype/demo, 7-8 = operational prototype, 9 = fully operational

---

## 8. What's Actually Achievable for a Student/Startup?

### Realistic Assessment by Platform Type

**Stratospheric super-pressure balloon — MOST ACCESSIBLE**
- This is the most realistic entry point for a student or small team
- A basic high-altitude balloon (HAB) launch to 30+ km is achievable for under £500 (weather balloon, helium, payload, tracker)
- **But**: This gives you 2-3 hours, not persistence. The balloon ascends, bursts, and the payload parachutes down.
- A super-pressure balloon for multi-day flight is much harder — requires custom envelope fabrication, gas management, and more sophisticated systems. Budget: £5,000-50,000+.
- **Open-source projects**: The amateur HAB community is very active. UKHAS (UK High Altitude Society) has extensive resources. https://ukhas.org.uk/

**Solar HAPS plane — EXTREMELY DIFFICULT**
- Building a solar-powered aircraft that can fly overnight is a PhD-level project
- The power-weight ratio required is extraordinary — every gram matters
- Estimated minimum budget for a meaningful demonstrator: £50,000-200,000+
- Some university groups have built solar drones that fly during the day, but overnight flight remains the critical challenge

**Tethered aerostat — MODERATELY ACCESSIBLE**
- A small tethered balloon (weather balloon on a line) is trivially easy
- A proper tethered aerostat with a useful payload (cameras, comms) at 100-500m is achievable for £2,000-10,000
- This is actually a practical and useful project with real applications
- Could be combined with your existing drone platform — tethered operation of a multirotor for persistent surveillance is a real commercial product category

**Thermal soaring — ACCESSIBLE AND EDUCATIONAL**
- Adding thermal detection and autonomous soaring to your drone platform is achievable
- ArduPilot has a thermal soaring mode (SOAR) that works with fixed-wing platforms
- Good research project with published academic papers to reference
- Budget: Existing platform + software development

### Open-Source Stratospheric Projects and Communities

1. **UKHAS (UK High Altitude Society)**: The go-to resource for amateur high-altitude ballooning in the UK. Wiki, trackers, launch guides, radio systems. https://ukhas.org.uk/
2. **Project Horus** (Australia): Open-source HAB tracking and telemetry
3. **SondeHub**: Open platform for tracking radiosondes and HABs
4. **Global Space Balloon Challenge**: Annual competition (or was — check current status) for student teams to fly HAB payloads
5. **GSBC / Stratonaut**: Student-accessible balloon competitions
6. **ArduPilot**: Open-source autopilot with high-altitude balloon tracker firmware

### Can Your LARGE Tier Airframe Reach the Stratosphere?

**Almost certainly not. Here's why:**

The stratosphere starts at approximately 11-12 km at UK latitudes (tropopause). Let's analyse the physics:

1. **Air density**: At 12 km, air density is ~0.31 kg/m³ (25% of sea level's 1.225 kg/m³). At 20 km, it's ~0.088 kg/m³ (7% of sea level). Your propellers and wings are designed for sea-level air.

2. **Propeller efficiency collapse**: Propeller thrust is proportional to air density. A propeller generating 10 N of thrust at sea level generates only 2.5 N at 12 km and 0.7 N at 20 km. You would need either:
   - Much larger propellers (impractical beyond a point)
   - Much higher RPM (motor and prop tip speed limits)
   - Fundamentally different prop design (large, slow, high-pitch — like Zephyr's 4-5m diameter props)

3. **Reynolds number effects**: At low air density and the small scale of your platform, Reynolds numbers drop below 100,000 where airfoil performance degrades dramatically. Conventional airfoils stall or produce minimal lift. Stratospheric aircraft use specialised low-Reynolds-number airfoils.

4. **Power requirements**: To maintain altitude at low density, you need higher airspeed (lift = ½ρv²SCL — if ρ drops, v must increase). Higher airspeed at low density still requires more power than at sea level for the same aircraft.

5. **Battery energy density**: Even with the best LiPo/Li-ion cells (~250 Wh/kg), you cannot carry enough battery to sustain powered flight at 20 km for more than a few hours, let alone overnight.

### Maximum Practical Altitude for Your Platform

Based on typical multirotor/fixed-wing drone characteristics:
- **Multirotor configuration**: Maximum ~5-6 km with standard components. World record for a multirotor is ~10 km (DJI-class frame with highly optimised props), but this is a brief ascent, not sustained flight.
- **Fixed-wing configuration**: Maximum ~8-10 km with significant modifications (larger prop, higher-pitch, optimised airfoil). Sustained flight at this altitude requires a very efficient platform.
- **Practical ceiling for useful missions**: 3-5 km. Above this, performance degrades rapidly and you're in controlled airspace with serious regulatory issues.
- **To reach the stratosphere (>12 km)**: You would need a purpose-built airframe with enormous wingspan (10m+), ultra-low wing loading (<5 kg/m²), specialised low-Re airfoils, and either solar power or an enormous battery. This is a fundamentally different aircraft from your modular platform.

**Recommendation**: Your platform is excellent for tropospheric operations (0-5 km). For stratospheric ambitions, a high-altitude balloon is the realistic path — launch a payload to 30+ km for a few hundred pounds. Don't try to fly there with a propeller-driven drone.

---

## 9. UK-Specific Considerations

### UK CAA Regulations for Stratospheric Operations

The UK regulatory framework for stratospheric platforms is **still evolving** but there are pathways:

1. **High-altitude balloon launches**: Regulated under the Air Navigation Order 2016 (ANO). You need permission from the CAA under Article 253 to launch a balloon above 60,000 ft or with a payload exceeding certain mass limits. For small HAB launches (< 2 kg payload, latex balloon), a standard NOTAM (Notice to Airmen) may suffice, but you MUST contact the CAA. The UKHAS community has a well-established process for this.

2. **BVLOS drone operations above FL600 (60,000 ft)**: The CAA is developing a framework. As of 2025, there is no standard "off the shelf" approval process for stratospheric UAS. You would need a bespoke Operational Authorisation from the CAA, demonstrating:
   - Safety case (what happens if it fails at 20 km?)
   - Separation from manned aviation (commercial aircraft cruise at 10-12 km)
   - Communication and tracking
   - Recovery/termination procedures
   - Insurance

3. **The UK is actually ahead of many countries**: The CAA has been proactive about HAPS regulation, partly because Airbus Zephyr is a UK programme and BAE PHASA-35 is UK-developed. The CAA has published CAP 722 (UAS policy) which includes high-altitude considerations.

4. **Airspace classes**: UK airspace above FL600 (18,290 m / 60,000 ft) is generally Class A or uncontrolled (depending on location). Stratospheric platforms would operate above most manned traffic, which simplifies separation — but the transit through controlled airspace (FL0-FL600) during launch/recovery is the regulatory pinch point.

5. **For amateur HAB**: The process is well-established. Contact the CAA at least 28 days before launch, specify launch site, expected trajectory, payload details. Many UK sites are used regularly (Cambridge, Elsworth, various others). UKHAS has a flight document process.

### UK Companies in the Stratospheric Space

1. **Airbus Defence and Space (Farnborough)**: Zephyr HAPS programme. The primary UK player. Zephyr is designed and built at the Farnborough facility. This is world-leading capability.

2. **BAE Systems (various UK sites)**: PHASA-35 originated from Prismatic Ltd (acquired). BAE integrates it into broader UK defence programmes.

3. **QinetiQ**: UK defence technology company with heritage in high-altitude work. QinetiQ's predecessor (DERA/DRA) was involved in early HAPS research. They operate the Boscombe Down test facility.

4. **DSTL (Defence Science and Technology Laboratory)**: The UK government's defence research agency. Has funded and evaluated various HAPS concepts. Based at Porton Down, Wiltshire.

5. **Various startups**: The UK has a growing ecosystem of companies in adjacent spaces — satellite data, drone services, communications. Several have expressed interest in stratospheric platforms as delivery mechanisms.

### Regulatory Path for a Student Project

For a **high-altitude balloon** (most realistic):
1. Join UKHAS community and learn the established procedures
2. Build and test payload at ground level
3. Apply for CAA permission via the standard UKHAS process
4. Launch from an established site with experienced mentors
5. This is entirely achievable and legal — hundreds of UK launches happen each year

For a **stratospheric drone** (much harder):
1. This would require a bespoke CAA engagement process
2. You would need to demonstrate a mature safety case
3. Realistically, this is a post-university/company endeavour, not a student project
4. Testing would likely need to happen overseas (Zephyr tests at Yuma, Arizona; PHASA-35 at Woomera, Australia — UK weather and airspace are not ideal for testing)

---

## Key Takeaways

1. **No platform has fully solved persistent stratospheric flight** as a routine, operational capability. Zephyr's 64 days is the record but it crashed on subsequent flights. Balloons routinely do months but can't hold precise station.

2. **Balloons are the most mature technology** for stratospheric persistence. Raven Aerostar is operationally deploying them today. If you want to "do something stratospheric," start here.

3. **Solar HAPS planes are the highest-profile approach** but remain fragile and payload-limited. The overnight energy problem at high latitudes is unsolved for year-round operation.

4. **Stratospheric airships are the theoretically ideal solution** but no one has made them work yet. If someone cracks this, it could be transformative.

5. **Tethered aerostats are the boring but working answer** for persistent airborne platforms below 5 km. The US military has used them operationally for 20+ years.

6. **For your project specifically**: High-altitude ballooning is the accessible entry point. Your LARGE-tier drone cannot reach the stratosphere due to fundamental physics (air density, Reynolds number, propeller efficiency). But a HAB payload launch to 30+ km is achievable on a student budget through UKHAS. Consider this as a complementary project — your modular drone platform for 0-5 km operations, and a balloon-launched payload for stratospheric data collection.
