# Каталог провайдеров v4.5.x

`v4.5.0` расширяет provider surface так, чтобы было проще работать в
self-hosted, hybrid и multi-vendor сценариях.

## Hosted и online-oriented провайдеры

- OpenAI
- Anthropic или Claude
- Gemini
- Perplexity
- Mistral
- Cohere
- DeepSeek
- xAI или Grok
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
- Hugging Face
- Novita
- Nebius
- Zhipu
- Moonshot
- DashScope
- Qianfan
- Friendli
- Inference.net
- OpenAI-compatible gateway

## Local и self-hosted runtime-поверхности

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
- LiteLLM
- Llamafile
- GPT4All
- AnythingLLM
- Xinference
- LlamaSwap
- Exo
- FastChat
- h2oGPT
- MLX-LM

## Почему это важно

- команды могут оставаться полностью локальными
- можно стартовать локально и потом перейти на hosted providers
- агентства могут держать один операторский workflow на смешанных client setups
- AI coding agents могут разворачивать проект в ту provider surface, которая
  уже принадлежит пользователю

## Рекомендуемые сочетания

- Самый простой local demo: Ollama или LM Studio
- Hybrid production-friendly path: OpenAI или Anthropic плюс fallback на Ollama
- Широкие multi-vendor эксперименты: OpenRouter плюс один local runtime
- RU-oriented mixed stack: Yandex data integrations плюс hosted LLM и один
  local runtime для контроля затрат
