from __future__ import annotations

import json
import os
from datetime import datetime
from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access, require_workspace_access
from ..config import load_settings
from ..database import get_db
from ..deps import get_current_user
from ..metrics import (
    PROVIDER_CALLS,
    PROVIDER_FAILURES,
    PROVIDER_LATENCY_SECONDS,
    SOV_RUNS,
)
from ..models import Project, ProviderConfiguration, SovRun, User
from ..providers.base import ProviderError
from ..providers.registry import build_provider
from ..schemas import SovCheckRequest, SovRunRead
from ..services.logging import log_event
from ..services.scoring import ai_citation_score

router = APIRouter(prefix="/sov", tags=["sov"])


def _estimate_share(results: list[dict]) -> float:
    if not results:
        return 0.0
    mentioned = sum(1 for row in results if row.get("mentioned"))
    return round(mentioned / len(results), 2)


def _serialize(row: SovRun) -> SovRunRead:
    return SovRunRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        brand=row.brand,
        queries=json.loads(row.queries_json or "[]"),
        providers=json.loads(row.providers_json or "[]"),
        results=json.loads(row.results_json or "[]"),
        mention_summary=row.mention_summary,
        share_estimate=row.share_estimate,
        notes=row.notes,
        status=row.status,
        report_language=row.report_language,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


def _configured_provider_map(
    db: Session, workspace_id: int, provider_names: list[str]
) -> dict[str, ProviderConfiguration]:
    rows = (
        db.query(ProviderConfiguration)
        .filter(ProviderConfiguration.workspace_id == workspace_id)
        .filter(ProviderConfiguration.is_enabled.is_(True))
        .all()
    )
    wanted = {name.lower() for name in provider_names}
    return {
        row.provider_name.lower(): row
        for row in rows
        if row.provider_name.lower() in wanted
    }


def _provider_based_result(
    provider_config: ProviderConfiguration,
    query: str,
    brand: str,
    settings,
) -> dict:
    env_var = (
        provider_config.api_key_env_var
        or f"{provider_config.provider_name.upper()}_API_KEY"
    )
    api_key = getattr(
        settings, f"{provider_config.provider_name.lower()}_api_key", ""
    ) or os.getenv(env_var, "")
    prompt = (
        "Evaluate AI discoverability for one brand and one query.\n"
        f"Brand: {brand}\n"
        f"Query: {query}\n"
        "Return strict JSON with keys: mentioned (true/false), citation_count "
        "(0-3 integer), answer_quality (short string), notes (short string)."
    )
    started_at = perf_counter()
    try:
        provider = build_provider(
            provider_config.provider_name,
            api_key=api_key,
            model=provider_config.model,
            base_url=provider_config.base_url,
        )
        response = provider.generate_text(
            prompt,
            system_prompt="You are a strict JSON-only discoverability evaluator.",
        )
        duration = perf_counter() - started_at
        PROVIDER_CALLS.labels(
            provider=provider_config.provider_name, status=response.status
        ).inc()
        PROVIDER_LATENCY_SECONDS.labels(provider=provider_config.provider_name).observe(
            duration
        )
        try:
            parsed = json.loads(response.content)
            mentioned = bool(parsed.get("mentioned"))
            citation_count = max(0, min(3, int(parsed.get("citation_count", 0))))
            answer_quality = parsed.get("answer_quality", "unknown")
            notes = parsed.get("notes", "Provider-based AI SoV response.")
        except Exception:
            lowered = response.content.lower()
            mentioned = brand.lower() in lowered
            citation_count = min(
                3,
                sum(lowered.count(token) for token in ("http", "source", "citation")),
            )
            answer_quality = "unstructured"
            notes = "Provider responded outside the strict JSON contract; fallback parsing applied."
        log_event(
            "sov.provider_result",
            provider=provider_config.provider_name,
            model=provider_config.model,
            query=query,
            latency_seconds=round(duration, 3),
            mentioned=mentioned,
            citation_count=citation_count,
        )
        return {
            "query": query,
            "provider": provider_config.provider_name,
            "brand": brand,
            "mentioned": mentioned,
            "citation_count": citation_count,
            "answer_quality": answer_quality,
            "notes": notes,
            "execution_mode": "provider",
            "latency_seconds": round(duration, 3),
        }
    except ProviderError as exc:
        duration = perf_counter() - started_at
        PROVIDER_CALLS.labels(
            provider=provider_config.provider_name, status="error"
        ).inc()
        PROVIDER_FAILURES.labels(provider=provider_config.provider_name).inc()
        PROVIDER_LATENCY_SECONDS.labels(provider=provider_config.provider_name).observe(
            duration
        )
        log_event(
            "sov.provider_failure",
            provider=provider_config.provider_name,
            model=provider_config.model,
            query=query,
            error=str(exc),
            latency_seconds=round(duration, 3),
        )
        return {
            "query": query,
            "provider": provider_config.provider_name,
            "brand": brand,
            "mentioned": False,
            "citation_count": 0,
            "answer_quality": "error",
            "notes": f"Provider-backed SoV failed: {exc}",
            "execution_mode": "fallback_after_error",
            "latency_seconds": round(duration, 3),
        }


