# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml)
[![Script Smoke Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml)
[![Python Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml)
[![Docs Build](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml)
[![Docker](https://img.shields.io/badge/docker-self--hosted-2496ED?logo=docker&logoColor=white)](./docker-compose.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-app-009688?logo=fastapi&logoColor=white)](./app/backend/app/main.py)
![Self-Hosted Ready](https://img.shields.io/badge/self--hosted-ready-1f6f50)

Free, transparent, self-hosted platform for SEO, GEO, and AI discoverability.
Deploy it on your own machine or server, connect your own AI providers, run
audits, track AI share of voice, manage brand facts, and deliver bilingual
reports without mandatory paid cloud.

[Русская версия](./README_RU.md)

## What this is

This repository has three connected layers:

- Framework: the methodology, prompts, templates, checklists, and scripts
- Platform: the self-hosted app for operators, teams, and client delivery
- Service system: the repeatable way to audit, prioritize, fix, and re-run

The differentiator is not "more docs". It is one practical system that a human
operator or an AI coding agent can use end to end:

1. deploy
2. connect provider(s)
3. run a real audit
4. generate reports and artifacts
5. prioritize fixes
6. re-run and compare deltas over time

## Who it is for

- Agencies running recurring audits and client-ready reporting
- In-house SEO, growth, content, and AI operations teams
- Founders and expert operators managing their own multilingual sites
- Teams working across English and Russian-speaking markets

## Who it is not for

- Teams expecting a black-box crawler with no human review
- Users who only want a hosted SaaS with no self-hosted option
- People looking for GEO hype as a replacement for technical SEO
- Buyers who want rankings promised without proof, evidence, or governance

## What happens in 15 minutes, 30 days, and 90 days

### In 15 minutes

- clone the repo
- run the stack
- sign in
- create one workspace and one project
- connect one provider or stay in transparent starter mode
- run one audit and one AI SoV check
- open a report and export package

### In 30 days

- you move from one-off audits to a repeatable operating rhythm
- brand facts, prompts, and evidence stay in one place
- you can show score and visibility deltas to yourself or clients

### In 90 days

- you build a reusable operator system instead of ad hoc SEO work
- AI SoV, factual consistency, and reporting become measurable routines
- agency, in-house, and founder modes can share the same platform

## Outcome-based scenarios

- Agency mode: one workspace per client, one project per site, repeatable
  bilingual reporting, AI-assisted prioritization, exportable artifacts
- In-house mode: one truth center, recurring audits, provider-backed AI SoV,
  evidence-driven backlog for product, content, and engineering
- Founder mode: one self-hosted stack for site audits, AI visibility checks,
  fact governance, and periodic re-runs without vendor lock-in

## Start here

- Human quickstart: [WALKTHROUGH.md](./WALKTHROUGH.md)
- AI quickstart: [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
- Deployment: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Verification: [VERIFY_DEPLOYMENT.md](./VERIFY_DEPLOYMENT.md)
- API reference: [docs/en/api-reference.md](./docs/en/api-reference.md)

## AI handoff block

Give this repository to your AI coding agent and tell it:

1. read [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
2. follow [AGENTS.md](./AGENTS.md)
3. run `make turnkey-demo`
4. run `make agent-self-check`
5. report what was verified, what was simulated, and what still needs human
   review

The repository is intentionally structured so an AI agent can deploy it from
scratch and keep the EN/RU operator layer aligned.

## Product proof

These screenshots are from the actual local app flow, not placeholder diagrams.
If you need a live demo, use the local demo flow below. No always-on public SaaS
demo is promised in this repository.

![Login and dashboard proof](./docs_site/assets/screenshots/app-login-dashboard-proof.png)
![Provider configuration proof](./docs_site/assets/screenshots/app-provider-proof.png)
![Audit run proof](./docs_site/assets/screenshots/app-audit-proof.png)
![Report and artifact proof](./docs_site/assets/screenshots/app-report-proof.png)

## Why this repository exists

Most SEO repositories stop at advice. Most GEO discussions stop at theory. Most
AI tooling hides the scoring, forces a cloud dependency, or ignores Russian
markets. This project is built for the opposite direction:

- self-hosted first
- transparent metrics
- bilingual from day one
- human-usable and AI-agent-usable
- proof before claims
- technical SEO plus GEO/AI, not GEO instead of SEO

## What is inside

- App layer: [`app`](./app)
- Docs: [`docs/en`](./docs/en) and [`docs/ru`](./docs/ru)
- Checklists: [`checklists`](./checklists)
- Prompt library: [`prompts`](./prompts)
- Templates: [`templates`](./templates)
- Examples: [`examples`](./examples)
- Scripts: [`scripts`](./scripts)
- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md)
- Positioning: [POSITIONING.md](./POSITIONING.md)
- Real cases: [REAL_CASES.md](./REAL_CASES.md)
- Operations runbook: [OPERATIONS_RUNBOOK.md](./OPERATIONS_RUNBOOK.md)
- Known limitations: [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md)

## App quickstart

- Frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/healthz`
- Readiness: `http://localhost:8000/readyz`
- Metrics: `http://localhost:8000/metrics`

### Turnkey local demo

```bash
make turnkey-demo
make verify-demo
make agent-self-check
```

Expected demo credentials:

- Email: `demo@example.com`
- Password: `DemoPlatform123`

## Canonical operator flow

1. Create workspace
2. Create project
3. Fill brand facts
4. Configure providers
5. Run audit
6. Open report and artifacts
7. Run AI SoV
8. Prioritize fixes
9. Re-run after changes
10. Export client or internal delivery pack

## Transparent scoring and implementation output

`v3.0.0` formalizes two proof-first layers:

- AI Citation Score: a transparent 0-100 signal based on whether a brand is
  mentioned, cited, and described well in structured AI SoV checks
- Prioritization engine: impact, effort, confidence, and benchmark status for
  findings such as LCP, CLS, INP, schema coverage, factual consistency, and AI
  readiness

Read more:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/en/api-reference.md](./docs/en/api-reference.md)
- [docs/en/patch-mode.md](./docs/en/patch-mode.md)
- [docs/en/client-delivery.md](./docs/en/client-delivery.md)
- [docs/en/search-data-connectors.md](./docs/en/search-data-connectors.md)
- [docs/en/cms-connectors.md](./docs/en/cms-connectors.md)

## Real cases

`v3.0.0` expands the real-case layer with bounded, honest public-site snapshots
for:

- `sitepravo.ru`
- `auditguard.ru`
- `anmalishev.ru`

See [REAL_CASES.md](./REAL_CASES.md).

## Verification discipline

Use these commands before treating a release as complete:

- `make verify-demo`
- `make agent-self-check`
- `PYTHONPATH=app/backend ./.venv/bin/python -m pytest app/backend/tests`
- `./.venv/bin/python -m mkdocs build`

## Honest boundaries

This project is not claiming:

- full autonomous remediation with no human review
- guaranteed AI citations across volatile AI answer surfaces
- enterprise SLA, SSO, or billing in the current release
- replacement of technical SEO with GEO alone

See [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md).

## Latest changes

- `v3.1.0`: search and analytics integration starters, CMS connector flows,
  patch packs, client delivery packs, project package import, stronger
  white-label framing, review-mode guidance, and richer EN/RU operator docs
- `v3.0.0`: proof-first positioning rewrite, stronger onboarding, real app
  screenshots, AI Citation Score documentation, prioritization engine,
  provider-backed AI SoV, structured observability, role/invite hardening, and
  richer EN/RU operator docs
- `v2.3.0`: AI SoV persistence, prompt library metadata, webhook notifications,
  project export package, top-20 local LLM matrix, benchmark and search-data
  documentation
- `v2.2.0`: operator-ready platform upgrade with permissions, invites, and
  verify-demo discipline

## License

This repository is distributed under the license defined in [LICENSE](./LICENSE).
