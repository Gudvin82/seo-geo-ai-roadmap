# Архитектура

## Модель слоев в v3.0.0

У `seo-geo-ai-roadmap` теперь четыре практических слоя:

1. Методологический слой
   - `docs/`, `checklists/`, `prompts/`, `templates/`, `examples/`
2. Скриптовый слой
   - `scripts/`
3. Приложенческий слой
   - `app/backend/`, `app/frontend/`, `app/shared/`
4. Дистрибуционный слой
   - `docs_site/`, `mkdocs.yml`, `.github/workflows/`

Приложение не заменяет методологию. Оно делает ее операционной.

## Архитектура backend

Базовый стек:

- Python
- FastAPI
- SQLAlchemy
- SQLite как local fallback
- PostgreSQL-ready путь через Docker

Ключевые задачи backend:

- auth и workspace isolation
- настройка providers
- запуск аудитов
- reports и artifacts
- сохранение AI SoV
- observability и structured logs

## Архитектура frontend

Frontend остается намеренно легким:

- статический HTML, CSS и JavaScript
- без обязательного build pipeline
- EN/RU operator labels
- прямое API integration

Так платформа остается deployable в self-hosted средах без тяжелого frontend
dependency tree.

## Что добавлено в v3.0.0

- operator overview pane
- первый onboarding прямо внутри app
- компактные history charts
- более явная видимость provider, audit, report и SoV flow

## Стратегия shared logic

Репозиторий по-прежнему ценит CLI-режим. Платформа должна дополнять scripts, а
не прятать их.

## Честные границы

Текущая архитектура рассчитана на прагматичную self-hosted работу. Это еще не
полноценная enterprise control plane с billing, SSO и warehouse-grade
analytics.
