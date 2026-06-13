# Guidance по ai.txt

`ai.txt` здесь рассматривается как optional AI-facing guidance file. Это
короткая карта публичных AI-маршрутов, а не замена `robots.txt`, `llms.txt`
или видимым фактами сайта.

## Для чего он нужен

- короткие policy hints для AI-facing layer
- явные route hints для публичных страниц
- связка с `llms.txt` и sitemap
- краткие reminders, чего нельзя додумывать

## Для чего он не нужен

- скрытые инструкции
- юридические disclaimers вместо crawler-policy
- facts и pages, которых нет в публичном контенте
- правила, противоречащие `robots.txt`

## Минимальный паттерн

База: [templates/ai.txt.example](../../templates/ai.txt.example)

Рекомендуемые directives:

- `policy`
- `summary`
- `contact`
- `llms`
- `sitemap`
- `allow`
- `disallow`
- `notes`

## Workflow проверки

1. Соберите черновик `ai.txt`.
2. Убедитесь, что он не противоречит `robots.txt`.
3. Проверьте, что он не уехал от `llms.txt`.
4. Запустите:

```bash
python scripts/check-ai-txt.py --url https://example.com
```

или

```bash
python scripts/check-ai-txt.py --file ./ai.txt --robots-file ./robots.txt --llms-file ./llms.txt
```

## Типичные противоречия

- `ai.txt` приветствует широкий AI-access, а `robots.txt` блокирует AI-ботов
- `ai.txt` ссылается на `llms.txt` или пути, которых уже нет
- `ai.txt` описывает support, pricing или product facts, которых нет на сайте

## Честное ограничение

`ai.txt` пока остается emergent pattern. Он полезен для operator clarity и
будущей AI hygiene, но не дает гарантированного crawling или citations.
