from __future__ import annotations

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request
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
ALLOWED_PUBLIC_PORTS = {80, 443}
DEFAULT_FETCH_TIMEOUT_SECONDS = 15
DEFAULT_MAX_RESPONSE_BYTES = 2_000_000
DEFAULT_MAX_REDIRECTS = 5


def normalize_target_url(raw_url: str, settings: Settings) -> tuple[str, str]:
    normalized = normalize_public_url(raw_url, settings)
    return normalized, urlsplit(normalized).hostname or ""


def normalize_public_url(raw_url: str, settings: Settings) -> str:
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
    validate_public_port(parsed.port)

    return urlunsplit(
        (
            scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.query,
            "",
        )
    )


def validate_public_port(port: int | None) -> None:
    if port is None:
        return
    if port not in ALLOWED_PUBLIC_PORTS:
        raise HTTPException(
            status_code=400,
            detail="Only public HTTP(S) ports 80 and 443 are allowed.",
        )


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


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def safe_fetch_url_bytes(
    raw_url: str,
    settings: Settings,
    *,
    timeout: int = DEFAULT_FETCH_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_RESPONSE_BYTES,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    method: str | None = None,
) -> tuple[bytes, str, str, list[str]]:
    opener = urllib.request.build_opener(_NoRedirectHandler)
    current_url = normalize_public_url(raw_url, settings)
    redirect_chain = [current_url]

    for _ in range(max_redirects + 1):
        request = urllib.request.Request(
            current_url,
            data=data,
            headers=headers or {},
            method=method,
        )
        try:
            with opener.open(request, timeout=timeout) as response:
                final_url = normalize_public_url(response.geturl(), settings)
                content_type = response.headers.get("Content-Type", "")
                body = _read_limited_response(response, max_bytes)
                if final_url != redirect_chain[-1]:
                    redirect_chain.append(final_url)
                return body, content_type, final_url, redirect_chain
        except urllib.error.HTTPError as exc:
            if exc.code in {301, 302, 303, 307, 308}:
                location = exc.headers.get("Location")
                if not location:
                    raise HTTPException(
                        status_code=400, detail="Redirect target is missing."
                    ) from exc
                next_url = urllib.parse.urljoin(current_url, location)
                current_url = normalize_public_url(next_url, settings)
                redirect_chain.append(current_url)
                continue
            raise
    raise HTTPException(status_code=400, detail="Too many redirects.")


def safe_fetch_url_text(
    raw_url: str,
    settings: Settings,
    *,
    timeout: int = DEFAULT_FETCH_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_RESPONSE_BYTES,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    method: str | None = None,
) -> tuple[str, str, list[str]]:
    body, _content_type, final_url, redirect_chain = safe_fetch_url_bytes(
        raw_url,
        settings,
        timeout=timeout,
        max_bytes=max_bytes,
        max_redirects=max_redirects,
        headers=headers,
        data=data,
        method=method,
    )
    return body.decode("utf-8", errors="replace"), final_url, redirect_chain


def _read_limited_response(response, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, max_bytes - total + 1))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(
                status_code=400, detail="Remote response exceeds scanner size limit."
            )
    return b"".join(chunks)
