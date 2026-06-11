#!/usr/bin/env python3
"""Check sitemap freshness and generate a simple stale-content report."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path


@dataclass
class FreshnessRow:
    url: str
    detected_lastmod: str
    status: str
    recommendation: str
    age_days: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check sitemap freshness and output a markdown, CSV, or JSON report."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sitemap-url", help="Remote sitemap URL, for example https://example.com/sitemap.xml")
    group.add_argument("--sitemap-file", help="Local sitemap file path")
    parser.add_argument(
        "--days-stale",
        type=int,
        default=180,
        help="Threshold after which a page is marked stale (default: 180)",
    )
    parser.add_argument(
        "--output-file",
        help="Optional destination path. Prints to stdout when omitted.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "csv", "json"],
        default="markdown",
        help="Report output format (default: markdown)",
    )
    return parser.parse_args()


def load_sitemap(url: str | None, file_path: str | None) -> bytes:
    if url:
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                return response.read()
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network failure while fetching sitemap URL: {exc}") from exc
    if not file_path:
        raise RuntimeError("Missing sitemap source: pass --sitemap-url or --sitemap-file.")
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise RuntimeError(f"Unreadable sitemap file: {path}")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"Unable to read sitemap file: {exc}") from exc


def extract_entries(data: bytes) -> list[tuple[str, str]]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid XML sitemap: {exc}") from exc
    rows: list[tuple[str, str]] = []
    for node in root.findall(".//{*}url"):
        loc = (node.findtext("{*}loc") or "").strip()
        lastmod = (node.findtext("{*}lastmod") or "").strip()
        if loc:
            rows.append((loc, lastmod))
    return rows


def parse_lastmod(raw: str) -> date | None:
    if not raw:
        return None
    cleaned = raw.strip()
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(cleaned).date()
    except ValueError:
        pass
    try:
        return datetime.strptime(cleaned[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def classify_rows(entries: list[tuple[str, str]], days_stale: int) -> list[FreshnessRow]:
    today = datetime.now(timezone.utc).date()
    rows: list[FreshnessRow] = []
    for url, lastmod_raw in entries:
        lastmod = parse_lastmod(lastmod_raw)
        if lastmod is None:
            rows.append(
                FreshnessRow(
                    url=url,
                    detected_lastmod=lastmod_raw or "unknown",
                    status="unknown freshness",
                    recommendation="Review page manually and add a reliable lastmod signal.",
                    age_days=None,
                )
            )
            continue
        age_days = (today - lastmod).days
        if age_days > days_stale:
            status = "stale"
            recommendation = "Review the page, refresh proof, and update numbers or examples if needed."
        else:
            status = "fresh"
            recommendation = "Keep monitoring and refresh only when facts or offers change."
        rows.append(
            FreshnessRow(
                url=url,
                detected_lastmod=lastmod.isoformat(),
                status=status,
                recommendation=recommendation,
                age_days=age_days,
            )
        )
    return rows


def render_markdown(rows: list[FreshnessRow], days_stale: int) -> str:
    lines = [
        "# Content freshness report",
        "",
        f"Stale threshold: {days_stale} days",
        "",
        "| URL | Detected lastmod | Status | Recommendation |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.url} | {row.detected_lastmod} | {row.status} | {row.recommendation} |"
        )
    return "\n".join(lines) + "\n"


def render_json(rows: list[FreshnessRow], days_stale: int) -> str:
    payload = {
        "stale_threshold_days": days_stale,
        "rows": [asdict(row) for row in rows],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def write_csv(rows: list[FreshnessRow], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["url", "detected_lastmod", "status", "recommendation", "age_days"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def main() -> int:
    args = parse_args()
    try:
        data = load_sitemap(args.sitemap_url, args.sitemap_file)
        entries = extract_entries(data)
        if not entries:
            raise RuntimeError("Zero URLs parsed from sitemap.")
        rows = classify_rows(entries, args.days_stale)
    except RuntimeError as exc:
        print(f"Failed to build freshness report: {exc}", file=sys.stderr)
        return 1

    output_path = Path(args.output_file) if args.output_file else None
    if args.format == "csv":
        if output_path is None:
            print("CSV output requires --output-file.", file=sys.stderr)
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_csv(rows, output_path)
        rendered = None
    elif args.format == "json":
        rendered = render_json(rows, args.days_stale)
    else:
        rendered = render_markdown(rows, args.days_stale)

    if rendered is not None:
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    print(f"Processed URLs: {len(rows)}", file=sys.stderr)
    print(f"Fresh pages: {sum(row.status == 'fresh' for row in rows)}", file=sys.stderr)
    print(f"Stale pages: {sum(row.status == 'stale' for row in rows)}", file=sys.stderr)
    print(
        f"Unknown freshness: {sum(row.status == 'unknown freshness' for row in rows)}",
        file=sys.stderr,
    )
    if output_path:
        print(f"Output file: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
