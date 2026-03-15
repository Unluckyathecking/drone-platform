# Technical Specifications — Efficient Cargo Drone

## Design Category
**High-aspect-ratio fixed-wing pusher-prop UAV** (long-endurance cargo drone)

## Target Performance Envelope

| Parameter        | Target         | Notes                          |
|------------------|----------------|--------------------------------|
| Wingspan         | 2–4 m          | Higher = more efficient        |
| Payload          | 1–5 kg         | Medical supplies, lab samples  |
| Range            | 80–200 km      | One-way or round-trip TBD      |
| Endurance        | 2–8 hours       |                                |
| Cruise speed     | 70–110 km/h    | Slow = efficient               |
| Payload fraction | 20–40% of MTOW | Key efficiency metric          |

## Core Design Principles

### 1. High Lift-to-Drag Ratio (L/D)
- Target: L/D ≈ 15–25
- Achieved through long, glider-like wings
- Reduces energy needed per kilometre

### 2. Pusher Propeller Configuration
- Propeller mounted at rear of fuselage
- Clean airflow over wings and sensors at front
- Less aerodynamic interference
- Large, slow-spinning props are more efficient than small fast ones

### 3. Slow Cruise Speed
- Flying slower reduces drag dramatically
- Sweet spot: 70–110 km/h for this class

### 4. Lightweight Structure
- Carbon fibre or foam composites
- High strength-to-weight ratio
- Target: powered glider efficiency

## Configuration Options

| Configuration          | Pros                              | Cons                        |
|------------------------|-----------------------------------|-----------------------------|
| High-wing pusher       | Simple, proven, stable            | Needs runway/catapult       |
| Flying wing cargo      | Very efficient, compact           | Harder to design/control    |
| Twin-boom pusher       | Good payload volume, stable       | Slightly heavier            |
| VTOL-fixed-wing hybrid | Lands anywhere (no runway needed) | Heavier, more complex       |

## Key Fact
> The most efficient cargo drones behave more like powered gliders than traditional aircraft. Some can fly 100 km using only the energy in a laptop battery.

## Autopilot Options
- **PX4** — open source, widely used
- **ArduPilot** — open source, very mature
- Both support GPS waypoint navigation, autonomous flight, return-to-home
