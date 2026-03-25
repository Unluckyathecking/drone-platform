# Ground Station Hardware Architecture

## Three-Tier Ground Station Design for Multipurpose Drone Platform Family

This document specifies the complete ground station hardware architecture across
three deployment scales: portable field kit, vehicle-mounted mobile station, and
fixed automated airbase. Each tier supports the platform family (MICRO 500g through
LARGE 100-200kg) as defined in document 22.

All tiers share the same software stack: QGroundControl or Mission Planner running
ArduPilot MAVLink v2 protocol, with the custom mission engine (document 07) layered
on top for autonomous goal-based operations.

```
  GROUND STATION TIER OVERVIEW
  ============================

  TIER 1               TIER 2                  TIER 3
  Portable Field Kit   Vehicle-Mounted         Automated Airbase
  (Backpack/Pelican)   (Land Rover/Van)        (Fixed Installation)

  ┌──────────┐         ┌──────────────┐        ┌────────────────────┐
  │ 1 operator│         │ 2-3 operators │        │ 0-2 operators      │
  │ 1 drone   │         │ 2-5 drones    │        │ 10-50 drones       │
  │ MINI tier │         │ MINI-MEDIUM   │        │ ALL tiers          │
  │ 30km range│         │ 80km range    │        │ 200+ km range      │
  │ 2hr ops   │         │ 8-12hr ops    │        │ 24/7 continuous    │
  │ £500-800  │         │ £8,000-15,000 │        │ £150,000-500,000   │
  └──────────┘         └──────────────┘        └────────────────────┘
       │                      │                         │
       └──────────────────────┴─────────────────────────┘
                    Same MAVLink protocol
                    Same mission engine software
                    Same ArduPilot parameter system
```

---

## TIER 1: PORTABLE FIELD KIT (Backpack / Pelican Case)

### Mission Profile

Single-operator deployment of one MINI-tier drone (2-4m wingspan, 5-15kg MTOW).
Typical missions: survey, ISR, search and rescue, cargo delivery demo. Duration
2-3 hours including setup and teardown. Deployable anywhere on foot, by bicycle,
or from a vehicle.

### System Architecture

```
  TIER 1 SYSTEM BLOCK DIAGRAM
  ============================

  ┌─────────────────────────────────────────────────────────────────┐
  │  DRONE (MINI TIER)                                              │
  │  ┌──────────┐  ┌──────────────┐  ┌─────────────┐              │
  │  │ Pixhawk  │──│ RFD900x      │──│ 5.8GHz VTX  │              │
  │  │ Cube     │  │ Telemetry TX │  │ 600mW       │              │
  │  │ Orange+  │  │ 915/433 MHz  │  │ Video TX    │              │
  │  └──────────┘  └──────┬───────┘  └──────┬──────┘              │
  │                        │                  │                     │
  └────────────────────────┼──────────────────┼─────────────────────┘
                           │ 915/433 MHz      │ 5.8 GHz
                           │ MAVLink          │ Analog/Digital Video
                           │ (bidirectional)  │ (downlink only)
                           │                  │
  ┌────────────────────────┼──────────────────┼─────────────────────┐
  │  GROUND STATION        │                  │                     │
  │                        ▼                  ▼                     │
  │  ┌──────────────┐  ┌──────────┐  ┌─────────────┐              │
  │  │ RC TX        │  │ RFD900x  │  │ 5.8GHz VRX  │              │
  │  │ RadioMaster  │  │ Ground   │  │ Receiver    │              │
  │  │ Boxer        │  │ Module   │  │ + DVR       │              │
  │  │ (safety      │  │          │  │             │              │
  │  │  override)   │  └────┬─────┘  └──────┬──────┘              │
  │  └──────────────┘       │               │                      │
  │         │               │   USB         │  HDMI/USB            │
  │         │  ┌────────────┴───────────────┴──────┐               │
  │         │  │                                    │               │
  │  ELRS   │  │  LAPTOP / TABLET                   │               │
  │  915MHz │  │  ┌─────────────────────────────┐   │               │
  │         │  │  │ QGroundControl              │   │               │
  │         │  │  │ + Mission Engine            │   │               │
  │         │  │  │ + Video Display (picture    │   │               │
  │         │  │  │   in-picture or second      │   │               │
  │         │  │  │   window)                   │   │               │
  │         │  │  └─────────────────────────────┘   │               │
  │         │  │                                    │               │
  │         │  └────────────────────────────────────┘               │
  │         │                                                       │
  │  ┌──────┴────────┐  ┌──────────┐  ┌──────────────────┐        │
  │  │ Antenna       │  │ Power    │  │ Weather Station  │        │
  │  │ Tracker Mount │  │ Battery  │  │ (portable        │        │
  │  │ (optional -   │  │ 12V 20Ah│  │  anemometer)     │        │
  │  │  hill-climb   │  │ LiFePO4 │  │                  │        │
  │  │  project)     │  │          │  │                  │        │
  │  └───────────────┘  └──────────┘  └──────────────────┘        │
  └─────────────────────────────────────────────────────────────────┘
```

### Hardware Bill of Materials

```
  TIER 1 — COMPLETE BOM
  ═════════════════════

  ┌────┬───────────────────────────────────┬──────────────┬────────┐
  │ #  │ Component                         │ Specification│ Cost   │
  │    │                                   │              │ (GBP)  │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ COMPUTE                           │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 1  │ Laptop (refurbished ThinkPad      │ i5/Ryzen 5   │ £150   │
  │    │ T480/T490 or similar)             │ 16GB RAM     │        │
  │    │                                   │ 256GB SSD    │        │
  │    │ OR: Samsung Galaxy Tab S6 Lite    │ 1080p screen │ £200   │
  │    │ with USB-C hub                    │ min 5hr batt │        │
  │    │                                   │              │        │
  │    │ RECOMMENDATION: Laptop preferred  │              │        │
  │    │ for full QGC + video processing.  │              │        │
  │    │ Tablet for ultra-light deployments│              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ TELEMETRY                         │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 2  │ RFD900x telemetry radio (ground)  │ 1W, 900MHz   │ £90    │
  │    │                                   │ FHSS         │        │
  │    │                                   │ 40+ km LOS   │        │
  │    │                                   │ USB interface │        │
  │    │                                   │              │        │
  │    │ ALTERNATIVE (budget): SiK 433MHz  │ 100mW        │ £25    │
  │    │ telemetry pair (mRo or Holybro)   │ 5-10 km LOS  │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 3  │ Ground antenna for telemetry      │ 5dBi dipole  │ £15    │
  │    │ (RFD900x or SiK)                 │ SMA connector│        │
  │    │                                   │ omnidirec.   │        │
  │    │ UPGRADE: 8dBi Yagi for extended   │ directional  │ £30    │
  │    │ range (requires manual or tracker │ 30+ km       │        │
  │    │ pointing)                         │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ VIDEO                             │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 4  │ 5.8GHz video receiver             │              │        │
  │    │ Option A: Eachine ROTG02          │ OTG USB to   │ £20    │
  │    │ (connects directly to Android/PC) │ phone/tablet │        │
  │    │                                   │              │        │
  │    │ Option B: ImmersionRC rapidFIRE   │ Module for   │ £65    │
  │    │ (fits in goggles or monitor)      │ Fat Shark    │        │
  │    │                                   │              │        │
  │    │ Option C: HDZero VRX              │ Digital HD   │ £90    │
  │    │ (digital video system)            │ 720p/90fps   │        │
  │    │                                   │              │        │
  │    │ RECOMMENDATION: Start with analog │              │        │
  │    │ (Eachine ROTG02) — cheapest,      │              │        │
  │    │ proven, low latency. Upgrade to   │              │        │
  │    │ digital later.                    │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 5  │ 5.8GHz patch antenna (RX)        │ 8dBi         │ £10    │
  │    │                                   │ directional  │        │
  │    │                                   │ RP-SMA       │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ RC CONTROL (SAFETY OVERRIDE)      │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 6  │ RadioMaster Boxer                 │ ELRS 915MHz  │ £110   │
  │    │                                   │ 16ch         │        │
  │    │                                   │ EdgeTX       │        │
  │    │                                   │ 250mW ELRS   │        │
  │    │                                   │ built-in     │        │
  │    │                                   │              │        │
  │    │ BUDGET ALT: RadioMaster Zorro     │ ELRS         │ £75    │
  │    │                                   │              │        │
  │    │ PURPOSE: Manual override only.    │              │        │
  │    │ Normal ops are fully autonomous.  │              │        │
  │    │ RC is the safety kill switch.     │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ ANTENNA TRACKER (OPTIONAL)        │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 7  │ Pan-tilt antenna tracker          │ 2-axis       │ £40    │
  │    │ (from hill-climbing project,      │ servo gimbal │        │
  │    │  doc 23)                          │ Arduino Nano │        │
  │    │                                   │ RSSI-based   │        │
  │    │ BOM: 2x MG996R servo (£8),       │ tracking     │        │
  │    │ Arduino Nano (£5), 3D-printed    │              │        │
  │    │ bracket (£2), wiring (£5),       │              │        │
  │    │ SMA cables (£5), Yagi antenna    │              │        │
  │    │ (£15)                             │              │        │
  │    │                                   │              │        │
  │    │ Reads MAVLink GPS position from   │              │        │
  │    │ QGC to calculate initial bearing, │              │        │
  │    │ then hill-climb refines pointing. │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ POWER                             │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 8  │ 12V 20Ah LiFePO4 battery         │ 240Wh        │ £45    │
  │    │ (Talentcell or similar)           │ ~2kg         │        │
  │    │                                   │ Powers radio │        │
  │    │                                   │ + tracker    │        │
  │    │                                   │ 8-12hr       │        │
  │    │                                   │ runtime      │        │
  │    │                                   │              │        │
  │    │ ALTERNATIVE: 2x 18650 USB power   │ 100Wh total  │ £25    │
  │    │ banks (Anker 20,000mAh each)     │ lighter      │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 9  │ 12V distribution board            │ Anderson     │ £10    │
  │    │ (fused, 3 outputs)               │ powerpole    │        │
  │    │                                   │ connectors   │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ WEATHER                           │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 10 │ Portable anemometer               │ Bluetooth    │ £20    │
  │    │ (Vaavud or WeatherFlow)          │ wind speed   │        │
  │    │                                   │ + direction  │        │
  │    │                                   │ + temp       │        │
  │    │ BUDGET ALT: Handheld wind meter   │ No Bluetooth │ £8     │
  │    │ (Proster digital)                │ manual read  │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ CARRYING CASE                     │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 11 │ Pelican 1510 (carry-on size)      │ 559x351x229  │ £120   │
  │    │ with custom foam insert           │ mm internal  │        │
  │    │                                   │ IP67 rated   │        │
  │    │                                   │ wheels +     │        │
  │    │                                   │ handle       │        │
  │    │                                   │              │        │
  │    │ BUDGET ALT: Apache 4800           │ Similar size │ £45    │
  │    │ (Harbour Freight equivalent,      │ less durable │        │
  │    │  available in UK via Amazon)      │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │    │ CABLES AND ACCESSORIES            │              │        │
  ├────┼───────────────────────────────────┼──────────────┼────────┤
  │ 12 │ USB cables (USB-A to micro,       │ 3x cables    │ £10    │
  │    │ USB-C, SMA extension)            │ 30cm + 1m   │        │
  │ 13 │ SMA patch cables (2x 30cm)       │ RG316        │ £8     │
  │ 14 │ Tripod (lightweight aluminium)    │ 1.5m height  │ £15    │
  │    │ for antenna mounting              │ 1kg weight   │        │
  │ 15 │ Sunshade for laptop/tablet        │ Collapsible  │ £10    │
  │    │                                   │ hood         │        │
  │ 16 │ Laminated checklist card          │ Pre-flight   │ £2     │
  │    │                                   │ procedures   │        │
  └────┴───────────────────────────────────┴──────────────┴────────┘

  COST SUMMARY (TIER 1)
  ═════════════════════

  BUDGET BUILD (SiK telemetry, analog video, budget case):
  ┌─────────────────────────────────┬────────┐
  │ Refurbished laptop              │ £150   │
  │ SiK 433MHz telemetry pair       │ £25    │
  │ Dipole antenna                  │ £15    │
  │ Eachine ROTG02 video RX         │ £20    │
  │ 5.8GHz patch antenna            │ £10    │
  │ RadioMaster Zorro               │ £75    │
  │ USB power banks (2x)            │ £25    │
  │ Handheld wind meter             │ £8     │
  │ Apache 4800 case                │ £45    │
  │ Cables + tripod + accessories   │ £45    │
  ├─────────────────────────────────┼────────┤
  │ TOTAL (BUDGET)                  │ £418   │
  └─────────────────────────────────┴────────┘

  RECOMMENDED BUILD (RFD900x, analog video, Pelican case, tracker):
  ┌─────────────────────────────────┬────────┐
  │ Refurbished laptop              │ £150   │
  │ RFD900x telemetry radio         │ £90    │
  │ 5dBi dipole + 8dBi Yagi        │ £45    │
  │ Eachine ROTG02 video RX         │ £20    │
  │ 5.8GHz patch antenna            │ £10    │
  │ RadioMaster Boxer               │ £110   │
  │ Antenna tracker (DIY)           │ £40    │
  │ 12V 20Ah LiFePO4 battery       │ £45    │
  │ 12V distribution board          │ £10    │
  │ Bluetooth anemometer            │ £20    │
  │ Pelican 1510 case               │ £120   │
  │ Cables + tripod + accessories   │ £45    │
  ├─────────────────────────────────┼────────┤
  │ TOTAL (RECOMMENDED)             │ £705   │
  └─────────────────────────────────┴────────┘

  TOTAL WEIGHT (RECOMMENDED BUILD):  ~6.5 kg
  ├── Case (empty)                    2.7 kg
  ├── Laptop                          1.5 kg
  ├── Battery                         2.0 kg
  ├── Radios + antennas               0.5 kg
  ├── RC transmitter                  0.5 kg
  ├── Cables + misc                   0.3 kg
  └── Antenna tracker                 0.4 kg
      (tripod carried separately:     1.0 kg)
```

