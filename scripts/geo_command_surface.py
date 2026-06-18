#!/usr/bin/env python3
"""Route GEO/SEO/AI tasks to the right repo assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.command_router import (  # noqa: E402
    command_catalog,
    resolve_command_route,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show the command surface for GEO, SEO, and AI discoverability tasks."
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="catalog",
        help="Command name such as audit, quick, citability, llmstxt, or compare.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format.",
    )
    return parser


def render_markdown_catalog() -> str:
    lines = ["# GEO Command Surface", "", "Canonical prefix: `/geo ...`", ""]
    for item in command_catalog():
        lines.extend(
            [
                f"## {item.command}",
                item.summary,
                "",
                f"- Title: {item.title}",
                f"- Intent: {item.intent}",
                f"- Aliases: {', '.join(item.aliases) or 'n/a'}",
                f"- Scripts: {', '.join(item.recommended_scripts) or 'n/a'}",
                f"- Docs: {', '.join(item.recommended_docs) or 'n/a'}",
                f"- API: {', '.join(item.api_routes) or 'n/a'}",
                f"- Examples: {', '.join(item.example_invocations) or 'n/a'}",
                f"- Outputs: {', '.join(item.output_artifacts) or 'n/a'}",
                f"- Use cases: {', '.join(item.use_cases) or 'n/a'}",
                f"- Next step: {item.next_step}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def render_markdown_route(command: str) -> str:
    route = resolve_command_route(command)
    lines = [
        f"# {route.command}",
        "",
        route.summary,
        "",
        f"- Title: {route.title}",
        f"- Intent: {route.intent}",
        f"- Aliases: {', '.join(route.aliases) or 'n/a'}",
        f"- Scripts: {', '.join(route.recommended_scripts) or 'n/a'}",
        f"- Docs: {', '.join(route.recommended_docs) or 'n/a'}",
        f"- API: {', '.join(route.api_routes) or 'n/a'}",
        f"- Examples: {', '.join(route.example_invocations) or 'n/a'}",
        f"- Outputs: {', '.join(route.output_artifacts) or 'n/a'}",
        f"- Use cases: {', '.join(route.use_cases) or 'n/a'}",
        f"- Next step: {route.next_step}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "catalog":
        payload = [
            {
                "command": item.command,
                "title": item.title,
                "summary": item.summary,
                "intent": item.intent,
                "aliases": item.aliases,
                "recommended_scripts": item.recommended_scripts,
                "recommended_docs": item.recommended_docs,
                "api_routes": item.api_routes,
                "example_invocations": item.example_invocations,
                "output_artifacts": item.output_artifacts,
                "use_cases": item.use_cases,
                "next_step": item.next_step,
            }
            for item in command_catalog()
        ]
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_markdown_catalog(), end="")
        return 0

    try:
        route = resolve_command_route(args.command)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = {
        "command": route.command,
        "title": route.title,
        "summary": route.summary,
        "intent": route.intent,
        "aliases": route.aliases,
        "recommended_scripts": route.recommended_scripts,
        "recommended_docs": route.recommended_docs,
        "api_routes": route.api_routes,
        "example_invocations": route.example_invocations,
        "output_artifacts": route.output_artifacts,
        "use_cases": route.use_cases,
        "next_step": route.next_step,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_route(args.command), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
