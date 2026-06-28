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

Бесплатная, прозрачная, self-hosted платформа для SEO, GEO и AI
discoverability. Она объединяет:

- слой методологии
- реальный app layer
- scripts и validation helpers
- AI-agent task packs
- двуязычные operator и client-delivery flows

[English version](./README.md)
[Карта документации](./DOCS_INDEX_RU.md)

## Что это за репозиторий на самом деле

Этот repo нужно понимать как систему из трех слоев:

1. Framework
   Методология, playbooks, prompts, checklists, templates и scripts.
2. Platform
   Self-hosted FastAPI app с auth, workspaces, projects, audits, reports,
   scanner flows, exports и integrations.
3. Service system
   Повторяемый способ проводить аудит, приоритизировать, исправлять, проверять и
   повторно прогонять.

Смысл не в том, что здесь “много документации”.

Смысл в одной end-to-end operating system, которой реально может пользоваться
человек или AI coding agent.

## Честное публичное обещание

Безопасные формулировки:

- ручное использование как framework
- AI-agent-assisted аудит и delivery
- self-hosted foundation для своего scanner или audit service

Небезопасные формулировки:

- готовый hosted SaaS с uptime от автора
- enterprise-продукт без настройки
- ИИ, который тихо чинит production-сайты сам

Перед публичными формулировками прочитайте:

- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [WHAT_THIS_PROJECT_IS_RU.md](./WHAT_THIS_PROJECT_IS_RU.md)
- [WHAT_THIS_PROJECT_IS_NOT_RU.md](./WHAT_THIS_PROJECT_IS_NOT_RU.md)
- [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
- [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)

## Чем репозиторий отличается

Большинство repo в этой нише останавливаются на чем-то одном:

- методология без runtime
- scanner без честной методологии
- набор prompts без product layer
- оболочка продукта со скрытым scoring и неясным proof

Этот репозиторий пытается связать:

- technical SEO
- GEO и AI visibility
- RU и Yandex reality
- factual consistency
- operator evidence
- task export и repeatable delivery

## Core path

Если вы открыли repo впервые, идите так:

1. [README_RU.md](./README_RU.md)
2. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
3. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
4. [REAL_CASES_RU.md](./REAL_CASES_RU.md)
5. [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md) или [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
6. [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
7. [DOCS_ARCHIVE_RU.md](./DOCS_ARCHIVE_RU.md)

## Глубокие практические playbooks

Это ключевые “substance-first” документы v6:

- [Technical SEO Deep Playbook](./docs/ru/technical-seo-deep-playbook.md)
- [Semantic Core and Intent Playbook](./docs/ru/semantic-core-and-intent-playbook.md)
- [Competitor Gap and Authority Playbook](./docs/ru/competitor-gap-and-authority-playbook.md)
- [GEO and AI Operations Playbook](./docs/ru/geo-ai-operations-playbook.md)

## Путь SEO intelligence

- `/api/v1/settings/seo-intelligence-center`
- `scripts/keyword_research_stub.py`
- `scripts/competitor_intelligence_stub.py`
- `scripts/backlink_intelligence_stub.py`
- `scripts/rank_tracking_stub.py`

## Доказательства и кейсы

- [REAL_CASES_RU.md](./REAL_CASES_RU.md)
- [публичный аудит anmalishev.ru](./docs/ru/v600-case-anmalishev-audit.md)
- [anmalishev.ru before/after case](./docs/ru/v430-case-anmalishev.md)
- [auditguard.ru + sitepravo.ru case](./docs/ru/v430-case-auditguard-sitepravo.md)

## Путь для AI-агента

Для Cursor, Claude Code, Codex, VS Code и подобных агентов:

- [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- [AGENTS.md](./AGENTS.md)
- [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
- [prompts/ru/repo-site-audit-agent-prompt.md](./prompts/ru/repo-site-audit-agent-prompt.md)
- [prompts/ru/deploy-client-scanner-agent-prompt.md](./prompts/ru/deploy-client-scanner-agent-prompt.md)
- [prompts/ru/improve-existing-site-agent-prompt.md](./prompts/ru/improve-existing-site-agent-prompt.md)

## Self-hosted path

- [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- [VERIFY_DEPLOYMENT_RU.md](./VERIFY_DEPLOYMENT_RU.md)
- [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
- [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
- `make turnkey-demo`

## Что такое чеклисты и чем они не являются

Папка `checklists/` специально компактная.

Эти файлы — это:

- quick execution cards
- QA reminders
- handoff summaries

Сами по себе они не являются всей методологией.

Для серьезной работы сочетайте:

- один deep playbook
- один checklist
- один prompt или task pack
- один script или app flow
- один case или proof reference

## Прозрачный scoring

Репозиторий не заявляет universal SEO truth score.

Он явно раскрывает:

- overall audit scoring
- priority scoring через impact / effort / confidence
- формулу AI Citation Score
- логику benchmark status
- ограничения heuristic scripts

Читайте:

- [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
- [docs/ru/ai-citation-score.md](./docs/ru/ai-citation-score.md)

## На чем сфокусирован v6.6.0

`v6.6.0` делает repo более operator-ready multi-tenant платформой за счет
tenant admin visibility, managed-integration proof, docs consolidation и более
строгой release hygiene поверх зрелости `v6.5.0`.

Он добавляет:

- tenant-admin console для видимости plan posture, quota pressure,
  onboarding state и API keys
- managed-integration center, который собирает GSC, GA4, Ads, Yandex, local
  business, Alice AI и CrUX в одну production-flow матрицу
- docs-consolidation center, чтобы current docs, AI-agent paths,
  service-builder paths и archive policy были явно видны
- более богатую frontend-видимость tenant, docs и integration maturity слоев,
  а не только backend-only surfaces
- более сильную release hygiene для runtime contracts, docs, frontend markers,
  docs build и syntax verification

## Текущие границы

Сильные стороны уже сейчас:

- self-hosted app
- AI-agent-ready workflow
- RU GEO и Yandex framing
- evidence-first reporting
- bounded scoring и repeatable audit flow

Что все еще на уровне foundation:

- часть integrations пока guided или starter-first
- hosted SaaS maturity не входит в текущее обещание
- не каждая SEO-поддисциплина описана на уровне “финальной агентской библии”

Эта граница намеренно обозначена публично.
