"""Upload missions to ArduPilot via MAVLink (SITL or real vehicle).

Connects to ArduPilot, clears existing mission, uploads new mission items.
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


def upload_mission(
    items: list[MissionItem],
    connection_string: str = "tcp:127.0.0.1:5760",
    timeout: int = 10,
) -> None:
    """Upload mission items to ArduPilot via MAVLink.

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

    # Connect
    try:
        mav = mavutil.mavlink_connection(connection_string)
        mav.wait_heartbeat(timeout=timeout)
    except Exception as e:
        raise UploadError(
            f"Failed to connect to {connection_string}: {e}. "
            f"Is SITL running? Start with: sim_vehicle.py -v ArduPlane --map --console"
        ) from e

    print(f"Connected to vehicle (system {mav.target_system}, component {mav.target_component})")

    # Clear existing mission
    mav.waypoint_clear_all_send()
    ack = mav.recv_match(type="MISSION_ACK", blocking=True, timeout=timeout)
    if ack is None:
        raise UploadError("No acknowledgement received when clearing mission")

    # Send mission count
    mav.waypoint_count_send(len(items))

    # Upload each item as requested by the autopilot
    for i in range(len(items)):
        msg = mav.recv_match(type="MISSION_REQUEST", blocking=True, timeout=timeout)
        if msg is None:
            raise UploadError(f"Timeout waiting for MISSION_REQUEST for item {i}")

        item = items[msg.seq]
        mav.mav.mission_item_send(
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
            item.latitude,
            item.longitude,
            item.altitude,
        )

    # Wait for final acknowledgement
    ack = mav.recv_match(type="MISSION_ACK", blocking=True, timeout=timeout)
    if ack is None:
        raise UploadError("No acknowledgement received after uploading mission")
    if ack.type != 0:  # MAV_MISSION_ACCEPTED = 0
        raise UploadError(f"Mission rejected by autopilot (error code: {ack.type})")

    print(f"Mission uploaded successfully ({len(items)} items)")
