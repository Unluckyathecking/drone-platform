# Technology Audit Report — Full Project Review

## 10 Independent Audits, March 2026

Each technology area was reviewed by a specialist Sonnet agent instructed to be harsh. PASS/FAIL/CAUTION on every major claim.

---

## EXECUTIVE SUMMARY

```
  AREA                    PASS  CAUTION  FAIL   VERDICT
  ═══════════════════     ════  ═══════  ════   ═══════════════════════
  Mission Engine Code      2      3       4     Fix upload.py, add tests
  Payload Interface        2      1       4     Clearance, angle, CG, lanyard
  Tileable Microdrone      1      2       3     Freefall 4-6m not 2m, thrust marginal
  Solar Endurance          1      1       6     L/D 30 impossible for multipurpose
  Laser Power Beaming      1      4       4     Mass/cost off by 10x
  Airship Concept          0      2       5     Cost off 5-10x, no precedent
  Ground Station           0      4       3     State machine incomplete, catapult unrealistic
  Regulatory Strategy      0      2       3     Real BVLOS cost £8-15K not £3.6K
  Business Model           0      3       3     No customer validation, margins overstated
  Tube-Launch Design       0      3       4     Tumble, prop start, spring reliability
  ─────────────────────────────────────────────────────────────────
  TOTAL                    7     25      39
```

**Pattern:** Near-term engineering (built and tested) has fixable bugs. Long-term vision (theoretical) has order-of-magnitude errors in cost, mass, and performance.

---

## CRITICAL FIXES NEEDED (Before Summer 2026 Build)

### 1. upload.py — Will Fail on Real Pixhawk
- Uses deprecated `MISSION_REQUEST` instead of `MISSION_REQUEST_INT`
- Race condition: loop counter desyncs from `msg.seq` under packet loss
- Float32 lat/lon gives 2m error per waypoint
- No connection teardown (file descriptor leak)
- **Fix:** Rewrite upload to use `MISSION_ITEM_INT` protocol

### 2. Payload Interface — 4 Safety-Critical Failures
- 0.3mm clearance too tight for FDM PETG on aluminum (need 0.5-0.6mm)
- 60° dovetail should be 45° (easier to print, equally strong)
- CG management unverified — no moment arm data, Velcro battery rail will creep
- Lanyard anchor will shear through PETG under dynamic load (need metal through-bolt)
- **Fix:** Update config.py, reprint, validate with actual hardware

### 3. Test Coverage — 55% (Needs 80%)
- Writer, upload, and CLI modules have zero tests
- Missing boundary tests (altitude = max, zero-distance route)
- **Fix:** Write tests for all untested modules

### 4. Home Altitude — AMSL vs AGL Undocumented
- Home waypoint uses MAVFrame.GLOBAL (absolute altitude)
- No validation that user provides AMSL, not AGL
- **Fix:** Add documentation and validation

---

## VISION DOCUMENTS — HONEST ASSESSMENT

### Solar Perpetual Flight
- **Claim:** Perpetual flight achievable in UK summer
- **Reality:** Only for purpose-built aircraft (Zephyr class). A multipurpose 8m platform achieves L/D 15-22, not 30-35. Corrected energy balance shows ~9,000 Wh/day deficit, not surplus. Solar extends missions from hours to longer, but doesn't enable perpetual flight on a multipurpose airframe.
- **Action:** Reclassify solar as "endurance extension" not "perpetual flight"

### Laser Power Beaming
- **Claim:** 19% efficiency, £100-250K system cost, 10-20kg laser mass
- **Reality:** 10-12% realistic efficiency. Laser systems weigh 80-200kg not 10-20kg. Cost £2-10M not £100-250K. Scintillation not modelled. Gondola pointing stability is a major unsolved problem.
- **Action:** Archive as long-term R&D concept. The physics is sound but the engineering is 10x harder and more expensive than documented.

### Rigid Airship
- **Claim:** £5-20M per airship, national network of 30-80
- **Reality:** Comparable projects cost £50-200M per unit. 30-year commercial airship failure history. Geodesic antenna claim physically unworkable. National network permanently loss-making at projected revenues.
- **Action:** Archive as decade-plus vision. The stratospheric balloon variant (Raven Aerostar class) is the viable near-term path.

