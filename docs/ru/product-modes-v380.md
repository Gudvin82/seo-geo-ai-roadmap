# Product Modes v3.8.0

Чтобы репозиторий не выглядел как "все сразу", `v3.8.0` теперь разделяет три
first-class surfaces:

- Repo methodology mode
- App control panel mode
- Scanner intake mode

Machine-readable source:

- `GET /api/v1/settings/product-modes`

Идея простая:

- repo объясняет и маршрутизирует
- app управляет
- scanner принимает и экспортирует
