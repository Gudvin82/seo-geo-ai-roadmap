# Сводка релиза v6.1.0

`v6.1.0` делает RU/Yandex GEO-слой более реальным за счет того, что
официальная `Видимость сайта в Алисе AI` из Яндекс Вебмастера становится
first-class surface внутри продукта.

## Что изменилось

- добавлен новый integration source `alice_ai_visibility`
- добавлен starter payload с weekly SoV, примерами запросов и overlap по сайтам
- добавлен `ru_geo_score` в executive dashboard
- расширен RU executive layer: Webmaster, Metrica, Direct, Neuro и Alice AI
  теперь смотрятся вместе
- обновлены RU и EN документы методологии, чтобы Алиса AI считалась
  официальным answer-surface сигналом Яндекса

## Почему это важно

До `v6.1.0` repo смотрел на RU AI discoverability в основном через:

- `YandexAdditional`
- `Yandex Neuro readiness`
- RU answer-ready content

После `v6.1.0` продукт может отдельно выражать:

- официальный share of voice по Алисе AI
- сценарий `insufficient data`
- review по запросам, страницам и сайтам-источникам
- более ясный RU GEO operating score

## Чего релиз все еще не обещает

- прямого управления ответами Алисы AI
- гарантированного попадания в ответы Яндекс AI
- готового публичного SaaS вокруг Яндекс API

Это все еще честная self-hosted execution system с operator-first моделью.
