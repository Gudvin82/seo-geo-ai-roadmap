# Архитектура

## Модель слоев v2.0.0

Теперь `seo-geo-ai-roadmap` состоит из четырех понятных слоев:

1. Методологический слой
   - `docs/`, `checklists/`, `prompts/`, `templates/`, `examples/`
   - человекочитаемая логика выполнения
2. Скриптовый слой
   - `scripts/`
   - переиспользуемые CLI-утилиты и валидаторы
3. Приложенческий слой
   - `app/backend/`, `app/frontend/`, `app/shared/`
   - SaaS-ready foundation продукта
4. Дистрибуционный слой
   - `docs_site/`, `mkdocs.yml`, `.github/workflows/`
   - публичная документация и CI/CD

Приложение не заменяет методологию репозитория, а оркестрирует и переиспользует ее.

## Архитектура backend

Стек:

- Python
- FastAPI
- pydantic
- SQLAlchemy
- SQLite как fallback для локальной разработки
- готовность к PostgreSQL через Docker

Структура:

- `app/backend/app/api/` для REST-endpoints
- `app/backend/app/services/` для запуска аудитов и отчетности
- `app/backend/app/providers/` для мультипровайдерной AI-абстракции
- `app/backend/app/models.py` для доменной модели
- `app/backend/tests/` для backend и API-валидации

## Архитектура frontend

Первый frontend сделан намеренно простым:

- статический HTML, CSS и JavaScript
- без обязательного build-step
- двуязычные EN/RU labels
- прямое подключение к FastAPI backend

Это делает продуктовый слой разворачиваемым без лишнего frontend-спrawl.

## Стратегия shared logic

В репозитории уже есть рабочие скрипты в `scripts/`.

Для `v2.0.0` стратегия такая:

- сохранить существующий CLI
- там, где это практично, вызывать те же скрипты из backend services
- оставить `app/shared/` как место для дальнейшего выноса общей логики и схем

Так одна кодовая база поддерживает:

- ручной CLI-режим
- repo-driven usage
- app/API usage

## Доменная модель

В foundation SaaS-слоя входят:

- User
- Workspace
- Project
- Site
- Audit Run
- Report
- Provider Configuration
- Brand Facts Profile
- Prompt Set
- Artifact
- Scheduled Check

Ключевые связи:

- один user -> много workspaces
- один workspace -> много projects
- один project -> много audit runs
- один project -> много artifacts и reports
- один project -> один или несколько truth-center / brand-facts profiles

## Provider abstraction

Первый слой провайдеров поддерживает:

- OpenAI
- Anthropic / Claude
- Gemini
- Perplexity

Цели:

- единый интерфейс для prompt execution
- настройка модели на уровне провайдера
- маршрутизация ключей через env или config
- нормализованная обработка ошибок

## Reporting и evidence flow

Каждый audit run создает:

- статус
- список выбранных проверок
- findings
- score
- artifacts
- структурированные отчеты в Markdown и JSON

Артефакты сохраняются в backend artifact root и отдаются через API.

## Модель деплоя

Поддерживаемый foundation для `v2.0.0`:

- контейнер frontend
- контейнер backend
- контейнер PostgreSQL
- опциональный worker

См.:

- [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md)

## Что будет дальше

Намеренно не входит в `v2.0.0`:

- billing и payments
- enterprise SSO
- сложная tenancy / permissions matrix
- usage metering
- warehouse-grade analytics
- production SLA

Текущий релиз — это сильный foundation продукта, а не раздутый enterprise-комбайн.
