# AI Operator Mode

Платформа сделана так, чтобы человек или AI coding agent могли адаптировать ее под реальный сайт.

## Типовой operator loop

1. Развернуть платформу локально или в self-hosted режиме.
1. Подключить cloud providers или local LLM endpoints, например Ollama или LocalAI.
1. Открыть `/docs`, `/redoc` и frontend UI.
1. Создать workspace и project для целевого сайта.
1. Добавить brand facts, provider settings и при необходимости team roles.
1. Запустить canonical audit job через `POST /api/v1/audit-runs/run`.
1. Просмотреть artifacts, findings, reports и audit logs.
1. Превратить выводы в implementation tasks или patch artifacts.
1. После внедрения повторно запустить аудит и сравнить outputs.

## Что может делать AI coding agent

- запускать проверки через API
- разбирать reports и artifacts
- сопоставлять выводы с docs и checklists
- генерировать `llms.txt` и связанные AI-файлы
- обновлять brand facts и truth-center контент
- готовить implementation tasks и release notes

## Playbooks “адаптируй мой сайт”

- Local business site
- Service company site
- Expert / personal brand site
- SaaS / product site
- Multilingual site
- Agency client onboarding

Репозиторная методология и app-layer должны работать вместе. Платформа не должна быть black box.
