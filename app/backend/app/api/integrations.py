from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import (
    CmsConnector,
    EvidenceRecord,
    IntegrationConnection,
    IntegrationSyncEvent,
    ProjectResearchContext,
    User,
)
from ..schemas import (
    IntegrationConnectionCreate,
    IntegrationConnectionRead,
    IntegrationContractsResponse,
    IntegrationDetailRead,
    IntegrationRuntimePolicyUpdate,
    IntegrationSourceContractRead,
    IntegrationSyncEventRead,
    IntegrationVerificationMatrixRead,
    IntegrationVerificationRowRead,
)
from ..services.cms import cms_contract
from ..services.integrations import (
    all_integration_contracts,
    build_integration_verification_row,
    compact_integration_summary,
    DATAFORSEO_SOURCES,
    integration_capability_matrix,
    integration_contract,
    integration_env_status,
    integration_runtime_profile,
    integration_sync_diagnostics,
    sync_integration_source,
)

router = APIRouter(prefix="/integrations", tags=["integrations"])


def _serialize(row: IntegrationConnection) -> IntegrationConnectionRead:
    contract = integration_contract(row.source_type)
    env_status = integration_env_status(contract)
    freshness = "never_synced"
    if row.last_sync_at:
        freshness = "fresh" if row.last_sync_status == "completed" else "stale"
    return IntegrationConnectionRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        source_type=row.source_type,
        label=row.label,
        property_identifier=row.property_identifier,
        credentials_env_var=row.credentials_env_var,
        config=json.loads(row.config_json or "{}"),
        latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
        last_sync_status=row.last_sync_status,
        last_sync_at=row.last_sync_at,
        readiness_tier=contract["readiness_tier"],
        sync_mode=contract["sync_mode"],
        required_env_vars=contract["required_env_vars"],
        credential_status="configured"
        if (
            env_status["live_credentials_ready"]
            if env_status["required_env_vars"]
            else bool(row.credentials_env_var)
        )
        else "partial"
        if row.credentials_env_var
        else "missing",
        recommended_ci_workflow=contract["recommended_ci_workflow"],
        ci_gates=contract["ci_gates"],
        contract_version=contract["contract_version"],
        sync_capabilities=contract["capabilities"],
        production_flow=contract.get("production_flow", []),
        runtime_profile=integration_runtime_profile(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
        ),
        sync_freshness=freshness,
        next_step=contract["next_step"],
        created_at=row.created_at,
    )


def _serialize_sync_event(row: IntegrationSyncEvent) -> IntegrationSyncEventRead:
    metadata = json.loads(row.metadata_json or "{}")
    return IntegrationSyncEventRead(
        id=row.id,
        status=row.status,
        attempt_number=row.attempt_number,
        retry_count=row.retry_count,
        scope_status=row.scope_status,
        credential_status=row.credential_status,
        dataset_status=row.dataset_status,
        provenance_level=row.provenance_level,
        freshness_label=row.freshness_label,
        error_summary=row.error_summary,
        metadata=metadata,
        sync_policy=metadata.get("sync_policy", {}),
        diagnostics=metadata.get("diagnostics", {}),
        started_at=row.started_at,
        finished_at=row.finished_at,
    )


@router.get("/contracts", response_model=IntegrationContractsResponse)
def list_integration_contracts() -> IntegrationContractsResponse:
    return IntegrationContractsResponse(
        contracts=[
            IntegrationSourceContractRead(**contract)
            for contract in all_integration_contracts()
        ]
    )


@router.get("/capability-matrix")
def capability_matrix() -> dict:
    """Machine-readable public status of connector maturity and boundaries."""
    return integration_capability_matrix()


@router.get("/lifecycle")
def integration_lifecycle() -> dict:
    """Acceptance criteria, not a claim that every source is connected."""
    sources = ["gsc", "yandex_webmaster", "ga4", "yandex_metrica"]
    return {
        "levels": ["foundation", "prototype", "connected", "production_ready"],
        "production_ready_requires": [
            "operator-authorized credential configuration",
            "successful read-only API call",
            "refresh-token recovery where OAuth applies",
            "controlled failure and retry evidence",
            "disconnect or credential revocation procedure",
            "automated integration test with a provider-safe fixture",
        ],
        "sources": [
            {
                "source_type": source,
                "current_contract": integration_contract(source)["readiness_tier"],
                "current_level": "foundation",
                "boundary": "Do not claim production_ready without an operator-owned end-to-end proof record.",
            }
            for source in sources
        ],
    }


