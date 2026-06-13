#!/usr/bin/env python3
"""Calculate a heuristic citation-readiness score."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import (  # noqa: E402
    citability_score_report,
    fetch_url_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a citability score.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    parser.add_argument(
        "--site-type",
        choices=["saas", "local-business", "service", "ecommerce", "content"],
        help="Optional site-type hint for stronger schema expectations.",
    )
    args = parser.parse_args()

    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = citability_score_report(
        html,
        page_url=args.url,
        site_type=args.site_type,
    )
    print(f"Status: {report['status'].upper()}")
    print(f"Citability score: {report['score']}/{report['max_score']}")
    print("Breakdown:")
    for item in report["breakdown"]:
        mark = "PASS" if item["passed"] else "MISS"
        print(f"- {item['check']}: {mark} ({item['weight']})")
    if report["quick_wins"]:
        print("Quick wins:")
        for item in report["quick_wins"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
