# TODOS

## Phase A Deferred Work

### TODO: Automated SITL E2E test harness
**What:** Script that launches SITL, uploads a mission, monitors MISSION_ITEM_REACHED events, asserts completion, and exits.
**Why:** Manual SITL testing works for learning but doesn't catch regressions when you modify the waypoint writer or planner.
**Effort:** S (50 lines of pymavlink code)
**Priority:** P2 — build by end of Phase A, after manual testing is comfortable.
**Depends on:** Phase A core (models, planner, writer) must be working first.

### TODO: Waypoint file parser (read .waypoints back into Mission objects)
**What:** Inverse of the writer — parse a QGC WPL 110 file into Mission/MissionItem objects.
**Why:** Enables roundtrip testing (write → parse → compare), importing missions from QGC/Mission Planner, and future mission editing.
**Effort:** S (mirrors the writer, ~40 lines)
**Priority:** P3 — nice for testing but not blocking.
**Depends on:** Writer must be stable first.

## Phase B+ Deferred Work

### TODO: Full Goal/ConstraintSet data model hierarchy
**What:** Expand from BasicMission to the full Goal → ConstraintSet → Mission architecture documented in 07-Mission-Engine-Architecture.md.
**Why:** Phase B mission types (SAR, ISR, loiter) need structured goal input and constraint checking.
**Effort:** M
**Priority:** P1 for Phase B
**Depends on:** Phase A complete.

### TODO: Rewrite doc 06 Phases 2-7 for automation-first
**What:** Phase 0 has been fixed. Phases 2-7 still reference manual flight progression and may have stale dependencies.
**Why:** Documentation consistency — the roadmap should match the automation-first philosophy throughout.
**Effort:** S
**Priority:** P3 — not blocking any work.

### TODO: Remote ID compliance research
**What:** Research Remote ID hardware/software options for the UK 2028 deadline.
**Why:** Mandatory for privately-built drones by Jan 2028. Need to plan early to avoid retrofit.
**Effort:** S (research only)
**Priority:** P3 — deadline is far out.
**Depends on:** Airframe selection finalized.
