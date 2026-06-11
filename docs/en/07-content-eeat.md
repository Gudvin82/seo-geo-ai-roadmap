# Content and E-E-A-T

> **Tags:** [U] [AI/GEO]  
> **Priority:** High  
> **Roadmap phase:** Month 1-6

## Why It Matters

This section matters because discoverability grows only when experience, proof, experts, citations, answer-ready blocks are handled as an execution system rather than isolated tasks.

## When to Use

Use it for YMYL, B2B, local experts, agencies, SaaS. Prioritize it early if the site is launching, relaunching, or recovering from a traffic or trust problem.

## Outcomes

- Clear decisions instead of assumptions
- Repeatable workstream with owners and QA
- Inputs for reporting, prioritization, and release planning

## Inputs Required

- Current site URLs, analytics access, and business goals
- List of priority offers, regions, and audience segments
- Access to at least one SEO crawl and one AI testing workflow

## Step-by-Step Instructions

1. Document the current state and desired business outcome.
2. Capture both search-engine and AI-surface implications before deciding what to ship.
3. Break the work into actions around experience, proof, experts, citations, answer-ready blocks.
4. Assign one owner, one QA gate, and one reporting metric for each action.
5. Ship changes in small batches with validation notes.
6. Review impact monthly and feed learnings back into the roadmap.

## Validation / QA

- Check that every action can be traced to a page, owner, and KPI.
- Confirm the changes are visible in HTML, analytics, or reporting artifacts.
- Reject work that cannot be rechecked by another teammate.
- Keep before/after evidence in screenshots, exports, or markdown notes.

## Checklist

- [ ] Scope documented
- [ ] Owner assigned
- [ ] Validation method defined
- [ ] Expected output prepared
- [ ] Release note ready

## Decision Tree

- If the section affects crawling, fix technical blockers before content expansion.
- If the section affects trust or conversion, ship to money pages before secondary pages.
- If AI outputs are unstable, add proof assets and stricter answer-ready formatting.

## Prompts for AI / Codex

```text
Role: Senior discoverability strategist.
Inputs: business context, target market, current pages, known blockers.
Task: produce an action plan for Content and E-E-A-T with priorities, QA steps, risks, and expected outputs.
Output format: markdown table plus bullet actions.
Evaluation criteria: clarity, feasibility, business alignment, measurable next steps.
```

## Expected Outputs

- Prioritized backlog entry
- Owner and validation rule
- Reusable artifact such as checklist, brief, or report note
- Short decision log for future releases

## Examples

Example AI Agency applies Content and E-E-A-T first to audit, GEO service pages, and branded AI prompts before scaling to the full blog.

## Common Mistakes

- Treating the work as a one-time task instead of an operating loop.
- Shipping changes without a validation owner.
- Mixing several intents or markets into one page or report.

## Anti-Patterns

- Framework theater: long docs with no execution path.
- Metrics without business interpretation.
- AI-generated text with no proof, examples, or review.

## Tools

| Tool | Market | Free | Use |
|---|---|---|---|
| Google Search Console | Global | Yes | search performance, coverage, indexing |
| Bing Webmaster Tools | Global | Yes | Bing visibility and crawl diagnostics |
| Yandex Webmaster | RU/CIS | Yes | indexation and diagnostics for Yandex |
| Yandex Metrica | RU/CIS | Yes | behavioral analytics and goals |
| Screaming Frog | Global | Partly | crawl audits and extraction |
| ChatGPT / Claude / Gemini / Codex | Global | Partly | analysis, drafting, QA, prompt testing |

## Related Sections

- [06-semantics-onpage.md](./06-semantics-onpage.md)
- [08-geo-ai-search.md](./08-geo-ai-search.md)
- [14-neural-search-ai.md](./14-neural-search-ai.md)
