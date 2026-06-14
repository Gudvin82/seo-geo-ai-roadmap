# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/markdown-lint.yml)
[![Script Smoke Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/script-smoke-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/script-smoke-tests.yml)
[![Python Tests](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/python-tests.yml)
[![Docs Build](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/docs-site.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/docs-site.yml)
[![Security Scans](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/security-scans.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/security-scans.yml)
[![Coverage](https://img.shields.io/badge/coverage-pytest--cov%20artifact-2ea44f)](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/.github/workflows/python-tests.yml)
[![Docker](https://img.shields.io/badge/docker-self--hosted-2496ED?logo=docker&logoColor=white)](./docker-compose.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-app-009688?logo=fastapi&logoColor=white)](./app/backend/app/main.py)
![Self-Hosted Ready](https://img.shields.io/badge/self--hosted-ready-1f6f50)

Бесплатная, прозрачная, self-hosted платформа для SEO, GEO и AI
discoverability. Ее можно развернуть на своем компьютере или сервере,
подключить свои AI providers, запускать аудиты, отслеживать AI Share of Voice,
вести brand facts и выдавать двуязычные отчеты без обязательного paid cloud.

[English version](./README.md)
[Карта документации](./DOCS_INDEX_RU.md)

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

## Публичное обещание, точно

Репозиторий уже поддерживает три реальных публично безопасных режима:

1. ручное использование как framework
1. AI-agent-assisted аудит и delivery
1. self-hosted product foundation для своего scanner или audit-сервиса

Чем он не является:

- hosted SaaS, который поддерживает автор репозитория
- enterprise SLA продукт из коробки
- тихий autopilot, который меняет production-сайты без review

Перед публичными формулировками используйте:

- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
- [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)

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

- Карта docs: [DOCS_INDEX_RU.md](./DOCS_INDEX_RU.md)
- Быстрый вход для человека: [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
- Быстрый вход для ИИ: [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- Онбординг за 15 минут: [docs/ru/15-minute-onboarding-v450.md](./docs/ru/15-minute-onboarding-v450.md)
- Публичная readiness-рамка: [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- One-day blueprint сервиса: [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
- One-click deploy options: [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
- Матрица production-flow интеграций: [docs/ru/integration-production-matrix-v450.md](./docs/ru/integration-production-matrix-v450.md)
- Каталог провайдеров: [docs/ru/provider-catalog-v450.md](./docs/ru/provider-catalog-v450.md)
- Сводка релиза v4.6.0: [docs/ru/v460-release.md](./docs/ru/v460-release.md)
- Сводка релиза v4.5.2: [docs/ru/v452-release.md](./docs/ru/v452-release.md)
- Сводка релиза v4.5.0: [docs/ru/v450-release.md](./docs/ru/v450-release.md)
- Deployment: [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- Verification: [VERIFY_DEPLOYMENT_RU.md](./VERIFY_DEPLOYMENT_RU.md)
- API reference: [docs/ru/api-reference.md](./docs/ru/api-reference.md)
- Hosted validator: [docs site validator](./docs_site/validator.md)
- Scanner foundation: [docs/ru/public-scanner-v360.md](./docs/ru/public-scanner-v360.md)
- Discoverability coverage: [docs/ru/discoverability-coverage-v370.md](./docs/ru/discoverability-coverage-v370.md)
- AI guidance file: [docs/ru/ai-txt.md](./docs/ru/ai-txt.md)
- Command surface: [docs/ru/command-catalog-v340.md](./docs/ru/command-catalog-v340.md)
- v3.8 command UX: [docs/ru/command-catalog-v380.md](./docs/ru/command-catalog-v380.md)
- Graph intelligence: [docs/ru/graph-intelligence-v380.md](./docs/ru/graph-intelligence-v380.md)
- GTM and distribution: [docs/ru/distribution-and-gtm-v380.md](./docs/ru/distribution-and-gtm-v380.md)
- Research loop: [docs/ru/research-build-improve-repeat-v380.md](./docs/ru/research-build-improve-repeat-v380.md)
- Framework integrations: [docs/ru/framework-integrations-v380.md](./docs/ru/framework-integrations-v380.md)
- Integration production flows: [docs/ru/integration-production-flows-v380.md](./docs/ru/integration-production-flows-v380.md)
- v4.2 production proof: [docs/ru/v420-production-proof.md](./docs/ru/v420-production-proof.md)
- v4.3 response на внешний review и upgrade path: [docs/ru/v430-review-response-and-upgrade-path.md](./docs/ru/v430-review-response-and-upgrade-path.md)
- v4.3 public case studies: [docs/ru/v430-case-anmalishev.md](./docs/ru/v430-case-anmalishev.md), [docs/ru/v430-case-auditguard-sitepravo.md](./docs/ru/v430-case-auditguard-sitepravo.md)
- Product modes: [docs/ru/product-modes-v380.md](./docs/ru/product-modes-v380.md)
- CI gating: [docs/ru/ci-gating-v380.md](./docs/ru/ci-gating-v380.md)
- Executive dashboard: [docs/ru/executive-dashboard-v380.md](./docs/ru/executive-dashboard-v380.md)
- AI Agent Mode: [docs/ru/ai-agent-mode-v400.md](./docs/ru/ai-agent-mode-v400.md)
- Product surfaces: [docs/ru/product-surfaces-v400.md](./docs/ru/product-surfaces-v400.md)
- Managed API boundary: [docs/ru/managed-api-v400.md](./docs/ru/managed-api-v400.md)
- Extensions and automation: [docs/ru/extensions-and-automation-v400.md](./docs/ru/extensions-and-automation-v400.md)
- Bootstrap guide: [docs/ru/bootstrap-guide-v340.md](./docs/ru/bootstrap-guide-v340.md)
- Architecture note: [ARCHITECTURE_NOTE_RU.md](./ARCHITECTURE_NOTE_RU.md)
- Evaluation kit: [EVALUATE_THIS_REPO_RU.md](./EVALUATE_THIS_REPO_RU.md)
- Evaluate first prompt: [EVALUATE_THIS_REPO_FIRST_RU.md](./EVALUATE_THIS_REPO_FIRST_RU.md)
- Commercial boundary: [COMMERCIAL_ROADMAP_RU.md](./COMMERCIAL_ROADMAP_RU.md)

## AI-agent scenario prompts

Для команд, которые хотят просто дать репозиторий Cursor, Claude Code, Codex
или другому AI coding agent без ручного сочинения prompt:

- [Prompt: оценка репозитория и сайта](./prompts/ru/repo-site-audit-agent-prompt.md)
- [Prompt: развернуть client scanner](./prompts/ru/deploy-client-scanner-agent-prompt.md)
- [Prompt: улучшить существующий сайт](./prompts/ru/improve-existing-site-agent-prompt.md)

## Что добавляет `v4.6.0`

- first-class starter integrations для Google Ads, IndexNow, Google Business Profile, Yandex Business, Merchant Center, Meta Ads, VK Ads, Telegram, YouTube, LinkedIn и Instagram или Facebook organic
- executive dashboard, который разделяет Google, RU, local-business и distribution layers
- более сильную сравнительную рамку для organic demand, paid demand, AI visibility и landing-page conversion

## Что добавляет `v4.5.2`

- еще 10 hosted или online providers и еще 10 local или self-hosted runtimes
- first-class контракт интеграции `yandex_direct` и starter sync path
- machine-readable service-foundation endpoint для branded scanner или audit service
- более сильную упаковку product foundation для команд, которые хотят self-hosted развернуть репозиторий и превратить его в свой клиентский сервис

## Что добавляет `v4.5.0`

- полностью зеленый root-plus-backend pytest path без оговорок
- более сильные scanner abuse controls, queue visibility и notification retries
- environment-aware integration verification для GSC, GA4, Yandex и CrUX
- заметно более широкий каталог hosted и local providers
- более ясная docs consolidation через явные актуальные entrypoints и onboarding за 15 минут
- более четкая маршрутизация по RU market depth через Yandex и RU GEO entrypoints

## Что добавляет `v4.4.0`

- явную public-product readiness-рамку, чтобы репозиторий можно было точно описывать в публичных постах и внешних оценках
- one-day blueprint для превращения репозитория в свой scanner или audit-сервис
- более ясные one-click deploy options для local demo, Docker VPS, Coolify, Railway, Render и Kubernetes starter paths
- AI-agent scenario prompts для оценки репозитория и сайта, разворачивания client scanner и улучшения существующего сайта
- более сильный routing через README, AI handoff, deployment docs, docs-site и proof-layer для истории про self-hosted product foundation

## Что добавляет `v4.1.0`

- более жесткий scan-job access control для tasks и graph runtime, чтобы scanner sessions оставались приватными по умолчанию
- redirect-aware защита scanner fetch и webhook с ограничением public ports и response size
- recoverable DB-backed scan worker semantics вместо thread-only fire-and-forget выполнения
- governed CMS change requests с lifecycle preview → approve → apply → verify → rollback
- report assistant endpoint и app-surface для operator Q&A по сохраненным отчетам
- более сильные production-flow и CI-readiness paths для GSC, GA4, Yandex и CMS integrations
- еще более четкое разделение scanner / product-app / repo-operator surfaces плюс расширенные machine-readable contracts
- trusted delivery targets и генерация PR proposal с auto-merge eligibility flags для trusted repositories
- реальный Telegram webhook runtime, более зрелые Chrome и VS Code operator packages и managed-cloud Kubernetes pack

## Что добавляет `v4.2.0`

- аудит AI readability для видимой структуры, machine-readable guidance layers и answer-ready блоков
- heuristic citability scoring с machine-readable breakdown и quick wins
- проверка CDN или edge-блокировок для GPTBot, ClaudeBot и PerplexityBot
- проверка RAG chunk readiness для длинных секций, heading depth и definition-style контента
- путь для CrUX field data и новый integration verification matrix endpoint
- расширенное покрытие провайдеров: OpenAI, Anthropic, Gemini, Perplexity, Mistral, Cohere, DeepSeek, xAI или Grok, Ollama, LocalAI и vLLM
- stack packs для WordPress, React и Angular
- optional Lighthouse CI path для PR-level synthetic gating

## Что добавляет `v4.3.0`

- двуязычные public case studies по `anmalishev.ru`, `auditguard.ru` и `sitepravo.ru`
- структурированный ответ на внешнюю критику репозитория с вердиктами: `true`, `partial`, `outdated` или `not yet proven`
- конкретный план “как дойти до 10/10” по proof loops, integration maturity, docs consolidation, cost governance и monitoring
- более сильный real-case слой внутри `REAL_CASES.md`, а не только абстрактные bounded models

## Что добавляет `v4.0.0`

- реальный AI Agent Mode contract, overview и run surfaces с безопасной action boundary
- one-click URL audit result flow с прямыми входами в task generation и graph runtime
- нормализованные task bundles и export adapters, включая реальный GitHub Issues path
- динамический graph intelligence из live scan или audit data, а не только из статичных demo-режимов
- явная managed/public API boundary и более сильные machine-readable contracts в `contracts/*.schema.json`
- first-class GitHub Action path плюс честные scaffolds для VS Code, Chrome и Telegram
- более четкое разделение scanner / product-app / repo-operator surfaces в docs, app и API

## Что добавляет `v3.8.0`

- канонический `/geo ...` command UX с алиасами, примерами, outputs и use-case packaging
- interactive graph intelligence layer для структуры сайта, discoverability surfaces, issue dependencies и trust mapping
- более сильную distribution и GTM-упаковку для agencies, founders, consultants и in-house команд
- более ясный operating loop research → build → improve → re-measure
- reporting packs для executive summaries, fix packs и graph snapshots
- более понятные framework integration guidance для self-hosted scanner и delivery flows
- production-guided GSC, Yandex и CMS contracts с CI-aware next steps
- более полноценный executive dashboard и более четкое разделение repo, app и scanner modes

## Что добавляет `v3.3.0`

- hosted или deploy-ready поверхность для `llms.txt` validator
- явная retry-модель и terminal failure semantics
- рабочие scheduling modes для регулярных проверок
- более безопасная CMS writeback boundary с review-first execution
- security scanning и coverage generation в CI
- docs по fact drift, trust surfaces, ROI и executive reporting
- public evaluation и proof-review assets

## Что добавляет `v3.4.0`

- GEO command surface для AI agents и операторов
- command-router API и CLI routing script
- self-hosted bootstrap planner для demo и production-like setup
- более ясные modular docs "how it works" и scoring model
- более сильная adoption-поверхность без отказа от self-hosted-first honesty

## Что добавляет `v3.5.0`

- встроенные AI handoff task packs, чтобы пользователю не приходилось писать prompt самому
- scanner-oriented bootstrap mode для команд, которые строят client-facing intake surface
- публичная архитектурная справка на EN и RU с описанием deployment, audit flow и развития scanner-контура
- расширение command-catalog под `deploy` и `scanner` сценарии

## Что добавляет `v3.7.0`

- реальное RU/Yandex AI hardening с отдельной политикой для `YandexAdditional`
- практическая валидация `ai.txt` и проверка противоречий с `robots.txt` и `llms.txt`
- аудит покрытия structured data с поддержкой `WebSite` schema
- эвристический detector FAQ / answer-ready блоков
- проверка полноты Open Graph и Twitter Card
- интегрированная проверка связки `robots.txt` ↔ sitemap
- RU guidance по маркировке AI-контента как practical compliance, а не legal advice

## Что добавляет `v3.6.0`

- dedicated scanner intake page для passive, active и feature-flagged full scan modes
- ownership verification и consent flow для active scanning
- async scan jobs со статусом, событиями, cancellation и artifact visibility
- versioned JSON, markdown, CSV и HTML exports плюс completion hooks
- public-service limitations прямо в UI и docs до запуска скана

## Блок для передачи AI

Передайте этот репозиторий своему AI coding agent и скажите ему:

1. прочитать [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
2. следовать [AGENTS.md](./AGENTS.md)
3. выполнить `python scripts/geo_command_surface.py catalog`
4. выполнить `python scripts/agent_handoff_pack.py --task deploy-demo --language ru`
5. выполнить `python scripts/bootstrap_self_hosted.py --mode demo --format markdown`
6. выполнить `make turnkey-demo`
7. выполнить `make agent-self-check`
8. если нужен scanner intake, открыть `app/frontend/scanner.html` и пройти встроенный verification/status flow
9. если нужно объяснение или приоритизация, открыть `app/frontend/graph.html` и использовать `/geo graph`
10. отдельно отчитаться, что реально проверено, что смоделировано и где нужен
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
- Публичная архитектурная справка: [ARCHITECTURE_NOTE_RU.md](./ARCHITECTURE_NOTE_RU.md)
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

`v3.2.0` делает GEO/AI-слой более decision-grade:

- три явных outcome-слоя: rankings, AI visibility и conversion trust
- measurement maturity framing, чтобы proxy-метрики не продавались как абсолютная правда
- priority maps, AI-surface playbooks, RU LLM context и anti-hype guardrails
- linkable operator tool: standalone `llms.txt` validator с public API

`v3.3.0` добавляет operational proof слой:

- hosted/deploy-ready validator page через docs site
- retry semantics для provider calls, notifications и governed CMS preparation
- documented recurring execution model для scheduled checks
- fact drift detection, trust-surface mapping, executive summaries и ROI framing
- более ясный commercial boundary и public evaluation flow

В `v3.0.0` были зафиксированы два proof-first слоя:

- AI Citation Score: прозрачный сигнал 0-100, показывающий, упоминается ли
  бренд, цитируется ли он и насколько качественно описан в структурированных AI
  SoV-проверках
- Prioritization engine: impact, effort, confidence и benchmark status для
  findings по LCP, CLS, INP, schema coverage, factual consistency и AI
  readiness

Подробнее:

- [docs/ru/ai-citation-score.md](./docs/ru/ai-citation-score.md)
- [docs/ru/api-reference.md](./docs/ru/api-reference.md)
- [docs/ru/patch-mode.md](./docs/ru/patch-mode.md)
- [docs/ru/client-delivery.md](./docs/ru/client-delivery.md)
- [docs/ru/search-data-connectors.md](./docs/ru/search-data-connectors.md)
- [docs/ru/cms-connectors.md](./docs/ru/cms-connectors.md)
- [docs/ru/geo-measurement-maturity.md](./docs/ru/geo-measurement-maturity.md)
- [docs/ru/geo-priority-maps.md](./docs/ru/geo-priority-maps.md)
- [docs/ru/geo-ai-surfaces.md](./docs/ru/geo-ai-surfaces.md)
- [docs/ru/answer-ready-patterns.md](./docs/ru/answer-ready-patterns.md)
- [docs/ru/entity-seo-and-kg.md](./docs/ru/entity-seo-and-kg.md)
- [docs/ru/geo-red-team-and-risks.md](./docs/ru/geo-red-team-and-risks.md)
- [docs/ru/llms-validator.md](./docs/ru/llms-validator.md)
- [docs/ru/ai-visibility-check-action.md](./docs/ru/ai-visibility-check-action.md)
- [docs/ru/telegram-sov-alerts.md](./docs/ru/telegram-sov-alerts.md)
- [app/frontend/llms-validator.html](./app/frontend/llms-validator.html)

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
- enterprise SLA в текущем релизе
- полностью turnkey enterprise SSO или live billing automation в текущем релизе
- замену technical SEO одним только GEO

См. [KNOWN_LIMITATIONS_RU.md](./KNOWN_LIMITATIONS_RU.md).

## Latest changes

- `v4.1.0`: security hardening, recoverable scanner execution, governed CMS lifecycle,
  report assistant, trusted delivery targets, Telegram webhook runtime,
  repo-ready Chrome/VS Code packages и managed cloud deployment assets
- `v4.0.0`: AI Agent Mode, one-click URL audit result flow, task generation and export,
  dynamic graph runtime, managed API boundary, contracts catalog, GitHub Action path,
  and VS Code / Chrome / Telegram scaffolds
- `v3.6.0`: dedicated scanner intake page, ownership verification и consent flow,
  async scan jobs, versioned export artifacts, notification hooks и public
  limitations в UI и docs
- `v3.5.0`: встроенные AI handoff task packs, scanner-oriented bootstrap mode,
  публичные EN/RU архитектурные справки и расширение command surface для
  deploy/scanner сценариев
- `v3.4.0`: GEO command surface, command-router API, bootstrap planner,
  modular how-it-works docs, scoring-model clarification и более сильный
  AI/operator onboarding
- `v3.3.0`: hosted/deploy-ready validator page, docs по retry и scheduling,
  первая practical fact-drift implementation, более безопасная CMS writeback
  boundary, security scans, coverage artifacts, governance docs, executive
  reporting assets и public evaluation surfaces
- `v3.2.0`: GEO/AI deep-dive docs, measurement maturity, priority maps,
  AI-surface playbooks, answer-ready и entity/KG layers, anti-hype docs,
  RU LLM guidance, `llms.txt` validator, AI Visibility Check example и
  расширенные JSON-LD templates
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
