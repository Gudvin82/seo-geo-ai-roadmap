#!/usr/bin/env python3
"""Detect basic fact drift across multiple discoverability surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect strong fact drift across website, schema, llms.txt, and AI output surfaces."
    )
    parser.add_argument(
        "--surface",
        action="append",
        default=[],
        help="Surface definition in the form name=path-to-text-file. Repeat for multiple surfaces.",
    )
    return parser.parse_args()


def detect_fact_drift(surfaces: list[dict[str, str]]) -> dict:
    keyword_groups = {
        "phone": ["phone", "telephone", "tel", "+7", "+1"],
        "pricing": ["price", "pricing", "cost", "from ", "usd", "rub", "eur"],
        "address": ["address", "office", "street", "city", "moscow", "new york"],
        "founder": ["founder", "ceo", "author", "expert", "dr.", "doctor", "lawyer"],
    }
    items = []
    for drift_type, keywords in keyword_groups.items():
        present = [
            surface["name"]
            for surface in surfaces
            if any(keyword in surface["content"].lower() for keyword in keywords)
        ]
        absent = [
            surface["name"] for surface in surfaces if surface["name"] not in present
        ]
        if present and absent:
            items.append(
                {
                    "drift_type": drift_type,
                    "severity": "medium" if len(present) >= len(absent) else "high",
                    "observed": (
                        f"{drift_type} signals appear on {', '.join(present)} "
                        f"but not on {', '.join(absent)}."
                    ),
                    "recommended_next_step": (
                        f"Align canonical {drift_type} facts across site copy, schema, "
                        "llms.txt, and AI-facing outputs."
                    ),
                }
            )
    return {
        "status": "drift_detected" if items else "no_strong_drift_detected",
        "surface_count": len(surfaces),
        "detected_types": sorted({item["drift_type"] for item in items}),
        "drift_items": items,
    }


def main() -> int:
    args = parse_args()
    surfaces = []
    for definition in args.surface:
        if "=" not in definition:
            raise SystemExit(f"Invalid --surface value: {definition}")
        name, path = definition.split("=", 1)
        surfaces.append(
            {
                "name": name.strip(),
                "content": Path(path.strip()).read_text(encoding="utf-8"),
            }
        )
    print(json.dumps(detect_fact_drift(surfaces), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
