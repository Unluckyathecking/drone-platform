# Tube-Packaged Folding-Wing Drone Variants

## Concept Overview

An alternate form factor for the multi-scale platform family (see 22-Multi-Scale-Platform-Family.md), optimized for dense cylindrical tube packing and rapid mass deployment. The same design philosophy applies -- pusher prop, ArduPilot, modular payload, composite construction -- but the airframe is redesigned around the constraint of fitting inside a tube with wings and tail that fold/deploy after ejection.

Two variants are specified:
- **Variant A (MICRO Tube):** Sonobuoy-sized, 80-120mm diameter, 300-800g. Reference: PERDIX, Coyote Block 1.
- **Variant B (MINI Tube):** Torpedo-tube-sized, 150-200mm diameter, 3-10kg. Reference: Coyote, JSOW/Rapid Dragon.

Both share a common deployment philosophy: eject from tube, freefall briefly, deploy wings and tail via spring mechanisms, start propulsion, stabilize under ArduPilot control, execute mission.

---

## VARIANT A: MICRO Tube (Sonobuoy-Sized)

### Dimensional Envelope

```
  TUBE CONSTRAINTS
  ════════════════

  Outer tube diameter:   124 mm (A-size sonobuoy standard)
  Inner tube diameter:   118 mm (3mm wall thickness)
  Tube length:           500 mm (standard sonobuoy length is 914mm;
                                 we use half-length for lighter drone)

  Available cross-section for drone:  ~110mm diameter circle
  (allowing 4mm clearance per side for rails/guides)

  DRONE SPECIFICATIONS (STOWED)
  ═════════════════════════════
  Fuselage diameter:     75 mm (circular cross-section)
  Fuselage length:       420 mm (nose to prop hub)
  Folded wing envelope:  110 mm diameter (wings wrapped around fuselage)
  Total stowed length:   450 mm (including folded prop)
  Mass:                  550 g (target), 700 g (maximum)

  DRONE SPECIFICATIONS (DEPLOYED)
  ═══════════════════════════════
  Wingspan:              700 mm
  Wing chord:            90 mm (root), 65 mm (tip)
  Wing area:             ~5.3 dm^2
  Aspect ratio:          ~9.2
  Tail span:             200 mm (cruciform)
  Overall length:        430 mm (nose to tail trailing edge)
  Wing loading:          ~10-13 g/dm^2
```

### Cross-Section View (Stowed in Tube)

```
  LOOKING FROM FRONT (nose-on view, stowed in tube)
  ══════════════════════════════════════════════════

            ┌─── Tube wall (124mm OD) ───┐
           ╱                               ╲
          │    ╱── Wing panel A (wrapped)    │
          │   ╱  ┌───────────────┐           │
          │  ╱   │               │  ╲        │
          │ │    │   FUSELAGE    │   │       │
          │ │    │   (75mm dia)  │   │       │
          │  ╲   │               │  ╱        │
          │   ╲  └───────────────┘           │
          │    ╲── Wing panel B (wrapped)    │
           ╲                               ╱
            └─────────────────────────────┘

  DETAIL: Wing wrapping scheme
  ────────────────────────────
  Each wing panel (350mm semi-span) has a single hinge at the root.
  Wings fold BACKWARD along the fuselage, then INWARD to wrap partially
  around the fuselage body. The leading edges of both wing panels face
  outward, pressed against the inner tube wall.

  Cross-section packing:
  ┌──────────────────────┐
  │      110mm           │
  │   ╭──────────╮       │
  │  ╱  wing A    ╲      │   Wing panels occupy the crescent-shaped
  │ │ ╭──────────╮ │     │   space between the 75mm fuselage and the
  │ │ │ fuselage │ │     │   110mm available diameter.
  │ │ │  75mm    │ │     │
  │ │ ╰──────────╯ │     │   Each wing panel is ~4mm thick (foam core
  │  ╲  wing B    ╱      │   with carbon skin), so two panels stacked
  │   ╰──────────╯       │   radially = 8mm.
  │                       │
  │  75 + 2*8 = 91mm     │   Fits within 110mm with 19mm margin for
  │  (minimum envelope)   │   hinge mechanisms and wiring.
  └──────────────────────┘
```

### Side View (Stowed in Tube)

```
  SIDE VIEW (stowed in tube, nose pointing UP for vertical ejection)
  ══════════════════════════════════════════════════════════════════

  ┌─────────┐ ← Tube cap (blowout panel or spring-loaded lid)
  │ ┌─────┐ │
  │ │NOSE │ │  ← Pitot tube (retracted), GPS antenna (conformal)
  │ │     │ │
  │ ├─────┤ │  ← Forward avionics bay: flight controller, GPS, IMU
  │ │ FC  │ │     Pixhawk Nano or custom STM32-based FC
  │ │ GPS │ │     20g total
  │ ├─────┤ │
  │ │BATT │ │  ← Battery: 2S 850mAh LiPo (50g)
  │ │     │ │     Provides ~20 min endurance at cruise
  │ ├─────┤ │
  │ │ P/L │ │  ← Payload bay: 50-150g capacity
  │ │     │ │     Mini camera, sensor, or expendable package
  │ ├─────┤ │
  │ │WINGS│ │  ← Folded wing section (wings wrapped around fuselage)
  │ │(fold│ │     Spring-loaded root hinges held by retaining band
  │ │ ed) │ │     Retaining band releases when drone exits tube
  │ ├─────┤ │
  │ │TAIL │ │  ← Cruciform tail fins (folded flat against fuselage)
  │ │(fold│ │     4 fins, spring-loaded, fold forward along body
  │ │ ed) │ │
  │ ├─────┤ │
  │ │MOTOR│ │  ← Brushless motor + ESC (30g total)
  │ │PROP │ │     Folding propeller (2-blade, 6x3 or 7x3.5)
  │ │     │ │     Blades fold forward against motor shaft
  │ └─────┘ │
  │ [PISTON]│ ← Ejection piston (spring or pneumatic)
  └─────────┘ ← Tube base cap

  Component stack (nose to tail):
  ──────────────────────────────
  Nose fairing:      15mm
  Avionics bay:      60mm   (FC + GPS + receiver + ESC)
  Battery:           70mm   (2S 850mAh pack)
  Payload bay:       80mm   (modular, accepts mini payloads)
  Wing fold zone:    100mm  (folded wing panels + hinge mechanisms)
  Tail fold zone:    50mm   (cruciform fins folded forward)
  Motor + prop:      55mm   (motor bell + folded prop blades)
  ──────────────────────────────
  TOTAL:             430mm  (within 450mm stowed length budget)
```

### Wing Folding Mechanism (Variant A)

```
  WING DEPLOYMENT SEQUENCE
  ════════════════════════

  STEP 1: STOWED (in tube)

  Wings folded backward along fuselage, held by Kevlar retaining band.
  Band passes through a slot in the tube wall near the muzzle.

           ┌─ retaining band (Kevlar loop)
           │
    ───────┤═══════════════════┤────────
    nose   │    fuselage       │  motor
           │  ╱── wing A ──╲  │
           │ ╱   (folded)   ╲ │
           └────────────────────

  STEP 2: EJECTION (band shears or slides off as drone exits tube)

  As the drone is pushed out of the tube, the retaining band catches
  on the tube lip and slides off the fuselage. Wings are now free but
  still folded by airflow pressure during initial ejection.

    ───────═══════════════════────────
    nose      fuselage         motor
              ╱── wing A ──╲
             ╱   (released) ╲

  STEP 3: WINGS DEPLOY (0.1-0.3 seconds after ejection)

  Torsion springs at root hinges (0.15 N-m each) drive wings outward.
  Aerodynamic forces assist once wings begin to open.
  Wings snap to deployed position and lock via over-center detent.

                      ╱ wing A
                     ╱
    ────────════════╱═══════════════────────
    nose   fuselage      tail        motor
    ────────════════╲═══════════════────────
                     ╲
                      ╲ wing B

  STEP 4: LOCKED AND FLYING

  Over-center spring detent locks each wing at the deployed dihedral
  angle (2-3 degrees). The detent provides a positive "click" lock
  that requires ~5x the deployment spring force to overcome.
  No return to folded state is possible in flight.

  HINGE DETAIL (root hinge, viewed from above):
  ══════════════════════════════════════════════

  FOLDED:                    DEPLOYED:

  fuselage ─┬─ hinge pin    fuselage ─┬─ hinge pin
             │                         │
             ├── wing                  ├────── wing ──────
             │  (along body)           │  (perpendicular)
             │                         │
         torsion spring            spring relaxed,
         (loaded, 0.15 Nm)        detent engaged
```

### Tail Deployment (Variant A)

```
  CRUCIFORM TAIL (4 fins)
  ═══════════════════════

  Fin dimensions: 60mm span x 50mm chord each
  Total tail span: 200mm (tip-to-tip, horizontal pair)

  STOWED:                        DEPLOYED:

  Fins fold FORWARD along            │
  the fuselage, flat against         ─┼─  ← cruciform, 4 fins
  the body. Held by friction          │      at 90-degree intervals
  fit inside tube wall.
                                 Each fin has a leaf spring at root.
  ├──fin──┤                      When tube constraint is removed,
  │fuselage│                     springs push fins to 90-degree
  ├──fin──┤                      deployed position in <50ms.

  LOCK: Each fin has a small over-center dimple that the spring
  drives past. Once deployed, fin cannot fold back under flight loads.

  SIDE VIEW (deployed):

                         ┌── vertical fin (upper)
                         │
  ══════════════════════─┤─ ◎ ← motor + prop
                         │
                         └── vertical fin (lower)

  (Horizontal fins not shown -- they extend left and right)
```

### Propeller Deployment (Variant A)

