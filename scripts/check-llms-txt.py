#!/usr/bin/env python3
"""Validate llms.txt from a local file or URL."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

REQUIRED_HINTS = ["/", "faq", "about"]


def load_from_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def load_from_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate llms.txt structure from --url or --file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL to llms.txt")
    group.add_argument("--file", help="Local llms.txt path")
    args = parser.parse_args()
    try:
        content = load_from_url(args.url) if args.url else load_from_file(args.file)
    except (urllib.error.URLError, FileNotFoundError) as exc:
        print(f"Unable to load llms.txt: {exc}", file=sys.stderr)
        return 1
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    missing = [
        hint
        for hint in REQUIRED_HINTS
        if not any(hint in line.lower() for line in lines)
    ]
    has_header = any(line.startswith("#") for line in lines)
    bullet_like = [
        line for line in lines if line.startswith(("-", "*", ">")) or " - " in line
    ]
    print(f"Checked {len(lines)} non-empty lines")
    if missing or not has_header or not bullet_like:
        print("Missing sections:")
        for item in missing:
            print(f"- {item}")
        if not has_header:
            print("- top-level heading")
        if not bullet_like:
            print("- structured entries or bullet-like URL lines")
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
