# Provider Catalog v4.5.0

`v4.5.0` expands the provider surface so self-hosted, hybrid, and multi-vendor
operation is easier.

## Hosted and online-oriented providers

- OpenAI
- Anthropic or Claude
- Gemini
- Perplexity
- Mistral
- Cohere
- DeepSeek
- xAI or Grok
- OpenRouter
- Groq
- Together
- Fireworks
- SambaNova
- Cerebras
- NVIDIA NIM
- DeepInfra
- Azure OpenAI
- Cloudflare AI

## Local and self-hosted runtimes

- Ollama
- LocalAI
- vLLM
- LM Studio
- llama.cpp
- KoboldCpp
- Text Generation Web UI
- TabbyAPI
- SGLang
- mistral.rs
- Aphrodite
- Jan
- OpenWebUI

## Why this matters

- teams can stay fully local
- teams can start local and later move to hosted providers
- agencies can maintain one operator workflow across mixed client setups
- AI coding agents can route deployments into the provider surface a user
  already owns

## Suggested default combinations

- Lowest friction local demo: Ollama or LM Studio
- Hybrid production-friendly path: OpenAI or Anthropic plus Ollama fallback
- Broad multi-vendor experimentation: OpenRouter plus one local runtime
- RU-focused mixed stack: Yandex data integrations plus a hosted LLM and one
  local runtime for controlled cost
