"""Tests for the AIS receiver module.

Tests decode_nmea with real AIS test vectors from the pyais documentation.
UDP socket testing is out of scope (requires network).
"""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from mpe.vessel_tracker import VesselTracker


# ---------------------------------------------------------------------------
# Real AIS test vectors (from pyais docs / ITU test data)
# ---------------------------------------------------------------------------

# Type 1 position report: MMSI 366053209, lat ~37.80, lon ~-122.34
TYPE1_NMEA = "!AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0*73"
TYPE1_MMSI = 366053209

# Type 5 static data: MMSI 351759000, name "EVER DAINTY" (multi-sentence)
TYPE5_NMEA_1 = "!AIVDM,2,1,3,B,55?MbV02>H97ac<H4eEK6WtO422teleH000000000000P1@D23m@N0k0Ep,0*28"
TYPE5_NMEA_2 = "!AIVDM,2,2,3,B,00000000000,2*23"


# ---------------------------------------------------------------------------
# AISReceiver.decode_nmea
# ---------------------------------------------------------------------------

class TestDecodeNmea:
    """Test AIS NMEA decoding into the vessel tracker."""

    def test_type1_position_report(self):
        """Type 1 position report should update lat/lon on the tracker."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)
        receiver.decode_nmea(TYPE1_NMEA)

        track = tracker.get(TYPE1_MMSI)
        assert track is not None
        assert track.latitude != 0.0
        assert track.longitude != 0.0

    def test_type1_has_reasonable_coordinates(self):
        """Decoded type 1 should produce plausible coordinates."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)
        receiver.decode_nmea(TYPE1_NMEA)

        track = tracker.get(TYPE1_MMSI)
        assert track is not None
        # Known position from this test vector: approx lat 37.80, lon -122.34
        assert 37.0 < track.latitude < 38.0
        assert -123.0 < track.longitude < -122.0

    def test_type5_static_data(self):
        """Type 5 static data should update vessel name and ship type."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)
        receiver.decode_nmea(TYPE5_NMEA_1, TYPE5_NMEA_2)

        track = tracker.get(351759000)
        assert track is not None
        assert track.vessel_name != ""

    def test_position_then_static_merges(self):
        """Position update followed by static data should merge into one track."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)

        # Simulate two separate updates for the same MMSI
        tracker.update(mmsi=351759000, latitude=10.0, longitude=20.0)
        receiver.decode_nmea(TYPE5_NMEA_1, TYPE5_NMEA_2)

        track = tracker.get(351759000)
        assert track is not None
        assert track.latitude == 10.0      # preserved from position update
        assert track.vessel_name != ""     # added by static data

    def test_malformed_input_does_not_raise(self):
        """Malformed NMEA should be silently skipped."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)
        receiver.decode_nmea("this is not valid NMEA at all")
        assert len(tracker.all_tracks) == 0

    def test_empty_string_does_not_raise(self):
        """Empty string should be silently skipped."""
        from mpe.ais_receiver import AISReceiver

        tracker = VesselTracker()
        receiver = AISReceiver(tracker)
        receiver.decode_nmea("")
        assert len(tracker.all_tracks) == 0


# ---------------------------------------------------------------------------
# Graceful handling of missing pyais
# ---------------------------------------------------------------------------

class TestMissingPyais:
    """Verify that AISReceiver handles missing pyais gracefully."""

    def test_require_pyais_raises_ais_error(self):
        """_require_pyais should raise AISError when pyais is not importable."""
        saved = {}
        keys = [k for k in sys.modules if k == "pyais" or k.startswith("pyais.")]
        for k in keys:
            saved[k] = sys.modules.pop(k)

        try:
            with patch.dict(sys.modules, {"pyais": None}):
                from mpe.ais_receiver import _require_pyais, AISError
                with pytest.raises(AISError, match="pyais is not installed"):
                    _require_pyais()
        finally:
            for k, v in saved.items():
                sys.modules[k] = v

    def test_decode_nmea_raises_when_pyais_missing(self):
        """decode_nmea should raise AISError when pyais is not available."""
        saved = {}
        keys = [k for k in sys.modules if k == "pyais" or k.startswith("pyais.")]
        for k in keys:
            saved[k] = sys.modules.pop(k)

        try:
            with patch.dict(sys.modules, {"pyais": None}):
                from mpe.ais_receiver import AISReceiver, AISError
                tracker = VesselTracker()
                receiver = AISReceiver(tracker)
                with pytest.raises(AISError, match="pyais is not installed"):
                    receiver.decode_nmea(TYPE1_NMEA)
        finally:
            for k, v in saved.items():
                sys.modules[k] = v
