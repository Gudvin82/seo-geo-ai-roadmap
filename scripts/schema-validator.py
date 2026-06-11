#!/usr/bin/env python3
"""Validate schema JSON or JSON-LD payloads."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate schema JSON.")
    parser.add_argument("--file", required=True, help="Path to schema JSON file")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print("File not found")
        return 1
    json.loads(path.read_text(encoding="utf-8"))
    print("Valid JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
