# Real Cases

This file does not claim private customer telemetry. It combines:

- current public signals that can be checked now
- bounded implementation records from the rollout process
- transparent methodology scoring rather than exaggerated success claims

Scoring model used in this file:

- Technical SEO and crawl readiness: `0-20`
- Factual consistency and truth-center discipline: `0-20`
- Entity clarity and trust proof: `0-20`
- AI readiness and answer extraction: `0-20`
- Reporting and operator packaging: `0-20`

Detailed case studies:

- [anmalishev.ru — public before / after case](./docs/en/v430-case-anmalishev.md)
- [auditguard.ru + sitepravo.ru — AI crawler access and public before / after case](./docs/en/v430-case-auditguard-sitepravo.md)

## sitepravo.ru

Current public signals observed:

- legal-service positioning is explicit
- public copy claims `570+` parameters and `15` directions
- legal documents, operator identity, and policy links are visible
- `robots.txt` now explicitly allows the target AI crawler set, including `ClaudeBot` and `YandexAdditional`

### Current snapshot

- Current public snapshot: `88/100`
- Current findings count in the bounded rollout model: `14`
- Current explicit AI-bot allow coverage in rollout records: `14/14`

### Bounded before / after implementation record

- Before GEO AI crawler hardening: `88/100`
- After GEO AI crawler hardening: `88/100`
- Findings delta in rollout record: `15 -> 14`
- AI-bot explicit allow coverage in rollout record: `6/14 -> 14/14`

Interpretation:

- the score stayed flat because the public product report for this surface does not weigh the GEO layer strongly
- the AI crawler access layer still improved materially
- this is a good example of “real discoverability improvement without vanity-metric inflation”

## auditguard.ru

Current public signals observed:

- public-first technical audit framing is clear
- homepage exposes `340+` parameters, `46+` tools, and `2-5` minute checks
- service explains scope, legal basis, and public-only audit boundary
- `llms.txt` is detailed and public
- `robots.txt` now explicitly allows the target AI crawler set, including `ClaudeBot` and `YandexAdditional`

### Current snapshot

- Current public snapshot: `94/100`
- Current findings count in the bounded rollout model: `11`
- Current explicit AI-bot allow coverage in rollout records: `14/14`

### Bounded before / after implementation record

- Before AI crawler hardening and false-positive cleanup: `92/100`
- After AI crawler hardening and false-positive cleanup: `94/100`
- Findings delta in rollout record: `13 -> 11`
- AI-bot explicit allow coverage in rollout record: `6/14 -> 14/14`

Interpretation:

- AI crawler intent became materially clearer
- false-positive leak findings around `llms.txt` and `ai.txt` were removed
- the gain is measurable both in bounded score and in public `robots.txt`

## anmalishev.ru

Current public signals observed:

- founder identity, legal details, and location are explicit
- RU and EN service surfaces are already visible
- the site links consulting, products, case studies, and methodology assets
- current `sitemap.xml` includes stronger canonical surfaces such as `/contacts`, `/projects/seo-geo-ai-roadmap.html`, `/expert/yandex-neuro-ai-visibility.html`, and `/expert/ai-site-audit.html`
- current `llms.txt` and `ai.txt` are coherent and public
- current `robots.txt` keeps public AI and search surfaces open while protecting admin or raw-template paths

### Current snapshot

- Current public snapshot: `88/100`

### Bounded before / after implementation record

- Before the June public-surface expansion: `79/100`
- After the June public-surface expansion: `88/100`
- Methodology delta: `+9`

Publicly visible sources of gain:

- stronger homepage entity and trust graph
- dedicated canonical contacts surface
- dedicated Yandex AI / Neuro page
- dedicated AI site audit page
- dedicated repository-overview page
- tighter alignment between `llms.txt`, `ai.txt`, `robots.txt`, and `sitemap.xml`

## Cross-case lessons

- factual consistency is its own subsystem, not a side note
- public proof matters more when several related entities cross-link
- bilingual discoverability performs better when EN and RU are governed as production layers
- AI visibility works best when it reinforces technical SEO instead of trying to replace it
- explicit AI crawler policy can create a real public delta even when a product score does not fully reflect it yet
- good case studies should separate current public facts from bounded rollout records and from unproven private outcomes

See also:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/en/canonical-facts-and-entity-consistency.md](./docs/en/canonical-facts-and-entity-consistency.md)
- [docs/en/v430-review-response-and-upgrade-path.md](./docs/en/v430-review-response-and-upgrade-path.md)
- [WALKTHROUGH.md](./WALKTHROUGH.md)
