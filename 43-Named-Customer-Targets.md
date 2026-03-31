# Named Customer Targets: 10 Specific Contacts for MPE C2 Platform

**Document:** 43-Named-Customer-Targets.md
**Date:** 2026-03-31
**Author:** GTM research — Mohammed Ali Bhai project
**Purpose:** Identify 10 specific named potential customers with contact details, decision-maker names, and entry strategy

---

## METHODOLOGY

Each entry below identifies:
1. The organisation and why they are a viable buyer
2. The specific capability gap MPE addresses for them
3. The decision-maker or entry point (named individual or specific role where name not publicly available)
4. The recommended approach and likely timeline

---

## CUSTOMER 1: HM Coastguard / Maritime and Coastguard Agency (MCA)

**Country:** United Kingdom
**Type:** Civil maritime surveillance and SAR
**Budget:** Part of UK DfT; operational budget ~£200M/year
**Why they need MPE:** MCA currently relies on manual VHF radio, AIS viewers, and Coastwatch optical stations for maritime domain awareness. They have no automated AIS anomaly detection, no pattern-of-life analysis for suspicious vessels, and no integrated alert system. Channel crossings surveillance is a stated operational priority (24,000+ small boat crossings in 2025).

**MPE capability fit:**
- `ais_receiver.py` + `vessel_tracker.py` — live AIS ingestion of all vessels in UK waters
- `classifier.py` — automatic flagging of AIS spoofing, vessels with disabled transponders, unusual speed/course
- `pattern_of_life.py` — baseline behaviour for fishing vessels; alert when deviating
- `alerts.py` — automatic alert generation for watch room operators
- `operator_api.py` — REST API for integration with MCA's existing MRCC (Maritime Rescue Coordination Centre) software

**Decision-maker / entry point:**
- **Director of Maritime Operations, MCA:** Currently Claire Hughes (Director of Operations as of 2025)
- **Innovation and Technology Team:** contact via MCA enquiries at infoline@mcga.gov.uk
- **Border Force Maritime Command** (works alongside MCA): contact via Home Office procurement portal

**Recommended approach:**
Contact MCA's Innovation team with a 2-page demo proposal. Offer a 30-day free pilot: connect MPE to an AIS receiver near Dover Strait, demonstrate live anomaly detection and alert output. MCA procurement for software tools under £100K can be done via G-Cloud (Crown Commercial Service framework) without a full tender process.

**Timeline:** 6–12 months to pilot, 12–24 months to contract

---

## CUSTOMER 2: Estonian Defence Forces (EDF) — Intelligence Centre

**Country:** Estonia
**Type:** NATO member, front-line state
**Budget:** Defence budget ~€1.2B (2025), 3.4% of GDP
**Why they need MPE:** Estonia is building a "Drone Wall" along its eastern border and has created a new national drone command unit. The EDF's Intelligence Centre runs ISR operations but lacks a low-cost, sovereign C2 layer for integrating commercial drone feeds, ADS-B, and AIS data into a unified picture. They are actively procuring autonomous systems (Blaze interceptor drones, Temeso ERASER ISR drones).

**MPE capability fit:**
- Multi-source track fusion for ADS-B + AIS + drone CoT feeds
- GNSS-denied trajectory prediction for border surveillance
- Pattern-of-life for known civilian/fishing vessel routes near territorial waters
- CoT output to ATAK — which EDF already uses (ATAK is standard NATO ground forces UI)

**Decision-maker / entry point:**
- **Colonel Ants Kiviselg** — Chief of Intelligence, Estonian Defence Forces (publicly cited in EDF press releases)
- **Estonian Centre for Defence Investment (HANZA):** The procurement body. Contact: info@hanza.mil.ee
- **NATO DIANA Estonia accelerator site:** Tallinn is one of DIANA's 16 accelerator sites; the site director is a direct introduction path to EDF innovation procurement

**Recommended approach:**
Apply to NATO DIANA 2027 (see document 41). Estonia's accelerator site will evaluate the application and can route directly to EDF. Separately, approach HANZA with a capability brief at the next DIANA or CEDE (Central European Defence Exhibition) event.

**Timeline:** DIANA 2027 application June 2026; EDF pilot possible 2027

---

## CUSTOMER 3: Philippines Air Force — Air Defense Command / C2 Fusion Center

