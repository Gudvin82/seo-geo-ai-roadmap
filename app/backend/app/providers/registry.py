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


class MistralProvider(OpenAIProvider):
    provider_name = "mistral"
    endpoint = "https://api.mistral.ai/v1/chat/completions"


class CohereProvider(JsonHttpProvider):
    provider_name = "cohere"
    endpoint = "https://api.cohere.ai/v2/chat"

    def build_payload(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        return {
            "model": self.model,
            "messages": [
                *(
                    [{"role": "system", "content": system_prompt}]
                    if system_prompt
                    else []
                ),
                {"role": "user", "content": prompt},
            ],
        }

    def build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def parse_content(self, body: dict) -> str:
        message = body.get("message") or {}
        content = message.get("content") or []
        if content and isinstance(content, list):
            first = content[0]
            if isinstance(first, dict):
                return str(first.get("text", ""))
        raise ProviderError("cohere returned an unexpected response shape.")


class DeepSeekProvider(OpenAIProvider):
    provider_name = "deepseek"
    endpoint = "https://api.deepseek.com/chat/completions"


class XAIProvider(OpenAIProvider):
    provider_name = "xai"
    endpoint = "https://api.x.ai/v1/chat/completions"


class OpenRouterProvider(OpenAIProvider):
    provider_name = "openrouter"
    endpoint = "https://openrouter.ai/api/v1/chat/completions"


class GroqProvider(OpenAIProvider):
    provider_name = "groq"
    endpoint = "https://api.groq.com/openai/v1/chat/completions"


class TogetherProvider(OpenAIProvider):
    provider_name = "together"
    endpoint = "https://api.together.xyz/v1/chat/completions"


class FireworksProvider(OpenAIProvider):
    provider_name = "fireworks"
    endpoint = "https://api.fireworks.ai/inference/v1/chat/completions"


class SambaNovaProvider(OpenAIProvider):
    provider_name = "sambanova"
    endpoint = "https://api.sambanova.ai/v1/chat/completions"


class CerebrasProvider(OpenAIProvider):
    provider_name = "cerebras"
    endpoint = "https://api.cerebras.ai/v1/chat/completions"


class NvidiaNIMProvider(OpenAIProvider):
    provider_name = "nvidia_nim"
    endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"


class DeepInfraProvider(OpenAIProvider):
    provider_name = "deepinfra"
    endpoint = "https://api.deepinfra.com/v1/openai/chat/completions"


class AzureOpenAIProvider(OpenAIProvider):
    provider_name = "azure_openai"
    endpoint = "https://example-resource.openai.azure.com/openai/deployments/example/chat/completions?api-version=2024-10-21"


class CloudflareProvider(OpenAIProvider):
    provider_name = "cloudflare"
    endpoint = "https://api.cloudflare.com/client/v4/accounts/example/ai/v1/chat/completions"


class OllamaProvider(OpenAIProvider):
    provider_name = "ollama"
    requires_api_key = False
    endpoint = "http://localhost:11434/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class LocalAIProvider(OpenAIProvider):
    provider_name = "localai"
    requires_api_key = False
    endpoint = "http://localhost:8080/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class VLLMProvider(OpenAIProvider):
    provider_name = "vllm"
    requires_api_key = False
    endpoint = "http://localhost:8001/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class LMStudioProvider(OpenAIProvider):
    provider_name = "lmstudio"
    requires_api_key = False
    endpoint = "http://localhost:1234/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class LlamaCppProvider(OpenAIProvider):
    provider_name = "llamacpp"
    requires_api_key = False
    endpoint = "http://localhost:8080/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class KoboldCppProvider(OpenAIProvider):
    provider_name = "koboldcpp"
    requires_api_key = False
    endpoint = "http://localhost:5001/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class TextGenWebUIProvider(OpenAIProvider):
    provider_name = "textgenwebui"
    requires_api_key = False
    endpoint = "http://localhost:5000/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class TabbyAPIProvider(OpenAIProvider):
    provider_name = "tabbyapi"
    requires_api_key = False
    endpoint = "http://localhost:5000/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class SGLangProvider(OpenAIProvider):
    provider_name = "sglang"
    requires_api_key = False
    endpoint = "http://localhost:30000/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class MistralRSProvider(OpenAIProvider):
    provider_name = "mistralrs"
    requires_api_key = False
    endpoint = "http://localhost:8081/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class AphroditeProvider(OpenAIProvider):
    provider_name = "aphrodite"
    requires_api_key = False
    endpoint = "http://localhost:2242/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class JanProvider(OpenAIProvider):
    provider_name = "jan"
    requires_api_key = False
    endpoint = "http://localhost:1337/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class OpenWebUIProvider(OpenAIProvider):
    provider_name = "openwebui"
    requires_api_key = False
    endpoint = "http://localhost:3000/ollama/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


PROVIDERS: dict[str, type[BaseProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "claude": AnthropicProvider,
    "gemini": GeminiProvider,
    "perplexity": PerplexityProvider,
    "mistral": MistralProvider,
    "cohere": CohereProvider,
    "deepseek": DeepSeekProvider,
    "xai": XAIProvider,
    "grok": XAIProvider,
    "openrouter": OpenRouterProvider,
    "groq": GroqProvider,
    "together": TogetherProvider,
    "fireworks": FireworksProvider,
    "sambanova": SambaNovaProvider,
    "cerebras": CerebrasProvider,
    "nvidia_nim": NvidiaNIMProvider,
    "deepinfra": DeepInfraProvider,
    "azure_openai": AzureOpenAIProvider,
    "cloudflare": CloudflareProvider,
    "ollama": OllamaProvider,
    "localai": LocalAIProvider,
    "vllm": VLLMProvider,
    "lmstudio": LMStudioProvider,
    "llamacpp": LlamaCppProvider,
    "koboldcpp": KoboldCppProvider,
    "textgenwebui": TextGenWebUIProvider,
    "tabbyapi": TabbyAPIProvider,
    "sglang": SGLangProvider,
    "mistralrs": MistralRSProvider,
    "aphrodite": AphroditeProvider,
    "jan": JanProvider,
    "openwebui": OpenWebUIProvider,
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
