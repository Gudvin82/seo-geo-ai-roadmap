# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/markdown-lint.yml)
[![Script Smoke Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/script-smoke-tests.yml)
[![Python Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/python-tests.yml)
[![Docs Build](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/docs-site.yml)
[![Security Scans](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/security-scans.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/security-scans.yml)
[![Docker](https://img.shields.io/badge/docker-self--hosted-2496ED?logo=docker&logoColor=white)](./docker-compose.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-app-009688?logo=fastapi&logoColor=white)](./app/backend/app/main.py)

![SEO GEO AI Project Badge](./docs_site/assets/screenshots/project-badge-v530.png)

Free, transparent, self-hosted platform for SEO, GEO, and AI discoverability.
It combines:

- a methodology layer
- a real app layer
- scripts and validation helpers
- AI-agent task packs
- bilingual operator and client-delivery flows

[Русская версия](./README_RU.md)
[Docs map](./DOCS_INDEX.md)

## What this repository really is

This repo should be read as a connected system with three layers:

1. Framework
   Methodology, playbooks, prompts, checklists, templates, and scripts.
2. Platform
   Self-hosted FastAPI app with auth, workspaces, projects, audits, reports,
   scanner flows, exports, and integrations.
3. Service system
   A repeatable way to audit, prioritize, fix, verify, and re-run.

The point is not “more docs”.

The point is one end-to-end operating system that a human operator or AI coding
agent can actually use.

## The honest public promise

Safe claims:

- manual framework use
- AI-agent-assisted audit and delivery
- self-hosted foundation for your own scanner or audit service

Not safe claims:

- finished hosted SaaS with maintainer-operated uptime
- enterprise product with zero setup
- AI that silently fixes production sites by itself

Read this before making public claims:

- [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
- [WHAT_THIS_PROJECT_IS.md](./WHAT_THIS_PROJECT_IS.md)
- [WHAT_THIS_PROJECT_IS_NOT.md](./WHAT_THIS_PROJECT_IS_NOT.md)
- [METHODOLOGY.md](./METHODOLOGY.md)
- [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)

## Why it is different

Most repos in this space stop at one of these:

- a methodology with no runtime
- a scanner with no honest methodology
- a prompt collection with no product surface
- a product shell with hidden scoring and unclear proof

This repository tries to connect:

- technical SEO
- GEO and AI visibility
- RU and Yandex reality
- factual consistency
- operator evidence
- task export and repeatable delivery

## Core path

If you are new, use this path first:

1. [README.md](./README.md)
2. [METHODOLOGY.md](./METHODOLOGY.md)
3. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
4. [REAL_CASES.md](./REAL_CASES.md)
5. [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md) or [WALKTHROUGH.md](./WALKTHROUGH.md)
6. [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
7. [DOCS_ARCHIVE.md](./DOCS_ARCHIVE.md)

## Deep practical playbooks

These are the v6 “substance first” docs:

- [Technical SEO Deep Playbook](./docs/en/technical-seo-deep-playbook.md)
- [Semantic Core and Intent Playbook](./docs/en/semantic-core-and-intent-playbook.md)
- [Competitor Gap and Authority Playbook](./docs/en/competitor-gap-and-authority-playbook.md)
- [GEO and AI Operations Playbook](./docs/en/geo-ai-operations-playbook.md)

## SEO intelligence path

- `/api/v1/settings/seo-intelligence-center`
- `scripts/keyword_research_stub.py`
- `scripts/competitor_intelligence_stub.py`
- `scripts/backlink_intelligence_stub.py`
- `scripts/rank_tracking_stub.py`

## Evidence and cases

- [REAL_CASES.md](./REAL_CASES.md)
- [anmalishev.ru public audit case](./docs/en/v600-case-anmalishev-audit.md)
- [anmalishev.ru before/after case](./docs/en/v430-case-anmalishev.md)
- [auditguard.ru + sitepravo.ru case](./docs/en/v430-case-auditguard-sitepravo.md)

## AI-agent path

For Cursor, Claude Code, Codex, VS Code, or similar agents:

- [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
- [AGENTS.md](./AGENTS.md)
- [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
- [prompts/en/repo-site-audit-agent-prompt.md](./prompts/en/repo-site-audit-agent-prompt.md)
- [prompts/en/deploy-client-scanner-agent-prompt.md](./prompts/en/deploy-client-scanner-agent-prompt.md)
- [prompts/en/improve-existing-site-agent-prompt.md](./prompts/en/improve-existing-site-agent-prompt.md)

## Self-hosted path

- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [VERIFY_DEPLOYMENT.md](./VERIFY_DEPLOYMENT.md)
- [ONE_CLICK_DEPLOY_OPTIONS.md](./ONE_CLICK_DEPLOY_OPTIONS.md)
- [ONE_DAY_SERVICE_BLUEPRINT.md](./ONE_DAY_SERVICE_BLUEPRINT.md)
- `make turnkey-demo`

## What the checklists are, and what they are not

The `checklists/` folder is intentionally compact.

Those files are:

- quick execution cards
- QA reminders
- handoff summaries

They are not the full methodology by themselves.

For serious work, combine:

- one deep playbook
- one checklist
- one prompt or task pack
- one script or app flow
- one case or proof reference

## Transparent scoring

The repo does not claim a universal SEO truth score.

It exposes:

- overall audit scoring
- priority scoring by impact / effort / confidence
- AI Citation Score formula
- benchmark status logic
- heuristic script boundaries

Read:

- [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)

## v6.3.0 focus

`v6.3.0` turns the repo into a more trustworthy operating system by tightening
the gap between public claims, runtime behavior, and script-first execution.

It adds:

- calibrated GEO/AI guidance that distinguishes Google guidance, provider-specific AI signals, and experimental extras
- OAI-SearchBot coverage plus stronger multi-agent `robots.txt` evaluation
- safer frontend token handling and lower-XSS UI rendering paths
- fuller frontend Docker packaging for scanner, graph, validator, and operator surfaces
- stricter release and security hygiene for scans, docs, and version alignment
- stronger standalone script DX so repo-level tooling matches the AI-agent-ready promise

## Current boundaries

Strong today:

- self-hosted app
- AI-agent-ready workflow
- RU GEO and Yandex framing
- evidence-first reporting
- bounded scoring and repeatable audit flow

Still foundation-level:

- some integrations remain guided or starter-first
- hosted SaaS maturity is outside the current promise
- not every SEO subdiscipline is documented at “final agency bible” depth

That boundary is intentional and public.
