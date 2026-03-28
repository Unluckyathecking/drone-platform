"""Entity auto-classifier -- rule-based classification of tracks.

Applies configurable rules to observable attributes (position, speed,
heading, type, behaviour history) to classify entities and detect anomalies.

This is the intelligence layer -- it turns raw sensor data into:
- Affiliation assessment (friendly/neutral/hostile/suspect/unknown)
- Threat level (0-10)
- Anomaly flags with reasoning
- Confidence scores

Designed as rule-based first, upgradeable to ML later.  The classifier is
duck-typed: it works with any object that exposes the expected attributes
(VesselTrack, SimpleNamespace, dict-wrapper, etc.).  This keeps it decoupled
from specific data models and easy to wire into tracker update loops.

Future ML upgrade path:
    1. Collect classification decisions as training data
    2. Train a lightweight model (e.g. gradient-boosted tree) on features
    3. Replace individual rule methods with model.predict()
    4. Keep rule engine as fallback / explainability layer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


# ---------------------------------------------------------------------------
# Enums & value objects
# ---------------------------------------------------------------------------


class ThreatLevel(StrEnum):
    """Qualitative threat category mapped from numeric 0-10 scale."""

    NONE = "none"           # 0 - Known friendly, no concern
    LOW = "low"             # 1-3 - Normal commercial traffic
    MEDIUM = "medium"       # 4-6 - Unusual but not threatening
    HIGH = "high"           # 7-8 - Suspicious, warrants attention
    CRITICAL = "critical"   # 9-10 - Immediate threat or emergency


@dataclass(frozen=True)
class Anomaly:
    """A detected anomaly on a track.

    Immutable so anomalies can be safely stored, compared, and logged.
    """

    anomaly_type: str           # e.g. "ais_spoofing", "excessive_speed"
    description: str            # Human-readable explanation
    confidence: float = 1.0     # 0.0-1.0
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


@dataclass
class Classification:
    """Result of classifying an entity.

    Contains the affiliation assessment, numeric threat level (0-10),
    qualitative threat category, any detected anomalies, and a chain
    of reasoning strings that explain how the classification was reached.
    """

    affiliation: str = "unknown"    # friendly/hostile/neutral/suspect/unknown
    threat_level: int = 0           # 0-10
    threat_category: str = "none"   # ThreatLevel value
    anomalies: list[Anomaly] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)
    confidence: float = 0.5         # Overall classification confidence
    classified_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @property
    def is_suspect(self) -> bool:
        """True if the entity is assessed as hostile/suspect or high threat."""
        return self.affiliation in ("hostile", "suspect") or self.threat_level >= 7

    @property
    def has_anomalies(self) -> bool:
        """True if any anomalies were detected."""
        return len(self.anomalies) > 0


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------


class EntityClassifier:
    """Rule-based entity classifier.

    Configurable with known-entity lists and threshold parameters.
    All rules are deterministic and explainable -- every classification
    comes with a reasoning chain.

    Parameters
    ----------
    known_friendly_mmsis:
        Set of vessel MMSIs known to be friendly (e.g. own fleet).
    known_hostile_mmsis:
        Set of vessel MMSIs on a threat list.
    known_friendly_icaos:
        Set of aircraft ICAO hex addresses known to be friendly.
    max_cargo_speed_kts:
        Speed above which a cargo vessel is flagged (AIS type 70-79).
    max_tanker_speed_kts:
        Speed above which a tanker is flagged (AIS type 80-89).
    position_jump_km:
        Distance threshold for AIS spoofing detection between updates.
    loiter_radius_km:
        Radius within which repeated circling counts as loitering.

    ML upgrade notes
    ----------------
    Each ``classify_*`` method returns a ``Classification`` with reasoning.
    To upgrade to ML: replace individual rule blocks with feature extraction
    + model inference, keep the Classification output contract unchanged.
    """

    def __init__(
        self,
        known_friendly_mmsis: set[int] | None = None,
        known_hostile_mmsis: set[int] | None = None,
        known_friendly_icaos: set[str] | None = None,
        max_cargo_speed_kts: float = 25.0,
        max_tanker_speed_kts: float = 20.0,
        position_jump_km: float = 50.0,
        loiter_radius_km: float = 2.0,
    ) -> None:
        self._friendly_mmsis: frozenset[int] = frozenset(
            known_friendly_mmsis or (),
        )
        self._hostile_mmsis: frozenset[int] = frozenset(
            known_hostile_mmsis or (),
        )
        self._friendly_icaos: frozenset[str] = frozenset(
            known_friendly_icaos or (),
        )
        self._max_cargo_speed = max_cargo_speed_kts
        self._max_tanker_speed = max_tanker_speed_kts
        self._position_jump_km = position_jump_km
        self._loiter_radius_km = loiter_radius_km

    # -- Vessel classification ------------------------------------------------

    def classify_vessel(
        self,
        track: object,
        previous_track: object | None = None,
    ) -> Classification:
        """Classify a vessel track.

        Args:
            track: Any object with attributes ``mmsi``, ``latitude``,
                ``longitude``, ``speed_over_ground``, ``course_over_ground``,
                ``ship_type``, ``vessel_name``, ``nav_status``.
            previous_track: Previous state of the same vessel (for detecting
                position jumps / spoofing).

        Returns:
            Classification with affiliation, threat level, anomalies,
            and reasoning chain.
        """
        result = Classification()

        # Rule 1: Known-entity lists
        mmsi = getattr(track, "mmsi", 0)
        if mmsi in self._friendly_mmsis:
            result.affiliation = "friendly"
            result.threat_level = 0
            result.reasoning.append(f"MMSI {mmsi} in known friendly list")
            result.confidence = 0.95
        elif mmsi in self._hostile_mmsis:
            result.affiliation = "hostile"
            result.threat_level = 9
            result.reasoning.append(f"MMSI {mmsi} in known hostile list")
            result.confidence = 0.95
        else:
            result.affiliation = "neutral"
            result.threat_level = 1
            result.reasoning.append(
                "Default classification: neutral commercial traffic",
            )

        # Rule 2: Ship type classification
        ship_type = getattr(track, "ship_type", 0)
        if ship_type == 35:  # Military operations
            if result.affiliation == "neutral":
                result.affiliation = "unknown"
                result.threat_level = max(result.threat_level, 5)
                result.reasoning.append(
                    "AIS ship type 35 (military operations)",
                )
        elif ship_type == 55:  # Law enforcement
            result.affiliation = "friendly"
            result.threat_level = 0
            result.reasoning.append("Law enforcement vessel")
        elif ship_type == 51:  # SAR
            result.affiliation = "friendly"
            result.threat_level = 0
            result.reasoning.append("Search and rescue vessel")

        # Rule 3: Speed anomaly
        speed = getattr(track, "speed_over_ground", 0.0) or 0.0
        if 70 <= ship_type <= 79 and speed > self._max_cargo_speed:
            result.anomalies.append(Anomaly(
                anomaly_type="excessive_speed",
                description=(
                    f"Cargo vessel at {speed:.1f} kts "
                    f"(max expected {self._max_cargo_speed})"
                ),
                confidence=0.8,
            ))
            result.threat_level = max(result.threat_level, 4)
            result.reasoning.append(
                f"Speed anomaly: {speed:.1f} kts exceeds cargo threshold",
            )
        elif 80 <= ship_type <= 89 and speed > self._max_tanker_speed:
            result.anomalies.append(Anomaly(
                anomaly_type="excessive_speed",
                description=(
                    f"Tanker at {speed:.1f} kts "
                    f"(max expected {self._max_tanker_speed})"
                ),
                confidence=0.8,
            ))
            result.threat_level = max(result.threat_level, 4)
            result.reasoning.append(
                f"Speed anomaly: tanker at {speed:.1f} kts",
            )

        # Rule 4: Position jump (spoofing detection)
        if previous_track is not None:
            self._check_position_jump(
                track, previous_track, result, self._position_jump_km,
            )

        # Rule 5: Missing name on large vessel (suspicious)
        vessel_name = getattr(track, "vessel_name", "")
        if not vessel_name and ship_type >= 60:
            result.anomalies.append(Anomaly(
                anomaly_type="missing_identity",
                description="Large vessel with no AIS name broadcast",
                confidence=0.6,
            ))
            result.threat_level = max(result.threat_level, 3)
            result.reasoning.append(
                "Missing vessel name for large vessel type",
            )

        # Final: set qualitative threat category
        result.threat_category = _threat_level_to_category(result.threat_level)

        return result

    # -- Aircraft classification ----------------------------------------------

    def classify_aircraft(
        self,
        track: object,
        previous_track: object | None = None,
    ) -> Classification:
        """Classify an aircraft track.

        Args:
            track: Any object with attributes ``icao_hex``, ``callsign``,
                ``altitude_baro_ft``, ``ground_speed_kts``, ``heading``,
                ``squawk``, ``category``, ``on_ground``.
            previous_track: Previous state of the same aircraft (reserved
                for future anomaly detection such as ADS-B disappearance).

        Returns:
            Classification with affiliation, threat level, anomalies,
            and reasoning chain.
        """
        result = Classification()

        # Rule 1: Known-entity lists
        icao = getattr(track, "icao_hex", "").upper()
        if icao in self._friendly_icaos:
            result.affiliation = "friendly"
            result.threat_level = 0
            result.reasoning.append(f"ICAO {icao} in known friendly list")
            result.confidence = 0.95
        else:
            result.affiliation = "neutral"
            result.threat_level = 1
            result.reasoning.append("Default: neutral air traffic")

        # Rule 2: Emergency squawk codes
        squawk = getattr(track, "squawk", "")
        if squawk == "7700":
            result.anomalies.append(Anomaly(
                anomaly_type="emergency",
                description="Squawk 7700: General emergency",
                confidence=1.0,
            ))
            result.threat_level = max(result.threat_level, 8)
            result.threat_category = "critical"
            result.reasoning.append("EMERGENCY: Squawk 7700")
        elif squawk == "7600":
            result.anomalies.append(Anomaly(
                anomaly_type="emergency",
                description="Squawk 7600: Communications failure",
                confidence=1.0,
            ))
            result.threat_level = max(result.threat_level, 6)
            result.reasoning.append("COMMS FAILURE: Squawk 7600")
        elif squawk == "7500":
            result.anomalies.append(Anomaly(
                anomaly_type="emergency",
                description="Squawk 7500: HIJACK",
                confidence=1.0,
            ))
            result.affiliation = "hostile"
            result.threat_level = 10
            result.threat_category = "critical"
            result.reasoning.append("HIJACK: Squawk 7500")

        # Rule 3: Military ICAO address ranges
        if icao and len(icao) == 6:
            try:
                icao_int = int(icao, 16)
                # UK military ICAO range (approximate)
                if 0x43C000 <= icao_int <= 0x43CFFF:
                    result.affiliation = "friendly"
                    result.reasoning.append("UK military ICAO range")
                # US military ICAO range (approximate)
                elif 0xADF7C8 <= icao_int <= 0xAFFFFF:
                    result.affiliation = "friendly"
                    result.reasoning.append("US military ICAO range")
            except ValueError:
                pass

        # Rule 4: Very low altitude (potential drone / threat)
        alt = getattr(track, "altitude_baro_ft", 0) or 0
        on_ground = getattr(track, "on_ground", False)
        if 0 < alt < 500 and not on_ground:
            result.anomalies.append(Anomaly(
                anomaly_type="low_altitude",
                description=f"Aircraft at {alt} ft AGL (very low)",
                confidence=0.7,
            ))
            result.threat_level = max(result.threat_level, 4)
            result.reasoning.append(f"Low altitude alert: {alt} ft")

        # Final: set qualitative threat category
        result.threat_category = _threat_level_to_category(result.threat_level)

        return result

    # -- Internal helpers -----------------------------------------------------

    @staticmethod
    def _check_position_jump(
        track: object,
        previous_track: object,
        result: Classification,
        threshold_km: float = 50.0,
    ) -> None:
        """Detect impossible position jumps (potential AIS spoofing)."""
        prev_lat = getattr(previous_track, "latitude", 0.0)
        prev_lon = getattr(previous_track, "longitude", 0.0)
        curr_lat = getattr(track, "latitude", 0.0)
        curr_lon = getattr(track, "longitude", 0.0)

        if not (prev_lat and prev_lon and curr_lat and curr_lon):
            return

        try:
            from mpe.planner import _haversine_km
            from mpe.models import Coordinate

            dist = _haversine_km(
                Coordinate(latitude=prev_lat, longitude=prev_lon),
                Coordinate(latitude=curr_lat, longitude=curr_lon),
            )
        except ImportError:
            return

        if dist > threshold_km:
            result.anomalies.append(Anomaly(
                anomaly_type="position_jump",
                description=(
                    f"Position jumped {dist:.1f} km (possible spoofing)"
                ),
                confidence=0.9,
            ))
            result.affiliation = "suspect"
            result.threat_level = max(result.threat_level, 7)
            result.reasoning.append(
                f"Position jump of {dist:.1f} km detected "
                f"(threshold: {threshold_km} km)",
            )


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def _threat_level_to_category(level: int) -> str:
    """Map numeric threat level (0-10) to qualitative category string."""
    if level == 0:
        return ThreatLevel.NONE
    elif level <= 3:
        return ThreatLevel.LOW
    elif level <= 6:
        return ThreatLevel.MEDIUM
    elif level <= 8:
        return ThreatLevel.HIGH
    else:
        return ThreatLevel.CRITICAL
