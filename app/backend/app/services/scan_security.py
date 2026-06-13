from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit

from fastapi import HTTPException

from ..config import Settings

BLOCKED_HOSTS = {
    "localhost",
    "localhost.localdomain",
    "metadata.google.internal",
}
BLOCKED_IPS = {
    "169.254.169.254",
    "100.100.100.200",
}


def normalize_target_url(raw_url: str, settings: Settings) -> tuple[str, str]:
    candidate = raw_url.strip()
    if not candidate:
        raise HTTPException(status_code=400, detail="URL is required.")
    if len(candidate) > settings.scanner_max_url_length:
        raise HTTPException(status_code=400, detail="URL is too long.")

    parsed = urlsplit(candidate)
    scheme = parsed.scheme.lower()
    if scheme not in settings.scanner_allowed_scheme_list():
        raise HTTPException(status_code=400, detail="Unsupported URL scheme.")
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="A valid absolute URL is required.")
    host = (parsed.hostname or "").strip().lower()
    if not host:
        raise HTTPException(status_code=400, detail="Target host is required.")
    validate_public_host(host)

    normalized = urlunsplit(
        (
            scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.query,
            "",
        )
    )
    return normalized, host


def validate_public_host(host: str) -> None:
    if host in BLOCKED_HOSTS:
        raise HTTPException(
            status_code=400, detail="Local or metadata hosts are blocked."
        )
    try:
        address = ipaddress.ip_address(host)
        _validate_public_ip(address)
        return
    except ValueError:
        pass

    try:
        results = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return

    for result in results:
        ip_text = result[4][0]
        if ip_text in BLOCKED_IPS:
            raise HTTPException(
                status_code=400, detail="Metadata service addresses are blocked."
            )
        _validate_public_ip(ipaddress.ip_address(ip_text))


def _validate_public_ip(address: ipaddress._BaseAddress) -> None:
    if (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    ):
        raise HTTPException(
            status_code=400, detail="Local or internal addresses are blocked."
        )
