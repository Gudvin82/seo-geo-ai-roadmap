from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..config import Settings
from ..database import get_db
from ..deps import get_optional_current_user
from ..models import (
    ScanJob,
    User,
    VerificationToken,
)
from ..scanner_schemas import (
    ConsentRecordCreate,
    ConsentRecordRead,
    PublicScannerConfigRead,
    PublicUrlAuditCreate,
    ScanArtifactRead,
    ScanJobAccepted,
    ScanJobCreate,
    ScanJobEventRead,
    ScanJobRead,
    ScanJobResultRead,
    VerificationRequestCreate,
    VerificationRequestRead,
)
from ..services import scan_jobs

router = APIRouter(prefix="/scanner", tags=["scanner"])
jobs_router = APIRouter(prefix="/scan-jobs", tags=["scan-jobs"])


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def _session_id(session_id: Optional[str]) -> str:
    value = (session_id or "").strip()
    if not value:
        raise HTTPException(
            status_code=400, detail="X-Scanner-Session header is required."
        )
    return value


def _requester_ip(request: Request) -> str:
    return (
        request.headers.get(
            "x-forwarded-for", request.client.host if request.client else "unknown"
        )
        .split(",")[0]
        .strip()
    )


def _token_value(db: Session, verification_request_id: int) -> str:
    token = (
        db.query(VerificationToken)
        .filter(VerificationToken.verification_request_id == verification_request_id)
        .order_by(VerificationToken.id.desc())
        .first()
    )
    if not token:
        raise HTTPException(status_code=404, detail="Verification token not found.")
    return token.challenge_value


def _authorize_scan_job(
    row: ScanJob,
    current_user: Optional[User],
    session_id: str,
) -> None:
    scan_jobs.authorize_scan_job_access(row, current_user, session_id)


def _machine_report(row: ScanJob) -> dict:
    for artifact in json.loads(row.report_artifacts_json or "[]"):
        path = Path(artifact["path"])
        if artifact.get("kind") == "machine_report" and path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Machine report artifact not found.")


@router.get("/config", response_model=PublicScannerConfigRead)
def get_public_scanner_config(request: Request) -> PublicScannerConfigRead:
    return PublicScannerConfigRead(
        **scan_jobs.scanner_config_payload(_settings(request))
    )


