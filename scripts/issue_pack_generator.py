#!/usr/bin/env python3
"""Generate a fix issue pack from simple finding inputs."""

from __future__ import annotations

import argparse
import json


def parse_finding(raw: str) -> dict[str, str]:
    parts = [part.strip() for part in raw.split("|")]
    while len(parts) < 4:
        parts.append("")
    return {
        "title": parts[0],
        "priority": parts[1] or "medium",
        "owner": parts[2] or "operator",
        "action": parts[3] or "review and fix",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a lightweight issue pack from findings."
    )
    parser.add_argument("--project", required=True, help="Project or site name.")
    parser.add_argument(
        "--finding",
        action="append",
        default=[],
        help="Finding in 'title|priority|owner|action' format.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def build_payload(project: str, findings: list[str]) -> dict[str, object]:
    rows = [parse_finding(item) for item in findings]
    return {
        "project": project,
        "issue_count": len(rows),
        "issues": rows,
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        f"# Issue Pack: {payload['project']}",
        "",
        f"- issue_count: `{payload['issue_count']}`",
        "",
        "| Title | Priority | Owner | Action |",
        "|---|---|---|---|",
    ]
    for row in payload["issues"]:
        lines.append(
            f"| {row['title']} | {row['priority']} | {row['owner']} | {row['action']} |"
        )
    lines.extend(
        [
            "",
            "## Delivery note",
            "",
            "Convert high-priority rows into GitHub, GitLab, Notion, Trello, or Linear tasks after human review.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    payload = build_payload(args.project, args.finding)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