@router.get("", response_model=list[IntegrationConnectionRead])
def list_integrations(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[IntegrationConnectionRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.post("", response_model=IntegrationConnectionRead)
def create_integration(
    payload: IntegrationConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationConnectionRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    row = IntegrationConnection(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        source_type=payload.source_type,
        label=payload.label,
        property_identifier=payload.property_identifier,
        credentials_env_var=payload.credentials_env_var,
        config_json=json.dumps(payload.config, ensure_ascii=False),
        latest_snapshot_json="{}",
        last_sync_status="created",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    record_audit_log(
        db,
        "integration.created",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"source_type": row.source_type, "label": row.label},
    )
    db.commit()
    return _serialize(row)


@router.delete("/{integration_id}")
def disconnect_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    record_audit_log(
        db,
        "integration.disconnected",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"integration_id": row.id, "source_type": row.source_type},
    )
    # Credentials are never persisted by this app. Operators must revoke or
    # remove the referenced environment secret separately.
    db.delete(row)
    db.commit()
    return {
        "status": "disconnected",
        "integration_id": integration_id,
        "operator_action": "Revoke the provider grant and remove the referenced environment secret if it is no longer needed.",
    }


@router.patch(
    "/{integration_id}/runtime-policy", response_model=IntegrationConnectionRead
)
def update_integration_runtime_policy(
    integration_id: int,
    payload: IntegrationRuntimePolicyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationConnectionRead:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    config = json.loads(row.config_json or "{}")
    updates = payload.model_dump(exclude_unset=True)
    config.update(updates)
    row.config_json = json.dumps(config, ensure_ascii=False)
    db.add(row)
    record_audit_log(
        db,
        "integration.runtime_policy_updated",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"integration_id": row.id, "updated_fields": sorted(updates.keys())},
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.post("/{integration_id}/sync", response_model=IntegrationConnectionRead)
def sync_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationConnectionRead:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    if row.source_type in DATAFORSEO_SOURCES:
        row = (
            db.query(IntegrationConnection)
            .filter(IntegrationConnection.id == integration_id)
            .with_for_update()
            .populate_existing()
            .first()
        )
        if not row:
            raise HTTPException(status_code=404, detail="Integration not found.")
    contract = integration_contract(row.source_type)
    config = json.loads(row.config_json or "{}")
    context_row = (
        db.query(ProjectResearchContext)
        .filter(ProjectResearchContext.project_id == row.project_id)
        .first()
    )
    project = row.project
    project_context = context_row.model_values() if context_row else {}
    provider_spend = 0.0
    provider_calls = 0
    provider_charge_uncertain = False
    cached_snapshot: dict | None = None
    now_utc = datetime.now(timezone.utc)
    if row.source_type in DATAFORSEO_SOURCES:
        try:
            parsed_snapshot = json.loads(row.latest_snapshot_json or "{}")
            existing_snapshot = parsed_snapshot if isinstance(parsed_snapshot, dict) else {}
        except json.JSONDecodeError:
            existing_snapshot = {}
        observed_raw = existing_snapshot.get("observed_at")
        try:
            observed_at = datetime.fromisoformat(str(observed_raw).replace("Z", "+00:00"))
            ttl_seconds = min(max(int(config.get("cache_ttl_seconds", 21600)), 60), 86400)
            if (
                existing_snapshot.get("provider") == "dataforseo"
                and now_utc - observed_at < timedelta(seconds=ttl_seconds)
            ):
                cached_snapshot = existing_snapshot
        except (TypeError, ValueError):
            pass
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        events = (
            db.query(IntegrationSyncEvent)
            .filter(
                IntegrationSyncEvent.integration_connection_id == row.id,
                IntegrationSyncEvent.started_at >= today,
            )
            .all()
        )
        for previous_event in events:
            try:
                metadata = json.loads(previous_event.metadata_json or "{}")
            except json.JSONDecodeError:
                continue
            if metadata.get("provider") == "dataforseo":
                try:
                    provider_calls += max(0, int(metadata.get("provider_call_count", 0)))
                except (TypeError, ValueError):
                    provider_charge_uncertain = True
                try:
                    event_cost = float(metadata.get("cost_usd") or 0.0)
                    if not math.isfinite(event_cost) or event_cost < 0:
                        raise ValueError("invalid cost")
                    provider_spend += event_cost
                except (TypeError, ValueError):
                    provider_charge_uncertain = True
                provider_charge_uncertain = provider_charge_uncertain or bool(
                    metadata.get("cost_unknown") or previous_event.status == "running"
                )
        if provider_charge_uncertain and cached_snapshot is None:
            raise HTTPException(
                status_code=424,
                detail="A previous DataForSEO request has unknown billing outcome. Check the provider account before retrying today.",
            )
    env_status = integration_env_status(contract)
    credentials_ready = (
        env_status["live_credentials_ready"]
        if row.source_type in DATAFORSEO_SOURCES
        else bool(row.credentials_env_var or env_status["live_credentials_ready"])
    )
    event = IntegrationSyncEvent(
        integration_connection_id=row.id,
        status="running",
        attempt_number=1,
        retry_count=0,
        scope_status="starter_scope",
        credential_status="configured" if credentials_ready else "missing",
        dataset_status="sync_started",
        provenance_level="starter_sync",
        freshness_label="sync_in_progress",
        metadata_json=json.dumps(
            {
                "source_type": row.source_type,
                **(
                    {
                        "provider": "dataforseo",
                        "flow": row.source_type,
                        "provider_call_count": int(cached_snapshot is None),
                        "request_reserved": cached_snapshot is None,
                        "cost_usd": 0.0,
                    }
                    if row.source_type in DATAFORSEO_SOURCES
                    else {}
                ),
                "sync_policy": integration_runtime_profile(
                    row.source_type,
                    config=config,
                    credentials_env_var=row.credentials_env_var,
                ),
            },
            ensure_ascii=False,
        ),
    )
    db.add(event)
    db.flush()
    if row.source_type in DATAFORSEO_SOURCES and cached_snapshot is None:
        # Persist intent before the paid HTTP call. If the worker dies afterward,
        # the running event prevents an automatic duplicate charge.
        db.commit()
        db.refresh(event)
    try:
        if cached_snapshot is not None:
            snapshot = dict(cached_snapshot)
            snapshot["cache_hit"] = True
            snapshot["cache_age_seconds"] = max(
                0, int((now_utc - observed_at).total_seconds())
            )
        else:
            snapshot = sync_integration_source(
                row.source_type,
                property_identifier=row.property_identifier,
                config=config,
                project_context=project_context,
                project_market=project.market,
                project_language=project.language,
                spent_today_usd=provider_spend,
                requests_today=provider_calls,
            )
        snapshot["summary"] = compact_integration_summary(snapshot)
        row.latest_snapshot_json = json.dumps(snapshot, ensure_ascii=False)
        row.last_sync_status = "completed"
        row.last_sync_at = datetime.utcnow()
        event.status = "completed"
        event.scope_status = "verified_contract_scope"
        event.credential_status = "configured" if credentials_ready else "missing_but_starter_allowed"
        event.dataset_status = "available"
        event.provenance_level = (
            "managed_runtime"
            if contract["readiness_tier"] == "managed_runtime"
            else "live_runtime"
            if "live" in str(snapshot.get("source", "")).lower()
            else "starter_sync"
        )
        event.freshness_label = "fresh"
        event.finished_at = datetime.utcnow()
        provider_cost = float(snapshot.get("cost_usd") or 0.0)
        cache_hit = bool(snapshot.get("cache_hit"))
        if snapshot.get("provider") == "dataforseo" and not cache_hit:
            evidence_summary = json.dumps(
                {
                    "provider": "dataforseo",
                    "flow": row.source_type,
                    "market": snapshot.get("market"),
                    "language": snapshot.get("language"),
                    "observed_at": snapshot.get("observed_at"),
                    "cost_usd": provider_cost,
                    "cache_ttl_seconds": snapshot.get("cache_ttl_seconds"),
                    "findings": snapshot.get("findings", []),
                    "rows": snapshot.get("rows", [])[:30],
                },
                ensure_ascii=False,
            )
            db.add(
                EvidenceRecord(
                    workspace_id=row.workspace_id,
                    project_id=row.project_id,
                    label_type="internal_evidence",
                    title=f"DataForSEO {row.source_type} snapshot",
                    summary=evidence_summary,
                    source_ref=str(snapshot.get("provider_task_id") or "DataForSEO API"),
                    links_json="[]",
                )
            )
        event.metadata_json = json.dumps(
            {
                "source_type": row.source_type,
                "provider": snapshot.get("provider"),
                "flow": snapshot.get("flow"),
                "cost_usd": 0.0 if cache_hit else provider_cost,
                "snapshot_cost_usd": provider_cost,
                "cache_hit": cache_hit,
                "provider_call_count": 0 if cache_hit else int(snapshot.get("provider") == "dataforseo"),
                "budget_overrun": snapshot.get("budget_overrun", False),
                "recommended_ci_workflow": contract["recommended_ci_workflow"],
                "sync_policy": integration_runtime_profile(
                    row.source_type,
                    config=config,
                    credentials_env_var=row.credentials_env_var,
                    latest_snapshot=snapshot,
                ),
                "diagnostics": integration_sync_diagnostics(
                    row.source_type,
                    config=json.loads(row.config_json or "{}"),
                    credentials_env_var=row.credentials_env_var,
                    latest_snapshot=snapshot,
                ),
            },
            ensure_ascii=False,
        )
    except Exception as exc:
        row.last_sync_status = "failed"
        event.status = "failed"
        event.retry_count = 0
        event.dataset_status = "unavailable"
        event.error_summary = str(exc)
        event.freshness_label = "stale"
        event.finished_at = datetime.utcnow()
        if row.source_type in DATAFORSEO_SOURCES:
            request_started = bool(
                getattr(exc, "request_started", cached_snapshot is None)
            )
            event.metadata_json = json.dumps(
                {
                    "provider": "dataforseo",
                    "flow": row.source_type,
                    "provider_call_count": int(request_started),
                    "cost_usd": 0.0,
                    "cost_unknown": request_started,
                    "cache_hit": False,
                    "request_started": request_started,
                    "error_kind": exc.__class__.__name__,
                },
                ensure_ascii=False,
            )
        db.add(row)
        db.add(event)
        db.commit()
        if row.source_type in DATAFORSEO_SOURCES:
            raise HTTPException(status_code=424, detail=str(exc)) from exc
        raise
    db.add(row)
    db.add(event)
    record_audit_log(
        db,
        "integration.synced",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"integration_id": row.id, "source_type": row.source_type},
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.get("/{integration_id}/detail", response_model=IntegrationDetailRead)
def integration_detail(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationDetailRead:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="viewer")
    contract = integration_contract(row.source_type)
    latest_snapshot = json.loads(row.latest_snapshot_json or "{}")
    events = (
        db.query(IntegrationSyncEvent)
        .filter(IntegrationSyncEvent.integration_connection_id == row.id)
        .order_by(IntegrationSyncEvent.id.desc())
        .all()
    )
    latest_event = events[0] if events else None
    return IntegrationDetailRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        source_type=row.source_type,
        label=row.label,
        connection_state=row.last_sync_status or "created",
        credential_status=latest_event.credential_status
        if latest_event
        else ("configured" if row.credentials_env_var else "missing"),
        scope_status=latest_event.scope_status if latest_event else "unknown",
        dataset_availability=latest_event.dataset_status
        if latest_event
        else "contract_only",
        freshness=latest_event.freshness_label if latest_event else "never_synced",
        readiness_tier=contract["readiness_tier"],
        runtime_level=latest_event.provenance_level
        if latest_event
        else "contract_only",
        last_successful_pull=row.last_sync_at,
        last_error=latest_event.error_summary if latest_event else None,
        recommended_next_steps=contract.get("production_flow", [])
        + [contract["next_step"]],
        runtime_profile=integration_runtime_profile(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=latest_snapshot,
        ),
        sync_diagnostics=integration_sync_diagnostics(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=latest_snapshot,
        ),
        sync_logs=[_serialize_sync_event(event) for event in events[:10]],
        latest_snapshot_summary=compact_integration_summary(latest_snapshot)
        if latest_snapshot
        else {},
    )


@router.get("/{integration_id}/readiness-plan")
def integration_readiness_plan(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="viewer")
    contract = integration_contract(row.source_type)
    env_status = integration_env_status(contract)
    return {
        "integration_id": row.id,
        "source_type": row.source_type,
        "contract_version": contract["contract_version"],
        "ci_first_class": True,
        "workflow": contract["recommended_ci_workflow"],
        "ci_gates": contract["ci_gates"],
        "production_flow": contract.get("production_flow", []),
        "current_status": row.last_sync_status or "created",
        "credential_status": "configured"
        if row.credentials_env_var or env_status["live_credentials_ready"]
        else "missing",
        "env_status": env_status,
        "next_step": contract["next_step"],
    }


@router.get("/health-center")
def integration_health_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    cms_rows = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project_id)
        .order_by(CmsConnector.id.desc())
        .all()
    )

    items: list[dict] = []
    healthy_count = 0
    degraded_count = 0

    for row in integration_rows:
        contract = integration_contract(row.source_type)
        latest_event = (
            db.query(IntegrationSyncEvent)
            .filter(IntegrationSyncEvent.integration_connection_id == row.id)
            .order_by(IntegrationSyncEvent.id.desc())
            .first()
        )
        connection_state = row.last_sync_status or "created"
        if connection_state == "completed":
            healthy_count += 1
        else:
            degraded_count += 1
        items.append(
            {
                "surface_type": "integration",
                "id": row.id,
                "label": row.label,
                "source_type": row.source_type,
                "readiness_tier": contract["readiness_tier"],
                "connection_state": connection_state,
                "credential_status": latest_event.credential_status
                if latest_event
                else ("configured" if row.credentials_env_var else "missing"),
                "freshness": latest_event.freshness_label
                if latest_event
                else "never_synced",
                "retry_count": latest_event.retry_count if latest_event else 0,
                "last_error": latest_event.error_summary if latest_event else None,
                "recommended_next_step": contract["next_step"],
                "runtime_profile": integration_runtime_profile(
                    row.source_type,
                    config=json.loads(row.config_json or "{}"),
                    credentials_env_var=row.credentials_env_var,
                    latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
                ),
                "sync_diagnostics": integration_sync_diagnostics(
                    row.source_type,
                    config=json.loads(row.config_json or "{}"),
                    credentials_env_var=row.credentials_env_var,
                    latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
                ),
                "diagnostics": contract.get("production_flow", []),
            }
        )

    for row in cms_rows:
        contract = cms_contract(row.cms_type)
        connection_state = row.last_sync_status or "created"
        if connection_state == "completed":
            healthy_count += 1
        else:
            degraded_count += 1
        items.append(
            {
                "surface_type": "cms",
                "id": row.id,
                "label": row.label,
                "source_type": row.cms_type,
                "readiness_tier": contract["readiness_tier"],
                "connection_state": connection_state,
                "credential_status": "configured" if row.auth_env_var else "missing",
                "freshness": "fresh" if connection_state == "completed" else "stale",
                "retry_count": 0,
                "last_error": None,
                "recommended_next_step": contract["next_step"],
                "diagnostics": contract.get("production_flow", []),
            }
        )

    return {
        "project_id": project_id,
        "summary": {
            "healthy_count": healthy_count,
            "degraded_count": degraded_count,
            "total_surfaces": len(items),
        },
        "items": items,
    }


