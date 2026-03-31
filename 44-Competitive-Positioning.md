# Competitive Positioning: MPE C2 vs. Palantir Maven, Anduril Lattice, Systematic SitaWare, Elbit TORCH-X

**Document:** 44-Competitive-Positioning.md
**Date:** 2026-03-31
**Author:** GTM research — Mohammed Ali Bhai project
**Purpose:** One-page competitive comparison for use in customer briefings and investor conversations

---

## THE MARKET CONTEXT

Four systems dominate the military C2 and AI-enabled intelligence market as of March 2026:

1. **Palantir Maven Smart System (MSS)** — US AI-enabled intelligence and fires platform; $1.3B DoD contract (to 2029); now deployed to NATO via $480M contract (April 2025). The gold standard for AI-enabled C2.
2. **Anduril Lattice** — US AI autonomy platform; $20B US Army enterprise contract (March 2026); counter-UAS focused, expanding to all-domain C2.
3. **Systematic SitaWare** — Danish battle management suite; NATO's primary land C2 (DEMETER programme); deployed in 50+ countries.
4. **Elbit TORCH-X** — Israeli C4ISR suite; 30+ customers globally; includes HQ, dismounted, artillery, and fires variants.

MPE is not currently competitive with any of these systems as a like-for-like replacement. The strategic opportunity is not replacement — it is filling the gap these systems cannot or will not address.

---

## COMPARISON TABLE

| Dimension | Palantir Maven | Anduril Lattice | Systematic SitaWare | Elbit TORCH-X | **MPE (Current)** |
|-----------|---------------|----------------|---------------------|---------------|-------------------|
| **Primary customer** | US military, NATO Five Eyes | US military, US allies | NATO land forces (50+ nations) | 30+ nations, focus Middle East/Asia | Undeployed — pre-commercial |
| **Core capability** | AI-enabled intelligence, targeting, fires integration | Autonomous mission orchestration, C-UAS, mesh C2 | Battle management, Blue Force Tracking, orders management | Land C4ISR — HQ, dismounted, artillery, fires | Multi-source track fusion, AIS/ADS-B ingestion, classification, anomaly detection, CoT output |
| **AI / ML** | Large-scale LLM integration (Palantir AIP), computer vision, targeting chain AI | Lattice ML: autonomous target ID, sensor fusion, mission replanning | SitaWare Insight: ML pattern-of-life, LLM for intelligence staff | AI decision support, CV for reconnaissance | Rule-based classifier (ML upgrade path designed); LLM SITREP via Claude API |
| **TAK / CoT integration** | Maven outputs to TAK Server; CoT is native | Lattice Mesh is proprietary; Lattice SDK opened December 2024 | SitaWare can receive CoT input | No native CoT | **Native CoT output (UDP/TCP); full ATAK integration** |
| **Price point** | $10B+ US Army contract; £240M UK MoD; not publicly priced for smaller nations | $20B enterprise contract; not available to non-US allies without FMS | EUR 28M NATO contract (Headquarters only); ~EUR 500K–5M per nation deployment | Not publicly priced; estimated $1M–$10M per deployment | **Free (open source) to £500K (commercial licence)** |
| **ITAR / export restrictions** | ITAR-controlled; requires US government approval for all exports; Five Eyes only for full capability | ITAR-controlled; US ally restrictions apply | No ITAR; Danish origin; exports under EU dual-use rules — available to 50+ nations | ITAR-equivalent Israeli controls (Category XV); requires Israeli government approval | **No export restrictions; UK OGEL for NATO/Five Eyes free; SIEL routinely granted for most others** |
| **Deployment model** | Cloud-first (AWS GovCloud); edge capability requires Palantir-managed edge nodes | Cloud + edge (Lattice OS runs on Anduril hardware); no sovereign cloud option | Software licence; runs on customer hardware; SitaWare BattleCloud optional | Software + hardware package; customer-managed | **Headless Python daemon; runs on any Linux hardware; Docker container; fully sovereign** |
| **Minimum viable hardware** | Palantir-managed servers or AWS GovCloud | Anduril-specified edge compute (proprietary) | Customer-provided Windows/Linux servers | Customer-provided hardware (specific specs) | **Raspberry Pi 4 (tested); standard x86 laptop; no cloud dependency** |
| **Open source / open architecture** | Proprietary; Palantir AIP APIs exposed under contract | Lattice SDK released December 2024 (partial openness) | Proprietary; STANAG compliance claimed | Proprietary; E-CIX framework (internal modular, not open) | **Source code available; pure Python stdlib for core modules; no proprietary dependencies** |
| **Drone / MAVLink integration** | No native MAVLink; requires third-party bridge | Lattice autonomy directly controls Anduril drones; other drones via SDK | No native drone C2 (land BMS focus) | No native MAVLink; drone integration via STANAG 4586 | **Native MAVLink MISSION_ITEM_INT; tested against ArduPilot SITL; STANAG 4586 on roadmap** |
| **AIS / maritime integration** | Palantir Gotham includes AIS (separate product) | No native AIS | Limited; primarily land domain | Sea Tiger separate maritime product | **Native pyais NMEA decoder; live AIS ingestion; vessel tracker; CoT bridge** |
| **Maturity / TRL** | TRL 9 — deployed in active conflict (Ukraine, US Army) | TRL 8–9 — deployed to US Army C-UAS operations | TRL 9 — deployed in 50+ countries | TRL 9 — deployed in multiple conflicts | **TRL 4 — working code, live data tested, not field-deployed** |
| **Support / maintenance** | Palantir professional services (£/$ millions per year) | Anduril professional services | Systematic support contracts | Elbit Systems UK support | **Self-supported; community support roadmap** |

