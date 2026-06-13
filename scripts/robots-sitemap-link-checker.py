#!/usr/bin/env python3
"""Check robots.txt and sitemap linkage together."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import robots_sitemap_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check robots.txt and sitemap linkage together."
    )
    parser.add_argument("--url", required=True, help="Site URL")
    parser.add_argument(
        "--sitemap-url",
        help="Optional explicit sitemap URL to test even if not declared in robots.txt",
    )
    args = parser.parse_args()

    report = robots_sitemap_report(args.url, sitemap_url=args.sitemap_url)
    print(f"Status: {report['status'].upper()}")
    print(f"Robots file: {report['robots_url']}")
    print("Declared sitemaps:")
    for item in report["declared_sitemaps"] or ["none"]:
        print(f"- {item}")
    print("Sitemap checks:")
    for item in report["sitemap_results"] or []:
        print(
            f"- {item['url']} :: {item['status']} :: {item['message']} :: loc_count={item['loc_count']}"
        )
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
