"""Structured JSON logging for the C2 engine.

Replaces plain text logging with JSON output suitable for:
- SIEM ingestion (Splunk, Elastic, etc.)
- jq command-line filtering
- Automated alerting pipelines
"""

import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record):
        log_entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Add extra fields if present
        for key in (
            "entity_id",
            "source",
            "domain",
            "threat_level",
            "alert_type",
            "event_type",
            "observation_count",
        ):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


def configure_logging(
    level: str = "INFO",
    json_output: bool = True,
    log_file: str | None = None,
):
    """Configure logging for the engine.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_output: If True, output JSON. If False, output human-readable.
        log_file: If set, also write to this file.
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Clear existing handlers
    root.handlers.clear()

    if json_output:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    root.addHandler(console)

    # File handler (optional)
    if log_file:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=50_000_000,
            backupCount=5,  # 50MB, keep 5 rotations
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
