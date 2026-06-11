"""v2.3.0 operator reliability and AI workflow upgrade."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260612_000003"
down_revision = "20260611_000002"
branch_labels = None
depends_on = None


def _table_names(inspector: sa.Inspector) -> set[str]:
    return set(inspector.get_table_names())


def _column_names(inspector: sa.Inspector, table_name: str) -> set[str]:
    return {column["name"] for column in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = _table_names(inspector)

    if "workspaces" in tables:
        workspace_columns = _column_names(inspector, "workspaces")
        if "client_report_footer" not in workspace_columns:
            op.add_column(
                "workspaces",
                sa.Column("client_report_footer", sa.String(length=255), nullable=True),
            )

    if "workspace_invites" in tables:
        invite_columns = _column_names(inspector, "workspace_invites")
        if "expires_at" not in invite_columns:
            op.add_column(
                "workspace_invites",
                sa.Column("expires_at", sa.DateTime(), nullable=True),
            )
        if "revoked_at" not in invite_columns:
            op.add_column(
                "workspace_invites",
                sa.Column("revoked_at", sa.DateTime(), nullable=True),
            )
        if "last_sent_at" not in invite_columns:
            op.add_column(
                "workspace_invites",
                sa.Column("last_sent_at", sa.DateTime(), nullable=True),
            )
        if "sent_count" not in invite_columns:
            op.add_column(
                "workspace_invites",
                sa.Column(
                    "sent_count",
                    sa.Integer(),
                    nullable=False,
                    server_default="1",
                ),
            )
        op.execute(
            "UPDATE workspace_invites SET sent_count = 1 WHERE sent_count IS NULL"
        )

    if "prompt_sets" in tables:
        prompt_columns = _column_names(inspector, "prompt_sets")
        if "purpose" not in prompt_columns:
            op.add_column(
                "prompt_sets",
                sa.Column("purpose", sa.String(length=255), nullable=True),
            )
        if "output_format" not in prompt_columns:
            op.add_column(
                "prompt_sets",
                sa.Column("output_format", sa.String(length=100), nullable=True),
            )
        if "model_recommendation" not in prompt_columns:
            op.add_column(
                "prompt_sets",
                sa.Column(
                    "model_recommendation", sa.String(length=255), nullable=True
                ),
            )
        if "risk_notes" not in prompt_columns:
            op.add_column(
                "prompt_sets",
                sa.Column("risk_notes", sa.Text(), nullable=True),
            )
        if "human_review_required" not in prompt_columns:
            op.add_column(
                "prompt_sets",
                sa.Column(
                    "human_review_required",
                    sa.Boolean(),
                    nullable=False,
                    server_default=sa.true(),
                ),
            )
        op.execute(
            "UPDATE prompt_sets SET human_review_required = 1 "
            "WHERE human_review_required IS NULL"
        )

    if "notification_endpoints" not in tables:
        op.create_table(
            "notification_endpoints",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id")),
            sa.Column("channel_type", sa.String(length=50), nullable=False),
            sa.Column("label", sa.String(length=255), nullable=False),
            sa.Column("target_url", sa.String(length=1000), nullable=False),
            sa.Column("events_json", sa.Text(), nullable=False, server_default="[]"),
            sa.Column(
                "is_enabled", sa.Boolean(), nullable=False, server_default=sa.true()
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False),
        )

    if "sov_runs" not in tables:
        op.create_table(
            "sov_runs",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id")),
            sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
            sa.Column("brand", sa.String(length=255), nullable=False),
            sa.Column("queries_json", sa.Text(), nullable=False, server_default="[]"),
            sa.Column(
                "providers_json", sa.Text(), nullable=False, server_default="[]"
            ),
            sa.Column("results_json", sa.Text(), nullable=False, server_default="[]"),
            sa.Column(
                "mention_summary", sa.Text(), nullable=False, server_default=""
            ),
            sa.Column("share_estimate", sa.Float(), nullable=True),
            sa.Column("notes", sa.Text(), nullable=False, server_default=""),
            sa.Column(
                "status",
                sa.String(length=50),
                nullable=False,
                server_default="completed",
            ),
            sa.Column(
                "report_language",
                sa.String(length=8),
                nullable=False,
                server_default="en",
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("completed_at", sa.DateTime(), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = _table_names(inspector)

    if "sov_runs" in tables:
        op.drop_table("sov_runs")
    if "notification_endpoints" in tables:
        op.drop_table("notification_endpoints")
    if "prompt_sets" in tables:
        prompt_columns = _column_names(inspector, "prompt_sets")
        if "human_review_required" in prompt_columns:
            op.drop_column("prompt_sets", "human_review_required")
        if "risk_notes" in prompt_columns:
            op.drop_column("prompt_sets", "risk_notes")
        if "model_recommendation" in prompt_columns:
            op.drop_column("prompt_sets", "model_recommendation")
        if "output_format" in prompt_columns:
            op.drop_column("prompt_sets", "output_format")
        if "purpose" in prompt_columns:
            op.drop_column("prompt_sets", "purpose")
    if "workspace_invites" in tables:
        invite_columns = _column_names(inspector, "workspace_invites")
        if "sent_count" in invite_columns:
            op.drop_column("workspace_invites", "sent_count")
        if "last_sent_at" in invite_columns:
            op.drop_column("workspace_invites", "last_sent_at")
        if "revoked_at" in invite_columns:
            op.drop_column("workspace_invites", "revoked_at")
        if "expires_at" in invite_columns:
            op.drop_column("workspace_invites", "expires_at")
    if "workspaces" in tables:
        workspace_columns = _column_names(inspector, "workspaces")
        if "client_report_footer" in workspace_columns:
            op.drop_column("workspaces", "client_report_footer")
