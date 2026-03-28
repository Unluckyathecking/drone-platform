"""CoT output -- sends CoT XML events to TAK networks.

Simpler than cot_sender.py (which uses PyTAK's full async framework).
This module provides a plain socket-based sender for the engine's
periodic output cycle.

Supports:
- UDP unicast/multicast (udp://host:port or udp+wo://host:port)
- TCP (tcp://host:port) -- persistent connection with reconnect
"""

from __future__ import annotations

import logging
import socket
import struct
from urllib.parse import urlparse

logger = logging.getLogger("mpe.cot_output")


class CoTOutput:
    """Sends CoT XML events to a TAK endpoint."""

    def __init__(self, url: str = "udp+wo://239.2.3.1:6969") -> None:
        self._url = url
        parsed = urlparse(url.replace("+wo", ""))
        self._scheme = "udp" if "udp" in url else "tcp"
        self._host = parsed.hostname or "239.2.3.1"
        self._port = parsed.port or 6969
        self._socket: socket.socket | None = None
        self._connected = False
        self._sent_count = 0
        self._error_count = 0

    def connect(self) -> None:
        """Open the socket connection."""
        try:
            if self._scheme == "udp":
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # If multicast (224-239 range), set TTL
                first_octet = int(self._host.split(".")[0])
                if 224 <= first_octet <= 239:
                    self._socket.setsockopt(
                        socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32,
                    )
                self._connected = True
                logger.info("CoT UDP output ready: %s:%d", self._host, self._port)

            elif self._scheme == "tcp":
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.settimeout(5.0)
                self._socket.connect((self._host, self._port))
                self._connected = True
                logger.info("CoT TCP connected: %s:%d", self._host, self._port)

        except Exception:
            logger.exception("CoT output connection failed")
            self._connected = False

    def send(self, cot_xml: str) -> bool:
        """Send a single CoT XML event. Returns True on success."""
        if not self._connected or not self._socket:
            self.connect()
            if not self._connected:
                return False

        try:
            data = cot_xml.encode("utf-8")
            if self._scheme == "udp":
                self._socket.sendto(data, (self._host, self._port))
            else:
                self._socket.sendall(data)
            self._sent_count += 1
            return True
        except Exception:
            self._error_count += 1
            self._connected = False
            logger.exception("CoT send failed")
            return False

    def send_batch(self, events: list[str]) -> int:
        """Send multiple CoT events. Returns count of successfully sent."""
        sent = 0
        for xml in events:
            if self.send(xml):
                sent += 1
        return sent

    def disconnect(self) -> None:
        """Close the socket."""
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None
            self._connected = False

    @property
    def stats(self) -> dict:
        """Current sender statistics."""
        return {
            "url": self._url,
            "connected": self._connected,
            "sent": self._sent_count,
            "errors": self._error_count,
        }
