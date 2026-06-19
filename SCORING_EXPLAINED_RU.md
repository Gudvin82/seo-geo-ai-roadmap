# Объяснение scoring

Этот файл существует для того, чтобы репозиторий нельзя было упрекнуть в
скрытой логике scoring.

## Что именно сейчас оценивается

Репозиторий не выдает одну магическую universal SEO-оценку.

Он использует несколько ограниченных score-слоев:

- `overall_score` для давления backlog по findings
- `priority_score` для очередности исправлений
- `AI Citation Score` для текущей mention-plus-citation visibility в отслеживаемых AI-результатах
- benchmark statuses для метрик вроде LCP, CLS, INP, schema coverage, AI visibility readiness и factual consistency
- heuristic scores в отдельных scripts, например citability или AI readability

## 1. Audit overall score

Источник в коде:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Текущая логика:

- у каждого finding есть severity
- severity превращается в penalty points
- high-priority findings добавляют дополнительный penalty через свой priority score
- итоговая оценка стартует со `100` и вычитает накопленный penalty

Текущие веса severity:

- `critical = 30`
- `high = 18`
- `medium = 9`
- `low = 4`

Текущая формула:

```text
overall_score = max(0, 100 - severity_penalty_sum - priority_penalty_sum)
priority_penalty_sum = sum(priority_score / 20)
```

Как это понимать:

- это operator score, а не market truth score
- низкий score означает тяжелый backlog, а не “сайт мертв”
- часть реальных улучшений может произойти раньше, чем заметно двинется этот score

## 2. Priority score

Источник в коде:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Входы:

- severity
- impact
- effort
- confidence
- benchmark status

Текущая формула:

```text
raw = severity_points + (impact * 8) + (confidence * 6) - (effort * 4)
score = clamp(raw + benchmark_modifier, 0, 100)
```

Benchmark modifiers:

- `urgent_fix = +18`
- `worse_than_baseline = +8`
- `better_than_baseline = -8`
- `insufficient_data = 0`

Priority labels:

- `80-100 = fix_now`
- `60-79 = next_batch`
- `40-59 = planned`
- `0-39 = observe`

Как это понимать:

- score нужен для sequencing
- он прозрачен, но специально сделан простым
- он не заменяет operator judgment в вопросах revenue, legal risk и brand risk

## 3. AI Citation Score

Источник в коде:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Текущая логика:

- у каждого tracked result есть `mentioned`
- у каждого tracked result есть `citation_count`
- mention status дает `70%`
- citation count дает `30%`
- citation count ограничен максимумом `3`

Текущая формула:

```text
per_result = (mentioned ? 1.0 : 0.0) * 0.7 + (min(citation_count, 3) / 3) * 0.3
AI Citation Score = average(per_result) * 100
```

Как это понимать:

- это directional visibility proxy
- он полезен для трендов и сравнений
- он не обещает rankings, leads или коммерческий результат
- он не является навсегда стабильным между всеми провайдерами

## 4. Benchmark statuses

Источник в коде:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Семейства benchmark-метрик:

- `lcp_seconds`
- `cls`
- `inp_ms`
- `schema_coverage`
- `ai_visibility_readiness`
- `factual_consistency`

Каждая метрика получает один из статусов:

- `better_than_baseline`
- `worse_than_baseline`
- `urgent_fix`
- `insufficient_data`

Как это понимать:

- benchmark status проще объяснять, чем raw numbers в отрыве от контекста
- его надо читать рядом с evidence, а не как истину сам по себе

## 5. Heuristic script scores

Часть repo scripts специально отдает heuristic, а не fully deterministic scores:

- `scripts/citability_score.py`
- `scripts/ai_readability_audit.py`
- `scripts/rag_chunk_audit.py`
- `scripts/schema-coverage-checker.py`
- `scripts/faq-detector.py`

Они полезны, потому что быстро поднимают реальные слабые места.

Их ограничения:

- HTML parsing не равен реальному поведению моделей
- client-side rendering может прятать контент от простых детекторов
- поведение провайдеров меняется
- коммерчески сильная страница может выглядеть средне в рамках bounded detector

## Что можно говорить публично

Безопасные формулировки:

- “transparent, bounded scoring for prioritization”
- “directional proxy for AI citation readiness”
- “evidence-backed audit scoring”

Нежелательные формулировки:

- “proprietary AI score, который предсказывает rankings”
- “гарантированный citation score”
- “одно число, которое доказывает SEO-успех”

## Как правильно использовать score

Используйте score, чтобы:

- сравнивать before vs after
- сортировать backlog
- объяснять, почему что-то выросло или упало
- строить repeatable operator rhythm

Не используйте score, чтобы:

- обещать результат сам по себе
- прятать слабые доказательства
- сводить любой бизнес к одному числу

## Что улучшает v6

`v6.0.0` не делает вид, что scoring уже идеален.

Он делает его:

- явным
- привязанным к коду
- объяснимым для человека
- безопасным для AI-агентов, которым надо описывать репозиторий без overclaiming
