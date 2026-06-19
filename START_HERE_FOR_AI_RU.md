# Start Here For AI

Используйте этот файл, когда пользователь хочет, чтобы AI coding agent честно
развернул, проаудировал, адаптировал или оценил репозиторий.

## Сначала поймите, что это за repo

Этот репозиторий:

- open-source
- self-hosted
- AI-agent-ready
- methodology plus app plus scripts

Этот репозиторий не является:

- finished hosted SaaS от автора
- silent autopilot для production changes
- заменой human approval на рискованных изменениях

Сначала прочитайте:

1. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
2. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
3. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
4. [REAL_CASES_RU.md](./REAL_CASES_RU.md)

## Самый быстрый безопасный deployment path

Если пользователь говорит “разверни это мне”:

1. `git clone https://github.com/Gudvin82/seo-geo-ai-roadmap.git`
2. `cd seo-geo-ai-roadmap`
3. `cp .env.example .env`
4. заполните обязательные ключи или оставьте demo-safe defaults
5. `make up`
6. `make migrate`
7. `make seed`, если нужны demo data
8. проверьте:
   - `http://localhost:3000`
   - `http://localhost:8000/docs`
   - demo login работает

Самый быстрый demo route:

- `make turnkey-demo`

## Если пользователю нужен готовый prompt

Начинайте отсюда:

- [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)

Также доступны:

- [prompts/ru/repo-site-audit-agent-prompt.md](./prompts/ru/repo-site-audit-agent-prompt.md)
- [prompts/ru/deploy-client-scanner-agent-prompt.md](./prompts/ru/deploy-client-scanner-agent-prompt.md)
- [prompts/ru/improve-existing-site-agent-prompt.md](./prompts/ru/improve-existing-site-agent-prompt.md)

## Базовый порядок работы для AI

Если неясно, что читать дальше, идите так:

1. [README_RU.md](./README_RU.md)
2. [AGENTS.md](./AGENTS.md)
3. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
4. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
5. [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
6. нужный deep playbook в `docs/ru/`
7. нужный checklist в `checklists/`
8. нужный script в `scripts/`
9. [REAL_CASES_RU.md](./REAL_CASES_RU.md)

## Если задача звучит как “проаудируй сайт”

Используйте:

- [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)
- [docs/ru/technical-seo-deep-playbook.md](./docs/ru/technical-seo-deep-playbook.md)
- [docs/ru/semantic-core-and-intent-playbook.md](./docs/ru/semantic-core-and-intent-playbook.md)
- [docs/ru/geo-ai-operations-playbook.md](./docs/ru/geo-ai-operations-playbook.md)

И затем по возможности repo-native helpers:

- `python scripts/check-robots-ai-bots.py --url https://example.com`
- `python scripts/check-ai-txt.py --url https://example.com`
- `python scripts/check-llms-txt.py --url https://example.com/llms.txt`
- `python scripts/schema-coverage-checker.py --url https://example.com --site-type service`
- `python scripts/faq-detector.py --url https://example.com`
- `python scripts/open-graph-checker.py --url https://example.com`
- `python scripts/rag_chunk_audit.py --url https://example.com`
- `python scripts/citability_score.py --url https://example.com`

## Обязательный self-check перед словом “готово”

Если менялось поведение кода или runtime:

1. запустите `make agent-self-check`
2. запустите `make verify-demo`, если стек поднят
3. прогоните relevant test path

Всегда отдельно сообщайте:

- что реально проверено
- что было heuristic
- где еще нужен human review
- обновлены ли и EN, и RU user-facing layers
