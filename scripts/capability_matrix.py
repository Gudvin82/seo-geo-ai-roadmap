"""Generate the public integration capability matrix from the runtime registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.services.integrations import integration_capability_matrix  # noqa: E402


def markdown(payload: dict) -> str:
    lines = [
        "# Integration Capability Matrix",
        "",
        "Generated from the runtime registry. `starter_or_operator_guided` is not a live API claim.",
        "",
        "| Surface | Delivery state | Credentials | Boundary |",
        "| --- | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        credentials = ", ".join(row["required_env_vars"]) or "none"
        lines.append(
            f"| {row['label']} | {row['delivery_state']} | {credentials} | {row['limitations']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate integration capability metadata."
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = integration_capability_matrix()
    output = (
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json"
        else markdown(payload)
    )
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
