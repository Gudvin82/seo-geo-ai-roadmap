#!/usr/bin/env python3
"""Thin product CLI for the self-hosted application runtime.

This command intentionally contains no SEO/GEO analysis logic. It only calls
the scanner and unified-report API exposed by the running application.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request


def _request(
    base_url: str, path: str, method: str, session: str, payload: dict | None = None
) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "X-Scanner-Session": session},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API request failed ({exc.code}): {body}") from exc


def _scan_and_report(
    base_url: str, target: str, session: str, timeout_seconds: int
) -> dict:
    accepted = _request(
        base_url,
        "/api/v1/scanner/url-audit",
        "POST",
        session,
        {"url": target, "mode": "passive", "limitations_accepted": True},
    )
    scan_job_id = accepted["scan_job_id"]
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        status = _request(base_url, f"/api/v1/scan-jobs/{scan_job_id}", "GET", session)
        if status["status"] == "completed":
            return _request(
                base_url,
                f"/api/v1/geo-intelligence/scan-jobs/{scan_job_id}/unified-report",
                "GET",
                session,
            )
        if status["status"] in {"failed", "cancelled"}:
            raise RuntimeError(
                status.get("error_summary")
                or f"Scan job {scan_job_id} did not complete."
            )
        time.sleep(1)
    raise RuntimeError(
        f"Scan job {scan_job_id} is still running. Re-run with a longer --wait value."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the self-hosted GEO product through its API."
    )
    parser.add_argument("command", choices=("audit", "score", "roadmap", "monitor"))
    parser.add_argument(
        "target", nargs="?", help="Absolute site URL for audit, score, or roadmap."
    )
    parser.add_argument(
        "--api-url", default=os.getenv("GEO_API_URL", "http://localhost:8000")
    )
    parser.add_argument(
        "--scanner-session", default=os.getenv("GEO_SCANNER_SESSION", "")
    )
    parser.add_argument(
        "--project-id", type=int, help="Required only for monitor history."
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GEO_API_TOKEN", ""),
        help="Reserved for authenticated project commands.",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=60,
        help="Maximum seconds to wait for a passive scan.",
    )
    args = parser.parse_args()
    if args.command == "monitor":
        if not args.project_id or not args.token:
            raise SystemExit(
                "monitor requires --project-id and GEO_API_TOKEN; it reads authenticated project history."
            )
        request = urllib.request.Request(
            f"{args.api_url.rstrip('/')}/api/v1/geo-intelligence/visibility-snapshots?project_id={args.project_id}",
            headers={"Authorization": f"Bearer {args.token}"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            print(
                json.dumps(
                    json.loads(response.read().decode("utf-8")),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        return 0
    if not args.target:
        raise SystemExit(f"{args.command} requires an absolute target URL.")
    if not args.scanner_session:
        raise SystemExit(
            "Set GEO_SCANNER_SESSION to a random local session value before submitting a public scan."
        )
    report = _scan_and_report(
        args.api_url, args.target, args.scanner_session, args.wait
    )
    if args.command == "score":
        output = {
            "target_url": report["target_url"],
            "geo_score": report["geo_score"],
            "evidence": report["evidence"],
        }
    elif args.command == "roadmap":
        output = {
            "target_url": report["target_url"],
            "roadmap": report["roadmap"],
            "tasks": report["tasks"],
        }
    else:
        output = report
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
