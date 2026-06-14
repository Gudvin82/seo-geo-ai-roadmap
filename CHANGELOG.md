# Changelog

## v4.4.0 — Public Readiness, One-Day Service Blueprint, and AI-Agent Scenarios

- Added explicit EN/RU public-product readiness docs so the repository can be described accurately as a self-hosted platform and product foundation
- Added EN/RU one-day service blueprint docs for teams who want to turn the repo into their own scanner or audit service
- Added EN/RU one-click deploy option docs covering local demo, Docker VPS, Coolify, Railway, Render, and Kubernetes starter paths
- Added AI-agent scenario prompt packs for repo plus site audit, client-scanner deployment, and existing-site improvement
- Updated README, README_RU, AGENTS, START_HERE_FOR_AI, deployment docs, docs-site routing, and limitations framing to align the public promise with what the repo really supports

## v4.3.0 — Public Case Studies, Review Response, and 10/10 Upgrade Path

- Added bilingual public case studies for `anmalishev.ru`, `auditguard.ru`, and `sitepravo.ru` with explicit fact vs inference boundaries
- Updated `REAL_CASES.md` and `REAL_CASES_RU.md` so the repository now shows concrete public before/after implementation framing instead of abstract-only snapshots
- Added a bilingual review-response layer that classifies external criticism as true, partial, outdated, or not-yet-proven and turns it into a roadmap
- Added a stronger `10/10` upgrade path for proof, integration maturity, monitoring, cost governance, docs consolidation, and repeatable case evidence
- Updated README, docs-site real-cases surface, and roadmap links for the new v4.3.0 evidence layer

## v4.2.0 — Production Proof, GEO Signal Expansion, and Wider Provider Coverage

- Added scanner-first GEO modules for AI readability, citation probability, CDN or edge AI-bot blocking, and RAG chunk readiness
- Added `scripts/crux_field_data.py` plus a new `crux` integration contract for field-data oriented CWV tracking
- Added a machine-readable integration verification matrix endpoint and JSON schema
- Expanded provider coverage with Mistral, Cohere, DeepSeek, and xAI or Grok aliases
- Added stack packs for WordPress, React, and Angular plus an optional Lighthouse CI workflow path
- Added bilingual v4.2 production-proof docs and extended script coverage for the new modules

## v4.1.0 — Security Hardening, Governed CMS Apply Flow, and Operator Follow-Up

- Closed scan-job access gaps so task bundles and graph runtime now require the same session or user boundary as the scanner result surface
- Hardened scanner fetch and webhook behavior with public-port enforcement, redirect-aware validation, and response-size limits
- Replaced thread-only scan execution with a recoverable DB-backed worker loop that can re-queue interrupted jobs after restart
- Added a lightweight technical SEO baseline module to scanner reporting alongside existing AI, schema, FAQ, and social checks
- Added governed CMS change requests with preview, approve, apply, verify, and rollback lifecycle states
- Added report assistant follow-up endpoint plus frontend operator surface for asking focused questions about stored reports
- Expanded integration contracts with clearer production flows, CI-first readiness planning, and stronger machine-readable contract coverage
- Added trusted delivery targets, PR proposal generation, and governed auto-merge eligibility flags for trusted repositories
- Added a real Telegram webhook runtime plus richer repo-ready Chrome and VS Code operator packages
- Added a managed-cloud Kubernetes pack for DigitalOcean Kubernetes, GKE, and EKS style deployment paths
- Updated EN/RU architecture notes, app version markers, frontend surfaces, contract catalog, and tests for the new v4.1.0 runtime

## v4.0.0 — AI Agent Mode, Product Surfaces, and One-Click Delivery

- Added real AI Agent Mode contracts, overview, and execution surfaces for `manual`, `scheduled`, `watch`, `agent-review`, `agent-plan`, and `agent-fix-proposal`
- Added one-click URL audit result flow with direct machine-readable links into task bundles and dynamic graph runtime
- Added normalized task bundle generation for scan jobs and audit runs plus export adapters with a real GitHub Issues path and honest templates for GitLab, Notion, Trello, and Linear
- Added dynamic graph runtime APIs that build nodes and edges from live scan JSON and audit findings instead of relying on static graph demos alone
- Added a contracts catalog plus JSON schemas for audits, task bundles, graph snapshots, report exports, command routing, and integration contracts
- Added a managed/public API boundary endpoint, first-class CI action packaging, and scaffolds for VS Code, Chrome, and Telegram operational surfaces
- Updated README, README_RU, ROADMAP, AGENTS, START_HERE docs, docs-site navigation, reporting templates, and frontend scanner/graph surfaces for the new product split

