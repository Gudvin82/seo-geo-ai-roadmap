# Privacy-First Measurement

Use this path when product policy, regulation, or visitor trust rules out a
third-party browser analytics tag.

## What remains measurable

- server access logs with IP minimization and a documented retention period
- Search Console and Yandex Webmaster aggregate search performance
- consented CRM events and offline conversion imports
- self-hosted, cookieless analytics chosen and operated by the deployer
- synthetic performance checks and CrUX aggregate field data

## Operating rules

1. Collect the minimum metric needed for a decision.
2. Keep raw logs separate from the evidence pack and restrict operator access.
3. Label every metric by source: `server`, `search_console`, `webmaster`,
   `consented_crm`, `synthetic`, or `field_aggregate`.
4. Never infer an individual visitor's identity from an audit artifact.
5. State measurement gaps in the final report instead of filling them with an
   estimated conversion claim.

## Decision use

This mode can still compare crawlability, index coverage, search demand,
landing-page quality, performance, citation readiness, and approved business
outcomes. It cannot replace a properly consented product-analytics study where
that study is required.
