# v4.2.0 Production Proof and Expansion

`v4.2.0` strengthens the repo in the exact places that were still medium,
partial, or missing:

- AI readability auditing
- citation probability scoring
- CDN or edge blocking checks for major AI bots
- RAG chunk readiness checks
- CrUX field-data ingestion path
- integration verification matrix
- wider provider coverage
- stack packs for WordPress, React, and Angular

## New scanner modules

- `ai_readability`
- `citability_score`
- `cdn_ai_bot_blocking`
- `rag_chunk_readiness`

These are available through the app scanner flow and the standalone scripts.

## New scripts

- `python scripts/ai_readability_audit.py --url https://example.com`
- `python scripts/citability_score.py --url https://example.com`
- `python scripts/check_cdn_blocking.py --url https://example.com`
- `python scripts/rag_chunk_audit.py --url https://example.com/page`
- `python scripts/crux_field_data.py --url https://example.com`
- `python scripts/integration_verification_matrix.py --json`

## Integration proof layer

The repo now exposes a machine-readable verification matrix through:

- `GET /api/v1/integrations/verification-matrix?project_id={project_id}`

Each row makes the current state explicit:

- `contract_only`
- `starter_or_stub`
- `live_api_or_runtime`
- `live_inventory_or_reviewed_flow`

This avoids vague claims about “production-ready” integrations.

## Expanded providers

Cloud:

- OpenAI
- Anthropic
- Gemini
- Perplexity
- Mistral
- Cohere
- DeepSeek
- xAI / Grok

Local or self-hosted:

- Ollama
- LocalAI
- vLLM

## Stack packs

The new `stack-packs/` folder gives AI agents and operators a smaller,
CMS-aware starting surface:

- `stack-packs/wordpress.yaml`
- `stack-packs/react.yaml`
- `stack-packs/angular.yaml`

## Limits still kept honest

- live GSC / GA4 / Yandex proof still depends on real credentials and operator setup
- CrUX live mode depends on `CRUX_API_KEY`
- citation score remains a proxy metric, not a promise of mentions
- CDN bot checks are edge probes, not a guarantee of crawler behavior over time
