# AI-боты и robots.txt

| Бот | Типичная роль | Подсказка по управлению доступом |
|---|---|---|
| GPTBot | training-oriented bot | при необходимости регулируйте через `robots.txt` |
| ChatGPT-User | user-triggered fetching | разрешайте public pages, которые должны читаться |
| ClaudeBot | crawling или retrieval в зависимости от сценария | делайте намерение явным в robots rules |
| PerplexityBot | retrieval и citation-oriented fetching | следите, чтобы ключевые страницы были доступны |
| Google-Extended | контроль training-use слоя | регулируйте отдельно от Googlebot |
| Applebot-Extended | extended AI usage control у Apple | явно документируйте intent доступа |

## Практическое правило

- `robots.txt` управляет намерением crawl access
- `llms.txt` помогает перечислить priority pages и facts
- `ai.txt` может дополнять AI-facing guidance

## Пример директив

```text
User-agent: GPTBot
Disallow:

User-agent: Google-Extended
Disallow: /
```
