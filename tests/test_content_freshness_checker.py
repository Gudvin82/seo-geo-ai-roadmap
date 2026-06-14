from __future__ import annotations

from pathlib import Path

from tests.script_harness import run_script_main


def run_command(*args: str):
    return run_script_main("scripts/content_freshness_checker.py", *args)


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
