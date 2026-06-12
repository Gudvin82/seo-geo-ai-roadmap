# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml)
[![Script Smoke Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml)
[![Python Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml)
[![Docs Build](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml)
[![Docker](https://img.shields.io/badge/docker-self--hosted-2496ED?logo=docker&logoColor=white)](./docker-compose.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-app-009688?logo=fastapi&logoColor=white)](./app/backend/app/main.py)
![Self-Hosted Ready](https://img.shields.io/badge/self--hosted-ready-1f6f50)

Бесплатная, прозрачная, self-hosted платформа для SEO, GEO и AI
discoverability. Ее можно развернуть на своем компьютере или сервере,
подключить свои AI providers, запускать аудиты, отслеживать AI Share of Voice,
вести brand facts и выдавать двуязычные отчеты без обязательного paid cloud.

[English version](./README.md)

## Что это такое

У репозитория три связанных слоя:

- Framework: методология, промпты, шаблоны, чеклисты и скрипты
- Platform: self-hosted приложение для операторов, команд и клиентской выдачи
- Service system: повторяемый способ аудита, приоритизации, исправлений и
  повторных прогонов

Наша главная разница не в том, что здесь "много документации". Разница в том,
что это одна практическая система, которую человек или AI coding agent может
использовать под ключ:

1. развернуть
2. подключить provider(s)
3. запустить реальный аудит
4. получить reports и artifacts
5. расставить приоритеты
6. повторно прогнать и показать дельты

## Для кого

- Агентства с регулярными аудитами и клиентской отчетностью
- In-house SEO, growth, content и AI operations команды
- Фаундеры и экспертные операторы, ведущие свои мультиязычные сайты
- Команды, работающие одновременно с английскими и русскоязычными рынками

## Для кого это не подходит

- Командам, которым нужен black-box crawler без human review
- Пользователям, которым нужен только hosted SaaS без self-hosted сценария
- Тем, кто ищет GEO-хайп вместо технической SEO-дисциплины
- Тем, кто хочет обещаний без доказательств, evidence и governance

## Что происходит за 15 минут, 30 дней и 90 дней

### За 15 минут

- клонируете репозиторий
- поднимаете стек
- входите в систему
- создаете один workspace и один project
- подключаете одного провайдера или остаетесь в прозрачном starter-режиме
- запускаете один audit и одну AI SoV-проверку
- открываете report и export package

### За 30 дней

- вы уходите от разовых аудитов к повторяемому операционному циклу
- факты, промпты и доказательства живут в одной системе
- можно показывать дельты по score и visibility себе или клиентам

### За 90 дней

- у вас появляется переиспользуемая операторская система вместо ad hoc SEO
- AI SoV, factual consistency и отчетность становятся регулярной практикой
- agency, in-house и founder режимы могут жить в одном контуре

## Сценарии по результату

- Agency mode: отдельный workspace на клиента, отдельный project на сайт,
  двуязычная отчетность, AI-assisted приоритизация, экспортируемые artifacts
- In-house mode: единый truth center, регулярные аудиты, provider-backed AI
  SoV и evidence-driven backlog для продукта, контента и разработки
- Founder mode: один self-hosted стек для аудитов сайта, AI visibility checks,
  fact governance и повторных прогонов без vendor lock-in

## С чего начать

- Быстрый вход для человека: [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
- Быстрый вход для ИИ: [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- Deployment: [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- Verification: [VERIFY_DEPLOYMENT_RU.md](./VERIFY_DEPLOYMENT_RU.md)
- API reference: [docs/ru/api-reference.md](./docs/ru/api-reference.md)

## Блок для передачи AI

Передайте этот репозиторий своему AI coding agent и скажите ему:

1. прочитать [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
2. следовать [AGENTS.md](./AGENTS.md)
3. выполнить `make turnkey-demo`
4. выполнить `make agent-self-check`
5. отдельно отчитаться, что реально проверено, что смоделировано и где нужен
   human review

Репозиторий специально собран так, чтобы AI-агент мог развернуть его с нуля и
сохранить синхронность EN/RU-операционного слоя.

## Product proof

Ниже скриншоты из реального локального app-flow, а не placeholder-схемы. Если
вам нужен live demo, используйте локальный demo-flow ниже. Постоянный публичный
SaaS demo в этом репозитории не обещается.

![Login and dashboard proof](./docs_site/assets/screenshots/app-login-dashboard-proof.png)
![Provider configuration proof](./docs_site/assets/screenshots/app-provider-proof.png)
![Audit run proof](./docs_site/assets/screenshots/app-audit-proof.png)
![Report and artifact proof](./docs_site/assets/screenshots/app-report-proof.png)

## Зачем нужен этот репозиторий

Большинство SEO-репозиториев заканчиваются на советах. Большинство GEO-дискуссий
заканчиваются на теории. Большинство AI-инструментов скрывают scoring,
привязывают к облаку или игнорируют русскоязычные рынки. Этот проект строится в
обратную сторону:

- self-hosted first
- прозрачные метрики
- двуязычность с первого дня
- human-usable и AI-agent-usable
- proof before claims
- technical SEO плюс GEO/AI, а не GEO вместо SEO

## Что внутри

- App layer: [`app`](./app)
- Документация: [`docs/en`](./docs/en) и [`docs/ru`](./docs/ru)
- Чеклисты: [`checklists`](./checklists)
- Prompt library: [`prompts`](./prompts)
- Шаблоны: [`templates`](./templates)
- Примеры: [`examples`](./examples)
- Скрипты: [`scripts`](./scripts)
- Архитектура: [ARCHITECTURE_RU.md](./ARCHITECTURE_RU.md)
- Positioning: [POSITIONING.md](./POSITIONING.md)
- Реальные кейсы: [REAL_CASES_RU.md](./REAL_CASES_RU.md)
- Operations runbook: [OPERATIONS_RUNBOOK_RU.md](./OPERATIONS_RUNBOOK_RU.md)
- Ограничения: [KNOWN_LIMITATIONS_RU.md](./KNOWN_LIMITATIONS_RU.md)

## App quickstart

- Frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/healthz`
- Readiness: `http://localhost:8000/readyz`
- Metrics: `http://localhost:8000/metrics`

### Turnkey local demo

```bash
make turnkey-demo
make verify-demo
make agent-self-check
```

Ожидаемые demo credentials:

- Email: `demo@example.com`
- Password: `DemoPlatform123`

## Канонический operator flow

1. Создать workspace
2. Создать project
3. Заполнить brand facts
4. Настроить providers
5. Запустить audit
6. Открыть report и artifacts
7. Запустить AI SoV
8. Расставить приоритеты fixes
9. Повторно прогнать после изменений
10. Экспортировать client или internal delivery pack

## Прозрачный scoring и implementation output

В `v3.0.0` зафиксированы два proof-first слоя:

- AI Citation Score: прозрачный сигнал 0-100, показывающий, упоминается ли
  бренд, цитируется ли он и насколько качественно описан в структурированных AI
  SoV-проверках
- Prioritization engine: impact, effort, confidence и benchmark status для
  findings по LCP, CLS, INP, schema coverage, factual consistency и AI
  readiness

Подробнее:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/ru/api-reference.md](./docs/ru/api-reference.md)
- [docs/ru/patch-mode.md](./docs/ru/patch-mode.md)
- [docs/ru/client-delivery.md](./docs/ru/client-delivery.md)
- [docs/ru/search-data-connectors.md](./docs/ru/search-data-connectors.md)
- [docs/ru/cms-connectors.md](./docs/ru/cms-connectors.md)

## Реальные кейсы

`v3.0.0` расширяет слой real cases честными и ограниченными public-site
snapshot-оценками для:

- `sitepravo.ru`
- `auditguard.ru`
- `anmalishev.ru`

См. [REAL_CASES_RU.md](./REAL_CASES_RU.md).

## Дисциплина верификации

Перед тем как считать релиз завершенным, используйте:

- `make verify-demo`
- `make agent-self-check`
- `PYTHONPATH=app/backend ./.venv/bin/python -m pytest app/backend/tests`
- `./.venv/bin/python -m mkdocs build`

## Честные границы

Проект не заявляет:

- полностью автономное исправление без human review
- гарантированные AI citations на волатильных AI surfaces
- enterprise SLA, SSO или billing в текущем релизе
- замену technical SEO одним только GEO

См. [KNOWN_LIMITATIONS_RU.md](./KNOWN_LIMITATIONS_RU.md).

## Latest changes

- `v3.1.0`: starter-интеграции с search/analytics, CMS connector flows,
  patch packs, client delivery packs, import project package, более сильный
  white-label слой, review-mode guidance и расширенный EN/RU operator layer
- `v3.0.0`: proof-first positioning rewrite, stronger onboarding, реальные
  app-скриншоты, документация по AI Citation Score, prioritization engine,
  provider-backed AI SoV, structured observability, role/invite hardening и
  более сильный EN/RU operator layer
- `v2.3.0`: сохранение AI SoV в приложении, metadata-rich prompt library,
  webhook notifications, project export package, top-20 local LLM matrix и
  benchmark/search-data documentation
- `v2.2.0`: operator-ready platform upgrade с permissions, invites и
  verify-demo discipline

## Лицензия

Репозиторий распространяется по лицензии из [LICENSE](./LICENSE).
