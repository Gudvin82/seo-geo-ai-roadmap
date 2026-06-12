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
    client_report_footer: Optional[str] = None


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    default_report_language: Optional[str] = None
    branding_logo_url: Optional[str] = None
    client_report_title: Optional[str] = None
    client_report_subtitle: Optional[str] = None
    client_report_footer: Optional[str] = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    slug: str
    default_report_language: str
    branding_logo_url: Optional[str]
    client_report_title: Optional[str]
    client_report_subtitle: Optional[str]
    client_report_footer: Optional[str]
    created_at: datetime


class WorkspaceMembershipRead(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: str
    created_at: datetime


class WorkspaceMembershipUpdate(BaseModel):
    role: str

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


class WorkspaceInviteCreate(BaseModel):
    email: str
    role: str = "viewer"
    expires_in_days: int = 7

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
    expires_at: Optional[datetime]
    accepted_at: Optional[datetime]
    revoked_at: Optional[datetime]
    last_sent_at: Optional[datetime]
    sent_count: int
    created_at: datetime


class WorkspaceInviteUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: Optional[str]) -> Optional[str]:
        return value.strip().lower() if value is not None else value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"owner", "admin", "editor", "viewer"}
        role = value.strip().lower()
        if role not in allowed:
            raise ValueError(
                f"Unsupported role '{value}'. Allowed: {', '.join(sorted(allowed))}."
            )
        return role


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


class ProviderConfigUpdate(BaseModel):
    label: Optional[str] = None
    model: Optional[str] = None
    api_key_env_var: Optional[str] = None
    base_url: Optional[str] = None
    is_enabled: Optional[bool] = None


class IntegrationConnectionCreate(BaseModel):
    workspace_id: int
    project_id: int
    source_type: str
    label: str
    property_identifier: Optional[str] = None
    credentials_env_var: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source_type")
    @classmethod
    def validate_source_type(cls, value: str) -> str:
        source = value.strip().lower()
        allowed = {"gsc", "ga4", "yandex_webmaster", "yandex_metrica"}
        if source not in allowed:
            raise ValueError(
                f"Unsupported source_type '{value}'. Allowed: {', '.join(sorted(allowed))}."
            )
        return source


class IntegrationConnectionRead(BaseModel):
    id: int
    workspace_id: int
    project_id: int
    source_type: str
    label: str
    property_identifier: Optional[str]
    credentials_env_var: Optional[str]
    config: dict[str, Any]
    latest_snapshot: dict[str, Any]
    last_sync_status: Optional[str]
    last_sync_at: Optional[datetime]
    created_at: datetime


class CmsConnectorCreate(BaseModel):
    workspace_id: int
    project_id: int
    cms_type: str
    label: str
    base_url: str
    auth_env_var: Optional[str] = None
    writeback_mode: Literal["read_only", "draft", "human_approved_publish"] = (
        "read_only"
    )

    @field_validator("cms_type")
    @classmethod
    def validate_cms_type(cls, value: str) -> str:
        cms_type = value.strip().lower()
        allowed = {"wordpress", "tilda", "bitrix", "webflow"}
        if cms_type not in allowed:
            raise ValueError(
                f"Unsupported cms_type '{value}'. Allowed: {', '.join(sorted(allowed))}."
            )
        return cms_type


class CmsConnectorRead(BaseModel):
    id: int
    workspace_id: int
    project_id: int
    cms_type: str
    label: str
    base_url: str
    auth_env_var: Optional[str]
    writeback_mode: str
    last_inventory: dict[str, Any]
    last_sync_status: Optional[str]
    last_sync_at: Optional[datetime]
    allowed_actions: list[str] = Field(default_factory=list)
    risky_actions: list[str] = Field(default_factory=list)
    unsupported_actions: list[str] = Field(default_factory=list)
    retry_policy: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class CmsWritebackAttemptRead(BaseModel):
    connector_id: int
    project_id: int
    workspace_id: int
    writeback_mode: str
    status: Literal[
        "blocked",
        "queued",
        "retrying",
        "failed",
        "dead",
        "completed",
        "awaiting_human_approval",
    ]
    summary: str
    next_step: str
    retry_policy: dict[str, Any] = Field(default_factory=dict)
    attempts: int
    artifact_preview: dict[str, Any] = Field(default_factory=dict)


class PatchPackRequest(BaseModel):
    project_id: int
    workspace_id: int
    audit_run_id: Optional[int] = None
    report_language: str = "en"
    mode: Literal["read_only", "draft", "human_approved_publish"] = "draft"
    audience: Literal["agency", "in_house", "founder"] = "agency"


class PatchPackRead(BaseModel):
    project_id: int
    workspace_id: int
    report_language: str
    audience: str
    review_mode: str
    outputs: dict[str, Any]


class ProjectImportRequest(BaseModel):
    workspace_id: int
    payload: dict[str, Any]


class ProjectImportRead(BaseModel):
    project_id: int
    imported_sections: list[str]
    message: str


class LlmsValidatorRequest(BaseModel):
    url: Optional[str] = None
    content: Optional[str] = None


class LlmsValidatorResponse(BaseModel):
    is_valid: bool
    line_count: int
    checked_source: str
    warnings: list[str]
    recommendations: list[str]
    observed_facts: list[str]


class PromptSetCreate(BaseModel):
    workspace_id: int
    name: str
    description: Optional[str] = None
    purpose: Optional[str] = None
    output_format: Optional[str] = None
    model_recommendation: Optional[str] = None
    risk_notes: Optional[str] = None
    human_review_required: bool = True
    prompt_items: list[str] = Field(default_factory=list)


class PromptSetRead(BaseModel):
    id: int
    workspace_id: int
    name: str
    description: Optional[str]
    purpose: Optional[str]
    output_format: Optional[str]
    model_recommendation: Optional[str]
    risk_notes: Optional[str]
    human_review_required: bool
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
    schedule_mode: str
    execution_path: str
    next_run_hint: str
    last_status: str
    limitations: list[str] = Field(default_factory=list)
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
    workspace_id: int
    project_id: int
    market: Optional[str] = None
    language: Optional[str] = None
    notes: Optional[str] = None


class SovRunRead(BaseModel):
    id: int
    workspace_id: int
    project_id: int
    brand: str
    queries: list[str]
    providers: list[str]
    results: list[dict[str, Any]]
    mention_summary: str
    share_estimate: Optional[float]
    notes: str
    status: str
    report_language: str
    created_at: datetime
    completed_at: Optional[datetime]


class NotificationEndpointCreate(BaseModel):
    workspace_id: int
    channel_type: str
    label: str
    target_url: str
    events: list[str] = Field(default_factory=list)
    is_enabled: bool = True


class NotificationEndpointRead(BaseModel):
    id: int
    workspace_id: int
    channel_type: str
    label: str
    target_url: str
    events: list[str]
    is_enabled: bool
    retry_policy: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class FactDriftSurface(BaseModel):
    name: str
    content: str


class FactDriftRequest(BaseModel):
    surfaces: list[FactDriftSurface] = Field(default_factory=list)


class FactDriftItemRead(BaseModel):
    drift_type: str
    severity: str
    observed: str
    inferred_issue: str
    recommended_next_step: str


class FactDriftResponse(BaseModel):
    status: str
    surface_count: int
    drift_items: list[FactDriftItemRead]
    detected_types: list[str]
    limitations: list[str]
