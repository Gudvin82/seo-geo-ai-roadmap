# Telegram AI SoV Alerts

## Use case

Отправлять Telegram-style уведомление, когда monitored brand теряет visibility
по priority query на отслеживаемой AI surface.

## Рекомендуемый payload

- event: `sov.completed`
- summary: короткий статус brand + query + provider
- metadata: query, provider, prior score, current score, confidence

## Пример сообщения

`[sov.completed] Brand X dropped in Perplexity for query "best seo geo audit".`
