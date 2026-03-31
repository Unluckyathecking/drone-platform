# Export Control: UK ECJU, OGEL, ITAR vs UK Regime
*Research document for mpe-c2 team. Author: INTEROP agent. Date: 2026-03-31.*
*Covers: UK ECJU process, OGEL applicability, ITAR vs UK export control for C2/drone software.*
*Status: READ-ONLY reference. NOT legal advice. Verify with a specialist before any export.*

---

## CRITICAL DISCLAIMER

Export control law is complex, jurisdiction-specific, and changes frequently. This document is research compiled for strategic planning purposes. Before exporting any controlled software or hardware:
1. Obtain a formal commodity jurisdiction (CJ) determination from ECJU
2. Consult a UK export control specialist (law firm or specialist consultancy)
3. Apply for appropriate licence well in advance of any demonstration, transfer, or sale

Violation of export control law is a criminal offence under the Export Control Act 2002 (UK) and carries custodial sentences.

---

## 1. The Two Regulatory Regimes That Matter

MPE is UK-developed software. Two export control regimes are relevant:

### UK Export Control (Primary Regime for MPE)

**Authority:** Export Control Joint Unit (ECJU), part of the Department for Business & Trade (DBT)
**Primary legislation:** Export Control Act 2002, Export Control Order 2008
**Control list:** UK Strategic Export Control Lists (SECO lists), which mirror the EU Dual-Use Regulation post-Brexit and include the UK Military List
**System:** SPIRE (being replaced by LITE for SIEL applications from 2024)

### US ITAR (Affects MPE if US-Origin Technology Is Incorporated)

**Authority:** Directorate of Defense Trade Controls (DDTC), US State Department
**Legislation:** Arms Export Control Act (AECA), International Traffic in Arms Regulations (22 CFR Parts 120–130)
**Critical rule:** ITAR applies to any item with US-origin defence article content — including software libraries, algorithms, data

**The ITAR "see-through" rule:** If MPE incorporates any ITAR-controlled US-origin technology (code, algorithms, data), ITAR controls apply to the entire system regardless of where MPE is developed. This is not just hardware — it applies to software.

