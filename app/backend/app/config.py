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

    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_settings() -> Settings:
    repo_root = get_repo_root()
    data_dir = repo_root / "app" / "backend" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    artifact_root = repo_root / "app" / "backend" / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    return Settings(
        database_url=os.getenv("APP_DATABASE_URL", f"sqlite:///{data_dir / 'discoverability.db'}"),
        secret_key=os.getenv("APP_SECRET_KEY", "dev-secret-key"),
        artifact_root=os.getenv("APP_ARTIFACT_ROOT", str(artifact_root)),
        default_report_language=os.getenv("APP_DEFAULT_REPORT_LANGUAGE", "en"),
        cors_origins=os.getenv("APP_CORS_ORIGINS", "*"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY", ""),
    )