@router.get("/runtime-center")
def integration_runtime_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    rows: list[dict] = []
    managed_ready = 0
    live_ready = 0
    ru_surfaces = 0
    seo_surfaces = 0
    auth_gaps = 0
    recovery_backlog: list[dict] = []
    owner_queue: list[dict] = []
    for row in integration_rows:
        snapshot = json.loads(row.latest_snapshot_json or "{}")
        runtime_profile = integration_runtime_profile(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=snapshot,
        )
        diagnostics = integration_sync_diagnostics(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=snapshot,
        )
        if runtime_profile["runtime_level"] == "managed_runtime":
            managed_ready += 1
        if runtime_profile["runtime_level"] in {"managed_runtime", "live_runtime"}:
            live_ready += 1
        if not runtime_profile["credential_ready"]:
            auth_gaps += 1
        if row.source_type.startswith("yandex") or row.source_type in {
            "alice_ai_visibility",
            "vk_ads",
            "vk_organic",
            "telegram_ads",
            "telegram_channels",
            "dzen",
            "rutube",
        }:
            ru_surfaces += 1
        if row.source_type in {
            "keyword_research",
            "competitor_intelligence",
            "backlink_intelligence",
            "rank_tracking",
        }:
            seo_surfaces += 1
        rows.append(
            {
                "id": row.id,
                "label": row.label,
                "source_type": row.source_type,
                "runtime_profile": runtime_profile,
                "diagnostics": diagnostics,
                "latest_snapshot_source": snapshot.get("source"),
                "recommended_ci_workflow": integration_contract(row.source_type)[
                    "recommended_ci_workflow"
                ],
            }
        )
        if diagnostics["checks"]["credentials"] == "missing":
            owner_queue.append(
                {
                    "source_type": row.source_type,
                    "label": row.label,
                    "owner": runtime_profile["runtime_owner"],
                    "action": "configure credentials and rerun first sync",
                    "priority": "high",
                }
            )
        elif diagnostics["checks"]["snapshot_mode"] == "starter_or_stub":
            owner_queue.append(
                {
                    "source_type": row.source_type,
                    "label": row.label,
                    "owner": runtime_profile["runtime_owner"],
                    "action": "replace starter snapshot with live feed or reviewed export",
                    "priority": "medium",
                }
            )
        if runtime_profile["failure_recovery_mode"] != "retry_then_operator_review":
            recovery_backlog.append(
                {
                    "source_type": row.source_type,
                    "label": row.label,
                    "recovery_mode": runtime_profile["failure_recovery_mode"],
                    "retry_backoff_minutes": runtime_profile["retry_backoff_minutes"],
                }
            )
    return {
        "project_id": project_id,
        "summary": {
            "total_integrations": len(rows),
            "managed_runtime_ready": managed_ready,
            "live_runtime_ready": live_ready,
            "auth_gaps": auth_gaps,
            "ru_market_surfaces": ru_surfaces,
            "seo_intelligence_surfaces": seo_surfaces,
        },
        "operator_policies": [
            "refresh high-signal demand sources at least daily",
            "rotate tokens on a fixed schedule and keep a fallback owner",
            "treat RU search, local, and social surfaces as one operating layer",
            "treat keyword, competitor, authority, and rank data as one SEO intelligence layer",
            "attach sync diagnostics to executive and delivery workflows",
        ],
        "managed_runtime_gaps": [
            "credentials missing" if auth_gaps else None,
            "some integrations still run on starter snapshots"
            if any(
                row["diagnostics"]["checks"]["snapshot_mode"] == "starter_or_stub"
                for row in rows
            )
            else None,
        ],
        "owner_queue": owner_queue,
        "recovery_backlog": recovery_backlog,
        "rows": rows,
    }


