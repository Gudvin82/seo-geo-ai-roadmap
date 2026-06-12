# Уведомления и webhooks

В `v2.3.0` добавлен starter-слой notification endpoints для webhook-based
operator flows.

## Что уже есть

- создание endpoints на уровне workspace
- привязка endpoints к конкретным событиям
- отправка JSON payload в Slack-style, Telegram-style или generic webhooks

## С каких событий лучше начать

- `audit.run_requested`
- `sov.completed`
- `project.package_exported`

## Telegram AI SoV starter

Для GEO/AI operator workflows Telegram — удобный первый канал для
`sov.completed` alerts. См. [telegram-sov-alerts.md](./telegram-sov-alerts.md).

## Текущие ограничения

- пока нет durable retry queue
- пока нет UI для ротации секретов
- пока нет dashboard по доставке

Используйте этот слой как легкий operator-awareness механизм, а не как
гарантированную incident-доставку.