```
  FOLDING PROPELLER
  ═════════════════

  2-blade folding propeller, 6-inch (152mm) diameter, 3-inch pitch.
  Blades fold FORWARD against the motor shaft when not spinning.

  STOWED:                    DEPLOYED:

       │                          │
   ────┤── blade A               ─┤─
   ────┤── blade B               ─┤─  ← blades extend under
       │   (folded forward)       │     centrifugal force when
       ●   motor bell             ●     motor spins up

  Deployment method: CENTRIFUGAL FORCE
  - Motor spins up to idle (~3000 RPM)
  - Centrifugal force overcomes blade hinge friction
  - Blades swing outward to fully deployed position
  - At operating RPM (8000-12000), centrifugal force holds blades rigid
  - No mechanical lock needed -- centrifugal retention is sufficient

  Time to deploy: <0.2 seconds from motor start to stable thrust

  PROP CLEARANCE IN TUBE:
  Folded prop blades (each ~70mm long, 12mm wide) lie flat against
  motor shaft. Folded envelope: 75mm diameter (fits within fuselage OD).
```

### Tube Orientation and Ejection

```
  EJECTION CONFIGURATION: NOSE-FIRST, DOWNWARD
  ═════════════════════════════════════════════

  For air-deployed systems (dropped from carrier aircraft or dispenser):
  Tube is oriented vertically with nose pointing DOWN.

  ┌───────────┐ ← Tube top (sealed, attached to carrier)
  │  [SPRING] │ ← Compressed spring (15-25 N, 30mm travel)
  │  ┌─────┐  │
  │  │MOTOR│  │ ← Drone tail end (motor + folded prop)
  │  │TAIL │  │
  │  │WINGS│  │
  │  │ P/L │  │
  │  │BATT │  │
  │  │ FC  │  │
  │  │NOSE │  │ ← Drone nose (exits first)
  │  └─────┘  │
  ├───────────┤ ← Blowout panel or spring-loaded cap
  └───────────┘   (breaks away under spring force)

  EJECTION SEQUENCE:

  1. Controller signals ejection (solenoid releases spring catch)
  2. Spring drives piston downward, pushing drone out nose-first
  3. Blowout panel breaks free (retained by lanyard to prevent FOD)
  4. Drone exits at 3-8 m/s relative to tube
  5. Retaining band slides off at tube lip, freeing wings
  6. Drone enters freefall + forward airspeed from carrier

  SPRING EJECTION PARAMETERS:
  ─────────────────────────────
  Drone mass:           0.55 kg
  Spring force:         20 N (average over stroke)
  Spring stroke:        30 mm
  Energy:               0.6 J
  Exit velocity:        v = sqrt(2 * 0.6 / 0.55) = 1.48 m/s

  This is LOW -- for gravity-drop from a moving carrier, 1.5 m/s
  downward plus ~20 m/s forward airspeed from the carrier is sufficient.
  The drone needs only to clear the tube, not achieve flight speed.

  For ground-launched or vertical tube systems:
  Pneumatic ejection with CO2 cartridge:
  - Chamber pressure: 5-8 bar
  - Piston area: ~70 cm^2
  - Force: 350-560 N
  - Over 30mm stroke: 10.5-16.8 J
  - Exit velocity: 6.2-7.8 m/s (adequate for vertical launch)
```

### Deployment Sequence with Timing (Variant A)

```
  FULL DEPLOYMENT TIMELINE
  ════════════════════════

  T = 0.000s  EJECT command received
              Spring releases, drone begins exiting tube

  T = 0.050s  Drone nose clears tube
              Retaining band begins sliding off

  T = 0.100s  Drone fully clear of tube
              Retaining band released -- wings FREE
              Tail fins spring outward (tube constraint removed)
              IMU begins sensing freefall + airspeed

  T = 0.150s  Tail fins fully deployed and locked (cruciform)
              Wings beginning to swing outward (torsion springs)

  T = 0.250s  Wings at ~45 degrees -- aerodynamic force now assists
              Significant deceleration begins (drag increasing)

  T = 0.350s  Wings fully deployed and locked (over-center detent)
              Drone now has full aerodynamic surfaces
              ArduPilot detects valid airspeed + attitude data

  T = 0.400s  Motor starts spinning (ESC receives throttle command)
              Prop blades begin unfolding under centrifugal force

  T = 0.500s  Prop fully deployed, generating thrust
              ArduPilot enters FBWA (Fly By Wire A) stabilization

  T = 0.700s  Drone has pulled out of dive, climbing or level
              GPS lock acquired (antenna now pointed skyward)

  T = 1.000s  Full autonomous flight established
              Drone transitions to AUTO mode, begins mission waypoints

  ALTITUDE BUDGET:
  ────────────────
  Freefall during 0-0.35s: ~0.6m (mostly spring ejection, low speed)
  Dive during 0.35-0.70s: ~8-15m (wings deployed but gaining speed,
                           converting altitude to airspeed)
  Pull-out arc: ~5-10m additional altitude loss

  TOTAL ALTITUDE LOSS: 15-25m from ejection to level flight

  MINIMUM SAFE DEPLOYMENT ALTITUDE: 50m AGL
  (provides 25-35m margin for deployment failures and wind gusts)
```

### Component Mass Budget (Variant A)

```
  MASS BUDGET: VARIANT A (MICRO TUBE)
  ════════════════════════════════════

  Component                  Mass (g)    Notes
  ─────────────────────────  ────────    ──────────────────────────
  Airframe (fuselage)           80       3D-printed nylon or carbon tube
  Wing panels (2x)              60       EPP foam core, carbon skin
  Wing hinges + springs         15       Stainless steel spring + Al hinge
  Wing retaining band            2       Kevlar cord
  Tail fins (4x)                20       Carbon fiber sheet, 1mm
  Tail springs + detents         8       Stainless leaf springs
  Motor (2206 size)             28       Brushless outrunner
  ESC (20A)                     10       BLHeli_S compact
  Propeller (6x3 folding)        6       Nylon folding prop
  Flight controller             12       Custom STM32F4 or Matek F405 Nano
  GPS module                     8       u-blox M10 mini
  IMU (onboard FC)               -       Included in FC weight
  Receiver (ELRS 2.4G)           2       Micro receiver
  Battery (2S 850mAh)           50       LiPo, 25C discharge
  Wiring + connectors           12       JST-SH, silicone wire
  Payload (mission-specific)   100       Camera, sensor, or expendable
  Structural fasteners           8       M2 screws, pins, adhesive
  ─────────────────────────  ────────
  TOTAL                        511 g     Within 550g target

  Margin to 700g max:          189 g     Available for heavier payloads
```

### Payload Options (Variant A)

```
  MICRO TUBE PAYLOAD OPTIONS
  ══════════════════════════

  The payload bay is 30mm diameter x 80mm long (~56 cm^3 volume).
  Mass budget: 50-200g (depending on other component choices).

  A. VISUAL SENSOR (ISR)
     ├── Micro FPV camera (RunCam Nano 2, 2g)
     ├── Video transmitter (25mW, 2g)
     ├── SD card recorder (5g)
     └── Total: ~15g, leaves mass margin for other sensors

  B. ELECTRONIC DECOY
     ├── RF emitter module (ESP32 + amplifier, 8g)
     ├── Programmable to mimic radar return or comms signature
     └── Total: ~12g

  C. ENVIRONMENTAL SENSOR
     ├── Gas/particulate sensor (BME680 + PM2.5, 5g)
     ├── Temperature + humidity + pressure (onboard)
     └── Total: ~10g

  D. COMMUNICATIONS RELAY NODE
     ├── LoRa transceiver (RFM95W, 2g)
     ├── PCB antenna (trace, <1g)
     ├── Dedicated processor (ESP32-C3, 3g)
     └── Total: ~8g

  E. ACOUSTIC SENSOR (noise monitoring, wildlife survey)
     ├── MEMS microphone array (3x SPH0645, 3g)
     ├── Audio processor (onboard FC or dedicated)
     └── Total: ~8g

  Note: The Variant A payload interface is NOT the same dovetail as the
  standard platform. Instead, it uses a cylindrical bayonet mount:
  - Payload module is a cylinder (28mm dia x 75mm long)
  - Twist-lock bayonet with 2 lugs (1/4 turn to lock)
  - 4-pin pogo connector for power + data (5V, UART TX, UART RX, GND)
  - Auto-detection via I2C EEPROM on payload module
```

---

## VARIANT B: MINI Tube (Torpedo-Tube-Sized)

### Dimensional Envelope

```
  TUBE CONSTRAINTS
  ════════════════

  Outer tube diameter:   200 mm
  Inner tube diameter:   190 mm (5mm wall, structural aluminum or CF)
  Tube length:           1200 mm

  Available cross-section for drone:  ~180mm diameter circle
  (allowing 5mm clearance per side for rail guides)

  DRONE SPECIFICATIONS (STOWED)
  ═════════════════════════════
  Fuselage cross-section: 140mm wide x 120mm tall (oval)
  Fuselage length:        1050mm (nose to prop hub)
  Folded wing envelope:   180mm diameter
  Total stowed length:    1100mm (including folded prop)
  Mass:                   6.5 kg (target), 9.0 kg (maximum)

  DRONE SPECIFICATIONS (DEPLOYED)
  ═══════════════════════════════
  Wingspan:              2200 mm (2.2m)
  Wing chord:            180 mm (root), 120 mm (tip)
  Wing area:             ~30 dm^2
  Aspect ratio:          ~16
  Tail span:             500 mm (V-tail)
  Tail boom length:      400 mm (telescoping from fuselage)
  Overall length:        1400 mm (nose to tail tip, with boom extended)
  Wing loading:          ~22-30 g/dm^2
```

### Wing Folding Architecture (Variant B)

The central design challenge: fitting a 2.2m wingspan into a 180mm diameter circle. Three options were evaluated:

```
  OPTION EVALUATION MATRIX
  ════════════════════════

  Option              Complexity  Weight   Reliability  Deployed Stiffness
  ──────────────────  ──────────  ───────  ───────────  ──────────────────
  A. Double-fold      Medium      Low      High         High
  B. Telescoping      High        Medium   Medium       Medium
  C. Wrap-around      Low         Low      High         Medium-Low
  D. Inflatable       Medium      Low      Medium       Low

  SELECTED: OPTION A — DOUBLE-FOLD (primary)
  BACKUP:   OPTION C — WRAP-AROUND (for simplified variant)
```

#### Option A: Double-Fold Wing (Selected)