## v3.8.0 — Graph Intelligence, Command UX, Reporting, and GTM Distribution

- Added a richer canonical `/geo ...` command layer with aliases, examples, expected outputs, and use-case packaging for agents and operators
- Added a new graph intelligence frontend at `app/frontend/graph.html` with site, surface, issue, and trust modes plus JSON export
- Added EN/RU docs for graph intelligence, distribution and GTM packaging, research-to-re-measure workflow, and framework integrations
- Added reporting packs for executive summary, fix pack, and graph snapshot delivery
- Updated README, README_RU, AGENTS, AI handoff prompts, START_HERE docs, docs-site pages, and tests to reflect the new v3.8.0 operator surface
- Added production-guided machine-readable contracts for GSC, GA4, Yandex, and CMS connector flows
- Added CI gating and product mode machine-readable endpoints plus a fuller executive dashboard surface in the app

## v3.7.0 — RU AI Hardening, ai.txt, and Discoverability Coverage

- Added real RU and AI bot policy hardening with separate `YandexAdditional` handling alongside `YandexBot`
- Added `scripts/check-ai-txt.py`, `templates/ai.txt.example`, and EN/RU documentation for practical `ai.txt` usage and contradiction review
- Added `templates/schema/website-schema.json` plus a new schema coverage checker that audits JSON-LD presence by site type instead of validating JSON syntax only
- Added practical FAQ / answer-ready detection, Open Graph / Twitter Card completeness checks, and integrated robots.txt ↔ sitemap verification
- Expanded the scanner reporting model so exported summaries now include module-level findings for AI bot policy, `ai.txt`, schema, FAQ, social metadata, and robots+sitemap linkage
- Added RU-focused practical guidance for AI-content marking as a compliance-aware trust and GEO layer, explicitly framed as non-legal advice
- Updated README, README_RU, AGENTS, AI handoff prompts, START_HERE docs, scripts reference, docs-site, and bilingual checklists for the new coverage layer

## v3.6.0 — Public Scanner Foundation, Ownership Verification, and Async Job UX

- Added a dedicated scanner intake page with passive, active, and feature-flagged full scan modes
- Added ownership verification requests, verification tokens, and consent records for public/self-hosted scanner flows
- Added async scan jobs with queued, verifying, running, partial-success, completed, failed, cancelled, and expired lifecycle states
- Added scan job events, artifacts, cancellation support, per-IP and per-domain throttling, and SSRF-oriented target blocking
- Added versioned JSON, markdown, CSV, and HTML export artifacts plus webhook, SMTP/email, and Telegram completion hooks
- Added EN/RU scanner foundation docs, docs-site scanner page, and public limitations visibility in UI and release-facing docs
- Updated public architecture notes to describe the implemented scanner foundation and removed the old next-step backlog section

## v3.5.0 — AI Handoff Packs, Scanner Bootstrap, and Public Architecture Note

- Added `scripts/agent_handoff_pack.py` so users can generate ready-to-paste AI task prompts for audit, demo deployment, scanner deployment, and client setup flows
- Expanded the command router and command catalog to cover `deploy` and `scanner` scenarios in addition to the existing GEO and reporting surfaces
- Added a scanner-oriented bootstrap mode to `scripts/bootstrap_self_hosted.py` with explicit delivery-surface guidance
- Added public EN/RU architecture notes that explain the product layers, self-hosted deployment model, audit loop, AI handoff strategy, scanner evolution path, and current limits
- Updated README, README_RU, AGENTS, START_HERE_FOR_AI, AI handoff prompts, docs-site navigation, and architecture docs to make the new zero-friction handoff path visible
- Added tests for the new AI handoff pack generator and expanded bootstrap and command catalog coverage

## v3.4.0 — Command Surface, Bootstrap, and Adoption UX

- Added a command surface for GEO, SEO, and AI discoverability tasks through a new backend routing layer and CLI entrypoint
- Added `GET /api/v1/tools/command-catalog` and `POST /api/v1/tools/command-router` so agents and operators can map broad tasks to scripts, docs, and API routes
- Added `scripts/geo_command_surface.py` and `scripts/bootstrap_self_hosted.py` to improve AI handoff and self-hosted onboarding
- Added tests for the new command surface and bootstrap planner plus smoke coverage in CI
- Added EN/RU docs for command catalog, bootstrap guide, scoring model, and modular how-it-works framing
- Updated AGENTS, README, README_RU, docs site navigation, and the app badge to reflect the new adoption surface

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
