"""Alert engine -- turns classifications into actionable CoT alerts.

When the classifier flags an entity (threat_level >= threshold), the alert
engine generates a CoT alert event and queues it for transmission to TAK.
Operators see these as pop-up alerts on their ATAK tablets.

Alert types:
- EMERGENCY: squawk 7500/7600/7700, threat_level >= 9
- THREAT: hostile/suspect classification, threat_level >= 7
- ANOMALY: spoofing, unusual speed, etc., threat_level >= 4
- INFO: new entity detected, classification change
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
import logging

logger = logging.getLogger("mpe.alerts")


@dataclass
class AlertRule:
    """A configurable alert rule.

    Rules are evaluated against Classification results.
    All conditions must be true (AND logic) for the rule to fire.
    """

    name: str
    alert_type: str = "threat"          # emergency, threat, anomaly, info
    min_threat_level: int = 7           # Minimum threat level to trigger
    domains: list[str] | None = None    # Filter by domain (air, sea, None=all)
    affiliations: list[str] | None = None  # Filter by affiliation
    anomaly_types: list[str] | None = None  # Filter by specific anomaly types
    cooldown_seconds: int = 300         # Don't re-alert for same entity within this window
    severity: int = 7                   # Alert severity (1-10)
    enabled: bool = True


@dataclass
class AlertEvent:
    """A generated alert ready for dispatch."""

    alert_id: str
    entity_id: str
    alert_type: str
    severity: int
    title: str
    description: str
    latitude: float = 0.0
    longitude: float = 0.0
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    rule_name: str = ""
    cot_xml: str = ""  # Pre-generated CoT XML


# Default alert rules
DEFAULT_RULES: list[AlertRule] = [
    AlertRule(
        name="hijack",
        alert_type="emergency",
        min_threat_level=10,
        severity=10,
        cooldown_seconds=60,
    ),
    AlertRule(
        name="emergency_squawk",
        alert_type="emergency",
        min_threat_level=8,
        anomaly_types=["emergency"],
        severity=9,
        cooldown_seconds=120,
    ),
    AlertRule(
        name="high_threat",
        alert_type="threat",
        min_threat_level=7,
        severity=7,
        cooldown_seconds=300,
    ),
    AlertRule(
        name="ais_spoofing",
        alert_type="anomaly",
        min_threat_level=4,
        anomaly_types=["position_jump"],
        severity=6,
        cooldown_seconds=600,
    ),
    AlertRule(
        name="speed_anomaly",
        alert_type="anomaly",
        min_threat_level=4,
        anomaly_types=["excessive_speed"],
        severity=5,
        cooldown_seconds=600,
    ),
    AlertRule(
        name="military_vessel_detected",
        alert_type="info",
        min_threat_level=4,
        domains=["sea"],
        severity=4,
        cooldown_seconds=3600,
    ),
]


class AlertEngine:
    """Evaluates classifications against rules and generates alerts.

    Usage:
        engine = AlertEngine(rules=DEFAULT_RULES)
        alerts = engine.evaluate(entity_id, classification, domain, lat, lon)
        for alert in alerts:
            # send alert.cot_xml to TAK
    """

    def __init__(self, rules: list[AlertRule] | None = None) -> None:
        self._rules = list(DEFAULT_RULES) if rules is None else list(rules)
        self._cooldowns: dict[str, datetime] = {}  # "rule_name:entity_id" -> last alert time
        self._alert_counter = 0

    def evaluate(
        self,
        entity_id: str,
        classification: object,  # Classification from classifier.py
        domain: str = "air",
        latitude: float = 0.0,
        longitude: float = 0.0,
        callsign: str = "",
    ) -> list[AlertEvent]:
        """Evaluate a classification against all rules. Returns triggered alerts."""
        alerts: list[AlertEvent] = []
        now = datetime.now(timezone.utc)

        for rule in self._rules:
            if not rule.enabled:
                continue

            # Check threat level
            if classification.threat_level < rule.min_threat_level:
                continue

            # Check domain filter
            if rule.domains and domain not in rule.domains:
                continue

            # Check affiliation filter
            if rule.affiliations and classification.affiliation not in rule.affiliations:
                continue

            # Check anomaly type filter
            if rule.anomaly_types:
                anomaly_types_present = {
                    a.anomaly_type for a in classification.anomalies
                }
                if not anomaly_types_present.intersection(rule.anomaly_types):
                    continue

            # Check cooldown
            cooldown_key = f"{rule.name}:{entity_id}"
            last_fired = self._cooldowns.get(cooldown_key)
            if last_fired and (now - last_fired).total_seconds() < rule.cooldown_seconds:
                continue

            # Rule triggered -- generate alert
            self._alert_counter += 1
            alert_id = f"ALERT-{self._alert_counter:06d}"

            title = self._generate_title(rule, entity_id, classification, callsign)
            description = self._generate_description(classification)

            # FIX #2: Build AlertEvent once, then set cot_xml on the existing object
            alert = AlertEvent(
                alert_id=alert_id,
                entity_id=entity_id,
                alert_type=rule.alert_type,
                severity=rule.severity,
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                rule_name=rule.name,
            )
            alert.cot_xml = self._generate_cot_alert(alert)

            alerts.append(alert)
            self._cooldowns[cooldown_key] = now

            logger.warning("ALERT [%s] %s", rule.alert_type.upper(), title)

        return alerts

    def _generate_title(
        self,
        rule: AlertRule,
        entity_id: str,
        classification: object,
        callsign: str,
    ) -> str:
        name = callsign or entity_id
        if rule.alert_type == "emergency":
            reasoning_first = (
                classification.reasoning[0]
                if classification.reasoning
                else "Unknown"
            )
            return f"EMERGENCY: {name} — {reasoning_first}"
        elif rule.alert_type == "threat":
            return (
                f"THREAT: {name} classified {classification.affiliation} "
                f"(level {classification.threat_level})"
            )
        elif rule.alert_type == "anomaly":
            anomaly_desc = (
                classification.anomalies[0].description
                if classification.anomalies
                else "Unknown anomaly"
            )
            return f"ANOMALY: {name} — {anomaly_desc}"
        else:
            reasoning_first = (
                classification.reasoning[0]
                if classification.reasoning
                else "Detected"
            )
            return f"INFO: {name} — {reasoning_first}"

    def _generate_description(self, classification: object) -> str:
        parts: list[str] = []
        parts.append(f"Affiliation: {classification.affiliation}")
        parts.append(
            f"Threat level: {classification.threat_level}/10 "
            f"({classification.threat_category})"
        )
        if classification.anomalies:
            parts.append("Anomalies:")
            for a in classification.anomalies:
                parts.append(f"  - {a.anomaly_type}: {a.description}")
        if classification.reasoning:
            parts.append("Reasoning:")
            for r in classification.reasoning:
                parts.append(f"  - {r}")
        return "\n".join(parts)

    def _generate_cot_alert(self, alert: AlertEvent) -> str:
        """Generate a CoT alert event that appears as an alert on ATAK.

        CoT type "b-a-o-tbl" = alert.
        The <remarks> field carries the alert text.
        """
        now = datetime.now(tz=timezone.utc)
        time_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Stale time depends on severity
        stale_minutes = {10: 60, 9: 30, 8: 20, 7: 15}.get(alert.severity, 10)
        stale_str = (now + timedelta(minutes=stale_minutes)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Alert type mapping
        type_map = {
            "emergency": "b-a-o-tbl",    # Alert
            "threat": "b-a-o-tbl",        # Alert
            "anomaly": "b-a-o-can",       # Caution
            "info": "b-a-o-opn",          # Info
        }
        cot_type = type_map.get(alert.alert_type, "b-a-o-tbl")

        event = ET.Element("event", attrib={
            "version": "2.0",
            "type": cot_type,
            "uid": alert.alert_id,
            "how": "h-g-i-g-o",  # human-generated-information-general-observation
            "time": time_str,
            "start": time_str,
            "stale": stale_str,
        })

        ET.SubElement(event, "point", attrib={
            "lat": str(alert.latitude),
            "lon": str(alert.longitude),
            "hae": "0.0",
            "ce": "9999999",
            "le": "9999999",
        })

        detail = ET.SubElement(event, "detail")
        ET.SubElement(detail, "contact", attrib={
            "callsign": alert.title[:40],
        })

        remarks = ET.SubElement(detail, "remarks")
        remarks.text = alert.description

        # Link to the entity that triggered the alert
        if alert.entity_id:
            ET.SubElement(detail, "link", attrib={
                "uid": alert.entity_id,
                "type": "a-f-A",
                "relation": "p-s",  # parent-subject
            })

        return ET.tostring(event, encoding="unicode", xml_declaration=False)

    @property
    def active_rules(self) -> list[AlertRule]:
        """Return only enabled rules."""
        return [r for r in self._rules if r.enabled]

    @property
    def alert_count(self) -> int:
        """Total number of alerts generated since construction."""
        return self._alert_counter

    def clear_cooldowns(self) -> None:
        """Reset all cooldowns (useful for testing)."""
        self._cooldowns.clear()
