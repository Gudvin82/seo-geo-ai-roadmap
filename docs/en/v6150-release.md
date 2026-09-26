# v6.15.0 Release Summary

`v6.15.0` connects classic SEO research to the existing integration runtime and
gives AI clients an authenticated read-only view of saved project evidence.

## What changed

- DataForSEO now serves four credential-gated flows: keyword search metrics,
  Google organic live SERP, domain competitor discovery, and backlink summary.
- Each provider call requires explicit billable opt-in, an approved daily budget,
  and a per-day request limit. The connector reports actual response cost,
  market, language, observation time, provenance, TTL, cache hits, and canonical
  `provider-derived` evidence.
- Fresh snapshots are reused from persistent integration state. The app never
  retries a billable POST automatically; an unknown billing outcome blocks
  further paid calls for that connection for the UTC day pending operator review.
- Project research context stores competitors, goals, key pages, and seed
  keywords. Existing project market and language remain authoritative.
- `/api/v1/mcp` exposes project-scoped read tools for context, the latest
  unified report with graph and tasks, evidence records, connected snapshots,
  and AI visibility history.

## Runtime and security boundaries

- DataForSEO login and password are read from environment variables only; they
  are not persisted in connection config or snapshots.
- Provider hosts and endpoint paths are fixed in code. Redirects are disabled.
- MCP requires the app's bearer authentication and project membership. It only
  reads stored state and cannot trigger billable provider operations.
- DataForSEO signals are third-party estimates and dated observations. They do
  not prove ranking causality or guarantee traffic or AI citations.
- The local daily budget is a best-effort guard, not a hard provider-enforced
  cap; parallel calls can race and a provider response may report an overrun.

## Release status

The connector implementation and app integration are in place. A credentialed
live DataForSEO round trip requires operator account credentials and explicit
spend approval; without those, the connector remains classified as `foundation`
until that external proof exists.
