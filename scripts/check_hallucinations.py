#!/usr/bin/env python3
"""Create a starter hallucination-checking report from brand facts and questions."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a hallucination-checking scaffold from brand facts and question prompts."
    )
    parser.add_argument(
        "--brand-facts-file",
        required=True,
        help="Markdown or JSON file with canonical brand facts.",
    )
    parser.add_argument(
        "--questions-file",
        required=True,
        help="Markdown, TXT, or JSON file with question prompts.",
    )
    parser.add_argument("--output-file", required=True, help="Report output path.")
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "csv"],
        default="markdown",
        help="Report output format (default: markdown)",
    )
    parser.add_argument(
        "--provider", help="Optional provider label for future live integrations."
    )
    parser.add_argument(
        "--model", help="Optional model label for future live integrations."
    )
    return parser.parse_args()


def load_text_or_json(path: Path) -> str | dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(raw)
    return raw


def parse_brand_facts(value: str | dict) -> dict[str, list[str]]:
    if isinstance(value, dict):
        parsed: dict[str, list[str]] = {}
        for key, item in value.items():
            if isinstance(item, list):
                parsed[str(key)] = [str(entry) for entry in item]
            else:
                parsed[str(key)] = [str(item)]
        return parsed

    parsed = {"core facts": []}
    current = "core facts"
    for raw_line in value.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            current = line.lstrip("#").strip().lower()
            parsed.setdefault(current, [])
            continue
        if ":" in line and not line.startswith("-"):
            key, val = [part.strip() for part in line.split(":", 1)]
            parsed.setdefault(key.lower(), []).append(val)
            continue
        cleaned = re.sub(r"^[-*]\s*", "", line)
        parsed.setdefault(current, []).append(cleaned)
    return parsed


def parse_questions(value: str | dict) -> list[str]:
    if isinstance(value, dict):
        if isinstance(value.get("questions"), list):
            return [
                str(item).strip() for item in value["questions"] if str(item).strip()
            ]
        return [str(val).strip() for val in value.values() if str(val).strip()]
    questions: list[str] = []
    for raw_line in value.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        cleaned = re.sub(r"^[-*\d\.\)]\s*", "", line).strip()
        if cleaned:
            questions.append(cleaned)
    return questions


def infer_expected_facts(question: str, brand_facts: dict[str, list[str]]) -> str:
    normalized = question.lower()
    matches: list[str] = []
    for key, values in brand_facts.items():
        if key in normalized:
            matches.extend(values)
    if not matches:
        for key in (
            "official brand name",
            "preferred short name",
            "website",
            "core products",
            "core services",
        ):
            matches.extend(brand_facts.get(key, []))
    if not matches:
        flat = [item for values in brand_facts.values() for item in values]
        matches = flat[:3]
    return (
        "; ".join(matches[:5])
        if matches
        else "Review manually against canonical facts."
    )


def build_rows(
    brand_facts: dict[str, list[str]],
    questions: list[str],
    provider: str | None,
    model: str | None,
) -> list[dict[str, str]]:
    answer_placeholder = (
        "Manual answer capture or optional provider integration goes here."
    )
    next_action = "Compare the answer against the expected facts and log any drift."
    if provider or model:
        next_action = "Capture the live answer from the configured provider/model, then compare it against canonical facts."
    rows: list[dict[str, str]] = []
    for question in questions:
        rows.append(
            {
                "question": question,
                "expected_facts": infer_expected_facts(question, brand_facts),
                "answer_placeholder": answer_placeholder,
                "discrepancy_status": "pending review",
                "next_action": next_action,
            }
        )
    return rows


def render_markdown(
    rows: list[dict[str, str]], provider: str | None, model: str | None
) -> str:
    lines = ["# Hallucination checking report", ""]
    if provider or model:
        lines.append(f"Provider context: {provider or 'manual'} / {model or 'default'}")
        lines.append("")
    lines.extend(
        [
            "| Question | Expected facts | Answer placeholder | Discrepancy status | Next action |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| {question} | {expected_facts} | {answer_placeholder} | {discrepancy_status} | {next_action} |".format(
                **row
            )
        )
    return "\n".join(lines) + "\n"


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "question",
                "expected_facts",
                "answer_placeholder",
                "discrepancy_status",
                "next_action",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    brand_path = Path(args.brand_facts_file)
    questions_path = Path(args.questions_file)
    if not brand_path.exists() or not questions_path.exists():
        print("Input file is missing.", file=sys.stderr)
        return 1
    try:
        brand_facts = parse_brand_facts(load_text_or_json(brand_path))
        questions = parse_questions(load_text_or_json(questions_path))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to load input files: {exc}", file=sys.stderr)
        return 1
    if not questions:
        print("No questions parsed from the questions file.", file=sys.stderr)
        return 1

    rows = build_rows(brand_facts, questions, args.provider, args.model)
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "csv":
        write_csv(rows, output_path)
    elif args.format == "json":
        output_path.write_text(
            json.dumps({"rows": rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        output_path.write_text(
            render_markdown(rows, args.provider, args.model), encoding="utf-8"
        )
    print(f"Questions processed: {len(rows)}")
    print(f"Output file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
