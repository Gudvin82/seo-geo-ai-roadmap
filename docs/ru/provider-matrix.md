# Provider Matrix

| Provider | Auth | Local или cloud | Сильные стороны | Ограничения | Типичный use case |
|---|---|---|---|---|---|
| OpenAI | API key | Cloud | широкая экосистема моделей | зависимость от paid cloud | report commentary, structured prompts |
| Anthropic / Claude | API key | Cloud | сильная long-form reasoning | зависимость от paid cloud | strategy и editorial review |
| Gemini | API key | Cloud | мультиязычность и близость к Google-экосистеме | по умолчанию cloud-only | multilingual checks |
| Perplexity | API key | Cloud | research-oriented ответы | cloud dependency | research commentary |
| Mistral | API key | Cloud | efficient EU-friendly model access | cloud dependency | lower-cost multilingual operations |
| Cohere | API key | Cloud | enterprise-friendly text generation | response schema differs from OpenAI-style APIs | summarization and classification |
| DeepSeek | API key | Cloud | cost-sensitive reasoning coverage | provider-specific quota and stability patterns | cost-aware structured prompting |
| xAI / Grok | API key | Cloud | wider current-events and alternative-model coverage | cloud dependency | broader provider redundancy |
| Ollama | обычно без ключа | Local / self-hosted | privacy-first local inference | нужен локальный runtime и model pull | приватный audit commentary |
| LocalAI | обычно без ключа | Local / self-hosted | OpenAI-style локальная совместимость | runtime надо поддерживать самим | local API compatibility |
| vLLM | optional bearer token | Local / self-hosted | OpenAI-compatible serving для self-hosted моделей | тяжелее по infra, чем Ollama | larger self-hosted model serving |

## Примечания

- Cloud providers остаются опциональными.
- Local providers усиливают обещание free и self-hosted.
- Provider failures отражаются в artifacts и metrics, а не скрываются.
