from __future__ import annotations

import json
import urllib.parse
import urllib.request


def command_to_endpoint(api_base: str, command: str) -> str:
    cleaned = command.strip()
    if cleaned.startswith("/geo audit "):
        target = cleaned.replace("/geo audit ", "", 1).strip()
        return f"{api_base}/scanner/url-audit?target={urllib.parse.quote(target)}"
    if cleaned.startswith("/geo latest "):
        project_id = cleaned.replace("/geo latest ", "", 1).strip()
        return f"{api_base}/settings/executive-dashboard?project_id={project_id}"
    if cleaned.startswith("/geo alerts"):
        return f"{api_base}/agent-mode/contract"
    raise ValueError("Unsupported Telegram shortcut command.")


def telegram_message_preview(api_base: str, command: str) -> str:
    endpoint = command_to_endpoint(api_base, command)
    payload = {"command": command, "endpoint": endpoint}
    return json.dumps(payload, ensure_ascii=False, indent=2)


def fetch_preview(api_base: str, command: str) -> str:
    request = urllib.request.Request(command_to_endpoint(api_base, command))
    with urllib.request.urlopen(request, timeout=20) as response:  # pragma: no cover - networked path
        return response.read().decode("utf-8")
