#!/usr/bin/env python3
"""Validate that a JSON file can be parsed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate schema JSON.")
    parser.add_argument("path", help="Path to JSON file")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print("File not found")
        return 1

    json.loads(path.read_text(encoding="utf-8"))
    print("Valid JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
