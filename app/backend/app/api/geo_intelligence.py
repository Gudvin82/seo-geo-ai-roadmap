from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..config import load_settings
from ..database import get_db
from ..deps import get_current_user, get_optional_current_user
from ..models import AiVisibilitySnapshot, AuditRun, EvidenceRecord, ScanJob, User
from ..schemas import (
    AiVisibilitySnapshotCreate,
    AiVisibilitySnapshotRead,
    GeoIntelligenceRunRead,
    GeoIntelligenceRunRequest,
)
from ..services import scan_jobs
from ..services.audits import _persist_artifact
from ..services.geo_intelligence import (
    build_agent_audit_pack,
    build_geo_runtime,
    build_unified_report,
    normalize_scan_issue,
)
from ..services.graph_runtime import (
    build_graph_from_audit_findings,
    build_graph_from_scan_summary,
)
from ..services.reporting import dumps_json
from ..services.task_center import (
    build_task_bundle_from_audit_run,
    build_task_bundle_from_scan_job,
)

router = APIRouter(prefix="/geo-intelligence", tags=["geo-intelligence"])


def _scan_summary(scan_job: ScanJob) -> dict:
    for artifact in json.loads(scan_job.report_artifacts_json or "[]"):
        if artifact.get("kind") == "machine_report":
            try:
                with open(artifact["path"], "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=404, detail="Machine report artifact not found."
                ) from exc
    raise HTTPException(status_code=404, detail="Machine report artifact not found.")


def _snapshot_read(
    row: AiVisibilitySnapshot, changes: dict | None = None
) -> AiVisibilitySnapshotRead:
    return AiVisibilitySnapshotRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        target_url=row.target_url,
        query=row.query,
        query_set=row.query_set,
        provider=row.provider,
        model=row.model,
        evidence_type=row.evidence_type,
        confidence=row.confidence,
        response_reference=row.response_reference,
        evidence=json.loads(row.evidence_json or "{}"),
        snapshot=json.loads(row.snapshot_json or "{}"),
        observed_at=row.observed_at,
        created_at=row.created_at,
        changes=changes or {},
    )


