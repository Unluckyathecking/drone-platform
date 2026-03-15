# Physics & Engineering Principles

## Why Fixed-Wing Beats Multirotor for Cargo

Fixed-wing drones use **aerodynamic lift** (wing generates lift from forward motion).
Multirotors use **powered lift** (rotors must constantly push air down).

Result: fixed-wing uses ~5-10x less energy per km for the same payload.

## The Three Optimisation Variables

### 1. Lift-to-Drag Ratio (L/D)
- Measures aerodynamic efficiency
- L/D = Lift Force / Drag Force
- Higher L/D = less thrust needed = less energy per km
- Gliders: L/D ≈ 30-50
- Efficient cargo UAVs: L/D ≈ 15-25
- Typical quadcopter: L/D ≈ 3-5

### 2. Payload Fraction
- Payload mass / Total takeoff mass
- Target: 20-40%
- Every gram of airframe weight reduces payload capacity
- Drives material choices (carbon fibre, foam core, 3D printed parts)

### 3. Propulsion Efficiency
- Large diameter, slow RPM propellers are more efficient
- Pusher config avoids prop wash over fuselage (less drag)
- Electric motors: ~85-90% efficient
- Matching prop to motor KV rating is critical

## Range Estimation (Breguet-style for electric)

```
Range = (Battery_Energy / Total_Mass) × (L/D) × (Propulsion_Efficiency) / g
```

Where:
- Battery_Energy in Joules (Wh × 3600)
- Total_Mass in kg
- L/D is lift-to-drag ratio (dimensionless)
- Propulsion_Efficiency ≈ 0.7-0.85
- g = 9.81 m/s²

This equation shows why L/D and lightweight construction matter so much.

## Wing Design Basics

### Aspect Ratio (AR)
- AR = Wingspan² / Wing Area
- Higher AR = less induced drag = better L/D
- Trade-off: very high AR wings are fragile and harder to transport

### Airfoil Selection
- Low Reynolds number airfoils needed (Re ≈ 100,000-500,000 for small UAVs)
- Common choices: Eppler, Selig, Clark Y series
- Balance between lift coefficient and drag at cruise speed

## Structural Considerations
- Spar: carbon fibre tube or I-beam
- Skin: foam core with fiberglass/carbon layup
- Fuselage: payload bay + battery + avionics
- Keep centre of gravity forward of aerodynamic centre for stability
