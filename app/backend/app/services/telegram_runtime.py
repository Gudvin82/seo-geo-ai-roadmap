from __future__ import annotations

import json
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..config import Settings
from ..models import AuditRun, Project
from .scan_jobs import create_consent_record, create_scan_job
from .scan_security import normalize_public_url


def process_telegram_update(
    db: Session, settings: Settings, update: dict[str, Any]
) -> dict[str, Any]:
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()
    if not chat_id:
        raise HTTPException(status_code=400, detail="Telegram chat id is required.")

    if not text or text in {"/start", "/help", "/geo help"}:
        return {
            "action": "help",
            "message": (
                "SEO GEO AI bot commands:\n"
                "/geo audit https://example.com\n"
                "/geo latest PROJECT_ID\n"
                "/geo alerts PROJECT_ID"
            ),
        }

    if text.startswith("/geo audit "):
        target_url = text.replace("/geo audit ", "", 1).strip()
        normalized = normalize_public_url(target_url, settings)
        consent = create_consent_record(
            db,
            settings,
            url=normalized,
            scan_mode="passive",
            consent_scope="telegram_passive_ack",
            ownership_confirmed=False,
            load_warning_accepted=False,
            limitations_accepted=True,
            verification_request_id=None,
            current_user=None,
            session_id=f"telegram:{chat_id}",
            source_ip="telegram",
            user_agent="telegram-bot",
        )
        row = create_scan_job(
            db,
            settings,
            url=normalized,
            scan_mode="passive",
            consent_record_id=consent.id,
            verification_request_id=None,
            callback_webhook_url=None,
            notification_email=None,
            telegram_chat_id=str(chat_id),
            current_user=None,
            session_id=f"telegram:{chat_id}",
            source_ip="telegram",
            user_agent="telegram-bot",
        )
        return {
            "action": "audit",
            "scan_job_id": row.id,
            "message": (
                f"Passive audit queued for {normalized}\n"
                f"scan_job_id: {row.id}\n"
                f"status: /api/v1/scan-jobs/{row.id}\n"
                f"result: /api/v1/scan-jobs/{row.id}/result"
            ),
        }

    if text.startswith("/geo latest "):
        project_id = int(text.replace("/geo latest ", "", 1).strip())
        project = db.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")
        audit_run = (
            db.query(AuditRun)
            .filter(AuditRun.project_id == project.id)
            .order_by(AuditRun.id.desc())
            .first()
        )
        if not audit_run:
            return {
                "action": "latest",
                "message": f"No audit runs found for project #{project.id}.",
            }
        return {
            "action": "latest",
            "message": (
                f"Latest audit for {project.name}\n"
                f"status: {audit_run.status}\n"
                f"score: {audit_run.summary_score or 0}\n"
                f"report language: {audit_run.report_language}"
            ),
        }

    if text.startswith("/geo alerts "):
        project_id = int(text.replace("/geo alerts ", "", 1).strip())
        return {
            "action": "alerts",
            "message": (
                f"Alerts are operator-governed for project #{project_id}. "
                "Connect webhook, email, or Telegram notification endpoints in the app."
            ),
        }

    raise HTTPException(status_code=400, detail="Unsupported Telegram command.")


def telegram_send_message_payload(
    *, chat_id: str | int, text: str, parse_mode: Optional[str] = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    return payload


def telegram_webhook_preview(update: dict[str, Any]) -> str:
    return json.dumps(update, ensure_ascii=False, indent=2)
