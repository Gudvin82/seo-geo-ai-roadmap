# CI Gating v3.8.0

GitHub Actions is now treated as a first-class operating path, not just a repo
quality afterthought.

Machine-readable source:

- `GET /api/v1/settings/ci-gating`

Key idea:

- validate command contracts
- validate docs and app parity
- run recurring visibility and scanner-safe checks through workflows
