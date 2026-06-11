# Коннекторы search-data

В репозитории есть starter-коннекторы для команд, которые позже захотят
обогащать аудиты данными из Google Search Console и Яндекса.

## Что уже включено

- `scripts/gsc_data_stub.py`
- `scripts/yandex_data_stub.py`

## Какие данные ожидаются дальше

- clicks
- impressions
- average position
- top queries
- top landing pages
- geo split или market split, где доступно

## Рекомендуемый подход

1. Сначала убедитесь, что базовый audit-flow полезен без сторонних API.
2. Подключайте GSC и Яндекс только после стабилизации базового процесса.
3. Храните импорт как явный evidence-layer, а не как скрытый scoring.
4. Давайте оператору сопоставлять API evidence с AI SoV и brand-facts output.
