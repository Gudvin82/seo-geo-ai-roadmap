#!/usr/bin/env python3
"""Generate a ready-to-paste handoff prompt for an AI coding agent."""

from __future__ import annotations

import argparse
import json


REPO_URL = "https://github.com/Gudvin82/seo-geo-ai-roadmap"


TASKS = {
    "audit-site": {
        "en": {
            "title": "Audit one real website",
            "goal": "Deploy the platform, create the project, run the audit flow, and return an executive summary plus a fix backlog.",
            "steps": [
                "Read README.md, AGENTS.md, and START_HERE_FOR_AI.md first.",
                "Clone the repository and deploy the demo-safe self-hosted stack.",
                "Run make verify-demo and make agent-self-check before using the app.",
                "Create one workspace and one project for the target site.",
                "Fill brand facts, run one audit, run one AI SoV check, and review artifacts.",
                "Return a concise executive summary, score breakdown, quick wins, strategic fixes, and open risks.",
            ],
        },
        "ru": {
            "title": "Провести аудит реального сайта",
            "goal": "Развернуть платформу, создать проект, прогнать audit-flow и вернуть executive summary с backlog исправлений.",
            "steps": [
                "Сначала прочитай README_RU.md, AGENTS.md и START_HERE_FOR_AI_RU.md.",
                "Клонируй репозиторий и разверни demo-safe self-hosted стек.",
                "До использования app выполни make verify-demo и make agent-self-check.",
                "Создай один workspace и один project для целевого сайта.",
                "Заполни brand facts, запусти один audit, один AI SoV check и просмотри artifacts.",
                "Верни краткий executive summary, score breakdown, quick wins, strategic fixes и открытые риски.",
            ],
        },
    },
    "deploy-demo": {
        "en": {
            "title": "Deploy a demo instance",
            "goal": "Bring up a local or server demo that another operator can immediately open and verify.",
            "steps": [
                "Read README.md, AGENTS.md, and START_HERE_FOR_AI.md first.",
                "Clone the repository and copy .env.example to .env.",
                "Run make turnkey-demo, then make verify-demo and make agent-self-check.",
                "Return URLs, credentials, verification results, and any remaining manual steps.",
            ],
        },
        "ru": {
            "title": "Развернуть demo-инстанс",
            "goal": "Поднять локальное или серверное demo, которое другой оператор сразу сможет открыть и проверить.",
            "steps": [
                "Сначала прочитай README_RU.md, AGENTS.md и START_HERE_FOR_AI_RU.md.",
                "Клонируй репозиторий и скопируй .env.example в .env.",
                "Выполни make turnkey-demo, затем make verify-demo и make agent-self-check.",
                "Верни URL, credentials, результаты проверки и оставшиеся ручные шаги.",
            ],
        },
    },
    "deploy-scanner": {
        "en": {
            "title": "Deploy a reusable scanner surface",
            "goal": "Use the repository as the base for a client-facing or internal scanner that accepts a site and returns a structured audit.",
            "steps": [
                "Read README.md, AGENTS.md, START_HERE_FOR_AI.md, and ARCHITECTURE_NOTE.md first.",
                "Choose the scanner deployment path and run python scripts/bootstrap_self_hosted.py --mode scanner --format markdown.",
                "Deploy the stack, verify health endpoints, and keep the intake behind consent or authenticated access unless explicitly approved.",
                "Connect the intake flow to workspace/project creation and the audit/report path already present in the app.",
                "Return the architecture, public entrypoint, verification status, limitations, and next engineering steps.",
            ],
        },
        "ru": {
            "title": "Развернуть переиспользуемую scanner-поверхность",
            "goal": "Использовать репозиторий как основу для client-facing или internal scanner, который принимает сайт и возвращает структурированный аудит.",
            "steps": [
                "Сначала прочитай README_RU.md, AGENTS.md, START_HERE_FOR_AI_RU.md и ARCHITECTURE_NOTE_RU.md.",
                "Выбери scanner deployment path и выполни python scripts/bootstrap_self_hosted.py --mode scanner --format markdown.",
                "Разверни стек, проверь health endpoints и не открывай intake без consent-модели или авторизованного доступа, если это явно не согласовано.",
                "Свяжи intake-flow с созданием workspace/project и уже существующим audit/report path внутри app.",
                "Верни архитектуру, public entrypoint, статус проверки, ограничения и следующие инженерные шаги.",
            ],
        },
    },
    "client-setup": {
        "en": {
            "title": "Prepare a client-ready setup",
            "goal": "Deploy the platform, create a clean client workspace structure, and prepare a repeatable audit/reporting routine.",
            "steps": [
                "Read README.md, AGENTS.md, START_HERE_FOR_AI.md, and CLIENT_SETUP_PLAYBOOK.md first.",
                "Deploy the stack and verify it with make agent-self-check.",
                "Create one workspace per client and one project per website.",
                "Prepare the operator flow for audit, AI SoV, facts, and report export.",
                "Return the deployed URLs, workspace structure, demo or real access details, and the next weekly operating cadence.",
            ],
        },
        "ru": {
            "title": "Подготовить client-ready setup",
            "goal": "Развернуть платформу, создать чистую клиентскую структуру workspace/project и подготовить повторяемый audit/reporting цикл.",
            "steps": [
                "Сначала прочитай README_RU.md, AGENTS.md, START_HERE_FOR_AI_RU.md и CLIENT_SETUP_PLAYBOOK_RU.md.",
                "Разверни стек и проверь его через make agent-self-check.",
                "Создай отдельный workspace на клиента и отдельный project на сайт.",
                "Подготовь operator flow для audit, AI SoV, facts и export report.",
                "Верни URL развертывания, структуру workspace, demo или real access details и следующий weekly operating cadence.",
            ],
        },
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a ready-to-paste AI handoff prompt for common repository tasks."
    )
    parser.add_argument(
        "--task",
        choices=sorted(TASKS),
        required=True,
        help="Task pack to generate.",
    )
    parser.add_argument(
        "--language",
        choices=["en", "ru"],
        default="en",
        help="Prompt language.",
    )
    parser.add_argument(
        "--target-url",
        default="",
        help="Optional target website URL for audit-oriented tasks.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    return parser


def build_prompt(task: str, language: str, target_url: str) -> dict[str, object]:
    payload = TASKS[task][language].copy()
    payload["task"] = task
    payload["language"] = language
    payload["repository"] = REPO_URL
    if target_url:
        payload["target_url"] = target_url
    rules = {
        "en": [
            "Do not claim success without verification output.",
            "Report what was verified, what was heuristic, and what still needs human review.",
            "Keep EN and RU user-facing layers aligned if you change product scope.",
        ],
        "ru": [
            "Не объявляй успех без verification output.",
            "Отдельно укажи, что реально проверено, что было эвристикой и где нужен human review.",
            "Если меняешь product scope, синхронизируй EN и RU user-facing слои.",
        ],
    }
    payload["rules"] = rules[language]
    return payload


def render_markdown(prompt: dict[str, object]) -> str:
    lines = [
        f"# {prompt['title']}",
        "",
        f"Repository: {prompt['repository']}",
    ]
    if "target_url" in prompt:
        lines.append(f"Target URL: {prompt['target_url']}")
    lines.extend(
        [
            "",
            "## Goal",
            str(prompt["goal"]),
            "",
            "## Steps",
        ]
    )
    for index, step in enumerate(prompt["steps"], start=1):
        lines.append(f"{index}. {step}")
    lines.extend(["", "## Rules"])
    for item in prompt["rules"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()
    prompt = build_prompt(args.task, args.language, args.target_url.strip())
    if args.format == "json":
        print(json.dumps(prompt, ensure_ascii=False, indent=2))
        return 0

    print(render_markdown(prompt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
