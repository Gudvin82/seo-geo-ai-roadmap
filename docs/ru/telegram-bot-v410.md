# Telegram Bot Runtime v4.1.0

В `v4.1.0` появился реальный backend webhook path для Telegram, а не только
stub-файл.

## Runtime path

- `POST /api/v1/telegram/webhook`
- optional secret header: `X-Telegram-Bot-Api-Secret-Token`
- используется `SCANNER_TELEGRAM_BOT_TOKEN`
- optional `SCANNER_TELEGRAM_WEBHOOK_SECRET`

## Поддерживаемые команды

- `/start`
- `/help`
- `/geo help`
- `/geo audit https://example.com`
- `/geo latest PROJECT_ID`
- `/geo alerts PROJECT_ID`

## Что происходит на `/geo audit`

Бот создает passive scanner job и возвращает:

- scan job id
- status endpoint
- result endpoint

Теперь это реальный self-hosted operator path, а не только статический preview
helper.
