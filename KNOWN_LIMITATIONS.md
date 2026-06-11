# Known Limitations

## Production-ready today

- self-hosted FastAPI app with demo seed and migrations
- transparent report and artifact generation
- EN/RU documentation and operator guidance
- cloud and local provider configuration model

## MVP but usable

- workspace roles and invite flow
- canonical audit execution endpoint
- audit log and metrics expansion
- static frontend operator console

## Experimental

- local LLM adapters (`ollama`, `localai`, `vllm`) depend on external runtime setup
- patch-mode output is still artifact-first, not direct CMS writeback
- cloud manifests are starters, not a hosted support contract

## Roadmap

- richer queue/retry semantics
- deeper CMS write support
- stronger export/import tooling
- broader project-level permission model
