# DASA / UKDI Competition Research: Active Calls for C2, ISR, and Drone Autonomy

**Document:** 41-DASA-UKDI-Competition-Research.md
**Date:** 2026-03-31
**Author:** GTM research — Mohammed Ali Bhai project
**Purpose:** Identify currently open UK government innovation competitions relevant to the MPE C2 platform

---

## CONTEXT: DASA → UKDI TRANSITION

The Defence and Security Accelerator (DASA) is transitioning into UK Defence Innovation (UKDI), a broader body that absorbed DASA's Open Call function. The Open Call for Innovation closed after CY2025 Cycle 4 (extended to 13 January 2026). The new UKDI service will reopen before UKDI Full Operating Capability in **July 2026**.

For the period March–July 2026, the main active mechanisms are:
1. **Themed competitions** run by UKDI on behalf of DSTL (separate from the closed Open Call)
2. **NATO DIANA** (not DASA, but the best live opportunity for a team at this stage)
3. **Innovate UK / DSTL bilateral contracts** for specific capability programmes

---

## COMPETITION 1: UKDI Innovation Support to Operations — Phase 3, Cycle 7

**Status: OPEN — deadline 12 May 2026**

**Organisation:** UK Defence Innovation (UKDI) on behalf of the Ministry of Defence
**Contact:** accelerator@dstl.gov.uk
**Reference URL:** https://iuk-business-connect.org.uk/opportunities/uk-defence-innovation-competition-innovation-support-to-operations-phase-3-cycle-7/
**Funding:** Up to £350,000 per proposal (ceiling £1,000,000 total across funded projects)
**Project duration:** Maximum 6 months from contract start (aimed September 2026)
**TRL required:** Minimum TRL 6 by project end
**Eligibility:** UK-registered companies and organisations; collaboration encouraged

### Challenge Areas (7 total)

| # | Challenge | Description | MPE Relevance |
|---|-----------|-------------|---------------|
| 1 | Counter-UAS Interceptor Sensors | Sensors for high-speed C-UAS at combined closing speeds up to Mach 1, cost <£2,000/unit | Low (hardware) |
| 2 | One-Way Attack UAS Seeker | Passive seeker for sub-300kph systems resisting IR/visible decoys | Low (hardware) |
| 3 | UAS Survivability | Low-cost radar-absorbent materials, multi-spectral decoys | Low (hardware) |
| 4 | UAS Navigation | Autonomous GNSS-denied navigation, ≥50m positional accuracy (objective 5m) | **HIGH — MPE's track fusion + geofencing + predictor module** |
| 5 | Telemetry Data | LPD, jam-resistant telemetry >300km from low-altitude aircraft | Medium (comms layer) |
| 6 | Maritime Autonomous Navigation | Unmanned surface vessels at 60 knots, 48h endurance, GNSS-denied | Medium (AIS + track fusion angle) |
| 7 | Maritime Terminal Guidance | Automated terminal guidance using onboard FLIR cameras and radar | Low (hardware) |

### Assessment for MPE

Challenge 4 (UAS Navigation) is the strongest fit: MPE's `geofence.py`, `predictor.py`, and `track_manager.py` provide a software layer for GNSS-denied autonomous operation. However, the competition is hardware-oriented — they want the navigation solution to be onboard the UAS, not a ground-side C2 system. A credible submission would need a hardware partner (e.g., a UK drone manufacturer like Blue Bear Systems, Windracers, or BAE Systems ASTREA).

**Recommended action:** Pursue as a consortium proposal with a UK UAS manufacturer as prime. MPE contributes the C2/intelligence layer; the hardware partner brings the airframe and navigation compute. This is a realistic path to a funded pilot by September 2026.

---

## COMPETITION 2: Autonomous Sensor Management and Sensor Counter Deception — Phase 2

**Status: CLOSED (deadline was 10 February 2026)**

**Organisation:** DASA / DSTL
**Contact:** accelerator@dstl.gov.uk
**Reference URL:** https://www.gov.uk/government/news/1m-competition-launched-to-advance-autonomous-sensor-technologies
**Funding:** £1,000,000 total; expected to fund 2 collaborative projects
**Project period:** May 2026 – December 2027 (minimum 18 months)
**TRL required:** TRL 6 by completion

### What They Wanted

"Practical autonomous sensor management methods to counter activity designed to deceive Intelligence, Surveillance and Reconnaissance (ISR)." Must comply with the **SAPIENT open standard** for ISR enterprise integration. Solutions must use real sensing networks for demonstration.

### Why This Matters Even Though It's Closed

This competition maps almost exactly to what MPE does:
- AIS spoofing detection (`classifier.py` position jump rule) → sensor counter-deception
- Multi-source fusion (`track_manager.py`) → autonomous sensor management
- Pattern of life baseline deviation → anomaly detection for deceived ISR

The SAPIENT standard integration requirement is new — this is a concrete protocol target for MPE's next development phase. The DSTL team that ran this competition (contact: accelerator@dstl.gov.uk) is the right entry point for a Phase 3 follow-on.

**Recommended action:** Email DSTL at accelerator@dstl.gov.uk to ask about Phase 3 plans. Reference SAPIENT compliance as a development target. This builds a relationship for the next cycle.