### Pelican Case Layout (Top-Down View)

```
  PELICAN 1510 INTERIOR — CUSTOM FOAM LAYOUT
  ═══════════════════════════════════════════
  559mm x 351mm x 229mm (interior)

  TOP LAYER (lid — 50mm deep):
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  ┌─────────────────────────────────────────────────┐   │
  │  │        LID ORGANISER (mesh pocket)               │   │
  │  │                                                   │   │
  │  │  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │   │
  │  │  │ USB      │  │ SMA      │  │ Laminated     │  │   │
  │  │  │ cables   │  │ cables   │  │ checklists +  │  │   │
  │  │  │ (3x)     │  │ (2x)     │  │ frequencies   │  │   │
  │  │  └──────────┘  └──────────┘  └───────────────┘  │   │
  │  │                                                   │   │
  │  │  ┌──────────────┐  ┌────────────────────────┐    │   │
  │  │  │ Sunshade     │  │ Wind meter + spare     │    │   │
  │  │  │ (folded)     │  │ props/zip ties/tape    │    │   │
  │  │  └──────────────┘  └────────────────────────┘    │   │
  │  └─────────────────────────────────────────────────┘   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘

  BOTTOM LAYER (pick-and-pluck foam — 179mm deep):
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  ┌──────────────────────┐  ┌─────────────────────────┐ │
  │  │                      │  │                         │ │
  │  │     LAPTOP           │  │    12V LiFePO4          │ │
  │  │     (in sleeve)      │  │    Battery              │ │
  │  │                      │  │    + Distribution       │ │
  │  │     350x250x25mm     │  │      Board              │ │
  │  │                      │  │                         │ │
  │  │                      │  │    150x100x80mm         │ │
  │  ├──────────────────────┤  │                         │ │
  │  │                      │  ├─────────────────────────┤ │
  │  │  ┌────────┐ ┌──────┐│  │  ┌───────┐ ┌─────────┐ │ │
  │  │  │RFD900x │ │Video ││  │  │5dBi   │ │ 8dBi    │ │ │
  │  │  │Ground  │ │RX    ││  │  │Dipole │ │ Yagi    │ │ │
  │  │  │Module  │ │      ││  │  │Antenna│ │ (disasm)│ │ │
  │  │  │80x40x  │ │50x30 ││  │  │       │ │         │ │ │
  │  │  │20mm    │ │x20mm ││  │  │250mm  │ │ 300mm   │ │ │
  │  │  └────────┘ └──────┘│  │  └───────┘ └─────────┘ │ │
  │  │                      │  │                         │ │
  │  │  ┌──────────────────┐│  │  ┌─────────────────┐   │ │
  │  │  │ RadioMaster      ││  │  │ Antenna Tracker │   │ │
  │  │  │ Boxer            ││  │  │ (disassembled)  │   │ │
  │  │  │ (in foam cradle) ││  │  │ servos + bracket│   │ │
  │  │  │                  ││  │  │ + Arduino       │   │ │
  │  │  │ 200x150x80mm    ││  │  │                 │   │ │
  │  │  └──────────────────┘│  │  └─────────────────┘   │ │
  │  └──────────────────────┘  └─────────────────────────┘ │
  │                                                         │
  └─────────────────────────────────────────────────────────┘

  TRIPOD: Carried externally (strapped to case handle or
          in separate bag).
```

### Field Deployment Procedure

```
  SETUP TIME: ~5 minutes

  1. Open case, remove laptop and power battery
  2. Extend tripod, mount antenna tracker (or just clamp Yagi)
  3. Connect RFD900x ground radio to laptop via USB
  4. Connect video RX to laptop via USB
  5. Connect antenna(s) via SMA cables
  6. Power on battery → distribution board → radio + tracker
  7. Boot laptop → launch QGroundControl
  8. Power on RC transmitter → verify ELRS link
  9. Read wind meter → enter conditions in QGC
  10. Verify MAVLink telemetry from drone
  11. Mission is go

  TEARDOWN TIME: ~5 minutes (reverse order)
```

---

## TIER 2: VEHICLE-MOUNTED MOBILE STATION (Land Rover / Van)

### Mission Profile

Multi-drone operations with 2-3 operators. Supports MINI and MEDIUM tier drones
simultaneously. Missions lasting 8-12 hours. Extended communication range via
mast-mounted directional antennas. Operates as a forward command post for
multi-drone survey, search and rescue, or security patrol operations.

Suitable vehicles: Land Rover Defender (110), Ford Transit Custom, Mercedes
Sprinter, Toyota Land Cruiser (for rough terrain).

### System Architecture

```
  TIER 2 SYSTEM BLOCK DIAGRAM
  ============================

                        ┌──── TELESCOPING MAST (5-10m) ────┐
                        │                                    │
                        │  ┌──────────┐  ┌──────────────┐   │
                        │  │ Weather  │  │ High-gain    │   │
                        │  │ Station  │  │ Directional  │   │
                        │  │ (Davis   │  │ Antennas:    │   │
                        │  │  Vantage │  │              │   │
                        │  │  Vue)    │  │  ┌────────┐  │   │
                        │  │          │  │  │900MHz  │  │   │
                        │  └──────┬───┘  │  │12dBi   │  │   │
                        │         │      │  │Yagi    │  │   │
                        │         │      │  └────────┘  │   │
                        │         │      │  ┌────────┐  │   │
                        │         │      │  │5.8GHz  │  │   │
                        │         │      │  │14dBi   │  │   │
                        │         │      │  │Patch   │  │   │
                        │         │      │  │Array   │  │   │
                        │         │      │  └────────┘  │   │
                        │         │      │              │   │
                        │         │      │  ON ROTATOR: │   │
                        │         │      │  Yaesu G-450C│   │
                        │         │      │  or DIY      │   │
                        │         │      │  (stepper    │   │
                        │         │      │   motor +    │   │
                        │         │      │   belt drive)│   │
                        │         │      └──────┬───────┘   │
                        │         │             │           │
                        └─────────┼─────────────┼───────────┘
                                  │             │
                    ──────────────┼─────────────┼───────────── Vehicle Roof
                                  │             │
  ┌───────────────────────────────┼─────────────┼──────────────────────────┐
  │  VEHICLE INTERIOR             │             │                          │
  │                               │             │                          │
  │  ┌────────────────────────────┼─────────────┼───────────────────────┐  │
  │  │  COMMUNICATIONS RACK       │ coax        │ coax                  │  │
  │  │                            │             │                       │  │
  │  │  ┌───────────────┐  ┌─────┴──────┐  ┌──┴──────────┐            │  │
  │  │  │ 4G/5G Modem   │  │ Weather    │  │ Antenna     │            │  │
  │  │  │ (Cradlepoint  │  │ Display    │  │ Controller  │            │  │
  │  │  │  or Sierra    │  │ Unit       │  │ (rotator +  │            │  │
  │  │  │  Wireless)    │  │            │  │  tracker    │            │  │
  │  │  │               │  │            │  │  software)  │            │  │
  │  │  │ + external    │  │            │  │             │            │  │
  │  │  │   MIMO ant.   │  │            │  │ MAVLink GPS │            │  │
  │  │  └───────┬───────┘  └────────────┘  │ auto-point  │            │  │
  │  │          │ Ethernet                  └──────┬──────┘            │  │
  │  │          │                                  │ USB/Serial        │  │
  │  │  ┌───────┴──────────────────────────────────┴──────────────┐   │  │
  │  │  │  NETWORK SWITCH (Netgear GS108 or similar — 8-port)    │   │  │
  │  │  └───┬──────────┬──────────┬──────────┬────────────────────┘   │  │
  │  │      │          │          │          │                        │  │
  │  │      │          │          │          │                        │  │
  │  └──────┼──────────┼──────────┼──────────┼────────────────────────┘  │
  │         │          │          │          │                            │
  │  ┌──────┴────┐ ┌───┴─────┐ ┌─┴───────┐ │                            │
  │  │WORKSTATION│ │ VIDEO   │ │ DRONE   │ │                            │
  │  │ #1       │ │ SERVER  │ │ TELEMETRY│ │                            │
  │  │(Primary) │ │         │ │ HUB     │ │                            │
  │  │          │ │ Multi-  │ │         │ │                            │
  │  │ i7/Ryzen │ │ channel │ │ 3x     │ │                            │
  │  │ 7, 32GB │ │ VRX:   │ │ RFD900x │ │                            │
  │  │ dual     │ │         │ │ radios  │ │                            │
  │  │ monitor  │ │ 4x 5.8 │ │ (one per│ │                            │
  │  │          │ │ GHz RX  │ │ drone)  │ │                            │
  │  │ Runs:    │ │ modules │ │         │ │                            │
  │  │ QGC +    │ │ + HDMI  │ │ Each on │ │                            │
  │  │ Mission  │ │ capture │ │ unique  │ │                            │
  │  │ Engine   │ │ cards   │ │ NetID   │ │                            │
  │  │          │ │         │ │         │ │                            │
  │  └──────────┘ └─────────┘ └─────────┘ │                            │
  │                                        │                            │
  │  ┌─────────────────────────────────────┴──────────────────────┐    │
  │  │  POWER SYSTEM                                               │    │
  │  │                                                             │    │
  │  │  ┌──────────────┐  ┌───────────────┐  ┌────────────────┐   │    │
  │  │  │ Vehicle      │  │ 2kW Inverter  │  │ Auxiliary      │   │    │
  │  │  │ Alternator   │──│ (pure sine)   │──│ 12V 100Ah     │   │    │
  │  │  │ (engine on)  │  │               │  │ LiFePO4       │   │    │
  │  │  │              │  │ For AC equip  │  │ (engine off)  │   │    │
  │  │  └──────────────┘  └───────────────┘  └────────────────┘   │    │
  │  │                                                             │    │
  │  │  Backup: Honda EU22i generator (2.2kW) for extended ops    │    │
  │  └─────────────────────────────────────────────────────────────┘    │
  │                                                                      │
  │  ┌──────────────────────────────────────────────────────────────┐   │
  │  │  TEAM COMMS                                                   │   │
  │  │                                                               │   │
  │  │  ┌───────────────┐  ┌──────────────────────────────────────┐ │   │
  │  │  │ Baofeng UV-5R │  │ PMR446 handhelds (Motorola T82)     │ │   │
  │  │  │ (VHF/UHF      │  │ for operator-to-observer comms      │ │   │
  │  │  │  amateur radio │  │ (licence-free in UK)                │ │   │
  │  │  │  for base      │  │                                     │ │   │
  │  │  │  to HQ link)  │  │ 3x handhelds included               │ │   │
  │  │  └───────────────┘  └──────────────────────────────────────┘ │   │
  │  └──────────────────────────────────────────────────────────────┘   │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
```

### Vehicle Layout (Top-Down View)

