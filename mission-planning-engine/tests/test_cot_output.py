"""Tests for the CoT plain-socket output module.

All network calls are mocked -- no real sockets are opened.
"""

from __future__ import annotations

import socket
from unittest.mock import MagicMock, patch

import pytest

from mpe.cot_output import CoTOutput


# ---------------------------------------------------------------------------
# Construction / URL parsing
# ---------------------------------------------------------------------------


class TestCoTOutputCreation:
    """Test CoTOutput creation and URL parsing."""

    def test_default_url(self) -> None:
        out = CoTOutput()

        assert out._url == "udp+wo://239.2.3.1:6969"
        assert out._scheme == "udp"
        assert out._host == "239.2.3.1"
        assert out._port == 6969

    def test_udp_unicast_url(self) -> None:
        out = CoTOutput("udp://192.168.1.50:4242")

        assert out._scheme == "udp"
        assert out._host == "192.168.1.50"
        assert out._port == 4242

    def test_tcp_url(self) -> None:
        out = CoTOutput("tcp://takserver.local:8087")

        assert out._scheme == "tcp"
        assert out._host == "takserver.local"
        assert out._port == 8087

    def test_udp_write_only_url(self) -> None:
        out = CoTOutput("udp+wo://239.2.3.1:6969")

        assert out._scheme == "udp"
        assert out._host == "239.2.3.1"
        assert out._port == 6969


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestCoTOutputStats:
    """Test CoTOutput.stats initial state and structure."""

    def test_initial_stats(self) -> None:
        out = CoTOutput()
        stats = out.stats

        assert stats["url"] == "udp+wo://239.2.3.1:6969"
        assert stats["connected"] is False
        assert stats["sent"] == 0
        assert stats["errors"] == 0

    def test_stats_returns_dict(self) -> None:
        out = CoTOutput()

        assert isinstance(out.stats, dict)
        assert set(out.stats.keys()) == {"url", "connected", "sent", "errors"}


# ---------------------------------------------------------------------------
# UDP connect
# ---------------------------------------------------------------------------


class TestCoTOutputConnect:
    """Test CoTOutput.connect with mocked sockets."""

    @patch("mpe.cot_output.socket.socket")
    def test_udp_connect(self, mock_socket_cls: MagicMock) -> None:
        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        mock_socket_cls.assert_called_once_with(
            socket.AF_INET, socket.SOCK_DGRAM,
        )
        assert out._connected is True

    @patch("mpe.cot_output.socket.socket")
    def test_udp_multicast_sets_ttl(self, mock_socket_cls: MagicMock) -> None:
        """Multicast addresses (224-239) should set IP_MULTICAST_TTL."""
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://239.2.3.1:6969")
        out.connect()

        mock_sock.setsockopt.assert_called_once_with(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32,
        )
        assert out._connected is True

    @patch("mpe.cot_output.socket.socket")
    def test_udp_unicast_no_ttl(self, mock_socket_cls: MagicMock) -> None:
        """Unicast addresses should NOT set multicast TTL."""
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://192.168.1.1:4242")
        out.connect()

        mock_sock.setsockopt.assert_not_called()

    @patch("mpe.cot_output.socket.socket")
    def test_tcp_connect(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("tcp://takserver:8087")
        out.connect()

        mock_socket_cls.assert_called_once_with(
            socket.AF_INET, socket.SOCK_STREAM,
        )
        mock_sock.settimeout.assert_called_once_with(5.0)
        mock_sock.connect.assert_called_once_with(("takserver", 8087))
        assert out._connected is True

    @patch("mpe.cot_output.socket.socket")
    def test_connect_failure_sets_not_connected(
        self, mock_socket_cls: MagicMock,
    ) -> None:
        mock_socket_cls.side_effect = OSError("network down")

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        assert out._connected is False


# ---------------------------------------------------------------------------
# Send
# ---------------------------------------------------------------------------


class TestCoTOutputSend:
    """Test CoTOutput.send with mocked sockets."""

    @patch("mpe.cot_output.socket.socket")
    def test_udp_send(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        xml = '<event version="2.0" />'
        result = out.send(xml)

        assert result is True
        mock_sock.sendto.assert_called_once_with(
            xml.encode("utf-8"), ("10.0.0.1", 5555),
        )
        assert out._sent_count == 1

    @patch("mpe.cot_output.socket.socket")
    def test_tcp_send(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("tcp://takserver:8087")
        out.connect()

        xml = '<event version="2.0" />'
        result = out.send(xml)

        assert result is True
        mock_sock.sendall.assert_called_once_with(xml.encode("utf-8"))

    @patch("mpe.cot_output.socket.socket")
    def test_send_failure_increments_errors(
        self, mock_socket_cls: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.sendto.side_effect = OSError("send failed")

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()
        result = out.send("<event />")

        assert result is False
        assert out._error_count == 1
        assert out._connected is False

    @patch("mpe.cot_output.socket.socket")
    def test_send_when_not_connected_attempts_reconnect(
        self, mock_socket_cls: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://10.0.0.1:5555")
        # Do NOT call connect() -- send should auto-connect
        result = out.send("<event />")

        assert result is True
        assert out._connected is True
        # Socket should have been created during auto-connect
        mock_socket_cls.assert_called()

    def test_send_returns_false_when_connect_fails(self) -> None:
        out = CoTOutput("udp://10.0.0.1:5555")

        with patch("mpe.cot_output.socket.socket", side_effect=OSError("fail")):
            result = out.send("<event />")

        assert result is False


# ---------------------------------------------------------------------------
# send_batch
# ---------------------------------------------------------------------------


class TestCoTOutputSendBatch:
    """Test CoTOutput.send_batch."""

    @patch("mpe.cot_output.socket.socket")
    def test_send_batch_all_succeed(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        events = ["<event>1</event>", "<event>2</event>", "<event>3</event>"]
        sent = out.send_batch(events)

        assert sent == 3
        assert out._sent_count == 3

    @patch("mpe.cot_output.socket.socket")
    def test_send_batch_empty_list(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        sent = out.send_batch([])

        assert sent == 0

    @patch("mpe.cot_output.socket.socket")
    def test_send_batch_partial_failure(
        self, mock_socket_cls: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        # First call succeeds, second fails, third succeeds (reconnect)
        mock_sock.sendto.side_effect = [None, OSError("fail"), None]

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        events = ["<e>1</e>", "<e>2</e>", "<e>3</e>"]
        sent = out.send_batch(events)

        # First succeeds, second fails (disconnects), third reconnects and succeeds
        assert sent == 2
        assert out._error_count == 1


# ---------------------------------------------------------------------------
# Disconnect
# ---------------------------------------------------------------------------


class TestCoTOutputDisconnect:
    """Test CoTOutput.disconnect."""

    @patch("mpe.cot_output.socket.socket")
    def test_disconnect_closes_socket(self, mock_socket_cls: MagicMock) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()
        assert out._connected is True

        out.disconnect()

        mock_sock.close.assert_called_once()
        assert out._socket is None
        assert out._connected is False

    def test_disconnect_without_connect(self) -> None:
        """Disconnect on a never-connected output should not raise."""
        out = CoTOutput()
        out.disconnect()

        assert out._socket is None
        assert out._connected is False

    @patch("mpe.cot_output.socket.socket")
    def test_disconnect_handles_close_error(
        self, mock_socket_cls: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.close.side_effect = OSError("close failed")

        out = CoTOutput("udp://10.0.0.1:5555")
        out.connect()

        # Should not raise
        out.disconnect()

        assert out._socket is None
        assert out._connected is False
