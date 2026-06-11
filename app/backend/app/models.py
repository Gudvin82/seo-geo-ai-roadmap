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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)

    owner: Mapped[User] = relationship(back_populates="workspaces")
    projects: Mapped[list["Project"]] = relationship(back_populates="workspace")
    provider_configs: Mapped[list["ProviderConfiguration"]] = relationship(
        back_populates="workspace"
    )
    prompt_sets: Mapped[list["PromptSet"]] = relationship(back_populates="workspace")
    scheduled_checks: Mapped[list["ScheduledCheck"]] = relationship(
        back_populates="workspace"
    )


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
    selected_checks_json: Mapped[str] = mapped_column(Text, default="[]")
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
