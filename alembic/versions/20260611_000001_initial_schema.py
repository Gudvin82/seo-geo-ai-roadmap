"""Initial schema for the self-hosted app layer."""

from __future__ import annotations

import sys
from pathlib import Path

from alembic import op

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.database import Base  # noqa: E402
from app.models import *  # noqa: F401,F403,E402

revision = "20260611_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
