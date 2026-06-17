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
    endpoint = (
        "https://api.cloudflare.com/client/v4/accounts/example/ai/v1/chat/completions"
    )


class HuggingFaceProvider(OpenAIProvider):
    provider_name = "huggingface"
    endpoint = "https://router.huggingface.co/v1/chat/completions"


class NovitaProvider(OpenAIProvider):
    provider_name = "novita"
    endpoint = "https://api.novita.ai/v3/openai/chat/completions"


class NebiusProvider(OpenAIProvider):
    provider_name = "nebius"
    endpoint = "https://api.studio.nebius.com/v1/chat/completions"


class ZhipuProvider(OpenAIProvider):
    provider_name = "zhipu"
    endpoint = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


class MoonshotProvider(OpenAIProvider):
    provider_name = "moonshot"
    endpoint = "https://api.moonshot.ai/v1/chat/completions"


class DashScopeProvider(OpenAIProvider):
    provider_name = "dashscope"
    endpoint = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"


class QianfanProvider(OpenAIProvider):
    provider_name = "qianfan"
    endpoint = "https://qianfan.baidubce.com/v2/chat/completions"


class FriendliProvider(OpenAIProvider):
    provider_name = "friendli"
    endpoint = "https://api.friendli.ai/serverless/v1/chat/completions"


class InferenceNetProvider(OpenAIProvider):
    provider_name = "inference_net"
    endpoint = "https://api.inference.net/v1/chat/completions"


class OpenAICompatibleGatewayProvider(OpenAIProvider):
    provider_name = "openai_compatible_gateway"
    endpoint = "https://gateway.example.com/v1/chat/completions"


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


class LiteLLMProvider(OpenAIProvider):
    provider_name = "litellm"
    requires_api_key = False
    endpoint = "http://localhost:4000/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class LlamafileProvider(OpenAIProvider):
    provider_name = "llamafile"
    requires_api_key = False
    endpoint = "http://localhost:8082/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class GPT4AllProvider(OpenAIProvider):
    provider_name = "gpt4all"
    requires_api_key = False
    endpoint = "http://localhost:4891/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class AnythingLLMProvider(OpenAIProvider):
    provider_name = "anythingllm"
    requires_api_key = False
    endpoint = "http://localhost:3001/api/v1/openai/chat/completions"

    def build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class XinferenceProvider(OpenAIProvider):
    provider_name = "xinference"
    requires_api_key = False
    endpoint = "http://localhost:9997/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class LlamaSwapProvider(OpenAIProvider):
    provider_name = "llamaswap"
    requires_api_key = False
    endpoint = "http://localhost:8800/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class ExoProvider(OpenAIProvider):
    provider_name = "exo"
    requires_api_key = False
    endpoint = "http://localhost:52415/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class FastChatProvider(OpenAIProvider):
    provider_name = "fastchat"
    requires_api_key = False
    endpoint = "http://localhost:8000/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class H2OGPTProvider(OpenAIProvider):
    provider_name = "h2ogpt"
    requires_api_key = False
    endpoint = "http://localhost:7860/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


class MLXLMProvider(OpenAIProvider):
    provider_name = "mlx_lm"
    requires_api_key = False
    endpoint = "http://localhost:8083/v1/chat/completions"

    def build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}


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
    "huggingface": HuggingFaceProvider,
    "novita": NovitaProvider,
    "nebius": NebiusProvider,
    "zhipu": ZhipuProvider,
    "moonshot": MoonshotProvider,
    "dashscope": DashScopeProvider,
    "qianfan": QianfanProvider,
    "friendli": FriendliProvider,
    "inference_net": InferenceNetProvider,
    "openai_compatible_gateway": OpenAICompatibleGatewayProvider,
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
    "litellm": LiteLLMProvider,
    "llamafile": LlamafileProvider,
    "gpt4all": GPT4AllProvider,
    "anythingllm": AnythingLLMProvider,
    "xinference": XinferenceProvider,
    "llamaswap": LlamaSwapProvider,
    "exo": ExoProvider,
    "fastchat": FastChatProvider,
    "h2ogpt": H2OGPTProvider,
    "mlx_lm": MLXLMProvider,
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