```
  LAND ROVER DEFENDER 110 — TOP-DOWN LAYOUT
  ═════════════════════════════════════════
  (approximately 4.7m long x 1.8m wide)

                         FRONT
                    ┌─────────────┐
                    │   ENGINE    │
                    │             │
                    ├─────────────┤
                    │  DRIVER  │OP│  OP = Operator 1 (front passenger)
                    │          │ 1│  Can operate RC override from here
                    ├──────────┼──┤
                    │          │  │
                    │  OP 2    │OP│  OP 2 = Primary pilot/mission commander
                    │  (work-  │ 3│  OP 3 = Video/payload operator
                    │  station)│  │
                    │  ┌────┐  │  │
                    │  │Mon │  │  │  Monitors fold down for transit
                    │  │x2  │  │  │
                    │  └────┘  │  │
  ┌─────────────────┤          │  ├─────────────────┐
  │ SIDE ACCESS DOOR│  ┌────┐  │  │ SIDE ACCESS DOOR│
  │                 │  │Rack│  │  │                 │
  │                 │  │(19"│  │  │                 │
  │                 │  │ 6U)│  │  │                 │
  └─────────────────┤  └────┘  │  ├─────────────────┘
                    │          │  │
                    ├──────────┴──┤
                    │             │
                    │  CARGO /    │  Drone storage (2-3 MINI or 1 MEDIUM)
                    │  DRONE      │  Battery charging station
                    │  STORAGE    │  Spare parts bin
                    │             │  Launch rail (removable, slides out)
                    │  ┌───────┐  │
                    │  │Drones │  │
                    │  │(wing  │  │
                    │  │removed│  │
                    │  │stacked│  │
                    │  └───────┘  │
                    │             │
                    │  ┌───────┐  │
                    │  │Generator │
                    │  │(Honda   │  Mounts on slide-out tray at rear
                    │  │ EU22i)  │
                    │  └───────┘  │
                    │             │
                    └──────┬──────┘
                           │
                       REAR DOOR
                    (drops down as
                     work surface)
```

### Vehicle Layout (Side View)

```
  LAND ROVER DEFENDER 110 — SIDE VIEW
  ═══════════════════════════════════

                    TELESCOPING MAST
                    (Clark Masts QT-9
                     or Will-Burt equivalent)
                         │
                    5-10m │ extended
                    ┌────┐│
                    │Ant.│┤ ◄── Directional antennas
                    │    │┤     + weather station
                    └────┘│     on rotator
                         │
                    1.2m │ stowed
                         │
  ┌────────┬─────────────┼──────────┬───────────┐
  │        │ ████████████│██████████│           │
  │  CAB   │  OPERATOR   │  DRONE   │           │
  │        │  STATION    │  STORAGE │ GENERATOR │
  │        │  (seated)   │          │ (rear     │
  │   ●    │             │          │  slide-   │
  │  wheel │    ●        │     ●    │  out)     │
  └────────┴─────────────┴──────────┴───────────┘

  ROOF MOUNTED:
  ├── Mast base plate (bolted to roof rack)
  ├── 4G/5G MIMO antenna (shark fin)
  ├── GPS timing antenna (for network sync)
  └── Solar panel (optional, 100W flexible)

  ROOF RACK: Aluminium expedition rack
  (carries mast, solar panel, extra antenna cases)
```

### Antenna Mast Detail

```
  MAST DETAIL — CLARK MASTS QT-9 (or equivalent)
  ══════════════════════════════════════════════

  Extended:                         Stowed:

       ┌──┐ ◄ Weather station           Mast sections
       │WX│   (wind, temp, pressure)     telescope into
       └──┘                              base tube
        │
       ┌──┐ ◄ 900 MHz Yagi (12dBi)     ┌────────────┐
       │Y │   for telemetry             │            │
       └──┘   on Yaesu G-450C rotator   │  1.2m      │
        │                                │  stowed    │
       ┌──┐ ◄ 5.8 GHz patch array      │  height    │
       │PA│   (14dBi) for video         │            │
       └──┘                              │  ~15 kg    │
        │     ◄ 2.4 GHz omni (backup)   │  total     │
       (│)                               │            │
        │                                └────────────┘
        │
        │     10m height = line-of-sight
        │     to ~12 km (earth curvature)
        │
        │     + drone at 200m altitude:
        │     LOS to ~80 km
        │
  ──────┴────── Vehicle roof ──────────

  GUY WIRES: 3x at 120-degree spacing
  (staked to ground when mast extended above 5m)

  ROTATOR SPEC:
  ├── Yaesu G-450C: 450-degree rotation
  │   10 sec/revolution, 200 kg-cm torque
  │   £350 new, £150 used (ham radio market)
  │
  └── DIY ALTERNATIVE: NEMA 23 stepper motor
      + GT2 belt + 3D-printed housing
      Controlled by Arduino + MAVLink GPS data
      Cost: £40-60
```

### Hardware Bill of Materials

```
  TIER 2 — COMPLETE BOM
  ═════════════════════

  ┌────┬─────────────────────────────────┬────────────────┬────────┐
  │ #  │ Component                       │ Specification  │ Cost   │
  │    │                                 │                │ (GBP)  │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ COMPUTE                         │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 1  │ Workstation PC                  │ i7/Ryzen 7     │ £600   │
  │    │ (mini ITX or small form factor) │ 32GB RAM       │        │
  │    │                                 │ 512GB NVMe     │        │
  │    │                                 │ GPU (for video │        │
  │    │                                 │ decode + maps) │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 2  │ Monitors (2x portable 15.6")   │ 1080p IPS      │ £200   │
  │    │ USB-C powered                   │ fold-flat      │        │
  │    │                                 │ anti-glare     │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 3  │ Third monitor (optional)        │ 7" HDMI        │ £50    │
  │    │ dedicated video feed display    │ touch panel    │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ TELEMETRY                       │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 4  │ RFD900x radios (3x ground)     │ 1W each        │ £270   │
  │    │ (one per drone, unique NetID)   │ USB interface  │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 5  │ 900 MHz 12dBi Yagi antenna     │ Directional    │ £45    │
  │    │ (mast-mounted, on rotator)      │ 30-degree beam │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 6  │ 900 MHz 5dBi omni antenna      │ Backup/close   │ £15    │
  │    │ (vehicle-mounted)               │ range          │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ VIDEO                           │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 7  │ Video receivers (4x)            │ 5.8GHz         │ £80    │
  │    │ (Eachine ROTG02 or TBS Fusion)  │ diversity      │        │
  │    │                                 │ USB capture    │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 8  │ 5.8GHz 14dBi patch array       │ Mast-mounted   │ £35    │
  │    │ antenna                         │ on rotator     │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 9  │ HDMI capture cards (4x)        │ USB 3.0        │ £60    │
  │    │ (for multi-feed recording)      │ 1080p30        │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ RC CONTROL                      │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 10 │ RadioMaster Boxer (2x)         │ ELRS 915MHz    │ £220   │
  │    │ (one per active drone)          │ safety override│        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ ANTENNA SYSTEM                  │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 11 │ Telescoping mast                │ 10m extended   │ £800   │
  │    │ (Clark Masts QT-9 or equiv.)   │ 1.2m stowed   │        │
  │    │                                 │ pneumatic or   │        │
  │    │ BUDGET ALT: manual aluminium    │ manual crank   │ £150   │
  │    │ push-up mast (6m)              │               │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 12 │ Antenna rotator                 │ 360+ degrees   │ £350   │
  │    │ (Yaesu G-450C)                 │ auto-tracking  │        │
  │    │                                 │               │        │
  │    │ BUDGET ALT: DIY stepper rotator │ Arduino-based  │ £50    │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 13 │ Antenna rotator controller      │ Interfaces     │ £30    │
  │    │ (Arduino Mega + custom PCB)     │ with QGC       │        │
  │    │                                 │ MAVLink GPS    │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ NETWORKING                      │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 14 │ 4G/5G modem                    │ Dual SIM       │ £200   │
  │    │ (Sierra Wireless or Cradlepoint)│ external MIMO  │        │
  │    │                                 │ antenna        │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 15 │ Gigabit network switch          │ 8-port         │ £20    │
  │    │                                 │ unmanaged      │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 16 │ 4G/5G MIMO antenna (roof)      │ Shark fin      │ £45    │
  │    │                                 │ style          │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ POWER                           │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 17 │ 2kW pure sine inverter          │ 12V DC → 230V  │ £180   │
  │    │ (Victron Phoenix or Renogy)     │ AC             │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 18 │ Auxiliary 12V 100Ah LiFePO4    │ 1.28kWh        │ £350   │
  │    │ battery (engine-off operation)  │ ~12kg          │        │
  │    │                                 │ 4-6hr runtime  │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 19 │ DC-DC battery charger           │ Charges aux    │ £80    │
  │    │ (Sterling B2B or Renogy)        │ from alternator│        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 20 │ Honda EU22i generator           │ 2.2kW          │ £900   │
  │    │ (for extended ops, quiet)       │ inverter       │        │
  │    │                                 │ 4-8hr on 3.6L │        │
  │    │ BUDGET ALT: Skip generator,     │               │        │
  │    │ rely on vehicle + aux battery   │               │ £0     │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ WEATHER                         │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 21 │ Weather station                 │ Wind, temp,    │ £250   │
  │    │ (Davis Vantage Vue or equiv.)  │ pressure,      │        │
  │    │ Mast-mounted                    │ humidity       │        │
  │    │                                 │ USB data feed  │        │
  │    │ BUDGET ALT: Kestrel 3000       │ Handheld       │ £80    │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ TEAM COMMS                      │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 22 │ PMR446 handhelds (3x)          │ Motorola T82   │ £60    │
  │    │ (licence-free UK)              │ or Binatone    │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 23 │ VHF/UHF mobile radio           │ Baofeng UV-5R  │ £25    │
  │    │ (for base-to-HQ if amateur     │ or Icom IC-7300│        │
  │    │  licence held)                 │ (amateur)      │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ DRONE SUPPORT                   │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 24 │ Battery charger (ISDT Q8 Max)  │ 8-channel      │ £100   │
  │    │ for drone LiPo batteries        │ balance charge │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 25 │ Drone storage racks             │ Fits 3x MINI   │ £40    │
  │    │ (aluminium, custom)             │ wings removed  │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 26 │ Bungee launch rail              │ 3m aluminium   │ £60    │
  │    │ (removable, stored on roof rack)│ + surgical tube │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │    │ INSTALLATION                    │                │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 27 │ 19" rack (6U open frame)       │ Wall-mounted   │ £60    │
  │    │                                 │ in vehicle     │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 28 │ Cable management + connectors   │ Anderson, SMA  │ £50    │
  │    │ (fuses, distribution, labelling)│ N-type, USB   │        │
  ├────┼─────────────────────────────────┼────────────────┼────────┤
  │ 29 │ Roof rack + mast mount plate   │ Aluminium      │ £200   │
  │    │                                 │ expedition rack│        │
  └────┴─────────────────────────────────┴────────────────┴────────┘

  COST SUMMARY (TIER 2)
  ═════════════════════

  BUDGET BUILD (manual mast, DIY rotator, no generator):
  ┌─────────────────────────────────┬────────┐
  │ Workstation PC (refurbished)    │ £400   │
  │ Monitors (2x portable)         │ £200   │
  │ Telemetry (3x RFD900x)         │ £270   │
  │ Antennas (Yagi + omni + patch) │ £95    │
  │ Video (4x RX + capture)        │ £140   │
  │ RC transmitters (2x Boxer)     │ £220   │
  │ Manual mast (6m push-up)       │ £150   │
  │ DIY rotator                    │ £50    │
  │ 4G/5G modem + antenna          │ £245   │
  │ Network switch                 │ £20    │
  │ Power (inverter + aux battery) │ £530   │
  │ DC-DC charger                  │ £80    │
  │ Weather (Kestrel 3000)         │ £80    │
  │ PMR446 radios (3x)            │ £60    │
  │ Drone support (charger etc)    │ £200   │
  │ Installation (rack, cables)    │ £310   │
  ├─────────────────────────────────┼────────┤
  │ TOTAL (BUDGET)                  │ £3,050 │
  └─────────────────────────────────┴────────┘

  NOTE: Does not include vehicle cost. Assumes existing
  Land Rover or van.

  FULL SPEC BUILD (pneumatic mast, Yaesu rotator, generator):
  ┌─────────────────────────────────┬────────┐
  │ Workstation PC (new)            │ £600   │
  │ Monitors (2x + 1x video)       │ £250   │
  │ Telemetry (3x RFD900x)         │ £270   │
  │ Antennas (full set)            │ £95    │
  │ Video (4x RX + capture)        │ £140   │
  │ RC transmitters (2x Boxer)     │ £220   │
  │ Clark Masts QT-9 (10m)        │ £800   │
  │ Yaesu G-450C rotator           │ £350   │
  │ Rotator controller             │ £30    │
  │ 4G/5G modem + antenna          │ £245   │
  │ Network switch                 │ £20    │
  │ Power (inverter + aux battery) │ £530   │
  │ DC-DC charger                  │ £80    │
  │ Honda EU22i generator          │ £900   │
  │ Weather (Davis Vantage Vue)    │ £250   │
  │ PMR446 + VHF radio            │ £85    │
  │ Drone support (charger etc)    │ £200   │
  │ Installation (rack, cables,    │ £310   │
  │  roof rack)                    │        │
  ├─────────────────────────────────┼────────┤
  │ TOTAL (FULL SPEC)               │ £5,375 │
  └─────────────────────────────────┴────────┘

  TOTAL WEIGHT (installed in vehicle): ~80 kg
  (excluding vehicle, generator, and drones)
```

