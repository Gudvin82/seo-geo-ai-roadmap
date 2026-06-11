# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml)

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
- Полная документация по CLI-скриптам в
  [`scripts/README_RU.md`](./scripts/README_RU.md)
- Заполненные примеры в [`examples`](./examples)
- Глоссарий в [GLOSSARY.md](./GLOSSARY.md) и
  [GLOSSARY_RU.md](./GLOSSARY_RU.md)
- Отдельные файлы с positioning, governance, ecosystem и release logic в корне репозитория

## Быстрый старт

1. Прочитайте [POSITIONING.md](./POSITIONING.md) и [DIFFERENTIATORS.md](./DIFFERENTIATORS.md).
2. Начните с [docs/ru/01-audit.md](./docs/ru/01-audit.md).
3. Соберите матрицу страниц через [docs/ru/04-page-matrix.md](./docs/ru/04-page-matrix.md).
4. Настройте AI-видимость через [docs/ru/08-geo-ai-search.md](./docs/ru/08-geo-ai-search.md).
5. Зафиксируйте отчетность через [docs/ru/18-analytics.md](./docs/ru/18-analytics.md) и [ROADMAP.md](./ROADMAP.md).

## Для AI-агентов и IDE

Если вы используете Codex, Claude Code, Cursor и другие ИИ-агенты, начните с
[AGENTS.md](./AGENTS.md) — это отдельный вход для агентов, где описано, что и
как делать под ключ внутри репозитория.

AGENTS.md дает агенту:

- маршрутизацию типовых turnkey-задач
- карту репозитория и точные entrypoint-файлы
- список ключевых скриптов, с которых надо начинать
- краткий DoD для проверки готовности
- правила, когда надо запрашивать уточнение у пользователя

## Пример скрипта

В репозитории есть не только документы, но и рабочие helper-скрипты. Один из
самых полезных —
[`scripts/generate_llms_txt.py`](./scripts/generate_llms_txt.py), который
собирает `llms.txt` из sitemap.

### Generate llms.txt from sitemap

```bash
python scripts/generate_llms_txt.py \
  --sitemap-url https://example.com/sitemap.xml \
  --output-file ./llms.txt
```

Пример вывода:

```text
Processed URLs: 42
Output file: llms.txt
Warnings:
- Review description for https://example.com/solutions/ai-ops
```

Смотрите [scripts/README_RU.md](./scripts/README_RU.md) для полного описания
CLI-скриптов.

## Пример промпта

Этот prompt помогает быстро получить черновик `llms.txt`, который затем
проверяется вручную.

Purpose: превратить sitemap и ключевые страницы в краткий черновик `llms.txt`.

Input: главная, страницы услуг, FAQ, about page и sitemap.

```text
Роль: technical discoverability specialist
Входы: https://example.com, главная, страницы услуг, FAQ, about page
Задача: подготовь production-ready draft llms.txt с короткими описаниями
Формат ответа: одна строка на URL с кратким описанием
Критерии оценки: краткость, покрытие, дисциплина canonical
```

## Как использовать этот framework на живом проекте

1. Запустите стартовый аудит через
   [docs/ru/01-audit.md](./docs/ru/01-audit.md),
   [checklists/ru/technical-seo-checklist.md](./checklists/ru/technical-seo-checklist.md)
   и [`scripts/sitemap-checker.py`](./scripts/sitemap-checker.py).
2. Исправьте технические блокеры через
   [docs/ru/05-technical-seo.md](./docs/ru/05-technical-seo.md) и
   [`scripts/check-robots-ai-bots.py`](./scripts/check-robots-ai-bots.py).
3. Настройте GEO / AI visibility через
   [docs/ru/08-geo-ai-search.md](./docs/ru/08-geo-ai-search.md),
   [`scripts/generate_llms_txt.py`](./scripts/generate_llms_txt.py) и
   [`prompts/ru/llms-txt-generator-prompt.md`](./prompts/ru/llms-txt-generator-prompt.md).
4. Адаптируйте стратегию под Яндекс/RU или international сценарий через
   [docs/ru/13-russia-yandex.md](./docs/ru/13-russia-yandex.md) и
   [docs/ru/12-international-seo.md](./docs/ru/12-international-seo.md).
5. Усильте content + answer extraction через
   [docs/ru/07-content-eeat.md](./docs/ru/07-content-eeat.md) и
   [prompts/ru/answer-ready-page-prompt.md](./prompts/ru/answer-ready-page-prompt.md).
6. Отслеживайте аналитику и AI Share of Voice через
   [docs/ru/18-analytics.md](./docs/ru/18-analytics.md),
   [`scripts/ai-share-of-voice-tracker.py`](./scripts/ai-share-of-voice-tracker.py)
   , [examples/ai-share-of-voice-weekly-report.md](./examples/ai-share-of-voice-weekly-report.md)
   и sample-данные в
   [examples/ai-sov-report-sample.json](./examples/ai-sov-report-sample.json).
7. Управляйте релизами через [docs/ru/20-raci.md](./docs/ru/20-raci.md),
   [docs/ru/21-definition-of-done.md](./docs/ru/21-definition-of-done.md) и
   [RELEASE_PROCESS.md](./RELEASE_PROCESS.md).

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

## Vibe Coding Protocols

Дополнительно к этому framework есть отдельный репозиторий —
[Vibe Coding Protocols](https://github.com/Gudvin82/vibe-coding-protocols).

Он про:

- протоколы vibecoding, когда система собирается прямо в процессе работы с ИИ и IDE
- легкие итеративные сценарии для AI-assisted разработки
- связку структурированных SOP из этого репозитория с живой экспериментальной работой

Если вам ближе подход “собираем систему по ходу дела, кодим и думаем
одновременно”, Vibe Coding Protocols — естественное дополнение к этому
Discoverability OS.

## Превью roadmap

- Foundation: аудит, архитектура, матрица страниц, техническое SEO, GEO/AI-слой
- Execution: качество контента, Яндекс/RU-специфика, аналитика, governance, DoD
- Expansion: AI brand monitoring, international rollout, релизная дисциплина

## Последние изменения

- `v1.2.0`: добавлены `AGENTS.md`, agent-first onboarding и связка с
  `vibe-coding-protocols`.
- `v1.3.0`: добавлены docs по скриптам, глоссарий, sample AI SoV datasets,
  более строгая валидация `llms.txt` и ROI tooling.

## Что стало заметнее

- См. [GLOSSARY_RU.md](./GLOSSARY_RU.md) для основных терминов.
- См. [examples/ai-sov-report-sample.json](./examples/ai-sov-report-sample.json)
  и [examples/ai-sov-report-sample.csv](./examples/ai-sov-report-sample.csv)
  для sample-данных по AI Share of Voice.
- Сохраняем явную ссылку на companion repo:
  [https://github.com/Gudvin82/vibe-coding-protocols](https://github.com/Gudvin82/vibe-coding-protocols)

## Участие

См. [CONTRIBUTING.md](./CONTRIBUTING.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) и шаблон PR в [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md).
