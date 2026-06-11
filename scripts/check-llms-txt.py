#!/usr/bin/env python3
"""Validate a simple llms.txt file."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate llms.txt formatting.")
    parser.add_argument("path", help="Path to llms.txt")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print("File not found")
        return 1

    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        print("llms.txt is empty")
        return 1

    bad_lines = [line for line in lines if not line.startswith(("/", "#", "-"))]
    if bad_lines:
        print("Potentially invalid lines:")
        for line in bad_lines:
            print(f"- {line}")
        return 1

    print(f"OK: {len(lines)} non-empty lines checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
