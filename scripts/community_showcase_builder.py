from __future__ import annotations

import argparse
import json
from pathlib import Path


def infer_case_type(path: Path, text: str) -> str:
    lowered = f"{path.as_posix()} {text.lower()}"
    if "synthetic" in lowered:
        return "synthetic"
    if "case study" in lowered or "кейс" in lowered:
        return "public_case"
    return "reference"


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def summarize_case(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = extract_title(text, path.stem.replace("-", " "))
    case_type = infer_case_type(path, text)
    lowered = text.lower()
    language = "ru" if "/ru/" in path.as_posix() or "сводка" in lowered else "en"
    return {
        "path": path.as_posix(),
        "title": title,
        "case_type": case_type,
        "language": language,
        "publishable": case_type in {"public_case", "synthetic"},
        "recommended_use": (
            "public showcase"
            if case_type == "public_case"
            else "training/demo"
            if case_type == "synthetic"
            else "reference"
        ),
    }


def build_payload(paths: list[Path]) -> dict:
    items = [summarize_case(path) for path in paths]
    return {
        "case_count": len(items),
        "public_case_count": sum(
            1 for item in items if item["case_type"] == "public_case"
        ),
        "synthetic_case_count": sum(
            1 for item in items if item["case_type"] == "synthetic"
        ),
        "items": items,
        "next_steps": [
            "promote bounded public cases in SHOWCASE.md",
            "use synthetic cases only as labeled demo/training material",
            "attach proof boundaries before turning any case into a public post",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a compact community showcase index from case files."
    )
    parser.add_argument("paths", nargs="+", help="Markdown case or showcase files")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    paths = [Path(value) for value in args.paths]
    payload = build_payload(paths)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Community Showcase Index")
    print()
    print(f"- Total items: {payload['case_count']}")
    print(f"- Public cases: {payload['public_case_count']}")
    print(f"- Synthetic cases: {payload['synthetic_case_count']}")
    print()
    for item in payload["items"]:
        print(f"## {item['title']}")
        print()
        print(f"- Path: `{item['path']}`")
        print(f"- Type: `{item['case_type']}`")
        print(f"- Language: `{item['language']}`")
        print(f"- Recommended use: {item['recommended_use']}")
        print()
    print("## Next steps")
    print()
    for step in payload["next_steps"]:
        print(f"- {step}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
