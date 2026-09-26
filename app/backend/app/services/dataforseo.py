"""Credential-gated, read-only DataForSEO research connectors.

All provider calls are explicit billable operations. API credentials are read
from the process environment and are never copied into snapshots or logs.
"""

from __future__ import annotations

import base64
import json
import math
import os
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

import httpx


class DataForSEOUnavailable(RuntimeError):
    """Raised when a DataForSEO request cannot safely be completed."""

    def __init__(self, message: str, *, request_started: bool = False) -> None:
        super().__init__(message)
        self.request_started = request_started


FLOW_ENDPOINTS = {
    "keyword_research": "/v3/keywords_data/google_ads/search_volume/live",
    "rank_tracking": "/v3/serp/google/organic/live/advanced",
    "competitor_intelligence": "/v3/dataforseo_labs/google/competitors_domain/live",
    "backlink_intelligence": "/v3/backlinks/summary/live",
}

FLOW_CATEGORIES = {
    "keyword_research": "keyword_metrics",
    "rank_tracking": "organic_serp",
    "competitor_intelligence": "domain_competitors",
    "backlink_intelligence": "backlink_profile",
}


def _domain_target(value: str) -> str:
    candidate = value.strip()
    parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
    hostname = (parsed.hostname or "").lower().rstrip(".")
    if not hostname:
        raise DataForSEOUnavailable(
            "Set a valid project domain in the integration property identifier."
        )
    return hostname.removeprefix("www.")


def _int_setting(
    config: dict[str, Any], key: str, default: int, low: int, high: int
) -> int:
    try:
        value = int(config.get(key, default))
    except (TypeError, ValueError) as exc:
        raise DataForSEOUnavailable(f"Invalid DataForSEO setting '{key}'.") from exc
    if not low <= value <= high:
        raise DataForSEOUnavailable(f"DataForSEO setting '{key}' is out of range.")
    return value


def _credentials() -> tuple[str, str]:
    login = os.getenv("DATAFORSEO_LOGIN", "").strip()
    password = os.getenv("DATAFORSEO_PASSWORD", "").strip()
    if not login or not password:
        raise DataForSEOUnavailable(
            "Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD to enable live research."
        )
    return login, password


def _bounded_config(config: dict[str, Any]) -> dict[str, Any]:
    if config.get("allow_billable_requests") is not True:
        raise DataForSEOUnavailable(
            "Billable DataForSEO calls are disabled. Set allow_billable_requests=true after approving provider costs."
        )
    try:
        budget = float(config.get("approved_daily_budget_usd", 0))
        max_requests = int(config.get("max_requests_per_day", 5))
    except (TypeError, ValueError) as exc:
        raise DataForSEOUnavailable(
            "Invalid DataForSEO budget or request limit."
        ) from exc
    if not math.isfinite(budget) or budget <= 0 or max_requests < 1:
        raise DataForSEOUnavailable(
            "Set a positive approved_daily_budget_usd and max_requests_per_day."
        )
    if max_requests > 100:
        raise DataForSEOUnavailable("max_requests_per_day cannot exceed 100.")
    return {
        "approved_daily_budget_usd": budget,
        "max_requests_per_day": max_requests,
    }