@router.post("/runs", response_model=GeoIntelligenceRunRead)
def run_geo_intelligence(
    payload: GeoIntelligenceRunRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GeoIntelligenceRunRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    if payload.audit_run_id is None:
        raise HTTPException(
            status_code=400,
            detail="audit_run_id is required; run the platform audit before GEO analysis.",
        )
    audit_run = db.get(AuditRun, payload.audit_run_id)
    if not audit_run or audit_run.project_id != project.id:
        raise HTTPException(
            status_code=404, detail="Audit run not found for this project."
        )
    if audit_run.status != "completed":
        raise HTTPException(
            status_code=409, detail="GEO analysis requires a completed audit run."
        )
    runtime = build_geo_runtime(
        json.loads(audit_run.finding_groups_json or "[]"),
        payload.score_profile,
        payload.score_weights,
    )
    settings = getattr(request.app.state, "settings", load_settings())
    artifact = _persist_artifact(
        db,
        audit_run,
        project,
        settings,
        "geo_intelligence_runtime",
        dumps_json(runtime),
        "json",
        {
            "contract_version": runtime["contract_version"],
            "profile": runtime["scorecard"]["profile"]["name"],
        },
    )
    for item in runtime["findings"]:
        db.add(
            EvidenceRecord(
                workspace_id=project.workspace_id,
                project_id=project.id,
                label_type="internal_evidence",
                title=item["title"],
                summary=item["observation"],
                source_ref=item["source"],
                links_json=json.dumps(
                    [
                        e.get("reference", "")
                        for e in item["evidence"]
                        if e.get("reference")
                    ]
                ),
            )
        )
    task_bundle = build_task_bundle_from_audit_run(audit_run, runtime["findings"])
    record_audit_log(
        db,
        "geo_intelligence.completed",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={
            "audit_run_id": audit_run.id,
            "score_status": runtime["scorecard"]["status"],
        },
    )
    db.commit()
    return GeoIntelligenceRunRead(
        audit_run_id=audit_run.id,
        contract_version=runtime["contract_version"],
        findings=runtime["findings"],
        scorecard=runtime["scorecard"],
        roadmap=runtime["roadmap"],
        report_artifact_id=artifact.id,
        task_bundle=task_bundle,
    )


@router.get("/agent-audit-pack")
def agent_audit_pack() -> dict:
    return build_agent_audit_pack()


@router.get("/audit-runs/{audit_run_id}/unified-report")
def unified_audit_report(
    audit_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    audit_run = db.get(AuditRun, audit_run_id)
    if not audit_run:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    require_project_access(
        db, audit_run.project_id, current_user, minimum_role="viewer"
    )
    if audit_run.status != "completed":
        raise HTTPException(
            status_code=409, detail="Unified report requires a completed audit run."
        )
    findings = json.loads(audit_run.finding_groups_json or "[]")
    report = build_unified_report(
        target_url=audit_run.target_url or "", findings=findings
    )
    report["tasks"] = build_task_bundle_from_audit_run(audit_run, report["findings"])
    report["graph"] = build_graph_from_audit_findings(audit_run.id, report["findings"])
    report["source"] = {"type": "audit_run", "id": audit_run.id}
    return report


@router.get("/scan-jobs/{scan_job_id}/unified-report")
def unified_scan_report(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> dict:
    scan_job = db.get(ScanJob, scan_job_id)
    if not scan_job:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    scan_jobs.authorize_scan_job_access(scan_job, current_user, x_scanner_session)
    if scan_job.status != "completed":
        raise HTTPException(
            status_code=409, detail="Unified report requires a completed scan job."
        )
    summary = _scan_summary(scan_job)
    findings = [
        normalize_scan_issue(issue, summary.get("target_url", scan_job.normalized_url))
        for issue in summary.get("issues", [])
    ]
    report = build_unified_report(
        target_url=summary.get("target_url", scan_job.normalized_url), findings=findings
    )
    report["tasks"] = build_task_bundle_from_scan_job(scan_job, summary)
    report["graph"] = build_graph_from_scan_summary(scan_job.id, summary)
    report["source"] = {"type": "scan_job", "id": scan_job.id}
    return report


@router.post("/visibility-snapshots", response_model=AiVisibilitySnapshotRead)
def create_visibility_snapshot(
    payload: AiVisibilitySnapshotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AiVisibilitySnapshotRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    observed_at = payload.observed_at or datetime.now(timezone.utc)
    row = AiVisibilitySnapshot(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        target_url=payload.target_url,
        query=payload.query,
        query_set=payload.query_set,
        provider=payload.provider,
        model=payload.model,
        evidence_type=payload.evidence_type,
        confidence=payload.confidence,
        response_reference=payload.response_reference,
        evidence_json=json.dumps(payload.evidence, ensure_ascii=False),
        snapshot_json=json.dumps(payload.snapshot, ensure_ascii=False),
        observed_at=observed_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _snapshot_read(row)


@router.get("/visibility-snapshots", response_model=list[AiVisibilitySnapshotRead])
def list_visibility_snapshots(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AiVisibilitySnapshotRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(AiVisibilitySnapshot)
        .filter(AiVisibilitySnapshot.project_id == project_id)
        .order_by(AiVisibilitySnapshot.observed_at.desc())
        .limit(100)
        .all()
    )
    previous_by_key: dict[tuple[str, str, str], AiVisibilitySnapshot] = {}
    result: list[AiVisibilitySnapshotRead] = []
    for row in reversed(rows):
        key = (row.query, row.provider, row.model)
        previous = previous_by_key.get(key)
        changes = {"status": "first_observation"}
        if previous:
            current = json.loads(row.snapshot_json or "{}")
            prior = json.loads(previous.snapshot_json or "{}")
            changes = {
                "status": "compared",
                "changed": current != prior,
                "previous_snapshot_id": previous.id,
            }
        previous_by_key[key] = row
        result.append(_snapshot_read(row, changes))
    return list(reversed(result))
