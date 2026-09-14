# v6.12.0 Release Summary

`v6.12.0` is an integration and runtime-hardening release. It does not claim
new deterministic GEO ranking or citation capabilities.

## Delivered

- A canonical Finding/Evidence contract used by new audit findings, reports,
  task bundles, graph-compatible views, and persisted proof records.
- A completed audit can now produce a GEO runtime artifact with independent
  entity, citation, authority, and competitor analyzer outputs.
- Score profiles validate weights, carry a version and calibration status, and
  return `insufficient_data` instead of assigning missing components a zero.
- AI visibility snapshots persist query, provider, model, observation time,
  evidence provenance, response reference, and history comparisons.
- The Agent Audit Pack is exposed as an executable contract with tools, limits,
  sequence, and approval gates.

## Boundaries

- Provider-derived evidence is only provider-derived; heuristic evidence does
  not prove AI citations, rankings, traffic, or conversions.
- The runtime is approval-bound and does not write to a CMS automatically.
- Historical audit records remain supported through a legacy adapter.