```
  DOUBLE-FOLD WING MECHANISM
  ══════════════════════════

  Each wing half has TWO hinges:
  - Root hinge (at fuselage attachment)
  - Mid-span hinge (at ~550mm from root, half of semi-span)

  DEPLOYED (top view):

                    mid-span hinge
                         │
  ◄── 550mm ──►◄── 550mm ──►
  ┌────────────┬────────────┐
  │  inner     │   outer    │  ← wing panel (one side)
  │  panel     │   panel    │
  └──────┬─────┴────────────┘
         │
    root hinge
         │
  ══════════════════════════  fuselage
         │
    root hinge
         │
  ┌──────┴─────┬────────────┐
  │  inner     │   outer    │  ← wing panel (other side)
  │  panel     │   panel    │
  └────────────┴────────────┘


  FOLDING SEQUENCE (reverse of deployment):

  Step 1 (deployed):

       outer          inner   │   inner          outer
  ─────────────────────────── │ ───────────────────────────
                              │
                          fuselage

  Step 2 (outer panels fold UNDER inner panels at mid-span hinge):

                     ┌inner┐  │  ┌inner┐
                     │outer│  │  │outer│
                     └─────┘  │  └─────┘
                              │
                          fuselage

  Step 3 (doubled panels fold BACKWARD along fuselage at root hinge):

                              │
  ════════════════════════════│════ fuselage
           ┌inner┐            │
           │outer│  (folded   │
           └─────┘   back)    │
                              │
           ┌inner┐            │
           │outer│            │
           └─────┘            │

  STOWED (looking from front, cross-section):

         ┌── 180mm available ──┐
         │                      │
         │   ┌─── wing ───┐    │
         │   │ ┌────────┐ │    │
         │   │ │fuselage│ │    │   Wing panels (doubled-over) lie
         │   │ │ 140mm  │ │    │   along each side of the fuselage.
         │   │ │        │ │    │
         │   │ └────────┘ │    │   Each doubled panel: ~8mm thick
         │   └─── wing ───┘    │   (2 x 4mm panel)
         │                      │
         │   140 + 2*8 = 156mm │   Fits within 180mm with 24mm margin
         └──────────────────────┘

  HINGE DESIGN:

  Root hinge:
  ├── Aluminum 6061-T6 hinge plates (2mm thick)
  ├── 4mm stainless steel hinge pin
  ├── Torsion spring: 0.8 N-m (sufficient for 300g wing panel)
  ├── Over-center detent lock with 3mm steel ball + spring pocket
  └── Weight: 35g per hinge (x2 = 70g total for root hinges)

  Mid-span hinge:
  ├── Same design, lighter construction
  ├── Torsion spring: 0.4 N-m
  ├── Over-center detent
  └── Weight: 20g per hinge (x2 = 40g total)

  DEPLOYMENT ORDER:
  Root hinges deploy FIRST (wings swing outward from fuselage),
  then mid-span hinges deploy (outer panels swing outward from inner).
  This is achieved by spring preload differential:
  - Root spring: 0.8 N-m, deploys in 0.2s
  - Mid-span spring: 0.4 N-m, but mid-span hinge has a time-delay
    detent that releases 0.15s after root hinge deploys
  - Delay mechanism: a small friction detent on the mid-span hinge
    that holds until aerodynamic force + spring force overcomes it
    once the inner panel is in the airstream

  Total wing deployment time: 0.4-0.6 seconds

  SPAR CONTINUITY:
  The main spar is a carbon fiber tube (8mm OD, 6mm ID) that passes
  through each hinge via a sleeve bearing. When locked, the hinge
  detent also clamps the spar sleeve, creating a rigid joint.
  This provides ~80% of the bending stiffness of a continuous spar.
```

#### Option C: Wrap-Around Wing (Backup)

```
  WRAP-AROUND WING (cruise missile heritage)
  ═══════════════════════════════════════════

  Used on: BGM-109 Tomahawk, AGM-86 ALCM, various cruise missiles.

  The wing is a SINGLE PIECE that wraps around the fuselage body.
  Made from spring steel or pre-stressed composite.

  STOWED (cross-section):

         ┌── 180mm ──┐
         │            │
         │  ╭──────╮  │   Wing is a flat panel that has been bent
         │ ╭│fuse- │╮ │   into a C-shape around the fuselage.
         │ ││lage  ││ │   Leading edge faces outward.
         │ ╰│      │╯ │
         │  ╰──────╯  │   Spring energy stored in the bent wing
         │            │   drives deployment when released.
         └────────────┘

  DEPLOYED:

  Wing unrolls from fuselage and springs flat.
  Residual curve is removed by pre-stressed skin layers.

            ╱                              ╲
  ─────────╱────── fuselage ────────────────╲─────────
           ╲                                ╱
            wing (flat, slight dihedral)

  ADVANTAGES:
  - Simplest mechanism (no hinges at all)
  - Very fast deployment (<0.2s)
  - Lightest option (no hinge hardware)
  - Proven on full-scale cruise missiles

  DISADVANTAGES:
  - Wing must be thin and flexible (limits structural depth)
  - Airfoil shape compromised (cannot use thick high-lift profiles)
  - Wing stiffness is lower than hinged designs
  - Requires specific material layup (spring steel or unidirectional
    carbon with controlled pre-stress)
  - Not suitable for >2m span due to stiffness limitations

  VERDICT: Viable for Variant A (700mm span, thin wing OK).
  Marginal for Variant B (2.2m span needs structural depth).
  Selected as BACKUP for simplified Variant B builds.
```

### Tail Design (Variant B)

```
  V-TAIL ON TELESCOPING BOOM
  ═══════════════════════════

  Variant B uses a V-tail (2 surfaces at 110-degree included angle)
  on a telescoping tail boom, rather than a cruciform.

  Rationale:
  - V-tail has only 2 surfaces (lighter, less drag than cruciform 4)
  - Telescoping boom allows tail arm to extend beyond tube length
  - V-tail provides both pitch and yaw control via ruddervator mixing
    (native ArduPilot support: VTAIL_OUTPUT parameter)

  STOWED:

  ══════════════════════════════════════════
  fuselage    │boom│  ← boom retracted inside fuselage
              │stow│     (400mm boom stored in 140mm fuselage
              │    │      section, telescoping in 2 stages)
  ──v-tail fins folded flat against boom──

  DEPLOYED:

  ══════════════════════════════════════════════════════════════
  fuselage                    │    boom    │
                              │  (400mm)   │  ╱ V-tail fin (upper)
                              │            │╱
                              │            ├── motor + prop
                              │            │╲
                              │            │  ╲ V-tail fin (lower)

  TELESCOPING BOOM:

  3-stage telescoping tube (like a radio antenna):
  - Inner tube:  20mm OD carbon fiber, 350mm length
  - Middle tube: 26mm OD carbon fiber, 350mm length
  - Outer tube:  32mm OD carbon fiber, 350mm length (fixed to fuselage)

  Retracted length: 400mm (stages nested)
  Extended length:  900mm (additional 500mm behind fuselage)

  Lock: spring-loaded detent balls at each stage extension point.
  Deployment: compressed spring inside outer tube pushes inner
  stages out when retaining pin is released.

  V-TAIL FIN DETAILS:
  ├── Span: 250mm each (500mm total tip-to-tip)
  ├── Chord: 120mm root, 80mm tip
  ├── Area: ~2.5 dm^2 per fin
  ├── Construction: carbon fiber skin, foam core
  ├── Hinge: root hinge, spring-loaded (same design as wing root)
  ├── Servo: 1x 9g micro servo per fin for ruddervator actuation
  ├── Folded: fins fold forward along the boom
  └── Deployment: spring-loaded, deploys when boom extends
      (boom extension removes mechanical stop holding fins)
```

### Fuselage Design (Variant B)

```
  FUSELAGE LAYOUT (side view, stowed)
  ════════════════════════════════════

  ◄──────────────── 1050mm total length ──────────────────►

  ┌──────┬────────┬──────────┬───────────┬──────────┬──────────┬──────┐
  │ NOSE │ AVION- │ BATTERY  │ PAYLOAD   │ WING     │ TAIL     │MOTOR│
  │      │ ICS    │          │ BAY       │ FOLD     │ BOOM     │+PROP│
  │      │        │          │           │ ZONE     │ (stowed) │     │
  │ 40mm │ 120mm  │ 200mm    │ 250mm     │ 220mm    │ 150mm    │70mm │
  └──────┴────────┴──────────┴───────────┴──────────┴──────────┴──────┘

  CROSS-SECTION (fuselage, looking from front):

         ┌── 180mm tube limit ──┐
         │                       │
         │    ┌───────────┐      │
         │    │           │      │   Oval fuselage: 140mm W x 120mm H
         │    │  Payload   │      │
         │    │  Bay       │      │   Payload volume: ~120mm W x 100mm H
         │    │  120x100   │      │   x 250mm L = ~3000 cm^3 (3 liters)
         │    │           │      │
         │    └───────────┘      │   Usable payload mass: 1.5-3.5 kg
         │                       │
         └───────────────────────┘

  FUSELAGE CONSTRUCTION:
  ├── Monocoque carbon fiber shell (2-layer, 0.5mm wall)
  ├── Internal bulkheads at each bay boundary (CNC plywood, 3mm)
  ├── Payload bay has removable side panel for access
  ├── Wing attachment frames: machined aluminum inserts bonded into shell
  ├── Nose cone: 3D-printed ASA or nylon, contains pitot and antennas
  └── Total fuselage structural mass: ~350g

  PAYLOAD BAY INTERFACE:

  The standard dovetail rail from the main platform (08-Payload-System-Design.md)
  is adapted for the tube form factor:

  Standard (open airframe):     Tube variant:
  ┌─────────────────────┐       ┌─────────────────────┐
  │ slide in from below │       │ slide in from side   │
  │ dovetail + pins     │       │ through access panel │
  │ 200mm wide rail     │       │ 120mm wide rail      │
  └─────────────────────┘       └─────────────────────┘

  Electrical interface is IDENTICAL: Anderson PowerPole for power,
  JST-GH 8-pin for data, same ID pin scheme.

  The payload tray is scaled down:
  - Standard: 200mm W x 300mm L x 150mm H, 4.0 kg max
  - Tube variant: 120mm W x 250mm L x 100mm H, 3.5 kg max
  - Tray mass: 0.2 kg (lighter due to smaller size)
```

