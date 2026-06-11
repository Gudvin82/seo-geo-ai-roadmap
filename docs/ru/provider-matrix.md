# Provider Matrix

## Текущая поддержка провайдеров

| Provider | Status | Typical use | Notes |
|---|---|---|---|
| OpenAI | Supported | commentary, prompt tasks | нужен `OPENAI_API_KEY` |
| Anthropic / Claude | Supported | commentary, long-form review | нужен `ANTHROPIC_API_KEY` |
| Gemini | Supported | commentary, multilingual workflows | нужен `GEMINI_API_KEY` |
| Perplexity | Supported | commentary, research-oriented prompts | нужен `PERPLEXITY_API_KEY` |

## Комментарии по возможностям

- Сейчас все провайдеры поддерживаются через нормализованный text-generation интерфейс.
- Fallback logic пока намеренно консервативна и прозрачна.
- Missing keys и provider failures отражаются в artifacts и metadata.
- Cost-awareness пока только placeholder, а не billing system.
