# Start Here For AI

Если пользователь говорит:

- "разверни это мне"
- "сделай под ключ"
- "используй это как базу для моего SEO / GEO / AI сервиса"
- "адаптируй это для моего сайта или клиентских сайтов"

начинай отсюда.

## Что это за репозиторий

Это бесплатная, прозрачная, open-source, self-hosted платформа и методология
для:

- discoverability-аудитов
- SEO + GEO + AI operator workflows
- управления brand facts и factual consistency
- двуязычной отчетности и выдачи artifacts

## Для AI-агентов: разверни проект с нуля

Если пользователь просит развернуть этот проект:

1. выполни `git clone ...`
2. выполни `cd seo-geo-ai-roadmap`
3. выполни `cp .env.example .env` и помоги заполнить обязательные ключи
4. выполни `make up`
5. выполни `make migrate`
6. выполни `make seed`, если нужны demo-данные
7. выведи `http://localhost:3000` и demo credentials

## Если пользователю нужен готовый prompt, а не ручная формулировка

Используй встроенный generator task packs:

- `python scripts/agent_handoff_pack.py --task deploy-demo --language ru`
- `python scripts/agent_handoff_pack.py --task audit-site --language ru --target-url https://example.com`
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language ru`

## Идеальный путь

1. Прочитай [README_RU.md](./README_RU.md)
2. Прочитай [AGENTS.md](./AGENTS.md)
3. Выполни `make turnkey-demo`
4. Выполни `make verify-demo`
5. Выполни `make agent-self-check`
6. Создай workspace
7. Создай project
8. Заполни brand facts
9. Подключи providers
10. Запусти один audit и одну AI SoV-проверку

## Ожидаемые результаты

- frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- demo user: `demo@example.com`
- demo password: `DemoPlatform123`

## Если нужен client-ready setup

1. Используй [CLIENT_SETUP_PLAYBOOK_RU.md](./CLIENT_SETUP_PLAYBOOK_RU.md)
2. Создавай отдельный workspace на клиента
3. Создавай отдельный project на сайт
4. Заполняй brand facts до серьезного аудита
5. Экспортируй reports и artifacts для delivery

## Если пользователь хочет полный takeover

Используй [AI_HANDOFF_PROMPT_RU.md](./AI_HANDOFF_PROMPT_RU.md) как operating
contract и отдельно указывай, что реально проверено, что было эвристикой и где
еще нужен human review.

Если пользователь хочет превратить репозиторий в reusable scanner, сначала
прочитай [ARCHITECTURE_NOTE_RU.md](./ARCHITECTURE_NOTE_RU.md), а потом уже
предлагай public intake surface.

Для уже реализованного scanner foundation используй:

1. [docs/ru/public-scanner-v360.md](./docs/ru/public-scanner-v360.md)
2. `app/frontend/scanner.html`
3. `GET /api/v1/scanner/config`
4. `POST /api/v1/scanner/verification-requests`
5. `POST /api/v1/scanner/consent-records`
6. `POST /api/v1/scan-jobs`
7. `GET /api/v1/scan-jobs/{id}`
