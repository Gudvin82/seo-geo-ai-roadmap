from __future__ import annotations

import json
from typing import Any

from .script_runner import run_script


def inventory_cms(
    cms_type: str, base_url: str, auth_env_var: str | None = None
) -> dict[str, Any]:
    cms = cms_type.strip().lower()
    if cms == "wordpress":
        code, stdout, stderr = run_script(
            "wordpress_connector_starter.py", ["--base-url", base_url]
        )
        if code == 0:
            payload = json.loads(stdout)
            payload["writeback_support"] = [
                "read_only inventory",
                "draft metadata suggestions",
                "human-approved publish package",
            ]
            payload["mapping"] = ["title", "slug", "status", "link"]
            return payload
        return {
            "base_url": base_url,
            "cms_type": "wordpress",
            "status": "starter_fallback",
            "note": stderr or "Live WordPress inventory unavailable; returning starter fallback.",
            "pages": [],
            "posts": [],
            "mapping": ["title", "slug", "status", "link"],
        }
    return {
        "base_url": base_url,
        "cms_type": cms,
        "status": "starter",
        "auth_env_var": auth_env_var,
        "supported_modes": ["read_only", "draft", "human_approved_publish"],
        "mapping": ["title", "slug", "status", "url", "metadata"],
        "note": (
            f"{cms_type} starter connector prepared. Use it for inventory, mapping, "
            "and export of suggested changes before enabling deeper writeback."
        ),
    }


def cms_patch_package(
    cms_type: str,
    mode: str,
    project_name: str,
    website_url: str,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    top_findings = findings[:5]
    return {
        "cms_type": cms_type,
        "review_mode": mode,
        "safe_actions": [
            "read content inventory",
            "prepare metadata patches",
            "prepare schema patches",
            "prepare llms.txt and FAQ suggestions",
        ],
        "requires_review": [
            "title rewrites",
            "schema changes",
            "navigation edits",
            "publish operations",
        ],
        "unsupported": [
            "silent destructive content replacement",
            "automatic publish without review",
        ],
        "suggested_changes": [
            {
                "path_hint": website_url,
                "title": item.get("title", "Fix required"),
                "summary": item.get("summary", ""),
                "recommendation": item.get("recommendation", ""),
            }
            for item in top_findings
        ],
        "project_name": project_name,
    }
