#!/usr/bin/env python3
"""Generate llms.txt from a sitemap URL or local sitemap file."""

from __future__ import annotations

import argparse
import os
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
        description=(
            "Generate llms.txt from a sitemap URL or local sitemap file and "
            "write a production-ready draft to the target path."
        )
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--sitemap-url",
        help="Remote sitemap URL, for example https://example.com/sitemap.xml",
    )
    source.add_argument(
        "--sitemap-file",
        help="Local sitemap file path, for example ./sitemap.xml",
    )
    parser.add_argument(
        "--output-file",
        default="llms.txt",
        help="Destination llms.txt path (default: ./llms.txt)",
    )
    return parser.parse_args()


def load_sitemap(url: str | None, file_path: str | None) -> bytes:
    if url:
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                return response.read()
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Network failure while fetching sitemap URL: {exc}"
            ) from exc
    if not file_path:
        raise RuntimeError(
            "Missing sitemap source: pass --sitemap-url or --sitemap-file."
        )
    path = Path(file_path)
    if not path.exists():
        raise RuntimeError(f"Unreadable sitemap file: {path} does not exist.")
    if not path.is_file():
        raise RuntimeError(f"Unreadable sitemap file: {path} is not a file.")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"Unreadable sitemap file: {exc}") from exc


def extract_entries(data: bytes) -> list[dict[str, str]]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid XML sitemap: {exc}") from exc
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


def build_output(entries: list[dict[str, str]]) -> tuple[str, list[str], int]:
    lines = ["# Generated from sitemap"]
    warnings: list[str] = []
    skipped = 0
    for entry in entries:
        path, description = infer_description(entry["loc"])
        suffix = f" [lastmod: {entry['lastmod']}]" if entry["lastmod"] else ""
        if "review description" in description.lower():
            warnings.append(f"Review description for {entry['loc']}")
        if path.startswith("/tag/") or path.startswith("/author/"):
            skipped += 1
            continue
        lines.append(f"{entry['loc']} - {description}{suffix}")
    return "\n".join(lines) + "\n", warnings, skipped


def main() -> int:
    args = parse_args()
    try:
        data = load_sitemap(args.sitemap_url, args.sitemap_file)
        entries = extract_entries(data)
        if not entries:
            raise RuntimeError(
                "Zero URLs parsed from sitemap. Aborting llms.txt generation."
            )
    except RuntimeError as exc:
        print(f"Failed to generate llms.txt: {exc}", file=sys.stderr)
        return 1

    output, warnings, skipped = build_output(entries)
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    source_label = args.sitemap_url or os.fspath(
        Path(args.sitemap_file or "").resolve()
    )
    included = len(entries) - skipped
    print(f"Source: {source_label}")
    print(f"Processed URLs: {len(entries)}")
    print(f"Included URLs: {included}")
    print(f"Skipped URLs: {skipped}")
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
