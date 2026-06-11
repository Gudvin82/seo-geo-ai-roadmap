from __future__ import annotations

import json
from datetime import datetime
from typing import Optional


def build_markdown_report(
    language: str,
    project_name: str,
    findings: list[dict],
    score: Optional[float],
) -> str:
    is_ru = language.lower().startswith("ru")
    title = "Отчет по discoverability" if is_ru else "Discoverability report"
    summary = "Краткое резюме" if is_ru else "Executive summary"
    next_actions = "Следующие действия" if is_ru else "Next actions"
    sections = []
    for finding in findings:
        sections.append(
            f"## {finding['title']}\n\n"
            f"- Severity: {finding['severity']}\n"
            f"- Category: {finding['category']}\n"
            f"- Summary: {finding['summary']}\n"
        )
    top_actions = "\n".join(f"- {finding['recommendation']}" for finding in findings[:5])
    return (
        f"# {title}: {project_name}\n\n"
        f"- Generated at: {datetime.utcnow().isoformat()}Z\n"
        f"- Score: {score if score is not None else 'n/a'}\n\n"
        f"## {summary}\n\n"
        f"Total findings: {len(findings)}\n\n"
        f"{''.join(sections)}\n"
        f"## {next_actions}\n\n"
        f"{top_actions or '- Review findings and artifacts'}\n"
    )


def build_json_report(project_name: str, findings: list[dict], score: Optional[float]) -> dict:
    return {
        "project_name": project_name,
        "generated_at": f"{datetime.utcnow().isoformat()}Z",
        "summary_score": score,
        "findings": findings,
    }


def dumps_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)
