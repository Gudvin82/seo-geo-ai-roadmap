# Technical SEO Deep Playbook

This playbook exists to turn “check canonical and sitemap” into a real operator
workflow.

## Use this when

- the site is new, recovering, or being restructured
- pages are missing from search or underperforming
- the site is JS-heavy
- AI visibility looks weak because the technical surface is inconsistent

## What to inspect first

1. response codes for priority pages
2. canonical consistency
3. robots rules
4. sitemap hygiene
5. internal linking into money pages
6. rendering and server HTML availability
7. Core Web Vitals and asset weight
8. redirect chains and duplicate URL surfaces

## What “good” looks like

- every important page returns `200`
- canonical points to the page you actually want indexed
- robots rules protect only non-public or low-value surfaces
- sitemap contains canonical, indexable, current URLs
- server HTML exposes the critical business meaning of the page
- money pages receive internal links from relevant hubs
- CWV does not block usability on high-intent pages

## Common failure patterns

### Canonical conflict

Symptoms:

- canonical points to another page
- paginated or filtered pages collapse into the wrong target
- localized pages canonicalize to the default language

What to do:

- map each page type to an intentional canonical rule
- document exceptions, especially filters, tags, or language variants
- verify the final HTML, not just the CMS settings

### Sitemap pollution

Symptoms:

- old URLs remain in sitemap
- redirected URLs are still listed
- thin utility pages are present
- duplicated language or parameter URLs appear

What to do:

- export the current sitemap
- group URLs by page type
- remove redirected, blocked, duplicate, or non-canonical entries
- keep a clean canonical sitemap for the pages you want indexed

### JavaScript SEO gap

Symptoms:

- the raw HTML is thin
- content appears only after hydration
- structured data is injected late or inconsistently
- AI or crawler heuristics see less than users do

What to do:

- inspect raw HTML first
- expose title, headings, critical copy, facts, and schema server-side
- do not rely on client-side rendering for the business meaning of a page

### Internal linking weakness

Symptoms:

- strong commercial pages have few contextual links
- blog or support content does not pass relevance into service pages
- hubs are present visually but not semantically

What to do:

- map hub → service → proof → conversion page flows
- ensure contextual links use clear anchor language
- prioritize links into pages that matter for revenue or entity clarity

## Priority framework

Fix first:

1. indexing and crawl blockers
2. wrong canonicalization
3. rendering gaps on money pages
4. sitemap pollution
5. internal-linking gaps
6. CWV and redirect optimization

## Proof and QA

For each fix, store:

- before state
- after state
- page or template affected
- validation method
- expected business or discoverability effect

Do not ship technical SEO work as “done” without proof.

## Pair this with

- [../05-technical-seo.md](./05-technical-seo.md)
- [../../checklists/en/technical-seo-checklist.md](../../checklists/en/technical-seo-checklist.md)
- [./scoring-model-v340.md](./scoring-model-v340.md)
