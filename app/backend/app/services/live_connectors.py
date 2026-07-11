"""Read-only connectors for operator-owned search data credentials.

The adapters never persist access or refresh tokens. Operators provide secrets by
environment variable; the returned snapshots carry an explicit provenance label.
"""

from __future__ import annotations

import os
from datetime import date, timedelta
from typing import Any
from urllib.parse import quote

import httpx


class ConnectorUnavailable(RuntimeError):
    """Raised when a live connector cannot run with the current configuration."""


def _env(name: str) -> str:
    return os.getenv(name, "").strip()


def _access_token(prefix: str, default_access_env: str) -> str:
    direct_token = _env(default_access_env)
    if direct_token:
        return direct_token
    refresh_token = _env(f"{prefix}_REFRESH_TOKEN")
    client_id = _env(f"{prefix}_OAUTH_CLIENT_ID")
    client_secret = _env(f"{prefix}_OAUTH_CLIENT_SECRET")
    token_url = _env(f"{prefix}_OAUTH_TOKEN_URL")
    if not (refresh_token and client_id and client_secret and token_url):
        raise ConnectorUnavailable(
            f"{default_access_env} or a complete {prefix} refresh-token configuration is required."
        )
    response = httpx.post(
        token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=20,
    )
    response.raise_for_status()
    access_token = str(response.json().get("access_token") or "").strip()
    if not access_token:
        raise ConnectorUnavailable(
            "OAuth refresh response did not contain an access token."
        )
    return access_token


def fetch_gsc_snapshot(
    property_identifier: str | None, config: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Fetch a bounded read-only Search Console performance snapshot."""
    property_url = (property_identifier or "").strip()
    if not property_url:
        raise ConnectorUnavailable("A Search Console property identifier is required.")
    config = config or {}
    token = _access_token("GSC", "GSC_ACCESS_TOKEN")
    end_date = date.today() - timedelta(days=int(config.get("data_delay_days", 3)))
    start_date = end_date - timedelta(days=int(config.get("lookback_days", 28)))
    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["query", "page"],
        "type": "web",
        "rowLimit": min(max(int(config.get("row_limit", 100)), 1), 1000),
        "dataState": "final",
    }
    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{quote(property_url, safe='')}/searchAnalytics/query"
    )
    response = httpx.post(
        endpoint,
        json=body,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    response.raise_for_status()
    rows = []
    for item in response.json().get("rows", []):
        keys = item.get("keys") or []
        rows.append(
            {
                "query": keys[0] if len(keys) > 0 else None,
                "page": keys[1] if len(keys) > 1 else None,
                "clicks": item.get("clicks", 0),
                "impressions": item.get("impressions", 0),
                "ctr": item.get("ctr", 0),
                "position": item.get("position"),
            }
        )
    return {
        "source": "gsc-live-api",
        "property_identifier": property_url,
        "window": {"start_date": body["startDate"], "end_date": body["endDate"]},
        "rows": rows,
        "read_only": True,
    }


def fetch_yandex_webmaster_snapshot(
    property_identifier: str | None, config: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Fetch Yandex Webmaster host inventory and a selected host summary."""
    config = config or {}
    token = _access_token("YANDEX_WEBMASTER", "YANDEX_WEBMASTER_TOKEN")
    headers = {"Authorization": f"OAuth {token}"}
    base_url = "https://api.webmaster.yandex.net/v4"
    user_response = httpx.get(f"{base_url}/user/", headers=headers, timeout=30)
    user_response.raise_for_status()
    user_id = user_response.json().get("user_id")
    if user_id is None:
        raise ConnectorUnavailable("Yandex Webmaster did not return a user id.")
    hosts_response = httpx.get(
        f"{base_url}/user/{user_id}/hosts/", headers=headers, timeout=30
    )
    hosts_response.raise_for_status()
    hosts = hosts_response.json().get("hosts") or []
    requested_host_id = str(property_identifier or config.get("host_id") or "").strip()
    selected = next(
        (host for host in hosts if str(host.get("host_id")) == requested_host_id),
        hosts[0] if len(hosts) == 1 else None,
    )
    summary: dict[str, Any] = {}
    if selected:
        host_id = selected.get("host_id")
        summary_response = httpx.get(
            f"{base_url}/user/{user_id}/hosts/{host_id}/summary/",
            headers=headers,
            timeout=30,
        )
        summary_response.raise_for_status()
        summary = summary_response.json()
    return {
        "source": "yandex-webmaster-live-api",
        "user_id": user_id,
        "hosts": hosts,
        "selected_host": selected,
        "summary": summary,
        "read_only": True,
    }
