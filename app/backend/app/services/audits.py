from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import perf_counter
from typing import Optional

from sqlalchemy.orm import Session

from ..access import record_audit_log
from ..config import Settings
from ..database import create_session
from ..metrics import (
    AUDIT_DURATION_SECONDS,
    BACKGROUND_JOB_RETRIES,
    PROVIDER_CALLS,
    PROVIDER_FAILURES,
    PROVIDER_LATENCY_SECONDS,
    REPORT_GENERATIONS,
)
from ..models import (
    Artifact,
    AuditRun,
    BrandFactsProfile,
    Project,
    ProviderConfiguration,
    Report,
    SovRun,
)
from ..providers.base import ProviderError
from ..providers.registry import build_provider
from .logging import log_event
from .reporting import build_json_report, build_markdown_report, dumps_json
from .retries import RetryPolicy, run_with_retry
from .scoring import (
    ai_citation_score,
    benchmark_status,
    finding_priority,
    overall_score,
)
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


def _latest_sov_score(db: Session, project_id: int) -> float | None:
    row = (
        db.query(SovRun)
        .filter(SovRun.project_id == project_id)
        .order_by(SovRun.id.desc())
        .first()
    )
    if not row:
        return None
    return ai_citation_score(json.loads(row.results_json or "[]"))


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
    started_at = perf_counter()
    try:
        outcome = run_with_retry(
            f"provider_{provider.provider_name}",
            lambda: build_provider(
                provider.provider_name,
                api_key=api_key,
                model=provider.model,
                base_url=provider.base_url,
            ).generate_text(
                prompt, system_prompt="You are a discoverability audit assistant."
            ),
            RetryPolicy(max_attempts=3, initial_delay_seconds=0.5),
        )
        response = outcome.result
        if response is None:
            raise ProviderError(outcome.error or "Provider call failed.")
        duration = perf_counter() - started_at
        PROVIDER_CALLS.labels(
            provider=provider.provider_name, status=response.status
        ).inc()
        PROVIDER_LATENCY_SECONDS.labels(provider=provider.provider_name).observe(
            duration
        )
        log_event(
            "provider.call",
            provider=provider.provider_name,
            model=provider.model,
            status=response.status,
            latency_seconds=round(duration, 3),
            retry_status=outcome.status,
            attempts=len(outcome.attempts),
        )
        return response.content, {
            "status": response.status,
            "provider": response.provider,
            "model": response.model,
            "latency_seconds": round(duration, 3),
            "retry_status": outcome.status,
            "attempts": len(outcome.attempts),
        }
    except ProviderError as exc:
        duration = perf_counter() - started_at
        PROVIDER_CALLS.labels(provider=provider.provider_name, status="error").inc()
        PROVIDER_FAILURES.labels(provider=provider.provider_name).inc()
        PROVIDER_LATENCY_SECONDS.labels(provider=provider.provider_name).observe(
            duration
        )
        log_event(
            "provider.failure",
            provider=provider.provider_name,
            model=provider.model,
            error=str(exc),
            latency_seconds=round(duration, 3),
        )
        return f"Provider commentary unavailable: {exc}", {
            "status": "error",
            "error": str(exc),
            "latency_seconds": round(duration, 3),
        }


def _finding(
    *,
    check_name: str,
    severity: str,
    summary: str,
    recommendation: str,
    benchmark_metric_key: str | None,
    benchmark_value: float | None,
    impact: int,
    effort: int,
    confidence: int,
    notes: str = "",
) -> dict:
    benchmark = (
        benchmark_status(benchmark_metric_key, benchmark_value)
        if benchmark_metric_key
        else "insufficient_data"
    )
    priority_score, priority_label = finding_priority(
        severity=severity,
        impact=impact,
        effort=effort,
        confidence=confidence,
        benchmark=benchmark,
    )
    return {
        "title": check_name.replace("_", " ").title(),
        "category": check_name,
        "severity": severity,
        "summary": summary,
        "recommendation": recommendation,
        "impact": impact,
        "effort": effort,
        "confidence": confidence,
        "priority_score": priority_score,
        "priority_label": priority_label,
        "benchmark_status": benchmark,
        "benchmark_metric_key": benchmark_metric_key,
        "benchmark_value": benchmark_value,
        "notes": notes,
    }


