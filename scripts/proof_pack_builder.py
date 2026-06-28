#!/usr/bin/env python3
"""Build a publishable proof or case-study pack."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a structured proof pack from before/after facts."
    )
    parser.add_argument("--site", required=True, help="Domain or project name.")
    parser.add_argument(
        "--change",
        action="append",
        default=[],
        help="Concrete change that was implemented.",
    )
    parser.add_argument("--before-score", type=float, help="Optional score before.")
    parser.add_argument("--after-score", type=float, help="Optional score after.")
    parser.add_argument(
        "--evidence-link",
        action="append",
        default=[],
        help="Public or internal evidence link.",
    )
    parser.add_argument(
        "--fact",
        action="append",
        default=[],
        help="Observed fact that is safe to state.",
    )
    parser.add_argument(
        "--inference",
        action="append",
        default=[],
        help="Interpretation or bounded inference.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Recommended next step after the change.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    delta = None
    if args.before_score is not None and args.after_score is not None:
        delta = round(args.after_score - args.before_score, 2)
    return {
        "site": args.site,
        "changes": args.change,
        "score_before": args.before_score,
        "score_after": args.after_score,
        "score_delta": delta,
        "facts": args.fact,
        "inferences": args.inference,
        "evidence_links": args.evidence_link,
        "next_steps": args.next_step,
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        f"# Proof Pack: {payload['site']}",
        "",
        "## Change summary",
        "",
    ]
    for item in payload["changes"] or ["No change summary provided yet."]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Measured movement",
            "",
            f"- before_score: `{payload['score_before']}`",
            f"- after_score: `{payload['score_after']}`",
            f"- score_delta: `{payload['score_delta']}`",
            "",
            "## Safe facts",
            "",
        ]
    )
    for item in payload["facts"] or ["No explicit facts supplied."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Bounded inferences", ""])
    for item in payload["inferences"] or ["No bounded inferences supplied."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Evidence links", ""])
    for item in payload["evidence_links"] or ["No evidence links supplied."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommended next steps", ""])
    for item in payload["next_steps"] or ["No next steps supplied."]:
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