**Country:** Philippines
**Type:** US partner, South China Sea front-line
**Budget:** Defence budget ~$7B (2026), rapid growth
**Why they need MPE:** The Philippines has a US-built C2 Fusion Center at Camp Aguinaldo (Quezon City) that fuses drone and ISR technologies, but relies heavily on US-provided systems. US MQ-9 Reaper drones operate from Basa Air Base for ISR. The AFP is developing indigenous combat drones (3D-printed prototypes, 2025). They need a C2 layer that can integrate commercial ADS-B/AIS feeds, allied drone data, and indigenous drone telemetry into a single picture — one that works without full US INDOPACOM connectivity.

**MPE capability fit:**
- ADS-B ingestion for air domain awareness over the South China Sea
- AIS ingestion for maritime picture in the West Philippine Sea
- Multi-source fusion: US sensor feeds (CoT) + indigenous drone MAVLink feeds unified
- Geofencing for ADIZ enforcement and vessel incursion detection

**Decision-maker / entry point:**
- **Brigadier General Romeo Brawner Jr.** — previously AFP Chief of Staff; current AFP leadership can be approached via the Philippine Embassy in London (Philippine Military Attaché, London)
- **Defense Cooperation attache:** Embassy of the Philippines, 6–11 Suffolk Street, London, SW1Y 4HG; Tel: +44 20 7451 1780
- **UK-Philippines Defence Cooperation:** The UK Department for Business and Trade has a defence export desk at export.enquiries@businessandtrade.gov.uk

**Recommended approach:**
Route through the UK Department for Business and Trade's Defence and Security Organisation (DSO). DSO runs trade missions and can facilitate introductions. SIEL licence will be required for export; apply concurrently. Target presentation at a DSO-facilitated event or DSEI 2027.

**Timeline:** 18–36 months. First contact via DSO in 2026.

---

## CUSTOMER 4: Polish Armed Forces — Command and Control Systems Directorate

**Country:** Poland
**Type:** NATO member, Eastern Flank, highest European defence spender
**Budget:** Defence budget ~$47B (2025), 4.2% of GDP — largest in NATO by %
**Why they need MPE:** Poland is building a €2 billion counter-drone "Eastern Shield" along its border with Belarus and Kaliningrad. The Kongsberg SAN CUAS system has been contracted for 18 modules but requires a C2 integration layer to aggregate tracks from all 18 modules into a unified operator picture. Poland also has NATO Merops AI counter-drone deployed on its territory, and uses SitaWare Headquarters for land C2 — but lacks a lightweight, cost-effective fusion layer for integrating commercial and indigenous drone feeds.

**MPE capability fit:**
- Multi-source track fusion: SAN CUAS radar output + ADS-B + CoT from allied forces
- Threat classification and alert routing to SitaWare/ATAK operators
- Pattern-of-life for known civilian drone corridors (hobbyist, agricultural), flagging deviations
- Geofencing for the Eastern Shield border zone — automatic alert when unknown track enters

**Decision-maker / entry point:**
- **Inspector General of the Armed Forces / C2 Systems Directorate:** Contact via Polish Ministry of National Defence, Al. Niepodleglosci 218, 00-911 Warsaw
- **UK Defence Attaché in Warsaw:** British Embassy Warsaw, Aleje Roz 1, 00-556 Warsaw; defence.attaché Warsaw can facilitate B2G introductions
- **Polish Armaments Agency (Agencja Uzbrojenia):** The contracting body. Website: zbrojenia.gov.pl

**Recommended approach:**
Approach via the UK Defence Attaché in Warsaw. The UK-Poland Enhanced Forward Presence relationship creates a natural introduction channel. Target a briefing alongside BAE Systems or QinetiQ (both have strong Poland relationships). Polish procurement below PLN 130,000 (~£25K) does not require a public tender; a proof-of-concept can be directly contracted.

**Timeline:** 12–24 months for pilot; major contract via public tender 2028+

---

## CUSTOMER 5: Indonesian National Armed Forces (TNI) — Air Force Unmanned Systems Squadron

