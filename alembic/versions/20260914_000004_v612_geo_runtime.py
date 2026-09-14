"""v6.12 GEO runtime evidence and AI visibility history."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260914_000004"
down_revision = "20260612_000003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if "ai_visibility_snapshots" in sa.inspect(bind).get_table_names():
        return
    op.create_table(
        "ai_visibility_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("target_url", sa.String(length=2048), nullable=False),
        sa.Column("query", sa.String(length=1000), nullable=False),
        sa.Column("query_set", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=128), nullable=False),
        sa.Column("model", sa.String(length=255), nullable=False),
        sa.Column("evidence_type", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("response_reference", sa.String(length=2048), nullable=False, server_default=""),
        sa.Column("evidence_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("snapshot_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_ai_visibility_snapshots_project_id", "ai_visibility_snapshots", ["project_id"])


def downgrade() -> None:
    op.drop_index("ix_ai_visibility_snapshots_project_id", table_name="ai_visibility_snapshots")
    op.drop_table("ai_visibility_snapshots")
