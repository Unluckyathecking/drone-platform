"""AIS vessel type codes to CoT 2525 type mapping.

Maps AIS ship/vessel type codes (0-99) from ITU-R M.1371 to MIL-STD-2525D
Cursor on Target type strings for display on ATAK / WinTAK.
"""

from __future__ import annotations

# CoT base types for surface vessels
FRIENDLY_SURFACE = "a-f-S"
NEUTRAL_SURFACE = "a-n-S"
UNKNOWN_SURFACE = "a-u-S"
HOSTILE_SURFACE = "a-h-S"
SUSPECT_SURFACE = "a-j-S"

# Vessel category sub-types (neutral affiliation for commercial)
CARGO = "a-n-S-X-C"
TANKER = "a-n-S-X-T"
PASSENGER = "a-n-S-X-P"
FISHING = "a-n-S-X-F"
MILITARY = "a-u-S-W"        # Unknown affiliation until classified
SAR_VESSEL = "a-f-S"        # SAR = friendly by default
LAW_ENFORCEMENT = "a-f-S"


def ais_type_to_cot(ais_ship_type: int) -> str:
    """Map AIS ship type code (0-99) to CoT type string.

    AIS ship type ranges are defined in ITU-R M.1371-5 Table 53.
    Default is neutral surface (a-n-S) for unrecognised commercial vessels.

    Parameters
    ----------
    ais_ship_type:
        Integer 0-99 from AIS message type 5 or 24 ``shiptype`` field.

    Returns
    -------
    str
        CoT type string suitable for the ``<event type="...">`` attribute.
    """
    if ais_ship_type == 0:
        return UNKNOWN_SURFACE
    elif ais_ship_type == 35:
        return MILITARY
    elif 30 <= ais_ship_type <= 39:
        return FISHING
    elif ais_ship_type == 51:
        return SAR_VESSEL
    elif ais_ship_type == 55:
        return LAW_ENFORCEMENT
    elif 60 <= ais_ship_type <= 69:
        return PASSENGER
    elif 70 <= ais_ship_type <= 79:
        return CARGO
    elif 80 <= ais_ship_type <= 89:
        return TANKER
    else:
        return NEUTRAL_SURFACE
