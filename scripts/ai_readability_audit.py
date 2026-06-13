#!/usr/bin/env python3
"""Audit AI readability layers for a public page or local HTML file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import (  # noqa: E402
    ai_readability_report,
    fetch_url_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AI readability layers.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    args = parser.parse_args()

    page_url = args.url if args.url else None
    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = ai_readability_report(html, page_url=page_url)
    print(f"Status: {report['status'].upper()}")
    print(f"Score: {report['score']}/100")
    print("Detected layers:")
    for item in report["detected_layers"] or ["none"]:
        print(f"- {item}")
    print("Missing layers:")
    for item in report["missing_layers"] or ["none"]:
        print(f"- {item}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    if report["quick_wins"]:
        print("Quick wins:")
        for item in report["quick_wins"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
