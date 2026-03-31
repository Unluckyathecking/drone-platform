"""MPE intelligence sub-package.

Re-exports the analysis and correlation layer.

Modules grouped here:
- track_manager: multi-source entity fusion
- classifier: rule-based threat/affiliation scoring
- alerts: alert rules + CoT alert generation
- geofence: polygon zone checks + violation events
- predictor: dead-reckoning trajectory + geofence entry prediction
- pattern_of_life: behavioural baseline + deviation detection
- health: ingest source health monitoring
"""

import importlib.util as _ilu
import pathlib as _pl

# intelligence.py sits alongside this package directory; import it directly
# to avoid shadowing by this package.
_spec = _ilu.spec_from_file_location(
    "mpe._intelligence_module",
    _pl.Path(__file__).parent.parent / "intelligence.py",
)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
IntelligenceEngine = _mod.IntelligenceEngine
generate_sitrep_template = _mod.generate_sitrep_template
SITREP_TEMPLATE = _mod.SITREP_TEMPLATE

from mpe.alerts import AlertEngine, AlertEvent, AlertRule
from mpe.classifier import EntityClassifier
from mpe.geofence import DEMO_ZONES, GeofenceManager, GeofenceViolation, GeofenceZone
from mpe.health import HealthMonitor
from mpe.pattern_of_life import PatternOfLifeAnalyser
from mpe.predictor import PredictedPosition, TrajectoryForecast, TrajectoryPredictor
from mpe.track_manager import Observation, TrackedEntity, TrackManager

__all__ = [
    # Fusion
    "Observation",
    "TrackedEntity",
    "TrackManager",
    # Classification
    "EntityClassifier",
    # Alerts
    "AlertEngine",
    "AlertEvent",
    "AlertRule",
    # Geofence
    "DEMO_ZONES",
    "GeofenceManager",
    "GeofenceViolation",
    "GeofenceZone",
    # Prediction
    "PredictedPosition",
    "TrajectoryForecast",
    "TrajectoryPredictor",
    # Pattern of life
    "PatternOfLifeAnalyser",
    # Health
    "HealthMonitor",
    # LLM intelligence
    "IntelligenceEngine",
    "generate_sitrep_template",
    "SITREP_TEMPLATE",
]
