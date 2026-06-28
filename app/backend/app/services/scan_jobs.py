from __future__ import annotations

import csv
import hashlib
import json
import smtplib
import threading
import time
from datetime import timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log
from ..config import Settings
from ..database import create_session
from ..models import (
    ConsentRecord,
    ScanJob,
    ScanJobEvent,
    User,
    VerificationRequest,
    VerificationToken,
    now_utc,
)
from ..version import APP_VERSION
from .discoverability_checks import (
    ai_readability_report,
    ai_txt_report,
    bots_report,
    cdn_ai_blocking_report,
    citability_score_report,
    classify_finding_status,
    faq_detection_report,
    open_graph_report,
    rag_chunk_readiness_report,
    resolve_public_file_url,
    robots_sitemap_report,
    schema_coverage_report,
    technical_seo_report,
)
from .scan_security import (
    normalize_public_url,
    normalize_target_url,
    safe_fetch_url_text,
)

SCANNER_SCHEMA_VERSION = "v6.8.0"
SCAN_JOB_TERMINAL_STATES = {
    "partial_success",
    "completed",
    "failed",
    "cancelled",
    "expired",
}
SCAN_JOB_ACTIVE_STATES = {"queued", "verifying", "running"}
_THREADS: dict[int, threading.Thread] = {}
_WORKER_LOCK = threading.Lock()
_WORKER_THREAD: threading.Thread | None = None


def scanner_config_payload(settings: Settings) -> dict:
    return {
        "allow_public_intake": settings.allow_public_intake,
        "allow_active_scan": settings.allow_active_scan,
        "allow_anonymous_submission": settings.allow_anonymous_submission,
        "allow_full_scan": settings.allow_full_scan,
        "allowed_schemes": settings.scanner_allowed_scheme_list(),
        "max_url_length": settings.scanner_max_url_length,
        "max_concurrent_submissions_per_ip": settings.scanner_max_concurrent_submissions_per_ip,
        "max_concurrent_submissions_per_domain": getattr(
            settings, "scanner_max_concurrent_submissions_per_domain", 2
        ),
        "max_pending_jobs_total": getattr(
            settings, "scanner_max_pending_jobs_total", 25
        ),
        "rate_limit_window_seconds": getattr(
            settings, "scanner_rate_limit_window_seconds", 600
        ),
        "max_submissions_per_ip_per_window": getattr(
            settings, "scanner_max_submissions_per_ip_per_window", 6
        ),
        "notification_retry_attempts": getattr(
            settings, "scanner_notification_retry_attempts", 2
        ),
        "dangerous_modes_feature_flagged": True,
        "limitations": [
            "This scanner does not replace a penetration test.",
            "Active scan requires verified ownership or explicit authorization.",
            "Some checks remain heuristic or operator-guided.",
            "External sites may rate-limit or block the scanner.",
            "Results depend on target availability and selected scan mode.",
        ],
    }


def create_verification_request(
    db: Session,
    settings: Settings,
    *,
    url: str,
    scan_mode: str,
    method: str,
    current_user: Optional[User],
    session_id: str,
    source_ip: str,
    user_agent: str,
) -> tuple[VerificationRequest, str]:
    normalized_url, host = normalize_target_url(url, settings)
    request = VerificationRequest(
        target_url=normalized_url,
        target_domain=host,
        scan_mode=scan_mode,
        method=method,
        status="pending",
        actor_user_id=current_user.id if current_user else None,
        actor_session_id=session_id,
        source_ip=source_ip,
        user_agent=user_agent,
        expires_at=now_utc()
        + timedelta(minutes=settings.scanner_verification_ttl_minutes),
    )
    db.add(request)
    db.flush()
    plain = f"discoverability-{request.id}-{hashlib.sha256(normalized_url.encode()).hexdigest()[:16]}"
    token = VerificationToken(
        verification_request_id=request.id,
        token_hash=hashlib.sha256(plain.encode()).hexdigest(),
        challenge_value=plain,
        method=method,
        status="pending",
        expires_at=request.expires_at,
    )
    db.add(token)
    record_audit_log(
        db,
        "scanner.verification_requested",
        user_id=current_user.id if current_user else None,
        metadata={
            "verification_request_id": request.id,
            "method": method,
            "target_domain": host,
        },
    )
    db.commit()
    db.refresh(request)
    return request, plain


