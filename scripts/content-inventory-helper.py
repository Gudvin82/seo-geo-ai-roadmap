#!/usr/bin/env python3
"""Generate a markdown content inventory scaffold from URLs."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a content inventory table from URLs.")
    parser.add_argument("urls", nargs="+", help="List of URLs")
    args = parser.parse_args()
    print("| URL | Intent | Funnel | Owner | Refresh rule | Notes |")
    print("|---|---|---|---|---|---|")
    for url in args.urls:
        print(f"| {url} |  |  |  |  |  |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
