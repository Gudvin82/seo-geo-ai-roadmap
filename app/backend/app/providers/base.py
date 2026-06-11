from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class ProviderError(Exception):
    """Raised when provider orchestration fails."""


@dataclass
class ProviderResponse:
    provider: str
    model: str
    status: str
    content: str
    raw: dict


class BaseProvider:
    provider_name = "base"

    def __init__(
        self, api_key: Optional[str], model: str, base_url: Optional[str] = None
    ):
        self.api_key = api_key or ""
        self.model = model
        self.base_url = base_url

    def ensure_configured(self) -> None:
        if not self.api_key:
            raise ProviderError(f"Missing API key for provider {self.provider_name}.")

    def generate_text(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> ProviderResponse:
        raise NotImplementedError