---

## TIER 3: AUTOMATED AIRBASE (Fixed Installation)

### Mission Profile

Autonomous 24/7 drone operations. Zero or minimal human presence. Capable of
launching, recovering, recharging, reloading, and re-launching drones without
manual intervention. Supports all platform tiers. Target: 10-50 drones, 50+
missions per day.

Reference systems studied:
- Zipline P1/P2 distribution hubs (Rwanda, Ghana, USA)
- Wing (Google/Alphabet) delivery hubs (Australia, USA)
- Amazon Prime Air MK30 fulfilment hubs
- Insitu ScanEagle STUAS (military: catapult launch, Skyhook recovery)
- Aerovel Flexrotor (automated ship-based ops)

### Site Overview

```
  TIER 3 — AUTOMATED AIRBASE SITE PLAN (TOP-DOWN)
  ═══════════════════════════════════════════════
  Scale: 1 character = approximately 2 metres

  N
  ↑
  │
  │         ┌─── PERIMETER FENCE (2.4m chain-link + barbed wire) ───┐
  │         │                                                         │
  │         │   WIND SOCK                                             │
  │         │     ○                                                   │
  │         │                                                         │
  │  ───────┤   ════════════════════════════                          │
  │         │   ║  LAUNCH ZONE            ║     60m x 10m            │
  │         │   ║                          ║     Clear of obstacles   │
  │         │   ║  ┌──────────────────┐   ║                          │
  │         │   ║  │ CATAPULT RAIL    │   ║     20m rail             │
  │         │   ║  │ (pneumatic)      │   ║     oriented into        │
  │         │   ║  │ ═══════════════► │   ║     prevailing wind      │
  │  W ─────┤   ║  └──────────────────┘   ║     (rotatable on        │ ──── E
  │         │   ║                          ║      turntable for       │
  │         │   ════════════════════════════     variable winds)      │
  │         │                                                         │
  │         │                    20m gap                               │
  │         │                   (safety)                              │
  │         │                                                         │
  │         │   ════════════════════════════                          │
  │         │   ║  RECOVERY ZONE          ║     40m x 20m            │
  │         │   ║                          ║                          │
  │         │   ║   ┌────┐     ┌────┐     ║     Option A: Net        │
  │         │   ║   │NET │     │NET │     ║     (2 vertical poles    │
  │         │   ║   │POLE│     │POLE│     ║      + suspended net)    │
  │         │   ║   │ 8m │     │ 8m │     ║                          │
  │         │   ║   └──┬─┘     └──┬─┘     ║     Option B: Arresting │
  │         │   ║      └────╥─────┘       ║     wire (Zipline-style) │
  │         │   ║           ║ NET         ║                          │
  │         │   ║           ║ 10m wide    ║     Option C: Precision  │
  │         │   ║           ║ 6m high     ║     belly landing strip  │
  │         │   ║                          ║     (smooth surface,     │
  │         │   ════════════════════════════     GPS-RTK guided)      │
  │         │                                                         │
  │         │            TAXIWAY                                      │
  │         │   ─────────────────────────────                         │
  │         │                                                         │
  │         │   ┌────────────────────────────────────────────────┐   │
  │         │   │                                                │   │
  │         │   │              MAIN BUILDING                      │   │
  │         │   │              (12m x 8m, steel frame)           │   │
  │         │   │                                                │   │
  │         │   │  ┌──────────────────┐  ┌──────────────────┐   │   │
  │         │   │  │                  │  │                  │   │   │
  │         │   │  │  DRONE HANGAR    │  │  OPERATIONS      │   │   │
  │         │   │  │  (6m x 8m)      │  │  CENTRE          │   │   │
  │         │   │  │                  │  │  (6m x 8m)      │   │   │
  │         │   │  │  ┌──┐ ┌──┐ ┌──┐ │  │                  │   │   │
  │         │   │  │  │D1│ │D2│ │D3│ │  │  Servers         │   │   │
  │         │   │  │  └──┘ └──┘ └──┘ │  │  Monitors        │   │   │
  │         │   │  │  ┌──┐ ┌──┐ ┌──┐ │  │  Radio rack      │   │   │
  │         │   │  │  │D4│ │D5│ │D6│ │  │  UPS             │   │   │
  │         │   │  │  └──┘ └──┘ └──┘ │  │  Battery charger │   │   │
  │         │   │  │  ┌──┐ ┌──┐ ┌──┐ │  │  array           │   │   │
  │         │   │  │  │D7│ │D8│ │D9│ │  │                  │   │   │
  │         │   │  │  └──┘ └──┘ └──┘ │  │  Network equip   │   │   │
  │         │   │  │                  │  │  4G/5G + SATCOM  │   │   │
  │         │   │  │  ROBOTIC ARM     │  │                  │   │   │
  │         │   │  │  (battery swap   │  │  Weather display │   │   │
  │         │   │  │   + payload)     │  │                  │   │   │
  │         │   │  │                  │  │                  │   │   │
  │         │   │  │  BATTERY         │  │                  │   │   │
  │         │   │  │  CAROUSEL        │  │                  │   │   │
  │         │   │  │  (20 slots)      │  │                  │   │   │
  │         │   │  │                  │  │                  │   │   │
  │         │   │  └──────────────────┘  └──────────────────┘   │   │
  │         │   │                                                │   │
  │         │   └──────────────────────────┬─────────────────────┘   │
  │         │                              │                         │
  │         │                              │ LOADING BAY             │
  │         │                              │ (drone enters from      │
  │         │                              │  taxiway via motorised  │
  │         │                              │  conveyor)              │
  │         │                                                         │
  │         │   ┌──────────────┐  ┌──────────────┐                   │
  │         │   │ SOLAR ARRAY  │  │ SOLAR ARRAY  │                   │
  │         │   │ (5kW)        │  │ (5kW)        │                   │
  │         │   │ 12 panels    │  │ 12 panels    │                   │
  │         │   │ ground mount │  │ ground mount │                   │
  │         │   └──────────────┘  └──────────────┘                   │
  │         │                                                         │
  │         │   ┌──────────────────────────────────┐                 │
  │         │   │  POWER BUILDING (3m x 3m)        │                 │
  │         │   │  ├── Grid connection (if avail)  │                 │
  │         │   │  ├── Battery bank (48V 200Ah     │                 │
  │         │   │  │   LiFePO4 — 10kWh)            │                 │
  │         │   │  ├── Inverter/charger (Victron)  │                 │
  │         │   │  ├── Backup generator (diesel     │                 │
  │         │   │  │   7kW auto-start)              │                 │
  │         │   │  └── Solar charge controller     │                 │
  │         │   └──────────────────────────────────┘                 │
  │         │                                                         │
  │         │   CCTV cameras: 4x at corners, 2x at launch/recovery  │
  │         │   PIR motion sensors on perimeter                      │
  │         │   LED runway/approach lighting (solar-powered)         │
  │         │                                                         │
  │         │   GATE ═══                                              │
  │         │   (vehicle access, card reader)                        │
  │         │                                                         │
  │         └─────────────────────────────────────────────────────────┘
  │
  S

  OVERALL SITE DIMENSIONS: approximately 120m x 80m (0.96 hectares)
  SAFETY EXCLUSION ZONE: 50m beyond perimeter fence (public access restricted)
```

### A) LAUNCH SYSTEM

