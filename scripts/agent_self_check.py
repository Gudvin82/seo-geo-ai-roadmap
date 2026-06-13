from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()


def main() -> int:
    checks = [
        {
            "id": "readme_positioning",
            "label": "README exists for agent framing",
            "passed": exists("README.md") and exists("README_RU.md"),
        },
        {
            "id": "agent_entrypoint",
            "label": "AGENTS.md exists with deploy guidance",
            "passed": exists("AGENTS.md"),
        },
        {
            "id": "ai_start_here",
            "label": "AI-first handoff docs exist",
            "passed": all(
                exists(path)
                for path in [
                    "START_HERE_FOR_AI.md",
                    "START_HERE_FOR_AI_RU.md",
                    "CLIENT_SETUP_PLAYBOOK.md",
                    "CLIENT_SETUP_PLAYBOOK_RU.md",
                    "AI_HANDOFF_PROMPT.md",
                    "AI_HANDOFF_PROMPT_RU.md",
                ]
            ),
        },
        {
            "id": "deployment_docs",
            "label": "Deployment and verification docs exist",
            "passed": all(
                exists(path)
                for path in [
                    "DEPLOYMENT.md",
                    "DEPLOYMENT_RU.md",
                    "VERIFY_DEPLOYMENT.md",
                    "VERIFY_DEPLOYMENT_RU.md",
                ]
            ),
        },
        {
            "id": "self_hosted_stack",
            "label": "Self-hosted stack files exist",
            "passed": all(
                exists(path)
                for path in [
                    "docker-compose.yml",
                    ".env.example",
                    ".env.production.example",
                    "Makefile",
                ]
            ),
        },
        {
            "id": "app_layer",
            "label": "App layer entrypoints exist",
            "passed": all(
                exists(path)
                for path in [
                    "app/backend/app/main.py",
                    "app/frontend/index.html",
                    "app/backend/app/api/audit_runs.py",
                ]
            ),
        },
        {
            "id": "operator_docs",
            "label": "Operator docs exist in EN and RU",
            "passed": all(
                exists(path)
                for path in [
                    "docs/en/ai-operator-mode.md",
                    "docs/ru/ai-operator-mode.md",
                    "docs/en/api-reference.md",
                    "docs/ru/api-reference.md",
                    "docs/en/provider-matrix.md",
                    "docs/ru/provider-matrix.md",
                    "docs/en/local-llm-matrix.md",
                    "docs/ru/local-llm-matrix.md",
                    "docs/en/provider-benchmarks.md",
                    "docs/ru/provider-benchmarks.md",
                    "docs/en/search-data-connectors.md",
                    "docs/ru/search-data-connectors.md",
                ]
            ),
        },
        {
            "id": "proof_assets",
            "label": "Proof assets exist",
            "passed": all(
                exists(path)
                for path in [
                    "docs_site/assets/screenshots/app-overview-proof.svg",
                    "docs_site/assets/screenshots/report-flow-proof.svg",
                    "docs_site/assets/screenshots/login-dashboard-proof.svg",
                    "docs_site/assets/screenshots/provider-access-proof.svg",
                ]
            ),
        },
        {
            "id": "local_llm_support",
            "label": "Local LLM support files exist",
            "passed": all(
                exists(path)
                for path in [
                    "app/backend/app/providers/registry.py",
                    "docs/en/provider-matrix.md",
                    "docs/ru/provider-matrix.md",
                ]
            ),
        },
        {
            "id": "self_check_script",
            "label": "Agent self-check is present",
            "passed": exists("scripts/agent_self_check.py"),
        },
        {
            "id": "v330_operational_docs",
            "label": "v3.3.0 operational and evaluation docs exist",
            "passed": all(
                exists(path)
                for path in [
                    "docs/en/operational-retries.md",
                    "docs/ru/operational-retries.md",
                    "docs/en/scheduled-operations.md",
                    "docs/ru/scheduled-operations.md",
                    "docs/en/fact-drift-monitoring.md",
                    "docs/ru/fact-drift-monitoring.md",
                    "COMMERCIAL_ROADMAP.md",
                    "COMMERCIAL_ROADMAP_RU.md",
                    "EVALUATE_THIS_REPO.md",
                    "EVALUATE_THIS_REPO_RU.md",
                ]
            ),
        },
        {
            "id": "v340_command_surface",
            "label": "v3.4.0 command surface and bootstrap assets exist",
            "passed": all(
                exists(path)
                for path in [
                    "scripts/geo_command_surface.py",
                    "scripts/bootstrap_self_hosted.py",
                    "docs/en/command-catalog-v340.md",
                    "docs/ru/command-catalog-v340.md",
                    "docs/en/bootstrap-guide-v340.md",
                    "docs/ru/bootstrap-guide-v340.md",
                    "docs/en/how-it-works-v340.md",
                    "docs/ru/how-it-works-v340.md",
                ]
            ),
        },
    ]

    passed_count = sum(1 for item in checks if item["passed"])
    total = len(checks)
    score = round((passed_count / total) * 100, 1)

    result = {
        "project": "seo-geo-ai-roadmap",
        "mode": "agent-self-check",
        "score_percent": score,
        "passed": passed_count,
        "total": total,
        "status": "pass" if passed_count == total else "needs-review",
        "checks": checks,
        "next_step": (
            "If any check fails, the agent should fix the missing layer before claiming turnkey readiness."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed_count == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
