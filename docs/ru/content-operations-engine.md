# Content Operations Engine

Content Operations Engine превращает подтвержденный спрос в управляемый
редакционный backlog. Это не система автоматической публикации, не гарантия
позиций и не замена экспертизе автора.

## Операционный Цикл

1. Соберите спрос из разрешенных оператором источников: GSC, Яндекс Вебмастер,
   экспортов Wordstat, языка клиентов и конкурентного исследования.
2. Кластеризуйте тему по интенту и определите тип страницы.
3. Создайте задачу с demand, business value, evidence strength, effort, owner и
   обязательными review gates.
4. До черновика подготовьте brief: потребность пользователя, источники,
   внутренние ссылки, proof-активы, конверсионный путь и границы фактов.
5. До публикации получите factual, editorial, legal и technical approval.
6. Проверьте опубликованную страницу, сохраните evidence, затем по выбранному
   оператором расписанию контролируйте freshness и каннибализацию.

## Собрать Очередь

```bash
python scripts/content_ops_queue.py \
  --file examples/content-ops-queue-example.csv \
  --default-owner content_lead
```

Score намеренно объясним:

`0.35 demand + 0.35 business value + 0.20 evidence strength - 0.10 effort`

Он приоритизирует работу. Он не прогнозирует позиции, трафик, лиды или AI
citations.

## Запустить Полный Цикл

```bash
python scripts/content_lifecycle.py \
  --manifest examples/content-lifecycle/manifest.json \
  --output-dir ./artifacts/content-lifecycle
```

Пример объединяет экспорты GSC, Яндекс Вебмастера, Wordstat и конкурентного
исследования, проверяет реестр `страница ↔ кластер`, валидирует drafts, находит
возможности на позициях 4-15, собирает advisor summary без writeback и при
необходимости создает редактируемую SVG-обложку. Замените примеры данными,
полученными владельцем проекта.

После согласования и публикации страницы IndexNow запускается явно:

```bash
INDEXNOW_KEY=replace-me python scripts/indexnow_submit.py \
  --host example.com \
  --url https://example.com/new-page \
  --verify
```

Прием URL в IndexNow и доступность страницы не доказывают индексацию или рост
позиций.

## Обязательные Гейты

- Проверка интента и аудитории
- Проверка источников и фактических утверждений
- Проверка internal links и canonical
- Редакционное и юридическое согласование
- Post-publish verification

## Особенности RU

Используйте Wordstat и Яндекс Вебмастер только через разрешенные экспорты или
credentials владельца. Региональные формулировки, юридические утверждения,
цены и поверхности Яндекса/Алисы должны быть входом для ревью, а не поводом
массово генерировать страницы.

## Границы

- Не публикуйте массово сгенерированный текст без согласования человека.
- Не используйте страницы конкурентов как источник для переписывания.
- Не оптимизируйте материал только по количеству слов.
- Храните источники существенных утверждений.
- После публикации используйте имеющиеся freshness и fact-drift проверки.

## Связанные Инструменты

- `scripts/semantic_gap_mapper.py`
- `scripts/content_freshness_checker.py`
- `scripts/fact_drift_checker.py`
- `scripts/checklist_generator.py`
- `scripts/content_lifecycle.py`
- `scripts/indexnow_submit.py`
- `contracts/content-lifecycle.schema.json`
