# Drone Project — Overview

## Vision

Build a **multipurpose autonomous fixed-wing drone platform** with hotswappable payloads and an intelligent mission planning engine. One airframe, many roles — from cargo delivery to ISR to search and rescue.

## Platform Concept

```
┌─────────────────────────────────────────────────┐
│  AIRFRAME — Mini UAV class                       │
│  High-AR glider wings, pusher prop, electric     │
│  2-4m wingspan, ArduPilot on Pixhawk             │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ HOTSWAP PAYLOAD BAY                         │ │
│  │  ├─ Cargo pod (aid, food, meds, munitions)  │ │
│  │  ├─ Camera/ISR suite (gimbal, FPV)          │ │
│  │  ├─ SAR sensor pod (thermal + visible)      │ │
│  │  ├─ Radar/LiDAR scanner                     │ │
│  │  ├─ Comms relay                             │ │
│  │  └─ Generic sensor bay (future payloads)    │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ MISSION PLANNING ENGINE                     │ │
│  │  Goal → Constraints → Route → MAVLink file  │ │
│  │  Fully autonomous execution via ArduPilot   │ │
│  └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## Project Status

- [x] Initial research and concept exploration
- [x] Platform concept defined (multipurpose, automated)
- [x] Airframe selection (Skywalker X8 recommended)
- [x] Autopilot selected (ArduPilot on Pixhawk 6C)
- [x] Mission engine architecture designed
- [x] Payload interface designed (dovetail rail + quick-release)
- [x] UK CAA regulations researched
- [x] Test site identified (ERFC / Caterham club)
- [ ] Get Flyer ID + Operator ID + BMFA membership
- [ ] Set up SITL development environment
- [ ] Build mission engine Phase A (basic waypoint generator)
- [ ] Purchase airframe + avionics (~£700-800)
- [ ] First autonomous SITL mission
- [ ] First real autonomous flight
- [ ] Build payload interface
- [ ] First payload module (cargo pod)

## Key Design Philosophy

- **Automated from the start** — mission engine is the primary interface, not an RC controller
- **Modular by design** — standardized payload bay for any mission type
- **Platform, not product** — reusable for any future project
- **Efficiency over speed** — glider-like aerodynamics for endurance
- **Open-source stack** — ArduPilot, Python, pymavlink

## Notes Index

| File | Contents |
|------|----------|
| [01-Market-Research](01-Market-Research.md) | Operational context, target countries, use cases |
| [02-Technical-Specs](02-Technical-Specs.md) | Target performance specs, configuration options |
| [03-Physics-and-Engineering](03-Physics-and-Engineering.md) | Aerodynamic principles, range equations, wing design |
| [04-Zipline-Case-Study](04-Zipline-Case-Study.md) | Zipline system analysis, lessons learned |
| [05-African-Air-Defence-Context](05-African-Air-Defence-Context.md) | Air defence landscape, operational considerations |
| [06-Development-Roadmap-and-Test-Plan](06-Development-Roadmap-and-Test-Plan.md) | Phased roadmap, test plans, risk register |
| [07-Mission-Engine-Architecture](07-Mission-Engine-Architecture.md) | Mission engine design, data models, MAVLink integration |
| [08-Payload-System-Design](08-Payload-System-Design.md) | Hotswap interface, payload modules, CG management |
| [09-UK-Regulations-and-Test-Sites](09-UK-Regulations-and-Test-Sites.md) | CAA licensing, test sites, BVLOS path |

## Immediate Next Steps

1. **This week:** Get Flyer ID + Operator ID (free online, 30 min)
2. **This week:** Install ArduPilot SITL on laptop, run first simulation
3. **Weeks 1-3:** Build mission engine Phase A (Python → .waypoints → SITL)
4. **Week 2:** Contact ERFC or Caterham club, join BMFA
5. **Week 4:** Order Skywalker X8 + Pixhawk 6C + avionics (~£700-800)

## Budget Summary

| Phase | Cost |
|-------|------|
| Mission engine development (software) | £0 (open-source tools) |
| Airframe + avionics | £700-800 |
| Payload interface system | £70 |
| First payload (cargo pod) | £30 |
| CAA registration + BMFA | £52/yr |
| **Total to first autonomous flight with payload** | **~£850-950** |
