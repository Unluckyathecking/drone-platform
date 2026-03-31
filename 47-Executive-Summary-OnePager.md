# Mission Planning Engine — Executive Summary

**Document:** 47-Investor-One-Pager.md
**Date:** 2026-03-31
**Format:** PDF-ready one-pager for investors and defence procurement officers
**Version:** Pre-seed / pre-pilot (TRL 4)

---

> *Print or export as PDF. Designed to fit one A4 page at 10pt with standard margins. The section headers below map to a two-column layout: left column = Platform / Market / Capability; right column = Team / Timeline / Ask.*

---

## MISSION PLANNING ENGINE (MPE)

### The AI Intelligence Layer for the 150 Countries Palantir Cannot Serve

---

### THE PROBLEM

Palantir's Maven Smart System is the gold standard for AI-enabled military command and control. It is deployed by the US Army ($10B contract), NATO ($480M contract, April 2025), and the UK MoD (£240M contract, December 2025).

**It is unavailable to 150+ countries.** The reasons are structural and permanent:

- **ITAR:** US export law restricts military AI software to US treaty allies with State Department approval. Approximately 140 of the world's armed forces are effectively excluded.
- **Cost:** A Palantir deployment costs $10–30M over five years. Any military with a sub-$10B defence budget — roughly 140 of 193 UN member states — cannot absorb it.
- **Sovereignty:** Palantir requires US-managed cloud infrastructure and US personnel access. Countries with non-alignment policies (India, Indonesia, Brazil, Gulf states) cannot accept US visibility into their C2 operations.

The market gap: the global military drone C2 software market is growing rapidly. Palantir makes £782M internationally from ~40 countries. The remaining 150+ countries are structurally underserved.

---

### THE PLATFORM

The Mission Planning Engine (MPE) is a headless AI intelligence daemon that ingests multi-domain sensor data, classifies entities with threat scoring and anomaly detection, and streams enriched situational awareness to military operators over the standard Cursor on Target (CoT) protocol — compatible with all ATAK-equipped forces worldwide.

**What it does today (TRL 4, tested against live data):**

| Capability | Implementation |
|-----------|----------------|
| Live ADS-B air track ingestion | 33 global regions, ~1,600+ aircraft simultaneously |
| Live AIS maritime track ingestion | Full NMEA decode, all AIS message types |
| Multi-source track fusion | Exact ID + spatial correlation, multi-source confidence scoring |
| AI entity classification | Rule-based threat scoring 0–10, affiliation, anomaly detection |
| AIS spoofing detection | Haversine position jump analysis |
| Emergency squawk detection | 7500 HIJACK, 7600 COMMS FAIL, 7700 EMERGENCY |
| Pattern-of-life analysis | Behavioural baseline + deviation detection per entity |
| Geofencing | Polygon keep-in/out/alert zones, ray-casting, preset strategic zones |
| Trajectory prediction | Dead reckoning + geofence entry prediction, 30–90s look-ahead |
| Alert engine | 6 rule types, configurable cooldowns, CoT alert XML output |
| LLM-powered SITREP | Natural language situation reports via Claude API |
| CoT output to ATAK | UDP/TCP to any TAK Server; hostile tracks show red in ATAK |
| MAVLink drone tasking | MISSION_ITEM_INT upload to ArduPilot, tested against SITL |
| Operator REST API | FastAPI: watchlist, manual overrides, alert ack, health |
| PostgreSQL persistence | SQLAlchemy 2.0 async, PostGIS geometry, audit log |

**Architecture:** Headless Python daemon. Runs on any Linux hardware. No cloud dependency. No proprietary stack. Full Docker deployment included. Systemd service for bare-metal. 42 source modules, 692 automated tests, 98% coverage on core modules.

**The product is not a dashboard. The product is the intelligence layer.** ATAK is the UI — 600,000+ military and first responder users worldwide already have it. MPE is the system that makes their map smart.

