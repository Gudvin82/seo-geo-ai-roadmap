# Telegram Bot Runtime v4.1.0

`v4.1.0` now includes a real backend webhook path for Telegram instead of only a
stub file.

## Runtime path

- `POST /api/v1/telegram/webhook`
- optional secret header: `X-Telegram-Bot-Api-Secret-Token`
- uses `SCANNER_TELEGRAM_BOT_TOKEN`
- optional `SCANNER_TELEGRAM_WEBHOOK_SECRET`

## Supported commands

- `/start`
- `/help`
- `/geo help`
- `/geo audit https://example.com`
- `/geo latest PROJECT_ID`
- `/geo alerts PROJECT_ID`

## What happens on `/geo audit`

The bot creates a passive scanner job and returns:

- scan job id
- status endpoint
- result endpoint

This is now a real self-hosted operator path, not just a static preview helper.
