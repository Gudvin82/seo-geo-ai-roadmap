#!/usr/bin/env python3
"""Check how robots.txt treats major AI and search bots."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from urllib.robotparser import RobotFileParser


BOTS = [
    "GPTBot",
    "ChatGPT-User",
    "PerplexityBot",
    "ClaudeBot",
    "Google-Extended",
    "YandexBot",
]


@dataclass
class BotResult:
    bot: str
    status: str
    recommendation: str


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def fetch_robots(url: str) -> tuple[str, str]:
    site_url = normalize_url(url)
    parsed = urllib.parse.urlparse(site_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    with urllib.request.urlopen(robots_url, timeout=15) as response:
        content = response.read().decode("utf-8", errors="replace")
    return robots_url, content


def check_bots(robots_url: str) -> list[BotResult]:
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.read()

    results: list[BotResult] = []
    for bot in BOTS:
        allowed = parser.can_fetch(bot, "/")
        if allowed:
            status = "allowed"
            recommendation = "No action needed unless policy requires tighter control."
        else:
            status = "blocked"
            recommendation = "Review robots.txt if you want this bot to access public content."
        results.append(BotResult(bot=bot, status=status, recommendation=recommendation))
    return results


def print_table(results: list[BotResult]) -> None:
    print("| Bot | Status | Recommendation |")
    print("|---|---|---|")
    for result in results:
        print(f"| {result.bot} | {result.status} | {result.recommendation} |")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check robots.txt access for AI bots.")
    parser.add_argument("url", help="Website URL, for example example.com or https://example.com")
    args = parser.parse_args()

    try:
        robots_url, _content = fetch_robots(args.url)
        results = check_bots(robots_url)
    except urllib.error.URLError as exc:
        print(f"Failed to fetch robots.txt: {exc}", file=sys.stderr)
        return 1

    print(f"Robots file: {robots_url}")
    print_table(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