HOSTED_PROVIDERS = {
    "openai",
    "anthropic",
    "claude",
    "gemini",
    "perplexity",
    "mistral",
    "cohere",
    "deepseek",
    "xai",
    "grok",
    "openrouter",
    "groq",
    "together",
    "fireworks",
    "sambanova",
    "cerebras",
    "nvidia_nim",
    "deepinfra",
    "azure_openai",
    "cloudflare",
    "huggingface",
    "novita",
    "nebius",
    "zhipu",
    "moonshot",
    "dashscope",
    "qianfan",
    "friendli",
    "inference_net",
    "openai_compatible_gateway",
}

PROVIDER_FAMILIES = {
    "openai": "frontier_cloud",
    "anthropic": "frontier_cloud",
    "claude": "frontier_cloud",
    "gemini": "frontier_cloud",
    "perplexity": "research_cloud",
    "mistral": "eu_cloud",
    "cohere": "enterprise_cloud",
    "deepseek": "cost_reasoning_cloud",
    "xai": "frontier_cloud",
    "grok": "frontier_cloud",
    "openrouter": "gateway_cloud",
    "groq": "high_speed_cloud",
    "together": "open_model_cloud",
    "fireworks": "open_model_cloud",
    "sambanova": "high_speed_cloud",
    "cerebras": "high_speed_cloud",
    "nvidia_nim": "infra_cloud",
    "deepinfra": "open_model_cloud",
    "azure_openai": "enterprise_cloud",
    "cloudflare": "edge_cloud",
    "huggingface": "open_model_cloud",
    "novita": "open_model_cloud",
    "nebius": "open_model_cloud",
    "zhipu": "cn_cloud",
    "moonshot": "cn_cloud",
    "dashscope": "cn_cloud",
    "qianfan": "cn_cloud",
    "friendli": "gpu_cloud",
    "inference_net": "gateway_cloud",
    "openai_compatible_gateway": "gateway_cloud",
    "ollama": "local_runtime",
    "localai": "local_runtime",
    "vllm": "local_runtime",
    "lmstudio": "local_runtime",
    "llamacpp": "local_runtime",
    "koboldcpp": "local_runtime",
    "textgenwebui": "local_runtime",
    "tabbyapi": "local_runtime",
    "sglang": "local_runtime",
    "mistralrs": "local_runtime",
    "aphrodite": "local_runtime",
    "jan": "local_runtime",
    "openwebui": "local_runtime",
    "litellm": "gateway_runtime",
    "llamafile": "local_runtime",
    "gpt4all": "local_runtime",
    "anythingllm": "gateway_runtime",
    "xinference": "local_runtime",
    "llamaswap": "gateway_runtime",
    "exo": "local_runtime",
    "fastchat": "local_runtime",
    "h2ogpt": "local_runtime",
    "mlx_lm": "local_runtime",
}

