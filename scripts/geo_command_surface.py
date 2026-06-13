#!/usr/bin/env python3
"""Route GEO/SEO/AI tasks to the right repo assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from app.services.command_router import command_catalog, resolve_command_route
except ModuleNotFoundError:  # pragma: no cover - standalone script fallback
    sys.path.append(str(Path(__file__).resolve().parents[1] / "app" / "backend"))
    from app.services.command_router import command_catalog, resolve_command_route


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
    lines = ["# GEO Command Surface", ""]
    for item in command_catalog():
        lines.extend(
            [
                f"## {item.command}",
                item.summary,
                "",
                f"- Title: {item.title}",
                f"- Scripts: {', '.join(item.recommended_scripts) or 'n/a'}",
                f"- Docs: {', '.join(item.recommended_docs) or 'n/a'}",
                f"- API: {', '.join(item.api_routes) or 'n/a'}",
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
        f"- Scripts: {', '.join(route.recommended_scripts) or 'n/a'}",
        f"- Docs: {', '.join(route.recommended_docs) or 'n/a'}",
        f"- API: {', '.join(route.api_routes) or 'n/a'}",
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
                "recommended_scripts": item.recommended_scripts,
                "recommended_docs": item.recommended_docs,
                "api_routes": item.api_routes,
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
        "recommended_scripts": route.recommended_scripts,
        "recommended_docs": route.recommended_docs,
        "api_routes": route.api_routes,
        "next_step": route.next_step,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_route(args.command), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
