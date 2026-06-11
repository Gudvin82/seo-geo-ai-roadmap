# Changelog

## v2.2.0 — Operator-Ready Platform Upgrade

- Added a canonical `POST /api/v1/audit-runs/run` entrypoint with explicit job
  acceptance payloads, lifecycle status exposure, and richer audit metadata
- Added workspace memberships, invite flow, audit logs, and permission-aware
  access checks for projects, reports, artifacts, providers, and workspaces
- Added local provider support for Ollama, LocalAI, and vLLM-compatible
  endpoints alongside the existing cloud provider model
- Added deployment verification docs, runbooks, known limitations docs, cloud
  manifest starters, and a `make verify-demo` operator check
- Expanded EN/RU API, provider, patch-mode, CMS connector, and role/invite
  documentation together with more visible proof assets in the README layer

## v2.1.0 — Turnkey Self-Hosted Hardening

- Hardened authentication with Argon2id password hashing, expiring bearer
  tokens, and basic brute-force protection
- Added `SECURITY_CHECKLIST*.md`, `.env.production.example`, and safer
  environment defaults for production-minded self-hosted deployment
- Added Alembic migrations, demo seed data, `make` shortcuts, and local startup
  guidance
- Added `/metrics`, observability docs, provider matrix docs, AI operator mode
  docs, API reference docs, and self-hosted use case docs in EN and RU
- Expanded backend tests and CI quality checks for Python formatting, YAML
  readability, migrations, and app reliability
- Repositioned the app layer as a free, transparent, self-hosted platform
  rather than a cloud-first SaaS claim

## v2.0.0 — SaaS Foundation and Multi-Provider AI

- Added a first app layer under `app/` with a FastAPI backend, static frontend,
  shared folder, and worker stub
- Introduced user, workspace, project, site, audit run, report, provider,
  brand-facts, prompt-set, artifact, and scheduled-check domain foundations
- Added multi-provider AI abstraction for OpenAI, Anthropic/Claude, Gemini, and
  Perplexity with normalized provider handling
- Added structured audit execution, evidence storage, EN/RU reporting, and
  repo-asset reuse through API endpoints
- Added Dockerized self-hosted deployment foundations for backend, frontend,
  worker, and PostgreSQL
- Added architecture, deployment, and open-source vs SaaS boundary docs in
  English and Russian
- Extended CI coverage to run repository tests, backend API tests, and frontend
  asset sanity checks
- Extended the docs site and repository documentation to explain the new SaaS
  foundation without replacing the methodology layer

## v1.4.0 — Proof, Testing, and Distribution

- Added pytest coverage for key scripts and wired test execution into CI
- Added `.env.example`, content freshness checking, and a hallucination-checking starter
- Added real-world implementation docs, factual consistency docs, and entity hierarchy guidance in EN and RU
- Added ROI templates, brand-facts templates, walkthroughs, contributor guidance, and automation starters
- Added MkDocs configuration and GitHub Pages delivery for public documentation distribution

## v1.3.0 - 2026-06-11 - Documentation, Reliability, and AI Readability

- Added English and Russian script documentation under `scripts/README*.md`
- Hardened `generate_llms_txt.py` with louder failure modes and clearer summaries
- Added glossary files, AI SoV sample datasets, ROI tooling, and case-study templates
- Improved AGENTS onboarding, README visibility, and CI coverage for links, llms, and smoke tests

## v1.2.0 - 2026-06-11 - Agent Mode and Vibe Coding

- Added `AGENTS.md` as a dedicated agent-first entrypoint for coding agents
- Updated `README.md` and `README_RU.md` with agent onboarding sections
- Added a companion integration block for `vibe-coding-protocols`
- Extended the repository onboarding layer without changing the existing structure

## v1.1.0 - 2026-06-11 - Trust, Automation, and Workflow

- Added `generate_llms_txt.py` for sitemap-based `llms.txt` generation
- Connected Definition of Done to the pull request workflow
- Expanded `README.md` and `README_RU.md` with badges, example script,
  example prompt, and a live-project workflow
- Added an AI Share of Voice weekly report example and linked it from GEO docs
- Prepared the repository for the `v1.1.0` trust, automation, and workflow release

## v1.0.0 - 2026-06-11

- Repositioned the project as a discoverability operating system
- Added positioning, differentiators, ecosystem map, governance, roadmap, and release process files
- Expanded bilingual docs with standardized execution, QA, decision, prompt, and output sections
- Added expanded checklists, prompt library, templates, examples, helper scripts, and GitHub workflows

## 0.1.0 - 2026-06-11

- Initial public release
- Added bilingual roadmap structure for SEO, GEO, AI search, and Yandex workflows
- Added operational checklists, reusable templates, prompts, examples, and starter validation scripts
