# SEO + GEO + AI Discoverability OS

[![Релиз](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/Gudvin82/seo-geo-ai-roadmap/releases)
[![Лицензия: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Не очередной чеклист по SEO, а рабочая система роста видимости сайта в поиске, AI-ответах и локальных платформах.

[English version](./README.md)

## Зачем нужен этот репозиторий

Этот репозиторий собран как execution-first framework для команд, которым нужна единая практическая система на стыке классического SEO, GEO, AI discoverability, Яндекса, контент-операций, governance, отчетности и релизной дисциплины.

## Что нас отличает

- Двуязычность по умолчанию: EN и RU развиваются как полноценные слои, а не как перевод после факта.
- Google + Yandex + LLM в одном framework: глобальный поиск, русскоязычные рынки и AI-поверхности собраны в одну систему.
- Execution-first структура: документация, чеклисты, промпты, шаблоны, скрипты и примеры усиливают друг друга.
- AI-native слой: `llms.txt`, AI-боты, answer-ready контент, anti-hallucination и AI Share of Voice встроены в основу.
- Governance-ready подход: есть RACI, Definition of Done, roadmap внедрения, релизный процесс и шаблоны отчетности.
- Шире, чем SEO: мы описываем всю систему discoverability, а не только ранжирование страниц.

## Для кого

- In-house SEO, growth и content-команды
- Агентства, работающие и с RU/CIS, и с global markets
- Фаундеры и операционные команды, развивающие мультиязычные сайты
- Команды, которым нужны не теоретические списки, а практические SOP

## Что внутри

- Глубокие двуязычные документы в [`docs/en`](./docs/en) и [`docs/ru`](./docs/ru)
- Исполнительские чеклисты в [`checklists`](./checklists)
- Prompt library в [`prompts`](./prompts)
- Переиспользуемые шаблоны в [`templates`](./templates)
- Скрипты проверки и helper-утилиты в [`scripts`](./scripts)
- Заполненные примеры в [`examples`](./examples)
- Отдельные файлы с positioning, governance, ecosystem и release logic в корне репозитория

## Быстрый старт

1. Прочитайте [POSITIONING.md](./POSITIONING.md) и [DIFFERENTIATORS.md](./DIFFERENTIATORS.md).
2. Начните с [docs/ru/01-audit.md](./docs/ru/01-audit.md).
3. Соберите матрицу страниц через [docs/ru/04-page-matrix.md](./docs/ru/04-page-matrix.md).
4. Настройте AI-видимость через [docs/ru/08-geo-ai-search.md](./docs/ru/08-geo-ai-search.md).
5. Зафиксируйте отчетность через [docs/ru/18-analytics.md](./docs/ru/18-analytics.md) и [ROADMAP.md](./ROADMAP.md).

## Архитектура

```text
repo/
├── README.md / README_RU.md
├── POSITIONING.md / DIFFERENTIATORS.md / ECOSYSTEM_MAP.md
├── ROADMAP.md / RELEASE_PROCESS.md / CHANGELOG.md
├── docs/en и docs/ru
├── checklists/en и checklists/ru
├── prompts/en и prompts/ru
├── templates/ и templates/schema
├── scripts/
├── examples/
└── .github/
```

## Экосистема

Репозиторий не заменяет соседние продукты, а помогает понять, как использовать их внутри discoverability stack. Подробности в [ECOSYSTEM_MAP.md](./ECOSYSTEM_MAP.md).

## Превью roadmap

- Foundation: аудит, архитектура, матрица страниц, техническое SEO, GEO/AI-слой
- Execution: качество контента, Яндекс/RU-специфика, аналитика, governance, DoD
- Expansion: AI brand monitoring, international rollout, релизная дисциплина

## Участие

См. [CONTRIBUTING.md](./CONTRIBUTING.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) и шаблон PR в [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md).
