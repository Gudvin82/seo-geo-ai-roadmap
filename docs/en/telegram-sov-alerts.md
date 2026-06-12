# Telegram AI SoV Alerts

## Use case

Send a Telegram-style notification when a monitored brand loses visibility for a
priority query on a tracked AI surface.

## Suggested payload

- event: `sov.completed`
- summary: short brand + query + provider status
- metadata: query, provider, prior score, current score, confidence

## Example message

`[sov.completed] Brand X dropped in Perplexity for query "best seo geo audit".`
