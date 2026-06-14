from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def now_utc() -> datetime:
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="owner")
    memberships: Mapped[list["WorkspaceMembership"]] = relationship(
        back_populates="user", foreign_keys="WorkspaceMembership.user_id"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    default_report_language: Mapped[str] = mapped_column(String(8), default="en")
    branding_logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    client_report_title: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    client_report_subtitle: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    client_report_footer: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    owner: Mapped[User] = relationship(back_populates="workspaces")
    memberships: Mapped[list["WorkspaceMembership"]] = relationship(
        back_populates="workspace"
    )
    invites: Mapped[list["WorkspaceInvite"]] = relationship(back_populates="workspace")
    projects: Mapped[list["Project"]] = relationship(back_populates="workspace")
    provider_configs: Mapped[list["ProviderConfiguration"]] = relationship(
        back_populates="workspace"
    )
    prompt_sets: Mapped[list["PromptSet"]] = relationship(back_populates="workspace")
    scheduled_checks: Mapped[list["ScheduledCheck"]] = relationship(
        back_populates="workspace"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="workspace")
    tenant_profiles: Mapped[list["TenantProfile"]] = relationship(
        back_populates="workspace"
    )


class WorkspaceMembership(Base):
    __tablename__ = "workspace_memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(32), default="viewer")
    invited_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="memberships")
    user: Mapped[User] = relationship(
        back_populates="memberships", foreign_keys=[user_id]
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(32), default="client_viewer")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class WorkspaceInvite(Base):
    __tablename__ = "workspace_invites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    email: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="viewer")
    invite_token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    invited_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    sent_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="invites")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    name: Mapped[str] = mapped_column(String(255))
    website_url: Mapped[str] = mapped_column(String(500))
    market: Mapped[str] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(32))
    project_type: Mapped[str] = mapped_column(String(100))
    audit_preset: Mapped[str] = mapped_column(
        String(100), default="global_multilingual"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="projects")
    sites: Mapped[list["Site"]] = relationship(back_populates="project")
    audit_runs: Mapped[list["AuditRun"]] = relationship(back_populates="project")
    reports: Mapped[list["Report"]] = relationship(back_populates="project")
    brand_facts_profiles: Mapped[list["BrandFactsProfile"]] = relationship(
        back_populates="project"
    )
    artifacts: Mapped[list["Artifact"]] = relationship(back_populates="project")
    scheduled_checks: Mapped[list["ScheduledCheck"]] = relationship(
        back_populates="project"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="project")
    integration_connections: Mapped[list["IntegrationConnection"]] = relationship(
        back_populates="project"
    )
    cms_connectors: Mapped[list["CmsConnector"]] = relationship(
        back_populates="project"
    )


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    canonical_url: Mapped[str] = mapped_column(String(500))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    project: Mapped[Project] = relationship(back_populates="sites")


