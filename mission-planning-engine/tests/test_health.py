"""Tests for the health monitoring module."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from mpe.health import HealthMonitor, SourceHealth


# -- SourceHealth dataclass tests -------------------------------------------


class TestSourceHealthDefaults:
    def test_source_health_defaults(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.name == "adsb"
        assert src.source_type == "adsb"
        assert src.expected_interval_s == 10.0
        assert src.last_observation is None
        assert src.observation_count == 0
        assert src.error_count == 0
        assert src.last_error == ""
        assert src.enabled is True


class TestSourceHealthyAfterObservation:
    def test_source_healthy_after_observation(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        src.record_observation()
        assert src.is_healthy is True


class TestSourceUnhealthyWhenNeverObserved:
    def test_source_unhealthy_when_never_observed(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.is_healthy is False


class TestSourceStaleAfterTimeout:
    def test_source_stale_after_timeout(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        # Set last observation to well beyond 2x the expected interval
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=25)
        assert src.is_stale is True

    def test_source_not_stale_when_disabled(self):
        src = SourceHealth(
            name="adsb", source_type="adsb", expected_interval_s=10.0, enabled=False,
        )
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=25)
        assert src.is_stale is False

    def test_source_not_stale_when_never_observed(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.is_stale is False


class TestSourceHealthyWithinTolerance:
    def test_source_healthy_within_tolerance(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        # Within 3x tolerance (< 30s)
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=25)
        assert src.is_healthy is True

    def test_source_unhealthy_beyond_tolerance(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        # Beyond 3x tolerance (>= 30s)
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=35)
        assert src.is_healthy is False


class TestRecordObservationUpdatesTimestamp:
    def test_record_observation_updates_timestamp(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.last_observation is None
        src.record_observation()
        assert src.last_observation is not None
        ts1 = src.last_observation
        src.record_observation()
        assert src.last_observation >= ts1


class TestRecordObservationIncrementsCount:
    def test_record_observation_increments_count(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.observation_count == 0
        src.record_observation()
        assert src.observation_count == 1
        src.record_observation()
        assert src.observation_count == 2


class TestRecordErrorIncrementsCount:
    def test_record_error_increments_count(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.error_count == 0
        src.record_error("timeout")
        assert src.error_count == 1
        src.record_error("connection refused")
        assert src.error_count == 2


class TestRecordErrorStoresMessage:
    def test_record_error_stores_message(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        src.record_error("first error")
        assert src.last_error == "first error"
        src.record_error("second error")
        assert src.last_error == "second error"


# -- HealthMonitor tests ----------------------------------------------------


class TestRegisterSource:
    def test_register_source(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        src = monitor.get_source("adsb")
        assert src is not None
        assert src.name == "adsb"
        assert src.source_type == "adsb"
        assert src.expected_interval_s == 10.0
        assert src.enabled is True

    def test_register_source_disabled(self):
        monitor = HealthMonitor()
        monitor.register_source("ais", "ais", expected_interval_s=30.0, enabled=False)
        src = monitor.get_source("ais")
        assert src is not None
        assert src.enabled is False


class TestRecordUnknownSourceNoError:
    def test_record_unknown_source_no_error(self):
        monitor = HealthMonitor()
        # Should not raise
        monitor.record("nonexistent")
        monitor.record_error("nonexistent", "some error")


class TestCheckReturnsAlertsForDeadSources:
    def test_check_returns_alerts_for_dead_sources(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        # Never observed -- should be unhealthy
        alerts = monitor.check()
        assert len(alerts) == 1
        assert alerts[0]["source"] == "adsb"
        assert alerts[0]["alert_type"] == "system"
        assert alerts[0]["title"] == "INGEST OFFLINE: adsb"
        assert "never produced data" in alerts[0]["description"]

    def test_check_returns_alert_for_stale_source(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        src = monitor.get_source("adsb")
        # Set last observation beyond 3x tolerance
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=60)
        alerts = monitor.check()
        assert len(alerts) == 1
        assert "offline" in alerts[0]["description"]


class TestCheckNoAlertsWhenHealthy:
    def test_check_no_alerts_when_healthy(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        monitor.record("adsb")
        alerts = monitor.check()
        assert len(alerts) == 0


class TestCheckCooldownPreventsRepeatedAlerts:
    def test_check_cooldown_prevents_repeated_alerts(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        # First check: should get an alert (never observed)
        alerts1 = monitor.check()
        assert len(alerts1) == 1
        # Second check immediately: should be suppressed by cooldown
        alerts2 = monitor.check()
        assert len(alerts2) == 0


class TestCheckCooldownExpires:
    def test_check_cooldown_expires(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        # First alert
        alerts1 = monitor.check()
        assert len(alerts1) == 1
        # Simulate cooldown expiry by backdating the alert timestamp
        monitor._alerts_generated["adsb"] = datetime.now(timezone.utc) - timedelta(
            seconds=301,
        )
        # Should fire again now
        alerts2 = monitor.check()
        assert len(alerts2) == 1


class TestCheckDisabledSourceIgnored:
    def test_check_disabled_source_ignored(self):
        monitor = HealthMonitor()
        monitor.register_source("ais", "ais", expected_interval_s=30.0, enabled=False)
        alerts = monitor.check()
        assert len(alerts) == 0


class TestStatusOverallHealthy:
    def test_status_overall_healthy(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        monitor.record("adsb")
        status = monitor.status
        assert status["overall"] == "healthy"
        assert status["sources_healthy"] == 1
        assert status["sources_offline"] == 0


class TestStatusOverallDegraded:
    def test_status_overall_degraded(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        monitor.register_source("ais", "ais", expected_interval_s=30.0)
        monitor.record("adsb")
        # ais never observed -> unhealthy
        status = monitor.status
        assert status["overall"] == "degraded"
        assert status["sources_healthy"] == 1
        assert status["sources_offline"] == 1


class TestStatusSourceDetails:
    def test_status_source_details(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        monitor.record("adsb")
        status = monitor.status
        adsb = status["sources"]["adsb"]
        assert adsb["type"] == "adsb"
        assert adsb["enabled"] is True
        assert adsb["healthy"] is True
        assert adsb["observation_count"] == 1
        assert adsb["error_count"] == 0
        assert adsb["last_error"] is None
        assert adsb["last_observation"] is not None
        assert adsb["age_seconds"] is not None
        assert adsb["age_seconds"] < 5.0  # Just recorded

    def test_status_source_details_with_errors(self):
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        monitor.record("adsb")
        monitor.record_error("adsb", "timeout")
        status = monitor.status
        adsb = status["sources"]["adsb"]
        assert adsb["error_count"] == 1
        assert adsb["last_error"] == "timeout"

    def test_status_source_never_observed(self):
        monitor = HealthMonitor()
        monitor.register_source("ais", "ais", expected_interval_s=30.0)
        status = monitor.status
        ais = status["sources"]["ais"]
        assert ais["healthy"] is False
        assert ais["last_observation"] is None
        assert ais["age_seconds"] is None


class TestAlertSeverityScalesWithAge:
    def test_severity_low_for_recent_dead_source(self):
        """Sources offline for < 5x interval get severity 5."""
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        src = monitor.get_source("adsb")
        # 35s ago: beyond 3x (unhealthy) but below 5x (50s)
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=35)
        alerts = monitor.check()
        assert len(alerts) == 1
        assert alerts[0]["severity"] == 5

    def test_severity_high_for_long_dead_source(self):
        """Sources offline for > 5x interval get severity 7."""
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        src = monitor.get_source("adsb")
        # 60s ago: beyond 5x (50s)
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=60)
        alerts = monitor.check()
        assert len(alerts) == 1
        assert alerts[0]["severity"] == 7

    def test_severity_for_never_observed_source(self):
        """Sources that never produced data get severity 6."""
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10.0)
        alerts = monitor.check()
        assert len(alerts) == 1
        assert alerts[0]["severity"] == 6

    def test_disabled_source_healthy(self):
        """Disabled sources count as healthy."""
        src = SourceHealth(
            name="ais", source_type="ais", expected_interval_s=30.0, enabled=False,
        )
        assert src.is_healthy is True

    def test_age_seconds_none_when_never_observed(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        assert src.age_seconds is None

    def test_age_seconds_after_observation(self):
        src = SourceHealth(name="adsb", source_type="adsb", expected_interval_s=10.0)
        src.last_observation = datetime.now(timezone.utc) - timedelta(seconds=5)
        age = src.age_seconds
        assert age is not None
        assert 4.5 < age < 6.0
