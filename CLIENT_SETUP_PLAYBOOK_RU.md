# Client Setup Playbook

Используй этот сценарий, когда репозиторий должен стать реальной operator
средой для клиентского сайта.

## 1. Разверни платформу

1. `cp .env.example .env`
1. `make up`
1. `make migrate`
1. `make seed`, если сначала нужен demo baseline

## 2. Создай client workspace

Задай:

- название клиента или бренда
- язык отчетности
- white-label заголовок отчета
- white-label подзаголовок

## 3. Создай client project

Задай:

- URL сайта
- рынок
- язык
- тип проекта
- audit preset

## 4. Заполни truth center

До серьезного аудита зафиксируй:

- brand facts
- approved claims
- forbidden claims
- numeric facts
- primary CTA

## 5. Подключи providers

Выбери один или несколько:

- OpenAI
- Anthropic / Claude
- Gemini
- Perplexity
- Ollama
- LocalAI
- vLLM-compatible endpoint

## 6. Запусти первый аудит

Используй:

- UI flow
- или `POST /api/v1/audit-runs/run`

## 7. Просмотри outputs

Проверь:

- summary отчета
- artifacts
- audit logs
- пробелы в facts, pages и visibility structure

## 8. Преврати выводы в работу

Собери:

- implementation backlog
- page update tasks
- FAQ / schema / `llms.txt` drafts
- client-facing report pack

## 9. Проверь перед handoff

Запусти:

- `make verify-demo`, если demo stack активен
- `make agent-self-check`
- test и lint команды, если менялся код
