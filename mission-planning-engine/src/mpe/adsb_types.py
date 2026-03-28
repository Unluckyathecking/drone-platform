"""ADS-B aircraft category to CoT 2525 type mapping.

Maps ADS-B emitter category codes to MIL-STD-2525D Cursor on Target type
strings for display on ATAK / WinTAK.

ADS-B categories are defined by RTCA DO-260B / EUROCAE ED-102A and transmitted
in the aircraft's ADS-B out messages (Type Code 4 in Extended Squitter).
"""

from __future__ import annotations

# CoT base types for airborne entities
COMMERCIAL_FIXED = "a-n-A-C-F"     # Neutral civilian fixed-wing
COMMERCIAL_HELI = "a-n-A-C-H"      # Neutral civilian helicopter
MILITARY_FIXED = "a-f-A-M-F"       # Friendly military fixed-wing
MILITARY_HELI = "a-f-A-M-H"        # Friendly military helicopter
UNKNOWN_AIR = "a-u-A"              # Unknown air
LIGHT_AIRCRAFT = "a-n-A-C-F"       # Light GA = civilian fixed
GLIDER = "a-n-A-C-F"              # Glider = civilian fixed
UAV_AIR = "a-n-A-M-F-Q"           # UAV


def adsb_category_to_cot(category: str | None) -> str:
    """Map ADS-B emitter category to CoT type string.

    ADS-B categories (from readsb/dump1090):
      A0-A7: Aircraft categories
        A1 = light (<15500 lbs)
        A2 = small (15500-75000 lbs)
        A3 = large (75000-300000 lbs)
        A4 = high vortex large (e.g. B757)
        A5 = heavy (>300000 lbs)
        A6 = high performance (>5g, >400 kts)
        A7 = rotorcraft
      B0-B7: Non-aircraft
        B1 = glider / sailplane
        B2 = lighter-than-air
        B4 = skydiver
        B6 = UAV
      C0-C7: Reserved

    Parameters
    ----------
    category:
        ADS-B emitter category string (e.g. ``"A3"``, ``"B6"``).
        ``None`` maps to unknown air.

    Returns
    -------
    str
        CoT type string suitable for the ``<event type="...">`` attribute.
    """
    if category is None:
        return UNKNOWN_AIR

    cat = str(category).upper()

    if cat in ("A7",):                    # Rotorcraft
        return COMMERCIAL_HELI
    elif cat in ("B6",):                  # UAV
        return UAV_AIR
    elif cat in ("B1",):                  # Glider
        return GLIDER
    elif cat in ("A1", "A2"):             # Light / Small
        return LIGHT_AIRCRAFT
    elif cat in ("A3", "A4", "A5"):       # Large / High-vortex / Heavy
        return COMMERCIAL_FIXED
    else:
        return UNKNOWN_AIR