### Ejection Method (Variant B)

```
  PNEUMATIC EJECTION SYSTEM
  ═════════════════════════

  Variant B uses pneumatic (compressed gas) ejection due to higher mass.
  Spring ejection is impractical for 6.5-9 kg drones.

  SYSTEM COMPONENTS:
  ├── CO2 cartridge: 38g threaded (standard paintball size)
  │   Provides ~18 liters of gas at STP
  ├── Solenoid valve: 12V, normally closed, 3/8" orifice
  ├── Manifold: machined aluminum block
  ├── Piston: HDPE disk, 180mm diameter, O-ring sealed
  └── Burst disk or cap: at tube muzzle end

  EJECTION CALCULATION:
  ─────────────────────
  Piston area:        254 cm^2 (pi * 9^2)
  Working pressure:   3 bar (conservative, CO2 at 20C is ~57 bar;
                      regulator reduces to 3 bar)
  Force:              254 * 3 * 0.1 = 76.2 N per bar = 228.6 N at 3 bar
  Drone mass:         7.0 kg (mid-range)
  Acceleration:       228.6 / 7.0 = 32.7 m/s^2 = 3.3 g (gentle)
  Stroke:             100mm (piston travel)
  Exit velocity:      v = sqrt(2 * 32.7 * 0.1) = 2.56 m/s

  For higher ejection velocity (ground launch, vertical):
  Working pressure:   8 bar
  Force:              610 N
  Acceleration:       87 m/s^2 = 8.9 g
  Exit velocity:      v = sqrt(2 * 87 * 0.1) = 4.17 m/s

  STRUCTURAL LOADS:
  At 8.9 g axial acceleration, a 7 kg drone experiences 610 N axial load.
  This drives structural requirements:
  - Fuselage must withstand 610 N compression (nose-first ejection)
    or tension (tail-first) without buckling
  - Internal components must be secured against 9 g axial
  - Battery: strapped with 2mm nylon webbing, rated to 200 N
  - Flight controller: vibration-isolated mount, M3 bolts
  - Payload: retained by dovetail + spring-loaded latch

  AXIAL LOAD PATH:
  Force from piston → rear bulkhead → fuselage shell →
  internal bulkheads → forward bulkhead → nose cap

  Fuselage shell buckling check (carbon fiber tube, 140mm dia, 0.5mm wall):
  Critical buckling load = 0.6 * E * t / R
  E (CF) = 70 GPa, t = 0.5mm, R = 70mm
  Sigma_cr = 0.6 * 70000 * 0.5 / 70 = 300 MPa
  Cross-section area = pi * 140 * 0.5 = 220 mm^2
  Critical load = 300 * 220 = 66,000 N

  Safety factor: 66,000 / 610 = 108x — fuselage will not buckle.
  (Real-world knockdown factor of ~0.3 still gives 32x margin.)
```

### Deployment Sequence with Timing (Variant B)

```
  FULL DEPLOYMENT TIMELINE (VARIANT B)
  ════════════════════════════════════

  T = 0.000s   EJECT command received
               Solenoid valve opens, CO2 drives piston

  T = 0.050s   Nose cap separates (burst disk or latch release)
               Drone begins moving in tube

  T = 0.200s   Drone fully exits tube (nose-first)
               Enters freefall + carrier airspeed
               Tail boom retaining pin pulled by lanyard attached to tube

  T = 0.300s   Tail boom extends (spring-loaded, 3 stages telescope out)
               V-tail fins begin deploying as boom extends

  T = 0.500s   Tail boom fully extended and locked (500mm extension)
               V-tail fins deployed and locked at V-angle
               Drone now has tail authority

  T = 0.600s   Wing root hinges release (retaining band slides off
               or pyrotechnic pin fires)
               Inner wing panels begin swinging outward

  T = 0.800s   Inner panels fully deployed, root detents locked
               Mid-span hinges release (delay detent overcome)
               Outer panels begin deploying

  T = 1.000s   Outer panels fully deployed and locked
               Full 2.2m wingspan achieved
               Drone has complete aerodynamic surfaces

  T = 1.100s   Motor starts, prop blades deploy under centrifugal force
               (10-inch folding prop, 2-blade)

  T = 1.300s   Prop at operating RPM, producing cruise thrust
               ArduPilot enters FBWA stabilization mode

  T = 1.500s   Drone pulls out of deployment dive
               GPS lock acquired, airspeed stabilized

  T = 2.000s   Full autonomous flight, transitions to AUTO mode
               Begins mission waypoint execution

  ALTITUDE BUDGET:
  ────────────────
  Ejection phase (0-0.2s):           ~1m (slow ejection velocity)
  Tail deployment dive (0.2-0.6s):   ~5m
  Wing deployment dive (0.6-1.0s):   ~15m (significant drag building)
  Powered pull-out (1.0-1.5s):       ~10-20m

  TOTAL ALTITUDE LOSS: 30-40m from ejection to level flight

  MINIMUM SAFE DEPLOYMENT ALTITUDE: 80m AGL
  (provides 40-50m margin for deployment delays and wind effects)
```

### Component Mass Budget (Variant B)

```
  MASS BUDGET: VARIANT B (MINI TUBE)
  ═══════════════════════════════════

  Component                  Mass (g)    Notes
  ─────────────────────────  ────────    ──────────────────────────
  Fuselage shell + bulkheads    450      Carbon fiber monocoque
  Nose cone                      40      3D-printed ASA
  Wing panels (4x: 2 inner      380      Foam core, carbon skin, 95g each
    + 2 outer)
  Wing spars (2x)               120      Carbon tube 8mm OD through hinges
  Wing root hinges (2x)          70      Al 6061 + steel pin + spring
  Wing mid-span hinges (2x)     40      Lighter version of root
  Wing retaining mechanism       25      Kevlar band + release
  Tail boom (telescoping)       110      3-stage carbon tube
  V-tail fins (2x)              60      Carbon/foam, 30g each
  V-tail hinges + springs        25      Leaf spring + detent
  Tail servos (2x 9g)           18      Micro servos for ruddervator
  Motor (2814 size)              65      Brushless outrunner, 900kv
  ESC (40A)                      35      BLHeli_32
  Propeller (10x5 folding)       18      Carbon-nylon folding prop
  Flight controller              25      Matek H743 Slim or equiv
  GPS + compass                  15      u-blox M10 + HMC5883
  IMU (onboard FC)                -      Included in FC
  Telemetry radio (900MHz)       15      SiK compatible or ELRS
  Receiver (ELRS 900MHz)          5      Long-range receiver
  Battery (4S 5000mAh)          520      Li-ion 18650 pack (higher energy)
  BEC + power distribution       30      5V + 12V regulated outputs
  Wiring + connectors            40      Silicone wire, JST, XT60
  Payload tray + interface       45      Scaled dovetail rail system
  Structural fasteners           25      M2/M3 hardware, adhesive
  ─────────────────────────  ────────
  SUBTOTAL (empty)             2241 g

  Payload (mission-specific)   1500 g   Camera gimbal, sensors, cargo
  ─────────────────────────  ────────
  TOTAL (loaded)               3741 g   Well within 6.5kg target

  Margin to 9.0 kg max:       5259 g    Available for:
                                        - Larger battery (longer endurance)
                                        - Heavier payload (up to ~5 kg)
                                        - Armor/hardening
                                        - Additional sensors

  ENDURANCE ESTIMATE:
  4S 5000mAh = 74 Wh
  Cruise power (2.2m span, 6.5 kg, ~18 m/s): ~50W
  Endurance: 74/50 = 1.48 hours (~89 minutes)

  With 4S 8000mAh (830g battery, total mass ~5.0 kg):
  118 Wh / 60W = 1.97 hours (~118 minutes)
```

---

## PALLET / MAGAZINE SYSTEM

### Tube Magazine for Variant A (Vertical Stack)

```
  MICRO DRONE MAGAZINE (Variant A, vertical stack)
  ════════════════════════════════════════════════

  Magazine holds N tubes in a vertical stack.
  Each tube: 124mm OD x 500mm length
  Inter-tube spacing: 10mm (structural divider + wiring)

  SINGLE MAGAZINE (12-tube):

  ┌──────────────────────────────────┐
  │  ┌────────────────────────────┐  │  Tube 1 (top, first to eject)
  │  │  ═══ DRONE (550g) ═══     │  │
  │  └────────────────────────────┘  │
  │  ┌────────────────────────────┐  │  Tube 2
  │  │  ═══ DRONE (550g) ═══     │  │
  │  └────────────────────────────┘  │
  │  ┌────────────────────────────┐  │  Tube 3
  │  │  ═══ DRONE (550g) ═══     │  │
  │  └────────────────────────────┘  │
  │            . . .                  │
  │  ┌────────────────────────────┐  │  Tube 12 (bottom, last to eject)
  │  │  ═══ DRONE (550g) ═══     │  │
  │  └────────────────────────────┘  │
  │  ┌────────────────────────────┐  │
  │  │  CONTROLLER + CO2 SUPPLY   │  │  Deployment controller, CO2 manifold
  │  └────────────────────────────┘  │
  └──────────────────────────────────┘

  MAGAZINE DIMENSIONS:
  Width:    140mm (tube OD + structure)
  Depth:    140mm (tube OD + structure)
  Height:   12 * (124 + 10) + 80 = 1688mm (magazine controller adds 80mm)
            Round up: 1700mm tall

  But this is impractical (1.7m tall stack). Better arrangement:

  MATRIX MAGAZINE (4x3 grid, horizontal tubes):

  ┌─────────────────────────────────────────┐
  │  ═══1═══  ═══2═══  ═══3═══  ═══4═══    │  Row 1
  │  ═══5═══  ═══6═══  ═══7═══  ═══8═══    │  Row 2
  │  ═══9═══  ═══10══  ═══11══  ═══12══    │  Row 3
  │  [  CONTROLLER  +  CO2 MANIFOLD     ]   │
  └─────────────────────────────────────────┘

  Tubes horizontal, exit facing same direction (one end of magazine).

  MAGAZINE DIMENSIONS (4x3 grid):
  Width:    4 * 134mm = 536mm
  Height:   3 * 134mm = 402mm
  Depth:    500mm (tube length) + 60mm (controller) = 560mm

  Total volume:   536 * 402 * 560 = 120,560 cm^3 = 0.121 m^3
  Total drone mass: 12 * 0.55 kg = 6.6 kg
  Magazine structure: ~2.5 kg (aluminum frame + CO2 + controller)
  Total magazine mass: ~9.1 kg

  PACKING DENSITY:  12 drones / 0.121 m^3 = 99 drones/m^3

  HEXAGONAL PACKING (more efficient):

  Hexagonal close-packing of 124mm tubes:

       ○ ○ ○ ○           Row 1: 4 tubes
        ○ ○ ○ ○          Row 2: 4 tubes (offset)
       ○ ○ ○ ○           Row 3: 4 tubes
        ○ ○ ○            Row 4: 3 tubes (short row)

  15 tubes in ~540mm x 480mm footprint
  Volume: 540 * 480 * 560 = 145,152 cm^3 = 0.145 m^3
  Packing density: 15 / 0.145 = 103 drones/m^3

  DEPLOYMENT RATE:
  ────────────────
  Pneumatic system can cycle valve in ~100ms.
  Minimum inter-drone spacing for safe deployment: 0.5 seconds
  (time for previous drone to clear blast zone + wing deploy area)

  Deployment rate: 2 drones/second (sequential from single manifold)
  Full magazine (12 drones): 6 seconds to deploy all

  With parallel manifolds (2x CO2 systems):
  Deployment rate: 4 drones/second (alternating rows)
  Full magazine: 3 seconds
```

