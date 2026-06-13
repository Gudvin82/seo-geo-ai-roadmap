from __future__ import annotations

import contextlib
import io
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check-llms-txt.py"


def run_command(*args: str) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(SCRIPT), *args]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(SCRIPT), run_name="__main__")
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 0
            else:
                code = 0
    finally:
        sys.argv = original_argv
    return code, stdout.getvalue(), stderr.getvalue()


def test_valid_llms_file_passes(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text(
        """# Example
> https://example.com/ - Homepage
> https://example.com/faq - FAQ
> https://example.com/about - About
""",
        encoding="utf-8",
    )
    code, stdout, _stderr = run_command("--file", str(llms_file))
    assert code == 0
    assert "PASS" in stdout


def test_missing_required_sections_fails(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text(
        "# Example\n> https://example.com/ - Homepage\n", encoding="utf-8"
    )
    code, stdout, _stderr = run_command("--file", str(llms_file))
    assert code == 1
    assert "faq" in stdout.lower()
    assert "about" in stdout.lower()


def test_malformed_structure_fails(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text("homepage\nfaq\nabout\n", encoding="utf-8")
    code, stdout, _stderr = run_command("--file", str(llms_file))
    assert code == 1
    assert (
        "top-level heading" in stdout.lower() or "structured entries" in stdout.lower()
    )
