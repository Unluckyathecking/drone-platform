# Expression of Interest: UKDI Innovation Support to Operations Phase 3 (Cycle 7)

**Document:** 42-UKDI-Expression-of-Interest.md
**Date:** 2026-03-31
**Prepared by:** Mohammed Ali Bhai
**Competition:** UKDI Innovation Support to Operations Phase 3 — Cycle 7, Challenge Area 4 (UAS Navigation)
**Deadline:** 12 May 2026 at 12:00 noon
**Submission method:** UKDI Online Submission Service (accelerator@dstl.gov.uk for queries)

---

> **Note:** This is a pre-submission Expression of Interest (EOI) document — a structured pitch used to approach potential consortium partners and to organise the proposal before formal submission via the UKDI portal. UKDI does not require a formal EOI; the document below serves as an internal planning tool and outreach letter for hardware partners.

---

## PART A: CONSORTIUM PARTNER OUTREACH LETTER

*(Adapt and send to: Blue Bear Systems Research, Windracers, Tekever UK, or BAE Systems ASTREA)*

---

**Re: UKDI Innovation Support to Operations Phase 3 (Cycle 7) — Challenge 4: UAS Navigation**
**Deadline: 12 May 2026**

Dear [Name],

I am writing to propose a consortium submission for UKDI's Innovation Support to Operations Phase 3, Cycle 7, targeting Challenge Area 4: autonomous GNSS-denied navigation for UAS.

I have built a working C2 intelligence engine — the Mission Planning Engine (MPE) — that provides real-time multi-source track fusion, entity classification, geofencing, trajectory prediction, and pattern-of-life analysis. The platform runs as a headless Python daemon, ingests ADS-B and AIS data live, and outputs enriched situational awareness to TAK/ATAK networks over the CoT protocol. It has 692 passing tests and is deployed on standard commercial hardware.

Challenge 4 requires a UAS navigation solution that achieves ≥50m positional accuracy (objective 5m) in GNSS-denied environments. My platform provides the C2 layer that such a navigation solution would report to and be tasked by — it handles waypoint planning, track management, geofence enforcement, and alert generation.

A joint proposal would position [your company]'s navigation hardware/firmware as the onboard system, with MPE providing the ground-side C2 and intelligence integration. Together we cover the full sensor-to-decision chain that UKDI is seeking to fund.

Would you be available for a 30-minute call this week to discuss a potential collaboration?

Yours sincerely,
Mohammed Ali Bhai
[Contact details]

---

## PART B: DRAFT PROPOSAL SUMMARY

*(For use in the UKDI Online Submission Service)*

### Competition: Innovation Support to Operations Phase 3, Cycle 7
### Challenge Area: 4 — UAS Navigation (GNSS-denied autonomous navigation)

---

### Project Title

**Resilient Autonomous Navigation with Ground-Side C2 Intelligence Integration for GNSS-Denied UAS Operations**

---

### Executive Summary (200 words)

We propose a joint hardware-software solution for GNSS-denied UAS autonomous navigation, combining [partner]'s onboard navigation system with the Mission Planning Engine (MPE) C2 intelligence platform. The solution will demonstrate end-to-end autonomous flight in a GNSS-denied environment, with the UAS reporting position to MPE's track manager, receiving updated waypoints via MAVLink, and operating within dynamically enforced geofences — all without GPS dependency.

MPE is a working Python daemon that fuses multi-source tracks (ADS-B, AIS, MAVLink, CoT), classifies entities using rule-based AI, enforces geofence boundaries via ray-casting algorithms, and predicts trajectory violations before they occur. It has 692 passing tests, runs on commercial hardware, and outputs to TAK/ATAK networks over CoT protocol. The platform has been built and tested against live ADS-B data covering aircraft across Europe.

This project will integrate [partner]'s GNSS-denied navigation solution into the MPE command loop, demonstrating ≥50m positional accuracy in a representative test environment. The output will be a documented, reproducible integration ready for further MoD evaluation and procurement.

---

### Problem Statement

Modern UAS operations in contested environments face GPS jamming, spoofing, and denial as a routine operational condition. Ukraine conflict data shows GPS denial is standard practice within 30km of any contested front. UK drone procurement at scale (target 8,000 drones by 2026) requires navigation solutions that function without GPS from the outset, not as a retrofit.

Current GNSS-denied navigation solutions address the onboard guidance problem in isolation. The ground-side C2 layer — which tasks the drone, monitors its track, enforces geofences, and escalates alerts — has not been developed to match. A UAS that navigates GNSS-denied is only operationally useful if the human operator has real-time situational awareness of its position and an intelligent C2 layer to re-task it.

---

### Proposed Solution

