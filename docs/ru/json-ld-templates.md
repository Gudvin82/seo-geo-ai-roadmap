# JSON-LD Templates для GEO и AI

Используйте шаблоны из `templates/schema/` как production-oriented starters, а
не как бездумный copy-paste.

## Что входит

- `organization-schema.json`
- `website-schema.json`
- `faq-schema.json`
- `howto-schema.json`
- `product-schema.json`
- `service-schema.json`
- `local-business-schema.json`

## Когда какой шаблон уместен

- Organization: brand entity, logo, sameAs и canonical identity
- WebSite: site-level identity, search action, language framing и publisher linkage
- Service: страницы услуг агентства или эксперта
- Product: SaaS, software или productized offer pages
- FAQ: снятие возражений и direct-response sections
- HowTo: процедурные материалы с реальными ordered steps
- LocalBusiness: коммерческие страницы, завязанные на локацию

## Как безопасно адаптировать

- замените placeholder names, URLs, identifiers и prices
- держите все claims синхронными с видимым контентом страницы
- связывайте organization, service, product и local pages с одной entity logic
- не добавляйте schema для того, что сама страница не подтверждает

## Workflow проверки

1. Возьмите ближайший starter template.
2. Замените placeholders на реальные данные страницы.
3. Убедитесь, что те же факты видны в самом page content.
4. Провалидируйте JSON локально.
5. Повторно проверьте после деплоя.
6. Для live page прогоните `python scripts/schema-coverage-checker.py --url https://example.com --site-type service`.

## Минимальный production checklist

- корректный canonical URL
- brand name совпадает с видимым copy
- service или product descriptions не противоречат странице
- prices, offers и area served отражают live version страницы
- FAQ answers реально показаны на странице, а не только спрятаны в schema

## Частые ошибки

- попытка добавить все возможные schema types на одну страницу
- забытые fake identifiers или example.com URLs в production
- FAQ schema для ответов, которых пользователь не видит на странице
- local business schema без адреса, телефона или local intent

## Польза для GEO/AI

Эти шаблоны снижают двусмысленность. Они не гарантируют citations, но помогают
поиску и моделям связать правильную entity, offer и supporting page.