def _benchmark_summary(
    findings: list[dict], ai_citation_score_value: float | None
) -> dict:
    summary: dict[str, str | float] = {}
    metric_keys = {
        item["benchmark_metric_key"]
        for item in findings
        if item.get("benchmark_metric_key")
    }
    for metric_key in sorted(metric_keys):
        values = [
            item.get("benchmark_value")
            for item in findings
            if item.get("benchmark_metric_key") == metric_key
            and item.get("benchmark_value") is not None
        ]
        avg_value = round(sum(values) / len(values), 3) if values else None
        summary[metric_key] = benchmark_status(metric_key, avg_value)
    summary["ai_citation_score"] = (
        ai_citation_score_value if ai_citation_score_value is not None else "n/a"
    )
    return summary


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
    audit_run.status = "running"
    audit_started = perf_counter()
    record_audit_log(
        db,
        "audit.started",
        user_id=audit_run.user_id,
        workspace_id=audit_run.workspace_id,
        project_id=audit_run.project_id,
        metadata={"mode": audit_run.mode},
    )
    db.commit()
    selected_checks = json.loads(audit_run.selected_checks_json)
    findings: list[dict] = []
    provider_config = (
        db.get(ProviderConfiguration, provider_config_id)
        if provider_config_id
        else None
    )
    brand_profile = _brand_profile(db, project.id)

    try:
        for check_name in selected_checks:
            severity = "low"
            summary = ""
            raw_output = ""
            recommendation = (
                f"Review the {check_name} artifact and prioritize fixes in the next "
                "release batch."
            )
            metadata: dict = {"check": check_name}
            benchmark_metric_key: str | None = None
            benchmark_value: float | None = None
            impact = 3
            effort = 2
            confidence = 3
            notes = ""

            if check_name == "robots_ai_bots":
                code, stdout, stderr = run_script(
                    "check-robots-ai-bots.py", ["--url", project.website_url]
                )
                raw_output = stdout or stderr
                severity = "medium" if code else "low"
                summary = "Reviewed robots access for AI and search bots."
                recommendation = (
                    "Open critical AI/search bots to the intended public surfaces and "
                    "re-check robots rules."
                )
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.4 if code else 0.8
                impact = 4
                effort = 2
                confidence = 4
            elif check_name == "sitemap":
                code, stdout, stderr = run_script(
                    "sitemap-checker.py",
                    ["--url", f"{project.website_url.rstrip('/')}/sitemap.xml"],
                )
                raw_output = stdout or stderr
                severity = "medium" if code else "low"
                summary = "Validated sitemap accessibility and URL count."
                recommendation = "Keep sitemap reachable, current, and aligned with the canonical URL set."
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.45 if code else 0.78
                impact = 4
                effort = 2
                confidence = 4
            elif check_name == "llms_txt":
                code, stdout, stderr = run_script(
                    "check-llms-txt.py",
                    ["--url", f"{project.website_url.rstrip('/')}/llms.txt"],
                )
                raw_output = stdout or stderr
                severity = "high" if code else "low"
                summary = "Validated llms.txt structure for public AI discovery."
                recommendation = "Publish or fix llms.txt so AI systems can map key pages and entity signals."
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.35 if code else 0.88
                impact = 5
                effort = 2
                confidence = 5
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
                    path.read_text(encoding="utf-8")
                    if path.exists()
                    else stdout or stderr
                )
                severity = "medium" if code else "low"
                summary = "Checked whether content signals look fresh or stale."
                recommendation = "Refresh stale high-intent URLs first and re-run the audit after publication."
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.5 if code else 0.7
                impact = 3
                effort = 3
                confidence = 3
            elif check_name == "factual_consistency":
                ratio = 0.0
                if brand_profile and brand_profile.facts_markdown.strip():
                    ratio += 0.34
                if brand_profile and brand_profile.approved_claims.strip():
                    ratio += 0.33
                if brand_profile and brand_profile.numeric_facts_json not in {"[]", ""}:
                    ratio += 0.33
                severity = "low" if ratio >= 0.67 else "high"
                raw_output = (
                    "Canonical truth set coverage:\n"
                    f"- Facts present: {'yes' if brand_profile and brand_profile.facts_markdown.strip() else 'no'}\n"
                    f"- Approved claims present: {'yes' if brand_profile and brand_profile.approved_claims.strip() else 'no'}\n"
                    f"- Numeric facts present: {'yes' if brand_profile and brand_profile.numeric_facts_json not in {'[]', ''} else 'no'}\n"
                )
                summary = "Reviewed the project truth center and factual consistency readiness."
                recommendation = "Expand the truth center until key claims, numbers, and boundaries are explicit."
                benchmark_metric_key = "factual_consistency"
                benchmark_value = round(ratio, 2)
                impact = 5
                effort = 2
                confidence = 5
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
                path = _artifact_path(
                    settings, audit_run.id, "hallucination-report", "md"
                )
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
                    path.read_text(encoding="utf-8")
                    if path.exists()
                    else stdout or stderr
                ) + f"\n\nProvider note:\n{provider_output}\n"
                metadata.update(provider_meta)
                severity = "medium" if code else "low"
                summary = "Generated a starter hallucination review pack."
                recommendation = "Use the truth center to close repeated hallucination patterns before scaling content."
                benchmark_metric_key = "factual_consistency"
                benchmark_value = 0.45 if code else 0.72
                impact = 4
                effort = 3
                confidence = 4
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
                    (
                        "Return a concise assessment of whether the brand is likely to be "
                        f"mentioned for discovery queries related to {project.name}. "
                        "Include answer surfaces, likely citations, and factual gaps."
                    ),
                    settings,
                )
                raw_output = (
                    f"{stdout or stderr}\n\nProvider note:\n{provider_output}\n"
                )
                metadata.update(provider_meta)
                severity = "medium" if code else "low"
                summary = "Prepared an AI Share of Voice starter workflow."
                recommendation = "Run provider-backed AI SoV monthly and compare citation presence across surfaces."
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.5 if code else 0.74
                impact = 4
                effort = 2
                confidence = 3
            elif check_name == "local_yandex_readiness":
                severity = (
                    "low"
                    if "ru" in project.language.lower()
                    or "ru" in project.market.lower()
                    else "medium"
                )
                raw_output = (
                    f"Project market: {project.market}\n"
                    f"Project language: {project.language}\n"
                    "Review Yandex Webmaster, Metrica, commercial factors, and regional proof.\n"
                )
                summary = "Prepared a local/Yandex readiness review."
                recommendation = "Align Yandex regional proof, commercial factors, and RU entity signals."
                benchmark_metric_key = "ai_visibility_readiness"
                benchmark_value = 0.7 if severity == "low" else 0.45
                impact = 3
                effort = 3
                confidence = 4
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
                recommendation = "Keep one explicit primary entity, map sibling entities, and reduce ambiguity."
                benchmark_metric_key = "factual_consistency"
                benchmark_value = 0.7 if brand_profile else 0.42
                impact = 4
                effort = 2
                confidence = 4
            else:
                raw_output = f"Unknown check: {check_name}"
                severity = "medium"
                summary = "Unsupported check requested."
                notes = "The check is not yet implemented in the current audit runner."

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
                _finding(
                    check_name=check_name,
                    severity=severity,
                    summary=summary,
                    recommendation=recommendation,
                    benchmark_metric_key=benchmark_metric_key,
                    benchmark_value=benchmark_value,
                    impact=impact,
                    effort=effort,
                    confidence=confidence,
                    notes=notes,
                )
            )
    except Exception as exc:
        audit_run.status = "failed"
        audit_run.completed_at = datetime.utcnow()
        record_audit_log(
            db,
            "audit.failed",
            user_id=audit_run.user_id,
            workspace_id=audit_run.workspace_id,
            project_id=audit_run.project_id,
            metadata={"error": str(exc)},
        )
        db.commit()
        raise

    ai_citation_score_value = _latest_sov_score(db, project.id)
    score = overall_score(findings)
    benchmark_summary = _benchmark_summary(findings, ai_citation_score_value)
    report_markdown = build_markdown_report(
        audit_run.report_language,
        project.name,
        findings,
        score,
        benchmark_summary,
        ai_citation_score_value,
    )
    report_json = build_json_report(
        project.name, findings, score, benchmark_summary, ai_citation_score_value
    )
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
    AUDIT_DURATION_SECONDS.labels(mode=audit_run.mode, status="completed").observe(
        perf_counter() - audit_started
    )
    record_audit_log(
        db,
        "audit.completed",
        user_id=audit_run.user_id,
        workspace_id=audit_run.workspace_id,
        project_id=audit_run.project_id,
        metadata={
            "summary_score": score,
            "ai_citation_score": ai_citation_score_value,
            "finding_count": len(findings),
        },
    )
    log_event(
        "audit.completed",
        audit_run_id=audit_run.id,
        workspace_id=audit_run.workspace_id,
        project_id=audit_run.project_id,
        score=score,
        ai_citation_score=ai_citation_score_value,
        findings=len(findings),
    )
    db.commit()


def execute_audit_run_by_id(
    settings: Settings, audit_run_id: int, provider_config_id: Optional[int] = None
) -> None:
    attempts = 0
    last_error: Exception | None = None
    while attempts < 2:
        attempts += 1
        db = create_session()
        try:
            audit_run = db.get(AuditRun, audit_run_id)
            if not audit_run:
                return
            execute_audit_run(db, audit_run, settings, provider_config_id)
            if attempts > 1:
                BACKGROUND_JOB_RETRIES.labels(
                    job_type="audit_run", status="recovered"
                ).inc()
            return
        except Exception as exc:  # pragma: no cover - retry guard
            last_error = exc
            BACKGROUND_JOB_RETRIES.labels(job_type="audit_run", status="retry").inc()
            audit_run = db.get(AuditRun, audit_run_id)
            if audit_run:
                audit_run.status = "failed"
                audit_run.completed_at = datetime.utcnow()
                AUDIT_DURATION_SECONDS.labels(
                    mode=audit_run.mode, status="failed"
                ).observe(0)
                db.commit()
        finally:
            db.close()
    if last_error is not None:
        raise last_error
