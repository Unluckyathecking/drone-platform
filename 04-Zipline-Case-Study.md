# Case Study — Zipline Drone Delivery System

## Overview
Zipline is the leading example of fixed-wing cargo drone delivery at scale in Africa. Understanding their system is key to designing a competing or complementary product.

## How the System Works

### Order Flow
1. Hospital sends order via app/SMS
2. Distribution hub receives and processes order
3. Drone loaded with payload
4. Catapult launch from hub
5. Autonomous GPS navigation to hospital
6. Payload dropped by small parachute (no landing)
7. Drone returns automatically to hub
8. Recovery by capture wire system

### Platform 1 Specs (approximate)
- Fixed-wing design
- Electric propulsion
- Range: ~190 km round-trip
- Payload: ~1.75 kg
- Cruise speed: ~100 km/h
- Launches by pneumatic catapult
- Recovers by tailhook + wire

## What Makes Zipline Work
- **No runway needed at delivery site** — parachute drop
- **Centralised hub model** — one hub serves many hospitals
- **Autonomous flight** — GPS waypoint navigation
- **Fast turnaround** — battery swap, reload, relaunch

## Potential Improvements / Differentiation
- Eliminate catapult dependency (hand-launch or VTOL hybrid?)
- Increase payload capacity beyond 1.75 kg
- Use open-source autopilot to reduce cost
- Design for local manufacturing and repair
- Belly landing or net recovery instead of wire system
- Modular payload bay for different cargo types

## Lessons for Our Design
1. Fixed-wing pusher is proven for this mission
2. Parachute delivery avoids need for landing infrastructure
3. Hub-and-spoke model makes logistics scalable
4. Simplicity of operations matters as much as drone performance
5. Regulatory relationships in-country are critical
