#!/usr/bin/env python3
"""Fetch or validate Chrome UX Report field data."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import crux_field_data_report  # noqa: E402


def _live_payload(url: str, api_key: str) -> dict:
    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"
    request = urllib.request.Request(
        f"{endpoint}?key={urllib.parse.quote(api_key)}",
        data=json.dumps({"url": url}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(
        request, timeout=30
    ) as response:  # pragma: no cover - network path
        return json.loads(response.read().decode("utf-8"))


def _starter_payload(url: str) -> dict:
    return {
        "url": url,
        "record": {
            "urlNormalizationDetails": {"originalUrl": url},
            "metrics": {
                "largest_contentful_paint": {"percentiles": {"p75": 2800}},
                "interaction_to_next_paint": {"percentiles": {"p75": 240}},
                "cumulative_layout_shift": {"percentiles": {"p75": 0.12}},
            },
        },
        "source": "crux-starter",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch or validate CrUX field data.")
    parser.add_argument("--url", help="Public URL to query")
    parser.add_argument("--sample-file", help="Path to a saved CrUX JSON payload")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    if not args.url and not args.sample_file:
        parser.error("Either --url or --sample-file is required.")

    if args.sample_file:
        payload = json.loads(Path(args.sample_file).read_text(encoding="utf-8"))
    else:
        api_key = os.environ.get("CRUX_API_KEY", "").strip()
        payload = (
            _live_payload(args.url, api_key) if api_key else _starter_payload(args.url)
        )

    report = crux_field_data_report(payload)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {report['status'].upper()}")
        print(f"Scope: {report['collection_scope']}")
        print("Metrics:")
        for key, value in report["metrics"].items():
            print(f"- {key}: p75={value['p75']} threshold={value['good_threshold']}")
        if report["warnings"]:
            print("Warnings:")
            for item in report["warnings"]:
                print(f"- {item}")
        print(f"Recommendation: {report['recommendation']}")
        print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] in {"pass", "warn"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
