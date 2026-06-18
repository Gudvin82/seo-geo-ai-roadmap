#!/usr/bin/env python3
"""Detect FAQ and answer-ready patterns in HTML."""

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
    faq_detection_report,
    fetch_url_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect FAQ and answer-ready blocks.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    args = parser.parse_args()

    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = faq_detection_report(html)
    print(f"Status: {report['status'].upper()}")
    print(f"Confidence: {report['confidence']}")
    print("Visible FAQ headings:")
    for item in report["visible_faq_headings"] or ["none"]:
        print(f"- {item}")
    print("Question-like headings:")
    for item in report["question_like_headings"] or ["none"]:
        print(f"- {item}")
    print(f"FAQ schema present: {report['faq_schema_present']}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
