"""Operator-ready schema upgrade for v2.2.0."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260611_000002"
down_revision = "20260611_000001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "audit_runs", sa.Column("mode", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "audit_runs", sa.Column("market", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "audit_runs", sa.Column("target_url", sa.String(length=500), nullable=True)
    )
    op.add_column(
        "audit_runs",
        sa.Column("provider_names_json", sa.Text(), nullable=True, server_default="[]"),
    )
    op.add_column(
        "audit_runs",
        sa.Column(
            "accepted_parameters_json", sa.Text(), nullable=True, server_default="{}"
        ),
    )
    op.execute("UPDATE audit_runs SET mode = 'quick' WHERE mode IS NULL")
    op.execute(
        "UPDATE audit_runs SET provider_names_json = '[]' WHERE provider_names_json IS NULL"
    )
    op.execute(
        "UPDATE audit_runs SET accepted_parameters_json = '{}' WHERE accepted_parameters_json IS NULL"
    )

    op.create_table(
        "workspace_memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id")),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="viewer"),
        sa.Column("invited_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "workspace_invites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id")),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="viewer"),
        sa.Column("invite_token", sa.String(length=255), nullable=False),
        sa.Column("invited_by_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_workspace_invites_invite_token",
        "workspace_invites",
        ["invite_token"],
        unique=True,
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.execute(
        """
        INSERT INTO workspace_memberships (workspace_id, user_id, role, created_at)
        SELECT id, owner_user_id, 'owner', CURRENT_TIMESTAMP
        FROM workspaces
        """
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_index("ix_workspace_invites_invite_token", table_name="workspace_invites")
    op.drop_table("workspace_invites")
    op.drop_table("workspace_memberships")
    op.drop_column("audit_runs", "accepted_parameters_json")
    op.drop_column("audit_runs", "provider_names_json")
    op.drop_column("audit_runs", "target_url")
    op.drop_column("audit_runs", "market")
    op.drop_column("audit_runs", "mode")
