from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_monitor_requires_real_evidence_shape() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/ai_visibility_monitor.py"),
            str(ROOT / "examples/ai-visibility-evidence.json"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["contract_version"] == "v1"
    assert payload["coverage"] == 0.5
