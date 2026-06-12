# AI Visibility Check GitHub Action

Используйте пример workflow из
[`examples/github-actions/ai-visibility-check.yml`](../../examples/github-actions/ai-visibility-check.yml),
чтобы запускать лёгкую GEO/AI-проверку в другом репозитории.

## Что он проверяет

- структуру `llms.txt`
- `robots.txt` access для основных AI-ботов
- baseline-валидность JSON-LD файлов

## Чего он не доказывает

- rankings
- гарантированные AI citations
- business lift
