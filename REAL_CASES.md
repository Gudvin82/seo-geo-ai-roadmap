# Real Cases

This file does not claim private customer telemetry. It models how the
repository's methodology reads three public websites using public-facing
evidence and bounded manual scoring. The numbers below are transparent snapshot
scores, not exaggerated success claims.

Scoring model used in this file:

- Technical SEO and crawl readiness: `0-20`
- Factual consistency and truth-center discipline: `0-20`
- Entity clarity and trust proof: `0-20`
- AI readiness and answer extraction: `0-20`
- Reporting and operator packaging: `0-20`

## sitepravo.ru

Public signals observed:

- legal-service positioning is explicit
- public copy claims `570+` parameters and `15` directions
- legal documents, operator identity, and policy links are visible
- cross-linking with sister entities is already present

### SitePravo snapshot score

- Technical SEO and crawl readiness: `16/20`
- Factual consistency and truth-center discipline: `15/20`
- Entity clarity and trust proof: `18/20`
- AI readiness and answer extraction: `16/20`
- Reporting and operator packaging: `17/20`
- Total public snapshot: `82/100`

### SitePravo bounded before/after model

- Before first v3-style pass: `82/100`
- After first 30-day truth-center and AI-surface sync target: `88/100`
- Expected gain: `+6`

Likely sources of gain:

- reduce repeated fact surfaces into one canonical truth center
- tighten cross-entity boundaries with `anmalishev.ru` and sibling products
- keep numeric claims synchronized across homepage, metadata, docs, and
  AI-facing files

## auditguard.ru

Public signals observed:

- public-first technical audit framing is clear
- homepage exposes `340+` parameters, `46+` tools, and `2-5` minute checks
- service explains scope, legal basis, and public-only audit boundary
- trust and evidence framing are strong

### AuditGuard snapshot score

- Technical SEO and crawl readiness: `17/20`
- Factual consistency and truth-center discipline: `14/20`
- Entity clarity and trust proof: `16/20`
- AI readiness and answer extraction: `15/20`
- Reporting and operator packaging: `18/20`
- Total public snapshot: `80/100`

### AuditGuard bounded before/after model

- Before first v3-style pass: `80/100`
- After first 30-day fact-sync and entity-governance target: `86/100`
- Expected gain: `+6`

Likely sources of gain:

- tighter synchronization between public copy, evidence pages, and AI-facing
  files
- sharper separation between AuditGuard and the surrounding product ecosystem
- stronger repeatable benchmark reporting inside the self-hosted app flow

## anmalishev.ru

Public signals observed:

- founder identity, legal details, and location are explicit
- RU and EN service surfaces are already visible
- the site links consulting, products, case studies, and methodology assets
- "practical AI for business" positioning is clear and commercially grounded

### anmalishev.ru snapshot score

- Technical SEO and crawl readiness: `15/20`
- Factual consistency and truth-center discipline: `14/20`
- Entity clarity and trust proof: `17/20`
- AI readiness and answer extraction: `17/20`
- Reporting and operator packaging: `15/20`
- Total public snapshot: `78/100`

### anmalishev.ru bounded before/after model

- Before first v3-style pass: `78/100`
- After first 30-day entity-hierarchy and bilingual fact-sync target: `85/100`
- Expected gain: `+7`

Likely sources of gain:

- clearer separation between founder entity, offers, products, and frameworks
- one canonical fact layer for legal, service, and product claims
- more explicit AI-facing truth surfaces for multilingual routing

## Cross-case lessons

- factual consistency is its own subsystem, not a side note
- public proof matters more when several related entities cross-link
- bilingual discoverability performs better when EN and RU are governed as
  production layers
- AI visibility works best when it reinforces technical SEO instead of trying
  to replace it

See also:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/en/canonical-facts-and-entity-consistency.md](./docs/en/canonical-facts-and-entity-consistency.md)
- [WALKTHROUGH.md](./WALKTHROUGH.md)
