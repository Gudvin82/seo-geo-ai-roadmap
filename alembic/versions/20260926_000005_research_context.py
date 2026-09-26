"""Persist reusable project research context."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260926_000005"
down_revision = "20260914_000004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if "project_research_contexts" in sa.inspect(bind).get_table_names():
        return
    op.create_table(
        "project_research_contexts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("competitors_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("goals_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("key_pages_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("seed_keywords_json", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("project_id", name="uq_project_research_context_project"),
    )
    op.create_index(
        "ix_project_research_contexts_project_id",
        "project_research_contexts",
        ["project_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_project_research_contexts_project_id",
        table_name="project_research_contexts",
    )
    op.drop_table("project_research_contexts")