**ITAR exposure assessment for MPE:**
- `pymavlink` library: MAVLink is an open protocol. `pymavlink` itself is not ITAR-controlled (it's open source, no US government classification). Low risk.
- `pytak` / CoT protocol: CoT is documented by the US government but the protocol specification is publicly released. Not ITAR-controlled. Low risk.
- Anthropic Claude API (intelligence.py): Accessing the Claude API is not a transfer of ITAR-controlled technology. Low risk.
- Custom code: MPE's classification, alerting, geofencing algorithms — developed by Mohammed in the UK — are not of US origin. No ITAR exposure from these.

**Conclusion:** MPE as currently designed does **not** appear to incorporate ITAR-controlled US-origin technology. The software is UK-developed, using open-source libraries that are not on the USML. This is a significant strategic advantage over US competitors. **ITAR-free status should be verified by a specialist before any export, but the current assessment is favourable.**

**2025 ITAR amendment (AUKUS):** On 30 December 2025, DDTC published a final rule adding an exemption for most defence trade among Australia, UK, and USA. This expands the space for UK-US collaboration on MPE without ITAR licence requirements in those bilateral contexts.

---

## 2. UK Export Control: Is MPE Controlled?

### Does MPE Require an Export Licence?

This depends on how ECJU classifies the software. The relevant UK control list entries are:

**Military List Entry ML21** — Software "specially designed" for military C2:
> "Software" specially designed or modified for the "development", "production" or "use" of equipment or materials controlled in this Military List

**Dual-Use List 4E001** — Technology for information security systems (if cryptography is incorporated)

**The key legal question:** Is MPE "specially designed" for military use?

**Arguments that MPE is NOT specially designed for military use (and thus not ML21):**
- MPE ingests publicly available data (ADS-B, AIS) that is civilian in nature
- The platform has civilian applications (coast guard, maritime surveillance, search and rescue)
- The CoT/ATAK ecosystem is not exclusively military — it is used by fire services, emergency management, and civilian SAR teams
- Pattern-of-life and anomaly detection are used in civilian surveillance analytics
- No weapons integration, no kinetic targeting

**Arguments that MPE IS specially designed for military use (creating ML21 risk):**
- The explicit design intent is military C2 (the GTM document names militaries as customers)
- The SITREP narration and threat classification are oriented toward military adversary identification
- Integration with STANAG 4586 (a NATO standard) is a military application indicator
- The marketing documents describe the product as analogous to Palantir Maven/Gotham

**Assessment:** The "specially designed" test is objective, not intent-based in UK law — but the design intent matters in practice when ECJU assesses an application. MPE is in a grey zone. The safest approach is to request a formal ECJU commodity classification before any export to any country.

### The OGEL Landscape for MPE

**Open General Export Licences (OGELs)** allow exports without individual application, subject to conditions. Several OGELs are potentially relevant:

#### OGEL: Military Goods, Software and Technology (May 2025)

The primary OGEL for military software. **Permitted destinations are severely limited:**
- Australia, Austria, Belgium, Canada, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Japan, Netherlands, New Zealand, Norway, Spain, Sweden, UK, USA

**Africa and the Middle East are NOT on this list.** This OGEL cannot be used for exports to Nigerian Navy, Kenyan Defence Forces, AU missions, or any other African/Middle Eastern customer.

Recent removals from permitted destinations: Burkina Faso, Haiti, Mali, Niger — all removed due to coups/instability.

#### OGEL: Military Goods, Software and Technology — Government or NATO End-Use (May 2025)

A separate OGEL specifically for exports to foreign governments or NATO use. This came into force on 9 May 2025 and is the most recent version.

This OGEL covers government-to-government transfers to a broader destination list. **This may cover AU/ECOWAS missions if they are government end-users** — but requires formal registration and compliance.

#### OGEL: Software and Source Code for Military Goods

A specific OGEL for software exports. Allows export of software (including source code) for military goods to a specified destination list. Registration on SPIRE/LITE required.

**For open-source components of MPE:** If MPE were made open source, it would fall under the Open Source OGEL — but the commercial product is proprietary and does not qualify.

#### OGEL: Technology for Military Goods (May 2025)

Covers technical data and technology rather than finished software. Relevant for sharing technical specs with potential partners.

---

## 3. The SIEL Process: Individual Licence for Non-OGEL Destinations

For any export to Africa, the Middle East, or other non-OGEL destinations, MPE will need a **Standard Individual Export Licence (SIEL)**.

### Process

1. **Classify the goods**: Determine which UK control list entry applies (or request formal ECJU classification)
2. **Identify end user**: Name, address, end-use statement, end-user undertaking (EUU) form signed by the customer
3. **Apply via LITE** (from September 2024, replacing SPIRE): `apply-for-a-siel.service.gov.uk`
4. **Processing time**: ECJU aim: 21 working days. Typical: 30–45 working days. Complex/sensitive applications longer.
5. **Duration**: Typically 2 years from issue, for specified quantities/values to named end user

### What ECJU Assesses

ECJU applies the **Consolidated EU and National Arms Export Licensing Criteria** (updated post-Brexit as UK criteria):

1. UK international obligations and commitments
2. Human rights and internal repression risk
3. Internal situation in destination country (armed conflict risk)
4. Regional stability
5. National security interests (UK and allied)
6. Behaviour of buying country with regard to international law
7. Diversion risk
8. Technology transfer impact

**For African customers:** Criteria 2 (human rights) and 3 (internal situation) are the main risks. Countries with active armed conflicts (Ethiopia, DRC, Sudan, Sahel states) will face high scrutiny. Stable democracies (Ghana, Botswana, Namibia) face much lower scrutiny.

### Practical Timeline

For any export to Africa:
- Start ECJU process at **minimum 3 months** before intended export
- Allow 6 months for politically sensitive destinations
- Do not promise delivery to customer until SIEL is granted

---

## 4. Export Control Classification of Specific MPE Components

| MPE Component | Classification Assessment | Export Concern |
|--------------|--------------------------|----------------|
| ADS-B receiver (`adsb_receiver.py`) | Dual-use (civilian aviation monitoring) — possibly 4A001 | Low — public data source |
| AIS receiver (`ais_receiver.py`) | Civilian maritime monitoring — not controlled | Very low |
| Entity classifier (`classifier.py`) | Could be ML21 if classified as military C2 AI | Medium — depends on end use |
| Alert engine (`alerts.py`) | Military C2 feature | Medium |
| CoT output (`cot_output.py`) | Protocol used by militaries, also civilian emergency services | Low-Medium |
| STANAG 4586 VSM (future) | Military-only standard — likely ML21 | High — requires SIEL |
| Geofencing (`geofence.py`) | Dual-use (civilian airspace, military exclusion zones) | Low-Medium |
| Pattern of life (`pattern_of_life.py`) | Surveillance/intelligence feature — dual use | Medium |
| LLM SITREP (`intelligence.py`) | AI military analysis — novel area; ECJU classification unclear | Uncertain — seek guidance |
| Database persistence (`db/`) | Generic software infrastructure — not controlled | Very low |
| Docker/deployment files | Not controlled | Very low |

**Highest risk components:** The classifier + alert engine + STANAG 4586 VSM combination as a military C2 package is the most likely to require a SIEL for non-OGEL destinations.

---

## 5. Recommended Export Control Strategy for MPE

### Phase 1: Pre-Export (Now — Before Any Demo or Transfer)

1. **Register for SPIRE/LITE**: Mohammed or the entity (company) that owns MPE must register with ECJU. Registration is free. URL: `apply-for-a-siel.service.gov.uk`

2. **Request ECJU classification**: Submit an informal enquiry to ECJU asking whether MPE falls under ML21 or any dual-use entry. This is not a licence application — it's a classification request. ECJU will provide a written response. This response is not legally binding but provides a documented good-faith baseline.

3. **Draft an end-user undertaking template**: Prepare a standard EUU document that African/other customers will sign. This states the end use (peacekeeping C2, maritime surveillance, etc.) and commits the customer not to re-export or divert to third parties.

### Phase 2: First Demo (Africa)

4. **Use OGEL where possible**: If the demo is to a government-to-government contact via UK trade mission to a country that qualifies under the Government/NATO end-use OGEL, the OGEL may cover the demonstration. Verify with ECJU first.

5. **Apply for SIEL for first export**: Once the target customer is identified, apply for a SIEL naming that customer. Build the 3–6 month timeline into the sales process.

### Phase 3: Ongoing Operations

6. **OGEL registration**: Register under the relevant OGELs for permitted destinations to streamline exports to NATO/partner nations.

7. **Compliance records**: Maintain records of all exports (ECJU requirement: 4 years). For each export: customer identity, end-use statement, delivery confirmation, SIEL reference number.

8. **Re-export controls**: Include contractual clauses preventing customer from re-exporting MPE to third countries without MPE's prior consent and UK ECJU approval.

---

## 6. ITAR-Free Positioning as a Strategic Asset

The fact that MPE is not ITAR-controlled is a **major competitive differentiator** in the African/non-NATO market:

- US companies (Anduril, Palantir) are ITAR-controlled — cannot export to most of Africa without DDTC licence
- Israeli companies face US ITAR on key components and political restrictions
- Chinese alternatives carry sovereignty/security concerns
- **MPE: UK-developed, open-source libraries, ITAR-free — no US government licence required**

This should be the central export control message in customer conversations:
> "MPE is built entirely on UK and open-source technology. It is not subject to US ITAR. Your government will have full sovereignty over the deployment — no US government access, no US government approval required for future updates."

---

## 7. Key References

- UK export controls military goods: [gov.uk/guidance/export-controls-military-goods-software-and-technology](https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology)
- OGEL military goods, software and technology (May 2025): [assets.publishing.service.gov.uk](https://assets.publishing.service.gov.uk/media/681c9b67275cb67b18d870b5/open-general-export-licence-military-goods-software-and-technology.pdf)
- OGEL military goods — government/NATO end-use (May 2025): [assets.publishing.service.gov.uk](https://assets.publishing.service.gov.uk/media/681c9cf59ef97b58cce3e5bd/open-general-export-licence-military-goods-software-and-technology-government-or-nato-end-use.pdf)
- OGEL technology for military goods (May 2025): [assets.publishing.service.gov.uk](https://assets.publishing.service.gov.uk/media/681c873843d6699b3c1d2a25/open-general-export-licence-technology-for-military-goods.pdf)
- SIEL application (LITE system): [gov.uk/guidance/apply-to-export-controlled-goods](https://www.gov.uk/guidance/apply-to-export-controlled-goods)
- UK export controls overview: [globalinvestigationsreview.com](https://globalinvestigationsreview.com/guide/the-guide-sanctions/sixth-edition/article/how-the-united-kingdom-approaches-export-controls)
- SPIRE → LITE transition: [strongandherd.co.uk](https://www.strongandherd.co.uk/the-export-control-joint-unit-is-preparing-to-launch-siel-applications-on-the-new-lite-system-replacing-spire)
- ITAR drone/UAS classification: [jrupprechtlaw.com](https://jrupprechtlaw.com/drone-export-control-laws-ear-itar/)
- ITAR in UK context: [clearborder.co.uk](https://clearborder.co.uk/resource/understanding-itar-regulations-in-the-uk/)
- AUKUS ITAR exemption (December 2025): [perkinscoie.com](https://perkinscoie.com/insights/update/export-control-exemptions-facilitate-us-defense-and-sensitive-technology-trade)
- UAV export controls working group (Stimson Center): [stimson.org](https://www.stimson.org/wp-content/files/file-attachments/ECRC%20Working%20Group%20Report.pdf)
- ECJU contact: Export Control Joint Unit, 3 Whitehall Place, London SW1A 2AW. Email: eco.enquiries@businessandtrade.gov.uk
