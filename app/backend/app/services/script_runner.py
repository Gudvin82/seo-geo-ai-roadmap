from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def run_script(script_name: str, args: list[str]) -> tuple[int, str, str]:
    script_path = SCRIPTS_DIR / script_name
    try:
        completed = subprocess.run(
            [sys.executable, str(script_path), *args],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        return completed.returncode, completed.stdout, completed.stderr
    except BlockingIOError:
        return _run_script_in_process(script_path, args)


def _run_script_in_process(script_path: Path, args: list[str]) -> tuple[int, str, str]:
    spec = importlib.util.spec_from_file_location(
        f"script_runner_{script_path.stem}", script_path
    )
    if spec is None or spec.loader is None:
        return 1, "", f"Unable to load script: {script_path.name}"

    module = importlib.util.module_from_spec(spec)
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    original_argv = sys.argv[:]

    try:
        spec.loader.exec_module(module)
        main = getattr(module, "main", None)
        if not callable(main):
            return 1, "", f"Script does not expose main(): {script_path.name}"
        sys.argv = [str(script_path), *args]
        with (
            contextlib.redirect_stdout(stdout_buffer),
            contextlib.redirect_stderr(stderr_buffer),
        ):
            result = main()
        return int(result or 0), stdout_buffer.getvalue(), stderr_buffer.getvalue()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
        return code, stdout_buffer.getvalue(), stderr_buffer.getvalue()
    except Exception as exc:  # pragma: no cover - defensive fallback boundary
        print(f"{exc.__class__.__name__}: {exc}", file=stderr_buffer)
        return 1, stdout_buffer.getvalue(), stderr_buffer.getvalue()
    finally:
        sys.argv = original_argv
