# GEO Intelligence Core

`v6.10.0` добавляет evidence-first operating loop, не заменяя существующие
scanner, graph, integrations, reports и task center.

Запуск отчета из проверенных оператором или provider-derived наблюдений:

```bash
python scripts/geo_intelligence.py audit https://example.com \
  --input examples/geo-intelligence-observations.json
```

Канонический артефакт - JSON. Markdown является представлением того же
артефакта. У каждого наблюдения должны быть source, confidence, evidence type и
verification method. Поддерживаются `verified`, `provider-derived`,
`heuristic` и `manual-review`.

Score - это configurable decision aid. Он не доказывает AI citation, позиции,
трафик или конверсию. Отсутствующие компоненты явно получают
`insufficient_data`, а не считаются пройденными.

Доступны команды `audit`, `score`, `entity`, `citation`, `roadmap`, `monitor` и
`doctor`. Первые шесть используют один evidence contract; `doctor` показывает
готовность локальных возможностей и не раскрывает credentials.