PROVIDER_SAMPLE_MODELS = {
    "openai": ["gpt-4.1", "gpt-4.1-mini", "o4-mini"],
    "anthropic": ["claude-sonnet-4", "claude-opus-4"],
    "claude": ["claude-sonnet-4", "claude-opus-4"],
    "gemini": ["gemini-2.5-pro", "gemini-2.5-flash"],
    "perplexity": ["sonar-pro", "sonar-reasoning-pro"],
    "mistral": ["mistral-large", "ministral-8b"],
    "cohere": ["command-r-plus", "command-r7b"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "xai": ["grok-3", "grok-3-mini"],
    "grok": ["grok-3", "grok-3-mini"],
    "openrouter": ["openai/gpt-4.1-mini", "anthropic/claude-sonnet-4"],
    "groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
    "together": ["meta-llama/Llama-3.3-70B-Instruct-Turbo"],
    "fireworks": ["accounts/fireworks/models/llama-v3p1-70b-instruct"],
    "sambanova": ["Meta-Llama-3.3-70B-Instruct"],
    "cerebras": ["llama-3.3-70b", "qwen-3-32b"],
    "nvidia_nim": ["meta/llama-3.3-70b-instruct"],
    "deepinfra": ["meta-llama/Meta-Llama-3.3-70B-Instruct"],
    "azure_openai": ["gpt-4.1", "gpt-4.1-mini"],
    "cloudflare": ["@cf/meta/llama-3.3-70b-instruct-fp8-fast"],
    "huggingface": ["openai/gpt-oss-120b", "Qwen/Qwen3-32B"],
    "novita": ["deepseek/deepseek-r1", "qwen/qwen3-32b"],
    "nebius": ["meta-llama/Meta-Llama-3.3-70B-Instruct"],
    "ollama": ["qwen3:8b", "llama3.1:8b", "deepseek-r1:8b"],
    "localai": ["llama-3.1-8b-instruct", "mistral-7b-instruct"],
    "vllm": ["Qwen/Qwen3-32B", "meta-llama/Llama-3.3-70B-Instruct"],
    "lmstudio": ["qwen3-8b", "gemma-3-12b"],
    "llamacpp": ["llama-3.1-8b-instruct-q4", "qwen3-8b-q4"],
    "litellm": ["router/openai", "router/claude", "router/local"],
}


def provider_runtime_kind(provider_name: str) -> str:
    return "cloud" if provider_name.lower() in HOSTED_PROVIDERS else "local"


def provider_catalog_entry(provider_name: str) -> dict:
    normalized = provider_name.lower()
    provider_cls = PROVIDERS[normalized]
    runtime = provider_runtime_kind(normalized)
    supports_openai_style = issubclass(provider_cls, OpenAIProvider)
    return {
        "provider_name": normalized,
        "runtime_kind": runtime,
        "family": PROVIDER_FAMILIES.get(normalized, "general"),
        "auth_mode": "api_key" if provider_cls.requires_api_key else "optional_or_none",
        "default_endpoint": getattr(provider_cls, "endpoint", ""),
        "supports_openai_style": supports_openai_style,
        "sample_models": PROVIDER_SAMPLE_MODELS.get(normalized, []),
        "routing_role": "primary_cloud" if runtime == "cloud" else "local_fallback",
        "capabilities": [
            "structured_prompting",
            "audit_commentary",
            "report_assistance",
            *(
                ["hybrid_cost_control", "local_privacy_lane"]
                if runtime == "local"
                else ["external_redundancy", "managed_latency_lane"]
            ),
        ],
    }


def list_provider_catalog() -> list[dict]:
    return [provider_catalog_entry(name) for name in sorted(PROVIDERS)]


def provider_catalog_summary() -> dict:
    catalog = list_provider_catalog()
    hosted = [item for item in catalog if item["runtime_kind"] == "cloud"]
    local = [item for item in catalog if item["runtime_kind"] == "local"]
    return {
        "total_supported": len(catalog),
        "hosted_supported": len(hosted),
        "local_supported": len(local),
        "suggested_default_stack": [
            "one frontier cloud provider",
            "one lower-cost or high-speed cloud provider",
            "one local fallback runtime",
        ],
    }


def model_registry_profiles() -> dict:
    return {
        "profiles": [
            {
                "id": "lowest_friction",
                "label": "Lowest-friction starter",
                "recommended_providers": ["openai", "gemini", "ollama"],
                "why": "Fastest setup for demos, audits, and multilingual operator flows.",
            },
            {
                "id": "agency_hybrid",
                "label": "Agency hybrid stack",
                "recommended_providers": [
                    "anthropic",
                    "openai",
                    "groq",
                    "ollama",
                ],
                "why": "Strong writing plus fast fallback plus controlled local backup.",
            },
            {
                "id": "cost_controlled",
                "label": "Cost-controlled production",
                "recommended_providers": [
                    "deepseek",
                    "mistral",
                    "groq",
                    "vllm",
                ],
                "why": "Lower spend with better redundancy and local override paths.",
            },
            {
                "id": "ru_hybrid",
                "label": "RU-focused hybrid stack",
                "recommended_providers": [
                    "gemini",
                    "deepseek",
                    "ollama",
                    "litellm",
                ],
                "why": "Pairs RU search-data integrations with a mixed cloud plus local stack.",
            },
        ],
        "routing_policies": [
            "Use one primary frontier provider for strategic generation.",
            "Use one fast or lower-cost provider for repeated audit commentary.",
            "Keep one local runtime for fallback, private work, and cost resilience.",
        ],
    }
