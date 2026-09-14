# GEO Intelligence Orchestrator

Use `scripts/geo_intelligence.py` as the canonical runner. Start with supplied
evidence, preserve its source and confidence, then produce a plan. Do not claim
that a heuristic score proves ranking, AI citation, traffic, or conversion.

## Input contract

- Absolute target URL.
- Observation JSON matching `contracts/geo-intelligence.schema.json`.
- Optional score weights only when an operator supplies a justified profile.

## Output contract

1. Canonical JSON report.
2. Markdown client summary rendered from that JSON.
3. Tasks with owner, dependency, verification, and approval status.

Never publish changes. Mark missing evidence as `manual-review` or
`insufficient_data`; do not invent provider results.
