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
- prompt library UI, project export package, and AI SoV history are practical but still lightweight
- webhook notifications are starter-grade and expect your own endpoint operations

## Experimental

- local LLM adapters (`ollama`, `localai`, `vllm`) depend on external runtime setup
- patch-mode output is still artifact-first, not direct CMS writeback
- cloud manifests are starters, not a hosted support contract
- heuristic benchmark scoring is a starter interpretation layer, not an industry benchmark API
- Google Search Console and Yandex integrations are bootstrap stubs, not full OAuth automations
- notification delivery does not yet include durable retry queues or guaranteed sequencing

## Roadmap

- richer queue/retry semantics
- deeper CMS write support
- stronger export/import tooling
- broader project-level permission model
- production-grade webhook retry, scheduling, and operator alerting
- stronger benchmark baselines per niche, region, and device mix
- deeper WordPress and CMS writeback with safer review gates
