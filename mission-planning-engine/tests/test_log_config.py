"""Tests for structured JSON logging configuration."""

from __future__ import annotations

import json
import logging
from unittest.mock import patch

import pytest

from mpe.log_config import JSONFormatter, configure_logging


class TestJSONFormatter:
    """Tests for the JSONFormatter class."""

    def setup_method(self):
        self.formatter = JSONFormatter()

    def _make_record(self, msg: str = "test message", level: int = logging.INFO,
                     name: str = "test.logger", **extras) -> logging.LogRecord:
        record = logging.LogRecord(
            name=name,
            level=level,
            pathname="test.py",
            lineno=1,
            msg=msg,
            args=(),
            exc_info=None,
        )
        for key, value in extras.items():
            setattr(record, key, value)
        return record

    def test_json_formatter_produces_valid_json(self):
        record = self._make_record()
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert isinstance(parsed, dict)

    def test_json_formatter_includes_timestamp(self):
        record = self._make_record()
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert "ts" in parsed
        # ISO format check -- contains T separator and timezone info
        assert "T" in parsed["ts"]

    def test_json_formatter_includes_level(self):
        record = self._make_record(level=logging.WARNING)
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert parsed["level"] == "WARNING"

    def test_json_formatter_includes_message(self):
        record = self._make_record(msg="hello world")
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert parsed["msg"] == "hello world"

    def test_json_formatter_includes_extra_fields(self):
        record = self._make_record(
            entity_id="ADSB-ABC123",
            source="adsb",
            domain="air",
            threat_level=8,
            alert_type="threat",
            event_type="classification",
            observation_count=5,
        )
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert parsed["entity_id"] == "ADSB-ABC123"
        assert parsed["source"] == "adsb"
        assert parsed["domain"] == "air"
        assert parsed["threat_level"] == 8
        assert parsed["alert_type"] == "threat"
        assert parsed["event_type"] == "classification"
        assert parsed["observation_count"] == 5

    def test_json_formatter_omits_absent_extra_fields(self):
        record = self._make_record()
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert "entity_id" not in parsed
        assert "threat_level" not in parsed

    def test_json_formatter_handles_exception(self):
        record = self._make_record()
        try:
            raise ValueError("something broke")
        except ValueError:
            import sys
            record.exc_info = sys.exc_info()

        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert "exception" in parsed
        assert "ValueError" in parsed["exception"]
        assert "something broke" in parsed["exception"]

    def test_json_formatter_no_exception_field_when_no_exc(self):
        record = self._make_record()
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert "exception" not in parsed

    def test_json_formatter_includes_logger_name(self):
        record = self._make_record(name="mpe.engine")
        output = self.formatter.format(record)
        parsed = json.loads(output)
        assert parsed["logger"] == "mpe.engine"

    def test_json_formatter_single_line(self):
        """JSON output must be a single line for log aggregation."""
        record = self._make_record(msg="line1\nline2\nline3")
        output = self.formatter.format(record)
        assert "\n" not in output


class TestConfigureLogging:
    """Tests for the configure_logging function."""

    def teardown_method(self):
        """Reset root logger after each test."""
        root = logging.getLogger()
        root.handlers.clear()
        root.setLevel(logging.WARNING)

    def test_configure_logging_sets_level(self):
        configure_logging(level="DEBUG", json_output=False)
        root = logging.getLogger()
        assert root.level == logging.DEBUG

    def test_configure_logging_sets_level_warning(self):
        configure_logging(level="WARNING", json_output=False)
        root = logging.getLogger()
        assert root.level == logging.WARNING

    def test_configure_logging_json_mode(self):
        configure_logging(level="INFO", json_output=True)
        root = logging.getLogger()
        assert len(root.handlers) == 1
        handler = root.handlers[0]
        assert isinstance(handler.formatter, JSONFormatter)

    def test_configure_logging_text_mode(self):
        configure_logging(level="INFO", json_output=False)
        root = logging.getLogger()
        assert len(root.handlers) == 1
        handler = root.handlers[0]
        assert not isinstance(handler.formatter, JSONFormatter)
        assert isinstance(handler.formatter, logging.Formatter)

    def test_configure_logging_clears_existing_handlers(self):
        root = logging.getLogger()
        # Record how many handlers pytest has already added
        baseline = len(root.handlers)
        root.addHandler(logging.StreamHandler())
        root.addHandler(logging.StreamHandler())
        assert len(root.handlers) == baseline + 2

        configure_logging(level="INFO", json_output=True)
        # Should have exactly 1 handler (console) -- all prior handlers cleared
        assert len(root.handlers) == 1

    def test_configure_logging_with_log_file(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        configure_logging(level="INFO", json_output=True, log_file=log_file)
        root = logging.getLogger()
        # Should have 2 handlers: console + file
        assert len(root.handlers) == 2

        from logging.handlers import RotatingFileHandler

        file_handlers = [
            h for h in root.handlers if isinstance(h, RotatingFileHandler)
        ]
        assert len(file_handlers) == 1
        assert file_handlers[0].baseFilename == log_file

    def test_configure_logging_file_handler_uses_json(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        configure_logging(level="INFO", json_output=True, log_file=log_file)
        root = logging.getLogger()

        from logging.handlers import RotatingFileHandler

        file_handler = next(
            h for h in root.handlers if isinstance(h, RotatingFileHandler)
        )
        assert isinstance(file_handler.formatter, JSONFormatter)

    def test_configure_logging_invalid_level_defaults_to_info(self):
        configure_logging(level="NONEXISTENT", json_output=False)
        root = logging.getLogger()
        assert root.level == logging.INFO
