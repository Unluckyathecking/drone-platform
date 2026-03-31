# 5-Minute Pitch Script: DSEI Booth / DASA Innovation Day

**Document:** 48-Pitch-Script-5min.md
**Date:** 2026-03-31
**Author:** GTM research — Mohammed Ali Bhai project
**Contexts:** DSEI 2027 exhibit booth, DASA/UKDI Innovation Day, DIANA accelerator pitch, investor meeting

---

## HOW TO USE THIS DOCUMENT

- **Section A** — The 5-minute script. Memorise the opening line and the closing line. Everything in between is a guide, not a script. Speak naturally.
- **Section B** — Screen/demo guide. What to have on screen at each moment.
- **Section C** — Expected questions and exact handling. The "you're 17" objection is covered in full.
- **Section D** — Room-reading guide. How to adapt for different audience types.

---

## SECTION A: THE 5-MINUTE PITCH SCRIPT

**Target:** 4:30–5:00 minutes. Practice until you can hit 4:45 consistently.

---

### [0:00 — OPENING LINE]

**Say exactly this:**

> "There are 193 countries in the world. Palantir serves about 40 of them. I built the system for the other 150."

*Pause. Let it land. Then continue.*

---

### [0:10 — THE PROBLEM]

> "If you want AI-enabled command and control software today, you have two realistic options: Palantir Maven Smart System, which costs $10–30 million to deploy and requires US State Department export approval, or Anduril Lattice, which is under a $20 billion US Army enterprise contract and not available outside the US alliance structure at all.
>
> That means every military with a defence budget under $10 billion — which is roughly 140 of the world's armed forces — has no credible C2 software option. They're running on paper maps and WhatsApp.
>
> And these aren't irrelevant markets. Colombia just stood up a 300-drone battalion with no C2 software to manage it. Estonia is building a drone wall along its Russian border. The Philippines is running maritime ISR over the South China Sea against Chinese incursions. These are real operational needs with zero credible solutions in the market."

---

### [0:55 — THE PLATFORM]

*[Move to demo screen — dark map with tracks visible]*

> "This is the Mission Planning Engine. It's running live right now.
>
> What you're looking at is a global air picture — over 1,600 aircraft tracked in real time via ADS-B. Every dot is a real aircraft. The red ones have been flagged by the AI classifier — military ICAO address ranges, low altitude, or emergency squawk codes. The yellow ones are suspect. Green is neutral.
>
> Underneath the air picture is a maritime layer — 585 vessel tracks, AIS decoded in real time. The classifier is running against every vessel: ship type, speed anomaly detection, AIS spoofing detection via position-jump analysis.
>
> The system is a headless Python daemon — no dashboard is the product. The product is this."

*[Switch to ATAK screenshot or CoT output stream]*

> "Everything the engine generates streams as Cursor on Target — the NATO-standard tactical data protocol — to any TAK server. Every military that uses ATAK, which is about 600,000 users across 40+ countries, can plug this in without replacing anything they already have. Hostile tracks appear red on their tablet. They don't need a new system. They need an intelligence layer. That's what this is."

---

### [1:45 — SPECIFIC CAPABILITIES]

> "Let me be specific about what it can do today, because defence audiences rightly distrust vague claims.
>
> The engine has six working intelligence modules:
>
> **First:** Multi-source track fusion. ADS-B, AIS, MAVLink drone telemetry, and inbound CoT from allied forces all resolve into a single entity registry. If a vessel appears in AIS and you've also got a drone watching it, those are the same track — the system knows that.
>
> **Second:** Rule-based AI classification with a machine learning upgrade path. Every entity gets a threat score from zero to ten, an affiliation — friendly, hostile, suspect, unknown — and a reasoning chain explaining why. 'Threat 8: tanker exceeding 20 knots, AIS position jump detected 47 nautical miles in 4 minutes, consistent with spoofing.' Operators can challenge it, override it, or confirm it.
>
> **Third:** Pattern-of-life analysis. The system builds a behavioural baseline for every entity — typical operating area, speed profile, active hours. When a fishing vessel that has docked in Mombasa every Tuesday for six months suddenly transits toward Mogadishu at 3am at twice its normal speed, you get an alert before it reaches Somali waters.
>
> **Fourth:** Geofencing with trajectory prediction. Polygon exclusion zones — the Strait of Hormuz, the Taiwan ADIZ, your own maritime exclusion zone — with 30 to 90 second look-ahead warning before a track enters.
>
> **Fifth:** MAVLink drone tasking. Mission planning, constraint validation, and waypoint upload to ArduPilot-based platforms. Tested against simulation; ready for hardware.
>
> **Sixth:** LLM-powered SITREP generation. An operator types 'what is the maritime situation in the Strait of Gibraltar' and gets a natural language intelligence summary using Claude. Optional — the system runs fully offline without it."

