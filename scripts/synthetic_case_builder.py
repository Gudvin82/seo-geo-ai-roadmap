#!/usr/bin/env python3
"""Generate a synthetic but bounded training case."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a synthetic case-study training artifact."
    )
    parser.add_argument("--name", required=True, help="Synthetic project name.")
    parser.add_argument("--market", default="global", help="Market context.")
    parser.add_argument("--site-type", default="service", help="Site type.")
    parser.add_argument("--before-score", type=float, required=True)
    parser.add_argument("--after-score", type=float, required=True)
    parser.add_argument("--finding-delta", default="12->7")
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--lesson", action="append", default=[])
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    return {
        "case_kind": "synthetic_example",
        "name": args.name,
        "market": args.market,
        "site_type": args.site_type,
        "before_score": args.before_score,
        "after_score": args.after_score,
        "score_delta": round(args.after_score - args.before_score, 2),
        "finding_delta": args.finding_delta,
        "changes": args.change,
        "lessons": args.lesson,
        "disclaimer": (
            "Synthetic example for operator training. Do not present as a public client result."
        ),
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        f"# Synthetic Case: {payload['name']}",
        "",
        "> Synthetic example for operator training. Do not publish as a real client result.",
        "",
        f"- market: `{payload['market']}`",
        f"- site_type: `{payload['site_type']}`",
        f"- before_score: `{payload['before_score']}`",
        f"- after_score: `{payload['after_score']}`",
        f"- score_delta: `{payload['score_delta']}`",
        f"- finding_delta: `{payload['finding_delta']}`",
        "",
        "## Simulated changes",
        "",
    ]
    for item in payload["changes"] or ["No simulated changes supplied."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Lessons", ""])
    for item in payload["lessons"] or ["No lessons supplied."]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
