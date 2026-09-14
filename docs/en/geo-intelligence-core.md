# GEO Intelligence Core

`v6.10.0` adds an evidence-first operating loop without replacing the existing
scanner, graph, integrations, reports, or task center.

Run a report from operator-reviewed or provider-derived observations:

```bash
python scripts/geo_intelligence.py audit https://example.com \
  --input examples/geo-intelligence-observations.json
```

The canonical artifact is JSON. Markdown is a rendering of the same artifact.
Every observation must record a source, confidence, evidence type, and a
verification method. Supported evidence types are `verified`,
`provider-derived`, `heuristic`, and `manual-review`.

Scores are configurable decision aids. They do not prove AI citations, search
rankings, traffic, or conversion. Missing components are explicitly reported as
`insufficient_data` rather than silently treated as passing.

Available commands: `audit`, `score`, `entity`, `citation`, `roadmap`,
`monitor`, and `doctor`. The first six share the same evidence contract;
`doctor` reports local capability readiness and never exposes credentials.
