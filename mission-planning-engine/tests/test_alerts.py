"""Tests for the alert engine (mpe.alerts).

Covers: AlertRule defaults, AlertEngine evaluation, domain/anomaly/cooldown
filtering, CoT XML generation, severity mapping, and edge cases.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import pytest

from mpe.alerts import AlertEngine, AlertEvent, AlertRule, DEFAULT_RULES
from mpe.classifier import Anomaly, Classification


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _make_classification(
    affiliation: str = "hostile",
    threat_level: int = 8,
    threat_category: str = "high",
    anomalies: list[Anomaly] | None = None,
    reasoning: list[str] | None = None,
    confidence: float = 0.9,
) -> Classification:
    """Create a Classification with sensible test defaults."""
    return Classification(
        affiliation=affiliation,
        threat_level=threat_level,
        threat_category=threat_category,
        anomalies=anomalies or [],
        reasoning=reasoning or ["Test reasoning"],
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# AlertRule defaults
# ---------------------------------------------------------------------------


class TestAlertRuleDefaults:
    def test_default_alert_type(self):
        rule = AlertRule(name="test")
        assert rule.alert_type == "threat"

    def test_default_min_threat_level(self):
        rule = AlertRule(name="test")
        assert rule.min_threat_level == 7

    def test_default_domains_is_none(self):
        rule = AlertRule(name="test")
        assert rule.domains is None

    def test_default_affiliations_is_none(self):
        rule = AlertRule(name="test")
        assert rule.affiliations is None

    def test_default_anomaly_types_is_none(self):
        rule = AlertRule(name="test")
        assert rule.anomaly_types is None

    def test_default_cooldown_seconds(self):
        rule = AlertRule(name="test")
        assert rule.cooldown_seconds == 300

    def test_default_severity(self):
        rule = AlertRule(name="test")
        assert rule.severity == 7

    def test_default_enabled(self):
        rule = AlertRule(name="test")
        assert rule.enabled is True


# ---------------------------------------------------------------------------
# AlertEngine — no rules
# ---------------------------------------------------------------------------


class TestAlertEngineNoRules:
    def test_empty_rules_returns_no_alerts(self):
        engine = AlertEngine(rules=[])
        classification = _make_classification(threat_level=10)
        alerts = engine.evaluate("ENT-001", classification)
        assert alerts == []

    def test_alert_count_stays_zero(self):
        engine = AlertEngine(rules=[])
        classification = _make_classification(threat_level=10)
        engine.evaluate("ENT-001", classification)
        assert engine.alert_count == 0


# ---------------------------------------------------------------------------
# AlertEngine — threat triggering
# ---------------------------------------------------------------------------


class TestAlertEngineThreatTriggering:
    def test_high_threat_triggers_alert(self):
        rule = AlertRule(name="threat_rule", min_threat_level=7, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 1
        assert alerts[0].alert_type == "threat"
        assert alerts[0].severity == 7

    def test_below_threshold_does_not_trigger(self):
        rule = AlertRule(name="threat_rule", min_threat_level=7, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=5)
        alerts = engine.evaluate("ENT-001", classification)
        assert alerts == []

    def test_exact_threshold_triggers(self):
        rule = AlertRule(name="threat_rule", min_threat_level=7, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=7)
        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 1

    def test_emergency_squawk_generates_emergency_alert(self):
        rule = AlertRule(
            name="emergency",
            alert_type="emergency",
            min_threat_level=8,
            anomaly_types=["emergency"],
            severity=9,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            threat_level=10,
            anomalies=[
                Anomaly(
                    anomaly_type="emergency",
                    description="Squawk 7500: HIJACK",
                ),
            ],
            reasoning=["HIJACK: Squawk 7500"],
        )
        alerts = engine.evaluate("AC-7500", classification, callsign="BAW123")
        assert len(alerts) == 1
        assert alerts[0].alert_type == "emergency"
        assert alerts[0].severity == 9


# ---------------------------------------------------------------------------
# Domain filter
# ---------------------------------------------------------------------------


class TestAlertEngineDomainFilter:
    def test_sea_rule_does_not_fire_for_air(self):
        rule = AlertRule(
            name="sea_only",
            min_threat_level=4,
            domains=["sea"],
            severity=5,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=6)
        alerts = engine.evaluate("ENT-001", classification, domain="air")
        assert alerts == []

    def test_sea_rule_fires_for_sea(self):
        rule = AlertRule(
            name="sea_only",
            min_threat_level=4,
            domains=["sea"],
            severity=5,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=6)
        alerts = engine.evaluate("VES-001", classification, domain="sea")
        assert len(alerts) == 1

    def test_no_domain_filter_fires_for_any(self):
        rule = AlertRule(name="any_domain", min_threat_level=4, severity=5)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=6)
        alerts_air = engine.evaluate("ENT-001", classification, domain="air")
        engine.clear_cooldowns()
        alerts_sea = engine.evaluate("ENT-001", classification, domain="sea")
        assert len(alerts_air) == 1
        assert len(alerts_sea) == 1


# ---------------------------------------------------------------------------
# Anomaly type filter
# ---------------------------------------------------------------------------


class TestAlertEngineAnomalyFilter:
    def test_anomaly_type_matches(self):
        rule = AlertRule(
            name="spoofing",
            alert_type="anomaly",
            min_threat_level=4,
            anomaly_types=["position_jump"],
            severity=6,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            threat_level=7,
            anomalies=[
                Anomaly(
                    anomaly_type="position_jump",
                    description="Position jumped 120 km",
                ),
            ],
        )
        alerts = engine.evaluate("VES-001", classification)
        assert len(alerts) == 1
        assert alerts[0].alert_type == "anomaly"

    def test_anomaly_type_mismatch_does_not_fire(self):
        rule = AlertRule(
            name="spoofing",
            alert_type="anomaly",
            min_threat_level=4,
            anomaly_types=["position_jump"],
            severity=6,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            threat_level=7,
            anomalies=[
                Anomaly(
                    anomaly_type="excessive_speed",
                    description="Cargo at 35 kts",
                ),
            ],
        )
        alerts = engine.evaluate("VES-001", classification)
        assert alerts == []

    def test_no_anomalies_does_not_fire_anomaly_rule(self):
        rule = AlertRule(
            name="spoofing",
            alert_type="anomaly",
            min_threat_level=4,
            anomaly_types=["position_jump"],
            severity=6,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=7, anomalies=[])
        alerts = engine.evaluate("VES-001", classification)
        assert alerts == []


# ---------------------------------------------------------------------------
# Cooldown
# ---------------------------------------------------------------------------


class TestAlertEngineCooldown:
    def test_cooldown_prevents_realert(self):
        rule = AlertRule(
            name="threat_rule",
            min_threat_level=7,
            severity=7,
            cooldown_seconds=300,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)

        alerts1 = engine.evaluate("ENT-001", classification)
        assert len(alerts1) == 1

        # Second evaluation within cooldown
        alerts2 = engine.evaluate("ENT-001", classification)
        assert alerts2 == []

    def test_cooldown_expires_and_realerts(self):
        rule = AlertRule(
            name="threat_rule",
            min_threat_level=7,
            severity=7,
            cooldown_seconds=300,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)

        alerts1 = engine.evaluate("ENT-001", classification)
        assert len(alerts1) == 1

        # Manually expire the cooldown by backdating it
        key = "threat_rule:ENT-001"
        engine._cooldowns[key] = datetime.now(timezone.utc) - timedelta(seconds=301)

        alerts2 = engine.evaluate("ENT-001", classification)
        assert len(alerts2) == 1

    def test_cooldown_is_per_entity(self):
        rule = AlertRule(
            name="threat_rule",
            min_threat_level=7,
            severity=7,
            cooldown_seconds=300,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)

        alerts1 = engine.evaluate("ENT-001", classification)
        assert len(alerts1) == 1

        # Different entity should still fire
        alerts2 = engine.evaluate("ENT-002", classification)
        assert len(alerts2) == 1

    def test_clear_cooldowns_resets(self):
        rule = AlertRule(
            name="threat_rule",
            min_threat_level=7,
            severity=7,
            cooldown_seconds=300,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)

        engine.evaluate("ENT-001", classification)
        engine.clear_cooldowns()

        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 1


# ---------------------------------------------------------------------------
# CoT XML validation
# ---------------------------------------------------------------------------


class TestAlertCotXml:
    def _get_alert_cot(self, **classification_kwargs) -> str:
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(**classification_kwargs)
        alerts = engine.evaluate(
            "ENT-001",
            classification,
            latitude=51.3,
            longitude=-0.15,
        )
        assert len(alerts) == 1
        return alerts[0].cot_xml

    def test_cot_xml_is_valid(self):
        xml_str = self._get_alert_cot(threat_level=8)
        # Should parse without error
        root = ET.fromstring(xml_str)
        assert root.tag == "event"

    def test_cot_has_required_attributes(self):
        xml_str = self._get_alert_cot(threat_level=8)
        root = ET.fromstring(xml_str)
        assert root.get("version") == "2.0"
        assert root.get("type") is not None
        assert root.get("uid") is not None
        assert root.get("how") == "h-g-i-g-o"
        assert root.get("time") is not None
        assert root.get("start") is not None
        assert root.get("stale") is not None

    def test_cot_has_point_element(self):
        xml_str = self._get_alert_cot(threat_level=8)
        root = ET.fromstring(xml_str)
        point = root.find("point")
        assert point is not None
        assert point.get("lat") == "51.3"
        assert point.get("lon") == "-0.15"

    def test_cot_has_detail_contact(self):
        xml_str = self._get_alert_cot(threat_level=8)
        root = ET.fromstring(xml_str)
        contact = root.find("detail/contact")
        assert contact is not None
        assert contact.get("callsign") is not None

    def test_cot_has_remarks(self):
        xml_str = self._get_alert_cot(threat_level=8)
        root = ET.fromstring(xml_str)
        remarks = root.find("detail/remarks")
        assert remarks is not None
        assert remarks.text is not None
        assert "Affiliation:" in remarks.text

    def test_cot_has_link_to_entity(self):
        xml_str = self._get_alert_cot(threat_level=8)
        root = ET.fromstring(xml_str)
        link = root.find("detail/link")
        assert link is not None
        assert link.get("uid") == "ENT-001"
        assert link.get("relation") == "p-s"

    def test_cot_alert_type_is_tbl_for_threats(self):
        rule = AlertRule(
            name="threat_rule",
            alert_type="threat",
            min_threat_level=1,
            severity=7,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate("ENT-001", classification)
        root = ET.fromstring(alerts[0].cot_xml)
        assert root.get("type") == "b-a-o-tbl"

    def test_cot_alert_type_is_can_for_anomalies(self):
        rule = AlertRule(
            name="anomaly_rule",
            alert_type="anomaly",
            min_threat_level=1,
            severity=5,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=5)
        alerts = engine.evaluate("ENT-001", classification)
        root = ET.fromstring(alerts[0].cot_xml)
        assert root.get("type") == "b-a-o-can"

    def test_cot_alert_type_is_opn_for_info(self):
        rule = AlertRule(
            name="info_rule",
            alert_type="info",
            min_threat_level=1,
            severity=3,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=3)
        alerts = engine.evaluate("ENT-001", classification)
        root = ET.fromstring(alerts[0].cot_xml)
        assert root.get("type") == "b-a-o-opn"

    def test_cot_alert_type_is_tbl_for_emergency(self):
        rule = AlertRule(
            name="emerg_rule",
            alert_type="emergency",
            min_threat_level=1,
            severity=10,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=10)
        alerts = engine.evaluate("ENT-001", classification)
        root = ET.fromstring(alerts[0].cot_xml)
        assert root.get("type") == "b-a-o-tbl"


# ---------------------------------------------------------------------------
# Alert title and description
# ---------------------------------------------------------------------------


class TestAlertTitleDescription:
    def test_title_contains_callsign(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate(
            "ENT-001", classification, callsign="FOXTROT-1",
        )
        assert "FOXTROT-1" in alerts[0].title

    def test_title_falls_back_to_entity_id(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate("ENT-001", classification, callsign="")
        assert "ENT-001" in alerts[0].title

    def test_description_contains_reasoning(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            threat_level=8,
            reasoning=["Known hostile MMSI", "Speed anomaly detected"],
        )
        alerts = engine.evaluate("ENT-001", classification)
        assert "Known hostile MMSI" in alerts[0].description
        assert "Speed anomaly detected" in alerts[0].description

    def test_description_contains_affiliation(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            affiliation="suspect", threat_level=8,
        )
        alerts = engine.evaluate("ENT-001", classification)
        assert "suspect" in alerts[0].description

    def test_description_contains_anomalies(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            threat_level=8,
            anomalies=[
                Anomaly(
                    anomaly_type="excessive_speed",
                    description="Cargo at 35 kts",
                ),
            ],
        )
        alerts = engine.evaluate("ENT-001", classification)
        assert "excessive_speed" in alerts[0].description
        assert "Cargo at 35 kts" in alerts[0].description


# ---------------------------------------------------------------------------
# Multiple rules
# ---------------------------------------------------------------------------


class TestAlertEngineMultipleRules:
    def test_multiple_rules_fire_for_same_entity(self):
        rules = [
            AlertRule(name="rule_a", min_threat_level=7, severity=7),
            AlertRule(name="rule_b", min_threat_level=5, severity=5),
        ]
        engine = AlertEngine(rules=rules)
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 2
        rule_names = {a.rule_name for a in alerts}
        assert rule_names == {"rule_a", "rule_b"}

    def test_disabled_rule_does_not_fire(self):
        rules = [
            AlertRule(name="enabled_rule", min_threat_level=7, severity=7),
            AlertRule(
                name="disabled_rule",
                min_threat_level=7,
                severity=7,
                enabled=False,
            ),
        ]
        engine = AlertEngine(rules=rules)
        classification = _make_classification(threat_level=8)
        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 1
        assert alerts[0].rule_name == "enabled_rule"


# ---------------------------------------------------------------------------
# Alert counter
# ---------------------------------------------------------------------------


class TestAlertCounter:
    def test_alert_count_increments(self):
        rule = AlertRule(name="test_rule", min_threat_level=1, severity=7)
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=5)

        engine.evaluate("ENT-001", classification)
        assert engine.alert_count == 1

        engine.evaluate("ENT-002", classification)
        assert engine.alert_count == 2

    def test_alert_count_starts_at_zero(self):
        engine = AlertEngine(rules=[])
        assert engine.alert_count == 0

    def test_alert_ids_are_sequential(self):
        rule = AlertRule(
            name="test_rule",
            min_threat_level=1,
            severity=7,
            cooldown_seconds=0,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(threat_level=5)

        a1 = engine.evaluate("ENT-001", classification)
        a2 = engine.evaluate("ENT-002", classification)
        assert a1[0].alert_id == "ALERT-000001"
        assert a2[0].alert_id == "ALERT-000002"


# ---------------------------------------------------------------------------
# Active rules property
# ---------------------------------------------------------------------------


class TestActiveRules:
    def test_active_rules_excludes_disabled(self):
        rules = [
            AlertRule(name="on", enabled=True),
            AlertRule(name="off", enabled=False),
        ]
        engine = AlertEngine(rules=rules)
        assert len(engine.active_rules) == 1
        assert engine.active_rules[0].name == "on"

    def test_active_rules_with_all_enabled(self):
        rules = [AlertRule(name="a"), AlertRule(name="b")]
        engine = AlertEngine(rules=rules)
        assert len(engine.active_rules) == 2


# ---------------------------------------------------------------------------
# Default rules smoke test
# ---------------------------------------------------------------------------


class TestDefaultRules:
    def test_default_rules_are_populated(self):
        assert len(DEFAULT_RULES) >= 6

    def test_default_engine_uses_default_rules(self):
        engine = AlertEngine()
        assert len(engine.active_rules) == len(DEFAULT_RULES)

    def test_hijack_triggers_with_default_rules(self):
        engine = AlertEngine()
        classification = _make_classification(
            affiliation="hostile",
            threat_level=10,
            threat_category="critical",
            anomalies=[
                Anomaly(
                    anomaly_type="emergency",
                    description="Squawk 7500: HIJACK",
                ),
            ],
            reasoning=["HIJACK: Squawk 7500"],
        )
        alerts = engine.evaluate("AC-7500", classification, domain="air")
        # Should trigger at least hijack + emergency_squawk + high_threat
        assert len(alerts) >= 2
        alert_types = {a.alert_type for a in alerts}
        assert "emergency" in alert_types


# ---------------------------------------------------------------------------
# Affiliation filter
# ---------------------------------------------------------------------------


class TestAffiliationFilter:
    def test_affiliation_filter_matches(self):
        rule = AlertRule(
            name="hostile_only",
            min_threat_level=1,
            affiliations=["hostile"],
            severity=7,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            affiliation="hostile", threat_level=8,
        )
        alerts = engine.evaluate("ENT-001", classification)
        assert len(alerts) == 1

    def test_affiliation_filter_rejects_mismatch(self):
        rule = AlertRule(
            name="hostile_only",
            min_threat_level=1,
            affiliations=["hostile"],
            severity=7,
        )
        engine = AlertEngine(rules=[rule])
        classification = _make_classification(
            affiliation="neutral", threat_level=8,
        )
        alerts = engine.evaluate("ENT-001", classification)
        assert alerts == []


# ---------------------------------------------------------------------------
# AlertEvent dataclass
# ---------------------------------------------------------------------------


class TestAlertEvent:
    def test_alert_event_defaults(self):
        event = AlertEvent(
            alert_id="A-001",
            entity_id="E-001",
            alert_type="threat",
            severity=7,
            title="Test",
            description="Desc",
        )
        assert event.latitude == 0.0
        assert event.longitude == 0.0
        assert event.rule_name == ""
        assert event.cot_xml == ""
        assert isinstance(event.timestamp, datetime)
