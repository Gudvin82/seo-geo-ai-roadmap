from __future__ import annotations

import pytest
from app.providers.base import ProviderError
from app.providers.registry import PROVIDERS, build_provider


def test_provider_registry_contains_required_providers() -> None:
    for name in ("openai", "anthropic", "gemini", "perplexity"):
        assert name in PROVIDERS


def test_missing_key_raises_provider_error() -> None:
    provider = build_provider("openai", api_key="", model="gpt-4o-mini")
    with pytest.raises(ProviderError):
        provider.generate_text("hello")
