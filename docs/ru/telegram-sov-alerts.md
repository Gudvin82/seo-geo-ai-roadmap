# Telegram AI SoV Alerts

## Use case

Отправлять Telegram-style уведомление, когда monitored brand теряет visibility
по priority query на отслеживаемой AI surface.

## Где это используется

Это operator-awareness слой поверх notification endpoint system. Он особенно
полезен:

- агентствам, которые следят сразу за несколькими клиентами
- in-house командам с небольшим набором high-value prompts
- фаундерам, которым нужен лёгкий alerting вместо dashboard-first процесса

## Рекомендуемый payload

- event: `sov.completed`
- summary: короткий статус brand + query + provider
- metadata: query, provider, prior score, current score, confidence

Пример:

```json
{
  "event": "sov.completed",
  "summary": "Brand X dropped on Perplexity for a priority prompt",
  "metadata": {
    "query": "best seo geo audit",
    "provider": "perplexity",
    "prior_score": 74,
    "current_score": 41,
    "confidence": "medium"
  }
}
```

## Пример сообщения

`[sov.completed] Brand X dropped in Perplexity for query "best seo geo audit".`

## Local test

1. создайте Telegram bot и chat id
2. настройте notification endpoint
3. отправьте один synthetic `sov.completed` payload
4. проверьте текст сообщения и operator usefulness

## Ограничения

- это alerting, а не durable incident management
- шумные prompts могут давать ложное чувство срочности
- успешная доставка в Telegram не доказывает GEO causality
