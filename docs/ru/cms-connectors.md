# CMS Connectors

## Текущий scope

`v2.2.0` задает WordPress-first направление и фиксирует ожидаемый patch-flow.

## WordPress

- забирать списки страниц и постов через REST API
- маппить URL, titles и statuses в audit workflows
- экспортировать implementation notes в draft-ready формате
- оставлять human review обязательным перед публикацией
- starter script: `scripts/wordpress_connector_starter.py`
- starter script: `scripts/wordpress_connector_starter.py`

## Webflow

- пока описан как starter path
- сначала рекомендуется read-only inventory и export-first workflow
- direct writeback остается задачей roadmap

## Что ожидается от patch mode

- read-only inventory безопасен по умолчанию
- generated changes должны становиться задачами, draft-черновиками или diff-like suggestions
- прямая публикация должна быть opt-in и проходить human review
