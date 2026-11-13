"""
- Successful TLS connection.
- Valid certificate.
- Certificate approaching expiry.
- Expired certificate.
- DNS lookup failure.
- Connection timeout.
- Connection refused.
- TLS handshake failure.
- Certificate verification failure.
- Unexpected network errors where applicable like ConnectionResetError.
"""

import socket
import ssl
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock

import pytest

from checker import tlsChecker
from checker.results import HostCheckResult


@pytest.fixture
def tls_environment(monkeypatch):
    # Mock both context managers: no TCP connection or real TLS handshake occurs.
    connection = MagicMock()
    context = MagicMock()
    tls_socket = context.wrap_socket.return_value.__enter__.return_value
    tls_socket.version.return_value = "TLSv1.3"
    monkeypatch.setattr(tlsChecker.socket, "create_connection", connection)
    monkeypatch.setattr(tlsChecker.ssl, "create_default_context", Mock(return_value=context))
    monkeypatch.setattr(tlsChecker.time, "monotonic", Mock(side_effect=[100.0, 100.012346]))

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2030, 1, 1, 12, tzinfo=timezone.utc)

    monkeypatch.setattr(tlsChecker, "datetime", FixedDatetime)
    return connection, context, tls_socket


@pytest.mark.parametrize(
    "days, expected_status, expected_code, expected_message",
    [
        (60, "PASS", 200, "cert expires in 60 days"),
        (30, "WARN", 200, "cert expires in 30 days"),
        (1, "WARN", 200, "cert expires in 1 days"),
        (-1, "FAIL", None, "certificate has expired (-1 days)"),
    ],
)
def test_certificate_classification(tls_environment, days, expected_status, expected_code, expected_message):
    connection, context, tls_socket = tls_environment
    expiry = datetime(2030, 1, 1, 12, tzinfo=timezone.utc) + timedelta(days=days)
    tls_socket.getpeercert.return_value = {"notAfter": expiry.strftime("%b %d %H:%M:%S %Y GMT")}

    result = tlsChecker.tls_checker("example.com", 443, warn_days=30, timeout_sec=7)

    assert isinstance(result, HostCheckResult)
    assert result.hostname == "example.com"
    assert result.status == expected_status
    assert result.http_status_code == expected_code
    assert result.message == expected_message
    assert result.response_time_ms == 12.35
    connection.assert_called_once_with(("example.com", 443), timeout=7)
    context.wrap_socket.assert_called_once_with(
        connection.return_value.__enter__.return_value, server_hostname="example.com"
    )
    tls_socket.getpeercert.assert_called_once_with()


@pytest.mark.parametrize(
    "error, message_fragment",
    [
        (socket.gaierror("name resolution failed"), "DNS lookup failed"),
        (TimeoutError("connection timed out"), "tim"),
        (ConnectionRefusedError("connection refused"), "refused"),
        (ConnectionResetError("connection reset"), "connection reset"),
    ],
    ids=["dns", "timeout", "refused", "reset"],
)
def test_network_failure(tls_environment, error, message_fragment):
    connection, context, _ = tls_environment
    connection.side_effect = error

    result = tlsChecker.tls_checker("example.com", 443)

    assert result.status == "FAIL"
    assert result.http_status_code is None
    assert message_fragment.lower() in str(result.message).lower()
    assert result.response_time_ms == 12.35
    context.wrap_socket.assert_not_called()


@pytest.mark.parametrize(
    "error, message_fragment",
    [
        (ssl.SSLError("handshake rejected"), "TLS handshake failed"),
        (ssl.SSLCertVerificationError("certificate verify failed"), "certificate verify failed"),
    ],
    ids=["handshake", "certificate-verification"],
)
def test_tls_failure(tls_environment, error, message_fragment):
    _, context, tls_socket = tls_environment
    context.wrap_socket.side_effect = error

    result = tlsChecker.tls_checker("example.com", 443)

    assert result.status == "FAIL"
    assert result.http_status_code is None
    assert message_fragment in str(result.message)
    assert result.response_time_ms == 12.35
    tls_socket.getpeercert.assert_not_called()
