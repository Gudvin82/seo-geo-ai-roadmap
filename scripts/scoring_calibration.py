"""Assess whether heuristic scores align with measured outcomes.

The script does not invent benchmarks. It only reports calibration after an
operator supplies dated, consented before/after records.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def correlation(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = math.sqrt(
        sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)
    )
    return numerator / denominator if denominator else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrate heuristic score records.")
    parser.add_argument(
        "input", help="CSV with heuristic_score and observed_outcome columns"
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    with Path(args.input).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    scores = [float(row["heuristic_score"]) for row in rows]
    outcomes = [float(row["observed_outcome"]) for row in rows]
    value = correlation(scores, outcomes)
    payload = {
        "record_count": len(rows),
        "correlation": value,
        "minimum_recommended_records": 30,
        "status": "insufficient_evidence"
        if len(rows) < 30
        else "calibration_signal_available",
        "boundary": "Correlation does not prove causation or guarantee outcomes.",
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("# Scoring Calibration")
        print()
        for key, value in payload.items():
            print(f"- {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
