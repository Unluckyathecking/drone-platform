"""Dovetail rail — mounts to fuselage floor, payload tray slides onto it.

Generates one rail. Mirror for the opposite side.
Material: 6061-T6 aluminum, CNC machined or extruded.

  CROSS-SECTION (looking from end):

      ┌──────────┐  ◄─ top_width (15mm)
      │          │
       ╲        ╱   ◄─ 45° dovetail angle (included)
        ╲      ╱
         └──┘       ◄─ base_width (≈2.6mm)

  With mounting holes along the base for M3 screws into fuselage floor.
"""

import cadquery as cq
import math
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    RAIL_HEIGHT, RAIL_TOP_WIDTH, RAIL_BASE_WIDTH, RAIL_LENGTH,
    RAIL_DOVETAIL_ANGLE, RAIL_MOUNTING_HOLE_DIA, RAIL_MOUNTING_HOLE_SPACING,
    DETENT_HOUSING_OD, DETENT_HOUSING_DEPTH, DETENT_OFFSET_FROM_END,
)


def make_dovetail_profile(top_width, base_width, height):
    """Create a 2D dovetail trapezoid profile centered at origin.

    The wide end (top) faces up (+Z in the extrusion direction).
    """
    half_top = top_width / 2
    half_base = base_width / 2

    pts = [
        (-half_base, 0),
        (half_base, 0),
        (half_top, height),
        (-half_top, height),
    ]

    result = cq.Workplane("XZ").polyline(pts).close()
    return result


def make_rail():
    """Generate the complete dovetail rail with mounting holes."""

    # Create dovetail cross-section and extrude along Y (flight axis)
    half_top = RAIL_TOP_WIDTH / 2
    half_base = RAIL_BASE_WIDTH / 2

    rail = (
        cq.Workplane("XZ")
        .moveTo(-half_base, 0)
        .lineTo(half_base, 0)
        .lineTo(half_top, RAIL_HEIGHT)
        .lineTo(-half_top, RAIL_HEIGHT)
        .close()
        .extrude(RAIL_LENGTH)
    )

    # Add a flat mounting flange at the base for screwing to fuselage
    flange_width = RAIL_TOP_WIDTH + 10  # 5mm extra on each side
    flange_thickness = 3.0

    flange = (
        cq.Workplane("XZ")
        .rect(flange_width, flange_thickness)
        .extrude(RAIL_LENGTH)
        .translate((0, 0, -flange_thickness / 2))
    )

    rail = rail.union(flange)

    # Mounting holes along the flange
    num_holes = int(RAIL_LENGTH / RAIL_MOUNTING_HOLE_SPACING) + 1
    first_hole_y = (RAIL_LENGTH - (num_holes - 1) * RAIL_MOUNTING_HOLE_SPACING) / 2

    for i in range(num_holes):
        y_pos = first_hole_y + i * RAIL_MOUNTING_HOLE_SPACING
        rail = (
            rail.faces("<Z")
            .workplane()
            .center(0, y_pos - RAIL_LENGTH / 2)
            .hole(RAIL_MOUNTING_HOLE_DIA, flange_thickness + 1)
        )

    # Detent pin housings (bored into the top of the rail)
    for offset in [DETENT_OFFSET_FROM_END, RAIL_LENGTH - DETENT_OFFSET_FROM_END]:
        rail = (
            rail.faces(">Z")
            .workplane()
            .center(0, offset - RAIL_LENGTH / 2)
            .hole(DETENT_HOUSING_OD, DETENT_HOUSING_DEPTH)
        )

    return rail


if __name__ == "__main__":
    rail = make_rail()

    # Export STEP and STL
    export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "dovetail_rail.step")
    stl_path = os.path.join(export_dir, "dovetail_rail.stl")

    cq.exporters.export(rail, step_path)
    cq.exporters.export(rail, stl_path)

    print(f"Exported: {step_path}")
    print(f"Exported: {stl_path}")
    print(f"Rail dimensions: {RAIL_TOP_WIDTH}mm top × {RAIL_BASE_WIDTH}mm base × {RAIL_HEIGHT}mm height × {RAIL_LENGTH}mm long")
