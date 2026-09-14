"""Generate the public product capability matrix from the runtime registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.services.capabilities import product_capability_matrix  # noqa: E402


def markdown(payload: dict) -> str:
    lines = [
        "# Product Capability Matrix",
        "",
        "Generated from the canonical runtime registry. A maturity label is an evidence-bound operational status, not a marketing claim.",
        "",
        "## Levels",
        "",
    ]
    for level in payload["levels"]:
        lines.append(f"- `{level}`: {payload['level_boundaries'][level]}")
    lines.extend(
        [
            "",
            "## Surfaces",
            "",
            "| Surface | Capability | Status | Evidence | Boundary |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            f"| {row['surface']} | {row['label']} | `{row['level']}` | {row['evidence']} | {row['boundary']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate evidence-bound product capability metadata."
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail unless the selected output file exactly matches generated content.",
    )
    args = parser.parse_args()
    if args.check and not args.output:
        parser.error("--check requires --output")
    payload = product_capability_matrix()
    output = (
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(payload)
    )
    if args.output:
        path = Path(args.output)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != output:
                print(f"capability-matrix-out-of-date:{path}", file=sys.stderr)
                return 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
