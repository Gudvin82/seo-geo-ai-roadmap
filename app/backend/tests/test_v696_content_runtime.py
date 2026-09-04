from __future__ import annotations

import json

from app.services import integrations


def test_indexnow_runtime_uses_env_key_without_process_argument(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_run_script(script_name: str, args: list[str]):
        captured["script_name"] = script_name
        captured["args"] = args
        return (
            0,
            json.dumps(
                {
                    "source": "indexnow-live",
                    "submission": {"status": "accepted", "http_status": 200},
                }
            ),
            "",
        )

    monkeypatch.setenv("INDEXNOW_KEY", "secret-indexnow-key")
    monkeypatch.setattr(integrations, "run_script", fake_run_script)
    payload = integrations.sync_integration_source(
        "indexnow",
        property_identifier="example.com",
        config={"urls": ["https://example.com/new-page"]},
    )

    assert payload["source"] == "indexnow-live"
    assert captured["script_name"] == "indexnow_submit.py"
    assert "secret-indexnow-key" not in captured["args"]