def _heuristic_result(query: str, provider: str, brand: str) -> dict:
    mentioned = provider.lower() in {"perplexity", "gemini"}
    return {
        "query": query,
        "provider": provider,
        "brand": brand,
        "mentioned": mentioned,
        "citation_count": 1 if mentioned and provider.lower() == "perplexity" else 0,
        "answer_quality": "heuristic",
        "notes": "Transparent heuristic starter. Manual review still required.",
        "execution_mode": "heuristic",
    }


@router.post("/check", response_model=SovRunRead)
def sov_check(
    payload: SovCheckRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SovRunRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    providers = payload.providers or ["openai", "anthropic", "gemini", "perplexity"]
    provider_map = _configured_provider_map(db, payload.workspace_id, providers)
    settings = getattr(request.app.state, "settings", load_settings())
    results = []
    for query in payload.queries:
        for provider_name in providers:
            provider_config = provider_map.get(provider_name.lower())
            if provider_config:
                results.append(
                    _provider_based_result(
                        provider_config, query, payload.brand, settings
                    )
                )
            else:
                results.append(_heuristic_result(query, provider_name, payload.brand))
    citation_score = ai_citation_score(results)
    mention_summary = (
        f"{payload.brand} evaluated across {len(payload.queries)} queries and "
        f"{len(providers)} providers for project {project.name}. "
        f"AI Citation Score: {citation_score}."
    )
    row = SovRun(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        user_id=current_user.id,
        brand=payload.brand,
        queries_json=json.dumps(payload.queries, ensure_ascii=False),
        providers_json=json.dumps(providers, ensure_ascii=False),
        results_json=json.dumps(results, ensure_ascii=False),
        mention_summary=mention_summary,
        share_estimate=_estimate_share(results),
        notes=payload.notes
        or (
            "Provider-backed where configuration exists; heuristic fallback otherwise. "
            "AI answer surfaces remain volatile and must be manually reviewed."
        ),
        status="completed",
        report_language=payload.language or project.language,
        completed_at=datetime.utcnow(),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "sov.completed",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        metadata={
            "brand": payload.brand,
            "queries": payload.queries,
            "providers": providers,
            "ai_citation_score": citation_score,
        },
    )
    db.commit()
    db.refresh(row)
    SOV_RUNS.labels(status=row.status).inc()
    return _serialize(row)


@router.get("/history", response_model=list[SovRunRead])
def list_sov_runs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SovRunRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(SovRun)
        .filter(SovRun.project_id == project_id)
        .order_by(SovRun.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.get("/{sov_run_id}", response_model=SovRunRead)
def get_sov_run(
    sov_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SovRunRead:
    row = db.get(SovRun, sov_run_id)
    project = db.get(Project, row.project_id) if row else None
    if not row or not project:
        raise HTTPException(status_code=404, detail="SOV run not found.")
    require_project_access(db, project.id, current_user, minimum_role="viewer")
    return _serialize(row)
