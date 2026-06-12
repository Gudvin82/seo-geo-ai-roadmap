# AI Visibility Check GitHub Action

Используйте пример workflow из
[`examples/github-actions/ai-visibility-check.yml`](../../examples/github-actions/ai-visibility-check.yml),
чтобы запускать лёгкую GEO/AI-проверку в другом репозитории.

## Что он проверяет

- структуру `llms.txt`
- `robots.txt` access для основных AI-ботов
- baseline-валидность JSON-LD файлов

## Как подключить

1. Скопируйте workflow в `.github/workflows/ai-visibility-check.yml`.
2. Замените demo URL `https://example.com` на реальный site URL.
3. Замените `./llms.txt`, если файл лежит в другом месте.
4. Замените путь к schema на один из ваших реальных JSON-LD files.
5. Сначала прогоните workflow вручную, а уже потом включайте его в PR policy.

## Ожидаемые outputs

- pass или fail по `llms.txt`
- pass или fail по robots access checks
- pass или fail по одной JSON-LD validation step

## Local dry-run

```bash
python scripts/check-llms-txt.py --file templates/llms.txt.example
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/schema-validator.py --file templates/schema/organization-schema.json
```

## Failure modes

- `llms.txt` отсутствует или слишком слаб по структуре
- robots rules случайно блокируют важные crawlers
- schema JSON невалиден или всё ещё содержит placeholder data

## Чего он не доказывает

- rankings
- гарантированные AI citations
- business lift
