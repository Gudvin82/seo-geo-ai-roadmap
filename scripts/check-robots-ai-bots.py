#!/usr/bin/env python3
"""Check robots.txt access for major search and AI bots."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request

BOTS = [
    "GPTBot",
    "ChatGPT-User",
    "PerplexityBot",
    "ClaudeBot",
    "Google-Extended",
    "Googlebot",
    "Bingbot",
    "YandexBot",
]


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def fetch_robots(site_url: str) -> tuple[str, str]:
    site_url = normalize_url(site_url)
    parsed = urllib.parse.urlparse(site_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    with urllib.request.urlopen(robots_url, timeout=15) as response:
        content = response.read().decode("utf-8", errors="replace")
    return robots_url, content


def parse_groups(content: str) -> list[dict[str, list[str]]]:
    groups: list[dict[str, list[str]]] = []
    current: dict[str, list[str]] | None = None
    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        key_lower = key.lower()
        if key_lower == "user-agent":
            current = {"agents": [value], "allow": [], "disallow": []}
            groups.append(current)
            continue
        if current is None:
            continue
        if key_lower == "allow":
            current["allow"].append(value)
        elif key_lower == "disallow":
            current["disallow"].append(value)
    merged: dict[str, dict[str, list[str]]] = {}
    for group in groups:
        agent = group["agents"][0]
        bucket = merged.setdefault(agent, {"allow": [], "disallow": []})
        bucket["allow"].extend(group["allow"])
        bucket["disallow"].extend(group["disallow"])
    return [{"agent": agent, **rules} for agent, rules in merged.items()]


def evaluate_bot(groups: list[dict[str, list[str]]], bot: str) -> tuple[str, str]:
    exact = next(
        (group for group in groups if group["agent"].lower() == bot.lower()), None
    )
    wildcard = next((group for group in groups if group["agent"] == "*"), None)
    target = exact or wildcard
    if target is None:
        return (
            "unspecified",
            "No matching group found. Add an explicit rule if this bot matters to your strategy.",
        )
    allows = target.get("allow", [])
    disallows = target.get("disallow", [])
    if "/" in disallows and "/" not in allows:
        return (
            "blocked",
            "Public content is blocked for this bot. Review whether that matches policy.",
        )
    if "/" in allows:
        return "allowed", "Top-level access is explicitly allowed."
    if not allows and not disallows:
        return (
            "unspecified",
            "The group exists but has no path rules. Make intent explicit.",
        )
    return (
        "unspecified",
        "There are partial rules. Manually review whether key public pages are reachable.",
    )


def print_table(results: list[tuple[str, str, str]]) -> None:
    print("| Bot | Status | Recommendation |")
    print("|---|---|---|")
    for bot, status, recommendation in results:
        print(f"| {bot} | {status} | {recommendation} |")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check robots.txt access for AI and search bots."
    )
    parser.add_argument(
        "--url", required=True, help="Site URL, for example https://example.com"
    )
    args = parser.parse_args()
    try:
        robots_url, content = fetch_robots(args.url)
    except urllib.error.URLError as exc:
        print(f"Failed to fetch robots.txt: {exc}", file=sys.stderr)
        return 1
    groups = parse_groups(content)
    results = [(bot, *evaluate_bot(groups, bot)) for bot in BOTS]
    print(f"Robots file: {robots_url}")
    print_table(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
