# Provider Matrix

| Provider | Auth | Local or cloud | Strengths | Limitations | Typical use |
|---|---|---|---|---|---|
| OpenAI | API key | Cloud | broad model ecosystem | paid cloud dependency | report commentary, structured prompts |
| Anthropic / Claude | API key | Cloud | strong long-form reasoning | paid cloud dependency | strategy, editorial review |
| Gemini | API key | Cloud | multilingual and Google ecosystem fit | cloud-only by default | multilingual checks |
| Perplexity | API key | Cloud | research-oriented answers | cloud dependency | research commentary |
| Mistral | API key | Cloud | efficient EU-friendly model access | cloud dependency | lower-cost multilingual operations |
| Cohere | API key | Cloud | enterprise-friendly text generation | response schema differs from OpenAI-style APIs | summarization and classification |
| DeepSeek | API key | Cloud | cost-sensitive reasoning coverage | provider-specific quota and stability patterns | cost-aware structured prompting |
| xAI / Grok | API key | Cloud | wider current-events and alternative-model coverage | cloud dependency | broader provider redundancy |
| Ollama | none by default | Local / self-hosted | privacy-first local inference | depends on local runtime and model pull | private audit commentary |
| LocalAI | none by default | Local / self-hosted | OpenAI-style local compatibility | operator-managed runtime | local API compatibility |
| vLLM | optional bearer token | Local / self-hosted | OpenAI-compatible serving for hosted local models | infra-heavy versus Ollama | larger self-hosted model serving |

## Notes

- Cloud providers remain optional.
- Local providers reinforce the free and self-hosted positioning.
- Provider failures are surfaced in artifacts and metrics rather than hidden.