```
  LAUNCH SYSTEM DESIGN
  ════════════════════

  PRIMARY: PNEUMATIC CATAPULT (for fixed-wing MINI and MEDIUM tiers)
  ─────────────────────────────────────────────────────────────────

  Reference: Zipline P1 pneumatic catapult, Insitu ScanEagle launcher

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  PNEUMATIC CATAPULT — SIDE VIEW                       │
  │                                                        │
  │              Drone on                                  │
  │              launch cradle                             │
  │                  ┌──┐                                  │
  │                  │██│ ◄── Drone (wing-locked)          │
  │                  └┬─┘                                  │
  │         ┌────────┴────────────────────────────┐       │
  │         │  RAIL (aluminium V-track)            │       │
  │         │  20m long, 15-degree incline         │       │
  │         │                                      │       │
  │     ════╪══════════════════════════════════╪═══╪═══►   │
  │         │                                  │   │       │
  │     ┌───┘                                  └───┘       │
  │     │                                          │       │
  │  ┌──┴──┐                                    ┌──┴──┐   │
  │  │PYLON│                                    │PYLON│   │
  │  │ 2m  │                                    │ 0.5m│   │
  │  │     │                                    │     │   │
  │  └──┬──┘                                    └──┬──┘   │
  │     │                                          │       │
  │  ═══╧══════════════════════════════════════════╧═══   │
  │     GROUND                                            │
  │                                                        │
  │  PNEUMATIC SYSTEM:                                     │
  │  ┌─────────────┐    ┌──────────────┐                   │
  │  │ Air         │    │ Launch       │                   │
  │  │ Compressor  │────│ Accumulator  │                   │
  │  │ (electric)  │    │ (200L tank)  │                   │
  │  │ 3kW        │    │ 10 bar       │                   │
  │  └─────────────┘    └──────┬───────┘                   │
  │                            │ pneumatic                  │
  │                            │ piston                     │
  │                            ▼                            │
  │                     ┌──────────────┐                   │
  │                     │ Launch piston│                   │
  │                     │ (inside rail)│                   │
  │                     │ 300mm bore   │                   │
  │                     │ 2m stroke    │                   │
  │                     └──────────────┘                   │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  ACCELERATION PROFILE BY TIER:
  ┌──────────┬─────────┬──────────┬──────────┬──────────────────────┐
  │ Tier     │ MTOW    │ Launch   │ Accel.   │ Force Required       │
  │          │         │ Speed    │ (over    │ (F = ma)             │
  │          │         │ (Vs x    │ 20m rail)│                      │
  │          │         │ 1.3)     │          │                      │
  ├──────────┼─────────┼──────────┼──────────┼──────────────────────┤
  │ MICRO    │ 0.5 kg  │ 10 m/s  │ 2.5 m/s² │ 1.25 N (hand-launch  │
  │          │         │         │          │ or tube — no catapult │
  │          │         │         │          │ needed)               │
  ├──────────┼─────────┼──────────┼──────────┼──────────────────────┤
  │ MINI     │ 10 kg   │ 15 m/s  │ 5.6 m/s² │ 56 N                 │
  │          │         │         │          │ (bungee can do this — │
  │          │         │         │          │ catapult is overkill  │
  │          │         │         │          │ but enables auto-     │
  │          │         │         │          │ mated launch)         │
  ├──────────┼─────────┼──────────┼──────────┼──────────────────────┤
  │ MEDIUM   │ 40 kg   │ 22 m/s  │ 12.1m/s² │ 484 N                │
  │          │         │         │          │ Pneumatic catapult    │
  │          │         │         │          │ sized for this        │
  ├──────────┼─────────┼──────────┼──────────┼──────────────────────┤
  │ LARGE    │ 150 kg  │ 28 m/s  │ 19.6m/s² │ 2,940 N              │
  │          │         │         │          │ Requires heavy-duty   │
  │          │         │         │          │ pneumatic or electro- │
  │          │         │         │          │ magnetic catapult,    │
  │          │         │         │          │ OR short runway       │
  │          │         │         │          │ (50-100m)             │
  └──────────┴─────────┴──────────┴──────────┴──────────────────────┘

  Note: Acceleration = v²/(2d), where v = launch speed, d = rail length.
  Force = mass x acceleration. Peak G-load on drone:
    MINI:  0.57g — gentle, well within structural limits
    MEDIUM: 1.23g — moderate, standard catapult territory
    LARGE:  2.0g — significant, requires reinforced airframe

  CATAPULT SPECIFICATIONS:
  ├── Rail: 20m aluminium V-track, modular sections (5m each)
  ├── Inclination: 15 degrees (adjustable 10-20 degrees)
  ├── Cradle: Universal with adjustable width (fits MINI through MEDIUM)
  ├── Release: Electromagnetic latch (fail-safe: releases on power loss)
  ├── Pneumatic piston: 300mm bore, 2m stroke, 10 bar operating pressure
  ├── Compressor: 3kW electric, charges accumulator in 3-5 minutes
  ├── Accumulator: 200L at 10 bar = enough for 3 launches before recharge
  ├── Turntable: Motorised base plate rotates entire rail ±180 degrees
  │   to align with wind direction (stepper motor + gearbox)
  └── Automated loading: Conveyor belt moves drone from hangar to cradle

  AUTOMATED LOADING SEQUENCE:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  1. Drone exits hangar on motorised roller conveyor         │
  │                                                             │
  │     ┌──┐                                                    │
  │     │██│──►  ○○○○○○○○○○  ──► CRADLE                        │
  │     └──┘     conveyor                                       │
  │   (hangar)   rollers         (at base of rail)              │
  │                                                             │
  │  2. Drone wings auto-lock (spring-loaded detent)            │
  │  3. Cradle clamps close (pneumatic, 2x clamps)             │
  │  4. Pre-launch checks: IMU, GPS lock, battery voltage,     │
  │     control surfaces deflect through full range             │
  │  5. Compressor confirms accumulator at 10 bar              │
  │  6. ArduPilot confirms ready (MAVLink COMMAND_ACK)         │
  │  7. Countdown: 3-2-1-LAUNCH                                │
  │  8. Electromagnetic latch releases → piston fires          │
  │  9. Drone accelerates along rail, becomes airborne         │
  │  10. Cradle decelerates (shock absorber at rail end)       │
  │  11. Cradle returns to base position (gravity + winch)     │
  │                                                             │
  │  TOTAL TIME: ~90 seconds from hangar exit to airborne      │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

### B) RECOVERY SYSTEM

```
  RECOVERY SYSTEM DESIGN
  ═════════════════════

  RECOVERY METHOD BY TIER:
  ┌──────────┬──────────────────────────────────────────────────────┐
  │ Tier     │ Recovery Method                                     │
  ├──────────┼──────────────────────────────────────────────────────┤
  │ MICRO    │ Expendable / belly landing on grass (no recovery    │
  │ (0.5kg)  │ infrastructure needed — drone is cheap enough to    │
  │          │ replace). Belly skid on foam underside. Collected   │
  │          │ manually or by ground robot.                        │
  ├──────────┼──────────────────────────────────────────────────────┤
  │ MINI     │ PRIMARY: Net capture (ScanEagle Skyhook concept)    │
  │ (5-15kg) │ BACKUP: Parachute + GPS-guided parafoil landing     │
  │          │ ALTERNATIVE: Belly landing on smooth surface        │
  ├──────────┼──────────────────────────────────────────────────────┤
  │ MEDIUM   │ PRIMARY: Arresting wire (Zipline P1 style)          │
  │ (25-50kg)│ BACKUP: Net capture (larger net, reinforced)        │
  │          │ ALTERNATIVE: Autonomous belly landing (GPS-RTK)     │
  ├──────────┼──────────────────────────────────────────────────────┤
  │ LARGE    │ PRIMARY: Autonomous runway landing (GPS-RTK         │
  │ (100-    │   + vision-based approach, 50-100m prepared strip)  │
  │  200kg)  │ BACKUP: Arresting wire (heavy duty)                 │
  │          │ EMERGENCY: Parachute + airbag                       │
  └──────────┴──────────────────────────────────────────────────────┘

  NET CAPTURE SYSTEM (MINI Tier — Primary)
  ────────────────────────────────────────

  Reference: Insitu ScanEagle Skyhook (vertical rope capture)
  Our variant: horizontal net barrier (simpler, lower risk)

  FRONT VIEW:
                    NET (nylon, 12mm mesh)
                    10m wide x 6m high
                    deceleration: 3-5m depth
              ┌─────────────────────────────┐
              │ ╲                         ╱ │
              │   ╲                     ╱   │
              │     ╲       ██        ╱     │ ◄── Drone flies into net
              │       ╲     ██      ╱       │     at approach speed
              │         ╲   ██    ╱         │     (~15 m/s)
              │           ╲ ██  ╱           │
              │             ╲╱              │     Motor cuts at net
              │              │              │     contact (geofence
              │              │              │     trigger)
          ┌───┴───┐          │          ┌───┴───┐
          │ POLE  │          │          │ POLE  │
          │ 8m    │   (APPROACH PATH)   │ 8m    │
          │ steel │          │          │ steel │
          │ tube  │          │          │ tube  │
          │       │          │          │       │
          │ guyed │          │          │ guyed │
          │ wires │          │          │ wires │
          └───┬───┘          │          └───┬───┘
          ════╧══════════════╧══════════════╧════
                         GROUND

  NET SPECIFICATIONS:
  ├── Material: High-tenacity nylon, knotless
  ├── Mesh size: 12mm (captures fuselage, does not snag wings)
  ├── Deceleration depth: 3-5m (net stretches backward)
  ├── Energy absorption: Bungee cords at attachment points
  │   absorb kinetic energy gradually
  ├── Kinetic energy at capture (10kg at 15m/s): 1,125 J
  │   Equivalent to catching a cricket ball at 50 m/s — manageable
  ├── Pole spacing: 10m
  ├── Pole height: 8m (net bottom at 2m, top at 8m)
  ├── Approach guidance: RTK-GPS (±2cm accuracy) steers drone
  │   to centre of net. Backup: IR beacon on net frame.
  └── After capture: Drone slides down into net pocket at base.
      Motorised conveyor carries drone to hangar entrance.

  ARRESTING WIRE SYSTEM (MEDIUM Tier — Primary)
  ──────────────────────────────────────────────

  Reference: Zipline P1 tailhook recovery

  TOP VIEW:
                    APPROACH
                       │
                       │
                       ▼
              ┌────────────────────┐
              │                    │
              │   WIRE spans 15m  │
              │   ════════════════│
              │        │          │
              │        │ hook     │
              │        │ catches  │
              │        ▼          │
              │   ┌──────────┐   │
              │   │ ARRESTING│   │
              │   │ ENGINE   │   │
              │   │ (rotary  │   │
              │   │ damper)  │   │
              │   └──────────┘   │
              └────────────────────┘

  DRONE MODIFICATION:
  ├── Tailhook: Retractable hook mounted beneath tail
  ├── Extends automatically at 200m from recovery zone
  ├── Hook aperture: 150mm wide (catches 6mm wire)
  ├── ArduPilot approach: GPS-RTK guided descending approach
  │   at 3-degree glide slope, crossing wire at 2-3m altitude

  WIRE SPECIFICATIONS:
  ├── Material: 6mm stainless steel cable, plastic-sheathed
  ├── Span: 15m between two uprights
  ├── Height: 2.5m above ground (adjustable)
  ├── Arresting engine: Rotary hydraulic damper
  │   Absorbs energy over 10-15m of wire run-out
  │   Resets automatically (electric winch rewinds wire)
  ├── Kinetic energy (40kg at 22m/s): 9,680 J
  │   Requires serious arresting gear — similar to model
  │   aircraft carrier systems but smaller scale
  └── After arrest: Drone lowers to ground, conveyor to hangar
```

### C) BATTERY / CHARGING SYSTEM

```
  BATTERY AND CHARGING SYSTEM
  ═══════════════════════════

  TWO APPROACHES (both implemented for redundancy):

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  APPROACH 1: AUTOMATED BATTERY SWAP (fast turnaround)          │
  │  ─────────────────────────────────────────────────────          │
  │                                                                 │
  │  Drone arrives in hangar → robotic arm removes depleted        │
  │  battery → inserts fresh pre-charged battery → drone ready     │
  │                                                                 │
  │  TIME: ~60 seconds per swap                                     │
  │                                                                 │
  │  BATTERY CAROUSEL DESIGN:                                       │
  │                                                                 │
  │         TOP VIEW OF CAROUSEL                                    │
  │                                                                 │
  │              ┌───┐                                              │
  │          ┌───┤ 1 ├───┐       Battery slots numbered 1-20       │
  │       ┌──┤20 │   │ 2 ├──┐   Each slot has:                    │
  │    ┌──┤19│   └─┬─┘   │ 3├─┐ ├── Charge contacts (spring-pin) │
  │    │  │  └──┐  │  ┌──┘  │ │ ├── Temperature sensor            │
  │    │18│     │  │  │     │4│ ├── Individual BMS monitoring      │
  │    │  │     │  │  │     │ │ ├── Status LED (R/Y/G)            │
  │    │  ├──┐  │  │  │  ┌──┤ │ └── Ejector mechanism (solenoid) │
  │    │17│  │  │AXIS │  │  │5│                                    │
  │    │  │  │  │  │  │  │  │ │ Carousel rotates to present next  │
  │    │  ├──┘  │  │  │  └──┤ │ charged battery to robotic arm    │
  │    │16│     │  │  │     │6│                                    │
  │    │  │     │  │  │     │ │ Motor: NEMA 34 stepper + worm     │
  │    └──┤15│  └──┘  │  │ 7├─┘ gear (self-locking)               │
  │       └──┤14│   │ 8├──┘                                        │
  │          └───┤13├───┘                                           │
  │              │  │                                               │
  │          ┌───┤12├───┐                                           │
  │          │11 │  │ 9 │                                           │
  │          └───┤10├───┘                                           │
  │              └───┘                                              │
  │                                                                 │
  │  ROBOTIC ARM (for battery swap + payload swap):                 │
  │  ├── Type: 4-axis SCARA or articulated arm                     │
  │  ├── Reach: 600mm                                               │
  │  ├── Payload capacity: 5kg (handles batteries up to 4kg)       │
  │  ├── Gripper: Custom pneumatic with battery alignment pins     │
  │  ├── Reference: Dobot Magician (educational SCARA, ~£1,200)    │
  │  │   or used industrial arm (Epson/Denso, £2,000-5,000 used)  │
  │  ├── BUDGET: Linear actuator gantry with servo gripper         │
  │  │   (aluminium extrusion + stepper motors, ~£300 DIY)         │
  │  └── Controller: Arduino Mega or Raspberry Pi running          │
  │      custom sequence, triggered by MAVLink landing event       │
  │                                                                 │
  │  BATTERY SPECIFICATIONS (MINI tier):                            │
  │  ├── Type: 6S 22.2V 10,000mAh LiPo (or Li-ion 18650 pack)   │
  │  ├── Weight: ~1.2 kg per pack                                  │
  │  ├── Energy: 222 Wh per pack                                   │
  │  ├── Connector: XT90 power + 7-pin balance + data (I2C)       │
  │  ├── Mounting: Quick-release dovetail (matches payload system) │
  │  └── Identification: RFID tag for cycle count tracking         │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  APPROACH 2: IN-PLACE CHARGING (simpler, slower)               │
  │  ───────────────────────────────────────────────                │
  │                                                                 │
  │  Drone lands on charging pad → spring-loaded contacts on       │
  │  pad mate with contacts on drone belly → charges in place      │
  │                                                                 │
  │  TIME: 45-60 minutes for 80% charge (fast charge)              │
  │         90-120 minutes for full charge (balance charge)         │
  │                                                                 │
  │       SIDE VIEW OF CHARGING PAD                                 │
  │                                                                 │
  │           ┌──────────────────┐                                  │
  │           │     DRONE        │                                  │
  │           │   ┌──┐  ┌──┐    │                                  │
  │           │   │  │  │  │    │                                  │
  │      ═════╪═══╪══╪══╪══╪════╪═════                             │
  │           │   ▲  ▲  ▲  ▲    │                                  │
  │           │   │  │  │  │    │                                  │
  │           │   SPRING-PIN    │                                  │
  │           │   CONTACTS      │ ◄── Charging pad surface         │
  │           │   (gold-plated  │     (aluminium, with alignment   │
  │           │    pogo pins)   │      V-groove for repeatable     │
  │           └──────────────────┘     positioning)                │
  │                                                                 │
  │  CHARGING PAD SPECIFICATIONS:                                   │
  │  ├── Contacts: 4x spring-loaded pogo pins (2x power, 2x data) │
  │  ├── Alignment: V-groove in pad surface + drone belly keel     │
  │  ├── Charger: iCharger X8 (1100W, 8S max, balance charge)     │
  │  ├── Per-pad cost: ~£200 (charger) + £30 (pad hardware)       │
  │  └── Number of pads: 6-10 for continuous fleet operations      │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  CHARGING INFRASTRUCTURE SIZING:

  Assumptions:
  ├── Fleet: 20 MINI-tier drones
  ├── Mission duration: 60 minutes
  ├── Battery: 222 Wh (6S 10Ah LiPo)
  ├── Fast charge rate: 2C (charges 80% in 25 min)
  ├── Full charge rate: 1C (charges 100% in 60 min)
  └── Desired sortie rate: 10 missions per hour

  OPTION A: Battery swap (60-second turnaround)
  ├── Need 10 drones cycling simultaneously
  ├── Need 10 spare batteries charging at any time
  ├── 10 chargers x 250W each = 2.5 kW charging load
  ├── 20 carousel slots (10 charging, 10 ready)
  └── Turnaround time: 90 seconds (swap + pre-flight check)

  OPTION B: In-place charging (60-minute turnaround)
  ├── For 10 missions/hour with 60-min charge time:
  │   Need 10 charging pads occupied continuously
  ├── 10 pads x 250W = 2.5 kW (same power, slower throughput)
  ├── Total fleet on ground at any time: 10 charging + 10 airborne
  └── Less efficient but mechanically simpler (no robotic arm)

  RECOMMENDATION: Start with in-place charging (simpler).
  Add battery swap capability when throughput demands it.

  THERMAL MANAGEMENT:
  ├── LiPo batteries must be charged between 10-45 degrees C
  ├── Carousel chamber: thermostatically controlled (heater + fan)
  ├── In winter (UK): Heating element maintains 20C minimum
  ├── In summer: Extraction fan prevents overheating
  ├── Each slot has individual thermocouple on battery surface
  ├── BMS data logged per battery: cycle count, internal resistance,
  │   capacity fade — batteries retired at 80% original capacity
  └── Fire safety: Each slot has ceramic wool separator
      + halon or aerosol fire suppression (per-slot)
