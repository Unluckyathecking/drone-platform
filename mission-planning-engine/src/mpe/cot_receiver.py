"""CoT receiver -- listens for incoming CoT events from TAK networks.

Parses incoming CoT XML, extracts entity position/type/affiliation,
and makes it available to the engine for correlation and display.

Supports:
- TCP client (connect to TAK Server, read stream)
- UDP listener (receive multicast or unicast)
"""

from __future__ import annotations

import logging
import socket
import struct
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable
from urllib.parse import urlparse

logger = logging.getLogger("mpe.cot_receiver")

# FIX #9: Maximum TCP buffer size to prevent unbounded memory growth
MAX_BUFFER_SIZE = 1_000_000  # 1 MB


@dataclass
class CotEvent:
    """A parsed incoming CoT event."""

    uid: str
    event_type: str  # e.g. "a-f-G-U-C" (friendly ground unit)
    latitude: float
    longitude: float
    altitude_hae: float = 0.0
    callsign: str = ""
    heading: float = 0.0
    speed_mps: float = 0.0
    how: str = ""  # e.g. "m-g" (machine GPS), "h-e" (human entered)
    stale: str = ""
    remarks: str = ""
    raw_xml: str = ""
    received_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @property
    def domain(self) -> str:
        """Infer domain from CoT type code.

        CoT type hierarchy: a-{affil}-{battle_dimension}-...
        Battle dimension codes: A=air, G=land, S=sea, U=subsurface.
        """
        if not self.event_type:
            return "unknown"
        parts = self.event_type.split("-")
        if len(parts) < 3:
            return "unknown"
        battle_dim = parts[2]
        return {
            "A": "air",
            "G": "land",
            "S": "sea",
            "U": "subsurface",
        }.get(battle_dim, "unknown")

    @property
    def affiliation(self) -> str:
        """Infer affiliation from CoT type code.

        Second element in the type hierarchy encodes affiliation:
        f=friendly, h=hostile, n=neutral, u=unknown, j=suspect,
        a=assumed friendly, p=pending.
        """
        if not self.event_type:
            return "unknown"
        parts = self.event_type.split("-")
        if len(parts) < 2:
            return "unknown"
        return {
            "f": "friendly",
            "h": "hostile",
            "n": "neutral",
            "u": "unknown",
            "j": "suspect",
            "a": "friendly",  # assumed friendly
            "p": "unknown",  # pending
        }.get(parts[1], "unknown")


def parse_cot_xml(xml_str: str) -> CotEvent | None:
    """Parse a CoT XML string into a CotEvent.

    Returns None if the XML is malformed or missing required fields
    (uid, point element).
    """
    try:
        root = ET.fromstring(xml_str.strip())
    except ET.ParseError:
        return None

    if root.tag != "event":
        return None

    uid = root.get("uid", "")
    event_type = root.get("type", "")
    how = root.get("how", "")
    stale = root.get("stale", "")

    if not uid:
        return None

    # Parse <point> -- required for a valid CoT position report
    point = root.find("point")
    if point is None:
        return None

    try:
        lat = float(point.get("lat", "0"))
        lon = float(point.get("lon", "0"))
        hae = float(point.get("hae", "0"))
    except (ValueError, TypeError):
        return None

    # Parse <detail> -- optional enrichment
    callsign = ""
    heading = 0.0
    speed = 0.0
    remarks = ""

    detail = root.find("detail")
    if detail is not None:
        contact = detail.find("contact")
        if contact is not None:
            callsign = contact.get("callsign", "")

        track = detail.find("track")
        if track is not None:
            try:
                heading = float(track.get("course", "0"))
                speed = float(track.get("speed", "0"))
            except (ValueError, TypeError):
                pass

        remarks_el = detail.find("remarks")
        if remarks_el is not None and remarks_el.text:
            remarks = remarks_el.text

    return CotEvent(
        uid=uid,
        event_type=event_type,
        latitude=lat,
        longitude=lon,
        altitude_hae=hae,
        callsign=callsign,
        heading=heading,
        speed_mps=speed,
        how=how,
        stale=stale,
        remarks=remarks,
        raw_xml=xml_str,
    )