def _request(endpoint: str, body: dict[str, Any]) -> dict[str, Any]:
    login, password = _credentials()
    token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        # Do not retry billable POSTs: a timeout can happen after the provider
        # accepted and charged the first request, so retrying could double-bill.
        response = httpx.post(
            f"https://api.dataforseo.com{endpoint}",
            json=[body],
            headers=headers,
            timeout=30.0,
            follow_redirects=False,
            trust_env=False,
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.TimeoutException as exc:
        raise DataForSEOUnavailable(
            "DataForSEO timed out; billing outcome is unknown. Check the provider account before retrying.",
            request_started=True,
        ) from exc
    except httpx.TransportError as exc:
        raise DataForSEOUnavailable(
            "DataForSEO transport failed; billing outcome may be unknown. Check the provider account before retrying.",
            request_started=True,
        ) from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        raise DataForSEOUnavailable(
            f"DataForSEO HTTP request failed with status {status}; check provider billing before retrying.",
            request_started=True,
        ) from exc
    except ValueError as exc:
        raise DataForSEOUnavailable(
            "DataForSEO returned an unreadable response; billing outcome may be unknown.",
            request_started=True,
        ) from exc

    if not isinstance(payload, dict):
        raise DataForSEOUnavailable(
            "DataForSEO returned an invalid response; billing outcome may be unknown.",
            request_started=True,
        )
    try:
        status_code = int(payload.get("status_code", 0))
    except (TypeError, ValueError) as exc:
        raise DataForSEOUnavailable(
            "DataForSEO returned an invalid status; billing outcome may be unknown.",
            request_started=True,
        ) from exc
    tasks = payload.get("tasks") or []
    if (
        status_code != 20000
        or not isinstance(tasks, list)
        or not tasks
        or not isinstance(tasks[0], dict)
    ):
        raise DataForSEOUnavailable(
            "DataForSEO returned an unsuccessful response. Check provider diagnostics and credentials.",
            request_started=True,
        )
    task = tasks[0]
    try:
        task_status = int(task.get("status_code", 0))
    except (TypeError, ValueError) as exc:
        raise DataForSEOUnavailable(
            "DataForSEO returned an invalid task status; billing outcome may be unknown.",
            request_started=True,
        ) from exc
    if task_status != 20000:
        raise DataForSEOUnavailable(
            "DataForSEO task failed. Check the request scope and provider account.",
            request_started=True,
        )
    return payload


def _provider_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = payload.get("tasks") or []
    if not isinstance(tasks, list) or not tasks or not isinstance(tasks[0], dict):
        return []
    results = tasks[0].get("result") or []
    if isinstance(results, dict):
        results = [results]
    if not isinstance(results, list):
        return []
    rows: list[dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        items = result.get("items")
        if isinstance(items, list):
            rows.extend(item for item in items if isinstance(item, dict))
        else:
            rows.append(result)
        if len(rows) >= 100:
            break
    return rows[:100]


def _canonical_finding(
    flow: str,
    rows: list[dict[str, Any]],
    *,
    observed_at: str,
    market: str,
    language: str,
    reference: str,
) -> dict[str, Any]:
    evidence = []
    for index, row in enumerate(rows[:100], start=1):
        evidence.append(
            {
                "id": f"dataforseo:{flow}:{index}",
                "observation": json.dumps(row, ensure_ascii=False, sort_keys=True)[
                    :4000
                ],
                "source": "DataForSEO API",
                "evidence_type": "provider-derived",
                "confidence": 0.95,
                "timestamp": observed_at,
                "verification_method": "DataForSEO authenticated read-only API response",
                "reference": reference,
                "provider": "dataforseo",
                "market": market,
                "language": language,
            }
        )
    if not evidence:
        evidence.append(
            {
                "id": f"dataforseo:{flow}:empty",
                "observation": "The provider request succeeded but returned no result rows for this scope.",
                "source": "DataForSEO API",
                "evidence_type": "provider-derived",
                "confidence": 0.95,
                "timestamp": observed_at,
                "verification_method": "DataForSEO authenticated read-only API response",
                "reference": reference,
            }
        )
    return {
        "id": f"dataforseo:{flow}:{observed_at}",
        "category": FLOW_CATEGORIES[flow],
        "observation": f"DataForSEO returned {len(rows)} provider-derived rows for {flow}.",
        "evidence": evidence,
        "source": "DataForSEO API",
        "evidence_type": "provider-derived",
        "confidence": 0.95,
        "timestamp": observed_at,
        "verification_method": "DataForSEO authenticated read-only API response",
        "recommendation": "Review provider data against first-party analytics and the project context before prioritizing work.",
        "priority": {"impact": 2, "effort": 1, "score": 50, "label": "review"},
    }


def fetch_dataforseo_snapshot(
    flow: str,
    *,
    target: str,
    config: dict[str, Any] | None = None,
    market: str = "",
    language: str = "",
    project_context: dict[str, Any] | None = None,
    spent_today_usd: float = 0.0,
    requests_today: int = 0,
) -> dict[str, Any]:
    """Run one bounded provider flow and return canonical evidence metadata."""
    if flow not in FLOW_ENDPOINTS:
        raise DataForSEOUnavailable(f"Unsupported DataForSEO flow '{flow}'.")
    config = config or {}
    context = project_context or {}
    policy = _bounded_config(config)
    if requests_today >= policy["max_requests_per_day"]:
        raise DataForSEOUnavailable("DataForSEO daily request limit has been reached.")
    if spent_today_usd >= policy["approved_daily_budget_usd"]:
        raise DataForSEOUnavailable(
            "DataForSEO approved daily budget has been reached."
        )

    body: dict[str, Any] = {}
    location_code = config.get("location_code")
    location_name = config.get("location_name")
    language_code = config.get("language_code")
    include_search_location = flow != "backlink_intelligence"
    if include_search_location and location_code is not None:
        try:
            parsed_location_code = int(location_code)
        except (TypeError, ValueError) as exc:
            raise DataForSEOUnavailable("location_code must be an integer.") from exc
        if parsed_location_code <= 0:
            raise DataForSEOUnavailable("location_code must be positive.")
        body["location_code"] = parsed_location_code
    elif include_search_location and location_name:
        body["location_name"] = str(location_name)[:160]
    if include_search_location and language_code:
        body["language_code"] = str(language_code)[:16]
    elif include_search_location and language:
        if len(str(language).strip()) <= 3:
            body["language_code"] = str(language).strip().lower()
        else:
            body["language_name"] = str(language)[:64]
    cache_ttl = _int_setting(config, "cache_ttl_seconds", 21600, 60, 86400)

    target_value = str(target or "").strip()
    if flow == "keyword_research":
        keywords = config.get("keywords") or context.get("seed_keywords") or []
        if not isinstance(keywords, list):
            raise DataForSEOUnavailable("keywords must be a list of strings.")
        keywords = [str(item).strip()[:80] for item in keywords if str(item).strip()]
        if not 1 <= len(keywords) <= 30:
            raise DataForSEOUnavailable("Provide between 1 and 30 seed keywords.")
        if any(len(keyword.split()) > 10 for keyword in keywords):
            raise DataForSEOUnavailable("Each keyword can contain at most 10 words.")
        if not location_code and not location_name:
            raise DataForSEOUnavailable(
                "Keyword metrics require an explicit location_code or location_name."
            )
        body["keywords"] = keywords
        body["tag"] = "seo-geo-ai-roadmap:keyword_research"
    elif flow == "rank_tracking":
        keyword = str(config.get("keyword") or "").strip()
        if not keyword:
            raise DataForSEOUnavailable(
                "Set a query in the integration config as 'keyword'."
            )
        if not location_code and not location_name:
            raise DataForSEOUnavailable(
                "SERP tracking requires an explicit location_code or location_name."
            )
        body.update(
            {
                "keyword": keyword[:160],
                "depth": _int_setting(config, "depth", 10, 10, 30),
            }
        )
        body["tag"] = "seo-geo-ai-roadmap:rank_tracking"
        if target_value:
            body["target"] = _domain_target(target_value)
    elif flow == "competitor_intelligence":
        if not target_value:
            raise DataForSEOUnavailable(
                "Set the project domain as the integration property identifier."
            )
        target_value = _domain_target(target_value)
        body.update(
            {"target": target_value, "limit": _int_setting(config, "limit", 20, 1, 100)}
        )
        body["tag"] = "seo-geo-ai-roadmap:competitor_intelligence"
        if not location_code and not location_name:
            raise DataForSEOUnavailable(
                "Competitor analysis requires an explicit location_code or location_name."
            )
    elif flow == "backlink_intelligence":
        if not target_value:
            raise DataForSEOUnavailable(
                "Set the project domain as the integration property identifier."
            )
        target_value = _domain_target(target_value)
        body["target"] = target_value
        body["tag"] = "seo-geo-ai-roadmap:backlink_intelligence"

    payload = _request(FLOW_ENDPOINTS[flow], body)
    tasks = payload.get("tasks") or []
    task = tasks[0] if tasks else {}
    rows = _provider_rows(payload)
    now = datetime.now(timezone.utc).isoformat()
    raw_cost = task.get("cost")
    if raw_cost is None:
        raw_cost = payload.get("cost")
    try:
        cost = float(raw_cost)
    except (TypeError, ValueError) as exc:
        raise DataForSEOUnavailable(
            "DataForSEO omitted its request cost; billing outcome is unknown. Check the provider account.",
            request_started=True,
        ) from exc
    if not math.isfinite(cost) or cost < 0:
        raise DataForSEOUnavailable(
            "DataForSEO returned an invalid request cost; billing outcome is unknown. Check the provider account.",
            request_started=True,
        )
    new_spend = round(spent_today_usd + cost, 8)
    return {
        "source": "dataforseo-live-api",
        "provider": "dataforseo",
        "flow": flow,
        "provider_task_id": task.get("id"),
        "market": market,
        "language": language,
        "location_code": body.get("location_code"),
        "location_name": body.get("location_name"),
        "language_code": body.get("language_code"),
        "observed_at": now,
        "cost_usd": cost,
        "spend_today_usd": new_spend,
        "approved_daily_budget_usd": policy["approved_daily_budget_usd"],
        "budget_overrun": new_spend > policy["approved_daily_budget_usd"],
        "requests_today": requests_today + 1,
        "daily_request_limit": policy["max_requests_per_day"],
        "cache_ttl_seconds": cache_ttl,
        "cache_hit": False,
        "rows": rows,
        "findings": [
            _canonical_finding(
                flow,
                rows,
                observed_at=now,
                market=market,
                language=language,
                reference=f"DataForSEO task {task.get('id') or 'response'}",
            )
        ],
        "project_context": {
            "competitors": context.get("competitors", []),
            "goals": context.get("goals", []),
            "key_pages": context.get("key_pages", []),
        },
        "provenance": {
            "provider": "DataForSEO",
            "evidence_type": "provider-derived",
            "verification_method": "authenticated read-only DataForSEO API request",
            "request_endpoint": FLOW_ENDPOINTS[flow],
        },
        "read_only": True,
        "billable": True,
    }
