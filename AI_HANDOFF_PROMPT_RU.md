# AI Handoff Prompt

Используй этот промпт, когда хочешь передать репозиторий другому ИИ и заставить
его выполнить setup или audit flow под ключ.

Если нужен task-specific вариант, сгенерируй его прямо из репозитория:

- `python scripts/agent_handoff_pack.py --task audit-site --language ru --target-url https://example.com`
- `python scripts/agent_handoff_pack.py --task deploy-demo --language ru`
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language ru`

```text
Ты принимаешь на себя бесплатную и прозрачную self-hosted платформу для SEO, GEO и AI discoverability.

Репозиторий:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Твоя задача:
1. Сначала прочитать README_RU.md, AGENTS.md и EVALUATE_THIS_REPO_FIRST_RU.md.
2. Развернуть стек локально или в self-hosted режиме.
3. Скопировать .env.example в .env и заполнить только минимально нужные значения.
4. Выполнить make up
5. Выполнить make migrate
6. Выполнить make seed, если demo-данные полезны
7. Выполнить make verify-demo
8. Выполнить make agent-self-check
9. Если задача про реальный сайт, создать workspace и project, подключить providers и запустить canonical audit job.
9a. Использовать канонический repo command path: `/geo quick`, `/geo audit`, `/geo graph`, `/geo report`, `/geo compare`, `/geo agent`.
10. Вернуть:
   - URL
   - credentials, если использовался demo
   - что реально проверено
   - что еще не сделано
   - результат demo-ready или production-like self-hosted ready

Если задача состоит в развертывании или эксплуатации public scanner-flow:
11. Открыть `app/frontend/scanner.html` и прочитать `docs/ru/public-scanner-v360.md`.
12. Вызвать `GET /api/v1/scanner/config` и учитывать feature flags до показа режимов в UI.
13. Для режимов `active` и `full` требовать ownership verification через HTML file, meta tag или DNS TXT до отправки job.
14. Создать scan job через `POST /api/v1/scan-jobs`, затем отслеживать его через `GET /api/v1/scan-jobs/{id}` и `GET /api/v1/scan-jobs/{id}/events`.
15. После завершения job открыть `GET /api/v1/scan-jobs/{id}/result`, `GET /api/v1/tasks/scan-job/{id}` и `GET /api/v1/graph-runtime/scan-job/{id}`.
15. Если важен discoverability coverage layer, отдельно проверить `robots.txt`, `YandexAdditional`, `ai.txt`, schema coverage, FAQ/answer-ready patterns, Open Graph/Twitter и связку robots+sitemap.
16. Открыть `app/frontend/graph.html`, если нужно объяснить связи между проблемами, trust nodes или порядок remediation.
17. Вернуть ссылки на artifacts, поведение notifications, public-service limitations и все heuristic uncertainty вместе с результатом сканирования.

Правила:
- Не заявляй "готово" без проверки.
- Если менялся user-facing scope, проверь, что EN и RU слои синхронизированы.
- Если менялся код, запусти tests и lint checks.
- Предпочитай встроенные workflows репозитория, а не придумывай свои.
```
