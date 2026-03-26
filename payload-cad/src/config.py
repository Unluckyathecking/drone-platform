"""Payload interface system — master configuration.

All dimensions in millimeters. Change values here to adjust all parts.
This is the single source of truth for the payload bay geometry.

  COORDINATE SYSTEM (matching ArduPilot NED):
    X = forward (nose)
    Y = right (starboard)
    Z = down

  PAYLOAD BAY CROSS-SECTION (looking forward):

        ◄────── bay_width (200mm) ──────►
        ┌──────────────────────────────────┐
        │         FUSELAGE SKIN            │
        │  ┌────────────────────────────┐  │  ▲
        │  │     PAYLOAD VOLUME         │  │  │ bay_height
        │  │                            │  │  │ (150mm)
        │  └────────────────────────────┘  │  ▼
        ╪══ RAIL ══╤═ CONNECTOR ╤══ RAIL ══╪
        └──────────┴───────────┴───────────┘
"""

import math

# ── Payload Bay Envelope ──────────────────────────────────────────
BAY_WIDTH = 200.0       # mm, internal width between fuselage walls
BAY_LENGTH = 300.0      # mm, along flight axis
BAY_HEIGHT = 150.0      # mm, depth below fuselage floor

# ── Dovetail Rail Profile ─────────────────────────────────────────
#
#    ┌──────────┐  ◄─ rail_top_width
#    │          │
#    ╲          ╱  ◄─ 45° dovetail angle (included)
#     ╲        ╱
#      └──────┘    ◄─ rail_base_width
#
# Geometry: 45° included dovetail → each face 22.5° from vertical
# offset_per_side = height × tan(22.5°) = 15 × 0.4142 = 6.21 mm
# base_width = top_width − 2 × offset = 15.0 − 12.43 = 2.57 → 2.6 mm
#
RAIL_HEIGHT = 15.0          # mm, height of the dovetail profile
RAIL_TOP_WIDTH = 15.0       # mm, width at the top (wide part)
RAIL_BASE_WIDTH = round(
    RAIL_TOP_WIDTH - 2 * RAIL_HEIGHT * math.tan(math.radians(22.5)),
    1,
)                           # mm, width at the narrow base (≈2.6 mm for 45° dovetail)
RAIL_LENGTH = 280.0         # mm, along flight axis (shorter than bay for clearance)
RAIL_DOVETAIL_ANGLE = 45.0  # degrees, included angle of the dovetail faces
RAIL_CLEARANCE = 0.55       # mm, gap between rail and tray for sliding fit

# ── Rail Mounting ─────────────────────────────────────────────────
# Rails mount on the fuselage floor, one on each side
RAIL_INSET = 10.0           # mm, distance from bay wall to rail outer edge
RAIL_MOUNTING_HOLE_DIA = 3.2    # mm, M3 clearance
RAIL_MOUNTING_HOLE_SPACING = 70.0  # mm, between mounting holes along rail

# ── Payload Tray ──────────────────────────────────────────────────
#
#    ┌──────────────────────────────────────┐
#    │         TRAY FLOOR                   │
#    │  ┌──────────────────────────────┐    │  ▲
#    │  │       PAYLOAD AREA           │    │  │ tray_depth
#    │  └──────────────────────────────┘    │  ▼
#    │                                      │
#    └──DOVETAIL──┴──CONNECTOR──┴──DOVETAIL─┘
#
TRAY_WIDTH = 180.0          # mm, between dovetail lips (< bay_width)
TRAY_LENGTH = 260.0         # mm, along flight axis (< rail_length for entry)
TRAY_DEPTH = 100.0          # mm, internal depth for payload
TRAY_WALL_THICKNESS = 2.5   # mm
TRAY_FLOOR_THICKNESS = 3.0  # mm
TRAY_FILLET_RADIUS = 3.0    # mm, internal corners

