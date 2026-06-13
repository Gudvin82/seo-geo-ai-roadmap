from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from ..config import Settings
from ..database import get_db
from ..schemas import TelegramWebhookRead
from ..services.scan_jobs import _send_telegram_text
from ..services.telegram_runtime import process_telegram_update

router = APIRouter(prefix="/telegram", tags=["telegram"])


def _settings_from_request(request: Request) -> Settings:
    return request.app.state.settings


@router.post("/webhook", response_model=TelegramWebhookRead)
async def telegram_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_telegram_bot_api_secret_token: Optional[str] = Header(
        default=None, alias="X-Telegram-Bot-Api-Secret-Token"
    ),
) -> TelegramWebhookRead:
    settings = _settings_from_request(request)
    if (
        settings.scanner_telegram_webhook_secret
        and x_telegram_bot_api_secret_token != settings.scanner_telegram_webhook_secret
    ):
        raise HTTPException(status_code=403, detail="Invalid Telegram webhook secret.")

    payload = await request.json()
    result = process_telegram_update(db, settings, payload)

    chat_id = payload.get("message", {}).get("chat", {}).get("id") or payload.get(
        "edited_message", {}
    ).get("chat", {}).get("id")
    if chat_id is not None and settings.scanner_telegram_bot_token:
        _send_telegram_text(settings, str(chat_id), result["message"])

    return TelegramWebhookRead(
        action=result["action"],
        message=result["message"],
        scan_job_id=result.get("scan_job_id"),
    )