---

## STRATEGIC POSITIONING SUMMARY

### Where MPE loses (honestly)

- **Maturity:** All four competitors are field-proven, deployed systems. MPE is a working prototype.
- **Features:** SitaWare has orders management, radio integration, and a 20-year feature library. TORCH-X has fires integration and artillery C2. Maven has billion-dollar AI infrastructure. Lattice has autonomous mission execution. MPE has none of these today.
- **Support:** A military buyer purchasing Palantir gets a team of engineers. Purchasing MPE at this stage gets a 17-year-old with a GitHub repo.

### Where MPE wins (honestly)

**1. Price.** Maven and Lattice are priced for the US DoD. SitaWare NATO contracts run to EUR 28M. TORCH-X deployments are estimated at $1–10M. MPE can be licensed for £50K–£500K. For a country with a $2B defence budget, the difference between a £50K and a £5M system is the difference between "yes" and "no".

**2. Export availability.** Maven and Lattice are US ITAR-controlled — unavailable to 150+ countries without US State Department approval. TORCH-X requires Israeli government export consent. SitaWare is the most accessible but still requires Danish/EU export approval. MPE is UK-origin, no ITAR, no weapons association, and eligible for standard SIEL export to most nations.

**3. Sovereignty.** All four competitors run some version of managed cloud or managed edge compute. MPE runs on any Linux box. A customer can take the source code, compile it on an air-gapped server, and operate it with zero external dependency. This is a strategic differentiator for any nation that has experienced US system shutdowns (Taiwan Strait scenario) or is subject to US pressure (Gulf states, Indonesia, India).

**4. TAK/ATAK interoperability.** MPE outputs CoT natively. SitaWare and TORCH-X do not; they are designed to replace ATAK, not integrate with it. Palantir Maven outputs to TAK Server but at enterprise cost. MPE plugs into existing ATAK deployments as an intelligence enrichment layer without requiring any other system to be replaced or upgraded.

**5. Open architecture.** MPE's pure Python stdlib core (classifier, geofence, predictor, track_manager) has no proprietary dependencies. It can be forked, modified, and integrated into any customer system. No other competitor offers this.

---

## POSITIONING STATEMENT (one sentence)

> MPE is the lightweight, sovereign, ATAK-native C2 intelligence engine for the 150 countries that Palantir cannot serve — available at 10x lower cost, with no ITAR restrictions, running on any hardware the customer already owns.

---

## COMPETITIVE RESPONSE PREP

**If a customer asks: "Why not buy Palantir?"**
> Palantir requires US government export approval, AWS GovCloud (US-managed infrastructure), and a budget most nations allocate entirely to hardware. If you're eligible for Palantir and can afford it, buy it. If not, here's what runs on your existing infrastructure today.

**If a customer asks: "Why not buy SitaWare?"**
> SitaWare is excellent for land force battle management. It doesn't ingest live AIS, it doesn't do pattern-of-life analysis for maritime vessels, and it isn't optimised for autonomous drone C2 with MAVLink. MPE does those things. They can coexist — MPE feeds enriched tracks into SitaWare via CoT.

**If a customer asks: "Why not buy Anduril Lattice?"**
> Lattice is a US product under a $20B US Army contract. It is not available to non-US allies without FMS approval, which requires a State Department determination. It runs on Anduril-specified hardware. MPE runs on a laptop you already own. For a country outside the Five Eyes that wants autonomy without US infrastructure dependency, Lattice is not an option.

**If a customer asks: "Why not build it ourselves?"**
> You could. MPE is open source. Fork it. The code is on GitHub. What MPE offers over a build-yourself approach is 692 existing tests, a working multi-domain fusion engine, an existing ATAK integration, and a team that will maintain and support it. Building from scratch takes 18–24 months and a team of 3–5 engineers. Starting from MPE takes 3–6 months and one integration engineer.
