# Product Surfaces v4.0.0

Теперь репозиторий явно разделен на три поверхности:

- `scanner surface`: URL-first intake, gated active scans и self-serve вход для лида или клиента
- `product/app surface`: dashboards, executive reporting, integrations, graph intelligence и task export
- `repo/docs/operator surface`: prompts, scripts, contracts, architecture и release discipline

Это разделение отражено в:

- `README` и `README_RU`
- `START_HERE_FOR_AI*`
- `/api/v1/settings/product-modes`
- frontend entrypoints для scanner, app и graph
