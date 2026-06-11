from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from sqlalchemy.orm import Session

from ..config import Settings
from ..database import create_session
from ..metrics import PROVIDER_CALLS, PROVIDER_FAILURES, REPORT_GENERATIONS
from ..models import (
    Artifact,
    AuditRun,
    BrandFactsProfile,
    Project,
    ProviderConfiguration,
    Report,
)
from ..providers.base import ProviderError
from ..providers.registry import build_provider
from .reporting import build_json_report, build_markdown_report, dumps_json
from .script_runner import run_script


def _artifact_path(
    settings: Settings, audit_run_id: int, slug: str, extension: str
) -> Path:
    artifact_dir = Path(settings.artifact_root) / f"audit-run-{audit_run_id}"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    return artifact_dir / f"{slug}.{extension}"


def _persist_artifact(
    db: Session,
    audit_run: AuditRun,
    project: Project,
    settings: Settings,
    artifact_type: str,
    content: str,
    fmt: str,
    metadata: dict,
) -> Artifact:
    extension = "json" if fmt == "json" else "md"
    path = _artifact_path(settings, audit_run.id, artifact_type, extension)
    path.write_text(content, encoding="utf-8")
    artifact = Artifact(
        audit_run_id=audit_run.id,
        project_id=project.id,
        artifact_type=artifact_type,
        format=fmt,
        file_path=str(path),
        metadata_json=json.dumps(metadata, ensure_ascii=False),
    )
    db.add(artifact)
    db.flush()
    return artifact


def _brand_profile(db: Session, project_id: int) -> Optional[BrandFactsProfile]:
    return (
        db.query(BrandFactsProfile)
        .filter(BrandFactsProfile.project_id == project_id)
        .order_by(BrandFactsProfile.id.desc())
        .first()
    )


def _provider_note(
    provider: Optional[ProviderConfiguration], prompt: str, settings: Settings
) -> tuple[str, dict]:
    if not provider or not provider.is_enabled:
        return "Provider commentary skipped: no enabled provider configuration.", {
            "status": "skipped"
        }
    env_var = provider.api_key_env_var or f"{provider.provider_name.upper()}_API_KEY"
    api_key = getattr(
        settings, f"{provider.provider_name.lower()}_api_key", ""
    ) or os.getenv(env_var, "")
    try:
        client = build_provider(
            provider.provider_name,
            api_key=api_key,
            model=provider.model,
            base_url=provider.base_url,
        )
        response = client.generate_text(
            prompt, system_prompt="You are a discoverability audit assistant."
        )
        PROVIDER_CALLS.labels(
            provider=provider.provider_name, status=response.status
        ).inc()
        return response.content, {
            "status": response.status,
            "provider": response.provider,
            "model": response.model,
        }
    except ProviderError as exc:
        PROVIDER_CALLS.labels(provider=provider.provider_name, status="error").inc()
        PROVIDER_FAILURES.labels(provider=provider.provider_name).inc()
        return f"Provider commentary unavailable: {exc}", {
            "status": "error",
            "error": str(exc),
        }


