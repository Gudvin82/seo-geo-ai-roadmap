from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import AuditRun, CmsConnector, User
from ..schemas import (
    CmsConnectorCreate,
    CmsConnectorRead,
    CmsWritebackAttemptRead,
    IntegrationContractsResponse,
    IntegrationSourceContractRead,
    PatchPackRead,
)
from ..services.cms import (
    all_cms_contracts,
    cms_contract,
    cms_patch_package,
    inventory_cms,
)
from ..services.retries import RetryPolicy, run_with_retry

router = APIRouter(prefix="/cms", tags=["cms"])


def _serialize(row: CmsConnector) -> CmsConnectorRead:
    contract = cms_contract(row.cms_type)
    allowed_actions = [
        "inventory sync",
        "metadata patch planning",
        "schema suggestion export",
    ]
    risky_actions = [
        "content overwrite",
        "publish to live pages",
        "bulk patch application",
    ]
    unsupported_actions = [
        "silent destructive updates",
        "publish without review",
        "unbounded site-wide writeback",
    ]
    if row.writeback_mode == "draft":
        allowed_actions.extend(
            [
                "draft patch generation",
                "human review bundle export",
            ]
        )
    if row.writeback_mode == "human_approved_publish":
        allowed_actions.append("human-approved publish package")
    return CmsConnectorRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        cms_type=row.cms_type,
        label=row.label,
        base_url=row.base_url,
        auth_env_var=row.auth_env_var,
        writeback_mode=row.writeback_mode,
        last_inventory=json.loads(row.last_inventory_json or "{}"),
        last_sync_status=row.last_sync_status,
        last_sync_at=row.last_sync_at,
        allowed_actions=allowed_actions,
        risky_actions=risky_actions,
        unsupported_actions=unsupported_actions,
        retry_policy={
            "max_attempts": 3,
            "initial_delay_seconds": 0.5,
            "backoff_multiplier": 2.0,
            "terminal_state": "dead",
            "scope": "inventory sync and governed writeback preparation",
        },
        readiness_tier=contract["readiness_tier"],
        execution_mode=contract["execution_mode"],
        contract_version=contract["contract_version"],
        required_env_vars=contract["required_env_vars"],
        credential_status="configured" if row.auth_env_var else "missing",
        production_path=contract["production_path"],
        next_step=contract["next_step"],
        created_at=row.created_at,
    )


@router.get("/contracts", response_model=IntegrationContractsResponse)
def list_cms_contracts() -> IntegrationContractsResponse:
    return IntegrationContractsResponse(
        contracts=[
            IntegrationSourceContractRead(
                source_type=contract["cms_type"],
                label=contract["cms_type"].replace("_", " ").title(),
                readiness_tier=contract["readiness_tier"],
                sync_mode=contract["execution_mode"],
                required_env_vars=contract["required_env_vars"],
                recommended_ci_workflow=".github/workflows/ai-visibility-check.yml",
                ci_gates=[
                    "inventory sync",
                    "patch export",
                    "human review gate",
                    "re-audit after apply",
                ],
                capabilities=contract["production_path"],
                contract_version=contract["contract_version"],
                next_step=contract["next_step"],
            )
            for contract in all_cms_contracts()
        ]
    )


