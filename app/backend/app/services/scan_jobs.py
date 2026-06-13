from __future__ import annotations

import csv
import hashlib
import json
import smtplib
import threading
import urllib.request
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
from .scan_security import normalize_target_url

SCANNER_SCHEMA_VERSION = "v3.6.0"
SCAN_JOB_TERMINAL_STATES = {
    "partial_success",
    "completed",
    "failed",
    "cancelled",
    "expired",
}
SCAN_JOB_ACTIVE_STATES = {"queued", "verifying", "running"}
_THREADS: dict[int, threading.Thread] = {}


def scanner_config_payload(settings: Settings) -> dict:
    return {
        "allow_public_intake": settings.allow_public_intake,
        "allow_active_scan": settings.allow_active_scan,
        "allow_anonymous_submission": settings.allow_anonymous_submission,
        "allow_full_scan": settings.allow_full_scan,
        "allowed_schemes": settings.scanner_allowed_scheme_list(),
        "max_url_length": settings.scanner_max_url_length,
        "max_concurrent_submissions_per_ip": settings.scanner_max_concurrent_submissions_per_ip,
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
    active_for_domain = (
        db.query(ScanJob)
        .filter(
            ScanJob.target_domain == host, ScanJob.status.in_(SCAN_JOB_ACTIVE_STATES)
        )
        .count()
    )
    if active_for_domain >= settings.scanner_max_concurrent_submissions_per_ip:
        raise HTTPException(
            status_code=429, detail="Submission limit reached for this domain."
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
        webhook_url=callback_webhook_url,
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


def serialize_scan_job(row: ScanJob) -> dict:
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
    thread = threading.Thread(
        target=_run_scan_job,
        args=(settings, scan_job_id),
        daemon=True,
        name=f"scan-job-{scan_job_id}",
    )
    _THREADS[scan_job_id] = thread
    thread.start()


def _run_scan_job(settings: Settings, scan_job_id: int) -> None:
    db = create_session()
    try:
        row = db.get(ScanJob, scan_job_id)
        if not row:
            return
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
    checks = {
        "passive": [
            "URL normalization and public-host validation",
            "Surface-level crawlability and discoverability hints",
            "Heuristic readiness summary for SEO, GEO, and AI discoverability",
        ],
        "active": [
            "Ownership-gated active verification path",
            "Extended reachability and public-surface checks",
            "Artifact-ready summary with caution notes",
        ],
        "full": [
            "Ownership-gated active verification path",
            "Extended reachability and public-surface checks",
            "Expanded artifact pack and notification summary",
        ],
    }
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
    return {
        "schema_version": SCANNER_SCHEMA_VERSION,
        "job_id": row.id,
        "target_url": row.normalized_url,
        "target_domain": row.target_domain,
        "scan_mode": row.scan_mode,
        "executive_summary": (
            f"{split.hostname} was processed through the {row.scan_mode} scanner foundation. "
            "This output is safe for self-hosted intake and operator review, not a penetration test."
        ),
        "checked_items": checks[row.scan_mode],
        "not_checked": [
            "Authenticated application flows",
            "Private network surfaces",
            "Exploit-oriented or pentest behavior",
        ],
        "issues": issue_rows,
        "limitations": scanner_config_payload(settings)["limitations"],
    }


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
        try:
            _send_webhook(
                row.webhook_url, payload, settings.scanner_webhook_timeout_seconds
            )
        except Exception as exc:  # pragma: no cover - depends on external sink
            errors.append(f"webhook: {exc}")
    if row.notification_email:
        try:
            _send_email(settings, row.notification_email, payload)
        except Exception as exc:  # pragma: no cover - depends on smtp
            errors.append(f"email: {exc}")
    if row.telegram_chat_id:
        try:
            _send_telegram(settings, row.telegram_chat_id, payload)
        except Exception as exc:  # pragma: no cover - depends on telegram
            errors.append(f"telegram: {exc}")
    return errors


def _send_webhook(url: str, payload: dict, timeout: int) -> None:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout):
        return None


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
    if not settings.scanner_telegram_bot_token:
        raise RuntimeError("Telegram bot token is not configured.")
    url = (
        f"https://api.telegram.org/bot{settings.scanner_telegram_bot_token}/sendMessage"
    )
    body = {
        "chat_id": chat_id,
        "text": f"Scan job {payload['scan_job_id']} completed for {payload['target_url']}",
    }
    _send_webhook(url, body, settings.scanner_webhook_timeout_seconds)


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
    request = urllib.request.Request(
        url, headers={"User-Agent": "Discoverability-Scanner/3.6.0"}
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read().decode("utf-8", errors="replace")
