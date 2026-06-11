from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def run_script(script_name: str, args: list[str]) -> tuple[int, str, str]:
    script_path = SCRIPTS_DIR / script_name
    completed = subprocess.run(
        [sys.executable, str(script_path), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return completed.returncode, completed.stdout, completed.stderr