### Pallet System for Variant B (Cargo Aircraft Deployment)

```
  PALLET SYSTEM (Variant B, C-130 / cargo aircraft)
  ═════════════════════════════════════════════════

  Based on standard 463L pallet (2235mm x 2743mm / 88" x 108")
  This is the standard US military air cargo pallet, fits C-130, C-17, etc.

  TUBE ARRANGEMENT ON 463L PALLET:

  Each tube: 200mm OD x 1200mm length
  Tube spacing: 220mm center-to-center (20mm structural gap)

  ┌──────────────────── 2235mm (pallet width) ──────────────────┐
  │                                                              │
  │  ═══1═══  ═══2═══  ═══3═══  ═══4═══  ═══5═══  ═══6═══     │  ▲
  │  ═══7═══  ═══8═══  ═══9═══  ═══10══  ═══11══  ═══12══     │  │
  │  ═══13══  ═══14══  ═══15══  ═══16══  ═══17══  ═══18══     │  2743mm
  │  ═══19══  ═══20══  ═══21══  ═══22══  ═══23══  ═══24══     │  │
  │  ═══25══  ═══26══  ═══27══  ═══28══  ═══29══  ═══30══     │  │
  │  ═══31══  ═══32══  ═══33══  ═══34══  ═══35══  ═══36══     │  ▼
  │                                                              │
  │  [ DEPLOYMENT CONTROLLER + PNEUMATICS + DROGUE CHUTE ]      │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  Columns: floor(2235 / 220) = 10 columns...

  Wait -- tubes are 1200mm long, oriented ACROSS the pallet width:

  Actually, let us orient tubes ALONG the pallet length (2743mm):
  - Tube length 1200mm fits once along 2743mm with ~1500mm remaining
    for controller + drogue system
  - Pallet width 2235mm / 220mm spacing = 10 tubes per row
  - Stack height limited by cargo bay (~2.4m for C-130 cargo floor to
    ceiling). Tubes 200mm OD + 20mm spacing = 220mm per layer.
    Layers: floor(2400 / 220) = 10 layers (theoretical)
    Practical limit with structure: 8 layers

  REVISED PALLET LAYOUT (side view):

  ┌────────────── 2743mm ──────────────────┐
  │  ┌── tubes (1200mm) ──┐ ┌─ ctrl ─┐    │
  │  │                     │ │        │    │
  │  │  10 tubes per row   │ │ drogue │    │  ▲
  │  │  8 rows high        │ │ chute  │    │  2400mm
  │  │  = 80 tubes         │ │ pneum. │    │  (cargo bay)
  │  │                     │ │ electr.│    │
  │  └─────────────────────┘ └────────┘    │  ▼
  └────────────────────────────────────────┘

  PALLET CAPACITY: 80 drones per 463L pallet

  But this is extremely ambitious. Practical numbers with structural
  reinforcement, access panels, and safety margins:

  CONSERVATIVE LAYOUT:
  - 6 tubes per row
  - 4 rows high
  - = 24 tubes per pallet

  ┌────────────────────────────────────────────────┐
  │  ╔══1══╗ ╔══2══╗ ╔══3══╗ ╔══4══╗ ╔══5══╗ ╔══6══╗  │  Layer 4
  │  ╔══7══╗ ╔══8══╗ ╔══9══╗ ╔10═══╗ ╔11═══╗ ╔12═══╗  │  Layer 3
  │  ╔13═══╗ ╔14═══╗ ╔15═══╗ ╔16═══╗ ╔17═══╗ ╔18═══╗  │  Layer 2
  │  ╔19═══╗ ╔20═══╗ ╔21═══╗ ╔22═══╗ ╔23═══╗ ╔24═══╗  │  Layer 1
  │  ═══════════════════════════════════════════════════  │
  │  [    PALLET BASE + DEPLOYMENT ELECTRONICS       ]  │
  └──────────────────────────────────────────────────────┘

  PALLET SPECIFICATIONS:
  ──────────────────────
  Drone mass:           6.5 kg each (mid-range)
  Drones per pallet:    24
  Drone mass total:     156 kg
  Pallet structure:     ~80 kg (aluminum frame, rails, pneumatics)
  Total pallet mass:    ~236 kg

  Pallet footprint:     2235 x 2743 mm = 6.13 m^2
  Pallet height:        4 * 220 + 100 (base) = 980mm (~1.0m)
  Pallet volume:        6.13 * 1.0 = 6.13 m^3

  PACKING DENSITY: 24 drones / 6.13 m^3 = 3.9 drones/m^3

  C-130 CAPACITY:
  C-130 cargo bay holds 6x 463L pallets.
  Total: 6 * 24 = 144 Variant B drones per C-130 sortie.
  Total drone mass: 144 * 6.5 = 936 kg (well within C-130 payload limit)

  DEPLOYMENT SEQUENCE (Rapid Dragon style):
  ──────────────────────────────────────────

  1. C-130 reaches deployment altitude (300-600m AGL) and speed
  2. Rear ramp opens
  3. Pallet rolls out on cargo rails (gravity + extraction chute)
  4. Drogue chute deploys to stabilize pallet descent
  5. At T+2s: pallet controller begins sequential tube ejection
  6. Tubes fire in a programmed sequence (2 per second, alternating sides)
  7. Each drone ejects nose-first from its tube
  8. Drones deploy wings at ~T+1.5s after individual ejection
  9. Drones establish autonomous flight
  10. Empty pallet descends under drogue chute, is expendable or recovered

  DEPLOYMENT RATE: 2 drones/second
  Full pallet (24 drones): 12 seconds
  Full C-130 load (6 pallets, deployed sequentially): ~90 seconds total
  144 drones airborne in under 2 minutes
```

### Packing Density Comparison

```
  PACKING DENSITY SUMMARY
  ═══════════════════════

  Configuration                      Drones/m^3    kg drones/m^3
  ─────────────────────────────────  ──────────    ──────────────
  Variant A: hex-packed magazine     103           56.7
  Variant A: rectangular magazine    99            54.5
  Variant B: pallet (conservative)   3.9           25.4
  Variant B: pallet (dense)          13.0          84.5

  For comparison:
  Sonobuoy (A-size) in standard      ~85           ~110
    aircraft dispenser
  PERDIX in flare dispenser          ~200          ~58
    (very small drone)
  Coyote in LOCUST launcher          ~12           ~71
```

---

## DEPLOYMENT SAFETY ANALYSIS

### What Happens If Deployment Fails

