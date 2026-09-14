# Сводка Релиза v6.14.0

`v6.14.0` - релиз доверия и консолидации документации. Он не добавляет новые
GEO-теории и не заявляет новые provider connections.

## Capability Matrix

Public API, generated JSON/Markdown artifacts и release CI теперь используют
один канонический capability registry. Каждая поставляемая поверхность получает
ровно один статус:

- `production_ready`
- `connected`
- `foundation`
- `stub`

В каждой строке есть operational evidence и граница. В частности,
credential-gated connector остается `foundation`, пока не появился
operator-owned E2E proof record; starter script остается `stub`.

## Калибровка Score

GEO score теперь явно описан и проверяется как explainable readiness score.
Данные калибровки должны содержать независимый case identity, дату,
сопоставимое outcome definition, observation window и evidence reference.
Инструмент возвращает `insufficient_evidence`, пока набор не отвечает этим
условиям и не содержит минимум 30 независимых записей.

## Документация

Каноническая EN/RU-карта теперь парная и machine-checked. Устаревшие reviewer
prompts, evaluation kits и launch wrappers перенесены в `archive/`; актуальные
operator и community assets остались на существующих entrypoints.

## Проверка

- root tests
- backend tests
- Ruff lint и formatting
- generated capability и documentation parity checks
- strict MkDocs build
- YAML и frontend syntax checks
