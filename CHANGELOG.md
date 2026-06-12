# Changelog

## v3.3.0 — Operational Proof, Hosted Validation, and Governance

- Added a hosted/deploy-ready docs-site `llms.txt` validator page and expanded EN/RU validator docs with honest browser-fetch limitations
- Added retry semantics for provider-backed commentary, notifications, and governed CMS writeback preparation together with visible retry metadata
- Added scheduling descriptors, CLI schedule planning, and EN/RU docs for recurring audits and visibility checks
- Added a first fact-drift detection API and CLI helper for cross-surface brand consistency review
- Expanded CMS safety semantics with explicit allowed, risky, and unsupported actions plus human-approval boundary handling
- Added security scanning workflow with `pip-audit` and `gitleaks`, plus coverage generation and artifact upload in Python CI
- Added EN/RU docs for trust surfaces, vertical playbooks, GEO-to-CRO bridge, executive dashboards, ROI framing, and commercial boundary clarity
- Added public evaluation assets inspired by `vibe-coding-protocols`, including evaluation and proof-review entrypoints
- Bumped the app version and release-facing surfaces to `v3.3.0`

## v3.2.0 — GEO/AI Deep Dive

- Reworked the GEO/AI methodology around three explicit outcome layers:
  rankings, AI visibility, and conversion trust
- Added EN/RU deep-dive docs for measurement maturity, business outcomes,
  priority maps, AI surfaces, bots and robots policy, answer-ready patterns,
  entity SEO, competitive gap, conversion layer, maturity model, anti-hype,
  meta-case analysis, and RU LLM context
- Added five EN/RU GEO playbooks for launch, citation recovery, fact
  consistency, multilingual governance, and Yandex-plus-LLM execution
- Added a public `llms.txt` validator API plus standalone frontend page as a
  linkable free tool
- Added an example GitHub Action for AI Visibility Check and expanded JSON-LD
  schema starters for GEO/AI operator use
- Finalized the release with stricter `llms.txt` asset consistency across
  validator logic, examples, templates, smoke checks, and operator docs

## v3.1.0 — Integrations, Patch Flows, and Client Delivery

- Added persisted search and analytics integrations for Google Search Console,
  GA4, Yandex Webmaster, and Yandex Metrica starter sync flows
- Added CMS connector flows for WordPress, Tilda, Bitrix, and Webflow together
  with inventory sync and governed writeback modes
- Added patch packs and client delivery packs with issue-ready backlog items,
  developer briefs, content briefs, schema suggestions, and llms.txt guidance
- Added project package import to complement export and improve portability
- Expanded EN/RU docs for search-data connectors, patch mode, client delivery,
  review mode, white-label use, and CMS operator workflows

## v3.0.0 — Proof-First Discoverability Platform

- Repositioned the project as a proof-first daily operating system for SEO,
  GEO, and AI discoverability rather than a docs-heavy repository
- Reworked README, README_RU, positioning, walkthrough, and AI handoff entry
  points around clear ICPs, 15-minute onboarding, 30-day and 90-day outcomes,
  and honest boundaries
- Productized the frontend with an operator overview, clearer onboarding, and
  compact charts for audits, reports, providers, and AI SoV history
- Added provider-backed AI SoV execution with persisted history, transparent
  AI Citation Score handling, and documented volatility notes
- Added a real prioritization layer with impact, effort, confidence, benchmark
  interpretation, and richer report payloads
- Expanded audit logging, request logging, provider latency, app error, and
  background retry visibility for a more operationally useful self-hosted app
- Strengthened role and invite operations with update, revoke, resend, and role
  change flows plus broader API and test coverage
- Expanded EN/RU documentation for API, operations, scoring, roles, and real
  case snapshots across `sitepravo.ru`, `auditguard.ru`, and `anmalishev.ru`

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
- Added multi-provider AI abstraction for OpenAI, Anthropic, Gemini, and
  Perplexity with normalized provider handling
- Added structured audit execution, evidence storage, EN/RU reporting, and
  repo-asset reuse through API endpoints
- Added Dockerized self-hosted deployment foundations for backend, frontend,
  worker, and PostgreSQL

## v1.x

- `v1.4.0`: proof, testing, and distribution
- `v1.3.0`: documentation, reliability, and AI readability
- `v1.2.0`: agent mode and vibe coding
- `v1.1.0`: trust, automation, and workflow
- `v1.0.0`: discoverability OS foundation
