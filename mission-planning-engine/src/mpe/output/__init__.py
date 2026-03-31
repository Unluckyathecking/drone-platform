"""MPE output sub-package.

Re-exports all outbound data components.

Modules grouped here:
- cot_output: plain-socket CoT sender (UDP/TCP)
- cot_sender: PyTAK-based async CoT streaming
- cot_types: CoT type code constants
- adsb_cot_bridge: AircraftTrack → CoT XML
- ais_cot_bridge: VesselTrack → CoT XML
- task_to_cot: Task/Entity → CoT XML
- writers: MissionWriter ABC, QGCWPLWriter, CoTWriter
"""

from mpe.adsb_cot_bridge import ADSBCoTBridge
from mpe.ais_cot_bridge import AISCoTBridge
from mpe.cot_output import CoTOutput
from mpe.cot_sender import CoTStreamer
from mpe.cot_types import MAVCMD_TO_COT
from mpe.task_to_cot import CoTTranslator
from mpe.writers import CoTWriter, MissionWriter, QGCWPLWriter

__all__ = [
    # Bridges
    "ADSBCoTBridge",
    "AISCoTBridge",
    # Senders
    "CoTOutput",
    "CoTStreamer",
    # Types
    "MAVCMD_TO_COT",
    # Translators
    "CoTTranslator",
    # Writers
    "CoTWriter",
    "MissionWriter",
    "QGCWPLWriter",
]
