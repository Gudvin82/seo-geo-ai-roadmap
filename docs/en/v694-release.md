# v6.9.4 Release Summary

`v6.9.4` is a release-integrity and runtime-hardening update.

## What changed

- Active application, frontend, contract, script, and current-document markers
  use `v6.9.4`.
- Tag releases now run a dedicated integrity gate that verifies `HEAD`, the
  Git tag, runtime version, release notes, and public entrypoints together.
- The integration capability matrix is generated from the runtime registry and
  labels each surface as live read-only, operator-guided, or starter/stub.
- The Docker worker now processes the database-backed scanner queue continuously
  and applies bounded retry plus dead-letter handling after worker failures.
- GSC and Yandex Webmaster gain read-only live API adapters for credentials
  owned by the operator. No tokens are persisted by the app.
- Privacy-first measurement and independent-case submission playbooks are now
  canonical documentation surfaces.
- A calibration utility now reports score/outcome correlation only from
  operator-supplied evidence and marks small samples as insufficient.

## Boundaries

Live connectors require the deployer's credentials and property access. Other
sources remain explicitly starter or operator-guided until a corresponding live
adapter exists. Scoring remains an auditable decision aid, not a promise of
rankings, traffic, conversions, or AI citations.
