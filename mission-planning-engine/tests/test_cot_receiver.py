"""Tests for the CoT receiver -- XML parsing, event properties, and buffer handling."""

from __future__ import annotations

import pytest

from mpe.cot_receiver import CotEvent, CotReceiver, parse_cot_xml

# ---------------------------------------------------------------------------
# Sample CoT XML strings
# ---------------------------------------------------------------------------

SAMPLE_FRIENDLY_GROUND = (
    '<event version="2.0" type="a-f-G-U-C" uid="ATAK-USER-001"'
    ' how="m-g" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:05:00Z">'
    '  <point lat="4.6097" lon="-74.0817" hae="2640.0" ce="10.0" le="10.0"/>'
    "  <detail>"
    '    <contact callsign="OPERATOR-1"/>'
    '    <track course="180.0" speed="1.5"/>'
    "    <remarks>On patrol near Bogota</remarks>"
    "  </detail>"
    "</event>"
)

SAMPLE_AIRCRAFT = (
    '<event version="2.0" type="a-f-A-M-F-Q" uid="DRONE-01"'
    ' how="m-g" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:05:00Z">'
    '  <point lat="51.3632" lon="-0.2652" hae="120.0" ce="5.0" le="5.0"/>'
    "  <detail>"
    '    <contact callsign="EAGLE-1"/>'
    '    <track course="90.0" speed="25.0"/>'
    "  </detail>"
    "</event>"
)

SAMPLE_VESSEL_NEUTRAL = (
    '<event version="2.0" type="a-n-S-C-M" uid="AIS-211234567"'
    ' how="m-g" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:10:00Z">'
    '  <point lat="50.8000" lon="-1.1000" hae="0.0" ce="50.0" le="50.0"/>'
    "  <detail>"
    '    <contact callsign="CARGO-VESSEL"/>'
    '    <track course="270.0" speed="5.14"/>'
    "    <remarks>Inbound to Southampton</remarks>"
    "  </detail>"
    "</event>"
)

SAMPLE_NO_DETAIL = (
    '<event version="2.0" type="a-u-A" uid="UNKNOWN-TRACK-99"'
    ' how="h-e" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:05:00Z">'
    '  <point lat="52.0" lon="0.0" hae="5000.0" ce="100.0" le="100.0"/>'
    "</event>"
)

SAMPLE_HOSTILE_AIR = (
    '<event version="2.0" type="a-h-A-M-F" uid="HOSTILE-01"'
    ' how="m-g" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:05:00Z">'
    '  <point lat="33.0" lon="44.0" hae="3000.0" ce="20.0" le="20.0"/>'
    "</event>"
)

SAMPLE_SUSPECT = (
    '<event version="2.0" type="a-j-G-E" uid="SUSPECT-01"'
    ' how="h-e" time="2026-03-28T12:00:00Z" start="2026-03-28T12:00:00Z"'
    ' stale="2026-03-28T12:05:00Z">'
    '  <point lat="10.0" lon="20.0" hae="0.0" ce="50.0" le="50.0"/>'
    "</event>"
)


# ===========================================================================
# parse_cot_xml tests
# ===========================================================================