---

## COMPETITION 3: DASA Innovation Focus Areas — IFA042 and IFA035

**Status: Both PAUSED / CLOSED after Cycle 4 (January 2026)**

| IFA | Title | Status |
|-----|-------|--------|
| IFA042 | Unlocking the True Potential of Test and Evaluation for Defence | Closed — pausing indefinitely |
| IFA035 | Making Science Fiction a Reality: Future Directed Energy Weapons | Paused — no reopen date |

Neither IFA is directly relevant to C2, ISR, or drone autonomy. The IFAs historically relevant to these areas (AI, autonomy, ISR) were run in earlier cycles and are now archived. The UKDI service reopening in July 2026 will likely introduce new IFAs aligned with the Strategic Defence Review 2025 priorities: the "Digital Targeting Web by 2027" and 50,000 drone procurement by 2026.

---

## COMPETITION 4: NATO DIANA 2027 Challenge Programme

**Status: 2026 cohort selected (December 2025). 2027 Call for Proposals expected mid-2026.**

**Organisation:** NATO Defence Innovation Accelerator for the North Atlantic
**Website:** https://www.diana.nato.int
**Funding Phase 1:** €100,000 per innovator (contractual, not grant)
**Funding Phase 2:** Up to €300,000 additional
**Eligibility:** Companies from any of 32 NATO member states (UK qualifies post-Brexit via continued participation)

### 2026 Cohort — Challenge Areas (10 total)

The 2026 cohort (150 companies selected December 2025) covers:
1. Advanced communications and contested electromagnetic environments
2. **Autonomy and unmanned systems** ← direct fit
3. Energy and power
4. Biotech and human resilience
5. Critical infrastructure and logistics
6. Underwater domain awareness
7. Counter-UAS (includes "ISR bubble" fleets of high-speed UAVs with autonomous hangars)
8. Space resilience
9. AI-enabled decision-making
10. Electronic warfare

### Application Timeline for 2027

- 2026 cohort was selected from a Challenge Call that opened approximately June 2025 and closed July 2025
- 2027 Call for Proposals is expected to open approximately **June 2026**
- Applications require: working prototype at minimum TRL 3–4, registered legal entity, NATO nation eligibility

### Assessment for MPE

"Autonomy and unmanned systems" and "AI-enabled decision-making" are both viable challenge areas for MPE. The strongest angle is the C2 intelligence layer for multi-domain autonomy — this is distinct from the hardware-focused drone companies that dominate typical applications.

**Required before applying:**
1. Register as a legal entity (Ltd company in UK — straightforward at Companies House)
2. Reach TRL 4: documented prototype with evidence of function against live data
3. Prepare a 10-minute pitch demonstrating the multi-domain fusion concept

**Recommended action:** Target the 2027 DIANA Challenge Call. Register a company by summer 2026. Use the SITL integration and real AIS/ADS-B demo as the TRL 4 evidence package.

---

## COMPETITION 5: Strategic Defence Review 2025 — Digital Targeting Web

**Not a competition — a £4B government programme**

The UK Strategic Defence Review 2025 mandated a "Digital Targeting Web" (DTW) to connect sensors, deciders, and effectors across all domains, with a Minimum Viable Product by 2026 and full capability by 2027. Total government spend on autonomy is £4 billion this parliament.

The DTW programme is run through DSTL, with prime integration contracts likely to go to BAE Systems, Thales, or QinetiQ. However, smaller sub-components — particularly AI/ML classification layers, track fusion software, and operator interfaces — are being procured through DASA/UKDI competitions and direct DSTL research contracts.

**Entry point:** DSTL's Innovation Partnerships team. Contact: dstl.cs@dstl.gov.uk or via the UKDI portal.

---

## SUMMARY TABLE

| Competition | Status | Funding | Deadline | Best Fit |
|-------------|--------|---------|----------|----------|
| UKDI Innovation Support to Operations Cycle 7 | **OPEN** | £350K/proposal | 12 May 2026 | Challenge 4 (UAS Navigation) — needs hardware partner |
| Autonomous Sensor Management Phase 2 | Closed | £1M total | Passed | Phase 3 follow-up via email |
| DASA Open Call IFAs | Paused | Varies | July 2026 reopen | Wait for new IFAs |
| NATO DIANA 2027 | Opens ~Jun 2026 | €100K–400K | ~Jul 2026 | Autonomy + AI decision-making |
| Digital Targeting Web | Programme, not competition | £4B total | Ongoing | Sub-component procurement |

---

## RECOMMENDED IMMEDIATE ACTION PLAN

1. **By 30 April 2026:** Contact accelerator@dstl.gov.uk to introduce MPE and ask about Phase 3 of the Autonomous Sensor Management competition. Attach a 2-page capability brief.
2. **By 12 May 2026:** Submit to UKDI Cycle 7 Challenge 4 as part of a consortium with a UK UAS hardware company. Start outreach to Blue Bear Systems Research (BBSR), Windracers, or Tekever UK.
3. **By June 2026:** Register MPE as a UK Ltd company to be eligible for DIANA 2027.
4. **By July 2026:** Prepare DIANA 2027 application targeting the "Autonomy and unmanned systems" challenge area.
