#!/usr/bin/env python3
"""Validate ai.txt from a local file or URL."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import (  # noqa: E402
    ai_txt_report,
    resolve_public_file_url,
    try_fetch_url_text,
)


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _print_report(report: dict) -> None:
    print(f"Status: {report['status'].upper()}")
    print("Directives:")
    for key, values in sorted(report["directives"].items()):
        print(f"- {key}: {', '.join(values)}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    if report["contradictions"]:
        print("Contradictions:")
        for item in report["contradictions"]:
            print(f"- {item}")
    print("Recommendations:")
    for item in report["recommendations"]:
        print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ai.txt structure and basic cross-file consistency."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Site URL or direct ai.txt URL")
    group.add_argument("--file", help="Local ai.txt path")
    parser.add_argument(
        "--robots-file", help="Optional local robots.txt for consistency checks"
    )
    parser.add_argument(
        "--llms-file", help="Optional local llms.txt for consistency checks"
    )
    args = parser.parse_args()

    try:
        if args.url:
            ai_url = resolve_public_file_url(args.url, "ai.txt")
            ai_content, ai_error = try_fetch_url_text(ai_url)
            if ai_error or ai_content is None:
                print(f"FAIL: Unable to load ai.txt: {ai_error}")
                return 1
            robots_content, _ = try_fetch_url_text(
                resolve_public_file_url(args.url, "robots.txt")
            )
            llms_content, _ = try_fetch_url_text(
                resolve_public_file_url(args.url, "llms.txt")
            )
        else:
            ai_content = _read_file(args.file)
            robots_content = _read_file(args.robots_file) if args.robots_file else None
            llms_content = _read_file(args.llms_file) if args.llms_file else None
    except FileNotFoundError as exc:
        print(f"FAIL: {exc}")
        return 1

    report = ai_txt_report(
        ai_content, robots_content=robots_content, llms_content=llms_content
    )
    _print_report(report)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
