from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ScriptResult:
    returncode: int
    stdout: str
    stderr: str


def _load_module(script_path: Path):
    module_name = f"test_module_{script_path.stem}_{abs(hash(script_path))}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_script_main(script_relative_path: str, *args: str) -> ScriptResult:
    script_path = REPO_ROOT / script_relative_path
    module = _load_module(script_path)
    if not hasattr(module, "main"):
        raise RuntimeError(f"Script {script_relative_path} has no main()")

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    argv_before = sys.argv[:]
    sys.argv = [str(script_path), *args]
    try:
        with (
            contextlib.redirect_stdout(stdout_buffer),
            contextlib.redirect_stderr(stderr_buffer),
        ):
            try:
                result = module.main()
                returncode = int(result) if isinstance(result, int) else 0
            except SystemExit as exc:  # pragma: no cover - defensive
                code = exc.code
                returncode = int(code) if isinstance(code, int) else 0
    finally:
        sys.argv = argv_before

    return ScriptResult(
        returncode=returncode,
        stdout=stdout_buffer.getvalue(),
        stderr=stderr_buffer.getvalue(),
    )