class AuditRun(Base):
    __tablename__ = "audit_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="queued")
    report_language: Mapped[str] = mapped_column(String(8), default="en")
    mode: Mapped[str] = mapped_column(String(32), default="quick")
    market: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    selected_checks_json: Mapped[str] = mapped_column(Text, default="[]")
    provider_names_json: Mapped[str] = mapped_column(Text, default="[]")
    accepted_parameters_json: Mapped[str] = mapped_column(Text, default="{}")
    finding_groups_json: Mapped[str] = mapped_column(Text, default="[]")
    summary_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    project: Mapped[Project] = relationship(back_populates="audit_runs")
    reports: Mapped[list["Report"]] = relationship(back_populates="audit_run")
    artifacts: Mapped[list["Artifact"]] = relationship(back_populates="audit_run")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_run_id: Mapped[int] = mapped_column(ForeignKey("audit_runs.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    language: Mapped[str] = mapped_column(String(8), default="en")
    format: Mapped[str] = mapped_column(String(20), default="markdown")
    summary_markdown: Mapped[str] = mapped_column(Text, default="")
    summary_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    audit_run: Mapped[AuditRun] = relationship(back_populates="reports")
    project: Mapped[Project] = relationship(back_populates="reports")


class ProviderConfiguration(Base):
    __tablename__ = "provider_configurations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    provider_name: Mapped[str] = mapped_column(String(50))
    label: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    api_key_env_var: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    base_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="provider_configs")


class BrandFactsProfile(Base):
    __tablename__ = "brand_facts_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(255))
    facts_markdown: Mapped[str] = mapped_column(Text, default="")
    approved_claims: Mapped[str] = mapped_column(Text, default="")
    forbidden_claims: Mapped[str] = mapped_column(Text, default="")
    numeric_facts_json: Mapped[str] = mapped_column(Text, default="[]")
    markets_json: Mapped[str] = mapped_column(Text, default="[]")
    languages_json: Mapped[str] = mapped_column(Text, default="[]")
    primary_cta: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    project: Mapped[Project] = relationship(back_populates="brand_facts_profiles")


class PromptSet(Base):
    __tablename__ = "prompt_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    purpose: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    output_format: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_recommendation: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    risk_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    prompt_items_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="prompt_sets")


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_run_id: Mapped[int] = mapped_column(ForeignKey("audit_runs.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    artifact_type: Mapped[str] = mapped_column(String(100))
    format: Mapped[str] = mapped_column(String(20), default="markdown")
    file_path: Mapped[str] = mapped_column(String(1000))
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    audit_run: Mapped[AuditRun] = relationship(back_populates="artifacts")
    project: Mapped[Project] = relationship(back_populates="artifacts")


class ScheduledCheck(Base):
    __tablename__ = "scheduled_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[str] = mapped_column(String(50))
    check_type: Mapped[str] = mapped_column(String(100))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    config_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="scheduled_checks")
    project: Mapped[Project] = relationship(back_populates="scheduled_checks")


class IntegrationConnection(Base):
    __tablename__ = "integration_connections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    source_type: Mapped[str] = mapped_column(String(64))
    label: Mapped[str] = mapped_column(String(255))
    property_identifier: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    credentials_env_var: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    config_json: Mapped[str] = mapped_column(Text, default="{}")
    latest_snapshot_json: Mapped[str] = mapped_column(Text, default="{}")
    last_sync_status: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    project: Mapped[Project] = relationship(back_populates="integration_connections")
    sync_events: Mapped[list["IntegrationSyncEvent"]] = relationship(
        back_populates="integration_connection"
    )


class IntegrationSyncEvent(Base):
    __tablename__ = "integration_sync_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    integration_connection_id: Mapped[int] = mapped_column(
        ForeignKey("integration_connections.id"), index=True
    )
    status: Mapped[str] = mapped_column(String(64), default="created")
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    scope_status: Mapped[str] = mapped_column(String(64), default="starter_scope")
    credential_status: Mapped[str] = mapped_column(String(64), default="missing")
    dataset_status: Mapped[str] = mapped_column(String(64), default="contract_only")
    provenance_level: Mapped[str] = mapped_column(String(64), default="starter_sync")
    freshness_label: Mapped[str] = mapped_column(String(64), default="never_synced")
    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    integration_connection: Mapped[IntegrationConnection] = relationship(
        back_populates="sync_events"
    )


class CmsConnector(Base):
    __tablename__ = "cms_connectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    cms_type: Mapped[str] = mapped_column(String(64))
    label: Mapped[str] = mapped_column(String(255))
    base_url: Mapped[str] = mapped_column(String(500))
    auth_env_var: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    writeback_mode: Mapped[str] = mapped_column(String(64), default="read_only")
    last_inventory_json: Mapped[str] = mapped_column(Text, default="{}")
    last_sync_status: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    project: Mapped[Project] = relationship(back_populates="cms_connectors")


class CmsChangeRequest(Base):
    __tablename__ = "cms_change_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    connector_id: Mapped[int] = mapped_column(ForeignKey("cms_connectors.id"))
    requested_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    source_audit_run_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("audit_runs.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(64), default="preview_ready")
    preview_payload_json: Mapped[str] = mapped_column(Text, default="{}")
    approval_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    applied_payload_json: Mapped[str] = mapped_column(Text, default="{}")
    verification_payload_json: Mapped[str] = mapped_column(Text, default="{}")
    rollback_payload_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    applied_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rolled_back_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class NotificationEndpoint(Base):
    __tablename__ = "notification_endpoints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    channel_type: Mapped[str] = mapped_column(String(50))
    label: Mapped[str] = mapped_column(String(255))
    target_url: Mapped[str] = mapped_column(String(1000))
    events_json: Mapped[str] = mapped_column(Text, default="[]")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class TenantProfile(Base):
    __tablename__ = "tenant_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), index=True)
    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organizations.id"), nullable=True
    )
    tenant_name: Mapped[str] = mapped_column(String(255))
    plan_code: Mapped[str] = mapped_column(String(64), default="starter")
    plan_status: Mapped[str] = mapped_column(String(64), default="active")
    quota_json: Mapped[str] = mapped_column(Text, default="{}")
    usage_json: Mapped[str] = mapped_column(Text, default="{}")
    onboarding_state_json: Mapped[str] = mapped_column(Text, default="{}")
    tenant_settings_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    workspace: Mapped[Workspace] = relationship(back_populates="tenant_profiles")


class TenantApiKey(Base):
    __tablename__ = "tenant_api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), index=True)
    label: Mapped[str] = mapped_column(String(255))
    key_prefix: Mapped[str] = mapped_column(String(32), index=True)
    token_hash: Mapped[str] = mapped_column(String(255))
    scopes_json: Mapped[str] = mapped_column(Text, default="[]")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class TrustedDeliveryTarget(Base):
    __tablename__ = "trusted_delivery_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    label: Mapped[str] = mapped_column(String(255))
    repository: Mapped[str] = mapped_column(String(255))
    base_branch: Mapped[str] = mapped_column(String(255), default="main")
    allowed_domains_json: Mapped[str] = mapped_column(Text, default="[]")
    auto_merge_mode: Mapped[str] = mapped_column(String(32), default="disabled")
    required_checks_json: Mapped[str] = mapped_column(Text, default="[]")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class SovRun(Base):
    __tablename__ = "sov_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    brand: Mapped[str] = mapped_column(String(255))
    queries_json: Mapped[str] = mapped_column(Text, default="[]")
    providers_json: Mapped[str] = mapped_column(Text, default="[]")
    results_json: Mapped[str] = mapped_column(Text, default="[]")
    mention_summary: Mapped[str] = mapped_column(Text, default="")
    share_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="completed")
    report_language: Mapped[str] = mapped_column(String(8), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    workspace_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workspaces.id"), nullable=True
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id"), nullable=True
    )
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    user: Mapped[Optional[User]] = relationship(back_populates="audit_logs")
    workspace: Mapped[Optional[Workspace]] = relationship(back_populates="audit_logs")
    project: Mapped[Optional[Project]] = relationship(back_populates="audit_logs")