**Onboard (provided by [consortium partner]):**
- GNSS-denied navigation using [visual inertial odometry / terrain-referenced navigation / RF-based positioning — partner to specify]
- Position output via MAVLink telemetry to ground station
- Minimum 50m positional accuracy; objective 5m

**Ground-side C2 (provided by MPE):**
- `track_manager.py` — receives MAVLink position reports, maintains UAS track in the Common Operating Picture
- `geofence.py` — enforces keep-in/keep-out zones via polygon ray-casting; alerts if UAS approaches boundary
- `predictor.py` — dead reckoning and geofence entry prediction, providing 30–90 second look-ahead for operator
- `planner.py` — validates and uploads updated waypoint plans via MAVLink MISSION_ITEM_INT
- `operator_api.py` — FastAPI REST interface for operator interaction; works on any web browser, no proprietary software
- CoT output to TAK Server / ATAK — operator sees the UAS on their standard military tablet

**Integration:**
The MPE engine daemon connects to the UAS via MAVLink over a radio link (or simulated link for demonstration). The GNSS-denied navigation system reports position to the autopilot, which reports to MPE. MPE fuses this with any available corroborating data (ADS-B returns from the aircraft itself if equipped, ground-based observers) and maintains a fused track with confidence scoring.

---

### Demonstration Plan (TRL 6 by project end)

| Milestone | Activity | Month |
|-----------|----------|-------|
| M1 | Software integration: GNSS-denied nav output connected to MPE MAVLink input | 1 |
| M2 | Indoor lab test: simulated GNSS-denied flight, MPE tracking, geofence enforcement | 2 |
| M3 | Outdoor field test: real flight, GNSS jamming or denial mode active, MPE tracking live | 3–4 |
| M4 | TAK Server integration: ATAK device shows UAS track and alerts | 5 |
| M5 | Demonstration to DSTL evaluators: end-to-end GNSS-denied flight with C2 intelligence | 6 |

The demonstration will be conducted at [partner]'s test site or a DSTL-approved UK test range.

---

### Why This Team

**Mohammed Ali Bhai (software/C2):**
- Built MPE from scratch: 42 source modules, 692 tests, live ADS-B/AIS ingestion, MAVLink integration
- ArduPilot SITL testing of mission upload protocol
- Full CoT/TAK Server integration designed and documented
- A-level Physics (predicted A*), Mathematics (predicted A*), Further Mathematics (predicted A*), Computer Science (predicted A*)

**[Consortium partner] (hardware/navigation):**
- [To be completed by partner]

---

### Costs (indicative, <£350,000)

| Item | Cost |
|------|------|
| MPE software development and integration (6 months) | £45,000 |
| Hardware (UAS platform, radio link, TAK Server) | £15,000 |
| Test range access and field trials (3 events) | £20,000 |
| [Partner] navigation system development | [Partner to specify] |
| Subcontractor costs | TBC |
| **Total** | **<£350,000** |

---

### Intellectual Property

MPE source code and architecture is owned by Mohammed Ali Bhai. The navigation solution is owned by [partner]. The integrated system IP will be jointly owned per a consortium agreement to be signed before proposal submission. Both parties retain rights to their respective components for independent commercialisation.

---

### Commercial Pathway

A successful TRL 6 demonstration creates a product ready for:
1. Further UKDI/DSTL procurement as a counter-UAS C2 enhancement layer
2. Export to allied nations under UK OGEL (free to Australia, Canada, NATO members, Japan, NZ) or SIEL (other friendly nations)
3. Integration into the UK MoD Digital Targeting Web programme as a compliant SAPIENT-compatible sensor management layer

---

## PART C: TIMELINE TO SUBMISSION

| Date | Action |
|------|--------|
| 1–7 April 2026 | Send Part A outreach letters to 3 hardware partners |
| 8–14 April 2026 | Consortium call(s) with interested partners |
| 15 April 2026 | Select consortium partner, sign MOU |
| 16–28 April 2026 | Draft full proposal in UKDI Online Submission Service |
| 29 April 2026 | Internal review and sign-off |
| 1–9 May 2026 | Final edits, cost schedule, subcontract agreements |
| 12 May 2026 | Submit by 12:00 noon |

---

## APPENDIX: UKDI SUBMISSION REQUIREMENTS CHECKLIST

- [ ] Registered on UKDI Online Submission Service
- [ ] UK-registered organisation (or consortium with a UK prime)
- [ ] Proposal does not contain information classified above Official
- [ ] Proposed budget ≤ £350,000
- [ ] Project duration ≤ 6 months
- [ ] TRL 6 target stated and demonstration plan included
- [ ] Commercial pathway described
- [ ] IP ownership and consortium agreement described
- [ ] Cyber Risk Assessment: RAR-240619B04, Very Low Risk acknowledged
