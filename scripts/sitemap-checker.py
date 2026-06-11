#!/usr/bin/env python3
"""Fetch a sitemap and report the number of URLs."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def main() -> int:
    parser = argparse.ArgumentParser(description="Check sitemap XML.")
    parser.add_argument("url", help="Sitemap URL")
    args = parser.parse_args()

    try:
        with urllib.request.urlopen(args.url, timeout=15) as response:
            data = response.read()
    except urllib.error.URLError as exc:
        print(f"Failed to fetch sitemap: {exc}", file=sys.stderr)
        return 1

    root = ET.fromstring(data)
    urls = root.findall(".//{*}loc")
    print(f"Found {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
