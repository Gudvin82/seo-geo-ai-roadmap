# AI Operator Mode

Платформа сделана так, чтобы человек или AI coding agent могли адаптировать ее под реальный сайт.

## Типовой operator loop

1. Развернуть платформу локально или в self-hosted режиме.
1. Открыть `/docs`, `/redoc` и frontend UI.
1. Создать workspace и project для целевого сайта.
1. Добавить brand facts и provider settings.
1. Запустить audit.
1. Просмотреть artifacts, findings и reports.
1. Превратить выводы в implementation tasks.

## Что может делать AI coding agent

- запускать проверки через API
- разбирать reports и artifacts
- сопоставлять выводы с docs и checklists
- генерировать `llms.txt` и связанные AI-файлы
- обновлять brand facts и truth-center контент
- готовить implementation tasks и release notes

## Playbooks “адаптируй мой сайт”

- Local business site
- Expert / personal brand site
- Product / service site
- Multilingual site

Репозиторная методология и app-layer должны работать вместе. Платформа не должна быть black box.
