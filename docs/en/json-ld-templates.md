# JSON-LD Templates for GEO and AI

Use the templates in `templates/schema/` as production-oriented starters, not
as blind copy-paste blocks.

## Included templates

- `organization-schema.json`
- `faq-schema.json`
- `howto-schema.json`
- `product-schema.json`
- `service-schema.json`
- `local-business-schema.json`

## When to use each one

- Organization: brand entity, logo, sameAs, canonical identity
- Service: agency or expert service pages with offer definition
- Product: SaaS, software, or productized offer pages
- FAQ: objection handling, support answers, direct-response sections
- HowTo: procedural guidance with real ordered steps
- LocalBusiness: location-specific commercial pages

## How to adapt them safely

- replace placeholder names, URLs, identifiers, and prices
- keep every claim aligned with visible page content
- connect organization, service, product, and local pages back to one entity
- do not add schema for content that the page itself does not support

## Validation workflow

1. Copy the nearest starter template.
2. Replace placeholders with real page data.
3. Check that the page visibly contains the same facts.
4. Validate the JSON locally.
5. Re-test after deployment.

## Minimum production checklist

- canonical URL is correct
- brand name matches visible copy
- service or product descriptions are not contradictory
- prices, offers, and area served fields reflect the live page
- FAQ answers are visible on-page, not hidden only in schema

## Common mistakes

- adding every possible schema type to one page
- leaving fake identifiers or example.com URLs in production
- publishing FAQ schema for answers the page does not actually show
- using local business schema with no address, phone, or local intent

## GEO/AI benefit

These templates reduce ambiguity. They do not guarantee citations, but they
make it easier for search systems and models to map the right entity, offer,
and supporting page.
