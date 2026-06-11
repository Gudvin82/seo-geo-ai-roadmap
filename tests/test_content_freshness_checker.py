from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "content_freshness_checker.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_generates_markdown_report(tmp_path: Path) -> None:
    sitemap = tmp_path / "sitemap.xml"
    output = tmp_path / "freshness.md"
    sitemap.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc><lastmod>2026-06-01</lastmod></url>
  <url><loc>https://example.com/old</loc><lastmod>2020-01-01</lastmod></url>
  <url><loc>https://example.com/unknown</loc></url>
</urlset>
""",
        encoding="utf-8",
    )
    result = run_command(
        "--sitemap-file",
        str(sitemap),
        "--days-stale",
        "180",
        "--output-file",
        str(output),
    )
    assert result.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert "Content freshness report" in content
    assert "stale" in content
    assert "unknown freshness" in content
