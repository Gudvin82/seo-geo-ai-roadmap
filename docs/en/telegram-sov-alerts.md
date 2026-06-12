# Telegram AI SoV Alerts

## Use case

Send a Telegram-style notification when a monitored brand loses visibility for a
priority query on a tracked AI surface.

## Where it fits

Use this as an operator-awareness layer on top of the notification endpoint
system. It is useful for:

- agency operators watching multiple clients
- in-house teams tracking a small set of high-value prompts
- founders who want lightweight alerts instead of dashboards

## Suggested payload

- event: `sov.completed`
- summary: short brand + query + provider status
- metadata: query, provider, prior score, current score, confidence

Example:

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

## Example message

`[sov.completed] Brand X dropped in Perplexity for query "best seo geo audit".`

## Local test

1. create a Telegram bot and chat id
2. configure the notification endpoint
3. send one synthetic `sov.completed` payload
4. verify the rendered message and operator usefulness

## Limitations

- this is alerting, not durable incident management
- noisy prompts can create false urgency
- Telegram delivery success does not prove GEO causality
