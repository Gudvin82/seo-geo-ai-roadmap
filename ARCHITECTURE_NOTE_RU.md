# Архитектурная справка

Публичная архитектурная справка по `seo-geo-ai-roadmap`, синхронизированная с
состоянием продукта после `v3.5.0`.

## 1. Форма продукта

Репозиторий специально разделен на три переиспользуемые поверхности:

- Методологическая поверхность: docs, prompts, checklists, templates, examples
- Исполнительная поверхность: scripts, API routes, command router,
  operator workflows
- Продуктовая поверхность: self-hosted app, reports, artifacts, delivery paths

Это позволяет использовать проект в трех режимах:

- как репозиторий-методологию без обязательного app-flow
- как self-hosted операторское приложение
- как основу для client-facing или internal scanner-сервиса

## 2. Модель развертывания

Базовая схема развертывания:

- frontend на порту `3000`
- API на порту `8000`
- база через локальный SQLite fallback или PostgreSQL-ready deployment
- docs site как публичный proof, validator и onboarding-слой

Модель развертывания намеренно простая:

- локальный demo-режим
- production-like self-hosted режим
- scanner-oriented режим для intake и выдачи аудитов

Репозиторий не выдает себя за завершенный multi-tenant public SaaS. Это
self-hosted platform foundation, которую можно развивать в эту сторону.

## 3. Исполнительный контур

Базовый operational loop выглядит так:

1. создать workspace
2. создать project
3. зафиксировать canonical brand facts
4. подключить providers
5. запустить audit
6. сохранить reports и artifacts
7. запустить AI SoV и recurring checks
8. сравнивать дельты во времени

Этот же цикл можно поставить за:

- operator dashboard
- AI coding agent handoff
- gated public intake form

## 4. Стратегия AI handoff

Репозиторий собран так, чтобы другому AI-агенту не нужно было каждый раз
сочинять prompt с нуля.

Текущие handoff-слои:

- `START_HERE_FOR_AI*.md`
- `AGENTS.md`
- `AI_HANDOFF_PROMPT*.md`
- `scripts/agent_handoff_pack.py`
- `scripts/geo_command_surface.py`
- `scripts/bootstrap_self_hosted.py`

Это значит, что пользователь может передать ссылку на репозиторий в Cursor,
Claude Code или Codex и указать встроенный task pack, например:

- `audit-site`
- `deploy-demo`
- `deploy-scanner`
- `client-setup`

## 5. Куда развивается scanner-архитектура

В репозитории уже есть audit core, reporting path и deployment surface, которые
нужны для scanner-style продукта.

Рекомендуемая форма scanner-контура:

- intake layer:
  operator form с авторизацией или consent-aware public form
- orchestration layer:
  создание workspace/project и запуск audit path
- evidence layer:
  brand facts, reports, artifacts, SoV snapshots, validator outputs
- delivery layer:
  operator dashboard, export report или customer-facing summary page

Этого достаточно, чтобы сделать:

- internal agency scanner
- client-gated audit intake
- semi-public scanner с ручным review

Но это еще не завершенный abuse-resistant public SaaS с billing, rate
isolation, queue tenancy и полноценно оформленным legal consent management.

## 6. Важные архитектурные паттерны

Нужно сохранять несколько ключевых паттернов:

- review-first execution вместо слепого writeback
- retries с явными terminal failure states
- recurring scheduling, а не только разовые аудиты
- fact drift и trust surface checks, а не логика "только позиции"
- command routing, чтобы агенты начинали с правильной поверхности
- public proof pages, чтобы claims можно было проверить вне app

## 7. Операционные риски и guardrails

Главные риски здесь операционные:

- развертывание может выглядеть healthy, пока deeper audit flow еще не
  провален до конца
- scanner-surface может создавать legal и trust problems, если сканирует
  сторонние домены без явного user intent или verification
- public intake требует abuse controls, queue protection и более явных
  ownership boundaries, чем текущий core product

Guardrails, которые уже есть в репозитории:

- `make verify-demo`
- `make agent-self-check`
- CI для markdown, scripts, Python, docs и security reporting
- дисциплина синхронизации EN/RU user-facing слоя

## 8. Следующий практический шаг

Если цель формулируется как "любой человек может развернуть свой scanner", то
следующий инженерный шаг не в переписывании продукта. Правильный шаг:

- добавить dedicated intake page
- добавить consent или ownership verification для active scanning
- усилить async queue и job status visibility
- усилить export и notification delivery
- явно оформить public-service limitations в UI и docs

Это расширяет текущую архитектуру, а не ломает ее.