```

### D) STORAGE AND MAINTENANCE

```
  STORAGE AND MAINTENANCE SYSTEM
  ══════════════════════════════

  DRONE HANGAR (6m x 8m, 3m ceiling height)
  ──────────────────────────────────────────

  FLOOR PLAN:
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  ENTRANCE   (motorised roller door, 3m wide x 2.5m)  │
  │  ═══════                                               │
  │                                                        │
  │  ┌─────────────────────────────────────────────────┐  │
  │  │           DRONE STORAGE RACKS                    │  │
  │  │                                                   │  │
  │  │   Rack 1    Rack 2    Rack 3    Rack 4    Rack 5 │  │
  │  │   ┌────┐   ┌────┐   ┌────┐   ┌────┐   ┌────┐  │  │
  │  │   │ D1 │   │ D3 │   │ D5 │   │ D7 │   │ D9 │  │  │ MINI
  │  │   ├────┤   ├────┤   ├────┤   ├────┤   ├────┤  │  │ drones
  │  │   │ D2 │   │ D4 │   │ D6 │   │ D8 │   │D10│  │  │ (wings
  │  │   └────┘   └────┘   └────┘   └────┘   └────┘  │  │  folded)
  │  │                                                   │  │
  │  │   Each rack: 800mm wide, 600mm deep, 2 levels    │  │
  │  │   Rack slides out on linear rails for access     │  │
  │  └─────────────────────────────────────────────────┘  │
  │                                                        │
  │  ┌──────────────────┐    ┌─────────────────────────┐  │
  │  │  ROBOTIC ARM     │    │  BATTERY CAROUSEL       │  │
  │  │  STATION         │    │  (20 slots)             │  │
  │  │                  │    │                         │  │
  │  │  ┌──┐            │    │  See carousel diagram   │  │
  │  │  │AR│ ◄── Arm    │    │  above                  │  │
  │  │  │M │   reach    │    │                         │  │
  │  │  └──┘   covers   │    │  10x chargers mounted   │  │
  │  │         rack +   │    │  on wall behind carousel│  │
  │  │         carousel │    │                         │  │
  │  └──────────────────┘    └─────────────────────────┘  │
  │                                                        │
  │  ┌──────────────────────────────────────────────────┐ │
  │  │  PAYLOAD SWAP STATION                             │ │
  │  │                                                    │ │
  │  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         │ │
  │  │  │Camera│  │LiDAR │  │Cargo │  │Sensor│  Payload│ │
  │  │  │  EO  │  │      │  │Bay   │  │Pod   │  shelf  │ │
  │  │  └──────┘  └──────┘  └──────┘  └──────┘         │ │
  │  │                                                    │ │
  │  │  Same dovetail quick-release as drone interface   │ │
  │  │  Robotic arm can swap payloads (60-second swap)   │ │
  │  └──────────────────────────────────────────────────┘ │
  │                                                        │
  │  ┌──────────────────────────────────────────────────┐ │
  │  │  AUTOMATED HEALTH CHECK STATION                   │ │
  │  │                                                    │ │
  │  │  When drone enters hangar after recovery:         │ │
  │  │  1. Weight measurement (load cell in floor rail)  │ │
  │  │     — detects payload loss or structural damage   │ │
  │  │  2. Visual inspection cameras (4x Raspberry Pi    │ │
  │  │     HQ cameras, top/bottom/left/right)            │ │
  │  │     — ML model detects cracks, missing parts,     │ │
  │  │       prop damage (future capability)             │ │
  │  │  3. Control surface test (ArduPilot servo test    │ │
  │  │     command via MAVLink — deflects all surfaces   │ │
  │  │     through full range while cameras watch)       │ │
  │  │  4. Battery health readout (I2C smart battery     │ │
  │  │     data — voltage, temp, cycle count, IR)        │ │
  │  │  5. GPS/IMU self-test (ArduPilot preflight check) │ │
  │  │                                                    │ │
  │  │  PASS → Drone cleared for next mission            │ │
  │  │  FAIL → Drone flagged, moved to maintenance bay   │ │
  │  │         (manual inspection required)              │ │
  │  └──────────────────────────────────────────────────┘ │
  │                                                        │
  │  ┌──────────────────────────────────────────────────┐ │
  │  │  SPARE PARTS STORAGE                              │ │
  │  │                                                    │ │
  │  │  Labelled bins:                                   │ │
  │  │  ├── Propellers (10x per drone type)              │ │
  │  │  ├── Servo motors (4x spare)                      │ │
  │  │  ├── Control surface hinges                       │ │
  │  │  ├── SMA connectors and antenna elements          │ │
  │  │  ├── Wiring harnesses (pre-made)                  │ │
  │  │  ├── Pixhawk carrier boards (2x spare)            │ │
  │  │  ├── GPS modules (2x spare)                       │ │
  │  │  └── Structural repair kit (epoxy, carbon cloth)  │ │
  │  └──────────────────────────────────────────────────┘ │
  │                                                        │
  └────────────────────────────────────────────────────────┘
```

### E) INFRASTRUCTURE

```
  INFRASTRUCTURE SYSTEMS
  ═════════════════════

  ┌──────────────────────────────────────────────────────────────┐
  │  POWER SYSTEM                                                │
  │  ────────────                                                │
  │                                                              │
  │  Designed for off-grid operation with grid connection as     │
  │  optional primary source.                                    │
  │                                                              │
  │  ┌────────────────────────────────────────────────────────┐ │
  │  │                                                        │ │
  │  │   ┌──────────┐    ┌──────────────┐    ┌────────────┐  │ │
  │  │   │ SOLAR    │    │ GRID         │    │ DIESEL     │  │ │
  │  │   │ ARRAY    │    │ CONNECTION   │    │ GENERATOR  │  │ │
  │  │   │ 10 kW    │    │ (if avail.)  │    │ 7kW        │  │ │
  │  │   │ 24 panels│    │ single-phase │    │ auto-start │  │ │
  │  │   │ @ 415W   │    │ 230V/32A     │    │ when batt  │  │ │
  │  │   └────┬─────┘    └──────┬───────┘    │ <20% SOC  │  │ │
  │  │        │                  │            └─────┬──────┘  │ │
  │  │        │                  │                  │         │ │
  │  │        ▼                  ▼                  ▼         │ │
  │  │   ┌──────────────────────────────────────────────┐    │ │
  │  │   │         VICTRON MULTIPLUS-II 48/5000          │    │ │
  │  │   │         (inverter/charger)                    │    │ │
  │  │   │                                               │    │ │
  │  │   │         + Victron MPPT 250/100 solar          │    │ │
  │  │   │           charge controller                   │    │ │
  │  │   └────────────────────┬─────────────────────────┘    │ │
  │  │                        │                               │ │
  │  │                        ▼                               │ │
  │  │   ┌──────────────────────────────────────────────┐    │ │
  │  │   │    BATTERY BANK                               │    │ │
  │  │   │    48V 200Ah LiFePO4 (9.6 kWh)              │    │ │
  │  │   │    (Pylontech US3000C x 4 modules)           │    │ │
  │  │   │                                               │    │ │
  │  │   │    Provides ~6 hours backup at full load      │    │ │
  │  │   │    (overnight operation without grid/gen)     │    │ │
  │  │   └────────────────────┬─────────────────────────┘    │ │
  │  │                        │                               │ │
  │  │                        ▼                               │ │
  │  │   ┌──────────────────────────────────────────────┐    │ │
  │  │   │  DISTRIBUTION                                 │    │ │
  │  │   │  ├── Operations centre: 1.5 kW (servers,     │    │ │
  │  │   │  │    monitors, comms, HVAC)                  │    │ │
  │  │   │  ├── Drone charging: 2.5 kW (10x chargers)  │    │ │
  │  │   │  ├── Catapult compressor: 3 kW (intermittent)│    │ │
  │  │   │  ├── Hangar systems: 0.5 kW (lighting,      │    │ │
  │  │   │  │    conveyor, robotic arm)                  │    │ │
  │  │   │  ├── External: 0.5 kW (CCTV, lighting,      │    │ │
  │  │   │  │    weather station, perimeter)             │    │ │
  │  │   │  └── TOTAL CONTINUOUS: ~5 kW                 │    │ │
  │  │   │      PEAK (with compressor): ~8 kW           │    │ │
  │  │   └──────────────────────────────────────────────┘    │ │
  │  │                                                        │ │
  │  └────────────────────────────────────────────────────────┘ │
  │                                                              │
  │  DAILY ENERGY BUDGET:                                        │
  │  ├── 5kW continuous x 24h = 120 kWh/day                    │
  │  ├── Solar generation (UK, 10kW array, average):            │
  │  │   Summer: ~40-50 kWh/day                                 │
  │  │   Winter: ~8-12 kWh/day                                  │
  │  ├── Grid/generator makes up deficit                        │
  │  ├── Off-grid operation (summer only): feasible with        │
  │  │   reduced sortie rate                                     │
  │  └── Off-grid operation (year-round): needs 20kW+ solar    │
  │      or reliable generator fuel supply                       │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  COMMUNICATIONS                                              │
  │  ──────────────                                              │
  │                                                              │
  │  REDUNDANT LINKS (3 independent paths):                      │
  │                                                              │
  │  1. PRIMARY: 4G/5G cellular (always-on data link)           │
  │     ├── Cradlepoint or Sierra Wireless modem                │
  │     ├── Roof-mounted MIMO antenna (4x4)                     │
  │     ├── Dual SIM (two carriers for redundancy)              │
  │     ├── VPN tunnel to cloud server / operations HQ          │
  │     └── Bandwidth: 10-100 Mbps (depends on coverage)       │
  │                                                              │
  │  2. SECONDARY: Satellite (Starlink or Iridium)              │
  │     ├── Starlink flat-panel antenna (roof-mounted)          │
  │     │   50-200 Mbps, £75/month, low latency                │
  │     │   PREFERRED for remote sites                          │
  │     ├── OR: Iridium Certus modem (for truly remote sites)  │
  │     │   700 kbps, £200+/month, global coverage              │
  │     └── Auto-failover from 4G to satellite when signal lost│
  │                                                              │
  │  3. TERTIARY: VHF/UHF radio (voice backup)                 │
  │     ├── Icom IC-7300 or similar HF/VHF transceiver         │
  │     ├── Voice communication with HQ / emergency services   │
  │     └── AIS receiver (if coastal installation)              │
  │                                                              │
  │  DRONE COMMUNICATION (separate from backhaul):              │
  │     ├── 3x RFD900x radios (telemetry, 40+ km range)        │
  │     ├── High-gain directional antennas on rotator           │
  │     ├── 5.8GHz patch array for video downlink               │
  │     └── All mast-mounted at 10-15m height                   │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  PERIMETER SECURITY                                          │
  │  ──────────────────                                          │
  │                                                              │
  │  ├── 2.4m chain-link fence with barbed wire top             │
  │  ├── Single vehicle gate (electromagnetic lock, card reader)│
  │  ├── 6x CCTV cameras (IP, PoE, 4MP, IR night vision)      │
  │  │   4x at fence corners, 2x covering launch/recovery      │
  │  ├── PIR motion sensors on fence line (8x units)           │
  │  ├── NVR (network video recorder) in operations centre     │
  │  ├── Alarm: siren + strobe + SMS alert to operator         │
  │  └── Remote monitoring via cellular/satellite link          │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  ENVIRONMENTAL MONITORING                                    │
  │  ─────────────────────────                                   │
  │                                                              │
  │  ├── Davis Vantage Pro2 weather station (mast-mounted)      │
  │  │   Wind speed/direction, temperature, humidity, pressure, │
  │  │   rain, UV index, solar radiation                        │
  │  ├── Wind sock (illuminated, visible from ops centre)       │
  │  ├── RTK-GPS base station (for precision approach)          │
  │  │   u-blox ZED-F9P + survey-grade antenna                 │
  │  │   Provides ±2cm corrections to all drones via MAVLink   │
  │  ├── Approach lighting: LED strip lights on recovery zone   │
  │  │   Solar-powered, automatic dusk-to-dawn                  │
  │  └── Obstruction lighting: Red LED beacon on mast top      │
  │      (CAA requirement if mast >10m)                         │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