def verify_verification_request(
    db: Session,
    settings: Settings,
    verification_request_id: int,
) -> VerificationRequest:
    request = db.get(VerificationRequest, verification_request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Verification request not found.")
    if request.expires_at and request.expires_at <= now_utc():
        request.status = "expired"
        db.commit()
        raise HTTPException(status_code=410, detail="Verification request expired.")
    token = (
        db.query(VerificationToken)
        .filter(VerificationToken.verification_request_id == request.id)
        .order_by(VerificationToken.id.desc())
        .first()
    )
    if not token:
        raise HTTPException(status_code=404, detail="Verification token not found.")

    verified = False
    if request.method == "html_file":
        verified = _verify_html_file(request.target_url, token.challenge_value)
    elif request.method == "meta_tag":
        verified = _verify_meta_tag(request.target_url, token.challenge_value)
    elif request.method == "dns_txt":
        verified = _verify_dns_txt(request.target_domain, token.challenge_value)

    request.status = "verified" if verified else "pending"
    token.status = request.status
    if verified:
        request.verified_at = now_utc()
    db.commit()
    return request


def create_consent_record(
    db: Session,
    settings: Settings,
    *,
    url: str,
    scan_mode: str,
    consent_scope: str,
    ownership_confirmed: bool,
    load_warning_accepted: bool,
    limitations_accepted: bool,
    verification_request_id: Optional[int],
    current_user: Optional[User],
    session_id: str,
    source_ip: str,
    user_agent: str,
) -> ConsentRecord:
    normalized_url, host = normalize_target_url(url, settings)
    if not limitations_accepted:
        raise HTTPException(status_code=400, detail="Limitations must be accepted.")
    if scan_mode in {"active", "full"} and not load_warning_accepted:
        raise HTTPException(
            status_code=400, detail="Active scanning requires load warning acceptance."
        )
    if scan_mode in {"active", "full"} and not ownership_confirmed:
        raise HTTPException(
            status_code=400,
            detail="Ownership or authorization confirmation is required.",
        )
    row = ConsentRecord(
        target_url=normalized_url,
        target_domain=host,
        scan_mode=scan_mode,
        consent_scope=consent_scope,
        ownership_confirmed=ownership_confirmed,
        load_warning_accepted=load_warning_accepted,
        limitations_accepted=limitations_accepted,
        actor_user_id=current_user.id if current_user else None,
        actor_session_id=session_id,
        source_ip=source_ip,
        user_agent=user_agent,
        verification_request_id=verification_request_id,
    )
    db.add(row)
    record_audit_log(
        db,
        "scanner.consent_recorded",
        user_id=current_user.id if current_user else None,
        metadata={"scan_mode": scan_mode, "target_domain": host},
    )
    db.commit()
    db.refresh(row)
    return row


def create_scan_job(
    db: Session,
    settings: Settings,
    *,
    url: str,
    scan_mode: str,
    consent_record_id: int,
    verification_request_id: Optional[int],
    callback_webhook_url: Optional[str],
    notification_email: Optional[str],
    telegram_chat_id: Optional[str],
    current_user: Optional[User],
    session_id: str,
    source_ip: str,
    user_agent: str,
) -> ScanJob:
    if not settings.allow_public_intake:
        raise HTTPException(status_code=403, detail="Public intake is disabled.")
    if current_user is None and not settings.allow_anonymous_submission:
        raise HTTPException(status_code=403, detail="Anonymous submission is disabled.")
    if scan_mode in {"active", "full"} and not settings.allow_active_scan:
        raise HTTPException(status_code=403, detail="Active scanning is disabled.")
    if scan_mode == "full" and not settings.allow_full_scan:
        raise HTTPException(status_code=403, detail="Full scan is disabled.")

    normalized_url, host = normalize_target_url(url, settings)
    normalized_webhook = None
    if callback_webhook_url:
        normalized_webhook = normalize_public_url(callback_webhook_url, settings)
    consent = db.get(ConsentRecord, consent_record_id)
    if not consent or consent.target_url != normalized_url:
        raise HTTPException(
            status_code=400, detail="Consent record does not match the target URL."
        )
    if scan_mode in {"active", "full"}:
        if not verification_request_id:
            raise HTTPException(
                status_code=400, detail="Active scan requires ownership verification."
            )
        verification = db.get(VerificationRequest, verification_request_id)
        if not verification or verification.status != "verified":
            raise HTTPException(
                status_code=403,
                detail="Active scan requires a verified ownership record.",
            )
    else:
        verification = (
            db.get(VerificationRequest, verification_request_id)
            if verification_request_id
            else None
        )

    active_for_ip = (
        db.query(ScanJob)
        .filter(
            ScanJob.requester_ip == source_ip,
            ScanJob.status.in_(SCAN_JOB_ACTIVE_STATES),
        )
        .count()
    )
    if active_for_ip >= settings.scanner_max_concurrent_submissions_per_ip:
        raise HTTPException(
            status_code=429, detail="Submission limit reached for this IP."
        )
    recent_for_ip = (
        db.query(ScanJob)
        .filter(
            ScanJob.requester_ip == source_ip,
            ScanJob.created_at
            >= now_utc()
            - timedelta(seconds=settings.scanner_rate_limit_window_seconds),
        )
        .count()
    )
    if recent_for_ip >= settings.scanner_max_submissions_per_ip_per_window:
        raise HTTPException(
            status_code=429,
            detail="Rate limit reached for this IP within the current window.",
        )
    active_for_domain = (
        db.query(ScanJob)
        .filter(
            ScanJob.target_domain == host, ScanJob.status.in_(SCAN_JOB_ACTIVE_STATES)
        )
        .count()
    )
    if active_for_domain >= settings.scanner_max_concurrent_submissions_per_domain:
        raise HTTPException(
            status_code=429, detail="Submission limit reached for this domain."
        )
    active_total = (
        db.query(ScanJob).filter(ScanJob.status.in_(SCAN_JOB_ACTIVE_STATES)).count()
    )
    if active_total >= settings.scanner_max_pending_jobs_total:
        raise HTTPException(
            status_code=429,
            detail="Scanner queue is currently full. Try again shortly.",
        )

    row = ScanJob(
        submitted_url=url.strip(),
        normalized_url=normalized_url,
        target_domain=host,
        scan_mode=scan_mode,
        status="queued",
        progress_percent=0,
        current_stage="queued",
        requester_user_id=current_user.id if current_user else None,
        requester_session_id=session_id,
        requester_ip=source_ip,
        requester_email=notification_email,
        webhook_url=normalized_webhook,
        notification_email=notification_email,
        telegram_chat_id=telegram_chat_id,
        verification_request_id=verification.id if verification else None,
        consent_record_id=consent.id,
    )
    db.add(row)
    db.flush()
    _append_event(
        db, row.id, "queued", "queued", "Scan job accepted.", {"scan_mode": scan_mode}
    )
    record_audit_log(
        db,
        "scanner.job_created",
        user_id=current_user.id if current_user else None,
        metadata={"scan_job_id": row.id, "scan_mode": scan_mode, "target_domain": host},
    )
    db.commit()
    db.refresh(row)
    _launch_scan_job(settings, row.id)
    return row


def authorize_scan_job_access(
    row: ScanJob,
    current_user: Optional[User],
    session_id: Optional[str],
) -> None:
    if current_user and row.requester_user_id == current_user.id:
        return
    if session_id and row.requester_session_id == session_id:
        return
    raise HTTPException(
        status_code=403, detail="Scan job is not available for this session."
    )


def cancel_scan_job(db: Session, scan_job_id: int) -> ScanJob:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    if row.status in SCAN_JOB_TERMINAL_STATES:
        return row
    row.cancellation_requested = True
    _append_event(
        db, row.id, row.status, row.current_stage, "Cancellation requested.", {}
    )
    db.commit()
    return row


def scan_job_queue_context(db: Session, row: ScanJob) -> dict:
    queue_position = None
    if row.status == "queued":
        queue_position = (
            db.query(ScanJob)
            .filter(ScanJob.status == "queued", ScanJob.id <= row.id)
            .count()
        )
    queue_depth = db.query(ScanJob).filter(ScanJob.status == "queued").count()
    active_jobs_for_domain = (
        db.query(ScanJob)
        .filter(
            ScanJob.target_domain == row.target_domain,
            ScanJob.status.in_(SCAN_JOB_ACTIVE_STATES),
        )
        .count()
    )
    return {
        "queue_position": queue_position,
        "queue_depth": queue_depth,
        "active_jobs_for_domain": active_jobs_for_domain,
    }


def serialize_scan_job(row: ScanJob, *, queue_context: dict | None = None) -> dict:
    queue_context = queue_context or {}
    return {
        "id": row.id,
        "submitted_url": row.submitted_url,
        "normalized_url": row.normalized_url,
        "target_domain": row.target_domain,
        "scan_mode": row.scan_mode,
        "status": row.status,
        "progress_percent": row.progress_percent,
        "current_stage": row.current_stage,
        "error_summary": row.error_summary,
        "report_artifacts": json.loads(row.report_artifacts_json or "[]"),
        "queue_position": queue_context.get("queue_position"),
        "queue_depth": queue_context.get("queue_depth", 0),
        "active_jobs_for_domain": queue_context.get("active_jobs_for_domain", 0),
        "created_at": row.created_at,
        "started_at": row.started_at,
        "finished_at": row.finished_at,
    }


def serialize_scan_job_event(row: ScanJobEvent) -> dict:
    return {
        "id": row.id,
        "scan_job_id": row.scan_job_id,
        "status": row.status,
        "stage": row.stage,
        "message": row.message,
        "metadata": json.loads(row.metadata_json or "{}"),
        "created_at": row.created_at,
    }


def list_scan_job_events(db: Session, scan_job_id: int) -> list[dict]:
    rows = (
        db.query(ScanJobEvent)
        .filter(ScanJobEvent.scan_job_id == scan_job_id)
        .order_by(ScanJobEvent.id.asc())
        .all()
    )
    return [serialize_scan_job_event(row) for row in rows]


def serialize_verification_request(
    row: VerificationRequest, challenge_value: str
) -> dict:
    payload = {
        "id": row.id,
        "target_url": row.target_url,
        "target_domain": row.target_domain,
        "scan_mode": row.scan_mode,
        "method": row.method,
        "status": row.status,
        "challenge_value": challenge_value,
        "verification_path": None,
        "verification_meta_tag": None,
        "verification_dns_name": None,
        "created_at": row.created_at,
        "verified_at": row.verified_at,
        "expires_at": row.expires_at,
    }
    if row.method == "html_file":
        payload["verification_path"] = (
            f"/.well-known/discoverability-verification-{challenge_value}.txt"
        )
    elif row.method == "meta_tag":
        payload["verification_meta_tag"] = (
            f'<meta name="discoverability-verification" content="{challenge_value}" />'
        )
    elif row.method == "dns_txt":
        payload["verification_dns_name"] = row.target_domain
    return payload


def _launch_scan_job(settings: Settings, scan_job_id: int) -> None:
    del scan_job_id
    with _WORKER_LOCK:
        global _WORKER_THREAD
        if _WORKER_THREAD is not None and _WORKER_THREAD.is_alive():
            return
        thread = threading.Thread(
            target=_scan_worker_loop,
            args=(settings,),
            daemon=True,
            name="scan-job-worker",
        )
        _WORKER_THREAD = thread
        thread.start()


def recover_incomplete_scan_jobs() -> int:
    db = create_session()
    try:
        rows = (
            db.query(ScanJob)
            .filter(ScanJob.status.in_(("verifying", "running")))
            .order_by(ScanJob.id.asc())
            .all()
        )
        recovered = 0
        for row in rows:
            row.status = "queued"
            row.current_stage = "recovered_after_restart"
            row.progress_percent = min(row.progress_percent or 0, 5)
            _append_event(
                db,
                row.id,
                "queued",
                "recovered_after_restart",
                "Recovered queued scan job after worker restart.",
                {},
            )
            recovered += 1
        if recovered:
            db.commit()
        return recovered
    finally:
        db.close()


def _scan_worker_loop(settings: Settings) -> None:
    recover_incomplete_scan_jobs()
    try:
        while True:
            claimed_job_id = _claim_next_scan_job()
            if claimed_job_id is None:
                return
            _run_scan_job(settings, claimed_job_id, already_claimed=True)
    finally:
        with _WORKER_LOCK:
            global _WORKER_THREAD
            _WORKER_THREAD = None


def _claim_next_scan_job() -> int | None:
    db = create_session()
    try:
        row = (
            db.query(ScanJob)
            .filter(ScanJob.status == "queued")
            .order_by(ScanJob.id.asc())
            .first()
        )
        if row is None:
            return None
        row.status = "verifying"
        row.current_stage = "worker_claimed"
        row.progress_percent = max(row.progress_percent or 0, 5)
        if row.started_at is None:
            row.started_at = now_utc()
        _append_event(
            db,
            row.id,
            "verifying",
            "worker_claimed",
            "Scan job claimed by the persistent worker.",
            {},
        )
        db.commit()
        return row.id
    finally:
        db.close()


def _run_scan_job(
    settings: Settings, scan_job_id: int, *, already_claimed: bool = False
) -> None:
    db = create_session()
    try:
        row = db.get(ScanJob, scan_job_id)
        if not row:
            return
        _THREADS[scan_job_id] = threading.current_thread()
        if not already_claimed:
            _transition_job(
                db, row, "verifying", 10, "verification", "Preparing scan context."
            )
        else:
            _transition_job(
                db, row, "verifying", 10, "verification", "Preparing scan context."
            )
        if row.scan_mode in {"active", "full"} and row.verification_request_id:
            verification = db.get(VerificationRequest, row.verification_request_id)
            if not verification or verification.status != "verified":
                _fail_job(db, row, "Ownership verification is missing or expired.")
                return

        if row.cancellation_requested:
            _cancel_job(db, row)
            return

        _transition_job(db, row, "running", 35, "discovery", "Collecting site signals.")
        summary = _build_summary(row, settings)
        if row.cancellation_requested:
            _cancel_job(db, row)
            return

        _transition_job(
            db, row, "running", 70, "reporting", "Generating report artifacts."
        )
        artifacts = _write_artifacts(settings, row, summary)
        row.report_artifacts_json = json.dumps(artifacts, ensure_ascii=False)

        if row.cancellation_requested:
            _cancel_job(db, row)
            return

        _transition_job(
            db, row, "running", 85, "notifications", "Delivering notifications."
        )
        notification_errors = _deliver_notifications(settings, row, artifacts)
        if notification_errors:
            row.status = "partial_success"
            row.progress_percent = 100
            row.current_stage = "completed_with_notification_errors"
            row.error_summary = "; ".join(notification_errors)
            row.finished_at = now_utc()
            _append_event(
                db,
                row.id,
                row.status,
                row.current_stage,
                "Scan completed but one or more notifications failed.",
                {"errors": notification_errors},
            )
        else:
            row.status = "completed"
            row.progress_percent = 100
            row.current_stage = "completed"
            row.finished_at = now_utc()
            _append_event(
                db,
                row.id,
                "completed",
                "completed",
                "Scan completed.",
                {"artifact_count": len(artifacts)},
            )
        db.commit()
    except Exception as exc:  # pragma: no cover - defensive worker boundary
        row = db.get(ScanJob, scan_job_id)
        if row:
            _fail_job(db, row, f"{exc.__class__.__name__}: {exc}")
    finally:
        _THREADS.pop(scan_job_id, None)
        db.close()


def _transition_job(
    db: Session, row: ScanJob, status: str, progress: int, stage: str, message: str
) -> None:
    if row.started_at is None:
        row.started_at = now_utc()
    row.status = status
    row.progress_percent = progress
    row.current_stage = stage
    _append_event(db, row.id, status, stage, message, {})
    db.commit()


def _append_event(
    db: Session,
    scan_job_id: int,
    status: str,
    stage: str,
    message: str,
    metadata: dict,
) -> None:
    db.add(
        ScanJobEvent(
            scan_job_id=scan_job_id,
            status=status,
            stage=stage,
            message=message,
            metadata_json=json.dumps(metadata, ensure_ascii=False),
        )
    )


def _fail_job(db: Session, row: ScanJob, error_summary: str) -> None:
    row.status = "failed"
    row.progress_percent = 100
    row.current_stage = "failed"
    row.error_summary = error_summary
    row.finished_at = now_utc()
    _append_event(db, row.id, "failed", "failed", error_summary, {})
    db.commit()


def _cancel_job(db: Session, row: ScanJob) -> None:
    row.status = "cancelled"
    row.progress_percent = 100
    row.current_stage = "cancelled"
    row.finished_at = now_utc()
    _append_event(db, row.id, "cancelled", "cancelled", "Scan was cancelled.", {})
    db.commit()


def _build_summary(row: ScanJob, settings: Settings) -> dict:
    split = urlsplit(row.normalized_url)
    module_results = _run_discoverability_modules(row)
    checks = {
        "passive": [
            "URL normalization and public-host validation",
            "Surface-level crawlability, AI policy, and discoverability hints",
            "Heuristic readiness summary for SEO, GEO, AI readability, citability, schema, FAQ, metadata, and chunking surfaces",
        ],
        "active": [
            "Ownership-gated active verification path",
            "Extended reachability and public-surface discoverability checks",
            "Artifact-ready summary with AI readability, citability, CDN bot, and chunking notes",
        ],
        "full": [
            "Ownership-gated active verification path",
            "Extended reachability and public-surface discoverability checks",
            "Expanded artifact pack, notification summary, and machine-readable GEO/AI findings",
        ],
    }
    issue_rows = _build_issue_rows(module_results)
    recommendations = [
        item["recommended_action"]
        for item in issue_rows
        if item.get("recommended_action")
    ][:6]
    return {
        "schema_version": SCANNER_SCHEMA_VERSION,
        "job_id": row.id,
        "target_url": row.normalized_url,
        "target_domain": row.target_domain,
        "scan_mode": row.scan_mode,
        "executive_summary": (
            f"{split.hostname} was processed through the {row.scan_mode} scanner foundation. "
            "This output is safe for self-hosted intake and operator review, not a penetration test. "
            "The report includes citation-readiness, AI readability, edge-policy, and chunking heuristics."
        ),
        "checked_items": checks[row.scan_mode],
        "not_checked": [
            "Authenticated application flows",
            "Private network surfaces",
            "Exploit-oriented or pentest behavior",
            "Definitive legal advice or guaranteed compliance conclusions",
        ],
        "recommendations": recommendations,
        "issues": issue_rows,
        "module_results": module_results,
        "limitations": scanner_config_payload(settings)["limitations"],
        "task_export_targets": [
            "github_issues",
            "gitlab",
            "notion",
            "trello",
            "linear",
        ],
    }


def _build_issue_rows(module_results: list[dict]) -> list[dict]:
    issue_rows = [
        {
            "issue_id": "scanner-limitations",
            "severity": "medium",
            "title": "Results remain heuristic without operator review",
            "recommended_action": "Review the exported summary before treating it as a final client deliverable.",
        },
        {
            "issue_id": "public-surface-variability",
            "severity": "medium",
            "title": "External sites may rate-limit or alter scanner visibility",
            "recommended_action": "Re-run the scan later if the target was unstable or partially blocked.",
        },
    ]
    for module in module_results:
        if module["status"] in {"pass", "info"}:
            continue
        recommendation = module.get("recommendation") or "; ".join(
            module.get("warnings", [])
        )
        issue_rows.append(
            {
                "issue_id": module["id"],
                "severity": "high" if module["status"] == "fail" else "medium",
                "title": module["title"],
                "recommended_action": recommendation
                or "Review the module output and align the public surface.",
            }
        )
    return issue_rows


def _run_discoverability_modules(row: ScanJob) -> list[dict]:
    settings = _scanner_runtime_settings()
    html, html_error = _try_fetch_scanner_text(row.normalized_url, settings)
    llms_content, _ = _try_fetch_scanner_text(
        resolve_public_file_url(row.normalized_url, "llms.txt"), settings
    )
    ai_content, ai_error = _try_fetch_scanner_text(
        resolve_public_file_url(row.normalized_url, "ai.txt"), settings
    )
    robots_content, robots_error = _try_fetch_scanner_text(
        resolve_public_file_url(row.normalized_url, "robots.txt"), settings
    )

    modules: list[dict] = []
    modules.append(
        _safe_module("ru_ai_bots", "RU and AI bot policy", lambda: _bot_module(row))
    )
    modules.append(
        _safe_module(
            "robots_sitemap_linkage",
            "robots.txt and sitemap linkage",
            lambda: _robots_sitemap_module(row),
        )
    )
    modules.append(
        _safe_module(
            "ai_txt",
            "ai.txt guidance and consistency",
            lambda: _ai_txt_module(ai_content, ai_error, robots_content, llms_content),
        )
    )
    modules.append(
        _safe_module(
            "ai_readability",
            "AI readability layers",
            lambda: _html_required_module(
                html,
                html_error,
                lambda body: ai_readability_report(body, page_url=row.normalized_url),
                "Unable to fetch page HTML for AI readability checks.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "schema_coverage",
            "Structured data coverage",
            lambda: _html_required_module(
                html,
                html_error,
                lambda body: schema_coverage_report(body),
                "Unable to fetch page HTML for schema coverage.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "faq_answer_ready",
            "FAQ and answer-ready coverage",
            lambda: _html_required_module(
                html,
                html_error,
                faq_detection_report,
                "Unable to fetch page HTML for FAQ detection.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "citability_score",
            "Citation probability and quick wins",
            lambda: _html_required_module(
                html,
                html_error,
                lambda body: citability_score_report(body, page_url=row.normalized_url),
                "Unable to fetch page HTML for citability scoring.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "social_meta",
            "Open Graph and Twitter card completeness",
            lambda: _html_required_module(
                html,
                html_error,
                open_graph_report,
                "Unable to fetch page HTML for social metadata checks.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "rag_chunk_readiness",
            "RAG chunk readiness",
            lambda: _html_required_module(
                html,
                html_error,
                rag_chunk_readiness_report,
                "Unable to fetch page HTML for chunking checks.",
            ),
        )
    )
    modules.append(
        _safe_module(
            "cdn_ai_bot_blocking",
            "CDN and edge blocking for AI bots",
            lambda: _cdn_ai_bot_module(row),
        )
    )
    modules.append(
        _safe_module(
            "technical_seo_basics",
            "Technical SEO baseline",
            lambda: _html_required_module(
                html,
                html_error,
                lambda body: technical_seo_report(body, row.normalized_url),
                "Unable to fetch page HTML for technical SEO checks.",
            ),
        )
    )
    return modules


def _safe_module(module_id: str, title: str, runner) -> dict:
    try:
        payload = runner()
    except Exception as exc:  # pragma: no cover - defensive boundary
        return {
            "id": module_id,
            "title": title,
            "status": "needs-review",
            "observed_fact": "",
            "inferred_issue": f"{exc.__class__.__name__}: {exc}",
            "recommendation": "Review this module manually because the automated check could not complete.",
            "limitations": ["Automated module execution failed unexpectedly."],
            "raw": {},
        }
    return {
        "id": module_id,
        "title": title,
        "status": classify_finding_status(payload["status"]),
        "observed_fact": payload.get("observed_fact", ""),
        "inferred_issue": payload.get("inferred_issue", ""),
        "recommendation": payload.get("recommendation", ""),
        "limitations": payload.get("limitations", []),
        "raw": payload.get("raw", {}),
    }


def _bot_module(row: ScanJob) -> dict:
    report = bots_report(row.normalized_url)
    yandex_additional = next(
        item for item in report["results"] if item["bot"] == "YandexAdditional"
    )
    unclear = [
        item["bot"] for item in report["results"] if item["status"] == "unspecified"
    ]
    return {
        "status": "warn" if unclear else "pass",
        "observed_fact": (
            f"YandexAdditional is {yandex_additional['status']} and evaluated separately from YandexBot."
        ),
        "inferred_issue": (
            f"Unclear policy for: {', '.join(unclear)}." if unclear else ""
        ),
        "recommendation": "Keep YandexBot and YandexAdditional policies explicit when RU AI discoverability matters.",
        "limitations": [
            "robots.txt policy does not prove actual inclusion in search or AI answer surfaces."
        ],
        "raw": report,
    }


def _cdn_ai_bot_module(row: ScanJob) -> dict:
    report = cdn_ai_blocking_report(row.normalized_url)
    blocked = [item["bot"] for item in report["probes"] if item["blocked"]]
    return {
        "status": report["status"],
        "observed_fact": f"Detected CDN: {report['detected_cdn']}; blocked bots: {', '.join(blocked) or 'none'}.",
        "inferred_issue": "; ".join(report["warnings"]),
        "recommendation": report["recommendation"],
        "limitations": [report["limitation"]],
        "raw": report,
    }


def _robots_sitemap_module(row: ScanJob) -> dict:
    report = robots_sitemap_report(
        row.normalized_url,
        sitemap_url=resolve_public_file_url(row.normalized_url, "sitemap.xml"),
    )
    return {
        "status": report["status"],
        "observed_fact": f"{len(report['declared_sitemaps'])} sitemap declaration(s) found in robots.txt.",
        "inferred_issue": "; ".join(report["warnings"]),
        "recommendation": "Declare reachable sitemap URLs in robots.txt and keep the linkage explicit.",
        "limitations": [
            "Reachable sitemap XML still does not guarantee desired indexing behavior."
        ],
        "raw": report,
    }


def _ai_txt_module(
    ai_content: Optional[str],
    ai_error: Optional[str],
    robots_content: Optional[str],
    llms_content: Optional[str],
) -> dict:
    if ai_content is None:
        return {
            "status": "warn",
            "observed_fact": "ai.txt could not be loaded from the public site.",
            "inferred_issue": ai_error or "Missing or unreachable ai.txt.",
            "recommendation": "Publish ai.txt only if you have a clear, short AI guidance file to maintain.",
            "limitations": [
                "ai.txt is not a guaranteed standard across all crawlers and answer engines."
            ],
            "raw": {},
        }
    report = ai_txt_report(
        ai_content, robots_content=robots_content, llms_content=llms_content
    )
    return {
        "status": report["status"],
        "observed_fact": f"ai.txt directives found: {', '.join(sorted(report['directives'].keys())) or 'none'}.",
        "inferred_issue": "; ".join(report["warnings"] + report["contradictions"]),
        "recommendation": "Keep ai.txt consistent with robots.txt and llms.txt, and avoid stale or conflicting route guidance.",
        "limitations": [
            "ai.txt semantics remain emergent and may be interpreted inconsistently."
        ],
        "raw": report,
    }


def _html_required_module(
    html: Optional[str],
    html_error: Optional[str],
    runner,
    error_message: str,
) -> dict:
    if html is None:
        return {
            "status": "needs-review",
            "observed_fact": error_message,
            "inferred_issue": html_error or error_message,
            "recommendation": "Retry when the page is reachable or review the page source manually.",
            "limitations": ["Public HTML could not be loaded during the scan."],
            "raw": {},
        }
    report = runner(html)
    warnings = report.get("warnings", [])
    return {
        "status": report["status"],
        "observed_fact": _module_observed_fact(report),
        "inferred_issue": "; ".join(warnings),
        "recommendation": report.get("recommendation", ""),
        "limitations": [report.get("limitation")] if report.get("limitation") else [],
        "raw": report,
    }


def _module_observed_fact(report: dict) -> str:
    if "found_types" in report:
        return "Found schema types: " + ", ".join(report["found_types"] or ["none"])
    if "visible_faq_headings" in report:
        count = len(report["visible_faq_headings"]) + len(
            report["question_like_headings"]
        )
        return f"Detected {count} FAQ or question-like signals."
    if "fields" in report:
        missing = report.get("missing_fields", [])
        return (
            "All required Open Graph and Twitter Card fields were found."
            if not missing
            else "Missing social metadata fields: " + ", ".join(missing)
        )
    if "canonical_url" in report:
        return (
            f"Canonical: {report.get('canonical_url') or 'missing'}; "
            f"hreflang entries: {len(report.get('hreflang_refs', []))}; "
            f"internal links: {report.get('internal_link_count', 0)}."
        )
    return ""


def _write_artifacts(settings: Settings, row: ScanJob, summary: dict) -> list[dict]:
    base_dir = Path(settings.artifact_root) / "scan-jobs" / f"job-{row.id}"
    base_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict] = []

    json_path = base_dir / "report.json"
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    artifacts.append(_artifact_entry("machine_report", "json", json_path, row.id))

    md_path = base_dir / "summary.md"
    md_lines = [
        f"# Scanner Summary for {row.target_domain}",
        "",
        f"- Scan mode: `{row.scan_mode}`",
        f"- Schema version: `{SCANNER_SCHEMA_VERSION}`",
        "",
        summary["executive_summary"],
        "",
        "## Checked items",
    ]
    md_lines.extend([f"- {item}" for item in summary["checked_items"]])
    md_lines.extend(["", "## Not checked"])
    md_lines.extend([f"- {item}" for item in summary["not_checked"]])
    md_lines.extend(["", "## Module results"])
    for item in summary["module_results"]:
        md_lines.append(
            f"- `{item['id']}`: **{item['status']}** — {item['observed_fact']}"
        )
        if item["inferred_issue"]:
            md_lines.append(f"  Issue: {item['inferred_issue']}")
        if item["recommendation"]:
            md_lines.append(f"  Next action: {item['recommendation']}")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    artifacts.append(_artifact_entry("summary", "markdown", md_path, row.id))

    csv_path = base_dir / "issues.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["issue_id", "severity", "title", "recommended_action"]
        )
        writer.writeheader()
        writer.writerows(summary["issues"])
    artifacts.append(_artifact_entry("issues", "csv", csv_path, row.id))

    html_path = base_dir / "summary.html"
    html_path.write_text(
        (
            "<!doctype html><html><body><h1>Scanner Summary</h1>"
            f"<p>{summary['executive_summary']}</p>"
            f"<p>Schema version: {SCANNER_SCHEMA_VERSION}</p>"
            "</body></html>"
        ),
        encoding="utf-8",
    )
    artifacts.append(_artifact_entry("executive_summary", "html", html_path, row.id))
    return artifacts


def _artifact_entry(kind: str, fmt: str, path: Path, job_id: int) -> dict:
    return {
        "kind": kind,
        "format": fmt,
        "path": str(path),
        "schema_version": SCANNER_SCHEMA_VERSION,
        "download_endpoint": f"/api/v1/scan-jobs/{job_id}/artifacts/{path.name}",
    }


def _deliver_notifications(
    settings: Settings, row: ScanJob, artifacts: list[dict]
) -> list[str]:
    payload = {
        "schema_version": SCANNER_SCHEMA_VERSION,
        "scan_job_id": row.id,
        "status": "completed",
        "target_url": row.normalized_url,
        "scan_mode": row.scan_mode,
        "artifacts": artifacts,
    }
    errors: list[str] = []
    if row.webhook_url:
        error = _retry_notification(
            settings,
            lambda: _send_webhook(
                row.webhook_url, payload, settings.scanner_webhook_timeout_seconds
            ),
        )
        if error:
            errors.append(f"webhook: {error}")
    if row.notification_email:
        error = _retry_notification(
            settings, lambda: _send_email(settings, row.notification_email, payload)
        )
        if error:
            errors.append(f"email: {error}")
    if row.telegram_chat_id:
        error = _retry_notification(
            settings, lambda: _send_telegram(settings, row.telegram_chat_id, payload)
        )
        if error:
            errors.append(f"telegram: {error}")
    return errors


def _retry_notification(settings: Settings, callback) -> str | None:
    last_error: Exception | None = None
    attempts = max(1, settings.scanner_notification_retry_attempts)
    for attempt in range(attempts):
        try:
            callback()
            return None
        except Exception as exc:  # pragma: no cover - depends on external sink
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(max(0, settings.scanner_notification_retry_backoff_seconds))
    return str(last_error) if last_error else "unknown notification error"


def _send_webhook(url: str, payload: dict, timeout: int) -> None:
    _send_webhook_with_settings(_scanner_runtime_settings(), url, payload, timeout)


def _send_webhook_with_settings(
    settings: Settings, url: str, payload: dict, timeout: int
) -> None:
    safe_fetch_url_text(
        url,
        settings,
        timeout=timeout,
        max_bytes=512_000,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
    )


def _send_email(settings: Settings, recipient: str, payload: dict) -> None:
    if not settings.scanner_smtp_host or not settings.scanner_smtp_from_email:
        raise RuntimeError("SMTP is not configured.")
    message = EmailMessage()
    message["Subject"] = f"Scan job {payload['scan_job_id']} completed"
    message["From"] = settings.scanner_smtp_from_email
    message["To"] = recipient
    message.set_content(json.dumps(payload, ensure_ascii=False, indent=2))
    with smtplib.SMTP(
        settings.scanner_smtp_host, settings.scanner_smtp_port, timeout=10
    ) as server:
        server.starttls()
        if settings.scanner_smtp_username:
            server.login(settings.scanner_smtp_username, settings.scanner_smtp_password)
        server.send_message(message)


def _send_telegram(settings: Settings, chat_id: str, payload: dict) -> None:
    _send_telegram_text(
        settings,
        chat_id,
        f"Scan job {payload['scan_job_id']} completed for {payload['target_url']}",
    )


def _send_telegram_text(settings: Settings, chat_id: str, text: str) -> None:
    if not settings.scanner_telegram_bot_token:
        raise RuntimeError("Telegram bot token is not configured.")
    url = (
        f"https://api.telegram.org/bot{settings.scanner_telegram_bot_token}/sendMessage"
    )
    body = {"chat_id": chat_id, "text": text}
    _send_webhook_with_settings(
        settings, url, body, settings.scanner_webhook_timeout_seconds
    )


def _verify_html_file(target_url: str, challenge_value: str) -> bool:
    url = (
        target_url.rstrip("/")
        + f"/.well-known/discoverability-verification-{challenge_value}.txt"
    )
    return challenge_value in _fetch_text(url)


def _verify_meta_tag(target_url: str, challenge_value: str) -> bool:
    content = _fetch_text(target_url)
    expected = f'<meta name="discoverability-verification" content="{challenge_value}"'
    return expected in content


def _verify_dns_txt(target_domain: str, challenge_value: str) -> bool:
    try:
        import dns.resolver  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency presence
        raise HTTPException(
            status_code=500, detail="DNS verification support is unavailable."
        ) from exc
    answers = dns.resolver.resolve(target_domain, "TXT")
    flattened = " ".join(
        "".join(
            part.decode() if isinstance(part, bytes) else str(part)
            for part in answer.strings
        )
        for answer in answers
    )
    return challenge_value in flattened


def _fetch_text(url: str) -> str:
    content, _final_url, _redirect_chain = safe_fetch_url_text(
        url,
        _scanner_runtime_settings(),
        timeout=10,
        headers={"User-Agent": f"Discoverability-Scanner/{APP_VERSION}"},
    )
    return content


def _scanner_runtime_settings() -> Settings:
    from ..config import load_settings

    return load_settings()


def _try_fetch_scanner_text(
    url: str, settings: Settings
) -> tuple[Optional[str], Optional[str]]:
    try:
        content, _final_url, _redirect_chain = safe_fetch_url_text(
            url,
            settings,
            headers={"User-Agent": f"Discoverability-Scanner/{APP_VERSION}"},
        )
        return content, None
    except Exception as exc:
        return None, str(exc)
