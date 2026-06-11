# International SEO

> **Tags:** [INT]  
> **Priority:** Medium  
> **Roadmap phase:** Month 2-6

## Why It Matters

This section matters because discoverability grows only when hreflang, market splits, localization, governance are handled as an execution system rather than isolated tasks.

## When to Use

Use it for multi-language and multi-region programs. Prioritize it early if the site is launching, relaunching, or recovering from a traffic or trust problem.

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
2. Break the work into actions around hreflang, market splits, localization, governance.
3. Assign one owner, one QA gate, and one reporting metric for each action.
4. Ship changes in small batches with validation notes.
5. Review impact monthly and feed learnings back into the roadmap.

## Validation / QA

- Check that every action can be traced to a page, owner, and KPI.
- Confirm the changes are visible in HTML, analytics, or reporting artifacts.
- Reject work that cannot be rechecked by another teammate.

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
Task: produce an action plan for International SEO with priorities, QA steps, risks, and expected outputs.
Output format: markdown table plus bullet actions.
Evaluation criteria: clarity, feasibility, business alignment, measurable next steps.
```

## Expected Outputs

- Prioritized backlog entry
- Owner and validation rule
- Reusable artifact such as checklist, brief, or report note

## Examples

Example AI Agency applies International SEO first to audit, GEO service pages, and branded AI prompts before scaling to the full blog.

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

- [04-site-architecture.md](./04-site-architecture.md)
- [18-analytics.md](./18-analytics.md)
- [24-roadmap.md](./24-roadmap.md)