### F) MAIN BUILDING DESIGN

```
  MAIN BUILDING — SIDE VIEW (CROSS SECTION)
  ═════════════════════════════════════════

                  ANTENNA MAST (15m)
                        │
                   ┌────┤ Rotator + antennas
                   │ANT │ Weather station
                   └────┤
                        │
  ┌──────────────────────┼──────────────────────────┐
  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ◄── Roof: insulated
  │                                                  │     steel panels
  │          3m ceiling height                       │     + solar panels
  │                                                  │     on south face
  │  ┌────────────┐          ┌────────────────────┐ │
  │  │            │          │                    │ │
  │  │   HANGAR   │   wall   │   OPERATIONS       │ │
  │  │            │   with   │   CENTRE            │ │
  │  │  drones   │   door   │                    │ │
  │  │  on racks │          │  server rack (12U) │ │
  │  │           │          │  2x monitors       │ │
  │  │  carousel │          │  comms equipment   │ │
  │  │  robo arm │          │  UPS               │ │
  │  │           │          │  workbench         │ │
  │  │           │          │                    │ │
  │  └────────────┘          └────────────────────┘ │
  │                                                  │
  ├──════════════──┤          ├──══════════════════──┤
  │  ROLLER DOOR   │          │  PERSONNEL DOOR     │
  │  3m x 2.5m     │          │  + WINDOW            │
  └────────────────┘          └──────────────────────┘

  ════════════════════════════════════════════════════
                     CONCRETE PAD
               (150mm reinforced slab)

  BUILDING SPECIFICATIONS:
  ├── Structure: Steel portal frame (pre-fabricated kit building)
  ├── Cladding: Insulated steel sandwich panels (50mm PIR)
  ├── Floor: 150mm reinforced concrete slab (power-floated)
  ├── Dimensions: 12m x 8m footprint, 3m eaves height
  ├── Hangar section: 6m x 8m with 3m roller door
  ├── Operations section: 6m x 8m with personnel door + window
  ├── HVAC: Split-system air conditioning (heating + cooling)
  ├── Electrical: Consumer unit, RCDs, properly earthed
  ├── Fire: Smoke detectors, CO2 extinguisher, fire blanket
  │   Battery area: aerosol fire suppression system
  └── Cost estimate: £15,000-25,000 for building shell
      (supply + erect, excluding groundworks)
```

### G) THROUGHPUT CALCULATIONS

```
  THROUGHPUT AND FLEET SIZING
  ═══════════════════════════

  MISSION CYCLE TIMELINE (MINI tier, battery swap):
  ────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  TIME     EVENT                              DURATION        │
  │  ─────    ──────────────────────────────     ────────        │
  │  T+0:00   RECOVERY (net capture)             10 sec          │
  │  T+0:10   Conveyor to hangar                 30 sec          │
  │  T+0:40   Health check (auto)                20 sec          │
  │  T+1:00   Battery swap (robotic arm)         60 sec          │
  │  T+2:00   Payload swap (if needed)           60 sec          │
  │  T+3:00   Pre-flight check (ArduPilot)       30 sec          │
  │  T+3:30   Conveyor to catapult               30 sec          │
  │  T+4:00   Load on catapult cradle            30 sec          │
  │  T+4:30   Catapult charge + alignment        60 sec          │
  │  T+5:30   LAUNCH                             5 sec           │
  │                                                              │
  │  ═══════════════════════════════════════════════════          │
  │  TOTAL TURNAROUND TIME: ~5.5 minutes                         │
  │  (with battery swap, including payload change)               │
  │                                                              │
  │  WITHOUT payload change: ~4.5 minutes                        │
  │  WITHOUT battery swap (in-place charge): 60-90 minutes      │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

  SORTIE RATE CALCULATION:
  ────────────────────────

  With battery swap:
  ├── Turnaround time: 5.5 minutes
  ├── Single catapult can launch every 5.5 minutes
  ├── MAXIMUM SORTIE RATE: ~10 launches per hour
  ├── With 2 catapults (A+B, alternating): ~18 launches per hour
  └── Practical rate (allowing for delays): 8 per hour (1 catapult)

  FLEET SIZING FOR 24/7 COVERAGE:
  ────────────────────────────────

  SCENARIO: Continuous ISR coverage of a 20km radius area
  ├── Mission duration: 60 minutes (MINI tier endurance)
  ├── Transit time (to 20km, at 20m/s): 17 minutes
  ├── Time on station: 60 - 34 (transit both ways) = 26 minutes
  ├── Desired: 2 drones on station at all times
  │
  ├── Drones airborne at any moment:
  │   2 (on station) + 2 (in transit) = 4
  ├── Drones on ground (turnaround + charging spare batteries):
  │   4 (matching airborne count) + 2 (maintenance reserve)
  │
  ├── TOTAL FLEET: 10 drones
  ├── SPARE BATTERIES: 20 (2x fleet size)
  ├── MISSIONS PER DAY: 96 (4 airborne x 24 launches each)
  │
  └── COST: 10 drones x £3,000 = £30,000 (drone fleet only)

  SCENARIO: Cargo delivery hub (Zipline-style)
  ├── Service radius: 40 km (round trip 80 km at 25 m/s = 53 min)
  ├── Turnaround: 5.5 minutes (battery swap + cargo load)
  ├── Total cycle time: 58.5 minutes
  ├── Fleet of 20 drones, cycling continuously:
  │   20 drones / 58.5 min cycle = ~20 deliveries per hour
  │   = 480 deliveries per 24 hours
  │
  └── COST: 20 drones x £3,000 = £60,000 (drone fleet only)

  THROUGHPUT SUMMARY TABLE:
  ┌────────────────────────┬─────────────┬──────────────┬──────────┐
  │ Metric                 │ Battery Swap│ In-Place     │ Notes    │
  │                        │ (robotic)   │ Charge       │          │
  ├────────────────────────┼─────────────┼──────────────┼──────────┤
  │ Turnaround time        │ 5.5 min     │ 65 min       │          │
  │ Max sorties/hour       │ 10          │ 1 per drone  │ 1 rail   │
  │ Fleet for 24/7 (2 on   │ 10          │ 30           │          │
  │   station, 20km radius)│             │              │          │
  │ Deliveries/day (20     │ 480         │ ~50          │ Big diff │
  │   drone fleet)         │             │              │          │
  │ Mechanical complexity  │ HIGH        │ LOW          │          │
  │ Reliability            │ Moderate    │ High         │          │
  └────────────────────────┴─────────────┴──────────────┴──────────┘
```

---

## 4. COST ESTIMATES

```
  COMPONENT-LEVEL COST ESTIMATES (GBP)
  ════════════════════════════════════

  TIER 1: PORTABLE FIELD KIT
  ┌──────────────────────────────────────┬─────────┬────────────┐
  │ Category                             │ Budget  │ Recommended│
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ Compute (laptop/tablet)              │ £150    │ £150       │
  │ Telemetry radio + antenna            │ £40     │ £135       │
  │ Video receiver + antenna             │ £30     │ £30        │
  │ RC transmitter                       │ £75     │ £110       │
  │ Antenna tracker (DIY)                │ —       │ £40        │
  │ Power                                │ £25     │ £55        │
  │ Weather                              │ £8      │ £20        │
  │ Case                                 │ £45     │ £120       │
  │ Cables + accessories                 │ £45     │ £45        │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ TOTAL                                │ £418    │ £705       │
  └──────────────────────────────────────┴─────────┴────────────┘

  TIER 2: VEHICLE-MOUNTED MOBILE STATION
  ┌──────────────────────────────────────┬─────────┬────────────┐
  │ Category                             │ Budget  │ Full Spec  │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ Compute (workstation + monitors)     │ £600    │ £850       │
  │ Telemetry (3x radio + antennas)      │ £365    │ £365       │
  │ Video (4x RX + capture + antenna)    │ £175    │ £175       │
  │ RC transmitters (2x)                 │ £220    │ £220       │
  │ Antenna mast                         │ £150    │ £800       │
  │ Antenna rotator + controller         │ £50     │ £380       │
  │ Networking (4G + switch + antenna)   │ £265    │ £265       │
  │ Power (inverter + battery + charger) │ £610    │ £1,510     │
  │ Weather station                      │ £80     │ £250       │
  │ Team comms                           │ £60     │ £85        │
  │ Drone support (chargers, storage)    │ £200    │ £200       │
  │ Installation (rack, cables, roof)    │ £310    │ £310       │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ TOTAL (excludes vehicle)             │ £3,085  │ £5,410     │
  └──────────────────────────────────────┴─────────┴────────────┘

  TIER 3: AUTOMATED AIRBASE
  ┌──────────────────────────────────────┬─────────┬────────────┐
  │ Category                             │ Budget  │ Full Spec  │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ BUILDING + GROUNDWORKS               │         │            │
  │   Steel building (12m x 8m)          │ £15,000 │ £25,000    │
  │   Concrete slab + groundworks        │ £5,000  │ £8,000     │
  │   Fit-out (HVAC, electrical, fire)   │ £3,000  │ £5,000     │
  │                                      │         │            │
  │ LAUNCH SYSTEM                        │         │            │
  │   Pneumatic catapult (DIY)           │ £2,000  │ £5,000     │
  │   Turntable mechanism                │ £500    │ £1,500     │
  │   Automated loading conveyor         │ £800    │ £2,000     │
  │                                      │         │            │
  │ RECOVERY SYSTEM                      │         │            │
  │   Net capture (poles + net + rigging) │ £500    │ £1,500     │
  │   Arresting wire (MEDIUM tier)       │ £1,000  │ £3,000     │
  │   Taxiway conveyor                   │ £500    │ £1,500     │
  │                                      │         │            │
  │ BATTERY/CHARGING                     │         │            │
  │   20-slot carousel (DIY)             │ £500    │ £2,000     │
  │   10x chargers (iCharger X8)         │ £2,000  │ £2,000     │
  │   Robotic arm (DIY gantry)           │ £300    │ £3,000     │
  │   Thermal management                 │ £200    │ £500       │
  │   Fire suppression                   │ £300    │ £800       │
  │   20x spare batteries (6S 10Ah)      │ £2,000  │ £2,000     │
  │                                      │         │            │
  │ DRONE STORAGE + MAINTENANCE          │         │            │
  │   Storage racks                      │ £200    │ £500       │
  │   Health check cameras (4x RPi)      │ £200    │ £400       │
  │   Load cells + sensors               │ £100    │ £300       │
  │   Spare parts inventory              │ £500    │ £1,000     │
  │                                      │         │            │
  │ POWER                                │         │            │
  │   Solar array 10kW (24 panels)       │ £5,000  │ £7,000     │
  │   Battery bank (48V 200Ah LiFePO4)  │ £3,000  │ £4,000     │
  │   Inverter/charger (Victron)         │ £1,500  │ £2,000     │
  │   Diesel generator 7kW (auto-start)  │ £2,000  │ £3,500     │
  │   Electrical distribution            │ £500    │ £1,000     │
  │                                      │         │            │
  │ COMMUNICATIONS                       │         │            │
  │   Antenna mast (15m, guyed)          │ £1,000  │ £2,500     │
  │   Rotator + antennas                 │ £500    │ £1,500     │
  │   Telemetry radios (5x RFD900x)     │ £450    │ £450       │
  │   4G/5G modem + antenna              │ £250    │ £500       │
  │   Starlink terminal                  │ £450    │ £450       │
  │   RTK-GPS base station               │ £200    │ £400       │
  │   Operations PC + monitors           │ £800    │ £1,500     │
  │   Server (NVR + data logging)        │ £300    │ £800       │
  │                                      │         │            │
  │ SECURITY                             │         │            │
  │   Perimeter fence (300m)             │ £3,000  │ £5,000     │
  │   Gate + access control              │ £500    │ £1,000     │
  │   CCTV (6x cameras + NVR)           │ £400    │ £1,000     │
  │   PIR sensors + alarm                │ £200    │ £500       │
  │                                      │         │            │
  │ ENVIRONMENTAL                        │         │            │
  │   Weather station (Davis Pro2)       │ £400    │ £400       │
  │   Wind sock + lighting               │ £100    │ £200       │
  │   Approach/runway lighting           │ £200    │ £500       │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ TOTAL (infrastructure only)          │ £53,350 │ £99,700    │
  │                                      │         │            │
  │ DRONE FLEET (10x MINI @ £3,000)      │ £30,000 │ £30,000    │
  │ DRONE FLEET (20x MINI @ £3,000)      │ —       │ £60,000    │
  ├──────────────────────────────────────┼─────────┼────────────┤
  │ GRAND TOTAL (10-drone fleet)         │ £83,350 │ £129,700   │
  │ GRAND TOTAL (20-drone fleet)         │ —       │ £159,700   │
  └──────────────────────────────────────┴─────────┴────────────┘

  STUDENT/STARTUP COST REDUCTION OPPORTUNITIES:
  ──────────────────────────────────────────────
  1. Building: Use shipping containers (2x 40ft = £5,000) instead of
     steel-frame building (saves £10,000-15,000)
  2. Catapult: Start with bungee launch (£60) before pneumatic (£2,000+)
  3. Recovery: Start with belly landing on grass (£0) before net system
  4. Robotic arm: Build linear gantry from aluminium extrusion and
     stepper motors (£300 vs £3,000+ for commercial arm)
  5. Power: If grid-connected, skip solar + battery bank (saves £8,000)
  6. Generator: Skip if grid-connected (saves £2,000-3,500)
  7. Security: Start with padlock + game cameras (£50) instead of
     full CCTV + alarm system (saves £3,000)
  8. Comms: Skip Starlink initially, use 4G only (saves £450 + monthly)
  9. Buy used: Antenna rotators, generators, and server equipment
     are abundantly available on eBay from ham radio operators
     and IT decommissions (30-50% savings)
```

