"""Tests for the MAVLink mission upload module.

All tests mock pymavlink so no real SITL connection is required.
The upload module does a lazy ``from pymavlink import mavutil`` inside
upload_mission(), so we inject a mock into sys.modules.
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from mpe.models import MAVCmd, MAVFrame, MissionItem
from mpe.upload import UploadError, upload_mission, _LAT_LON_SCALE


# ── Helpers ──────────────────────────────────────────────────────────


def _sample_items() -> list[MissionItem]:
    """Minimal 3-item mission: HOME, TAKEOFF, RTL."""
    return [
        MissionItem(
            seq=0, current=True, frame=MAVFrame.GLOBAL,
            command=MAVCmd.NAV_WAYPOINT,
            latitude=51.3632, longitude=-0.2652, altitude=84.0,
        ),
        MissionItem(
            seq=1, command=MAVCmd.NAV_TAKEOFF,
            param1=15.0, altitude=50.0,
        ),
        MissionItem(
            seq=2, command=MAVCmd.NAV_RETURN_TO_LAUNCH,
        ),
    ]


# MAV_MISSION_ACCEPTED = 0 in the real protocol
_MAV_MISSION_ACCEPTED = 0


def _build_mock_mavutil_module() -> MagicMock:
    """Create a mock pymavlink.mavutil that includes mavlink.MAV_MISSION_ACCEPTED."""
    mock_mavutil = MagicMock()
    mock_mavutil.mavlink.MAV_MISSION_ACCEPTED = _MAV_MISSION_ACCEPTED
    return mock_mavutil


def _mock_mav_connection(
    *,
    heartbeat_ok: bool = True,
    clear_ack_type: int = _MAV_MISSION_ACCEPTED,
    final_ack_type: int = _MAV_MISSION_ACCEPTED,
    request_seqs: list[int] | None = None,
    request_timeout_after: int | None = None,
    clear_ack_none: bool = False,
    final_ack_none: bool = False,
) -> MagicMock:
    """Build a mock MAVLink connection object.

    Args:
        heartbeat_ok: Whether wait_heartbeat succeeds.
        clear_ack_type: The ack.type for the clear-mission ack.
        final_ack_type: The ack.type for the final upload ack.
        request_seqs: Sequence numbers returned by MISSION_REQUEST_INT messages.
        request_timeout_after: If set, return None after this many requests.
        clear_ack_none: If True, clear ack returns None (timeout).
        final_ack_none: If True, final ack returns None (timeout).
    """
    mav = MagicMock()
    mav.target_system = 1
    mav.target_component = 1

    if not heartbeat_ok:
        mav.wait_heartbeat.side_effect = Exception("Connection refused")
        return mav

    if request_seqs is None:
        request_seqs = [0, 1, 2]

    # Build recv_match side_effect sequence:
    # 1. clear ack
    # 2. N x MISSION_REQUEST_INT
    # 3. final ack
    recv_values: list = []

    # Clear ack
    if clear_ack_none:
        recv_values.append(None)
    else:
        recv_values.append(SimpleNamespace(type=clear_ack_type))

    # Request messages
    if request_timeout_after is not None:
        for i, seq in enumerate(request_seqs):
            if i >= request_timeout_after:
                recv_values.append(None)
                break
            recv_values.append(SimpleNamespace(seq=seq))
    else:
        for seq in request_seqs:
            recv_values.append(SimpleNamespace(seq=seq))

        # Final ack
        if final_ack_none:
            recv_values.append(None)
        else:
            recv_values.append(SimpleNamespace(type=final_ack_type))

    mav.recv_match = MagicMock(side_effect=recv_values)
    return mav


@pytest.fixture()
def mock_pymavlink():
    """Fixture that patches pymavlink in sys.modules for the duration of the test.

    Yields (mock_mavutil, set_connection) where set_connection(mav) wires up
    mock_mavutil.mavlink_connection to return `mav`.
    """
    mock_mavutil = _build_mock_mavutil_module()

    pymavlink_mock = MagicMock()
    pymavlink_mock.mavutil = mock_mavutil

    # Remove any cached pymavlink imports so upload_mission() re-imports
    saved = {}
    keys = [k for k in sys.modules if k == "pymavlink" or k.startswith("pymavlink.")]
    for k in keys:
        saved[k] = sys.modules.pop(k)

    with patch.dict(sys.modules, {
        "pymavlink": pymavlink_mock,
        "pymavlink.mavutil": mock_mavutil,
    }):
        def set_connection(mav):
            mock_mavutil.mavlink_connection.return_value = mav

        yield mock_mavutil, set_connection

    # Restore
    for k, v in saved.items():
        sys.modules[k] = v


# ── Tests ────────────────────────────────────────────────────────────


class TestUploadMission:
    def test_successful_upload(self, mock_pymavlink):
        """Full happy-path: connect, clear, send items, final ack."""
        mock_mavutil, set_conn = mock_pymavlink
        items = _sample_items()
        mav = _mock_mav_connection(request_seqs=[0, 1, 2])
        set_conn(mav)

        upload_mission(items, connection_string="tcp:127.0.0.1:5760")

        mav.wait_heartbeat.assert_called_once()
        mav.waypoint_clear_all_send.assert_called_once()
        mav.waypoint_count_send.assert_called_once_with(3)
        assert mav.mav.mission_item_int_send.call_count == 3

    def test_connection_refused(self, mock_pymavlink):
        """Should raise UploadError when heartbeat times out."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(heartbeat_ok=False)
        set_conn(mav)

        with pytest.raises(UploadError, match="Failed to connect"):
            upload_mission(_sample_items())

    def test_mission_rejected_nonzero_ack(self, mock_pymavlink):
        """Non-zero final ack.type after upload should raise UploadError."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(request_seqs=[0, 1, 2], final_ack_type=1)
        set_conn(mav)

        with pytest.raises(UploadError, match="Mission rejected"):
            upload_mission(_sample_items())

    def test_clear_all_no_ack(self, mock_pymavlink):
        """If clear_all gets no ack (None), should raise UploadError."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(clear_ack_none=True)
        set_conn(mav)

        with pytest.raises(UploadError, match="No acknowledgement received when clearing"):
            upload_mission(_sample_items())

    def test_clear_all_rejected(self, mock_pymavlink):
        """If clear_all ack has non-zero type, should raise UploadError."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(clear_ack_type=1)
        set_conn(mav)

        with pytest.raises(UploadError, match="Clear-mission rejected"):
            upload_mission(_sample_items())

    def test_timeout_on_mission_request(self, mock_pymavlink):
        """Timeout waiting for MISSION_REQUEST_INT should raise UploadError."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(request_timeout_after=0)
        set_conn(mav)

        with pytest.raises(UploadError, match="Timeout waiting for MISSION_REQUEST_INT"):
            upload_mission(_sample_items())

    def test_no_final_ack_raises(self, mock_pymavlink):
        """If the final MISSION_ACK is None (timeout), should raise UploadError."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(request_seqs=[0, 1, 2], final_ack_none=True)
        set_conn(mav)

        with pytest.raises(UploadError, match="No acknowledgement received after uploading"):
            upload_mission(_sample_items())

    def test_connection_closed_in_finally(self, mock_pymavlink):
        """The connection should be closed even when upload succeeds."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(request_seqs=[0, 1, 2])
        set_conn(mav)

        upload_mission(_sample_items())

        mav.close.assert_called_once()

    def test_connection_closed_on_error(self, mock_pymavlink):
        """The connection should be closed even when upload fails."""
        _, set_conn = mock_pymavlink
        mav = _mock_mav_connection(request_seqs=[0, 1, 2], final_ack_type=1)
        set_conn(mav)

        with pytest.raises(UploadError):
            upload_mission(_sample_items())

        mav.close.assert_called_once()

    def test_pymavlink_not_installed(self):
        """If pymavlink is not importable, should raise UploadError."""
        saved = {}
        keys = [k for k in sys.modules if k == "pymavlink" or k.startswith("pymavlink.")]
        for k in keys:
            saved[k] = sys.modules.pop(k)

        try:
            with patch.dict(sys.modules, {"pymavlink": None}):
                with pytest.raises(UploadError, match="pymavlink is not installed"):
                    upload_mission(_sample_items())
        finally:
            for k, v in saved.items():
                sys.modules[k] = v


class TestUploadItemContent:
    """Verify the data sent via mission_item_int_send matches the MissionItem fields."""

    def test_item_fields_passed_correctly(self, mock_pymavlink):
        _, set_conn = mock_pymavlink
        items = _sample_items()
        mav = _mock_mav_connection(request_seqs=[0, 1, 2])
        set_conn(mav)

        upload_mission(items)

        # Check the first mission_item_int_send call (HOME item)
        call_args = mav.mav.mission_item_int_send.call_args_list[0]
        args = call_args[0]
        # Args: target_sys, target_comp, seq, frame, cmd, current, autocont,
        #       p1, p2, p3, p4, lat_int, lon_int, alt
        assert args[2] == 0                                      # seq
        assert args[3] == int(MAVFrame.GLOBAL)                   # frame
        assert args[4] == int(MAVCmd.NAV_WAYPOINT)               # command
        assert args[5] == 1                                      # current (True -> 1)
        assert args[11] == int(round(51.3632 * _LAT_LON_SCALE)) # latitude as int32
        assert args[12] == int(round(-0.2652 * _LAT_LON_SCALE)) # longitude as int32
        assert args[13] == 84.0                                  # altitude (float)
