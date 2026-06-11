#!/usr/bin/env python3
"""Create a CSV starter sheet for AI Share of Voice tracking."""

from __future__ import annotations

import argparse
import csv
from datetime import date


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AI Share of Voice CSV template.")
    parser.add_argument("output", help="Output CSV path")
    args = parser.parse_args()

    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "surface", "prompt", "brand_mentioned", "citation_source", "notes"])
        writer.writerow([date.today().isoformat(), "ChatGPT", "", "", "", ""])
    print(f"Created {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
