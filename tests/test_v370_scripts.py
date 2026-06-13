from __future__ import annotations

import contextlib
import io
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(script_name: str, *args: str) -> tuple[int, str, str]:
    script = REPO_ROOT / "scripts" / script_name
    stdout = io.StringIO()
    stderr = io.StringIO()
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(script), *args]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 0
            else:
                code = 0
    finally:
        sys.argv = original_argv
    return code, stdout.getvalue(), stderr.getvalue()


def test_ai_txt_validator_passes_valid_file(tmp_path: Path) -> None:
    ai_file = tmp_path / "ai.txt"
    llms_file = tmp_path / "llms.txt"
    robots_file = tmp_path / "robots.txt"
    ai_file.write_text(
        "policy: allow-public-facts\nsummary: Keep guidance explicit.\nallow: /\nllms: https://example.com/llms.txt\n",
        encoding="utf-8",
    )
    llms_file.write_text("# Example\n> https://example.com/ - Home\n", encoding="utf-8")
    robots_file.write_text("User-agent: GPTBot\nAllow: /\n", encoding="utf-8")
    code, stdout, _stderr = _run(
        "check-ai-txt.py",
        "--file",
        str(ai_file),
        "--robots-file",
        str(robots_file),
        "--llms-file",
        str(llms_file),
    )
    assert code == 0
    assert "PASS" in stdout


def test_ai_txt_validator_fails_malformed_file(tmp_path: Path) -> None:
    ai_file = tmp_path / "ai.txt"
    ai_file.write_text("allow /\nnotes only\n", encoding="utf-8")
    code, stdout, _stderr = _run("check-ai-txt.py", "--file", str(ai_file))
    assert code == 1
    assert "malformed" in stdout.lower() or "missing" in stdout.lower()


def test_schema_coverage_checker_warns_on_partial_schema(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        '<html><head><script type=\'application/ld+json\'>{"@context":"https://schema.org","@type":"Organization"}</script></head><body></body></html>',
        encoding="utf-8",
    )
    code, stdout, _stderr = _run(
        "schema-coverage-checker.py",
        "--file",
        str(html_file),
        "--site-type",
        "service",
    )
    assert code == 1
    assert "WebSite" in stdout


def test_faq_detector_reports_questions(tmp_path: Path) -> None:
    html_file = tmp_path / "faq.html"
    html_file.write_text(
        "<html><body><section id='faq'><h2>FAQ</h2><h3>What do you do?</h3></section></body></html>",
        encoding="utf-8",
    )
    code, stdout, _stderr = _run("faq-detector.py", "--file", str(html_file))
    assert code == 0
    assert "FAQ" in stdout


def test_open_graph_checker_fails_missing_fields(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        "<html><head><meta property='og:title' content='Home' /></head><body></body></html>",
        encoding="utf-8",
    )
    code, stdout, _stderr = _run("open-graph-checker.py", "--file", str(html_file))
    assert code == 1
    assert "Missing fields" in stdout
