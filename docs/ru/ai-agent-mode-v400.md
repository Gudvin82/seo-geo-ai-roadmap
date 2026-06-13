# AI Agent Mode v4.0.0

В `v4.0.0` появился реальный слой agent mode поверх скриптов и ручных команд.

Поддерживаемые режимы:

- `manual`
- `scheduled`
- `watch`
- `agent-review`
- `agent-plan`
- `agent-fix-proposal`

Что агент умеет:

- суммировать сканы и аудиты
- сравнивать результат с benchmark-контекстом
- готовить executive summaries
- собирать нормализованные task bundles
- готовить fix proposals и payloads для issue-export
- триггерить alerts через webhook, email и Telegram

Что агент не делает молча:

- не публикует production-изменения
- не мержит код и CMS-правки без approve
- не пересекает явную approval boundary для рискованных действий