class CotReceiver:
    """Receives CoT events from TAK networks.

    Parameters
    ----------
    on_event:
        Callback function invoked with each successfully parsed CotEvent.
    url:
        TAK endpoint. For TCP client mode use ``tcp://host:port``.
        For UDP listener mode use ``udp://host:port``.
    """

    def __init__(
        self,
        on_event: Callable[[CotEvent], None] | None = None,
        url: str = "tcp://0.0.0.0:8087",
    ) -> None:
        self._on_event = on_event or (lambda e: None)
        self._url = url

        # FIX #14: Use urlparse for scheme detection instead of substring check
        parsed = urlparse(url)
        self._scheme = parsed.scheme if parsed.scheme in ("tcp", "udp") else "tcp"

        self._host = parsed.hostname or "0.0.0.0"
        self._port = parsed.port or 8087

        self._running = False
        self._thread: threading.Thread | None = None
        self._events_received = 0
        self._events_parsed = 0
        self._buffer = ""  # TCP stream reassembly buffer

    def start(self) -> None:
        """Start receiving in a background daemon thread."""
        self._running = True
        self._thread = threading.Thread(
            target=self._receive_loop,
            daemon=True,
        )
        self._thread.start()
        logger.info("CoT receiver started: %s", self._url)

    def stop(self) -> None:
        """Stop the receiver and wait for the thread to finish."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        logger.info("CoT receiver stopped")

    def _receive_loop(self) -> None:
        """Main receive loop -- dispatches to TCP or UDP handler."""
        if self._scheme == "tcp":
            self._tcp_receive()
        else:
            self._udp_receive()

    def _tcp_receive(self) -> None:
        """Connect to TAK Server and read the CoT stream.

        TCP CoT is a continuous XML stream -- events arrive concatenated
        without framing.  We buffer incoming bytes and extract complete
        ``<event>...</event>`` elements as they appear.
        """
        while self._running:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5.0)
                sock.connect((self._host, self._port))
                logger.info(
                    "Connected to TAK Server at %s:%d",
                    self._host,
                    self._port,
                )

                self._buffer = ""
                while self._running:
                    try:
                        data = sock.recv(8192)
                        if not data:
                            break  # Connection closed by server
                        self._buffer += data.decode("utf-8", errors="ignore")
                        # FIX #9: Enforce buffer size limit
                        if len(self._buffer) > MAX_BUFFER_SIZE:
                            logger.error(
                                "TCP buffer exceeded %d bytes, resetting",
                                MAX_BUFFER_SIZE,
                            )
                            self._buffer = ""
                        self._process_buffer()
                    except socket.timeout:
                        continue
                    except Exception as exc:
                        logger.error("TCP receive error: %s", exc)
                        break
            except Exception as exc:
                logger.warning(
                    "TAK Server connection failed: %s, retrying in 5s",
                    exc,
                )
                time.sleep(5)
            finally:
                # FIX #7: Ensure TCP socket is always closed
                if sock is not None:
                    sock.close()

    def _udp_receive(self) -> None:
        """Listen for UDP CoT datagrams.

        Each UDP datagram is expected to contain exactly one complete
        CoT event.  Supports multicast group join when the bind address
        falls in 224.0.0.0/4.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.settimeout(1.0)

        # Join multicast group if the address is in the multicast range
        first_octet = (
            int(self._host.split(".")[0]) if self._host != "0.0.0.0" else 0
        )
        if 224 <= first_octet <= 239:
            mreq = struct.pack(
                "4sl",
                socket.inet_aton(self._host),
                socket.INADDR_ANY,
            )
            sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_ADD_MEMBERSHIP,
                mreq,
            )

        logger.info(
            "Listening for CoT on UDP %s:%d",
            self._host,
            self._port,
        )

        try:  # FIX #8: Ensure UDP socket is always closed
            while self._running:
                try:
                    data, _addr = sock.recvfrom(65535)
                    xml_str = data.decode("utf-8", errors="ignore")
                    self._events_received += 1
                    event = parse_cot_xml(xml_str)
                    if event:
                        self._events_parsed += 1
                        self._on_event(event)
                except socket.timeout:
                    continue
                except Exception as exc:
                    logger.error("UDP receive error: %s", exc)
        finally:
            sock.close()

    def _process_buffer(self) -> None:
        """Extract complete ``<event>...</event>`` elements from the TCP buffer.

        CoT over TCP is an unframed XML stream.  We scan for closing
        ``</event>`` tags and then look backwards for the matching
        ``<event`` opener.  Anything before the opener is discarded
        (inter-event whitespace or partial junk).
        """
        while "</event>" in self._buffer:
            end_idx = self._buffer.index("</event>") + len("</event>")
            start_idx = self._buffer.rfind("<event", 0, end_idx)
            if start_idx == -1:
                # No opener found -- discard everything up to end_idx
                self._buffer = self._buffer[end_idx:]
                continue

            xml_str = self._buffer[start_idx:end_idx]
            self._buffer = self._buffer[end_idx:]

            self._events_received += 1
            event = parse_cot_xml(xml_str)
            if event:
                self._events_parsed += 1
                self._on_event(event)

    @property
    def stats(self) -> dict:
        """Receiver statistics snapshot."""
        return {
            "url": self._url,
            "running": self._running,
            "events_received": self._events_received,
            "events_parsed": self._events_parsed,
        }
