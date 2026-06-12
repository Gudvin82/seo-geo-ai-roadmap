# llms.txt Validator

## Что это такое

В `v3.3.0` есть бесплатный `llms.txt` validator, которым можно пользоваться в
четырёх синхронизированных режимах:

- API endpoint: `POST /api/v1/tools/llms-validator`
- standalone page: [`app/frontend/llms-validator.html`](../../app/frontend/llms-validator.html)
- hosted docs-site page: `docs_site/validator.md`, если включен GitHub Pages
- CLI script: `python scripts/check-llms-txt.py --file ./llms.txt`

Его задача не "обещать AI citations", а быстро находить грубые структурные
ошибки до публикации файла в production.

## Текущие правила валидации

Сейчас validator ожидает разумный baseline:

- top-level heading, например `# Example llms.txt`
- структурированные записи, обычно bullet-like строки
- хотя бы один абсолютный URL, например `https://example.com/faq`
- достаточный объём, чтобы файл не был почти пустым
- базовые trust hints: homepage, FAQ и about/trust материал

Passing result означает "минимальная хорошая структура". Это не означает, что
файл уже полностью достаточен для любого бизнеса или рынка.

## Пример проходящего файла

```text
# Example llms.txt
- Home: https://example.com/
- FAQ: https://example.com/faq
- About: https://example.com/about
- Services: https://example.com/services/seo-geo-audit
```

## Типовые причины падения

- нет heading
- вместо структуры дан один абзац текста
- используются относительные пути, а не absolute URLs
- нет FAQ/about/trust reference
- файл слишком короткий и не даёт достаточного сигнала

## Как использовать

### Hosted page

Используйте публичную docs-site validator page, когда нужен linkable free tool
для операторов, клиентов и reviewers. Она полностью валидирует вставленный
текст в браузере и best-effort пытается читать публичный URL, если сайт не
блокирует cross-origin fetches.

### API

```json
{
  "content": "# Example llms.txt\n- Home: https://example.com/\n- FAQ: https://example.com/faq\n- About: https://example.com/about\n"
}
```

Ответ возвращает:

- `is_valid`
- `warnings`
- `recommendations`
- `observed_facts`
- `line_count`
- `checked_source`

### UI

Standalone page удобна для быстрого human-readable check. Она подходит для
операторов, QA и клиентских walkthroughs, потому что показывает не только факт
ошибки, но и что именно нужно исправить.

### CLI

Запускайте локальную проверку до коммита:

```bash
python scripts/check-llms-txt.py --file examples/sample-llms.txt
python scripts/check-llms-txt.py --file templates/llms.txt.example
```

## Рекомендуемый workflow

1. Соберите черновик `llms.txt`.
2. Прогоните validator локально.
3. Уберите все structural warnings.
4. Перепроверьте уже опубликованный файл по public URL.
5. Сохраните passing result в delivery notes или QA log.

## Что делать при ошибках

- Если файл слишком короткий: добавьте homepage, FAQ, about, contact и trust pages.
- Если нет URL: замените относительные пути на canonical absolute URLs.
- Если нет структуры: превратите prose в bullet-like entries.
- Если не хватает trust hints: добавьте about, proof, policy или expert pages.

## Правило синхронизации

Следующие артефакты должны описывать одни и те же правила:

- `scripts/check-llms-txt.py`
- `app/backend/app/services/llms_validator.py`
- `app/frontend/llms-validator.html`
- `examples/sample-llms.txt`
- `templates/llms.txt.example`

Если один asset принимает паттерн, который другой считает ошибкой, это нужно
считать release-bug и нормализовать rule set.

## Ограничения

- validator проверяет структуру, а не бизнес-правдивость
- он не обходит и не сравнивает связанные страницы
- он не доказывает, что LLM будет читать или цитировать файл
- hosted browser page может не прочитать удаленный URL, если цель блокирует cross-origin fetches
- в будущих релизах правила могут стать строже по мере развития operator model
