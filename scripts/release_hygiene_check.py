from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    version = read("app/backend/app/version.py")
    match = re.search(r'APP_VERSION = "(\d+\.\d+\.\d+)"', version)
    if not match:
        print("release-hygiene-failed:app-version-missing")
        return 1
    app_version = match.group(1)
    tag_version = f"v{app_version}"
    checks = {
        "README.md": tag_version,
        "README_RU.md": tag_version,
        "DOCS_INDEX.md": tag_version,
        "DOCS_INDEX_RU.md": tag_version,
        "PUBLIC_PRODUCT_READINESS.md": tag_version,
        "PUBLIC_PRODUCT_READINESS_RU.md": tag_version,
        "app/frontend/index.html": tag_version,
        "app/frontend/app.js": tag_version,
    }
    failures: list[str] = []
    for path, needle in checks.items():
        if needle not in read(path):
            failures.append(f"{path}:missing:{needle}")
    existence_checks = [
        "README_EN.md",
        "SUPPORT.md",
        "SECURITY.md",
        "docs/i18n-status.md",
        "assets/roadmap-visual.svg",
    ]
    for path in existence_checks:
        if not (ROOT / path).exists():
            failures.append(f"{path}:missing")
    release_doc = ROOT / "docs" / "en" / f"v{app_version.replace('.', '')}-release.md"
    release_doc_ru = (
        ROOT / "docs" / "ru" / f"v{app_version.replace('.', '')}-release.md"
    )
    if not release_doc.exists():
        failures.append(f"{release_doc.relative_to(ROOT)}:missing")
    if not release_doc_ru.exists():
        failures.append(f"{release_doc_ru.relative_to(ROOT)}:missing")
    if failures:
        print("release-hygiene-failed")
        for row in failures:
            print(row)
        return 1
    print(f"release-hygiene-ok:{app_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
