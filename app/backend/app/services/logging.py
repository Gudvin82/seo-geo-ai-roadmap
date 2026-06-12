from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

LOGGER = logging.getLogger("discoverability")

if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def log_event(event_type: str, **payload: Any) -> None:
    LOGGER.info(
        json.dumps(
            {
                "ts": f"{datetime.utcnow().isoformat()}Z",
                "event_type": event_type,
                **payload,
            },
            ensure_ascii=False,
        )
    )