@router.get("", response_model=list[CmsConnectorRead])
def list_cms_connectors(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CmsConnectorRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project_id)
        .order_by(CmsConnector.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.post("", response_model=CmsConnectorRead)
def create_cms_connector(
    payload: CmsConnectorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CmsConnectorRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    row = CmsConnector(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        cms_type=payload.cms_type,
        label=payload.label,
        base_url=payload.base_url,
        auth_env_var=payload.auth_env_var,
        writeback_mode=payload.writeback_mode,
        last_inventory_json="{}",
        last_sync_status="created",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.post("/{connector_id}/inventory", response_model=CmsConnectorRead)
def sync_cms_inventory(
    connector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CmsConnectorRead:
    row = db.get(CmsConnector, connector_id)
    if not row:
        raise HTTPException(status_code=404, detail="CMS connector not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    inventory = inventory_cms(row.cms_type, row.base_url, row.auth_env_var)
    row.last_inventory_json = json.dumps(inventory, ensure_ascii=False)
    row.last_sync_status = "completed"
    row.last_sync_at = datetime.utcnow()
    db.add(row)
    record_audit_log(
        db,
        "cms.inventory_synced",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"connector_id": row.id, "cms_type": row.cms_type},
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.post("/{connector_id}/patch-package", response_model=PatchPackRead)
def generate_cms_patch_package(
    connector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatchPackRead:
    row = db.get(CmsConnector, connector_id)
    if not row:
        raise HTTPException(status_code=404, detail="CMS connector not found.")
    project, _ = require_project_access(
        db, row.project_id, current_user, minimum_role="editor"
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    findings = (
        json.loads(latest_audit.finding_groups_json or "[]") if latest_audit else []
    )
    payload = cms_patch_package(
        row.cms_type,
        row.writeback_mode,
        project.name,
        project.website_url,
        findings,
    )
    return PatchPackRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        report_language=project.language,
        audience="agency",
        review_mode=row.writeback_mode,
        outputs=payload,
    )


@router.post(
    "/{connector_id}/writeback-attempt", response_model=CmsWritebackAttemptRead
)
def attempt_cms_writeback(
    connector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CmsWritebackAttemptRead:
    row = db.get(CmsConnector, connector_id)
    if not row:
        raise HTTPException(status_code=404, detail="CMS connector not found.")
    project, _ = require_project_access(
        db, row.project_id, current_user, minimum_role="editor"
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    retry_policy = {
        "max_attempts": 3,
        "initial_delay_seconds": 0.5,
        "backoff_multiplier": 2.0,
        "terminal_state": "dead",
        "scope": "governed writeback preparation only",
    }
    if row.writeback_mode == "read_only":
        record_audit_log(
            db,
            "cms.writeback_attempt_blocked",
            user_id=current_user.id,
            workspace_id=row.workspace_id,
            project_id=row.project_id,
            metadata={"connector_id": row.id, "writeback_mode": row.writeback_mode},
        )
        db.commit()
        return CmsWritebackAttemptRead(
            connector_id=row.id,
            project_id=row.project_id,
            workspace_id=row.workspace_id,
            writeback_mode=row.writeback_mode,
            status="blocked",
            summary="Read-only mode blocks writeback execution.",
            next_step="Switch to draft mode if you want patch generation without live publish.",
            retry_policy=retry_policy,
            attempts=0,
            artifact_preview={},
        )

    findings = (
        json.loads(latest_audit.finding_groups_json or "[]") if latest_audit else []
    )

    def _prepare_package() -> dict:
        if not findings:
            raise ValueError("No recent audit findings are available for writeback.")
        return cms_patch_package(
            row.cms_type,
            row.writeback_mode,
            project.name,
            project.website_url,
            findings,
        )

    outcome = run_with_retry(
        f"cms_writeback_{row.cms_type}",
        _prepare_package,
        RetryPolicy(max_attempts=3, initial_delay_seconds=0.5),
    )
    artifact_preview = outcome.result or {}
    if outcome.status == "dead":
        record_audit_log(
            db,
            "cms.writeback_attempt_dead",
            user_id=current_user.id,
            workspace_id=row.workspace_id,
            project_id=row.project_id,
            metadata={
                "connector_id": row.id,
                "writeback_mode": row.writeback_mode,
                "attempts": len(outcome.attempts),
                "error": outcome.error,
            },
        )
        db.commit()
        return CmsWritebackAttemptRead(
            connector_id=row.id,
            project_id=row.project_id,
            workspace_id=row.workspace_id,
            writeback_mode=row.writeback_mode,
            status="dead",
            summary="Governed writeback preparation reached terminal failure.",
            next_step="Review the latest audit availability and connector settings, then retry manually.",
            retry_policy=retry_policy,
            attempts=len(outcome.attempts),
            artifact_preview={},
        )

    final_status = (
        "awaiting_human_approval"
        if row.writeback_mode == "human_approved_publish"
        else "completed"
    )
    record_audit_log(
        db,
        f"cms.writeback_attempt_{final_status}",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={
            "connector_id": row.id,
            "writeback_mode": row.writeback_mode,
            "attempts": len(outcome.attempts),
            "retry_status": outcome.status,
        },
    )
    db.commit()
    return CmsWritebackAttemptRead(
        connector_id=row.id,
        project_id=row.project_id,
        workspace_id=row.workspace_id,
        writeback_mode=row.writeback_mode,
        status=final_status,
        summary=(
            "Draft patch bundle prepared."
            if final_status == "completed"
            else "Publish package prepared and now waiting for human approval."
        ),
        next_step=(
            "Review the patch package and apply changes in the CMS draft flow."
            if final_status == "completed"
            else "A human operator must review and approve before any live publish step."
        ),
        retry_policy=retry_policy,
        attempts=len(outcome.attempts),
        artifact_preview=artifact_preview,
    )