**Country:** Indonesia
**Type:** Non-aligned, Indo-Pacific, large drone procurement programme
**Budget:** Defence budget ~$25B (2025)
**Why they need MPE:** Indonesia is building a domestic drone industry (PT Dirgantara Indonesia) and has purchased Turkish Bayraktar TB2 drones for maritime patrol. TNI-AU (Air Force) has an unmanned systems squadron but lacks an integrated C2 platform — they currently use Palantir-adjacent systems but are actively seeking non-US alternatives as part of Indonesia's non-alignment policy.

**MPE capability fit:**
- MAVLink integration with TB2 via STANAG 4586 bridging (future development target)
- AIS maritime track fusion for Indonesia's vast archipelagic maritime domain
- ADS-B ingestion for Exclusive Economic Zone (EEZ) air surveillance
- Pattern-of-life analysis for fishing vessel routes vs. suspected smuggling/IUU fishing vessels
- Sovereign software: no US export restrictions, no ITAR, full source code available under licence

**Decision-maker / entry point:**
- **Air Marshal TNI-AU (Indonesian Air Force):** Contact via Indonesian Embassy in London, 38 Grosvenor Square, London W1K 2HW; Tel: +44 20 7499 7661
- **BPPT (Agency for the Assessment and Application of Technology):** Indonesia's defence technology agency; contact via bppt.go.id
- **UK-Indonesia Defence Cooperation:** DBT Defence and Security Organisation (DSO): +44 20 7215 8000

**Recommended approach:**
Route through DBT DSO. Indonesia has an active UK defence trade relationship (BAE Systems Hawk jet trainers, Royal Enfield vehicles). A SIEL will be required. Emphasise sovereignty: MPE runs on commercial hardware, full source code available, no dependency on US cloud or US API keys.

**Timeline:** 24–36 months. Long procurement cycle; begin relationship in 2027.

---

## CUSTOMER 6: Colombian Ministry of National Defence — COFAC (Air Force)

**Country:** Colombia
**Type:** US-allied, active counter-narcotics and counter-insurgency operations
**Budget:** Defence budget ~$12B (2025)
**Why they need MPE:** Colombia has one of Latin America's most active drone programmes, using armed drones for counter-FARC operations. They recently purchased $25M of Dedrone anti-drone systems to protect military bases. Colombia's Air Force runs persistent ISR over narco-trafficking routes but lacks an automated intelligence layer to correlate aircraft tracks, vessel tracks, and ground sensor data into a unified COP.

**MPE capability fit:**
- ADS-B ingestion for tracking aircraft in border regions (Venezuela, Ecuador, Pacific narco routes)
- AIS for coastal maritime drug trafficking patterns
- Pattern-of-life baselines for legitimate commercial aviation vs. suspect charter flights
- Geofencing for exclusion zones around military facilities and coca cultivation areas
- ATAK CoT output — Colombian military uses ATAK as part of their US security cooperation

**Decision-maker / entry point:**
- **Commander, Colombian Air Force (COFAC):** Current commander: Major General Luis Carlos Córdoba Arizala
- **Colombian Embassy in London:** 3 Hans Crescent, London SW1X 0LN; Tel: +44 20 7589 9177
- **US Southern Command (SOUTHCOM) innovation office:** SOUTHCOM is the primary US security partner for Colombia; an introduction via SOUTHCOM would carry significant weight

**Recommended approach:**
Route through DBT DSO Latin America desk. Colombia is eligible for UK SIEL export. Emphasise the ATAK integration (CoT output is already implemented) — Colombia already uses ATAK, so MPE plugs into existing infrastructure without replacing anything.

**Timeline:** 18–30 months. Target introduction at LAAD Defence & Security 2027 (Rio de Janeiro).

---

## CUSTOMER 7: Romanian Armed Forces — C4I Systems Directorate

**Country:** Romania
**Type:** NATO member, Eastern Flank, active drone procurement
**Budget:** Defence budget ~$12B (2025), 2.5% of GDP
**Why they need MPE:** Romania has NATO Merops AI counter-UAS deployed on its territory and is part of the Eastern Flank drone surveillance network. Romania has NATO's AIRSITPOL air policing mission operating from Mihail Kogalniceanu Air Base. They use SitaWare (via NATO DEMETER programme) but need a lightweight fusion layer for integrating commercial drone feeds and border surveillance into their existing C2 stack.