def execute_audit_run(
    db: Session,
    audit_run: AuditRun,
    settings: Settings,
    provider_config_id: Optional[int] = None,
) -> None:
    project = db.get(Project, audit_run.project_id)
    if not project:
        audit_run.status = "failed"
        db.commit()
        return
    selected_checks = json.loads(audit_run.selected_checks_json)
    findings: list[dict] = []
    provider_config = (
        db.get(ProviderConfiguration, provider_config_id)
        if provider_config_id
        else None
    )
    brand_profile = _brand_profile(db, project.id)

    for check_name in selected_checks:
        severity = "low"
        summary = ""
        raw_output = ""
        metadata: dict = {"check": check_name}
        if check_name == "robots_ai_bots":
            code, stdout, stderr = run_script(
                "check-robots-ai-bots.py", ["--url", project.website_url]
            )
            raw_output = stdout or stderr
            severity = "medium" if code else "low"
            summary = "Reviewed robots access for AI and search bots."
        elif check_name == "sitemap":
            code, stdout, stderr = run_script(
                "sitemap-checker.py",
                ["--url", f"{project.website_url.rstrip('/')}/sitemap.xml"],
            )
            raw_output = stdout or stderr
            severity = "medium" if code else "low"
            summary = "Validated sitemap accessibility and URL count."
        elif check_name == "llms_txt":
            code, stdout, stderr = run_script(
                "check-llms-txt.py",
                ["--url", f"{project.website_url.rstrip('/')}/llms.txt"],
            )
            raw_output = stdout or stderr
            severity = "high" if code else "low"
            summary = "Validated llms.txt structure for public AI discovery."
        elif check_name == "content_freshness":
            path = _artifact_path(settings, audit_run.id, "freshness-preview", "md")
            code, stdout, stderr = run_script(
                "content_freshness_checker.py",
                [
                    "--sitemap-url",
                    f"{project.website_url.rstrip('/')}/sitemap.xml",
                    "--days-stale",
                    "180",
                    "--output-file",
                    str(path),
                ],
            )
            raw_output = (
                path.read_text(encoding="utf-8") if path.exists() else stdout or stderr
            )
            severity = "medium" if code else "low"
            summary = "Checked whether content signals look fresh or stale."
        elif check_name == "factual_consistency":
            score = 0
            if brand_profile and brand_profile.facts_markdown.strip():
                score += 1
            if brand_profile and brand_profile.approved_claims.strip():
                score += 1
            if brand_profile and brand_profile.numeric_facts_json not in {"[]", ""}:
                score += 1
            severity = "low" if score >= 2 else "high"
            raw_output = (
                "Canonical truth set coverage:\n"
                f"- Facts present: {'yes' if brand_profile and brand_profile.facts_markdown.strip() else 'no'}\n"
                f"- Approved claims present: {'yes' if brand_profile and brand_profile.approved_claims.strip() else 'no'}\n"
                f"- Numeric facts present: {'yes' if brand_profile and brand_profile.numeric_facts_json not in {'[]', ''} else 'no'}\n"
            )
            summary = (
                "Reviewed the project truth center and factual consistency readiness."
            )
        elif check_name == "hallucination_framework":
            facts_text = (
                brand_profile.facts_markdown
                if brand_profile
                else "# Brand facts\nReview manually."
            )
            questions_text = (
                "# Questions\n"
                f"- What does {project.name} do?\n"
                f"- What markets and languages does {project.name} support?\n"
                f"- What should users trust most about {project.name}?\n"
            )
            with NamedTemporaryFile(
                "w", suffix=".md", encoding="utf-8", delete=False
            ) as facts_file:
                facts_file.write(facts_text)
                facts_path = facts_file.name
            with NamedTemporaryFile(
                "w", suffix=".md", encoding="utf-8", delete=False
            ) as questions_file:
                questions_file.write(questions_text)
                questions_path = questions_file.name
            path = _artifact_path(settings, audit_run.id, "hallucination-report", "md")
            code, stdout, stderr = run_script(
                "check_hallucinations.py",
                [
                    "--brand-facts-file",
                    facts_path,
                    "--questions-file",
                    questions_path,
                    "--output-file",
                    str(path),
                    "--format",
                    "markdown",
                ],
            )
            provider_prompt = f"Summarize hallucination risk for {project.name} using the truth center."
            provider_output, provider_meta = _provider_note(
                provider_config, provider_prompt, settings
            )
            raw_output = (
                path.read_text(encoding="utf-8") if path.exists() else stdout or stderr
            ) + f"\n\nProvider note:\n{provider_output}\n"
            metadata.update(provider_meta)
            severity = "medium" if code else "low"
            summary = "Generated a starter hallucination review pack."
        elif check_name == "ai_sov_starter":
            code, stdout, stderr = run_script(
                "ai-share-of-voice-tracker.py",
                [
                    project.name,
                    "--queries",
                    "best geo agency,ai visibility audit",
                    "--format",
                    "markdown",
                ],
            )
            provider_output, provider_meta = _provider_note(
                provider_config,
                f"Comment on AI share-of-voice starter queries for {project.name}.",
                settings,
            )
            raw_output = f"{stdout or stderr}\n\nProvider note:\n{provider_output}\n"
            metadata.update(provider_meta)
            severity = "medium" if code else "low"
            summary = "Prepared an AI Share of Voice starter workflow."
        elif check_name == "local_yandex_readiness":
            severity = (
                "low"
                if "ru" in project.language.lower() or "ru" in project.market.lower()
                else "medium"
            )
            raw_output = (
                f"Project market: {project.market}\n"
                f"Project language: {project.language}\n"
                "Review Yandex Webmaster, Metrica, commercial factors, and regional proof.\n"
            )
            summary = "Prepared a local/Yandex readiness review."
        elif check_name == "entity_hierarchy_review":
            related = brand_profile.markets_json if brand_profile else "[]"
            severity = "low" if brand_profile else "medium"
            raw_output = (
                f"Project type: {project.project_type}\n"
                f"Audit preset: {project.audit_preset}\n"
                f"Brand profile linked: {'yes' if brand_profile else 'no'}\n"
                f"Related entity payload: {related}\n"
            )
            summary = "Reviewed entity hierarchy and brand focus signals."
        else:
            raw_output = f"Unknown check: {check_name}"
            severity = "medium"
            summary = "Unsupported check requested."

        _persist_artifact(
            db,
            audit_run=audit_run,
            project=project,
            settings=settings,
            artifact_type=check_name,
            content=raw_output,
            fmt="markdown",
            metadata=metadata,
        )
        findings.append(
            {
                "title": check_name.replace("_", " ").title(),
                "category": check_name,
                "severity": severity,
                "summary": summary,
                "recommendation": f"Review the {check_name} artifact and prioritize fixes in the next release batch.",
            }
        )

    penalties = {"critical": 30, "high": 15, "medium": 7, "low": 3}
    score = max(0, 100 - sum(penalties[item["severity"]] for item in findings))
    report_markdown = build_markdown_report(
        audit_run.report_language, project.name, findings, score
    )
    report_json = build_json_report(project.name, findings, score)
    _persist_artifact(
        db,
        audit_run=audit_run,
        project=project,
        settings=settings,
        artifact_type="report_markdown",
        content=report_markdown,
        fmt="markdown",
        metadata={"language": audit_run.report_language},
    )
    _persist_artifact(
        db,
        audit_run=audit_run,
        project=project,
        settings=settings,
        artifact_type="report_json",
        content=dumps_json(report_json),
        fmt="json",
        metadata={"language": audit_run.report_language},
    )
    report = Report(
        audit_run_id=audit_run.id,
        project_id=project.id,
        language=audit_run.report_language,
        format="markdown",
        summary_markdown=report_markdown,
        summary_json=dumps_json(report_json),
    )
    audit_run.status = "completed"
    audit_run.summary_score = score
    audit_run.finding_groups_json = json.dumps(findings, ensure_ascii=False)
    audit_run.completed_at = datetime.utcnow()
    db.add(report)
    REPORT_GENERATIONS.labels(language=audit_run.report_language).inc()
    db.commit()


def execute_audit_run_by_id(
    settings: Settings, audit_run_id: int, provider_config_id: Optional[int] = None
) -> None:
    db = create_session()
    try:
        audit_run = db.get(AuditRun, audit_run_id)
        if not audit_run:
            return
        execute_audit_run(db, audit_run, settings, provider_config_id)
    finally:
        db.close()
