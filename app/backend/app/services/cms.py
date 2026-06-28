from __future__ import annotations

import json
from typing import Any

from .script_runner import run_script

CMS_CONTRACT_VERSION = "v6.5.0"

CMS_CONTRACTS: dict[str, dict[str, Any]] = {
    "wordpress": {
        "cms_type": "wordpress",
        "readiness_tier": "production_guided",
        "execution_mode": "inventory_plus_reviewed_patch_flow",
        "required_env_vars": ["WORDPRESS_APP_PASSWORD"],
        "production_path": [
            "inventory sync",
            "draft patch generation",
            "review bundle export",
            "human-approved publish",
        ],
        "next_step": "Use WordPress for the deepest reviewed path: inventory first, then controlled patch bundles.",
    },
    "webflow": {
        "cms_type": "webflow",
        "readiness_tier": "production_guided",
        "execution_mode": "inventory_plus_exported_patch_flow",
        "required_env_vars": ["WEBFLOW_API_TOKEN"],
        "production_path": [
            "inventory sync",
            "metadata patch plan",
            "schema patch plan",
            "human review before publish",
        ],
        "next_step": "Treat Webflow as governed export-first delivery, not silent writeback.",
    },
    "bitrix": {
        "cms_type": "bitrix",
        "readiness_tier": "production_guided",
        "execution_mode": "inventory_plus_review_gate",
        "required_env_vars": ["BITRIX_WEBHOOK_TOKEN"],
        "production_path": [
            "inventory sync",
            "field mapping validation",
            "patch export",
            "human-approved publish",
        ],
        "next_step": "Validate field mapping and approval path before proposing any publish automation.",
    },
    "tilda": {
        "cms_type": "tilda",
        "readiness_tier": "production_guided",
        "execution_mode": "inventory_plus_manual_apply",
        "required_env_vars": ["TILDA_API_KEY"],
        "production_path": [
            "inventory sync",
            "draft recommendations",
            "manual apply checklist",
            "re-audit after changes",
        ],
        "next_step": "Use Tilda as a governed manual-apply path backed by strong patch packages and re-audits.",
    },
}


def cms_contract(cms_type: str) -> dict[str, Any]:
    cms = cms_type.strip().lower()
    if cms not in CMS_CONTRACTS:
        raise ValueError(f"Unsupported cms_type '{cms_type}'.")
    return {
        **CMS_CONTRACTS[cms],
        "contract_version": CMS_CONTRACT_VERSION,
    }


def all_cms_contracts() -> list[dict[str, Any]]:
    return [cms_contract(key) for key in sorted(CMS_CONTRACTS)]


def inventory_cms(
    cms_type: str, base_url: str, auth_env_var: str | None = None
) -> dict[str, Any]:
    cms = cms_type.strip().lower()
    contract = cms_contract(cms)
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
            payload["contract"] = contract
            return payload
        return {
            "base_url": base_url,
            "cms_type": "wordpress",
            "status": "starter_fallback",
            "note": stderr
            or "Live WordPress inventory unavailable; returning starter fallback.",
            "pages": [],
            "posts": [],
            "mapping": ["title", "slug", "status", "link"],
            "contract": contract,
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
        "contract": contract,
    }


def cms_patch_package(
    cms_type: str,
    mode: str,
    project_name: str,
    website_url: str,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    top_findings = findings[:5]
    contract = cms_contract(cms_type)
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
        "contract": contract,
    }
