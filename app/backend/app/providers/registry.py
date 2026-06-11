from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Optional

from .base import BaseProvider, ProviderError, ProviderResponse


class JsonHttpProvider(BaseProvider):
    endpoint = ""
    provider_name = "generic"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        raise NotImplementedError

    def build_headers(self) -> dict[str, str]:
        raise NotImplementedError

    def parse_content(self, body: dict) -> str:
        raise NotImplementedError

    def generate_text(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> ProviderResponse:
        self.ensure_configured()
        payload = json.dumps(self.build_payload(prompt, system_prompt)).encode("utf-8")
        request = urllib.request.Request(
            self.base_url or self.endpoint,
            data=payload,
            headers=self.build_headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise ProviderError(
                f"{self.provider_name} quota or auth error: {exc}"
            ) from exc
        except urllib.error.URLError as exc:
            raise ProviderError(
                f"{self.provider_name} timeout or network error: {exc}"
            ) from exc
        content = self.parse_content(body)
        return ProviderResponse(
            provider=self.provider_name,
            model=self.model,
            status="ok",
            content=content,
            raw=body,
        )


class OpenAIProvider(JsonHttpProvider):
    provider_name = "openai"
    endpoint = "https://api.openai.com/v1/chat/completions"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return {"model": self.model, "messages": messages}

    def build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def parse_content(self, body: dict) -> str:
        return body["choices"][0]["message"]["content"]


class AnthropicProvider(JsonHttpProvider):
    provider_name = "anthropic"
    endpoint = "https://api.anthropic.com/v1/messages"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        payload = {
            "model": self.model,
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            payload["system"] = system_prompt
        return payload

    def build_headers(self) -> dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    def parse_content(self, body: dict) -> str:
        return body["content"][0]["text"]


class GeminiProvider(JsonHttpProvider):
    provider_name = "gemini"
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        content = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"
        return {"contents": [{"parts": [{"text": content}]}]}

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def generate_text(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> ProviderResponse:
        self.ensure_configured()
        self.base_url = (
            self.base_url
            or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        )
        return super().generate_text(prompt, system_prompt)

    def parse_content(self, body: dict) -> str:
        return body["candidates"][0]["content"]["parts"][0]["text"]


class PerplexityProvider(JsonHttpProvider):
    provider_name = "perplexity"
    endpoint = "https://api.perplexity.ai/chat/completions"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return {"model": self.model, "messages": messages}

    def build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def parse_content(self, body: dict) -> str:
        return body["choices"][0]["message"]["content"]


PROVIDERS: dict[str, type[BaseProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "claude": AnthropicProvider,
    "gemini": GeminiProvider,
    "perplexity": PerplexityProvider,
}


def build_provider(
    provider_name: str,
    api_key: Optional[str],
    model: str,
    base_url: Optional[str] = None,
) -> BaseProvider:
    provider_cls = PROVIDERS.get(provider_name.lower())
    if not provider_cls:
        raise ProviderError(f"Unsupported provider: {provider_name}")
    return provider_cls(api_key=api_key, model=model, base_url=base_url)
