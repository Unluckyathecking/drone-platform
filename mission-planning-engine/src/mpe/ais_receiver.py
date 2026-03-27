"""AIS receiver -- consumes AIS NMEA data and feeds the vessel tracker.

Supports two input modes:
- UDP socket (for AIS-catcher or other local NMEA sources on the boat)
- Direct NMEA sentence decoding (for testing with recorded data)

pyais is an **optional** dependency.  The receiver raises ``AISError`` at
decode time (not import time) if pyais is missing.  The VesselTracker
itself is pure Python and always available.
"""

from __future__ import annotations

import logging
import socket
import threading

from mpe.vessel_tracker import VesselTracker

logger = logging.getLogger(__name__)


class AISError(Exception):
    """Raised when AIS receiver encounters an error."""


def _require_pyais():
    """Return the ``pyais`` module or raise ``AISError``."""
    try:
        import pyais
        return pyais
    except ImportError as exc:
        raise AISError(
            "pyais is not installed. Install with: pip install 'mission-planning-engine[ais]'"
        ) from exc


class AISReceiver:
    """Receives AIS NMEA sentences and updates a VesselTracker.

    Parameters
    ----------
    tracker:
        VesselTracker instance to update with decoded positions.
    host:
        UDP listen address (default ``"0.0.0.0"``).
    port:
        UDP listen port (default 5050, matches AIS-catcher default output).
    """

    def __init__(
        self,
        tracker: VesselTracker,
        host: str = "0.0.0.0",
        port: int = 5050,
    ) -> None:
        self._tracker = tracker
        self._host = host
        self._port = port
        self._running = False
        self._thread: threading.Thread | None = None

    def decode_nmea(self, *nmea_sentences: str) -> None:
        """Decode one or more NMEA sentences and update the tracker.

        Handles AIS message types:
        - 1, 2, 3: Class A position report
        - 5: Static and voyage data (often multi-sentence)
        - 18: Class B position report
        - 24: Class B static data

        Multi-sentence messages (e.g. type 5) should be passed as
        multiple positional arguments so pyais can reassemble them.

        Parameters
        ----------
        *nmea_sentences:
            One or more raw NMEA strings (e.g. ``"!AIVDM,1,1,,B,..."``).
        """
        pyais = _require_pyais()

        try:
            decoded = pyais.decode(*nmea_sentences)
            msg = decoded.asdict()
        except Exception:
            return  # Skip malformed sentences silently

        mmsi = msg.get("mmsi")
        if mmsi is None:
            return

        msg_type = msg.get("msg_type", 0)

        if msg_type in (1, 2, 3):
            # status is a NavigationStatus enum in pyais -- convert to int
            raw_status = msg.get("status", 15)
            nav_status = int(raw_status) if raw_status is not None else 15
            self._tracker.update(
                mmsi=mmsi,
                latitude=msg.get("lat"),
                longitude=msg.get("lon"),
                course_over_ground=msg.get("course", 0.0),
                speed_over_ground=msg.get("speed", 0.0),
                heading=float(msg.get("heading", 0)),
                nav_status=nav_status,
            )
        elif msg_type == 5:
            # pyais uses "ship_type" (not "shiptype") in asdict()
            raw_ship_type = msg.get("ship_type", 0)
            ship_type_val = int(raw_ship_type) if raw_ship_type is not None else 0
            self._tracker.update(
                mmsi=mmsi,
                vessel_name=(msg.get("shipname") or "").strip(),
                callsign=(msg.get("callsign") or "").strip(),
                imo_number=msg.get("imo", 0),
                ship_type=ship_type_val,
                destination=(msg.get("destination") or "").strip(),
            )
        elif msg_type == 18:
            self._tracker.update(
                mmsi=mmsi,
                latitude=msg.get("lat"),
                longitude=msg.get("lon"),
                course_over_ground=msg.get("course", 0.0),
                speed_over_ground=msg.get("speed", 0.0),
                heading=msg.get("heading", 0.0),
            )
        elif msg_type == 24:
            update_kwargs: dict = {}
            if msg.get("shipname"):
                update_kwargs["vessel_name"] = msg["shipname"].strip()
            if msg.get("callsign"):
                update_kwargs["callsign"] = msg["callsign"].strip()
            if msg.get("ship_type"):
                update_kwargs["ship_type"] = int(msg["ship_type"])
            if update_kwargs:
                self._tracker.update(mmsi=mmsi, **update_kwargs)

    def start_udp(self) -> None:
        """Start listening for NMEA sentences on UDP in a background thread."""
        self._running = True
        self._thread = threading.Thread(target=self._udp_loop, daemon=True)
        self._thread.start()
        logger.info("AIS UDP receiver started on %s:%d", self._host, self._port)

    def stop(self) -> None:
        """Stop the UDP listener."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        logger.info("AIS receiver stopped")

    def _udp_loop(self) -> None:
        """Internal: blocking UDP receive loop."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.settimeout(1.0)

        while self._running:
            try:
                data, _ = sock.recvfrom(4096)
                for line in data.decode("ascii", errors="ignore").strip().splitlines():
                    if line.startswith("!"):
                        self.decode_nmea(line)
            except socket.timeout:
                continue
            except Exception:
                logger.exception("Error in AIS UDP receive loop")
                continue

        sock.close()