### Tileable Microdrone
- **Claim:** 180g, 2m freefall recovery, 2.5/sec deployment
- **Reality:** Prototype will be 195-210g. Freefall recovery is 4-6m (tumble case). Vertical collision risk during deployment unanalysed. Thrust-to-weight ratio marginal at mid-pack voltage (1.25:1).
- **Action:** Build and test — the design is fundamentally sound but every number needs experimental validation. Do not trust the paper specs.

### Regulatory Strategy
- **Claim:** £3,587 to UK BVLOS
- **Reality:** £8,000-15,000 including RPC-L2 training, SORA preparation, commercial insurance, and documentation. India-first strategy not executable without company and travel budget. Zipline comparison misleading (they had $600M).
- **Action:** Revise cost estimates upward. Focus on Open A3 → PDRA01 progression. Defer international plans until company exists.

### Business Model
- **Claim:** 80-90% margins, multi-sector from day one
- **Reality:** Drone services margins are 30-50%. No customer validation. No pricing model. Established DJI-equipped operators already serve the target market.
- **Action:** Pick ONE sector (conservation survey), find THREE named potential customers, model full cost-per-mission, earn £5,000 before worrying about anything else.

### Ground Station
- **Claim:** £83K automated airbase, 60-second battery swap
- **Reality:** Civil works alone push past £100K. DIY battery swap with £300 gantry won't achieve 60s reliably. Pneumatic catapult requires pressure vessel certification (PSSR 2000). State machine missing 5+ critical states.
- **Action:** Start with bungee launch + in-place charging (buildable). Add automation incrementally.

---

## WHAT'S ACTUALLY SOLID

Despite 35 FAIL verdicts, the audits confirmed several things work:

1. **Mission engine Phase A** — generates valid .waypoints files, works in SITL (PASS)
2. **Waypoint file format** — correct QGC WPL 110, right precision, right field order (PASS)
3. **Range validation** — catches dangerous total route distances (PASS)
4. **GPIO payload detection** — contradictions resolved, consistent design (PASS)
5. **Detent pin locking** — contradictions resolved, both docs agree (PASS)
6. **97% tileable packing efficiency** — geometrically correct (PASS)
7. **Winter solar analysis** — correctly identifies perpetual flight impossible (PASS)

The foundation is real. The bugs are fixable. The vision docs need recalibration.

---

## RECOMMENDED PRIORITY ORDER

```
  PRIORITY 1 (Before summer build):
  ├── Fix upload.py for real Pixhawk (MISSION_REQUEST_INT)
  ├── Update payload config.py (clearance 0.5mm, angle 45°)
  ├── Add metal lanyard anchors to CAD
  ├── Write missing tests (target 80% coverage)
  └── Document AMSL vs AGL for home altitude

  PRIORITY 2 (During summer build):
  ├── Validate payload interface with actual hardware
  ├── Measure real CG range with different payloads
  ├── Thrust-stand test the microdrone motor/prop combo
  ├── Drop-test freefall recovery (measure actual altitude loss)
  └── First real autonomous flight with validated upload code

  PRIORITY 3 (Post-summer):
  ├── Revise all cost estimates in vision docs
  ├── Find 3 named conservation survey customers
  ├── Budget RPC-L2 training (£800-1,500)
  ├── Model full cost-per-mission honestly
  └── Decide: purpose-built solar variant vs solar-as-supplement
```

---

### Tube-Launch Folding Wing
- **Claim:** 99.5% wing deployment reliability, 2m freefall recovery, PERDIX-comparable
- **Reality:** PERDIX had ~93% deployment success after years of DARPA funding. Asymmetric spring deployment causes uncontrollable tumble (430°/s roll). Pusher prop firing nose-down pushes nose further down. Over-centre wing detent may fold under 2g pull-out loads. Minimum deployment altitude should be 80-100m, not 50m.
- **Action:** Build bare-airframe prototypes for destructive drop testing. Redesign wing lock to positive mechanical latch. Add drogue chute or weathervaning tail.

---

*Audit conducted by 10 independent Sonnet agents, March 2026. All 10 complete.*
