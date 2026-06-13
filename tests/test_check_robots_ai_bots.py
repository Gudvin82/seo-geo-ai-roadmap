from __future__ import annotations

import contextlib
import io
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check-robots-ai-bots.py"


def run_script(*args: str) -> tuple[int, str, str]:
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


def test_help_works() -> None:
    code, stdout, _stderr = run_script("--help")
    assert code == 0
    assert "robots.txt" in stdout
