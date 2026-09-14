# v6.14.0 Release Summary

`v6.14.0` is a trust and documentation-consolidation release. It does not add
new GEO theories or claim new provider connections.

## Capability Matrix

The public API, generated JSON/Markdown artifacts, and release CI now use one
canonical capability registry. Every shipped surface is classified as exactly
one of:

- `production_ready`
- `connected`
- `foundation`
- `stub`

Each row includes its operational evidence and boundary. In particular, a
credential-gated connector remains `foundation` until an operator-owned E2E
proof record exists; a starter script remains `stub`.

## Score Calibration

The GEO score is now explicitly documented and checked as an explainable
readiness score. Calibration data must include an independent case identity,
date, comparable outcome definition, observation window, and evidence
reference. The utility returns `insufficient_evidence` until a dataset meets
those requirements and contains at least 30 independent records.

## Documentation

The canonical EN/RU map is now paired and machine-checked. Superseded reviewer
prompts, evaluation kits, and launch wrappers moved to `archive/`; maintained
operator and community assets remain in their existing entrypoints.

## Verification

- root tests
- backend tests
- Ruff lint and formatting
- generated capability and documentation parity checks
- strict MkDocs build
- YAML and frontend syntax checks
