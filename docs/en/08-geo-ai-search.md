# GEO and AI Search

`v3.2.0` makes the GEO/AI layer more concrete, more measurable, more scenario
driven, and more honest about volatility.

## Three outcome layers

GEO/AI work should be judged through three distinct outcome layers:

| Outcome layer | What it means | Stable metrics | Proxy metrics | Main risk |
|---|---|---|---|---|
| Rankings | Classical search visibility and qualified organic traffic | indexation, CWV, schema coverage, rankings, CTR | branded query lift | treating GEO as a substitute for SEO |
| AI citations / AI visibility | Whether LLM answer surfaces mention, cite, and correctly frame the brand | none are fully stable across vendors | AI SoV, AI Citation Score, answer-surface coverage | overclaiming volatile proxy metrics |
| Conversion and trust | Whether discoverability turns into leads, pipeline, or brand trust | form submissions, calls, assisted conversions | qualitative sales feedback, branded demand | visibility with no commercial intent or trust |

## What affects which layer

| Action | Rankings | AI visibility | Conversion and trust |
|---|---|---|---|
| Technical SEO hygiene | High | Medium | Medium |
| Canonical fact consistency | Medium | High | High |
| Answer-ready page structure | Medium | High | High |
| JSON-LD and entity clarity | High | High | Medium |
| llms.txt / AI bot accessibility | Low | Medium | Low |
| Strong offer, proof, and CTA design | Medium | Medium | High |
| Consistent brand mentions off-site | Medium | High | Medium |

## Minimal program by constraint

If time or resources are limited:

1. Fix crawlability, rendering, speed, canonicalization, and indexability.
2. Align homepage, about, service, FAQ, contacts, and policy pages on facts.
3. Add answer-ready sections and structured data to money pages.
4. Review robots rules for the AI/search surfaces that matter to your providers.
   Publish `llms.txt` only if it supports your publisher or agent workflow, and
   treat AI SoV as a proxy, not as ground truth.
5. Tie every GEO/AI action to one business-facing page or one buyer journey.

## Decision tree

- If technical SEO is weak, fix that before scaling GEO layers.
- If the brand is cited but misrepresented, prioritize fact consistency and
  entity clarity.
- If the site is readable by bots but weak for humans, improve proof, offer
  clarity, and conversion flow.
- If AI visibility rises without business lift, revisit audience intent and
  page-level commercial framing.

## GEO/AI execution loop

1. Baseline technical SEO and business goals.
2. Baseline AI surfaces and citation proxies.
3. Map entity facts, offer clarity, and answer-ready gaps.
4. Patch key pages and structured data.
5. Monitor changes in search, AI, and business layers separately.
6. Reclassify findings as observed fact, inferred issue, hypothesis, or
   recommended action.

## What not to promise

- guaranteed AI citations
- deterministic rankings from `llms.txt`
- universal benefits from experimental AI guidance files across every search or
  answer engine
- one universal GEO playbook for every niche
- “AI optimization” without technical SEO, facts, and trust assets

## Related docs

- [geo-measurement-maturity.md](./geo-measurement-maturity.md)
- [geo-business-outcomes.md](./geo-business-outcomes.md)
- [geo-priority-maps.md](./geo-priority-maps.md)
- [geo-ai-surfaces.md](./geo-ai-surfaces.md)
- [answer-ready-patterns.md](./answer-ready-patterns.md)
- [entity-seo-and-kg.md](./entity-seo-and-kg.md)
- [geo-red-team-and-risks.md](./geo-red-team-and-risks.md)
