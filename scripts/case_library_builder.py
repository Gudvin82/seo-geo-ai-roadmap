#!/usr/bin/env python3
"""Build a simple case-library index from markdown files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return path.stem


def infer_case_type(path: Path) -> str:
    name = path.name.lower()
    if "synthetic" in name:
        return "synthetic"
    if "real" in name or "case" in name or "audit" in name:
        return "bounded_public"
    return "reference"


def build_payload(paths: list[str]) -> dict[str, object]:
    rows = []
    for item in paths:
        path = Path(item)
        rows.append(
            {
                "path": item,
                "title": read_title(path),
                "case_type": infer_case_type(path),
            }
        )
    return {
        "case_count": len(rows),
        "cases": rows,
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Case Library Index",
        "",
        f"- case_count: `{payload['case_count']}`",
        "",
        "| Title | Type | Path |",
        "|---|---|---|",
    ]
    for row in payload["cases"]:
        lines.append(f"| {row['title']} | {row['case_type']} | `{row['path']}` |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a simple case-library index.")
    parser.add_argument("paths", nargs="+", help="Markdown case files to index.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(args.paths)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
