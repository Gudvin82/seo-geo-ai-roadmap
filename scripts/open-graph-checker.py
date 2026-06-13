#!/usr/bin/env python3
"""Check Open Graph and Twitter Card completeness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import (  # noqa: E402
    fetch_url_text,
    open_graph_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Open Graph and Twitter Card completeness."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    args = parser.parse_args()

    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = open_graph_report(html)
    print(f"Status: {report['status'].upper()}")
    print("Fields:")
    for key, value in report["fields"].items():
        print(f"- {key}: {value or 'missing'}")
    if report["missing_fields"]:
        print("Missing fields:")
        for item in report["missing_fields"]:
            print(f"- {item}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