# ── Dovetail Tray Lips ───────────────────────────────────────────
# The tray has matching inverse dovetails on each side that slide onto the rails
TRAY_LIP_HEIGHT = RAIL_HEIGHT
TRAY_LIP_TOP_WIDTH = RAIL_TOP_WIDTH + RAIL_CLEARANCE
TRAY_LIP_BASE_WIDTH = RAIL_BASE_WIDTH + RAIL_CLEARANCE

# ── Quick-Release Detent Pins ────────────────────────────────────
DETENT_PIN_DIAMETER = 4.0       # mm, hardened steel pin
DETENT_HOLE_DIAMETER = 4.2      # mm, in tray (slight clearance)
DETENT_SPRING_OD = 8.0          # mm, compression spring outer diameter
DETENT_HOUSING_OD = 12.0        # mm, housing bore in fuselage floor
DETENT_HOUSING_DEPTH = 20.0     # mm
DETENT_COUNT = 2                # one front, one rear
DETENT_OFFSET_FROM_END = 30.0   # mm, from each end of rail

# ── Connector Interface Plate ─────────────────────────────────────
CONNECTOR_PLATE_WIDTH = 60.0    # mm
CONNECTOR_PLATE_HEIGHT = 40.0   # mm
CONNECTOR_PLATE_THICKNESS = 2.0 # mm, FR4 or G10 fiberglass

# Anderson PP45 power connector cutout
ANDERSON_WIDTH = 16.0       # mm, per pole
ANDERSON_HEIGHT = 20.0      # mm
ANDERSON_COUNT = 4           # +5V, +12V, VBATT, GND

# JST-GH 8-pin data connector cutout
JSTGH_WIDTH = 12.0          # mm
JSTGH_HEIGHT = 4.5          # mm

# Alignment pins
ALIGN_PIN_DIA = 3.0         # mm dowel pin
ALIGN_PIN_LENGTH = 8.0      # mm
ALIGN_PIN_SPACING = 40.0    # mm between pins

# ── Battery Rail (threaded rod system) ───────────────────────────
BATTERY_RAIL_TYPE = "threaded_rod"
BATTERY_RAIL_THREAD = "M6"
BATTERY_RAIL_DETENT_SPACING = 10.0  # mm

# ── DIP Switch (payload ID / voltage select) ────────────────────
DIP_SWITCH_WIDTH = 10.0         # mm
DIP_SWITCH_HEIGHT = 6.0         # mm
DIP_SWITCH_POSITIONS = 3        # 5V, 12V, VBATT

# ── Pull-Up Resistor (payload ID line) ──────────────────────────
ID_PULLUP_RESISTANCE = 10000    # ohms, to 3.3V

# ── CG Management ────────────────────────────────────────────────
# Sliding rail sub-system for CG adjustment
CG_SLIDE_TRAVEL = 120.0    # mm, total fore-aft travel
CG_SLIDE_STEP = 10.0       # mm, detent positions along the slide

# ── Safety Lanyard ────────────────────────────────────────────────
LANYARD_ANCHOR_DIA = 5.0    # mm, hole for steel cable eye
LANYARD_ANCHOR_OFFSET = 10.0  # mm from tray edge
LANYARD_BOLT_DIA = 4.0         # mm, M4 stainless through-bolt
LANYARD_BACKING_PLATE_SIZE = 15.0       # mm square
LANYARD_BACKING_PLATE_THICKNESS = 2.0   # mm, stainless steel

# ── Material Notes ────────────────────────────────────────────────
# Rails: 6061-T6 aluminum (CNC or extruded)
# Tray: PETG or Nylon PA12 (3D printed, 40-60% infill)
# Detent pins: Spring steel, 4mm diameter
# Connector plate: FR4 / G10 fiberglass 2mm
# Fasteners: M3 stainless steel socket head cap screws
# Battery rail: M6 threaded rod, stainless steel
# Lanyard backing: 2mm stainless steel plate, M4 through-bolt
