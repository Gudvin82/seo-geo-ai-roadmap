"""Generate and verify EN/RU parity for canonical documentation surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "generated" / "canonical-docs-parity.json"

CANONICAL_PAIRS = (
    ("Product entry", "README.md", "README_RU.md"),
    ("Documentation index", "DOCS_INDEX.md", "DOCS_INDEX_RU.md"),
    ("Canonical documentation map", "DOCS_CANONICAL.md", "DOCS_CANONICAL_RU.md"),
    ("Methodology", "METHODOLOGY.md", "METHODOLOGY_RU.md"),
    ("Scoring", "SCORING_EXPLAINED.md", "SCORING_EXPLAINED_RU.md"),
    (
        "Scoring calibration",
        "docs/en/scoring-calibration.md",
        "docs/ru/scoring-calibration.md",
    ),
    (
        "Public readiness",
        "PUBLIC_PRODUCT_READINESS.md",
        "PUBLIC_PRODUCT_READINESS_RU.md",
    ),
    (
        "Product boundary",
        "WHAT_THIS_PROJECT_IS_NOT.md",
        "WHAT_THIS_PROJECT_IS_NOT_RU.md",
    ),
    ("Human onboarding", "WALKTHROUGH.md", "WALKTHROUGH_RU.md"),
    ("AI agent onboarding", "START_HERE_FOR_AI.md", "START_HERE_FOR_AI_RU.md"),
    ("Case evidence", "REAL_CASES.md", "REAL_CASES_RU.md"),
    ("Archive policy", "DOCS_ARCHIVE.md", "DOCS_ARCHIVE_RU.md"),
)


def build_payload() -> dict[str, object]:
    rows = []
    for topic, en_path, ru_path in CANONICAL_PAIRS:
        en_exists = (ROOT / en_path).is_file()
        ru_exists = (ROOT / ru_path).is_file()
        rows.append(
            {
                "topic": topic,
                "en_path": en_path,
                "ru_path": ru_path,
                "status": "paired" if en_exists and ru_exists else "missing_pair",
            }
        )
    return {
        "schema_version": "v1",
        "generated_from": "scripts/docs_parity_check.py",
        "summary": {
            "canonical_topics": len(rows),
            "paired": sum(row["status"] == "paired" for row in rows),
            "missing_pair": sum(row["status"] != "paired" for row in rows),
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify canonical EN/RU documentation parity."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path = Path(args.output)
    has_missing = payload["summary"]["missing_pair"] > 0
    if args.check:
        if has_missing:
            print("canonical-docs-parity-failed:missing-pairs", file=sys.stderr)
            return 1
        if not path.is_file() or path.read_text(encoding="utf-8") != output:
            print(f"canonical-docs-parity-out-of-date:{path}", file=sys.stderr)
            return 1
        print("canonical-docs-parity-ok")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 1 if has_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