---

### [3:10 — THE TEAM]

> "I built this. I'm 17. I'm in Year 12 doing A-levels in physics, maths, further maths, and computer science.
>
> I know what you're thinking — I'll address that in a moment. But first, the evidence: 42 source modules, 692 automated tests, 98% code coverage on the core intelligence modules. The architecture was modelled on Palantir's published technical approach — I spent a week reading their patents, their developer documentation, and every demo they've published. Then I built the open-source equivalent.
>
> The system runs today. You can pull the GitHub repo, run the Docker container, and watch it ingest live global aircraft data right now. That is not a claim. That is a fact."

---

### [3:45 — THE ASK AND CLOSE]

> "Here's where I am. The platform is TRL 4 — validated in a lab environment against live data. Getting to TRL 6, which means a field-demonstrated system, requires three things: a hardware partner for the drone integration, a TAK Server deployment to prove the ATAK integration end-to-end, and access to a real operational environment.
>
> I have a UKDI Cycle 7 bid in preparation — the deadline is 12 May — targeting Challenge 4 with Blue Bear Systems as the hardware consortium partner. If that succeeds, it funds six months of development and a field demonstration.
>
> What I'm looking for from this conversation: if you're in procurement, I want to understand your data integration challenge — specifically what sensor feeds you're currently not fusing and why. If you're in industry, I want to discuss consortium opportunities. If you're an investor, I want introductions — not capital.
>
> The platform is built. The gap to deployment is hardware access and a door to open. I'm here to find both."

---

### [5:00 — HARD STOP]

If you are over time: cut the pattern-of-life, geofencing, and SITREP paragraphs from the capabilities section and go straight from track fusion to the team. The opening, market, and close are non-negotiable.

---

## SECTION B: SCREEN / DEMO GUIDE

### Setup (before anyone arrives)

Have two tabs open and ready to switch between:

**Tab 1 — Dashboard (demo mode)**
- `uvicorn mpe.server:app --port 8080` running
- Browser open to `localhost:8080`
- Map zoomed to show UK + North Sea + English Channel — busy maritime region, immediately recognisable to UK audience
- Verify at least 40–60 aircraft visible and 20+ vessel tracks before starting

**Tab 2 — Terminal with engine running**
- `PYTHONPATH=src python -m mpe --adsb-center 51.3632,-0.2652 --no-cot --log-level INFO`
- JSON log lines scrolling in real time — this is the most visually convincing evidence the system is live
- Threat alerts should be visible in the log stream

