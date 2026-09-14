"""Assess whether readiness scores align with observed outcomes.

The utility never turns a readiness score into a prediction of rankings,
citations, or revenue. It reports the quality of an operator-supplied,
dated evidence dataset and only exposes a calibration signal when the sample
is sufficiently independent and comparable.
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


RECOMMENDED_COLUMNS = {
    "case_id",
    "heuristic_score",
    "observed_outcome",
    "outcome_definition",
    "observed_at",
    "observation_window_days",
    "evidence_reference",
}


def parse_number(row: dict[str, str], column: str, row_number: int) -> float:
    try:
        return float(row[column])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(
            f"Row {row_number} has no valid numeric {column!r} value."
        ) from exc


def dataset_quality(rows: list[dict[str, str]], headers: set[str]) -> dict[str, object]:
    missing = sorted(RECOMMENDED_COLUMNS - headers)
    case_ids = [row.get("case_id", "").strip() for row in rows]
    distinct_case_ids = {case_id for case_id in case_ids if case_id}
    outcomes = {
        row.get("outcome_definition", "").strip()
        for row in rows
        if row.get("outcome_definition", "").strip()
    }
    return {
        "required_columns_present": not missing,
        "missing_recommended_columns": missing,
        "distinct_case_count": len(distinct_case_ids),
        "outcome_definitions": sorted(outcomes),
        "comparable_outcome_definition": len(outcomes) == 1,
        "dated_observations": all(row.get("observed_at", "").strip() for row in rows),
        "evidence_references": all(
            row.get("evidence_reference", "").strip() for row in rows
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrate heuristic score records.")
    parser.add_argument(
        "input", help="CSV with heuristic_score and observed_outcome columns"
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    with Path(args.input).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = set(reader.fieldnames or [])
    if not rows:
        raise ValueError("Calibration input has no records.")
    scores = [
        parse_number(row, "heuristic_score", index) for index, row in enumerate(rows, 2)
    ]
    outcomes = [
        parse_number(row, "observed_outcome", index)
        for index, row in enumerate(rows, 2)
    ]
    value = correlation(scores, outcomes)
    quality = dataset_quality(rows, headers)
    is_independent_enough = quality["distinct_case_count"] >= 30
    is_comparable = bool(
        quality["required_columns_present"]
        and quality["comparable_outcome_definition"]
        and quality["dated_observations"]
        and quality["evidence_references"]
    )
    status = (
        "calibration_signal_available"
        if len(rows) >= 30
        and is_independent_enough
        and is_comparable
        and value is not None
        else "insufficient_evidence"
    )
    payload = {
        "metric_type": "explainable_readiness_score",
        "record_count": len(rows),
        "correlation": value,
        "minimum_recommended_records": 30,
        "status": status,
        "dataset_quality": quality,
        "boundary": (
            "Correlation does not prove causation, predict rankings or AI citations, "
            "or guarantee business outcomes."
        ),
        "next_step": (
            "Collect independent, dated records with one outcome definition and an evidence reference."
            if status == "insufficient_evidence"
            else "Review segment-level effects and publish null or negative results beside positive results."
        ),
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
