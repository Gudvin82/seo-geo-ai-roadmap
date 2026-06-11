from __future__ import annotations

import json
import urllib.error
import urllib.request

from sqlalchemy.orm import Session

from ..metrics import NOTIFICATION_DELIVERIES
from ..models import NotificationEndpoint


def _payload_for_channel(
    channel_type: str,
    event_type: str,
    summary: str,
    metadata: dict,
) -> dict:
    if channel_type == "slack":
        return {"text": f"[{event_type}] {summary}", "metadata": metadata}
    if channel_type == "telegram":
        return {"text": f"[{event_type}] {summary}", "metadata": metadata}
    return {"event_type": event_type, "summary": summary, "metadata": metadata}


def notify_workspace(
    db: Session,
    workspace_id: int,
    event_type: str,
    summary: str,
    metadata: dict | None = None,
) -> None:
    rows = (
        db.query(NotificationEndpoint)
        .filter(
            NotificationEndpoint.workspace_id == workspace_id,
            NotificationEndpoint.is_enabled.is_(True),
        )
        .all()
    )
    for row in rows:
        events = json.loads(row.events_json or "[]")
        if events and event_type not in events:
            continue
        payload = _payload_for_channel(
            row.channel_type, event_type, summary, metadata or {}
        )
        request = urllib.request.Request(
            row.target_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=10):
                NOTIFICATION_DELIVERIES.labels(
                    channel=row.channel_type, status="success"
                ).inc()
        except (urllib.error.URLError, urllib.error.HTTPError):
            NOTIFICATION_DELIVERIES.labels(
                channel=row.channel_type, status="failure"
            ).inc()
