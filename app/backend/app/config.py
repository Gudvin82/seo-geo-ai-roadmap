from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    app_name: str = "Discoverability OS App"
    api_prefix: str = "/api/v1"
    database_url: str = ""
    secret_key: str = "dev-secret-key"
    artifact_root: str = ""
    default_report_language: str = "en"
    cors_origins: str = "*"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    perplexity_api_key: str = ""
    token_ttl_minutes: int = 720
    login_attempt_window_seconds: int = 900
    login_attempt_limit: int = 5
    auto_create_schema: bool = True
    allow_active_scan: bool = False
    allow_public_intake: bool = False
    allow_anonymous_submission: bool = False
    allow_full_scan: bool = False
    scanner_allowed_schemes: str = "https,http"
    scanner_max_url_length: int = 2048
    scanner_max_concurrent_submissions_per_ip: int = 3
    scanner_verification_ttl_minutes: int = 30
    scanner_webhook_timeout_seconds: int = 10
    scanner_smtp_host: str = ""
    scanner_smtp_port: int = 587
    scanner_smtp_username: str = ""
    scanner_smtp_password: str = ""
    scanner_smtp_from_email: str = ""
    scanner_telegram_bot_token: str = ""
    scanner_telegram_webhook_secret: str = ""

    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    def scanner_allowed_scheme_list(self) -> list[str]:
        return [
            item.strip().lower()
            for item in self.scanner_allowed_schemes.split(",")
            if item.strip()
        ]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_settings() -> Settings:
    repo_root = get_repo_root()
    data_dir = repo_root / "app" / "backend" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    artifact_root = repo_root / "app" / "backend" / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    return Settings(
        database_url=os.getenv(
            "APP_DATABASE_URL", f"sqlite:///{data_dir / 'discoverability.db'}"
        ),
        secret_key=os.getenv("APP_SECRET_KEY", "dev-secret-key"),
        artifact_root=os.getenv("APP_ARTIFACT_ROOT", str(artifact_root)),
        default_report_language=os.getenv("APP_DEFAULT_REPORT_LANGUAGE", "en"),
        cors_origins=os.getenv("APP_CORS_ORIGINS", "*"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY", ""),
        token_ttl_minutes=int(os.getenv("APP_TOKEN_TTL_MINUTES", "720")),
        login_attempt_window_seconds=int(
            os.getenv("APP_LOGIN_ATTEMPT_WINDOW_SECONDS", "900")
        ),
        login_attempt_limit=int(os.getenv("APP_LOGIN_ATTEMPT_LIMIT", "5")),
        auto_create_schema=os.getenv("APP_AUTO_CREATE_SCHEMA", "true").lower()
        == "true",
        allow_active_scan=os.getenv("ALLOW_ACTIVE_SCAN", "false").lower() == "true",
        allow_public_intake=os.getenv("ALLOW_PUBLIC_INTAKE", "false").lower() == "true",
        allow_anonymous_submission=os.getenv(
            "ALLOW_ANONYMOUS_SUBMISSION", "false"
        ).lower()
        == "true",
        allow_full_scan=os.getenv("ALLOW_FULL_SCAN", "false").lower() == "true",
        scanner_allowed_schemes=os.getenv("SCANNER_ALLOWED_SCHEMES", "https,http"),
        scanner_max_url_length=int(os.getenv("SCANNER_MAX_URL_LENGTH", "2048")),
        scanner_max_concurrent_submissions_per_ip=int(
            os.getenv("SCANNER_MAX_CONCURRENT_SUBMISSIONS_PER_IP", "3")
        ),
        scanner_verification_ttl_minutes=int(
            os.getenv("SCANNER_VERIFICATION_TTL_MINUTES", "30")
        ),
        scanner_webhook_timeout_seconds=int(
            os.getenv("SCANNER_WEBHOOK_TIMEOUT_SECONDS", "10")
        ),
        scanner_smtp_host=os.getenv("SCANNER_SMTP_HOST", ""),
        scanner_smtp_port=int(os.getenv("SCANNER_SMTP_PORT", "587")),
        scanner_smtp_username=os.getenv("SCANNER_SMTP_USERNAME", ""),
        scanner_smtp_password=os.getenv("SCANNER_SMTP_PASSWORD", ""),
        scanner_smtp_from_email=os.getenv("SCANNER_SMTP_FROM_EMAIL", ""),
        scanner_telegram_bot_token=os.getenv("SCANNER_TELEGRAM_BOT_TOKEN", ""),
        scanner_telegram_webhook_secret=os.getenv(
            "SCANNER_TELEGRAM_WEBHOOK_SECRET", ""
        ),
    )
