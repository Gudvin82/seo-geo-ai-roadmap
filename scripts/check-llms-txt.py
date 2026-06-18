#!/usr/bin/env python3
"""Validate llms.txt from a local file or URL."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import URLError

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.llms_validator import (  # noqa: E402
    load_llms_text_from_url,
    validate_llms_text,
)


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
        content = (
            load_llms_text_from_url(args.url) if args.url else load_from_file(args.file)
        )
    except (URLError, FileNotFoundError) as exc:
        print(f"Unable to load llms.txt: {exc}", file=sys.stderr)
        return 1
    result = validate_llms_text(
        content, checked_source=args.url or args.file or "inline"
    )
    print(f"Checked {result.line_count} non-empty lines")
    for fact in result.observed_facts:
        print(f"- {fact}")
    if result.warnings:
        print("Warnings:")
        for item in result.warnings:
            print(f"- {item}")
        if result.recommendations:
            print("Recommendations:")
            for item in result.recommendations:
                print(f"- {item}")
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
