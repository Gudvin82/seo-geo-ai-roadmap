# Discoverability Coverage in v3.7.0

`v3.7.0` adds a broader practical discoverability coverage layer on top of the
scanner foundation.

## What is now checked

- RU and AI bot policy, including `YandexAdditional`
- `ai.txt` structure and consistency hints
- JSON-LD schema coverage, including `WebSite`
- FAQ and answer-ready patterns
- Open Graph and Twitter Card completeness
- `robots.txt` ↔ sitemap linkage

## Why this matters

This is shared hygiene across SEO, GEO, RU search, and AI discoverability.
These checks do not guarantee ranking or citations, but they reduce ambiguity
and make operator review more concrete.

## Available scripts

```bash
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/check-ai-txt.py --url https://example.com
python scripts/schema-coverage-checker.py --url https://example.com --site-type service
python scripts/faq-detector.py --url https://example.com
python scripts/open-graph-checker.py --url https://example.com
python scripts/robots-sitemap-link-checker.py --url https://example.com
```

## Reporting model

Each module should resolve into:

- observed fact
- inferred issue
- recommendation
- limitation or uncertainty

Severity levels:

- `pass`
- `info`
- `warn`
- `fail`
- `needs-review`

## Current limitations

- FAQ detection is heuristic
- Open Graph checks do not prove real social rendering
- schema coverage focuses on JSON-LD, not exhaustive microdata parsing
- `ai.txt` remains an emergent pattern, not a guaranteed standard
- `YandexAdditional` policy checks `robots.txt`, not real inclusion by Yandex Neuro