class EvidenceRecord(Base):
    __tablename__ = "evidence_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    label_type: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text, default="")
    source_ref: Mapped[str] = mapped_column(String(255), default="")
    links_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class ExperimentRecord(Base):
    __tablename__ = "experiment_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    source_type: Mapped[str] = mapped_column(String(64))
    source_id: Mapped[str] = mapped_column(String(128))
    change_summary: Mapped[str] = mapped_column(Text, default="")
    confidence_label: Mapped[str] = mapped_column(String(32), default="weak")
    before_snapshot_json: Mapped[str] = mapped_column(Text, default="{}")
    after_snapshot_json: Mapped[str] = mapped_column(Text, default="{}")
    evidence_links_json: Mapped[str] = mapped_column(Text, default="[]")
    outcome_metrics_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class GeneratedProjectManifest(Base):
    __tablename__ = "generated_project_manifests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workspaces.id"), nullable=True
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id"), nullable=True
    )
    blueprint_type: Mapped[str] = mapped_column(String(128))
    target_mode: Mapped[str] = mapped_column(String(64), default="self_hosted")
    status: Mapped[str] = mapped_column(String(64), default="generated")
    input_json: Mapped[str] = mapped_column(Text, default="{}")
    manifest_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_url: Mapped[str] = mapped_column(String(500))
    target_domain: Mapped[str] = mapped_column(String(255), index=True)
    scan_mode: Mapped[str] = mapped_column(String(32), default="active")
    method: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    actor_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    actor_session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    verification_request_id: Mapped[int] = mapped_column(
        ForeignKey("verification_requests.id")
    )
    token_hash: Mapped[str] = mapped_column(String(255))
    challenge_value: Mapped[str] = mapped_column(String(500))
    method: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_url: Mapped[str] = mapped_column(String(500))
    target_domain: Mapped[str] = mapped_column(String(255), index=True)
    scan_mode: Mapped[str] = mapped_column(String(32))
    consent_scope: Mapped[str] = mapped_column(String(64))
    ownership_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    load_warning_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    limitations_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    actor_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    actor_session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    verification_request_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("verification_requests.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)


class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submitted_url: Mapped[str] = mapped_column(String(500))
    normalized_url: Mapped[str] = mapped_column(String(500))
    target_domain: Mapped[str] = mapped_column(String(255), index=True)
    scan_mode: Mapped[str] = mapped_column(String(32), default="passive")
    status: Mapped[str] = mapped_column(String(32), default="queued")
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    current_stage: Mapped[str] = mapped_column(String(64), default="queued")
    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    report_artifacts_json: Mapped[str] = mapped_column(Text, default="[]")
    requester_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    requester_session_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    requester_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    requester_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    webhook_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    notification_email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    telegram_chat_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verification_request_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("verification_requests.id"), nullable=True
    )
    consent_record_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("consent_records.id"), nullable=True
    )
    cancellation_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ScanJobEvent(Base):
    __tablename__ = "scan_job_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_job_id: Mapped[int] = mapped_column(ForeignKey("scan_jobs.id"), index=True)
    status: Mapped[str] = mapped_column(String(32))
    stage: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
