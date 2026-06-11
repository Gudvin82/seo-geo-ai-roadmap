from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    expires_in_seconds: int


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=12)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("A valid email address is required.")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        has_upper = any(ch.isupper() for ch in value)
        has_lower = any(ch.islower() for ch in value)
        has_digit = any(ch.isdigit() for ch in value)
        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "Password must include uppercase, lowercase, and numeric characters."
            )
        return value


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


class WorkspaceMembershipRead(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: str
    created_at: datetime


class WorkspaceInviteCreate(BaseModel):
    email: str
    role: str = "viewer"

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        allowed = {"owner", "admin", "editor", "viewer"}
        role = value.strip().lower()
        if role not in allowed:
            raise ValueError(
                f"Unsupported role '{value}'. Allowed: {', '.join(sorted(allowed))}."
            )
        return role


class WorkspaceInviteAccept(BaseModel):
    invite_token: str


class WorkspaceInviteRead(BaseModel):
    id: int
    workspace_id: int
    email: str
    role: str
    invite_token: str
    status: str
    accepted_at: Optional[datetime]
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

    @field_validator("provider_name")
    @classmethod
    def validate_provider_name(cls, value: str) -> str:
        provider = value.strip().lower()
        allowed = {
            "openai",
            "anthropic",
            "gemini",
            "perplexity",
            "ollama",
            "localai",
            "vllm",
        }
        if provider not in allowed:
            raise ValueError(
                f"Unsupported provider '{value}'. Allowed: {', '.join(sorted(allowed))}."
            )
        return provider


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


class AuditRunRequest(BaseModel):
    workspace_id: int
    project_id: int
    domain_or_url: str
    selected_checks: list[str] = Field(default_factory=list)
    selected_providers: list[str] = Field(default_factory=list)
    report_language: str = "en"
    market: Optional[str] = None
    mode: Literal["quick", "full"] = "quick"
    brand_facts_profile_id: Optional[int] = None


class AuditRunAccepted(BaseModel):
    audit_job_id: int
    initial_status: str
    accepted_parameters: dict[str, Any]
    status_endpoint: str
    report_endpoint: str
    artifacts_endpoint: str


class AuditRunRead(BaseModel):
    id: int
    project_id: int
    workspace_id: int
    status: str
    report_language: str
    mode: str
    market: Optional[str]
    target_url: Optional[str]
    selected_checks: list[str]
    selected_providers: list[str] = Field(default_factory=list)
    accepted_parameters: dict[str, Any] = Field(default_factory=dict)
    finding_groups: list[dict[str, Any]]
    summary_score: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]


class AuditLogRead(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int]
    workspace_id: Optional[int]
    project_id: Optional[int]
    metadata: dict[str, Any]
    created_at: datetime


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


class SovCheckRequest(BaseModel):
    brand: str
    queries: list[str]
    providers: list[str] = Field(default_factory=list)
    market: Optional[str] = None
    language: Optional[str] = None
