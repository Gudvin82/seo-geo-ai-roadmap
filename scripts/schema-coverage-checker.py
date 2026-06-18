#!/usr/bin/env python3
"""Audit schema coverage in page HTML."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.discoverability_checks import (  # noqa: E402
    fetch_url_text,
    schema_coverage_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check schema coverage in HTML.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    parser.add_argument(
        "--site-type",
        choices=["saas", "local-business", "service", "ecommerce", "content"],
        help="Optional site-type hint for stronger recommendations.",
    )
    args = parser.parse_args()

    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = schema_coverage_report(html, site_type=args.site_type)
    print(f"Status: {report['status'].upper()}")
    print(f"Site type: {report['site_type']}")
    print("Found schema types:")
    for item in report["found_types"] or ["none"]:
        print(f"- {item}")
    print("Missing schema types:")
    for item in report["missing_types"] or ["none"]:
        print(f"- {item}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    if report["recommendations"]:
        print("Recommendations:")
        for item in report["recommendations"]:
            print(f"- {item['schema_type']}: {item['message']} ({item['template']})")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
