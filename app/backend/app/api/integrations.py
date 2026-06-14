from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import CmsConnector, IntegrationConnection, IntegrationSyncEvent, User
from ..schemas import (
    IntegrationConnectionCreate,
    IntegrationConnectionRead,
    IntegrationContractsResponse,
    IntegrationDetailRead,
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
    integration_contract,
    integration_env_status,
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
        if row.credentials_env_var or env_status["live_credentials_ready"]
        else "missing",
        recommended_ci_workflow=contract["recommended_ci_workflow"],
        ci_gates=contract["ci_gates"],
        contract_version=contract["contract_version"],
        sync_capabilities=contract["capabilities"],
        production_flow=contract.get("production_flow", []),
        sync_freshness=freshness,
        next_step=contract["next_step"],
        created_at=row.created_at,
    )


def _serialize_sync_event(row: IntegrationSyncEvent) -> IntegrationSyncEventRead:
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
        metadata=json.loads(row.metadata_json or "{}"),
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
    contract = integration_contract(row.source_type)
    event = IntegrationSyncEvent(
        integration_connection_id=row.id,
        status="running",
        attempt_number=1,
        retry_count=0,
        scope_status="starter_scope",
        credential_status="configured" if row.credentials_env_var else "missing",
        dataset_status="sync_started",
        provenance_level="starter_sync",
        freshness_label="sync_in_progress",
        metadata_json=json.dumps({"source_type": row.source_type}, ensure_ascii=False),
    )
    db.add(event)
    db.flush()
    try:
        snapshot = sync_integration_source(
            row.source_type,
            property_identifier=row.property_identifier,
            config=json.loads(row.config_json or "{}"),
        )
        snapshot["summary"] = compact_integration_summary(snapshot)
        row.latest_snapshot_json = json.dumps(snapshot, ensure_ascii=False)
        row.last_sync_status = "completed"
        row.last_sync_at = datetime.utcnow()
        event.status = "completed"
        event.scope_status = "verified_contract_scope"
        event.credential_status = (
            "configured" if row.credentials_env_var else "missing_but_starter_allowed"
        )
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
        event.metadata_json = json.dumps(
            {
                "source_type": row.source_type,
                "recommended_ci_workflow": contract["recommended_ci_workflow"],
            },
            ensure_ascii=False,
        )
    except Exception as exc:
        row.last_sync_status = "failed"
        event.status = "failed"
        event.retry_count = 1
        event.dataset_status = "unavailable"
        event.error_summary = str(exc)
        event.freshness_label = "stale"
        event.finished_at = datetime.utcnow()
        db.add(row)
        db.add(event)
        db.commit()
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
        runtime_level=latest_event.provenance_level if latest_event else "contract_only",
        last_successful_pull=row.last_sync_at,
        last_error=latest_event.error_summary if latest_event else None,
        recommended_next_steps=contract.get("production_flow", [])
        + [contract["next_step"]],
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
