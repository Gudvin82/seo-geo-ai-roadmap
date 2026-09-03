from __future__ import annotations

import json
from pathlib import Path

from tests.script_harness import run_script_main


def test_content_ops_queue_is_sorted_and_approval_first(tmp_path: Path) -> None:
    source = tmp_path / "topics.csv"
    source.write_text(
        "topic,intent,demand,business_value,evidence_strength,effort\n"
        "low priority,mixed,20,20,20,70\n"
        "high priority,commercial,90,90,90,20\n",
        encoding="utf-8",
    )
    result = run_script_main(
        "scripts/content_ops_queue.py", "--file", str(source), "--format", "json"
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["mode"] == "approval_first_content_operations"
    assert payload["items"][0]["topic"] == "high priority"
    assert payload["items"][0]["stage"] == "brief_required"
    assert "editorial and legal approval" in payload["items"][0]["required_gates"]