---

## 5. SCALING PATH: From £500 Field Kit to Automated Airbase

```
  INCREMENTAL SCALING ROADMAP
  ═══════════════════════════

  The key insight: every component built at a lower tier transfers
  directly to the next tier. Nothing is throwaway.

  PHASE 1: FIELD KIT (£400-700)
  ┌──────────────────────────────────────────────────────────────┐
  │ Summer 2026 — First flights                                  │
  │                                                              │
  │ BUILD:                                                       │
  │ ├── Pelican case ground station (Tier 1 BOM)                │
  │ ├── Single MINI-tier drone (Skywalker X8)                   │
  │ ├── Basic SiK telemetry (upgrade to RFD900x later)          │
  │ └── Antenna tracker project (doc 23) — this becomes a       │
  │     permanent component in all future tiers                  │
  │                                                              │
  │ LEARN:                                                       │
  │ ├── QGroundControl operation                                 │
  │ ├── MAVLink protocol deeply                                  │
  │ ├── ArduPilot tuning and configuration                       │
  │ ├── RF link budgets (practical experience)                   │
  │ └── Flight operations procedures                             │
  │                                                              │
  │ WHAT TRANSFERS TO TIER 2:                                    │
  │ ├── All radios, antennas, RC transmitter                    │
  │ ├── Antenna tracker (moves to vehicle mast)                  │
  │ ├── Laptop (becomes secondary display)                       │
  │ ├── All operational knowledge                                │
  │ └── Mission engine software (identical)                      │
  └──────────────────────────────────────────────────────────────┘
           │
           │  Upgrade cost: ~£2,500 (vehicle fit-out, excluding vehicle)
           ▼
  PHASE 2: VEHICLE STATION (cumulative ~£3,000-5,000)
  ┌──────────────────────────────────────────────────────────────┐
  │ 2027 — Multi-drone operations                               │
  │                                                              │
  │ BUILD (incremental on Phase 1):                              │
  │ ├── Fit existing vehicle with workstation                    │
  │ ├── Install telescoping mast (manual push-up first)         │
  │ ├── Add 2 more RFD900x radios (for multi-drone)            │
  │ ├── Add auxiliary battery + inverter                         │
  │ ├── Add 4G modem for remote connectivity                    │
  │ └── Bungee launch rail (first automated launch attempt)     │
  │                                                              │
  │ LEARN:                                                       │
  │ ├── Multi-drone coordination                                 │
  │ ├── Extended operations (8+ hours)                           │
  │ ├── Vehicle-based power management                           │
  │ ├── Mast-mounted antenna operations                          │
  │ └── Team coordination (multiple operators)                   │
  │                                                              │
  │ WHAT TRANSFERS TO TIER 3:                                    │
  │ ├── All telemetry radios + antennas                         │
  │ ├── Workstation PC + monitors                                │
  │ ├── Weather station                                          │
  │ ├── 4G modem + networking                                    │
  │ ├── Power management experience                              │
  │ └── Multi-drone operational procedures                       │
  └──────────────────────────────────────────────────────────────┘
           │
           │  Upgrade cost: ~£50,000-80,000 (site + infrastructure)
           │  This is where outside funding becomes necessary
           ▼
  PHASE 3A: MINIMUM VIABLE AIRBASE (cumulative ~£55,000-85,000)
  ┌──────────────────────────────────────────────────────────────┐
  │ 2028 — First fixed site (prove the concept)                  │
  │                                                              │
  │ BUILD (minimum viable):                                      │
  │ ├── Shipping container ops centre (1x 40ft, £2,500)         │
  │ ├── Concrete pad for launch/landing                          │
  │ ├── Bungee catapult (upgrade from vehicle rail)              │
  │ ├── Belly landing on grass (no recovery infrastructure)     │
  │ ├── Manual battery swap (no robotic arm yet)                │
  │ ├── 10x charging pads (in-place charging)                   │
  │ ├── Solar array (start with 5kW)                            │
  │ ├── Basic security (fence + game cameras)                   │
  │ └── 5 drones cycling (prove turnaround)                     │
  │                                                              │
  │ NOT YET:                                                     │
  │ ├── No robotic arm (manual battery swap is fine for 5 drones)│
  │ ├── No net recovery (belly landing works for MINI tier)     │
  │ ├── No automated health check (visual inspection by hand)   │
  │ └── No 24/7 ops (8-12 hour daily operation)                 │
  │                                                              │
  │ PROVE:                                                       │
  │ ├── Rapid turnaround is achievable                           │
  │ ├── Solar + battery power is sufficient                     │
  │ ├── Remote monitoring works (4G + Starlink)                 │
  │ └── Drones survive repeated belly landings                   │
  └──────────────────────────────────────────────────────────────┘
           │
           │  Upgrade cost: ~£30,000-50,000 (automation)
           ▼
  PHASE 3B: AUTOMATED AIRBASE (cumulative ~£85,000-130,000)
  ┌──────────────────────────────────────────────────────────────┐
  │ 2029+ — Full automation (the goal)                           │
  │                                                              │
  │ ADD (incremental automation):                                │
  │ ├── Pneumatic catapult (replace bungee)                     │
  │ ├── Net capture system (replace belly landing)              │
  │ ├── Robotic arm for battery swap                            │
  │ ├── Battery carousel                                         │
  │ ├── Automated health check cameras                           │
  │ ├── Motorised conveyor (hangar → catapult → hangar loop)    │
  │ ├── Expand solar to 10kW                                    │
  │ ├── Add diesel generator for 24/7 capability                │
  │ ├── Full CCTV + alarm system                                │
  │ ├── Expand fleet to 10-20 drones                            │
  │ └── Arresting wire (for future MEDIUM tier)                 │
  │                                                              │
  │ RESULT:                                                      │
  │ ├── Fully autonomous 24/7 operation                         │
  │ ├── 10+ sorties per hour                                     │
  │ ├── Remote monitoring only (no on-site operator)            │
  │ ├── Self-healing (auto-reroutes around failed drones)       │
  │ └── Revenue-generating capability (delivery, survey, etc.)  │
  └──────────────────────────────────────────────────────────────┘

  FUNDING MILESTONES:
  ───────────────────
  Phase 1: Self-funded (£500-700, summer job money)
  Phase 2: Self-funded (£2,500-3,000 additional)
  Phase 3A: Requires grant, competition prize, or angel investment
            Target: Innovate UK Smart Grant (up to £25,000)
            or university engineering department sponsorship
  Phase 3B: Requires commercial revenue or Series A investment
            (demonstrates revenue model first with Phase 3A)
```

---

## CONNECTION DIAGRAM: ALL THREE TIERS

```
  HOW THE TIERS INTERCONNECT
  ═════════════════════════

  All three tiers can operate simultaneously in a
  hierarchical command structure:

                    ┌─────────────────────────┐
                    │  TIER 3: AIRBASE        │
                    │  (command hub)           │
                    │                         │
                    │  Manages fleet of 10-50 │
                    │  drones autonomously    │
                    │                         │
                    │  Connected to cloud via │
                    │  4G + Starlink          │
                    └─────────┬───────────────┘
                              │
              4G/Starlink ────┤──── 4G/Starlink
              backhaul        │     backhaul
                              │
          ┌───────────────────┼──────────────────────┐
          │                   │                      │
          ▼                   ▼                      ▼
  ┌───────────────┐  ┌───────────────┐   ┌────────────────┐
  │ TIER 2:       │  │ TIER 2:       │   │ CLOUD SERVER   │
  │ VEHICLE #1    │  │ VEHICLE #2    │   │ (monitoring,   │
  │ (forward ops) │  │ (sector 2)    │   │  logging,      │
  │               │  │               │   │  customer      │
  │ 2-5 local     │  │ 2-5 local     │   │  portal)       │
  │ drones        │  │ drones        │   │                │
  └───────┬───────┘  └───────┬───────┘   └────────────────┘
          │                   │
   RFD900x telemetry   RFD900x telemetry
          │                   │
     ┌────┴────┐         ┌───┴────┐
     │ DRONES  │         │ DRONES │
     └─────────┘         └────────┘

  And a TIER 1 field kit can operate independently anywhere,
  or connect to the hierarchy via the operator's phone hotspot.

  ALL TIERS USE:
  ├── Same MAVLink v2 protocol
  ├── Same ArduPilot firmware
  ├── Same mission engine software
  ├── Same QGroundControl interface
  └── Same drone hardware
```

---

## APPENDIX: KEY VENDOR REFERENCES

```
  COMPONENT SOURCING (UK)
  ═══════════════════════

  Telemetry:
  ├── RFD900x: RFDesign (Australia), UK via Unmanned Tech, ~£90
  ├── SiK 433: Holybro or mRo, via GetFPV/Unmanned Tech, ~£25
  └── Doodle Labs (MEDIUM tier): direct from Doodle Labs, ~£500+

  Video:
  ├── Eachine ROTG02: Banggood/AliExpress, ~£20
  ├── TBS Fusion: Team BlackSheep via UK dealers, ~£65
  └── HDZero: HDZero store or UK FPV shops, ~£90

  RC:
  ├── RadioMaster: RadioMaster store or UK dealers, ~£75-150
  └── ELRS receivers: ExpressLRS ecosystem, ~£15-25

  Power:
  ├── LiFePO4 batteries: Fogstar, Epoch, or LiTime (UK), varies
  ├── Victron: Victron dealers UK, Bimble Solar
  └── Honda generators: Honda dealers UK

  Antennas:
  ├── Ham radio antennas/rotators: ML&S, Waters & Stanton
  ├── Masts: Clark Masts (UK manufacturer!), or used from MOD surplus
  └── Custom: 3D print + copper tape (patch antennas)

  Automation:
  ├── Stepper motors: Ooznest, RS Components
  ├── Linear actuators: Firgelli, Amazon
  ├── Industrial arms (used): eBay, Surplex auctions
  └── Aluminium extrusion: Ooznest, Motedis, RS Components

  Building:
  ├── Steel buildings: EasySteel, Olympia Steel Buildings
  ├── Shipping containers: ContainerTraders, Willbox
  └── Solar panels: Bimble Solar, Midsummer Energy
```

---

*Document version: 1.0*
*Created: 2026-03-25*
*Related documents: 22 (Multi-Scale Platform Family), 23 (Mesh Network and Directional Comms), 07 (Mission Engine Architecture), 08 (Payload System Design)*
*Next: Build Tier 1 field kit as first deliverable for Summer 2026 flight testing*
