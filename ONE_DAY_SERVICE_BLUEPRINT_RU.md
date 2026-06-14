# One-Day Blueprint Сервиса

Этот файл отвечает на практический вопрос:

- "Как за один день превратить этот репозиторий в свой client-facing scanner или audit-сервис?"

Цель не в том, чтобы "за день собрать единорога-SaaS".
Цель в том, чтобы:

- развернуть репозиторий
- забрендировать его
- безопасно открыть scanner intake
- запускать аудиты
- возвращать отчеты и задачи

## Какой результат должен быть к концу дня

У вас должно появиться:

- одно развернутое self-hosted решение
- один брендированный frontend
- одна public или semi-public scanner intake page
- один внутренний operator flow для review и delivery
- один повторяемый способ экспортировать findings, recommendations и tasks

## Рекомендуемый план на день

### Час 1: развернуть стек

1. Склонируйте репозиторий
1. Скопируйте `.env.example` в `.env`
1. Выполните `make up`
1. Выполните `make migrate`
1. Выполните `make seed`, если нужны demo-данные
1. Выполните `make verify-demo`

## Час 2: настроить операторскую сторону

1. Войдите в приложение
1. Создайте один workspace
1. Создайте один project
1. Заполните brand facts
1. Подключите хотя бы одного provider или оставьте starter mode для proof-first demo
1. Запустите один audit и одну SoV-проверку

## Час 3: включить публичную intake-сторону

1. Откройте `app/frontend/scanner.html`
1. Решите, какой у вас публичный режим:
   - только passive
   - passive плюс ownership-gated active
   - full, но все равно review-first
1. Оставьте ownership verification включенной для active scans
1. Оставьте public-service limitations видимыми в UI

## Час 4: забрендировать сервис

1. Заполните branding fields у workspace
1. Добавьте логотип, report title, subtitle и footer
1. Определите публичное обещание:
   - audit service
   - scanner intake
   - expert-led SEO плюс GEO плюс AI service

## Час 5: настроить слой delivery

1. Используйте report exports
1. Используйте patch pack generation
1. Используйте client delivery pack generation
1. Выберите, куда идет результат:
   - PDF или report artifact
   - внутренняя task board
   - GitHub Issues
   - handoff в стиле Notion, Trello или Linear

## Час 6: подготовить AI handoff

Используйте встроенные AI entrypoints:

- [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- [AGENTS.md](./AGENTS.md)
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language ru`

Также используйте prompt packs из `v4.4.0`:

- [prompts/ru/repo-site-audit-agent-prompt.md](./prompts/ru/repo-site-audit-agent-prompt.md)
- [prompts/ru/deploy-client-scanner-agent-prompt.md](./prompts/ru/deploy-client-scanner-agent-prompt.md)
- [prompts/ru/improve-existing-site-agent-prompt.md](./prompts/ru/improve-existing-site-agent-prompt.md)

## Час 7: оформить публичную историю

Безопасная упаковка:

- self-hosted
- open-source
- AI-agent-ready
- foundation для своего scanner или audit-сервиса

Не обещайте:

- hosted SaaS от автора репозитория
- enterprise billing и SSO из коробки
- тихие autopilot-изменения сайта

## Час 8: сделать один реальный proof run

1. Запустите один реальный аудит сайта
1. Экспортируйте один report
1. Экспортируйте один patch pack
1. Экспортируйте один client delivery pack
1. Сохраните screenshots:
   - login
   - dashboard
   - scanner intake
   - report

## Минимальная публичная архитектура

Для практичного первого релиза используйте:

- один VPS или VM
- Docker Compose
- PostgreSQL
- reverse proxy с HTTPS
- один frontend entrypoint
- один backend API
- один artifact storage path

## Безопасная версия публичного обещания

Безопасно:

- "Пользователь может ввести URL и получить структурированный SEO плюс GEO плюс AI audit flow, который наша команда просматривает и выдает."

Более смело, но все еще безопасно:

- "Этот репозиторий можно развернуть как foundation для client-facing scanner или audit-сервиса."

Небезопасно:

- "Это уже готовый hosted SaaS без настройки."

## Что читать дальше

- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
- [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- [REAL_CASES_RU.md](./REAL_CASES_RU.md)
