"""MPE ingest sub-package.

Re-exports all ingest-layer components so that both the canonical flat import
path (``from mpe.adsb_receiver import ADSBReceiver``) and the sub-package path
(``from mpe.ingest import ADSBReceiver``) work without moving any files.

Modules grouped here:
- ADS-B: receiver, tracker, type mapping
- AIS: receiver, tracker, type mapping
- CoT inbound: receiver + parser
"""

from mpe.adsb_receiver import ADSBReceiver
from mpe.adsb_types import adsb_category_to_cot
from mpe.aircraft_tracker import AircraftTrack, AircraftTracker
from mpe.ais_receiver import AISReceiver
from mpe.ais_types import ais_type_to_cot
from mpe.cot_receiver import CotReceiver
from mpe.vessel_tracker import VesselTrack, VesselTracker

__all__ = [
    # ADS-B
    "ADSBReceiver",
    "adsb_category_to_cot",
    "AircraftTrack",
    "AircraftTracker",
    # AIS
    "AISReceiver",
    "ais_type_to_cot",
    "VesselTrack",
    "VesselTracker",
    # CoT inbound
    "CotReceiver",
]
