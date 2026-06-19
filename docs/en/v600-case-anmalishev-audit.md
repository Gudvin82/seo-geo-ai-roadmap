# Case Study: anmalishev.ru public audit in v6

This case keeps the same evidence policy as the rest of the repository:

- public observations only
- bounded script outputs
- no private analytics claims
- explicit separation between real site strength and detector limitations

## Site

- URL: <https://anmalishev.ru/>
- Market: RU-first with EN surfaces
- Type: personal brand plus AI services and product surfaces

## What was checked

- homepage raw HTML
- `robots.txt`
- `sitemap.xml`
- `llms.txt`
- `ai.txt`
- Open Graph and Twitter metadata
- schema coverage
- FAQ detectability
- AI readability
- citability heuristic
- RAG chunk readiness heuristic

## Strong signals observed

- canonical is present
- hreflang is present
- Open Graph and Twitter fields are present
- Person, LocalBusiness, Service, WebSite, and FAQ schema are present
- `llms.txt` is public and valid
- `ai.txt` is public and coherent
- `robots.txt` is public, explicit, and AI-aware
- local and RU trust signals are strong

## Script results

- `check-llms-txt.py`: `PASS`
- `check-ai-txt.py`: `PASS`
- `open-graph-checker.py`: `PASS`
- `faq-detector.py`: `WARN`
- `schema-coverage-checker.py`: `WARN`
- `ai_readability_audit.py`: `WARN`, `50/100`
- `citability_score.py`: `WARN`, `55/100`
- `rag_chunk_audit.py`: `FAIL`

## Why the weak heuristic scores do not tell the whole story

The site is stronger than the raw heuristic scores suggest.

Main reason:

- meaningful content appears to rely partly on a client-rendered product layer
- bounded HTML detectors see less structure than a real user sees
- FAQ schema is present, but visible answer-ready layout is not strongly exposed to the detector

This is a real operating lesson:

- GEO and AI heuristics should not be confused with complete reality
- but they still reveal a useful improvement path

## Bounded interpretation

### SEO foundation

Strong.

The technical baseline is already above average for a founder-led site:

- canonical
- hreflang
- raw metadata
- public sitemap
- AI-facing files
- trust and legal structure

### GEO and AI readability

Mixed.

Facts and machine-readable assets are good, but answer-ready structure and
server-visible chunking can still improve.

### Local and RU readiness

Strong.

The site clearly communicates geography, entity identity, legal trust, and
Yandex-relevant market framing.

## Priority improvements

1. expose more visible FAQ and answer-ready HTML in the server response
2. add `Organization` schema alongside existing entities where it strengthens interpretation
3. add `BreadcrumbList` on pages where navigation hierarchy matters
4. strengthen heading-led chunk structure on important commercial pages
5. keep AI-facing files aligned with the site truth center

## Why this case matters

This case is useful because it shows the repository behaving honestly:

- public facts can already score well
- heuristics can still under-read a JS-heavy page
- bounded scripts are helpful, but operator interpretation is still required
