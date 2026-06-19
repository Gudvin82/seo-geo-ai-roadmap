# Repo + Site Audit Agent Prompt

Use this when handing the repository to an AI coding agent and you want a real,
bounded audit instead of a generic opinion.

```text
Use this repository as the operating framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Task:
1. Evaluate the repository first so you do not overclaim what it does.
2. Read these files before auditing:
   - README.md
   - PUBLIC_PRODUCT_READINESS.md
   - METHODOLOGY.md
   - SCORING_EXPLAINED.md
   - REAL_CASES.md
3. Then evaluate this site by the repository methodology: {{TARGET_URL}}
4. Focus on:
   - technical SEO
   - semantics and intent
   - GEO and AI discoverability
   - factual consistency
   - AI-bot access
   - schema
   - answer-readiness
   - entity and trust surfaces
5. Prefer repository-native scripts and docs where relevant.
6. Separate:
   - verified findings
   - heuristic findings
   - assumptions
7. Produce:
   - executive summary
   - score breakdown
   - strongest positives
   - top weaknesses
   - prioritized action plan by impact, effort, confidence
   - quick wins for 7 days
   - deeper fixes for 30 days
   - what is verified vs heuristic
   - what requires human approval before implementation
8. If script output conflicts with visible site reality, explain the likely cause.
9. If you make assumptions, state them explicitly.
10. End with:
   - a client-ready report
   - an operator backlog
```
