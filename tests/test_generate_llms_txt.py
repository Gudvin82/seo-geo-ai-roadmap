from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "generate_llms_txt.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_help_works() -> None:
    result = run_command("--help")
    assert result.returncode == 0
    assert "Generate llms.txt" in result.stdout


def test_valid_sitemap_generates_output(tmp_path: Path) -> None:
    sitemap = tmp_path / "sitemap.xml"
    output = tmp_path / "llms.txt"
    sitemap.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc><lastmod>2026-06-01</lastmod></url>
  <url><loc>https://example.com/faq</loc><lastmod>2026-06-02</lastmod></url>
  <url><loc>https://example.com/about</loc><lastmod>2026-06-03</lastmod></url>
</urlset>
""",
        encoding="utf-8",
    )
    result = run_command("--sitemap-file", str(sitemap), "--output-file", str(output))
    assert result.returncode == 0
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "Homepage, positioning, and navigation" in content
    assert "FAQ and direct answers" in content
    assert "Processed URLs: 3" in result.stdout


def test_invalid_xml_returns_non_zero(tmp_path: Path) -> None:
    sitemap = tmp_path / "broken.xml"
    sitemap.write_text("<urlset><url></urlset>", encoding="utf-8")
    result = run_command("--sitemap-file", str(sitemap))
    assert result.returncode == 1
    assert "Invalid XML sitemap" in result.stderr


def test_empty_sitemap_returns_non_zero(tmp_path: Path) -> None:
    sitemap = tmp_path / "empty.xml"
    sitemap.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>
""",
        encoding="utf-8",
    )
    result = run_command("--sitemap-file", str(sitemap))
    assert result.returncode == 1
    assert "Zero URLs parsed from sitemap" in result.stderr