---

### THE MARKET

**Target buyer profile:** Military or coast guard with a defence budget of $1–25B, active drone programme, no current C2 software contract, and structural barriers to buying Palantir.

**Tier 1 immediate targets:** Philippines (South China Sea ISR), Colombia (BANOT — 300-drone battalion, no C2 software), Poland (€2B Eastern Shield counter-drone wall), Estonia (Drone Wall, NATO front-line).

**Revenue model:**
- **Licence:** £50K–£500K per year per deployment (nation-state or operator)
- **Pilot programme:** £25K–£75K fixed-price 90-day pilot (entry point)
- **Training and integration:** £20K–£50K one-time
- **Conservative Year 3 target:** 5 deployments × £150K average = £750K ARR

**Export:** UK-origin, no ITAR. NATO OGEL covers free export to 30+ allies. SIEL routinely granted for remaining targets.

---

### THE TEAM

**Mohammed Ali Bhai** — Founder and sole engineer
- Year 12, A-levels: Physics (predicted A\*), Mathematics (A\*), Further Mathematics (A\*), Computer Science (A\*)
- Built MPE from zero: 42 modules, 692 tests, live multi-domain data integration
- Dual UK-Canadian citizen, near Epsom, Surrey
- Cambridge Engineering applicant, 2027 entry
- GitHub: github.com/Unluckyathecaking/drone-platform

**Why this team can execute:** The platform was built by one person in spare time around A-level study. It works against live data today. The gap to a deployable product is integration time and hardware access — not fundamental engineering challenges. The architecture was designed from day one for production deployment (headless daemon, PostgreSQL, Docker, systemd, structured JSON logging for SIEM).

---

### CURRENT STATUS AND GAPS

**Done:** Ingestion, fusion, classification, alerting, geofencing, prediction, CoT output, MAVLink tasking, operator API, persistence, Docker deployment, 692 tests.

**Not yet done (honest):**
- No real TAK Server field test (code is complete; hardware access needed)
- No COMSEC (WireGuard planned; currently plaintext)
- No auth on operator API (JWT on roadmap)
- No real AIS hardware (£150 SDR needed for live vessel data)
- TRL 4 → TRL 6 requires field demonstration with a hardware partner

---

### TIMELINE

| Date | Milestone |
|------|-----------|
| May 2026 | UKDI Cycle 7 consortium bid submitted (with Blue Bear Systems) |
| June 2026 | UK Ltd company registered; DIANA 2027 application prepared |
| July 2026 | NATO DIANA 2027 application submitted |
| Aug 2026 | A-level results; build phase begins |
| Sep–Dec 2026 | RTL-SDR AIS hardware; FreeTAK Server integration; TRL 5 demonstration |
| Jan 2027 | First pilot offer to HM Coastguard (MCA) / Estonian Defence Forces |
| Oct 2027 | Cambridge Engineering entry (if offer received) |
| 2027–2028 | First paid pilot deployment; seed funding round |

---

### THE ASK

**Stage:** Pre-seed / pre-pilot. No external funding to date.

**What would accelerate this:**

| Need | What it enables |
|------|----------------|
| £500 | RTL-SDR receiver for real AIS data |
| £2,000 | Cloud VPS for always-on TAK Server demo instance |
| Introductions | UK defence procurement, DSTL, NCIA, potential pilots |
| Mentorship | Defence company BD lead or ex-MoD procurement officer |
| Co-founder / technical partner | COMSEC implementation (WireGuard), computer vision (YOLOv8) |

**Investor note:** This is not a fundraising document. The platform does not need external capital to reach TRL 6 — it needs hardware access and a consortium partner. The ask is introductions and mentorship, not money. A first paid pilot in 2027–2028 is the realistic funding entry point.

---

*MPE C2 Platform — github.com/Unluckyathecking/drone-platform — Mohammed Ali Bhai — [contact]*
