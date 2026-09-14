# v6.13.0 Productization Layer

`v6.13.0` makes the existing runtime easier to use. It does not add new GEO
scores, new autonomous agents, or new claims about AI citations.

## One product path

The thin CLI calls the running self-hosted application:

```bash
export GEO_SCANNER_SESSION=local-dev-session
python scripts/geo.py audit https://example.com
python scripts/geo.py score https://example.com
python scripts/geo.py roadmap https://example.com
```

`monitor` reads persisted project visibility history and therefore also requires
an authenticated project token and project id.

## Unified report

Scanner machine reports now pass through an adapter to the same canonical
Finding/Evidence contract used by project audits. One Unified GEO Intelligence
Report links executive summary, score, technical SEO, entity, citation,
authority, AI visibility, competitor gaps, evidence, roadmap, tasks, graph, and
a repeat-audit verification plan.

## Integration maturity

The integration lifecycle endpoint labels sources by evidence of readiness:
`foundation`, `prototype`, `connected`, or `production_ready`. A source is not
production-ready merely because a schema or adapter exists. It needs authorized
credentials, a real API call, refresh/recovery where applicable, controlled
failure evidence, revocation/disconnect, and automated tests.

## Boundaries

- The CLI requires a running self-hosted API and a scanner session; it is not a
  local replacement for the application runtime.
- Disconnect removes the application connection record. Provider grant/token
  revocation remains an operator action because this app never stores secrets.
