#!/usr/bin/env python3
"""Generate a markdown-ready or CSV-ready AI share-of-voice tracking scaffold."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_queries(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create AI share-of-voice tracking scaffolds."
    )
    parser.add_argument("brand", help="Brand name")
    parser.add_argument("--queries", required=True, help="Comma-separated query list")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown")
    parser.add_argument("--output", help="Optional output file")
    args = parser.parse_args()

    queries = parse_queries(args.queries)
    if args.format == "markdown":
        rows = [
            "| Query | Surface | Brand mentioned | Citations | Notes |",
            "|---|---|---|---|---|",
        ]
        rows.extend(
            [
                f"| {query} | ChatGPT / Perplexity / Gemini |  |  |  |"
                for query in queries
            ]
        )
        rows.append("")
        rows.append(
            "Manual workflow: run the same prompt set monthly, log citations, and note hallucinations or missing brand facts."
        )
        content = "\n".join(rows)
        if args.output:
            Path(args.output).write_text(content + "\n", encoding="utf-8")
        else:
            print(content)
    else:
        if not args.output:
            parser.error("--output is required for csv format")
        with open(args.output, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["brand", "query", "surface", "brand_mentioned", "citations", "notes"]
            )
            for query in queries:
                writer.writerow(
                    [
                        args.brand,
                        query,
                        "",
                        "",
                        "",
                        "Manual workflow if API is unavailable",
                    ]
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