```
  FAILURE MODE AND EFFECTS ANALYSIS (FMEA)
  ════════════════════════════════════════

  FAILURE MODE 1: Wings fail to deploy (one or both sides)
  ────────────────────────────────────────────────────────
  Probability: Low (spring mechanisms are reliable, ~99.5% per wing)
  Combined probability of total failure: ~0.25%

  Effect: Drone enters uncontrolled spin/tumble
  Detection: ArduPilot detects abnormal attitude rates within 200ms
  Mitigation:
  - ArduPilot enters QLAND mode (if single wing) or MANUAL (kill motor)
  - Drone impacts ground as ballistic debris
  - Terminal velocity of 550g streamlined body: ~35 m/s
  - Kinetic energy at impact: 0.5 * 0.55 * 35^2 = 337 J
  - Equivalent to a cricket ball bowled at ~55 mph
  - Risk: moderate if deployed over populated areas

  Mitigation for populated areas:
  - Deploy only over water or uninhabited terrain
  - Ballistic parachute (adds 15g, deploys on deployment failure detect)

  FAILURE MODE 2: Motor fails to start
  ─────────────────────────────────────
  Probability: Low (~0.5%, ESC or motor fault)

  Effect: Wings deployed, drone glides unpowered
  Detection: ArduPilot detects zero RPM after throttle command
  Mitigation:
  - Drone enters best-glide configuration (ArduPilot FBWA)
  - Variant A (550g, L/D ~12): glide ratio allows ~12m forward per 1m lost
  - From 50m deployment altitude: ~600m glide range
  - ArduPilot guides to designated safe crash zone if programmed
  - Risk: low (unpowered glide is controlled descent)

  FAILURE MODE 3: Ejection failure (drone stuck in tube)
  ──────────────────────────────────────────────────────
  Probability: Very low (~0.1%, spring failure or tube jam)

  Effect: Drone remains in tube/magazine
  Detection: Deployment controller detects no ejection (tube cap intact
  or accelerometer on piston shows no movement)
  Mitigation:
  - Skip to next tube in sequence
  - Stuck drone is inert (motor not started, safe)
  - For pallet systems: stuck drone descends with pallet under drogue

  FAILURE MODE 4: Partial wing deployment (asymmetric)
  ────────────────────────────────────────────────────
  Probability: Low (~0.3%, one hinge jams)

  Effect: Drone rolls uncontrollably toward un-deployed wing
  Detection: ArduPilot detects sustained roll rate >300 deg/s
  Mitigation:
  - Motor kill commanded immediately
  - Ballistic descent (same as Failure Mode 1)
  - For Variant B: emergency parachute deployment (BRS-style)
    Parachute: 30g ripstop nylon, 0.8m diameter
    Descent rate: ~5 m/s (Variant B at 6.5 kg)
    Added mass: 50g (chute + mortar deployment tube)

  FAILURE MODE 5: GPS failure after deployment
  ─────────────────────────────────────────────
  Probability: Medium (~2%, especially if GPS antenna obscured during tumble)

  Effect: Drone flies but cannot navigate to waypoints
  Detection: ArduPilot GPS health flags
  Mitigation:
  - ArduPilot enters CIRCLE mode (loiter at current position using IMU)
  - Waits for GPS lock (typically 5-15 seconds from cold start)
  - If no GPS after 30 seconds: enter FBWA and fly pre-programmed heading
  - Dead-reckoning using IMU + airspeed until GPS acquired

  FAILURE MODE 6: Mid-span hinge fails to lock (Variant B)
  ────────────────────────────────────────────────────────
  Probability: Low (~0.5%, detent fails to engage)

  Effect: Outer wing panel flaps freely, creating asymmetric drag/lift
  Detection: Unusual vibration signature on IMU
  Mitigation:
  - Reduce airspeed (lower dynamic pressure on loose panel)
  - Fly modified mission at reduced performance
  - If uncontrollable: motor kill + parachute (Variant B)
```

### Freefall Parameters

```
  FREEFALL CALCULATIONS
  ═════════════════════

  VARIANT A (stowed, before wing deployment):
  Mass:                0.55 kg
  Stowed frontal area: 0.011 m^2 (pi * 0.055^2)
  Cd (cylinder):       0.82

  Terminal velocity = sqrt(2mg / (rho * Cd * A))
  = sqrt(2 * 0.55 * 9.81 / (1.225 * 0.82 * 0.011))
  = sqrt(10.79 / 0.011) = sqrt(981) = 31.3 m/s

  Freefall distance in 0.35s (wing deployment time):
  s = 0.5 * g * t^2 = 0.5 * 9.81 * 0.35^2 = 0.60 m
  (At low speed, well below terminal velocity, gravity dominates)

  Including ejection velocity (1.5 m/s downward):
  s = 1.5 * 0.35 + 0.5 * 9.81 * 0.35^2 = 0.525 + 0.601 = 1.13 m

  VARIANT B (stowed, before wing deployment):
  Mass:                6.5 kg
  Stowed frontal area: 0.025 m^2 (pi * 0.09^2, oval approximation)
  Cd (cylinder):       0.82

  Terminal velocity = sqrt(2 * 6.5 * 9.81 / (1.225 * 0.82 * 0.025))
  = sqrt(127.6 / 0.025) = sqrt(5104) = 71.4 m/s

  Freefall distance in 1.0s (wing deployment time):
  s = 2.5 * 1.0 + 0.5 * 9.81 * 1.0^2 = 2.5 + 4.9 = 7.4 m
  (2.5 m/s ejection velocity + gravity)

  Additional dive during powered pull-out (1.0-1.5s): ~10-15m
  Total altitude loss: ~20-25m (consistent with deployment sequence estimate)
```

---

## COMPARISON: TUBE FIXED-WING vs TILEABLE QUADCOPTER

```
  ╔══════════════════════╦════════════════════════╦═══════════════════════╗
  ║ Aspect               ║ Tube Fixed-Wing        ║ Tileable Quadcopter   ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Packing density      ║ ~100 drones/m^3        ║ ~150-300 drones/m^3   ║
  ║ (Variant A class)    ║ (cylindrical waste)    ║ (rectangular tiles)   ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Packing density      ║ ~4-13 drones/m^3       ║ ~8-20 drones/m^3      ║
  ║ (Variant B class)    ║ (large tube overhead)  ║ (folding arms help)   ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Endurance after      ║ MICRO: 20-25 min       ║ MICRO: 8-12 min       ║
  ║ deployment           ║ MINI: 60-120 min       ║ MINI: 20-35 min       ║
  ║                      ║ ★ CLEAR WINNER ★       ║                       ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Range after deploy   ║ MICRO: 5-15 km         ║ MICRO: 1-3 km         ║
  ║                      ║ MINI: 30-80 km         ║ MINI: 5-15 km         ║
  ║                      ║ ★ CLEAR WINNER ★       ║                       ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Speed                ║ MICRO: 10-20 m/s       ║ MICRO: 5-12 m/s       ║
  ║                      ║ MINI: 15-25 m/s        ║ MINI: 8-15 m/s        ║
  ║                      ║ ★ WINNER ★             ║                       ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Payload capacity     ║ MICRO: 50-200g         ║ MICRO: 20-80g         ║
  ║ (% of MTOW)         ║ MINI: 1.5-3.5 kg       ║ MINI: 0.5-1.5 kg      ║
  ║                      ║ (~25-40% of MTOW)      ║ (~15-25% of MTOW)     ║
  ║                      ║ ★ WINNER ★             ║                       ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Deployment           ║ HIGH                   ║ LOW                   ║
  ║ complexity           ║ Wing fold, tail deploy,║ Unfold arms, spin up  ║
  ║                      ║ prop deploy, pull-out  ║ motors, take off      ║
  ║                      ║ dive, 1-2s to flight   ║ 0.5-1s to hover       ║
  ║                      ║                        ║ ★ WINNER ★            ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Cost per unit        ║ MICRO: £50-200         ║ MICRO: £30-120        ║
  ║                      ║ MINI: £1000-4000       ║ MINI: £400-1500       ║
  ║                      ║ (folding mechanisms    ║ (simpler structure)   ║
  ║                      ║ add 20-40% cost)       ║ ★ WINNER ★            ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Wind resistance      ║ Good (15+ m/s)         ║ Moderate (10-12 m/s)  ║
  ║                      ║ Fixed wing handles     ║ Multirotor less       ║
  ║                      ║ wind well at speed     ║ efficient in wind     ║
  ║                      ║ ★ WINNER ★             ║                       ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Hover capability     ║ NO                     ║ YES                   ║
  ║                      ║ (must keep moving)     ║ ★ CLEAR WINNER ★      ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Deployment failure   ║ DANGEROUS              ║ MODERATE              ║
  ║ consequence          ║ Ballistic impact at    ║ Falls from hover      ║
  ║                      ║ 30+ m/s if wings fail  ║ height (~2m), minor   ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Air deployment       ║ EXCELLENT              ║ POOR                  ║
  ║ (from carrier a/c)   ║ Designed for tube      ║ Cannot deploy from    ║
  ║                      ║ ejection at speed      ║ moving aircraft       ║
  ║                      ║ ★ CLEAR WINNER ★       ║ easily                ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Ground deployment    ║ POOR                   ║ EXCELLENT             ║
  ║ (from ground base)   ║ Needs launch tube      ║ Just unfold and       ║
  ║                      ║ with ejection system   ║ take off vertically   ║
  ║                      ║                        ║ ★ CLEAR WINNER ★      ║
  ╠══════════════════════╬════════════════════════╬═══════════════════════╣
  ║ Stealth (acoustic)   ║ GOOD                   ║ POOR                  ║
  ║                      ║ Single slow prop       ║ 4 high-RPM props      ║
  ║                      ║ ★ WINNER ★             ║ loud at all speeds    ║
  ╚══════════════════════╩════════════════════════╩═══════════════════════╝

  SUMMARY VERDICT:

  Tube fixed-wing DOMINATES for:
  - Air-deployed operations (from carrier aircraft, C-130, etc.)
  - Long-range / long-endurance missions
  - High-speed transit to target area
  - Operations in windy conditions
  - Stealth requirements

  Tileable quadcopter DOMINATES for:
  - Ground-based deployment (parking lot, rooftop, vehicle)
  - Precision hover / station-keeping over a point
  - Low-complexity / low-cost swarm operations
  - Indoor or confined space operations
  - Situations where deployment failure risk must be minimized

  THEY ARE COMPLEMENTARY, NOT COMPETING:
  Use tube fixed-wing for area coverage, transit, and persistence.
  Use tileable quads for precision tasks, hover, and ground-based ops.
  Both can be controlled by the same mission engine and ground station.
```

---

## APPLICATIONS

### Variant A (MICRO Tube) Primary Use Cases

