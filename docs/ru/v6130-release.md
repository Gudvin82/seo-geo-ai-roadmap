# v6.13.0 Productization Layer

`v6.13.0` упрощает использование уже существующего runtime. Релиз не добавляет
новые GEO scores, автономных агентов или новые обещания AI citations.

## Один product path

Thin CLI вызывает запущенное self-hosted приложение:

```bash
export GEO_SCANNER_SESSION=local-dev-session
python scripts/geo.py audit https://example.com
python scripts/geo.py score https://example.com
python scripts/geo.py roadmap https://example.com
```

`monitor` читает сохраненную project visibility history, поэтому также требует
authenticated project token и project id.

## Unified report

Scanner machine reports теперь проходят через adapter к тому же Canonical
Finding/Evidence Model, что и project audits. Один Unified GEO Intelligence
Report связывает executive summary, score, technical SEO, entity, citation,
authority, AI visibility, competitor gaps, evidence, roadmap, tasks, graph и
repeat-audit verification plan.

## Integration maturity

Lifecycle endpoint маркирует источники по уровню доказанной готовности:
`foundation`, `prototype`, `connected` или `production_ready`. Источник не
становится production-ready только из-за schema или adapter: нужны authorized
credentials, реальный API call, refresh/recovery где применимо, controlled
failure evidence, revocation/disconnect и automated tests.

## Границы

- CLI требует запущенный self-hosted API и scanner session; это не локальная
  замена application runtime.
- Disconnect удаляет connection record приложения. Revocation provider grant
  или token остается действием оператора, так как приложение не хранит secrets.
