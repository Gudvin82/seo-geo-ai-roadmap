"""Check version consistency across key release surfaces."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = REPO_ROOT / "app" / "backend" / "app" / "version.py"

CHECKS = {
    "backend_app_version": (
        REPO_ROOT / "app" / "backend" / "app" / "version.py",
        r'APP_VERSION = "([^"]+)"',
    ),
    "frontend_index": (
        REPO_ROOT / "app" / "frontend" / "index.html",
        r"v(\d+\.\d+\.\d+)",
    ),
    "frontend_app_js": (
        REPO_ROOT / "app" / "frontend" / "app.js",
        r"v(\d+\.\d+\.\d+)",
    ),
    "readme_focus": (
        REPO_ROOT / "README.md",
        r"## v(\d+\.\d+\.\d+) focus",
    ),
    "readme_ru_focus": (
        REPO_ROOT / "README_RU.md",
        r"## На чем сфокусирован v(\d+\.\d+\.\d+)",
    ),
    "changelog_latest": (
        REPO_ROOT / "CHANGELOG.md",
        r"## v(\d+\.\d+\.\d+)",
    ),
}


def discover_version() -> str:
    text = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'APP_VERSION = "([^"]+)"', text)
    if not match:
        raise RuntimeError("Unable to discover APP_VERSION.")
    return match.group(1)


def extract_version(path: Path, pattern: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text)
    return match.group(1) if match else None


def tags_at_head() -> list[str]:
    result = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [item.strip() for item in result.stdout.splitlines() if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check release version consistency.")
    parser.add_argument(
        "--expected",
        help="Optional explicit expected version. Defaults to APP_VERSION.",
    )
    parser.add_argument(
        "--require-tag",
        action="store_true",
        help="Require HEAD to carry the matching vX.Y.Z Git tag.",
    )
    args = parser.parse_args()
    expected = args.expected or discover_version()

    failures: list[str] = []
    for label, (path, pattern) in CHECKS.items():
        found = extract_version(path, pattern)
        if found != expected:
            failures.append(f"{label}: expected {expected}, found {found!r}")

    if args.require_tag:
        expected_tag = f"v{expected}"
        try:
            tags = tags_at_head()
        except (OSError, subprocess.CalledProcessError) as exc:
            failures.append(f"git_tag_check: unable to inspect HEAD tags: {exc}")
        else:
            if expected_tag not in tags:
                failures.append(
                    f"git_tag: expected {expected_tag} at HEAD, found {tags or 'none'}"
                )

    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 1

    print(f"version-consistency-ok:{expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
