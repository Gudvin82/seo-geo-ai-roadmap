# Framework Integrations v3.8.0

Репозиторий остается framework-agnostic, но в `v3.8.0` яснее упакованы
integration patterns для:

- Next.js или static React frontends
- Astro content sites
- WordPress или headless CMS sites
- self-hosted scanner intake pages

## Рекомендуемый паттерн

1. держать репозиторий как audit и reporting core
2. выводить scanner intake под своим доменом или в client area
3. подключать provider configs и notifications на уровне workspace
4. экспортировать graph JSON, fix packs и reports в свою delivery-систему

## Почему это важно

Репозиторий проще интегрировать, когда command layer, graph layer и deliverables
описаны явно, а не подразумеваются.
