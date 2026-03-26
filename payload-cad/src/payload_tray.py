"""Payload tray — slides onto dovetail rails, carries payload modules.

3D printed in PETG or Nylon PA12 at 40-60% infill.

  TOP VIEW:
      ┌──────────────────────────────────┐
      │  ┌──────────────────────────┐    │
      │  │                          │    │
      │  │     PAYLOAD AREA         │    │
      │  │     (open top)           │    │
      │  │                          │    │
      │  └──────────────────────────┘    │
      │  ○ lanyard         lanyard ○     │
      └──DOVE──┴──CONNECTOR──┴──DOVE─────┘

  SIDE VIEW:
      ┌────────────────────────────────────┐
      │   TRAY WALLS (2.5mm thick)         │
      │   ┌────────────────────────────┐   │
      │   │       PAYLOAD AREA         │   │  tray_depth (100mm)
      │   │                            │   │
      │   └────────────────────────────┘   │
      │   ████ TRAY FLOOR (3mm) ████████   │
      │                                    │
      └──▼ dovetail lips ▼────────────────┘
           (match 45° dovetail rail + 0.55mm clearance)
"""

import cadquery as cq
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    TRAY_WIDTH, TRAY_LENGTH, TRAY_DEPTH,
    TRAY_WALL_THICKNESS, TRAY_FLOOR_THICKNESS, TRAY_FILLET_RADIUS,
    TRAY_LIP_HEIGHT, TRAY_LIP_TOP_WIDTH, TRAY_LIP_BASE_WIDTH,
    RAIL_CLEARANCE, RAIL_HEIGHT,
    DETENT_HOLE_DIAMETER, DETENT_OFFSET_FROM_END,
    LANYARD_ANCHOR_DIA, LANYARD_ANCHOR_OFFSET,
    LANYARD_BOLT_DIA, LANYARD_BACKING_PLATE_SIZE, LANYARD_BACKING_PLATE_THICKNESS,
    CONNECTOR_PLATE_WIDTH, CONNECTOR_PLATE_HEIGHT, CONNECTOR_PLATE_THICKNESS,
    ANDERSON_WIDTH, ANDERSON_HEIGHT, ANDERSON_COUNT,
    JSTGH_WIDTH, JSTGH_HEIGHT,
    ALIGN_PIN_DIA, ALIGN_PIN_SPACING,
)


def make_tray_body():
    """Create the main tray box — open-top container with dovetail lips."""

    # Outer shell
    outer = (
        cq.Workplane("XY")
        .box(TRAY_WIDTH, TRAY_LENGTH, TRAY_DEPTH + TRAY_FLOOR_THICKNESS)
        .translate((0, 0, (TRAY_DEPTH + TRAY_FLOOR_THICKNESS) / 2))
    )

    # Inner cavity (subtract from top, leaving floor)
    inner_width = TRAY_WIDTH - 2 * TRAY_WALL_THICKNESS
    inner_length = TRAY_LENGTH - 2 * TRAY_WALL_THICKNESS
    inner = (
        cq.Workplane("XY")
        .box(inner_width, inner_length, TRAY_DEPTH + 1)  # +1 to cut through top
        .translate((0, 0, TRAY_FLOOR_THICKNESS + TRAY_DEPTH / 2 + 0.5))
    )

    tray = outer.cut(inner)

    # Fillet internal edges
    try:
        tray = tray.edges("|Z").fillet(TRAY_FILLET_RADIUS)
    except Exception:
        pass  # Fillet may fail on some edges, continue

    return tray


def make_dovetail_lips():
    """Create the dovetail lips on each side that slide onto the rails.

    These are inverse dovetails — the tray hangs from the rails.
    """
    half_top = TRAY_LIP_TOP_WIDTH / 2
    half_base = TRAY_LIP_BASE_WIDTH / 2

    # Profile matches the rail but inverted (groove, not protrusion)
    # The lip wraps around the rail from below
    lip_profile = (
        cq.Workplane("XZ")
        .moveTo(-half_base, 0)
        .lineTo(half_base, 0)
        .lineTo(half_top, TRAY_LIP_HEIGHT)
        .lineTo(-half_top, TRAY_LIP_HEIGHT)
        .close()
    )

    lip = lip_profile.extrude(TRAY_LENGTH)

    # Position: one lip on each side of the tray
    # The lips sit below the tray floor (Z=0), hanging down
    left_lip = lip.translate((
        -(TRAY_WIDTH / 2 - TRAY_LIP_TOP_WIDTH / 2),
        0,
        -TRAY_LIP_HEIGHT
    ))

    right_lip = lip.translate((
        (TRAY_WIDTH / 2 - TRAY_LIP_TOP_WIDTH / 2),
        0,
        -TRAY_LIP_HEIGHT
    ))

    return left_lip, right_lip


