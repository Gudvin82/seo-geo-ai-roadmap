from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("A valid email address is required.")
        return email


class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class WorkspaceCreate(BaseModel):
    name: str
    slug: str
    default_report_language: str = "en"
    branding_logo_url: Optional[str] = None
    client_report_title: Optional[str] = None
    client_report_subtitle: Optional[str] = None


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    default_report_language: Optional[str] = None
    branding_logo_url: Optional[str] = None
    client_report_title: Optional[str] = None
    client_report_subtitle: Optional[str] = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    slug: str
    default_report_language: str
    branding_logo_url: Optional[str]
    client_report_title: Optional[str]
    client_report_subtitle: Optional[str]
    created_at: datetime


class ProjectCreate(BaseModel):
    workspace_id: int
    name: str
    website_url: str
    market: str
    language: str
    project_type: str
    audit_preset: str = "global_multilingual"


class ProjectRead(BaseModel):
    id: int
    workspace_id: int
    name: str
    website_url: str
    market: str
    language: str
    project_type: str
    audit_preset: str
    created_at: datetime


class SiteCreate(BaseModel):
    project_id: int
    canonical_url: str
    notes: Optional[str] = None


class SiteRead(BaseModel):
    id: int
    project_id: int
    canonical_url: str
    notes: Optional[str]
    created_at: datetime


class BrandFactsCreate(BaseModel):
    project_id: int
    name: str
    facts_markdown: str
    approved_claims: str = ""
    forbidden_claims: str = ""
    numeric_facts: list[str] = Field(default_factory=list)
    markets: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    primary_cta: Optional[str] = None


class BrandFactsRead(BaseModel):
    id: int
    project_id: int
    name: str
    facts_markdown: str
    approved_claims: str
    forbidden_claims: str
    numeric_facts: list[str]
    markets: list[str]
    languages: list[str]
    primary_cta: Optional[str]
    created_at: datetime


class ProviderConfigCreate(BaseModel):
    workspace_id: int
    provider_name: str
    label: str
    model: str
    api_key_env_var: Optional[str] = None
    base_url: Optional[str] = None
    is_enabled: bool = True


class ProviderConfigRead(BaseModel):
    id: int
    workspace_id: int
    provider_name: str
    label: str
    model: str
    api_key_env_var: Optional[str]
    base_url: Optional[str]
    is_enabled: bool
    created_at: datetime


class PromptSetCreate(BaseModel):
    workspace_id: int
    name: str
    description: Optional[str] = None
    prompt_items: list[str] = Field(default_factory=list)


class PromptSetRead(BaseModel):
    id: int
    workspace_id: int
    name: str
    description: Optional[str]
    prompt_items: list[str]
    created_at: datetime


class ScheduledCheckCreate(BaseModel):
    workspace_id: int
    project_id: int
    name: str
    frequency: str
    check_type: str
    is_enabled: bool = True
    config: dict[str, Any] = Field(default_factory=dict)


class ScheduledCheckRead(BaseModel):
    id: int
    workspace_id: int
    project_id: int
    name: str
    frequency: str
    check_type: str
    is_enabled: bool
    last_run_at: Optional[datetime]
    config: dict[str, Any]
    created_at: datetime


class AuditRunCreate(BaseModel):
    project_id: int
    workspace_id: int
    report_language: str = "en"
    selected_checks: list[str]
    provider_config_id: Optional[int] = None
    prompt_set_id: Optional[int] = None


class AuditRunRead(BaseModel):
    id: int
    project_id: int
    workspace_id: int
    status: str
    report_language: str
    selected_checks: list[str]
    finding_groups: list[dict[str, Any]]
    summary_score: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]


class ReportRead(BaseModel):
    id: int
    audit_run_id: int
    project_id: int
    language: str
    format: str
    summary_markdown: str
    summary_json: dict[str, Any]
    created_at: datetime


class ArtifactRead(BaseModel):
    id: int
    audit_run_id: int
    project_id: int
    artifact_type: str
    format: str
    file_path: str
    metadata: dict[str, Any]
    created_at: datetime


class ApiMessage(BaseModel):
    message: str
