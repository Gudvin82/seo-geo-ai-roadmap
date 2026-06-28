# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml)
[![Script Smoke Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml)
[![Python Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml)
[![Docs Build](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml)
[![Security Scans](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/security-scans.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/security-scans.yml)
[![Docker](https://img.shields.io/badge/docker-self--hosted-2496ED?logo=docker&logoColor=white)](./docker-compose.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-app-009688?logo=fastapi&logoColor=white)](./app/backend/app/main.py)

![SEO GEO AI Project Badge](./docs_site/assets/screenshots/project-badge-v530.png)

[🇬🇧 English](./README.md) | [🇷🇺 Русский root entry](./README_RU.md) | [Карта документации](./DOCS_INDEX_RU.md)

Бесплатная, прозрачная, self-hosted платформа для SEO, GEO и AI
discoverability.

Она объединяет:

- слой методологии
- реальный app layer
- scripts и validation helpers
- AI-agent task packs
- двуязычные operator и client-delivery flows

## Содержание

- [Что Это Такое](#что-это-такое)
- [Для Кого Это](#для-кого-это)
- [Визуальный Roadmap](#визуальный-roadmap)
- [Быстрый Старт За 5 Минут](#быстрый-старт-за-5-минут)
- [Как Использовать Репозиторий](#как-использовать-репозиторий)
- [Пути Обучения](#пути-обучения)
- [Инструменты И Ресурсы](#инструменты-и-ресурсы)
- [Кейсы И Доказательства](#кейсы-и-доказательства)
- [Контрибьютинг И Поддержка](#контрибьютинг-и-поддержка)
- [Roadmap Проекта](#roadmap-проекта)
- [FAQ](#faq)
- [Лицензия](#лицензия)

## Что Это Такое

Этот repo состоит из трех связанных слоев:

1. Framework
   Методология, playbooks, prompts, checklists, templates и scripts.
2. Platform
   Self-hosted FastAPI app с auth, workspaces, projects, audits, reports,
   scanner flows, exports и integrations.
3. Service system
   Повторяемый способ проводить аудит, приоритизировать, исправлять, проверять
   и повторно прогонять.

Прочитайте границы перед публичными обещаниями:

- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [WHAT_THIS_PROJECT_IS_RU.md](./WHAT_THIS_PROJECT_IS_RU.md)
- [WHAT_THIS_PROJECT_IS_NOT_RU.md](./WHAT_THIS_PROJECT_IS_NOT_RU.md)
- [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
- [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)

## Для Кого Это

Лучше всего подходит:

- агентствам с регулярными аудитами и клиентской выдачей
- in-house SEO, content, GEO и AI-командам
- фаундерам, которые строят discoverability-систему для своих сайтов
- AI coding agents, которым нужен понятный путь от repo к аудиту и delivery

Не подходит:

- тем, кто ожидает hosted SaaS от автора
- тем, кто хочет black-box automation без human review
- тем, кто считает GEO заменой technical SEO и качественного контента

## Визуальный Roadmap

Текущий learning и execution path показан здесь:

![Discoverability OS Roadmap](./assets/roadmap-visual.svg)

Поддерживающие документы:

- [DOCS_INDEX_RU.md](./DOCS_INDEX_RU.md)
- [ROADMAP.md](./ROADMAP.md)
- [docs/i18n-status.md](./docs/i18n-status.md)

## Быстрый Старт За 5 Минут

### 1. Откройте правильный entrypoint

- Человек-оператор: [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
- AI-агент: [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- Service builder: [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)

### 2. Выберите один практический путь

- Аудит сайта: [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
- Изучение системы: [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
- Деплой стека: [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- Проверка стека: [VERIFY_DEPLOYMENT_RU.md](./VERIFY_DEPLOYMENT_RU.md)

### 3. Прогоните локальный proof path

```bash
make turnkey-demo
make verify-demo
```

### 4. Посмотрите один публичный proof path

- [REAL_CASES_RU.md](./REAL_CASES_RU.md)
- [docs/ru/v600-case-anmalishev-audit.md](./docs/ru/v600-case-anmalishev-audit.md)

## Как Использовать Репозиторий

Есть три безопасных режима использования:

1. Ручное использование как framework
   Читайте docs, playbooks, prompts, checklists и применяйте сами.
2. AI-agent-assisted аудит и delivery
   Передайте repo в Cursor, Claude Code, Codex, VS Code или похожий агент.
3. Self-hosted product foundation
   Разверните платформу у себя и используйте как основу своего audit или
   scanner service.

Смотрите точные формулировки:

- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [SUPPORT.md](./SUPPORT.md)
- [SECURITY.md](./SECURITY.md)

## Пути Обучения

### Путь A: Освоить методологию

1. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
2. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
3. [docs/ru/technical-seo-deep-playbook.md](./docs/ru/technical-seo-deep-playbook.md)
4. [docs/ru/geo-ai-operations-playbook.md](./docs/ru/geo-ai-operations-playbook.md)

### Путь B: Делать реальную работу

1. [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
2. [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
3. [REAL_CASES_RU.md](./REAL_CASES_RU.md)
4. `make turnkey-demo`

### Путь C: Использовать с AI-агентом

1. [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
2. [AGENTS.md](./AGENTS.md)
3. [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
4. [prompts/ru/repo-site-audit-agent-prompt.md](./prompts/ru/repo-site-audit-agent-prompt.md)

### Путь D: Построить свой сервис

1. [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
2. [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
3. [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
4. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)

## Инструменты И Ресурсы

Текущие практические инструменты и helper paths:

- `/api/v1/settings/seo-intelligence-center`
- `scripts/checklist_generator.py`
- `scripts/semantic_gap_mapper.py`
- `scripts/proof_pack_builder.py`
- `scripts/case_library_builder.py`
- `scripts/synthetic_case_builder.py`
- `scripts/issue_pack_generator.py`
- `scripts/keyword_research_stub.py`
- `scripts/competitor_intelligence_stub.py`
- `scripts/backlink_intelligence_stub.py`
- `scripts/rank_tracking_stub.py`
- `scripts/release_hygiene_check.py`
- `scripts/version_consistency_check.py`

Ключевые ресурсы репозитория:

- [DOCS_INDEX_RU.md](./DOCS_INDEX_RU.md)
- [DOCS_ARCHIVE_RU.md](./DOCS_ARCHIVE_RU.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [ROADMAP.md](./ROADMAP.md)
- [docs/i18n-status.md](./docs/i18n-status.md)

## Кейсы И Доказательства

Базовый evidence path:

- [REAL_CASES_RU.md](./REAL_CASES_RU.md)
- [публичный аудит anmalishev.ru](./docs/ru/v600-case-anmalishev-audit.md)
- [anmalishev.ru before/after case](./docs/ru/v430-case-anmalishev.md)
- [auditguard.ru + sitepravo.ru case](./docs/ru/v430-case-auditguard-sitepravo.md)

Важное правило:

- public proof нужно трактовать как bounded evidence, а не universal guarantee
- разделяйте facts, inferences и operator judgment

## Контрибьютинг И Поддержка

- Гайд по участию: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Кодекс поведения: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- Путь поддержки: [SUPPORT.md](./SUPPORT.md)
- Репортинг безопасности: [SECURITY.md](./SECURITY.md)

## Roadmap Проекта

Активная release path сейчас такая:

- `v6.7.0`: docs and core UX foundation
- `v6.7.5`: operator tools для checklists, semantic mapping и proof packs
- `v6.8.0`: proof, case library, synthetic training packs и issue-pack maturity
- `v6.8.5`: community, launch, and contributor growth layer

Полный план:

- [ROADMAP.md](./ROADMAP.md)

## FAQ

### Это уже публичный hosted SaaS?

Нет. Это бесплатная self-hosted платформа и product foundation, а не
maintainer-operated hosted service.

### Можно ли дать repo AI coding agent?

Да. Это один из first-class supported use modes.

### Это заменяет классическое SEO?

Нет. GEO и AI discoverability — это более высокий слой поверх technical SEO,
semantic coverage, authority, trust и conversion clarity.

### Все integrations уже полностью production-ready и zero-touch?

Нет. Часть integrations уже сильнее и operational-ready, часть еще остается
guided или starter-first. Используйте runtime, readiness и proof layers честно.

## На чем сфокусирован v6.8.5

`v6.8.5` добавляет запланированный community, launch и contributor-growth
layer, чтобы репозиторий было проще публично представлять, улучшать и
маршрутизировать без overclaiming hosted SaaS maturity.

Он добавляет:

- `scripts/community_showcase_builder.py`
- `scripts/launch_pack_generator.py`
- [COMMUNITY_RU.md](./COMMUNITY_RU.md)
- [SHOWCASE_RU.md](./SHOWCASE_RU.md)
- [LAUNCH_PACK_RU.md](./LAUNCH_PACK_RU.md)
- [Community and Launch](./docs/ru/community-and-launch.md)

## Лицензия

Смотрите [LICENSE](./LICENSE).