```
  USE CASES WHERE TUBE FORM FACTOR ADDS VALUE
  ════════════════════════════════════════════

  1. AIR-DEPLOYED ISR SWARM
     ─────────────────────
     Scenario: Maritime patrol aircraft (or MEDIUM/LARGE tier mothership)
     deploys 12-50 MICRO drones over a search area.

     Why tube: Carrier aircraft cannot stop to deploy drones. Tube
     ejection works at cruise speed. No aircraft modification needed
     if sonobuoy tubes are available (P-3, P-8 have 48-84 tubes).

     Mission: Distributed visual search over 10 km^2. Each drone flies
     a lawn-mower pattern in its assigned sector. Mesh network relays
     detections to carrier or ground station.

     Duration: 20 minutes per drone (single sortie, expendable).

  2. ELECTRONIC DECOY FIELD
     ─────────────────────
     Scenario: Deploy 20-50 RF-emitting drones to create false targets
     for enemy radar / EW systems.

     Why tube: Mass deployment speed (20 drones in 10 seconds).
     Drones disperse rapidly to create a distributed signature field.
     Each drone carries a small RF emitter that mimics the radar return
     or emissions of a larger platform.

     Duration: 15-25 minutes. Expendable after use.

  3. RAPID ENVIRONMENTAL MONITORING
     ──────────────────────────────
     Scenario: Chemical spill, wildfire, volcanic eruption. Deploy
     a network of atmospheric sensors across a hazard zone in minutes.

     Why tube: Can be deployed from a helicopter or fixed-wing aircraft
     flying UPWIND of the hazard. No need to enter the danger zone.
     Drones transit into hazard area under own power.

     Sensors: Gas (BME680), particulate (PM2.5), temperature, humidity.
     Data relayed via mesh network to incident commander.

  4. COMMUNICATIONS RELAY DEPLOYMENT
     ──────────────────────────────
     Scenario: Disaster area with no cellular/radio infrastructure.
     Deploy a line of 6-10 relay drones to bridge a 30-50 km gap.

     Why tube: Rapid deployment along a line. Aircraft flies the route
     and ejects one drone every 5 km. Each drone loiters at altitude,
     forming an ad-hoc relay chain (see 23-Mesh-Network-and-Directional-Comms.md).

     Endurance: 20 minutes per drone. Carrier aircraft can deploy
     replacement drones on return pass.

  5. NAVAL ASW SUPPORT (sonobuoy tube compatible)
     ─────────────────────────────────────────────
     Scenario: Fit into existing A-size sonobuoy tubes on patrol aircraft.
     Provide aerial ISR support over a sonobuoy barrier field.

     Why tube: Uses EXISTING infrastructure. No aircraft modification.
     P-8 Poseidon carries 120 sonobuoy tubes -- dedicate 12 to drones,
     108 to actual sonobuoys. Drones provide visual identification of
     contacts detected acoustically.
```

### Variant B (MINI Tube) Primary Use Cases

```
  1. PALLETIZED MASS ISR DEPLOYMENT
     ──────────────────────────────
     Scenario: C-130 deploys 144 camera-equipped drones over a
     200 km x 200 km search area (40,000 km^2).

     Why tube: Only way to deploy this many capable drones this quickly.
     Each drone covers ~280 km^2 in a 90-minute sortie (at 18 m/s,
     500m swath width). 144 drones cover the full area in one pass.

     Applications: Search and rescue (missing vessel, downed aircraft),
     maritime domain awareness, post-disaster damage assessment.

  2. LOGISTICS DELIVERY SWARM
     ────────────────────────
     Scenario: Deploy 24 cargo drones from a single C-130 pass.
     Each carries 1-3 kg of medical supplies, batteries, or ammunition
     to distributed recipients across a large area.

     Why tube: Rapid deployment from altitude. Each drone navigates
     autonomously to a different GPS destination. Covers 80+ km radius
     from deployment point. More efficient than helicopter delivery
     when recipients are widely dispersed.

  3. DISTRIBUTED SENSOR NETWORK (persistent)
     ──────────────────────────────────────
     Scenario: Deploy a persistent surveillance network over a border,
     coastline, or critical infrastructure corridor.

     Why tube: Rapid deployment of 24-144 drones that can loiter for
     60-120 minutes each. Rolling replacement: second aircraft deploys
     fresh wave as first wave reaches end of endurance.

     Sensors: EO camera, thermal, radar (mmWave).
     Each drone covers a 2-5 km section of the border.

  4. COUNTER-UAS RESPONSE FORCE
     ─────────────────────────
     Scenario: Enemy drone swarm detected. Deploy interceptor drones
     to engage. Each Variant B drone carries a net gun or RF jammer
     payload to neutralize small hostile drones.

     Why tube: Rapid response time. Pre-loaded pallets stored on alert.
     Aircraft can deploy 24 interceptors in 12 seconds.

     Advantage over ground-launched: Can deploy ahead of the threat,
     at altitude, intercepting from above.

  5. MINE COUNTERMEASURES (maritime)
     ──────────────────────────────
     Scenario: Clear a shipping channel by deploying drones with
     towed magnetometers or downward-looking EO cameras to map
     the seabed for mines.

     Why tube: Deploy rapidly over the entire channel width.
     Each drone flies a precise low-altitude pattern (10-20m AGL)
     over its assigned lane. Data fused at command ship.
```

---

## WING DEPLOYMENT MECHANISM COMPARISON

```
  DEPLOYMENT MECHANISM ANALYSIS
  ═════════════════════════════

  ┌──────────────────┬──────────┬───────────┬──────────────┬──────────────────┐
  │ Mechanism        │ Weight   │ Reliability│ Deploy Time  │ Failure Modes    │
  │                  │ (per wing│ (per      │              │                  │
  │                  │  hinge)  │  cycle)    │              │                  │
  ├──────────────────┼──────────┼───────────┼──────────────┼──────────────────┤
  │ Spring-loaded    │ 15-35g   │ 99.5%     │ 0.15-0.30s   │ Spring fatigue   │
  │ hinge with       │          │           │              │ (after ~10,000   │
  │ over-center      │          │           │              │ cycles, N/A for  │
  │ detent lock      │          │           │              │ single-use).     │
  │                  │          │           │              │ Detent may not   │
  │ (SELECTED for    │          │           │              │ engage if hinge  │
  │  both variants)  │          │           │              │ is dirty/icy.    │
  │                  │          │           │              │ Retaining band   │
  │                  │          │           │              │ may not release.  │
  ├──────────────────┼──────────┼───────────┼──────────────┼──────────────────┤
  │ Shape memory     │ 5-15g    │ 98%       │ 0.5-2.0s     │ Slow in cold     │
  │ alloy (SMA)      │          │           │              │ weather (SMA     │
  │ actuator         │          │           │              │ transition temp  │
  │                  │          │           │              │ is ~70C, needs   │
  │ (Nitinol wire    │          │           │              │ electrical       │
  │  contracts when  │          │           │              │ heating, draws   │
  │  heated, pulls   │          │           │              │ 2-5A). Battery   │
  │  wing open)      │          │           │              │ must power       │
  │                  │          │           │              │ heating during   │
  │                  │          │           │              │ deployment.      │
  │                  │          │           │              │ Inconsistent     │
  │                  │          │           │              │ force output.    │
  ├──────────────────┼──────────┼───────────┼──────────────┼──────────────────┤
  │ Pneumatic (CO2   │ 40-80g   │ 99%       │ 0.05-0.15s   │ CO2 pressure     │
  │ cartridge drives │ (shared  │           │              │ varies with      │
  │ piston that      │ system)  │           │              │ temperature.     │
  │ pushes wings     │          │           │              │ Seals may leak   │
  │ open)            │          │           │              │ over storage.    │
  │                  │          │           │              │ Overpressure can │
  │                  │          │           │              │ damage wing.     │
  │                  │          │           │              │ Single-shot (no  │
  │                  │          │           │              │ retry possible). │
  ├──────────────────┼──────────┼───────────┼──────────────┼──────────────────┤
  │ Elastic band     │ 3-8g     │ 97%       │ 0.10-0.25s   │ Rubber degrades  │
  │ stored energy    │          │           │              │ with UV, heat,   │
  │ (rubber band     │          │           │              │ and age. Force   │
  │ under tension    │          │           │              │ output decreases │
  │ pulls wing to    │          │           │              │ over storage     │
  │ deployed         │          │           │              │ time. May not    │
  │ position)        │          │           │              │ have enough      │
  │                  │          │           │              │ force in cold    │
  │                  │          │           │              │ conditions.      │
  │                  │          │           │              │ Lightest option  │
  │                  │          │           │              │ for expendable   │
  │                  │          │           │              │ drones.          │
  └──────────────────┴──────────┴───────────┴──────────────┴──────────────────┘

  RECOMMENDATION:

  Variant A (MICRO, expendable, single-use):
  PRIMARY:  Spring-loaded hinge (proven, reliable, reasonable weight)
  FALLBACK: Elastic band (lightest, acceptable for expendable units)

  Variant B (MINI, recoverable, multi-mission):
  PRIMARY:  Spring-loaded hinge with over-center detent (reusable,
            wings can be re-folded for re-packing)
  FALLBACK: Pneumatic (fastest deployment, use for time-critical missions)

  SMA is NOT recommended for either variant:
  - Too slow (0.5-2.0s deployment time wastes altitude)
  - Temperature-dependent (unreliable at altitude where temp is low)
  - Requires electrical power during deployment (battery risk)
  - Lower reliability than mechanical springs

  Pneumatic is VIABLE but adds system complexity:
  - Best used when tube ejection already has a CO2 system (shared gas)
  - Fastest deployment time (50-150ms)
  - Best for Variant B where the CO2 manifold already exists for ejection
```

---

## STRUCTURAL DESIGN NOTES

### Ejection Loads

