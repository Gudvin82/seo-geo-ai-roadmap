from __future__ import annotations

import json
from datetime import datetime
from typing import Optional


def _finding_value(finding: dict, key: str, default: object = "n/a") -> object:
    """Read both the v6.12 canonical contract and historical audit records."""
    if key == "title":
        return (
            finding.get("title")
            or str(finding.get("category", "finding")).replace("_", " ").title()
        )
    if key == "summary":
        return finding.get("summary") or finding.get("observation", default)
    if key == "priority_score":
        return finding.get(
            "priority_score", finding.get("priority", {}).get("score", default)
        )
    if key == "priority_label":
        return finding.get(
            "priority_label", finding.get("priority", {}).get("label", default)
        )
    if key in {"impact", "effort"}:
        return finding.get(key, finding.get("priority", {}).get(key, default))
    return finding.get(key, default)


def build_markdown_report(
    language: str,
    project_name: str,
    findings: list[dict],
    score: Optional[float],
    benchmark_summary: Optional[dict] = None,
    ai_citation_score_value: Optional[float] = None,
) -> str:
    is_ru = language.lower().startswith("ru")
    title = "Отчет по discoverability" if is_ru else "Discoverability report"
    summary = "Краткое резюме" if is_ru else "Executive summary"
    next_actions = "Следующие действия" if is_ru else "Next actions"
    benchmark_title = "Бенчмарки" if is_ru else "Benchmarks"
    priority_label = "Priority" if not is_ru else "Приоритет"
    benchmark_label = "Benchmark status" if not is_ru else "Статус бенчмарка"
    impact_label = "Impact" if not is_ru else "Влияние"
    effort_label = "Effort" if not is_ru else "Сложность"
    confidence_label = "Confidence" if not is_ru else "Уверенность"
    citation_label = "AI Citation Score" if not is_ru else "AI Citation Score"
    sections = []
    for finding in findings:
        sections.append(
            f"## {_finding_value(finding, 'title')}\n\n"
            f"- Severity: {_finding_value(finding, 'severity')}\n"
            f"- Category: {_finding_value(finding, 'category')}\n"
            f"- {priority_label}: {_finding_value(finding, 'priority_label')} ({_finding_value(finding, 'priority_score')})\n"
            f"- {benchmark_label}: {finding.get('benchmark_status', 'insufficient_data')}\n"
            f"- {impact_label}: {_finding_value(finding, 'impact')}\n"
            f"- {effort_label}: {_finding_value(finding, 'effort')}\n"
            f"- {confidence_label}: {_finding_value(finding, 'confidence')}\n"
            f"- Summary: {_finding_value(finding, 'summary')}\n"
        )
    top_actions = "\n".join(
        f"- {_finding_value(finding, 'recommendation', 'Review finding')}"
        for finding in findings[:5]
    )
    benchmark_lines = ""
    if benchmark_summary:
        benchmark_lines = "\n".join(
            f"- {key}: {value}" for key, value in benchmark_summary.items()
        )
    return (
        f"# {title}: {project_name}\n\n"
        f"- Generated at: {datetime.utcnow().isoformat()}Z\n"
        f"- Score: {score if score is not None else 'n/a'}\n\n"
        f"- {citation_label}: {ai_citation_score_value if ai_citation_score_value is not None else 'n/a'}\n\n"
        f"## {summary}\n\n"
        f"Total findings: {len(findings)}\n\n"
        f"## {benchmark_title}\n\n"
        f"{benchmark_lines or '- insufficient_data'}\n\n"
        f"{''.join(sections)}\n"
        f"## {next_actions}\n\n"
        f"{top_actions or '- Review findings and artifacts'}\n"
    )


def build_json_report(
    project_name: str,
    findings: list[dict],
    score: Optional[float],
    benchmark_summary: Optional[dict] = None,
    ai_citation_score_value: Optional[float] = None,
) -> dict:
    return {
        "project_name": project_name,
        "generated_at": f"{datetime.utcnow().isoformat()}Z",
        "summary_score": score,
        "ai_citation_score": ai_citation_score_value,
        "benchmark_summary": benchmark_summary or {},
        "findings": findings,
    }


def dumps_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)
