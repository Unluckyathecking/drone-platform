"""Tests for the ADS-B receiver module.

All HTTP requests are mocked -- no real network calls are made.
Follows the same test pattern as test_ais_receiver.py.
"""

from __future__ import annotations

import io
import json
from unittest.mock import MagicMock, patch

import pytest

from mpe.aircraft_tracker import AircraftTracker
from mpe.adsb_receiver import ADSBReceiver, ADSBError


# ---------------------------------------------------------------------------
# Sample API responses for mocking
# ---------------------------------------------------------------------------

SAMPLE_AIRPLANES_LIVE_RESPONSE = {
    "ac": [
        {
            "hex": "4ca87c",
            "flight": "RYR1234 ",
            "lat": 51.47,
            "lon": -0.45,
            "alt_baro": 3500,
            "alt_geom": 3550,
            "gs": 180.5,
            "track": 270.3,
            "baro_rate": -500,
            "squawk": "4521",
            "category": "A3",
            "t": "B738",
            "r": "EI-DCL",
            "ground": False,
        },
    ],
    "total": 1,
    "now": 1711574400,
}

SAMPLE_AIRPLANES_LIVE_MULTI = {
    "ac": [
        {
            "hex": "4ca87c",
            "flight": "RYR1234 ",
            "lat": 51.47,
            "lon": -0.45,
            "alt_baro": 3500,
            "alt_geom": 3550,
            "gs": 180.5,
            "track": 270.3,
            "baro_rate": -500,
            "squawk": "4521",
            "category": "A3",
            "t": "B738",
            "r": "EI-DCL",
            "ground": False,
        },
        {
            "hex": "abc123",
            "flight": "BAW456  ",
            "lat": 51.50,
            "lon": -0.10,
            "alt_baro": 35000,
            "alt_geom": 35100,
            "gs": 450.0,
            "track": 90.0,
            "baro_rate": 0,
            "squawk": "1234",
            "category": "A5",
            "t": "A388",
            "r": "G-XLEA",
            "ground": False,
        },
    ],
    "total": 2,
    "now": 1711574400,
}

SAMPLE_AIRPLANES_LIVE_EMPTY = {
    "ac": [],
    "total": 0,
    "now": 1711574400,
}

SAMPLE_OPENSKY_RESPONSE = {
    "time": 1711574400,
    "states": [
        # [icao24, callsign, origin_country, time_position, last_contact,
        #  longitude, latitude, baro_altitude, on_ground, velocity,
        #  true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source]
        [
            "4ca87c", "RYR1234 ", "Ireland", 1711574390, 1711574399,
            -0.45, 51.47, 1066.8, False, 92.8,
            270.3, -2.54, None, 1082.04, "4521", False, 0,
        ],
    ],
}

SAMPLE_OPENSKY_EMPTY = {
    "time": 1711574400,
    "states": [],
}

SAMPLE_OPENSKY_NULL_STATES = {
    "time": 1711574400,
    "states": None,
}


def _mock_urlopen(response_data: dict):
    """Create a mock for urllib.request.urlopen that returns JSON data."""
    response_bytes = json.dumps(response_data).encode("utf-8")
    mock_response = MagicMock()
    mock_response.read.return_value = response_bytes
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


# ---------------------------------------------------------------------------
# airplanes.live tests
# ---------------------------------------------------------------------------