```
  STRUCTURAL LOAD CASES
  ═════════════════════

  LOAD CASE 1: EJECTION (axial acceleration)

  Variant A:
  - Spring ejection: 3-5 g axial (gentle)
  - Pneumatic ejection: 8-12 g axial (for ground launch)
  - Design to: 15 g axial (with 1.5x safety factor)
  - Critical components: battery retention, avionics mounting,
    wing fold mechanism must not release prematurely

  Variant B:
  - Pneumatic ejection: 3-9 g axial
  - Design to: 15 g axial (with 1.5x safety factor)
  - Critical path: fuselage shell compression (solved -- 32x margin),
    battery strap, payload dovetail retention latch,
    telescoping boom must not extend prematurely (retention pin)

  LOAD CASE 2: WING DEPLOYMENT (transient bending)

  When wings snap open, the sudden stop at the detent lock creates
  an impulse load on the hinge and spar root.

  Variant A:
  - Wing panel mass: 30g (one side)
  - Deployment angular velocity at lock: ~10 rad/s
  - Kinetic energy: 0.5 * 0.03 * (0.175)^2 * 100 = 0.046 J
    (where 0.175m is CG distance of panel from hinge)
  - Impact force at detent: ~20-40 N (absorbed by detent spring)
  - Spar root bending moment: ~7 N-m
  - Carbon tube spar (8mm OD): yield moment = ~15 N-m
  - Safety factor: 2.1x -- acceptable

  Variant B:
  - Inner wing panel mass: 95g
  - Deployment angular velocity: ~8 rad/s
  - Hinge impact force: ~60-100 N
  - Spar root bending moment: ~25 N-m
  - Carbon tube spar (8mm OD): yield moment = ~15 N-m -- INSUFFICIENT
  - Solution: larger spar (12mm OD, 10mm ID) at root
    Yield moment: ~35 N-m, safety factor: 1.4x
  - Or: damped hinge (viscous damper reduces impact) -- adds 10g but
    reduces impulse by 3x

  LOAD CASE 3: FLIGHT (steady-state and gust)

  Standard wing bending loads. For Variant B at 6.5 kg, 2.2m span:
  - Wing loading: ~22 g/dm^2
  - Design load factor: +4g / -2g (typical for small UAV)
  - Root bending moment at 4g: ~32 N-m
  - With 12mm spar: 35 N-m yield -- safety factor 1.1x (marginal)
  - Solution: spar web reinforcement at root, or 14mm spar
    14mm OD spar: yield moment = ~55 N-m, safety factor 1.7x

  LOAD CASE 4: PALLET EXTRACTION (lateral + vertical)

  For Variant B on 463L pallet:
  - Pallet extraction creates ~3g longitudinal deceleration
  - Drogue chute oscillation: +/- 15 degrees = ~1g lateral
  - Tubes must retain drones under combined 3g axial + 1g lateral
  - Retention: drone held by tube piston (rear) and nose cap (front)
    Both rated to 15g -- adequate margin
```

### Material Selection

```
  MATERIALS FOR TUBE-PACKAGED DRONE
  ══════════════════════════════════

  FUSELAGE:
  ├── Variant A: 3D-printed PA12 nylon (selective laser sintering)
  │   or wound carbon fiber tube (38mm ID, 0.5mm wall)
  │   Nylon chosen for cost at volume (<£5 per unit in batches of 100+)
  │   Carbon tube for performance variant
  │
  └── Variant B: Wet-layup carbon fiber monocoque
      2-layer spread-tow carbon (0.5mm total wall)
      Laid up on a male mold, vacuum-bagged, oven-cured
      Cost: ~£30-60 per fuselage in small batches

  WINGS:
  ├── Variant A: EPP (expanded polypropylene) foam core, 4mm thick
  │   Unidirectional carbon cap strip on upper and lower surface
  │   Total panel thickness: 5mm including skin
  │   Impact resistant (EPP does not shatter)
  │   Cost: ~£3 per wing panel
  │
  └── Variant B: Rohacell or Airex foam core, 6mm thick
      2-layer carbon fiber skin (0.2mm per layer, top and bottom)
      Total panel thickness: 7mm
      8mm carbon tube spar at root, 6mm at mid-span
      Cost: ~£15 per wing panel

  HINGES:
  ├── Aluminum 6061-T6 hinge plates (CNC machined or laser-cut)
  ├── 4mm stainless steel hinge pins (hardened 440C)
  ├── Music wire torsion springs (0.8mm or 1.0mm wire diameter)
  └── Cost: ~£2-5 per hinge assembly (CNC machined in batch)

  TAIL:
  ├── Variant A: 1mm carbon fiber sheet (waterjet or laser cut)
  │   Leaf spring at root (integral with fin)
  │
  └── Variant B: Foam core + carbon skin (same construction as wings)
      Servos: 9g digital micro servos (Emax ES08MD or equivalent)

  TUBE (launch canister):
  ├── Variant A: Filament-wound fiberglass or aluminum 6061 tube
  │   124mm OD, 3mm wall, 500mm length
  │   Fiberglass: ~80g per tube
  │   Aluminum: ~120g per tube
  │
  └── Variant B: Aluminum 6061-T6 drawn tube or carbon fiber wound
      200mm OD, 5mm wall, 1200mm length
      Aluminum: ~850g per tube
      Carbon fiber: ~500g per tube (2x cost)
```

---

## INTEGRATION WITH PLATFORM FAMILY

```
  HOW TUBE VARIANTS FIT INTO THE MULTI-SCALE FAMILY
  ═════════════════════════════════════════════════

  The tube variants are NOT separate platforms. They are ALTERNATE
  AIRFRAME CONFIGURATIONS of existing tiers:

  Variant A (MICRO Tube) = Tier 1 MICRO in tube packaging
  Variant B (MINI Tube)  = Tier 2 MINI in tube packaging

  ┌─────────────────────────────────────────────────────────┐
  │                   PLATFORM FAMILY                       │
  │                                                         │
  │  Tier 1: MICRO                                          │
  │  ├── Standard config (hand-launch, open airframe)       │
  │  └── ★ TUBE config (Variant A, sonobuoy-sized) ★       │
  │                                                         │
  │  Tier 2: MINI                                           │
  │  ├── Standard config (Skywalker X8, hand/bungee launch) │
  │  └── ★ TUBE config (Variant B, torpedo-tube-sized) ★    │
  │                                                         │
  │  Tier 3: MEDIUM                                         │
  │  └── Standard config only (too large for practical tube)│
  │                                                         │
  │  Tier 4: LARGE                                          │
  │  └── Standard config only                               │
  └─────────────────────────────────────────────────────────┘

  SHARED COMPONENTS:
  ├── Flight controller: same FC hardware, same ArduPilot firmware
  ├── Mission engine: identical software (same goal-to-waypoint pipeline)
  ├── Payload interface: electrically identical (scaled mechanically)
  ├── Ground station: same QGroundControl + custom mission planning
  ├── Communication: same protocols (MAVLink, mesh networking)
  └── Swarm coordination: same algorithms regardless of form factor

  TUBE-SPECIFIC ADDITIONS TO ARDUPILOT:
  ├── DEPLOY_SEQUENCE parameter set (timing for wing/tail/motor)
  ├── TUBE_LAUNCH mode (handles deployment state machine)
  ├── Emergency response for deployment failure detection
  └── Pre-loaded parameter file per tube variant
      (Variant A: MICRO_TUBE.param, Variant B: MINI_TUBE.param)
```

---

## DEVELOPMENT ROADMAP

```
  TUBE VARIANT DEVELOPMENT SEQUENCE
  ═════════════════════════════════

  These are LATER developments, after the standard configurations fly.

  PHASE 2A (2027): Variant A Prototype
  ├── Design and 3D-print Variant A fuselage
  ├── Develop spring-loaded wing hinge mechanism
  ├── Build and test single tube + ejection system
  ├── Flight test deployment sequence (ground-based tube launch)
  ├── Iterate on deployment timing and reliability
  └── Target: 10 successful deployments from tube at ground level

  PHASE 2B (2027-2028): Variant A Swarm
  ├── Build 8-12 Variant A units
  ├── Develop magazine system (4x3 matrix)
  ├── Test swarm deployment from vehicle-mounted magazine
  ├── Integrate with mesh networking (ESP-NOW or similar)
  └── Target: 12-drone swarm deployed in <10 seconds

  PHASE 3A (2028): Variant B Prototype
  ├── Design double-fold wing mechanism (CNC aluminum hinges)
  ├── Build telescoping tail boom
  ├── Develop pneumatic ejection system
  ├── Flight test deployment from ground-based tube
  └── Target: reliable 2.2m wing deployment from 200mm tube

  PHASE 3B (2028-2029): Variant B Pallet System
  ├── Build 4-tube pallet demonstrator
  ├── Test deployment from high altitude (balloon drop initially)
  ├── Integrate with standard payload interface
  └── Target: 4-drone palletized deployment from 200m altitude

  COST TARGETS:
  ├── Variant A unit cost: £80-150 (in batches of 50+)
  ├── Variant A tube: £20-40
  ├── Variant A magazine (12-tube): £300-500
  ├── Variant B unit cost: £800-2500 (in batches of 10+)
  ├── Variant B tube: £50-100
  └── Variant B pallet (24-tube): £2000-4000
```

---

## SUMMARY TABLE

```
  ╔════════════════════════╦══════════════════════╦══════════════════════╗
  ║ Parameter              ║ VARIANT A            ║ VARIANT B            ║
  ║                        ║ (MICRO Tube)         ║ (MINI Tube)          ║
  ╠════════════════════════╬══════════════════════╬══════════════════════╣
  ║ Tube diameter          ║ 124 mm (sonobuoy)    ║ 200 mm               ║
  ║ Tube length            ║ 500 mm               ║ 1200 mm              ║
  ║ Deployed wingspan      ║ 700 mm               ║ 2200 mm              ║
  ║ Mass (loaded)          ║ 550 g                ║ 3.7-6.5 kg           ║
  ║ Payload capacity       ║ 50-200 g             ║ 1.5-3.5 kg           ║
  ║ Endurance              ║ 20-25 min            ║ 60-120 min           ║
  ║ Range                  ║ 5-15 km              ║ 30-80 km             ║
  ║ Cruise speed           ║ 12-18 m/s            ║ 15-25 m/s            ║
  ║ Wing fold type         ║ Backward fold        ║ Double-fold          ║
  ║ Tail type              ║ Cruciform pop-out    ║ V-tail on boom       ║
  ║ Ejection method        ║ Spring (air) /       ║ Pneumatic (CO2)      ║
  ║                        ║ Pneumatic (ground)   ║                      ║
  ║ Deploy time to flight  ║ 1.0 s                ║ 2.0 s                ║
  ║ Altitude loss (deploy) ║ 15-25 m              ║ 30-40 m              ║
  ║ Min deploy altitude    ║ 50 m AGL             ║ 80 m AGL             ║
  ║ Packing density        ║ ~100 drones/m^3      ║ ~4-13 drones/m^3     ║
  ║ Magazine capacity      ║ 12-15 per magazine   ║ 24 per 463L pallet   ║
  ║ Unit cost target       ║ £80-150              ║ £800-2500            ║
  ║ Expendable?            ║ Yes                  ║ Recoverable          ║
  ║ Sonobuoy compatible?   ║ YES (A-size)         ║ No                   ║
  ╚════════════════════════╩══════════════════════╩══════════════════════╝
```
