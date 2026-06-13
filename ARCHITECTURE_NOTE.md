# Architecture Note

Public architecture note for `seo-geo-ai-roadmap`, aligned with the product
state after `v3.5.0`.

## 1. Product shape

The repository is intentionally split into three reusable surfaces:

- Methodology surface: docs, prompts, checklists, templates, examples
- Execution surface: scripts, API routes, command router, operator workflows
- Product surface: self-hosted app, reports, artifacts, delivery paths

This keeps the project usable in three modes:

- as a repository-only methodology kit
- as a self-hosted operator application
- as a base for a client-facing or internal scanner service

## 2. Deployment model

Primary deployment shape:

- frontend on port `3000`
- API on port `8000`
- database through local SQLite fallback or PostgreSQL-ready deployment
- docs site as a public proof, validator, and onboarding layer

The deployment model is intentionally simple:

- local demo mode
- production-like self-hosted mode
- scanner-oriented mode for reusable intake and audit delivery

The repository does not pretend to be a finished multi-tenant public SaaS. It
is a self-hosted platform foundation that can be extended into one.

## 3. Execution flow

The core execution loop is:

1. create workspace
2. create project
3. capture canonical brand facts
4. connect providers
5. run audit
6. store reports and artifacts
7. run AI SoV and recurring checks
8. compare deltas over time

This same loop can sit behind:

- an operator dashboard
- an AI coding agent handoff
- a gated public intake form

## 4. AI handoff strategy

The repository is designed so another AI agent does not need a custom prompt
from scratch every time.

Current handoff layers:

- `START_HERE_FOR_AI*.md`
- `AGENTS.md`
- `AI_HANDOFF_PROMPT*.md`
- `scripts/agent_handoff_pack.py`
- `scripts/geo_command_surface.py`
- `scripts/bootstrap_self_hosted.py`

This means a user can hand the repository URL to Cursor, Claude Code, or Codex
and point the agent to a built-in task pack such as:

- `audit-site`
- `deploy-demo`
- `deploy-scanner`
- `client-setup`

## 5. Scanner architecture direction

The repository already contains the audit core, reporting path, and deployment
surface required for a scanner-style product.

The recommended scanner shape is:

- intake layer:
  authenticated operator form or consent-aware public form
- orchestration layer:
  create workspace and project, then trigger the audit path
- evidence layer:
  brand facts, reports, artifacts, SoV snapshots, validator outputs
- delivery layer:
  operator dashboard, exported report, or customer-facing summary page

This is enough to build:

- internal agency scanner
- client-gated audit intake
- semi-public scanner with manual review

It is not yet a finished abuse-resistant public SaaS with billing, rate
isolation, queue tenancy, and legal consent management.

## 6. Operational patterns worth preserving

Several design patterns are important for keeping the system reliable:

- review-first execution instead of blind writeback
- retries with explicit terminal failure states
- recurring scheduling instead of one-off audits only
- fact drift and trust surface checks, not rankings-only logic
- command routing so agents choose the right surface first
- public proof pages so claims can be verified outside the app

## 7. Operational risks and guardrails

The main risks are operational, not conceptual:

- a deployment can appear healthy while a deeper audit flow is still miswired
- a scanner surface can create legal or trust issues if it scans third-party
  domains without explicit user intent or verification
- public intake requires abuse controls, queue protection, and clearer
  ownership boundaries than the current core product

Guardrails already present in the repository:

- `make verify-demo`
- `make agent-self-check`
- CI for markdown, scripts, Python, docs, and security reporting
- EN/RU user-facing synchronization discipline

## 8. Recommended next step

If the goal is "anyone can deploy their own scanner", the next engineering step
is not a rewrite. The right step is to add:

- a dedicated intake page
- consent or ownership verification for active scanning
- async queue and job status visibility
- stronger export and notification delivery
- explicit public-service limitations in the UI and docs

That extends the existing architecture instead of replacing it.