class TestFetchAirplanesLive:
    """Test fetching from airplanes.live API."""

    @patch("mpe.adsb_receiver.urlopen")
    def test_parses_single_aircraft(self, mock_urlopen):
        """Should parse a single aircraft from airplanes.live response."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_AIRPLANES_LIVE_RESPONSE)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        count = receiver.fetch_once()

        assert count == 1
        track = tracker.get("4CA87C")
        assert track is not None
        assert track.latitude == 51.47
        assert track.longitude == -0.45
        assert track.altitude_baro_ft == 3500
        assert track.altitude_geom_ft == 3550
        assert track.ground_speed_kts == 180.5
        assert track.heading == 270.3
        assert track.vertical_rate_fpm == -500
        assert track.callsign == "RYR1234"
        assert track.squawk == "4521"
        assert track.category == "A3"
        assert track.aircraft_type == "B738"
        assert track.registration == "EI-DCL"
        assert track.on_ground is False

    @patch("mpe.adsb_receiver.urlopen")
    def test_parses_multiple_aircraft(self, mock_urlopen):
        """Should parse multiple aircraft from response."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_AIRPLANES_LIVE_MULTI)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        count = receiver.fetch_once()

        assert count == 2
        assert tracker.get("4CA87C") is not None
        assert tracker.get("ABC123") is not None

    @patch("mpe.adsb_receiver.urlopen")
    def test_handles_empty_response(self, mock_urlopen):
        """Should handle an empty aircraft list gracefully."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_AIRPLANES_LIVE_EMPTY)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        count = receiver.fetch_once()

        assert count == 0
        assert len(tracker.all_tracks) == 0

    @patch("mpe.adsb_receiver.urlopen")
    def test_strips_callsign_whitespace(self, mock_urlopen):
        """Should strip trailing whitespace from callsign/flight field."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_AIRPLANES_LIVE_RESPONSE)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        receiver.fetch_once()

        track = tracker.get("4CA87C")
        assert track.callsign == "RYR1234"  # trailing space stripped

    @patch("mpe.adsb_receiver.urlopen")
    def test_handles_non_numeric_alt_baro(self, mock_urlopen):
        """Should handle alt_baro being 'ground' string."""
        response = {
            "ac": [{
                "hex": "abc123",
                "lat": 51.47,
                "lon": -0.45,
                "alt_baro": "ground",
                "alt_geom": 100,
                "gs": 5.0,
                "track": 90.0,
            }],
            "total": 1,
            "now": 1711574400,
        }
        mock_urlopen.return_value = _mock_urlopen(response)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        count = receiver.fetch_once()

        assert count == 1
        track = tracker.get("ABC123")
        assert track.altitude_baro_ft == 0.0  # default, since "ground" is not numeric

    @patch("mpe.adsb_receiver.urlopen")
    def test_skips_empty_hex(self, mock_urlopen):
        """Should skip aircraft with empty hex code."""
        response = {
            "ac": [
                {"hex": "", "lat": 51.0, "lon": -0.1},
                {"hex": "abc123", "lat": 51.5, "lon": -0.2},
            ],
            "total": 2,
            "now": 1711574400,
        }
        mock_urlopen.return_value = _mock_urlopen(response)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")
        count = receiver.fetch_once()

        assert count == 1

    @patch("mpe.adsb_receiver.urlopen")
    def test_network_error_raises_adsb_error(self, mock_urlopen):
        """Should raise ADSBError on network failure."""
        from urllib.error import URLError
        mock_urlopen.side_effect = URLError("Connection refused")

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="airplanes_live")

        with pytest.raises(ADSBError, match="Failed to fetch from airplanes.live"):
            receiver.fetch_once()


# ---------------------------------------------------------------------------
# OpenSky tests
# ---------------------------------------------------------------------------

class TestFetchOpenSky:
    """Test fetching from OpenSky Network API."""

    @patch("mpe.adsb_receiver.urlopen")
    def test_parses_opensky_state_vector(self, mock_urlopen):
        """Should parse OpenSky state vector correctly."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_OPENSKY_RESPONSE)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        count = receiver.fetch_once()

        assert count == 1
        track = tracker.get("4CA87C")
        assert track is not None
        assert track.latitude == 51.47
        assert track.longitude == -0.45
        assert track.callsign == "RYR1234"
        assert track.squawk == "4521"
        assert track.on_ground is False

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_altitude_conversion(self, mock_urlopen):
        """OpenSky gives altitude in metres; should convert to feet."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_OPENSKY_RESPONSE)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        receiver.fetch_once()

        track = tracker.get("4CA87C")
        # 1066.8 m * 3.28084 = ~3500 ft
        assert track.altitude_baro_ft == pytest.approx(1066.8 * 3.28084, rel=1e-3)

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_speed_conversion(self, mock_urlopen):
        """OpenSky gives velocity in m/s; should convert to knots."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_OPENSKY_RESPONSE)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        receiver.fetch_once()

        track = tracker.get("4CA87C")
        # 92.8 m/s * 1.94384 = ~180.4 knots
        assert track.ground_speed_kts == pytest.approx(92.8 * 1.94384, rel=1e-3)

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_empty_states(self, mock_urlopen):
        """Should handle empty states list."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_OPENSKY_EMPTY)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        count = receiver.fetch_once()

        assert count == 0

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_null_states(self, mock_urlopen):
        """Should handle null states field."""
        mock_urlopen.return_value = _mock_urlopen(SAMPLE_OPENSKY_NULL_STATES)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        count = receiver.fetch_once()

        assert count == 0

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_network_error(self, mock_urlopen):
        """Should raise ADSBError on network failure."""
        from urllib.error import URLError
        mock_urlopen.side_effect = URLError("Timeout")

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")

        with pytest.raises(ADSBError, match="Failed to fetch from OpenSky"):
            receiver.fetch_once()

    @patch("mpe.adsb_receiver.urlopen")
    def test_opensky_skips_short_state_vector(self, mock_urlopen):
        """Should skip state vectors with fewer than 17 elements."""
        response = {
            "time": 1711574400,
            "states": [
                ["4ca87c", "RYR1234"],  # too short
            ],
        }
        mock_urlopen.return_value = _mock_urlopen(response)

        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="opensky")
        count = receiver.fetch_once()

        assert count == 0


# ---------------------------------------------------------------------------
# General receiver tests
# ---------------------------------------------------------------------------

class TestADSBReceiverGeneral:
    """Test general ADSBReceiver behaviour."""

    def test_unknown_source_raises(self):
        """Should raise ADSBError for unknown source."""
        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, source="invalid_source")

        with pytest.raises(ADSBError, match="Unknown source"):
            receiver.fetch_once()

    def test_radius_capped_at_250(self):
        """Radius should be capped at 250 nm."""
        tracker = AircraftTracker()
        receiver = ADSBReceiver(tracker, radius_nm=500)
        assert receiver._radius_nm == 250
