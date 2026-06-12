# Коннекторы search-data

`v3.1.0` переводит search-data и analytics connectors из простых примеров в
starter-слой для оператора с persisted connections, sync endpoints, явными
evidence-snapshots и полной EN/RU-документацией.

## Поддерживаемые starter-источники

- Google Search Console
- Google Analytics 4
- Yandex Webmaster
- Yandex Metrica

## Минимально полезный setup

1. Создайте отдельную интеграцию на каждый project.
2. Храните credentials в переменных окружения, а не в коде.
3. Сохраняйте внешний property ID, domain или counter ID в записи интеграции.
4. Делайте sync явно и используйте импорт как evidence-layer, а не как скрытый
   scoring.

## Что импортируется

- clicks
- impressions
- CTR
- average position
- top pages
- top queries
- visit или engagement signals там, где это применимо
- compact sync summary для операторского ревью

## Credentials и scopes

- GSC: service account или delegated credentials управляются вне репозитория
- GA4: API credentials управляются вне репозитория
- Yandex Webmaster: operator-managed token flow вне репозитория
- Yandex Metrica: operator-managed token flow вне репозитория

Этот релиз специально сохраняет управление credentials прозрачным. Приложение
хранит ссылку на env var, а не сам секрет.

## Текущий API flow

1. `POST /api/v1/integrations`
2. `POST /api/v1/integrations/{id}/sync`
3. `GET /api/v1/integrations?project_id=...`

## Privacy notes

- imported snapshots могут содержать коммерчески чувствительные performance
  данные
- оператору нужно защищать env vars и резервные копии базы
- evidence-данные стоит отдавать клиенту только через проверенные deliverables

## Текущие ограничения

- в `v3.1.0` реализованы starter-grade sync flows, а не full OAuth automation
- импортированные метрики структурированы для operator review, а не для прямой
  billing-логики
- source APIs всё ещё требуют project-specific валидации перед production use