@router.post("/verification-requests", response_model=VerificationRequestRead)
def create_verification_request(
    payload: VerificationRequestCreate,
    request: Request,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> VerificationRequestRead:
    settings = _settings(request)
    row, plain = scan_jobs.create_verification_request(
        db,
        settings,
        url=payload.url,
        scan_mode=payload.scan_mode,
        method=payload.method,
        current_user=current_user,
        session_id=_session_id(x_scanner_session),
        source_ip=_requester_ip(request),
        user_agent=request.headers.get("user-agent", ""),
    )
    return VerificationRequestRead(
        **scan_jobs.serialize_verification_request(row, plain)
    )


@router.post(
    "/verification-requests/{verification_request_id}/verify",
    response_model=VerificationRequestRead,
)
def verify_verification_request(
    verification_request_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> VerificationRequestRead:
    settings = _settings(request)
    row = scan_jobs.verify_verification_request(db, settings, verification_request_id)
    return VerificationRequestRead(
        **scan_jobs.serialize_verification_request(
            row, _token_value(db, verification_request_id)
        )
    )


@router.post("/consent-records", response_model=ConsentRecordRead)
def create_consent_record(
    payload: ConsentRecordCreate,
    request: Request,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ConsentRecordRead:
    settings = _settings(request)
    row = scan_jobs.create_consent_record(
        db,
        settings,
        url=payload.url,
        scan_mode=payload.scan_mode,
        consent_scope=payload.consent_scope,
        ownership_confirmed=payload.ownership_confirmed,
        load_warning_accepted=payload.load_warning_accepted,
        limitations_accepted=payload.limitations_accepted,
        verification_request_id=payload.verification_request_id,
        current_user=current_user,
        session_id=_session_id(x_scanner_session),
        source_ip=_requester_ip(request),
        user_agent=request.headers.get("user-agent", ""),
    )
    return ConsentRecordRead(
        id=row.id,
        target_url=row.target_url,
        target_domain=row.target_domain,
        scan_mode=row.scan_mode,
        consent_scope=row.consent_scope,
        ownership_confirmed=row.ownership_confirmed,
        load_warning_accepted=row.load_warning_accepted,
        limitations_accepted=row.limitations_accepted,
        verification_request_id=row.verification_request_id,
        created_at=row.created_at,
    )


@router.post("/url-audit", response_model=ScanJobAccepted)
def create_url_audit(
    payload: PublicUrlAuditCreate,
    request: Request,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ScanJobAccepted:
    consent = scan_jobs.create_consent_record(
        db,
        _settings(request),
        url=payload.url,
        scan_mode=payload.mode,
        consent_scope="passive_ack"
        if payload.mode == "passive"
        else "active_authorized",
        ownership_confirmed=payload.ownership_confirmed,
        load_warning_accepted=payload.load_warning_accepted,
        limitations_accepted=payload.limitations_accepted,
        verification_request_id=payload.verification_request_id,
        current_user=current_user,
        session_id=_session_id(x_scanner_session),
        source_ip=_requester_ip(request),
        user_agent=request.headers.get("user-agent", ""),
    )
    row = scan_jobs.create_scan_job(
        db,
        _settings(request),
        url=payload.url,
        scan_mode=payload.mode,
        consent_record_id=consent.id,
        verification_request_id=payload.verification_request_id,
        callback_webhook_url=payload.callback_webhook_url,
        notification_email=payload.notification_email,
        telegram_chat_id=payload.telegram_chat_id,
        current_user=current_user,
        session_id=_session_id(x_scanner_session),
        source_ip=_requester_ip(request),
        user_agent=request.headers.get("user-agent", ""),
    )
    return ScanJobAccepted(
        scan_job_id=row.id,
        initial_status=row.status,
        status_endpoint=f"/api/v1/scan-jobs/{row.id}",
        events_endpoint=f"/api/v1/scan-jobs/{row.id}/events",
        artifacts_endpoint=f"/api/v1/scan-jobs/{row.id}/artifacts",
    )


@jobs_router.post("", response_model=ScanJobAccepted)
def create_scan_job(
    payload: ScanJobCreate,
    request: Request,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ScanJobAccepted:
    settings = _settings(request)
    row = scan_jobs.create_scan_job(
        db,
        settings,
        url=payload.url,
        scan_mode=payload.scan_mode,
        consent_record_id=payload.consent_record_id,
        verification_request_id=payload.verification_request_id,
        callback_webhook_url=payload.callback_webhook_url,
        notification_email=payload.notification_email,
        telegram_chat_id=payload.telegram_chat_id,
        current_user=current_user,
        session_id=_session_id(x_scanner_session),
        source_ip=_requester_ip(request),
        user_agent=request.headers.get("user-agent", ""),
    )
    return ScanJobAccepted(
        scan_job_id=row.id,
        initial_status=row.status,
        status_endpoint=f"/api/v1/scan-jobs/{row.id}",
        events_endpoint=f"/api/v1/scan-jobs/{row.id}/events",
        artifacts_endpoint=f"/api/v1/scan-jobs/{row.id}/artifacts",
    )


@jobs_router.get("/{scan_job_id}", response_model=ScanJobRead)
def get_scan_job(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ScanJobRead:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    return ScanJobRead(
        **scan_jobs.serialize_scan_job(
            row, queue_context=scan_jobs.scan_job_queue_context(db, row)
        )
    )


@jobs_router.post("/{scan_job_id}/cancel", response_model=ScanJobRead)
def cancel_scan_job(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ScanJobRead:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    cancelled = scan_jobs.cancel_scan_job(db, scan_job_id)
    return ScanJobRead(
        **scan_jobs.serialize_scan_job(
            cancelled, queue_context=scan_jobs.scan_job_queue_context(db, cancelled)
        )
    )


@jobs_router.get("/{scan_job_id}/events", response_model=list[ScanJobEventRead])
def get_scan_job_events(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> list[ScanJobEventRead]:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    return [
        ScanJobEventRead(**item)
        for item in scan_jobs.list_scan_job_events(db, scan_job_id)
    ]


@jobs_router.get("/{scan_job_id}/artifacts", response_model=list[ScanArtifactRead])
def get_scan_job_artifacts(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> list[ScanArtifactRead]:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    return [
        ScanArtifactRead(**item)
        for item in json.loads(row.report_artifacts_json or "[]")
    ]


@jobs_router.get("/{scan_job_id}/artifacts/{filename}")
def download_scan_job_artifact(
    scan_job_id: int,
    filename: str,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> FileResponse:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    for artifact in json.loads(row.report_artifacts_json or "[]"):
        path = Path(artifact["path"])
        if path.name == filename and path.exists():
            return FileResponse(path)
    raise HTTPException(status_code=404, detail="Artifact not found.")


@jobs_router.get("/{scan_job_id}/result", response_model=ScanJobResultRead)
def get_scan_job_result(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> ScanJobResultRead:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    _authorize_scan_job(row, current_user, _session_id(x_scanner_session))
    summary = _machine_report(row)
    recommendations = [
        item.get("recommended_action", "")
        for item in summary.get("issues", [])
        if item.get("recommended_action")
    ]
    return ScanJobResultRead(
        scan_job_id=row.id,
        schema_version=summary.get("schema_version", "v5.2.0"),
        target_url=summary.get("target_url", row.normalized_url),
        target_domain=summary.get("target_domain", row.target_domain),
        site_type=summary.get("site_type"),
        scan_mode=summary.get("scan_mode", row.scan_mode),
        executive_summary=summary.get("executive_summary", ""),
        checked_items=summary.get("checked_items", []),
        not_checked=summary.get("not_checked", []),
        recommendations=recommendations,
        issues=summary.get("issues", []),
        tasks_endpoint=f"/api/v1/tasks/scan-job/{row.id}",
        graph_endpoint=f"/api/v1/graph-runtime/scan-job/{row.id}",
        artifacts=json.loads(row.report_artifacts_json or "[]"),
    )
