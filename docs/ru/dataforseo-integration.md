# Интеграция DataForSEO для классического SEO

Приложение может использовать аккаунт DataForSEO, которым управляет
оператор, для четырех ограниченных сценариев только на чтение:

- `keyword_research`: частотность и конкуренция Google Ads для заданных запросов
- `rank_tracking`: снимок текущей органической выдачи Google для одного запроса
- `competitor_intelligence`: конкуренты домена для выбранного рынка
- `backlink_intelligence`: сводка ссылок домена

DataForSEO тарифицирует live-запросы. Интеграция необязательна и отключена,
пока оператор явно не разрешит платные запросы в настройках каждого подключения.
Приложение не сохраняет логин и пароль провайдера.

Первая версия использует Google endpoints для частотности, органической SERP,
доменов-конкурентов и сводки backlinks; частотность и SERP Яндекса сюда не входят.
См. документацию провайдера: [search volume](https://docs.dataforseo.com/v3/keywords_data-google_ads-search_volume-live/),
[Google organic SERP](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/),
[domain competitors](https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/),
[backlink summary](https://docs.dataforseo.com/v3/backlinks-summary-live/) и
[тарифы](https://dataforseo.com/pricing).

## Настройка

Задайте переменные окружения backend:

```dotenv
DATAFORSEO_LOGIN=ваш-api-login
DATAFORSEO_PASSWORD=ваш-api-password
```

Создайте отдельное подключение для каждого сценария через интерфейс Integrations
или `POST /api/v1/integrations`. Укажите подходящий `source_type`, а в
`credentials_env_var` можно записать справочную строку
`DATAFORSEO_LOGIN,DATAFORSEO_PASSWORD`. Для анализа конкурентов и ссылок
задайте домен проекта в `property_identifier`.

Каждый config подключения должен явно содержать:

```json
{
  "allow_billable_requests": true,
  "approved_daily_budget_usd": 2.0,
  "max_requests_per_day": 5,
  "cache_ttl_seconds": 21600,
  "location_name": "Russia",
  "language_code": "ru"
}
```

Параметры отдельных сценариев:

- `keyword_research`: передайте `keywords` (от 1 до 30 строк) или сохраните `seed_keywords` в контексте проекта.
- `rank_tracking`: передайте `keyword`; `depth` ограничен диапазоном от 10 до 30, регион нужно указать явно.
- `competitor_intelligence`: используйте домен проекта как `property_identifier`; `limit` не превышает 100.
- `backlink_intelligence`: используйте домен проекта как `property_identifier`.

Дневной бюджет — локальный best-effort предохранитель на подключение, а не
жесткий лимит, обеспечиваемый DataForSEO. Провайдер тарифицирует запросы; точная
стоимость заранее не гарантируется, а параллельные запросы могут одновременно
пройти локальную проверку. До включения вызовов проверьте текущие тарифы и
баланс аккаунта. Интерфейс запрашивает явное согласие при создании подключения и
повторно перед каждой ручной платной синхронизацией. Автоматических повторов нет,
чтобы не дублировать платные POST-запросы. Если после сетевого сбоя стоимость
неизвестна, платные вызовы этого подключения блокируются до конца UTC-дня, пока
оператор не проверит аккаунт DataForSEO.

## Evidence, кеш и история

Успешный ответ содержит провайдера, рынок, язык, время наблюдения, ссылку на
задачу, фактическую стоимость из ответа, число запросов, TTL кеша и provenance.
Строки оборачиваются в Canonical Finding/Evidence с типом
`provider-derived`. Снимок сохраняется в подключении, компактная evidence
запись попадает в историю. Свежий снимок читается из кеша без нового платного
запроса.

Контекст можно сохранить в разделе проекта **«Контекст исследований проекта»**
или через endpoints:

- `GET /api/v1/projects/{project_id}/research-context`
- `PUT /api/v1/projects/{project_id}/research-context`

Контекст хранит конкурентов, цели, ключевые страницы и стартовые запросы.
Рынок и язык берутся из существующих полей проекта.

## MCP

Stateless Streamable HTTP MCP endpoint доступен по адресу `/api/v1/mcp`.
Укажите в MCP-клиенте URL self-hosted приложения и действующий bearer token.
Каждый инструмент проверяет доступ к проекту и читает только сохранённые данные:

- `get_project_context`
- `get_latest_unified_report` (включая findings, graph и task bundle)
- `list_project_evidence`
- `list_connected_sources`
- `list_ai_visibility_history`

Инструменты MCP не запускают DataForSEO и не создают расходы провайдера.
Для обновления подключения оператор использует авторизованный integration sync API.

Сейчас endpoint объявляет протокол эпохи handshake `2025-03-26`. Это ограниченная
совместимость, а не заявление о поддержке всех актуальных MCP-клиентов и новых
версий протокола. Сверьте [версию MCP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports),
которую поддерживает ваш клиент.

## Границы данных

Документированные endpoints DataForSEO платные и зависят от рынка. Частотность
является оценкой провайдера, rank tracking — снимком выдачи на конкретную дату,
backlink метрики — данными стороннего индекса, а пересечение доменов не
доказывает эквивалентность бизнеса. Эти сигналы не доказывают причинность
изменения позиций и не гарантируют цитирование AI-системами.
