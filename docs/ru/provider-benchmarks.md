# Бенчмарки провайдеров

Используйте этот документ, когда нужен повторяемый benchmark-layer для cloud и
local providers перед внедрением в клиентскую работу.

## Измерения

- factual consistency относительно известного brand-facts файла
- качество ответа на EN и RU
- стабильность structured output
- дисциплина citations
- latency
- cost
- объем ручной доработки после генерации

## Практический flow

1. Выберите один проект и один утвержденный brand-facts profile.
2. Прогоните один и тот же audit или prompt set минимум через трех providers.
3. Сохраните output, time-to-first-token, полную длительность и human review notes.
4. Оцените каждого провайдера по простой шкале 1-5 по каждой категории.
5. Повторяйте ежемесячно или после обновления модели.

## Стартовые инструменты

- app provider configurations в UI
- `scripts/provider_benchmark_stub.py`
- `docs/ru/local-llm-matrix.md`
- `docs/ru/provider-matrix.md`

## Рекомендация

Не выбирайте provider только по raw output quality. Для self-hosted SEO, GEO и
AI visibility обычно выигрывает тот, кто дает лучший баланс прозрачности,
стабильности, EN/RU покрытия, скорости и review burden.
