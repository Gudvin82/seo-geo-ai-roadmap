#!/usr/bin/env python3
"""Check robots.txt access for major search and AI bots."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.discoverability_checks import bots_report  # noqa: E402


def print_table(results: list[dict]) -> None:
    print("| Bot | Kind | Status | Detected in | Why it matters | Recommended action |")
    print("|---|---|---|---|---|---|")
    for item in results:
        print(
            "| {bot} | {kind} | {status} | {detected_in} | {why_it_matters} | {recommendation} |".format(
                **item
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check robots.txt access for AI and search bots."
    )
    parser.add_argument(
        "--url", required=True, help="Site URL, for example https://example.com"
    )
    args = parser.parse_args()
    try:
        payload = bots_report(args.url)
    except Exception as exc:
        print(f"Failed to fetch robots.txt: {exc}", file=sys.stderr)
        return 1
    print(f"Robots file: {payload['robots_url']}")
    print_table(payload["results"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
