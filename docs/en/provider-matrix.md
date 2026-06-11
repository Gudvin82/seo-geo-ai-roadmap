# Provider Matrix

## Current provider support

| Provider | Status | Typical use | Notes |
|---|---|---|---|
| OpenAI | Supported | commentary, prompt tasks | requires `OPENAI_API_KEY` |
| Anthropic / Claude | Supported | commentary, long-form review | requires `ANTHROPIC_API_KEY` |
| Gemini | Supported | commentary, multilingual workflows | requires `GEMINI_API_KEY` |
| Perplexity | Supported | commentary, research-oriented prompts | requires `PERPLEXITY_API_KEY` |

## Capability notes

- All providers currently support normalized text generation calls.
- Fallback logic is conservative and transparent.
- Missing keys and provider failures are surfaced in artifacts and metadata.
- Cost-awareness is a placeholder for now, not a billing system.