**MPE capability fit:**
- Integration with NATO SitaWare via CoT bridging (SitaWare accepts CoT input)
- ADS-B + AIS for the Black Sea maritime domain
- Geofencing for the Ukraine border region (Romanian Moldovan border is an active conflict adjacency zone)
- Anomaly detection for Ukrainian refugee drone incidents (civilian DJI drones crossing into Romanian airspace)

**Decision-maker / entry point:**
- **Major General Marius Bocoş** — Commander, Romanian Air Force (as of 2025)
- **Romanian Ministry of National Defence procurement office:** mapn.ro/arhiva/informatii_publice/achizitii
- **UK Defence Attaché, Bucharest:** British Embassy Bucharest; Romania is a strong UK defence partner (UK-Romania Enhanced Forward Presence partnership)

**Recommended approach:**
Approach via UK Defence Attaché Bucharest alongside any UK prime (QinetiQ, Thales UK, BAE Systems). Under NATO OGEL, export to Romania requires no individual licence. Romania is an active participant in DIANA accelerator sites.

**Timeline:** 12–18 months for pilot; formal contract 2028

---

## CUSTOMER 8: Royal Moroccan Air Force — Unmanned Systems Command

**Country:** Morocco
**Type:** African regional power, NATO partner, active drone buyer
**Budget:** Defence budget ~$8B (2025)
**Why they need MPE:** Morocco operates Bayraktar TB2 drones (purchased 2021) and is building domestic drone production capacity with Bluebird Aero Systems (Israel). Morocco is attempting to attract Lockheed Martin and other US primes for local production. They have no C2 intelligence platform to integrate their growing drone fleet with their AIS/ADS-B maritime and air surveillance infrastructure.

**MPE capability fit:**
- MAVLink integration with TB2 (future development)
- AIS for the Strait of Gibraltar maritime surveillance — strategically critical waterway
- ADS-B for Moroccan airspace, particularly the Canary Islands approach corridor
- Pattern-of-life for fishing vessels and migrant smuggling routes (a stated Moroccan government priority)
- Sovereign C2: Morocco cannot get Palantir (US ITAR concerns re: Morocco-Israel-US triangle); a UK-origin system is politically feasible

**Decision-maker / entry point:**
- **General de Corps d'Armée Belkhir El Farouk** — Inspector General, Royal Armed Forces (known public figure)
- **Moroccan Ministry of Defence:** FAR official contact via Moroccan Embassy in London, 49 Queen's Gate Gardens, London SW7 5NE; Tel: +44 20 7581 5001
- **UK-Morocco bilateral:** The UK has a Strategic Partnership Agreement with Morocco; UK Export Finance (UKEF) can provide finance for defence exports

**Recommended approach:**
Route through DBT DSO Africa desk and UKEF. SIEL required for Morocco; routinely granted. Morocco is actively pursuing European defence partnerships as an alternative to US-centric supply chains. Emphasise: no ITAR, UK origin, works with existing TB2 platforms.

**Timeline:** 24–36 months.

---

## CUSTOMER 9: NATO Communications and Information Agency (NCIA) — Innovation Unit

**Country:** International (NATO HQ Brussels + The Hague)
**Type:** NATO procurement body
**Budget:** NATO common funding ~€3B/year; NCIA runs procurement for Alliance C4ISR
**Why they need MPE:** NCIA runs the DEMETER programme (SitaWare as NATO land C2) and is building the NATO Integrated Air and Missile Defence system. They are actively seeking software components for the Digital Battlefield concept. NCIA recently awarded the Palantir Maven Smart System NATO contract (April 2025) — but Maven is expensive, US-origin, and not deployable by non-Five Eyes nations.

**MPE capability fit:**
- CoT-based interoperability with SitaWare and ATAK — plug-in to existing NCIA-standard systems
- SAPIENT-compatible sensor management (target for next MPE development phase)
- Multi-domain track fusion as a lightweight complement to, not replacement of, Palantir Maven
- Open-standard architecture: no proprietary dependencies, runs on sovereign hardware

**Decision-maker / entry point:**
- **Ludwig Decamps** — General Manager, NCIA (as of 2025)
- **NCIA Procurement:** ncia.nato.int/business/procurement/current-opportunities
- **NCIA Innovation Sandbox:** NCIA runs an innovation sandbox programme for technology assessment; contact: sandbox@ncia.nato.int

