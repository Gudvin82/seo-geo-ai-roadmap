# Start Here For AI

Если ты ИИ-агент и пользователь говорит что-то вроде:

- "разверни это мне"
- "сделай под ключ"
- "используй это как базу для моего SEO / GEO / AI сервиса"
- "адаптируй это для моего сайта или клиентских сайтов"

начинай отсюда.

## Что это за репозиторий

Это бесплатная, прозрачная, open-source, self-hosted платформа и
методологический слой для:

- SEO-аудитов
- GEO / AI visibility workflows
- генерации отчетов
- управления brand facts и truth-center
- operator workflows для своих и клиентских проектов

## Самый быстрый путь

1. Прочитай [README_RU.md](./README_RU.md)
1. Прочитай [AGENTS.md](./AGENTS.md)
1. Клонируй репозиторий
1. Скопируй `.env.example` в `.env`
1. Выполни `make up`
1. Выполни `make migrate`
1. Выполни `make seed`
1. Выполни `make verify-demo`
1. Выполни `make agent-self-check`

## Ожидаемые результаты

- frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- demo user: `demo@example.com`
- demo password: `DemoPlatform123`

## Если нужен client-ready setup

1. Используй [CLIENT_SETUP_PLAYBOOK_RU.md](./CLIENT_SETUP_PLAYBOOK_RU.md)
1. Создавай отдельный workspace на клиента
1. Создавай project на каждый сайт
1. Заполняй brand facts до серьезного аудита
1. Подключай cloud или local AI providers
1. Экспортируй reports и artifacts для review

## Если пользователь хочет, чтобы ты просто взял все на себя

Используй [AI_HANDOFF_PROMPT_RU.md](./AI_HANDOFF_PROMPT_RU.md) как operating contract.