@router.get("/verification-matrix", response_model=IntegrationVerificationMatrixRead)
def integration_verification_matrix(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationVerificationMatrixRead:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    cms_rows = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project_id)
        .order_by(CmsConnector.id.desc())
        .all()
    )

    rows: list[IntegrationVerificationRowRead] = []
    for row in integration_rows:
        rows.append(
            IntegrationVerificationRowRead(
                **build_integration_verification_row(
                    row.source_type,
                    label=row.label,
                    credentials_env_var=row.credentials_env_var,
                    property_identifier=row.property_identifier,
                    latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
                )
            )
        )
    for row in cms_rows:
        contract = cms_contract(row.cms_type)
        inventory = json.loads(row.last_inventory_json or "{}")
        status = inventory.get("status", "")
        proof_level = (
            "starter_or_stub"
            if any(token in status for token in ["starter", "fallback"])
            else "live_inventory_or_reviewed_flow"
            if inventory
            else "contract_only"
        )
        rows.append(
            IntegrationVerificationRowRead(
                id=f"cms-{row.id}",
                surface_type="cms",
                surface_name=row.label,
                source_type=row.cms_type,
                readiness_tier=contract["readiness_tier"],
                proof_level=proof_level,
                credentials_status="configured" if row.auth_env_var else "missing",
                property_identifier=row.base_url,
                ci_workflow=".github/workflows/python-tests.yml",
                ci_gates=[
                    "inventory sync",
                    "patch package generation",
                    "approval-first apply path",
                    "post-apply verification",
                ],
                capabilities=[
                    "inventory",
                    "patch package",
                    "reviewed writeback path",
                ],
                production_flow=contract["production_path"],
                verification_checks=[
                    "credentials configured",
                    "inventory synced",
                    "patch preview generated",
                    "approval path defined",
                    "verify or rollback path available",
                ],
                latest_snapshot_source=inventory.get("status"),
                latest_snapshot_summary=inventory,
                next_step=contract["next_step"],
            )
        )

    return IntegrationVerificationMatrixRead(
        project_id=project_id,
        generated_at=datetime.utcnow(),
        rows=rows,
    )
