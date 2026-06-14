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
- public scanner service works as a self-hosted foundation, not as a maintainer-operated hosted SaaS

## Experimental

- local LLM adapters (`ollama`, `localai`, `vllm`) depend on external runtime setup
- patch-mode output is still artifact-first, not direct CMS writeback
- cloud manifests are starters, not a hosted support contract
- heuristic benchmark scoring is a starter interpretation layer, not an industry benchmark API
- Google Search Console and Yandex integrations are bootstrap stubs, not full OAuth automations
- notification delivery does not yet include durable retry queues or guaranteed sequencing
- the hosted validator page validates pasted content reliably, but public URL fetches can fail when remote sites block cross-origin browser requests
- scheduled checks expose a real execution model, but self-hosted users still need cron, GitHub Actions, or another scheduler
- CMS writeback is governed and safe-first; `v3.3.0` prepares packages and approval states, not uncontrolled live publishing
- public multi-tenant rate-limit, billing, and abuse-isolation expectations still depend on the operator's own infrastructure decisions
- managed deployments such as Railway, Render, or Coolify are realistic paths, but this repo does not claim a one-click vendor-owned hosted plan

## Roadmap

- richer queue/retry semantics
- deeper CMS write support
- stronger export/import tooling
- broader project-level permission model
- production-grade webhook retry, scheduling, and operator alerting
- stronger benchmark baselines per niche, region, and device mix
- deeper WordPress and CMS writeback with safer review gates
- more precise fact-drift detection across live AI outputs and structured source systems
- clearer public-service packaging for teams turning the repo into a scanner or audit business
