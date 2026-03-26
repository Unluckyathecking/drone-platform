"""Upload missions to ArduPilot via MAVLink MISSION_ITEM_INT protocol (SITL or real vehicle).

Connects to ArduPilot, clears existing mission, uploads new mission items
using the MISSION_ITEM_INT / MISSION_REQUEST_INT protocol (int32 lat/lon
scaled by 1e7 for sub-centimetre precision).

Default connection: tcp:127.0.0.1:5760 (SITL).

Usage:
    items = build_mission(mission)
    upload_mission(items)  # uploads to SITL on localhost
    upload_mission(items, connection_string="udp:192.168.1.10:14550")  # real vehicle
"""

from __future__ import annotations

from .models import MissionItem


class UploadError(Exception):
    """Raised when mission upload fails."""


_LAT_LON_SCALE = 1e7  # INT protocol: degrees * 1e7 -> int32


def upload_mission(
    items: list[MissionItem],
    connection_string: str = "tcp:127.0.0.1:5760",
    timeout: int = 10,
) -> None:
    """Upload mission items to ArduPilot via MAVLink MISSION_ITEM_INT protocol.

    Uses MISSION_COUNT, MISSION_REQUEST_INT, and MISSION_ITEM_INT messages
    so that latitude and longitude are transmitted as int32 values (degrees
    multiplied by 1e7) instead of floats, avoiding floating-point precision
    loss.

    Args:
        items: Ordered list of MissionItems to upload.
        connection_string: MAVLink connection string (default: SITL on localhost).
        timeout: Seconds to wait for connection and acknowledgements.

    Raises:
        UploadError: If connection fails or mission is rejected.
    """
    try:
        from pymavlink import mavutil
    except ImportError as e:
        raise UploadError(
            "pymavlink is not installed. Run: pip install pymavlink"
        ) from e

    mav = None
    try:
        # Connect
        try:
            mav = mavutil.mavlink_connection(connection_string)
            mav.wait_heartbeat(timeout=timeout)
        except Exception as e:
            raise UploadError(
                f"Failed to connect to {connection_string}: {e}. "
                f"Is SITL running? Start with: sim_vehicle.py -v ArduPlane --map --console"
            ) from e

        print(
            f"Connected to vehicle "
            f"(system {mav.target_system}, component {mav.target_component})"
        )

        # Named constant for acceptance check
        mav_mission_accepted = mavutil.mavlink.MAV_MISSION_ACCEPTED

        # Clear existing mission and verify acceptance
        mav.waypoint_clear_all_send()
        ack = mav.recv_match(type="MISSION_ACK", blocking=True, timeout=timeout)
        if ack is None:
            raise UploadError("No acknowledgement received when clearing mission")
        if ack.type != mav_mission_accepted:
            raise UploadError(
                f"Clear-mission rejected by autopilot "
                f"(error code: {ack.type})"
            )

        # Send mission count
        mav.waypoint_count_send(len(items))

        # Upload each item as requested by the autopilot.
        # The autopilot drives the sequence via MISSION_REQUEST_INT; we use
        # msg.seq as the sole index so retransmit requests are handled
        # correctly (the loop counter is only a bound on total messages).
        uploaded = 0
        while uploaded < len(items):
            msg = mav.recv_match(
                type="MISSION_REQUEST_INT", blocking=True, timeout=timeout
            )
            if msg is None:
                raise UploadError(
                    f"Timeout waiting for MISSION_REQUEST_INT "
                    f"(uploaded {uploaded}/{len(items)})"
                )

            seq = msg.seq
            if seq < 0 or seq >= len(items):
                raise UploadError(
                    f"Autopilot requested out-of-range seq {seq} "
                    f"(mission has {len(items)} items)"
                )

            item = items[seq]
            mav.mav.mission_item_int_send(
                mav.target_system,
                mav.target_component,
                item.seq,
                int(item.frame),
                int(item.command),
                1 if item.current else 0,
                1 if item.autocontinue else 0,
                item.param1,
                item.param2,
                item.param3,
                item.param4,
                int(round(item.latitude * _LAT_LON_SCALE)),
                int(round(item.longitude * _LAT_LON_SCALE)),
                item.altitude,
            )

            # Only count forward progress; a retransmit of an already-sent
            # seq does not advance the counter.
            if seq == uploaded:
                uploaded += 1

        # Wait for final acknowledgement
        ack = mav.recv_match(type="MISSION_ACK", blocking=True, timeout=timeout)
        if ack is None:
            raise UploadError("No acknowledgement received after uploading mission")
        if ack.type != mav_mission_accepted:
            raise UploadError(
                f"Mission rejected by autopilot (error code: {ack.type})"
            )

        print(f"Mission uploaded successfully ({len(items)} items)")

    finally:
        if mav is not None:
            mav.close()
