# CI Gating v3.8.0

GitHub Actions теперь рассматривается как first-class operating path, а не
просто как фоновая repo-quality проверка.

Machine-readable source:

- `GET /api/v1/settings/ci-gating`

Ключевая идея:

- валидировать command contracts
- валидировать согласованность docs и app
- прогонять recurring visibility и scanner-safe checks через workflows
