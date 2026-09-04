#!/usr/bin/env python3
"""Submit operator-approved URLs to IndexNow and optionally verify availability."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlparse

ENDPOINT = "https://api.indexnow.org/indexnow"


def build_payload(
    host: str, key: str, urls: list[str], key_location: str | None
) -> dict:
    if not key or len(key) < 8:
        raise ValueError("IndexNow key must contain at least 8 characters")
    normalized_host = host.lower().strip()
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != normalized_host:
            raise ValueError("Every URL must use HTTPS and match --host")
    payload = {"host": normalized_host, "key": key, "urlList": urls}
    if key_location:
        parsed_key = urlparse(key_location)
        if parsed_key.scheme != "https" or parsed_key.hostname != normalized_host:
            raise ValueError("--key-location must use HTTPS and match --host")
        payload["keyLocation"] = key_location
    return payload


def submit(payload: dict, timeout: float) -> dict:
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"status": "accepted", "http_status": response.status}
    except urllib.error.HTTPError as exc:
        return {"status": "rejected", "http_status": exc.code, "detail": exc.reason}


def verify_urls(urls: list[str], timeout: float) -> list[dict]:
    results = []
    for url in urls:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Discoverability-PostPublish/6.9.6"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                results.append(
                    {
                        "url": url,
                        "reachable": 200 <= response.status < 400,
                        "http_status": response.status,
                    }
                )
        except (urllib.error.URLError, TimeoutError) as exc:
            results.append({"url": url, "reachable": False, "error": str(exc)})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow.")
    parser.add_argument("--host", required=True)
    parser.add_argument(
        "--key",
        help="IndexNow key. Prefer INDEXNOW_KEY so the value is not exposed in command history.",
    )
    parser.add_argument("--url", action="append", required=True)
    parser.add_argument("--key-location")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    try:
        payload = build_payload(
            args.host,
            args.key or os.environ.get("INDEXNOW_KEY", ""),
            args.url,
            args.key_location,
        )
    except ValueError as exc:
        parser.error(str(exc))
    result = {
        "schema_version": "v6.9.6",
        "source": "indexnow-live" if not args.dry_run else "indexnow-dry-run",
        "host": payload["host"],
        "submitted_urls": payload["urlList"],
        "submission": {"status": "not_sent"}
        if args.dry_run
        else submit(payload, args.timeout),
        "verification": []
        if args.dry_run or not args.verify
        else verify_urls(args.url, args.timeout),
        "boundary": "IndexNow acceptance and URL reachability do not guarantee indexing or rankings.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["submission"]["status"] != "rejected" else 1


if __name__ == "__main__":
    raise SystemExit(main())
