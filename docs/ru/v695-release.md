# Сводка релиза v6.9.5

`v6.9.5` добавляет собственный Content Operations Engine с approval-first
подходом.

## Что Изменилось

- Добавлена content operations queue: она превращает demand от оператора в
  объяснимые редакционные задачи с owner.
- Добавлены обязательные factual, editorial, legal, technical и post-publish
  гейты.
- Добавлен двуязычный playbook для demand, брифов, quality control, freshness и
  проверки каннибализации.
- Автоматическая публикация явно оставлена вне scope.

## Граница

Очередь - инструмент планирования. Ее score не прогнозирует позиции, трафик,
конверсии или AI citations.
