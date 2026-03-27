"""Cursor on Target (CoT) type code constants.

CoT uses a hierarchical dot-separated type system:
  a = atom (position report), b = bit (information)
  f/h/u = friend/hostile/unknown
  A = air, M = military, F = fixed-wing, Q = UAV (drone)

Reference: MIL-STD-2525D / CoT Event Schemata
"""

from __future__ import annotations

from mpe.models import MAVCmd

# ---------------------------------------------------------------------------
# Atom types (position reports)
# ---------------------------------------------------------------------------
FRIENDLY_UAV_FIXEDWING = "a-f-A-M-F-Q"
HOSTILE_UAV = "a-h-A-M-F-Q"
UNKNOWN_AIR = "a-u-A"

# ---------------------------------------------------------------------------
# Bit types (information / map objects)
# ---------------------------------------------------------------------------
WAYPOINT = "b-m-p-w"
TARGET = "b-m-p-s-p-tgt"
POI = "b-m-p-s-p-POI"
ALERT = "b-a-o-tbl"

# ---------------------------------------------------------------------------
# Mapping from MAVCmd to CoT type codes
# ---------------------------------------------------------------------------
MAVCMD_TO_COT: dict[MAVCmd, str] = {
    MAVCmd.NAV_WAYPOINT: WAYPOINT,
    MAVCmd.NAV_TAKEOFF: WAYPOINT,
    MAVCmd.NAV_RETURN_TO_LAUNCH: WAYPOINT,
}