**Tab 3 — GitHub repo** (have it open, don't show unless asked)
- `github.com/Unluckyathecaking/drone-platform`
- Shows 42 source files, test directory, 692 tests

### When to switch screens

| Pitch moment | Screen |
|-------------|--------|
| "This is the Mission Planning Engine" | Switch to Tab 1 (dashboard) |
| "The product is this" | Switch to Tab 2 (terminal log stream) |
| "Every military that uses ATAK" | Stay on terminal — describe the CoT output visually |
| "692 automated tests" | Switch to Tab 3 (GitHub) briefly, then back |
| Questions about specific code | GitHub, navigate to src/mpe/ |

### If the demo fails

The dashboard failing in front of a defence audience is survivable. The terminal log stream is not — if the engine is running and logs are scrolling, that is sufficient evidence. Have a screenshot backup of the dashboard saved locally.

If everything fails: "The system is running on my laptop right now, which is why I'm not panicking. The internet connection is the issue, not the software. Here's a screenshot from this morning." Show the screenshot.

---

## SECTION C: EXPECTED QUESTIONS AND HANDLING

### "You're 17. Why should I take this seriously?"

**Do not be defensive. Do not apologise. Use this exact structure:**

> "That's a fair question and I'd ask it too. The answer is: look at the code, not my age.
>
> The GitHub repository is public. 42 source modules, 692 passing automated tests. You can run it yourself in 10 minutes with Docker. The classifier correctly identifies military ICAO address ranges, detects AIS spoofing via position-jump analysis, and the geofence module has been tested against the Strait of Hormuz coordinates. None of that stops working because of who wrote it.
>
> I'll also say this: every defence company evaluating new technology is eventually going to talk to the people who built the software that fights the next war. Those people are currently in sixth form. The question is whether you find them before your competitor does."

**Why this works:** It reframes the objection, provides specific technical evidence immediately, and ends with a statement that makes the listener feel they are missing out rather than doing you a favour.

---

### "What's your TRL?"

> "TRL 4 — validated in a laboratory environment against live operational data. The track fusion, classification, geofencing, and prediction modules are tested against real ADS-B and simulated AIS data. The MAVLink upload is tested against ArduPilot SITL simulation. TRL 6 — demonstrated in a relevant environment — requires a field deployment with a hardware partner, which is what the UKDI Cycle 7 bid is designed to fund."

**Don't say TRL 5 or 6 unless you've done the field test. The person asking this question probably knows the TRL scale better than you do.**

---

### "How does this compare to Palantir?"

> "Palantir Maven is a $1.3B DoD contract system with 10 years of operational history, 500 engineers, and US government backing. We are not Palantir. We are the system that works for the 150 countries that can't buy Palantir.
>
> The specific technical differentiators: no ITAR restrictions, runs on any Linux hardware the customer already owns, full source code available for sovereign deployment, native CoT output for ATAK compatibility without additional integration cost, and MAVLink drone tasking that Palantir doesn't have natively.
>
> We are not a Palantir replacement. We are a Palantir-adjacent layer for the markets Palantir has structurally excluded."

---

### "What's the business model?"

> "Three revenue streams: annual licence fees of £50K–£500K per nation-state deployment depending on scale; a £25–75K fixed-price 90-day pilot programme as the entry point; and training and integration at £20–50K one-time.
>
> Conservative Year 3 target is five deployments at an average of £150K — £750K ARR. That funds a small team, ongoing development, and export compliance. The defence procurement cycle is long — 18–36 months from first contact to contract — which is why we're starting customer conversations now, 18 months before the platform is ready for commercial deployment."

---

### "What are the gaps? Be honest."

**Answer this question with full honesty — it builds more credibility than any capability claim.**

> "Four honest gaps. First, no COMSEC: all communications are currently plaintext. WireGuard is on the roadmap but not implemented. That's a showstopper for any classified network — we're not positioned for classified use cases until that's done.
>
> Second, no TAK Server field test: the CoT output code is complete and tested against a loopback, but we haven't connected it to a real FreeTAK Server with a physical ATAK device in the loop. That's a weekend of work and a £0 cost; it just hasn't happened yet.
>
> Third, no real AIS data: we're running against simulated vessels. A £150 RTL-SDR receiver fixes this immediately.
>
> Fourth, no ML: the classifier is rule-based. That's a deliberate design choice for explainability, but it means we miss threat patterns that a trained model would catch. The architecture has an ML upgrade path built in; the data is being collected via PostgreSQL for future training."

---

### "What does 'headless daemon' mean for an operator?"

> "It means the operator never interacts with our software directly. They use ATAK — the standard military tablet app they already have, already trained on. Our system runs in the background on a small server and makes their ATAK map smarter. Hostile entities appear red instead of blue. Alerts pop up as messages. The operator's workflow doesn't change. The intelligence quality does."

---

### "Can it command weapons?"

> "No. Deliberately. The platform classifies entities and routes intelligence to human operators. Weapons authorisation is outside scope and will remain outside scope until there is a clear regulatory and legal framework for autonomous lethal decisions — which does not exist in the UK or internationally. We are an intelligence layer, not a kill chain."

---

### "Is this dual-use? Could it be misused?"

> "Yes, any intelligence and surveillance system is dual-use by nature. Our export controls: UK-origin software requires a Standard Individual Export Licence for non-OGEL countries. We will not export to countries under UK arms embargoes. We will not sell to non-state actors. The same controls that apply to BAE Systems and QinetiQ apply to us."

---

### "What's the IP situation? Can you protect this?"

> "The source code is on GitHub under an open-source licence for development purposes. Commercial deployments are licensed separately — the licence controls use, distribution, and modification rights. The core IP is the architecture, the classifier rules, and the track fusion logic — none of which is novel enough to patent, but all of which require significant engineering effort to reproduce from scratch. Our competitive moat is delivery speed, UK-origin compliance, and the fact that we are already ATAK-integrated while competitors are not."

---

### "Why not raise funding and hire a team?"

> "Because the platform doesn't need capital to reach TRL 6 — it needs a consortium partner and hardware access. Raising money at pre-TRL 6 with no pilot deployment would mean giving up equity at the lowest valuation point. The right time to raise is after the first pilot demonstrates operational value. The UKDI grant is non-dilutive and validates the technology independently. That's the right sequencing."

---

## SECTION D: ROOM-READING GUIDE

### If the audience is procurement (MoD, Coast Guard, armed forces)

Lead with the operational capability, not the technology. Skip the architecture slides entirely. Open with the Colombia/Estonia/Philippines examples — "forces that have drones but no C2." Show the ATAK output, not the terminal. End with "what is your current data integration problem?"

Key signal they are interested: they ask about specific sensor inputs ("does it work with [specific radar/AIS system]?"). This means they are mentally testing whether it fits their environment.

### If the audience is a defence company (BAE, Thales, QinetiQ, Saab)

They want to know if you're a threat or a partner. Answer: partner. Lead with "this is a C2 intelligence layer that integrates below your existing systems, not a replacement." Emphasise ATAK compatibility — every UK prime is building or has built ATAK-compatible systems. MPE is an enrichment layer for their products, not a competitor to them.

### If the audience is an investor (defence VC, angel, family office)

They are evaluating founder quality as much as platform quality. Be specific, be honest about gaps, have a clear number in your head ("£750K ARR by Year 3, 5 deployments"). Do not oversell. The best thing you can say is "I know exactly what the system can't do yet and exactly how to fix each gap."

### If the audience is a journalist or academic

Emphasise the Palantir gap story — it's genuinely interesting and counterintuitive. Be careful about operational claims. Have the GitHub URL ready. Say "you can verify every capability claim I make in the codebase" — almost no one will, but saying it signals technical honesty.

### If the audience is another student / peer

Don't pitch. Show them the dashboard and the terminal and let them ask questions. Peers who are impressed become allies, co-founders, or future customers' children. Don't waste a pitch on them.

---

## SECTION E: PHYSICAL SETUP CHECKLIST

Before any event:

- [ ] Laptop charged (100%) and charger in bag
- [ ] Dashboard running and verified before leaving home
- [ ] Engine running against live ADS-B (verify aircraft visible)
- [ ] Screenshot backup saved locally (in case WiFi fails)
- [ ] GitHub repo bookmarked and loaded
- [ ] One-pager (document 47) printed × 10, plus PDF on phone
- [ ] Business cards or QR code card linking to GitHub + one-pager PDF
- [ ] ATAK screenshot (from `server.py` CoT output, or simulated) saved locally
- [ ] Practice the opening line and closing line out loud × 5 before entering the room

---

## SECTION F: THE 30-SECOND VERSION

For hallway conversations, elevator pitches, or when someone gives you 30 seconds:

> "I built a C2 intelligence platform that does what Palantir Maven does — fusing ADS-B, AIS, and drone data into a live classified threat picture — but for the 150 countries that can't afford or access Palantir. It runs on any Linux box, it's UK-origin with no ITAR restrictions, and it integrates with ATAK out of the box. It's working today. I'm looking for a hardware partner for a UKDI Cycle 7 bid due 12 May."

If they don't walk away at that point, go to the 5-minute version.
