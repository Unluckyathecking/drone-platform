"""Health monitoring -- detects dead sources and reports system status.

Tracks the last observation timestamp per ingest source. If a source
goes silent for longer than its expected interval, generates an alert.
Also provides a structured health report for the operator API.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger("mpe.health")


@dataclass
class SourceHealth:
    """Health state of a single ingest source."""

    name: str
    source_type: str  # "adsb", "ais", "cot", "mavlink"
    expected_interval_s: float  # Expected update interval
    last_observation: datetime | None = None
    observation_count: int = 0
    error_count: int = 0
    last_error: str = ""
    enabled: bool = True

    @property
    def is_healthy(self) -> bool:
        if not self.enabled:
            return True  # Disabled sources are "healthy" (not expected)
        if self.last_observation is None:
            return False  # Never received data
        age = (datetime.now(timezone.utc) - self.last_observation).total_seconds()
        return age < self.expected_interval_s * 3  # 3x tolerance

    @property
    def is_stale(self) -> bool:
        if not self.enabled or self.last_observation is None:
            return False
        age = (datetime.now(timezone.utc) - self.last_observation).total_seconds()
        return age > self.expected_interval_s * 2

    @property
    def age_seconds(self) -> float | None:
        if self.last_observation is None:
            return None
        return (datetime.now(timezone.utc) - self.last_observation).total_seconds()

    def record_observation(self) -> None:
        """Record that an observation was received."""
        self.last_observation = datetime.now(timezone.utc)
        self.observation_count += 1

    def record_error(self, error: str) -> None:
        """Record an error."""
        self.error_count += 1
        self.last_error = error


class HealthMonitor:
    """Monitors system health and generates alerts for dead sources.

    Usage:
        monitor = HealthMonitor()
        monitor.register_source("adsb", "adsb", expected_interval_s=10)
        monitor.register_source("ais", "ais", expected_interval_s=30)

        # In the engine loop:
        monitor.record("adsb")  # When ADS-B data arrives
        alerts = monitor.check()  # Returns list of health alerts
    """

    def __init__(self) -> None:
        self._sources: dict[str, SourceHealth] = {}
        self._alerts_generated: dict[str, datetime] = {}  # source -> last alert time
        self._alert_cooldown_s: float = 300  # Don't re-alert for same source within 5 min

    def register_source(
        self,
        name: str,
        source_type: str,
        expected_interval_s: float = 10.0,
        enabled: bool = True,
    ) -> None:
        """Register an ingest source for monitoring."""
        self._sources[name] = SourceHealth(
            name=name,
            source_type=source_type,
            expected_interval_s=expected_interval_s,
            enabled=enabled,
        )
        logger.debug("Health monitor: registered source '%s' (%s)", name, source_type)

    def record(self, source_name: str) -> None:
        """Record that a source produced an observation."""
        if source_name in self._sources:
            self._sources[source_name].record_observation()

    def record_error(self, source_name: str, error: str) -> None:
        """Record a source error."""
        if source_name in self._sources:
            self._sources[source_name].record_error(error)
            logger.warning("Source '%s' error: %s", source_name, error)

    def check(self) -> list[dict]:
        """Check all sources and return alerts for unhealthy ones.

        Returns a list of alert dicts (not full AlertEvents -- the engine
        converts these to CoT alerts).
        """
        alerts: list[dict] = []
        now = datetime.now(timezone.utc)

        for name, source in self._sources.items():
            if not source.enabled:
                continue

            if not source.is_healthy:
                # Check cooldown
                last_alert = self._alerts_generated.get(name)
                if (
                    last_alert
                    and (now - last_alert).total_seconds() < self._alert_cooldown_s
                ):
                    continue

                if source.last_observation is None:
                    desc = (
                        f"Source '{name}' ({source.source_type}) "
                        f"has never produced data"
                    )
                    severity = 6
                else:
                    age = source.age_seconds
                    desc = (
                        f"Source '{name}' ({source.source_type}) "
                        f"offline -- last data {age:.0f}s ago"
                    )
                    severity = 7 if age > source.expected_interval_s * 5 else 5

                if source.last_error:
                    desc += f" (last error: {source.last_error})"

                alerts.append({
                    "source": name,
                    "source_type": source.source_type,
                    "alert_type": "system",
                    "severity": severity,
                    "title": f"INGEST OFFLINE: {name}",
                    "description": desc,
                })

                self._alerts_generated[name] = now
                logger.warning("Health alert: %s", desc)

        return alerts

    @property
    def status(self) -> dict:
        """Full health status report."""
        sources: dict[str, dict] = {}
        for name, src in self._sources.items():
            sources[name] = {
                "type": src.source_type,
                "enabled": src.enabled,
                "healthy": src.is_healthy,
                "stale": src.is_stale,
                "last_observation": (
                    src.last_observation.isoformat() if src.last_observation else None
                ),
                "age_seconds": (
                    round(src.age_seconds, 1) if src.age_seconds is not None else None
                ),
                "observation_count": src.observation_count,
                "error_count": src.error_count,
                "last_error": src.last_error or None,
            }

        all_healthy = all(
            s.is_healthy for s in self._sources.values() if s.enabled
        )

        return {
            "overall": "healthy" if all_healthy else "degraded",
            "sources": sources,
            "sources_total": len(self._sources),
            "sources_healthy": sum(1 for s in self._sources.values() if s.is_healthy),
            "sources_offline": sum(
                1
                for s in self._sources.values()
                if s.enabled and not s.is_healthy
            ),
        }

    def get_source(self, name: str) -> SourceHealth | None:
        """Get health state for a specific source."""
        return self._sources.get(name)
