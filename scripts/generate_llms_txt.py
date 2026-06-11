#!/usr/bin/env python3
"""Generate llms.txt from a sitemap URL or local sitemap file."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


TYPE_HINTS = [
    ("/faq", "FAQ and direct answers"),
    ("/about", "Company profile and expert proof"),
    ("/contact", "Contact page and conversion details"),
    ("/blog", "Articles, guides, and educational content"),
    ("/docs", "Documentation and reference content"),
    ("/case", "Case studies and proof assets"),
    ("/service", "Service page"),
    ("/product", "Product page"),
    ("/pricing", "Pricing and commercial terms"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate llms.txt from a sitemap URL or local sitemap file."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--sitemap-url", help="Remote sitemap URL")
    source.add_argument("--sitemap-file", help="Local sitemap file path")
    parser.add_argument(
        "--output-file",
        default="llms.txt",
        help="Output llms.txt path (default: ./llms.txt)",
    )
    return parser.parse_args()


def load_sitemap(url: str | None, file_path: str | None) -> bytes:
    if url:
        with urllib.request.urlopen(url, timeout=20) as response:
            return response.read()
    assert file_path is not None
    return Path(file_path).read_bytes()


def extract_entries(data: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(data)
    entries: list[dict[str, str]] = []
    for url_node in root.findall(".//{*}url"):
        loc = url_node.findtext("{*}loc", default="").strip()
        lastmod = url_node.findtext("{*}lastmod", default="").strip()
        if loc:
            entries.append({"loc": loc, "lastmod": lastmod})
    return entries


def infer_description(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path or "/"
    normalized = path.lower()
    if path in {"", "/"}:
        return path or "/", "Homepage, positioning, and navigation"
    for needle, description in TYPE_HINTS:
        if needle in normalized:
            return path, description
    slug = normalized.strip("/").split("/")[-1].replace("-", " ").strip()
    label = slug.title() if slug else "Page"
    return path, f"{label} page (review description for final production use)"


def build_output(entries: list[dict[str, str]]) -> tuple[str, list[str]]:
    lines = ["# Generated from sitemap"]
    warnings: list[str] = []
    for entry in entries:
        path, description = infer_description(entry["loc"])
        suffix = f" [lastmod: {entry['lastmod']}]" if entry["lastmod"] else ""
        if "review description" in description.lower():
            warnings.append(f"Review description for {entry['loc']}")
        lines.append(f"{path} - {description}{suffix}")
    return "\n".join(lines) + "\n", warnings


def main() -> int:
    args = parse_args()
    try:
        data = load_sitemap(args.sitemap_url, args.sitemap_file)
        entries = extract_entries(data)
    except (urllib.error.URLError, FileNotFoundError, ET.ParseError) as exc:
        print(f"Failed to generate llms.txt: {exc}", file=sys.stderr)
        return 1

    output, warnings = build_output(entries)
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    print(f"Processed URLs: {len(entries)}")
    print(f"Output file: {output_path}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Warnings: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