def make_detent_holes(tray):
    """Add detent pin holes in the dovetail lips for the quick-release pins."""
    for y_offset in [
        -TRAY_LENGTH / 2 + DETENT_OFFSET_FROM_END,
        TRAY_LENGTH / 2 - DETENT_OFFSET_FROM_END,
    ]:
        # Holes on both left and right lips
        for x_sign in [-1, 1]:
            x_pos = x_sign * (TRAY_WIDTH / 2 - TRAY_LIP_TOP_WIDTH / 2)
            tray = (
                tray.faces("<Z")
                .workplane()
                .center(x_pos, y_offset)
                .hole(DETENT_HOLE_DIAMETER, TRAY_LIP_HEIGHT + TRAY_FLOOR_THICKNESS)
            )
    return tray


def make_connector_cutout(tray):
    """Cut the connector opening in the rear wall of the tray.

    This is where the Anderson PP45 + JST-GH connectors mate.
    """
    # Rear wall is at Y = +TRAY_LENGTH/2
    cutout = (
        cq.Workplane("XZ")
        .rect(CONNECTOR_PLATE_WIDTH, CONNECTOR_PLATE_HEIGHT)
        .extrude(TRAY_WALL_THICKNESS + 2)
        .translate((0, TRAY_LENGTH / 2 - TRAY_WALL_THICKNESS / 2, TRAY_FLOOR_THICKNESS + CONNECTOR_PLATE_HEIGHT / 2))
    )

    tray = tray.cut(cutout)

    # Alignment pin holes in the rear wall
    for x_offset in [-ALIGN_PIN_SPACING / 2, ALIGN_PIN_SPACING / 2]:
        pin_hole = (
            cq.Workplane("XZ")
            .circle(ALIGN_PIN_DIA / 2)
            .extrude(TRAY_WALL_THICKNESS + 2)
            .translate((x_offset, TRAY_LENGTH / 2 - TRAY_WALL_THICKNESS / 2, TRAY_FLOOR_THICKNESS + 10))
        )
        tray = tray.cut(pin_hole)

    return tray


def make_lanyard_anchors(tray):
    """Add lanyard anchor holes with backing plate recesses.

    Each anchor uses an M4 stainless through-bolt with a 15mm square
    backing plate (2mm thick stainless steel) recessed into the tray floor.
    """
    for corner in [
        (-TRAY_WIDTH / 2 + LANYARD_ANCHOR_OFFSET, -TRAY_LENGTH / 2 + LANYARD_ANCHOR_OFFSET),
        (TRAY_WIDTH / 2 - LANYARD_ANCHOR_OFFSET, -TRAY_LENGTH / 2 + LANYARD_ANCHOR_OFFSET),
    ]:
        # Through-bolt hole (M4)
        tray = (
            tray.faces(">Z")
            .workplane()
            .center(corner[0], corner[1])
            .hole(LANYARD_BOLT_DIA, TRAY_WALL_THICKNESS + TRAY_FLOOR_THICKNESS)
        )

        # Backing plate recess on the underside of the tray floor
        recess = (
            cq.Workplane("XY")
            .rect(LANYARD_BACKING_PLATE_SIZE, LANYARD_BACKING_PLATE_SIZE)
            .extrude(LANYARD_BACKING_PLATE_THICKNESS)
            .translate((corner[0], corner[1], -LANYARD_BACKING_PLATE_THICKNESS))
        )
        tray = tray.cut(recess)

    return tray


def make_payload_tray():
    """Assemble the complete payload tray."""
    tray = make_tray_body()
    left_lip, right_lip = make_dovetail_lips()

    # Union lips to tray body
    tray = tray.union(left_lip).union(right_lip)

    # Add features
    tray = make_detent_holes(tray)
    tray = make_connector_cutout(tray)
    tray = make_lanyard_anchors(tray)

    return tray


if __name__ == "__main__":
    tray = make_payload_tray()

    export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
    os.makedirs(export_dir, exist_ok=True)

    step_path = os.path.join(export_dir, "payload_tray.step")
    stl_path = os.path.join(export_dir, "payload_tray.stl")

    cq.exporters.export(tray, step_path)
    cq.exporters.export(tray, stl_path)

    print(f"Exported: {step_path}")
    print(f"Exported: {stl_path}")
    print(f"Tray: {TRAY_WIDTH}×{TRAY_LENGTH}×{TRAY_DEPTH}mm internal")
    print(f"Lip profile: {TRAY_LIP_TOP_WIDTH}mm top × {TRAY_LIP_BASE_WIDTH}mm base × {TRAY_LIP_HEIGHT}mm")