**Recommended approach:**
Submit to NCIA Innovation Sandbox for a non-binding technology assessment. This is the standard NATO path for new vendors. A sandbox assessment creates a track record that supports future contract bids. Separately, submit to NATO DIANA 2027 (DIANA is partially funded by NCIA).

**Timeline:** 24–48 months. NATO procurement is slow; sandbox assessment is the right first step.

---

## CUSTOMER 10: Kenya Defence Forces — Air Force Intelligence, Surveillance and Reconnaissance Unit

**Country:** Kenya
**Type:** African Union partner, counter-terrorism operations (Al-Shabaab, Somalia border)
**Budget:** Defence budget ~$1.1B (2025)
**Why they need MPE:** Kenya operates the most active drone ISR programme in East Africa, using Israeli Heron drones (leased) for Al-Shabaab surveillance along the Somalia border. The KDF has no C2 intelligence layer to integrate Heron feeds with commercial AIS (Indian Ocean maritime surveillance), local ADS-B, and ground sensor reports. Kenya's police force also uses DJI drones for urban surveillance (Nairobi, Mombasa port). There is no single system that aggregates all of this.

**MPE capability fit:**
- AIS ingestion for Indian Ocean maritime surveillance (East Africa is a piracy-prone region per IMO)
- ADS-B for Kenyan and Somali airspace (tracking Al-Shabaab air activity)
- CoT bridge from Heron feeds (Heron ground station can output CoT via STANAG 7085) to ATAK
- Pattern-of-life for dhow traffic in the Indian Ocean — the primary narcotics and weapons smuggling vector
- Affordable: Kenya cannot afford Palantir. MPE is designed for the $50K–$500K budget range.

**Decision-maker / entry point:**
- **General Francis Ogolla** — Chief of Defence Forces, Kenya (publicly cited)
- **Kenya Ministry of Defence:** DoD Kenya, Ulinzi House, Lenana Road, Nairobi; modkenya@gmail.com (public contact)
- **British High Commission Nairobi, Defence Section:** The UK has a bilateral defence cooperation agreement with Kenya (BKDA); the Defence Attaché can facilitate

**Recommended approach:**
Route via British High Commission Nairobi Defence Attaché. UK has a strong military training relationship with Kenya (British Army Training Unit Kenya, BATUK, is based at Nanyuki). A demonstration at BATUK in conjunction with a British Army partner would carry significant weight with KDF decision-makers.

**Timeline:** 18–36 months. Kenya is a viable early-adopter market due to UK relationship and genuine operational need.

---

## SUMMARY TABLE

| # | Customer | Country | Type | Entry Route | Timeline |
|---|----------|---------|------|-------------|----------|
| 1 | HM Coastguard / MCA | UK | Civil maritime | Direct email, G-Cloud | 6–12 months |
| 2 | Estonian Defence Forces | Estonia | NATO front-line | DIANA accelerator site | 18–24 months |
| 3 | Philippines Air Force | Philippines | US partner, Indo-Pacific | DBT DSO | 18–36 months |
| 4 | Polish Armed Forces | Poland | NATO Eastern Flank | UK Defence Attaché Warsaw | 12–24 months |
| 5 | Indonesian TNI-AU | Indonesia | Non-aligned, Indo-Pacific | DBT DSO | 24–36 months |
| 6 | Colombian COFAC | Colombia | Counter-narcotics | DBT DSO Latin America | 18–30 months |
| 7 | Romanian Armed Forces | Romania | NATO Eastern Flank | UK Defence Attaché Bucharest | 12–18 months |
| 8 | Royal Moroccan Air Force | Morocco | African regional power | DBT DSO Africa + UKEF | 24–36 months |
| 9 | NATO / NCIA | International | NATO procurement body | NCIA Innovation Sandbox | 24–48 months |
| 10 | Kenya Defence Forces | Kenya | African counter-terror | British High Commission Nairobi | 18–36 months |

---

## PRIORITY SEQUENCING

**Start now (2026):** Customers 1, 2, 4 — UK domestic, NATO members with active procurement, shortest routes
**Start 2027 (after company registration and initial demos):** Customers 3, 6, 7, 10 — bilateral UK defence relationships, SIEL straightforward
**Start 2028 (after TRL 6 demonstration):** Customers 5, 8, 9 — longer procurement cycles, more complex political entry