class TestParseCotXml:
    """Tests for the parse_cot_xml function."""

    def test_parse_valid_friendly_ground_unit(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.uid == "ATAK-USER-001"
        assert event.event_type == "a-f-G-U-C"
        assert event.latitude == pytest.approx(4.6097)
        assert event.longitude == pytest.approx(-74.0817)
        assert event.altitude_hae == pytest.approx(2640.0)
        assert event.how == "m-g"
        assert event.stale == "2026-03-28T12:05:00Z"

    def test_parse_valid_aircraft_position(self) -> None:
        event = parse_cot_xml(SAMPLE_AIRCRAFT)
        assert event is not None
        assert event.uid == "DRONE-01"
        assert event.event_type == "a-f-A-M-F-Q"
        assert event.latitude == pytest.approx(51.3632)
        assert event.longitude == pytest.approx(-0.2652)
        assert event.altitude_hae == pytest.approx(120.0)

    def test_parse_vessel_neutral(self) -> None:
        event = parse_cot_xml(SAMPLE_VESSEL_NEUTRAL)
        assert event is not None
        assert event.uid == "AIS-211234567"
        assert event.event_type == "a-n-S-C-M"
        assert event.latitude == pytest.approx(50.8)
        assert event.longitude == pytest.approx(-1.1)

    def test_parse_malformed_xml_returns_none(self) -> None:
        assert parse_cot_xml("<not valid xml<<<") is None

    def test_parse_missing_uid_returns_none(self) -> None:
        xml = (
            '<event version="2.0" type="a-f-G" uid=""'
            ' how="m-g" time="2026-03-28T12:00:00Z"'
            ' start="2026-03-28T12:00:00Z" stale="2026-03-28T12:05:00Z">'
            '  <point lat="0" lon="0" hae="0"/>'
            "</event>"
        )
        assert parse_cot_xml(xml) is None

    def test_parse_missing_point_returns_none(self) -> None:
        xml = (
            '<event version="2.0" type="a-f-G" uid="NO-POINT-1"'
            ' how="m-g" time="2026-03-28T12:00:00Z"'
            ' start="2026-03-28T12:00:00Z" stale="2026-03-28T12:05:00Z">'
            "</event>"
        )
        assert parse_cot_xml(xml) is None

    def test_parse_with_detail_contact_callsign(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.callsign == "OPERATOR-1"

    def test_parse_with_track_heading_speed(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.heading == pytest.approx(180.0)
        assert event.speed_mps == pytest.approx(1.5)

    def test_parse_with_remarks(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.remarks == "On patrol near Bogota"

    def test_parse_without_detail(self) -> None:
        event = parse_cot_xml(SAMPLE_NO_DETAIL)
        assert event is not None
        assert event.uid == "UNKNOWN-TRACK-99"
        assert event.callsign == ""
        assert event.heading == 0.0
        assert event.speed_mps == 0.0
        assert event.remarks == ""

    def test_parse_non_event_root_returns_none(self) -> None:
        xml = '<point lat="0" lon="0" hae="0"/>'
        assert parse_cot_xml(xml) is None

    def test_raw_xml_preserved(self) -> None:
        event = parse_cot_xml(SAMPLE_AIRCRAFT)
        assert event is not None
        assert "DRONE-01" in event.raw_xml


# ===========================================================================
# CotEvent property tests
# ===========================================================================


class TestCotEventProperties:
    """Tests for CotEvent domain and affiliation properties."""

    def test_domain_air_from_type(self) -> None:
        event = parse_cot_xml(SAMPLE_AIRCRAFT)
        assert event is not None
        assert event.domain == "air"

    def test_domain_sea_from_type(self) -> None:
        event = parse_cot_xml(SAMPLE_VESSEL_NEUTRAL)
        assert event is not None
        assert event.domain == "sea"

    def test_domain_land_from_type(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.domain == "land"

    def test_domain_unknown_for_empty_type(self) -> None:
        event = CotEvent(uid="test", event_type="", latitude=0, longitude=0)
        assert event.domain == "unknown"

    def test_domain_unknown_for_short_type(self) -> None:
        event = CotEvent(uid="test", event_type="a", latitude=0, longitude=0)
        assert event.domain == "unknown"

    def test_affiliation_friendly(self) -> None:
        event = parse_cot_xml(SAMPLE_FRIENDLY_GROUND)
        assert event is not None
        assert event.affiliation == "friendly"

    def test_affiliation_hostile(self) -> None:
        event = parse_cot_xml(SAMPLE_HOSTILE_AIR)
        assert event is not None
        assert event.affiliation == "hostile"

    def test_affiliation_neutral(self) -> None:
        event = parse_cot_xml(SAMPLE_VESSEL_NEUTRAL)
        assert event is not None
        assert event.affiliation == "neutral"

    def test_affiliation_unknown_type(self) -> None:
        event = parse_cot_xml(SAMPLE_NO_DETAIL)
        assert event is not None
        # type "a-u-A" -> affiliation "u" -> "unknown"
        assert event.affiliation == "unknown"

    def test_affiliation_suspect(self) -> None:
        event = parse_cot_xml(SAMPLE_SUSPECT)
        assert event is not None
        assert event.affiliation == "suspect"

    def test_affiliation_empty_type(self) -> None:
        event = CotEvent(uid="test", event_type="", latitude=0, longitude=0)
        assert event.affiliation == "unknown"


# ===========================================================================
# CotReceiver tests
# ===========================================================================


class TestCotReceiver:
    """Tests for the CotReceiver class (no real sockets)."""

    def test_receiver_creation(self) -> None:
        receiver = CotReceiver(url="tcp://192.168.1.100:8087")
        assert receiver._host == "192.168.1.100"
        assert receiver._port == 8087
        assert receiver._scheme == "tcp"

    def test_receiver_creation_udp(self) -> None:
        receiver = CotReceiver(url="udp://239.2.3.1:6969")
        assert receiver._host == "239.2.3.1"
        assert receiver._port == 6969
        assert receiver._scheme == "udp"

    def test_receiver_stats_initial(self) -> None:
        receiver = CotReceiver()
        stats = receiver.stats
        assert stats["events_received"] == 0
        assert stats["events_parsed"] == 0
        assert stats["running"] is False

    def test_process_buffer_extracts_complete_events(self) -> None:
        received: list[CotEvent] = []
        receiver = CotReceiver(on_event=received.append)

        receiver._buffer = SAMPLE_FRIENDLY_GROUND
        receiver._process_buffer()

        assert receiver._events_received == 1
        assert receiver._events_parsed == 1
        assert len(received) == 1
        assert received[0].uid == "ATAK-USER-001"

    def test_process_buffer_handles_partial_events(self) -> None:
        received: list[CotEvent] = []
        receiver = CotReceiver(on_event=received.append)

        # Only the first half of an event -- no </event> yet
        partial = SAMPLE_FRIENDLY_GROUND[: len(SAMPLE_FRIENDLY_GROUND) // 2]
        receiver._buffer = partial
        receiver._process_buffer()

        assert receiver._events_received == 0
        assert len(received) == 0
        # Buffer should still contain the partial data
        assert len(receiver._buffer) > 0

    def test_process_buffer_handles_multiple_events(self) -> None:
        received: list[CotEvent] = []
        receiver = CotReceiver(on_event=received.append)

        receiver._buffer = SAMPLE_FRIENDLY_GROUND + SAMPLE_AIRCRAFT
        receiver._process_buffer()

        assert receiver._events_received == 2
        assert receiver._events_parsed == 2
        assert len(received) == 2
        assert received[0].uid == "ATAK-USER-001"
        assert received[1].uid == "DRONE-01"

    def test_process_buffer_discards_junk_before_event(self) -> None:
        received: list[CotEvent] = []
        receiver = CotReceiver(on_event=received.append)

        receiver._buffer = "some junk data " + SAMPLE_AIRCRAFT
        receiver._process_buffer()

        assert receiver._events_parsed == 1
        assert received[0].uid == "DRONE-01"

    def test_process_buffer_handles_no_opener(self) -> None:
        received: list[CotEvent] = []
        receiver = CotReceiver(on_event=received.append)

        # Just a closing tag with no opener
        receiver._buffer = "garbage</event>"
        receiver._process_buffer()

        assert receiver._events_received == 0
        assert len(received) == 0
        assert receiver._buffer == ""

    def test_stop_without_start(self) -> None:
        receiver = CotReceiver()
        # Should not raise
        receiver.stop()
        assert receiver._running is False

    def test_default_callback_does_not_raise(self) -> None:
        receiver = CotReceiver()
        receiver._buffer = SAMPLE_FRIENDLY_GROUND
        # Default no-op callback should not raise
        receiver._process_buffer()
        assert receiver._events_parsed == 1
