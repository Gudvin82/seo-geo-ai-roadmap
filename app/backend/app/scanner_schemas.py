from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class PublicScannerConfigRead(BaseModel):
    allow_public_intake: bool
    allow_active_scan: bool
    allow_anonymous_submission: bool
    allow_full_scan: bool
    allowed_schemes: list[str]
    max_url_length: int
    max_concurrent_submissions_per_ip: int
    dangerous_modes_feature_flagged: bool = True
    limitations: list[str]


class VerificationRequestCreate(BaseModel):
    url: str
    scan_mode: Literal["passive", "active", "full"] = "active"
    method: Literal["html_file", "meta_tag", "dns_txt"]


class VerificationRequestRead(BaseModel):
    id: int
    target_url: str
    target_domain: str
    scan_mode: str
    method: str
    status: str
    challenge_value: str
    verification_path: Optional[str] = None
    verification_meta_tag: Optional[str] = None
    verification_dns_name: Optional[str] = None
    created_at: datetime
    verified_at: Optional[datetime]
    expires_at: Optional[datetime]


class ConsentRecordCreate(BaseModel):
    url: str
    scan_mode: Literal["passive", "active", "full"]
    consent_scope: Literal["passive_ack", "active_authorized"]
    ownership_confirmed: bool = False
    load_warning_accepted: bool = False
    limitations_accepted: bool = False
    verification_request_id: Optional[int] = None


class ConsentRecordRead(BaseModel):
    id: int
    target_url: str
    target_domain: str
    scan_mode: str
    consent_scope: str
    ownership_confirmed: bool
    load_warning_accepted: bool
    limitations_accepted: bool
    verification_request_id: Optional[int]
    created_at: datetime


class ScanJobCreate(BaseModel):
    url: str
    scan_mode: Literal["passive", "active", "full"] = "passive"
    consent_record_id: int
    verification_request_id: Optional[int] = None
    callback_webhook_url: Optional[str] = None
    notification_email: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    @field_validator("notification_email")
    @classmethod
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value == "":
            return None
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("A valid notification email is required.")
        return email


class ScanJobRead(BaseModel):
    id: int
    submitted_url: str
    normalized_url: str
    target_domain: str
    scan_mode: str
    status: str
    progress_percent: int
    current_stage: str
    error_summary: Optional[str]
    report_artifacts: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]


class ScanJobEventRead(BaseModel):
    id: int
    scan_job_id: int
    status: str
    stage: str
    message: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ScanArtifactRead(BaseModel):
    kind: str
    format: str
    path: str
    schema_version: str
    download_endpoint: str


class ScanJobAccepted(BaseModel):
    scan_job_id: int
    initial_status: str
    status_endpoint: str
    events_endpoint: str
    artifacts_endpoint: str
