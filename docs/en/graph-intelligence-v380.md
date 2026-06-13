# Graph Intelligence v3.8.0

`v3.8.0` adds an explainable graph layer for discoverability operations.

This is not a generic code graph. It is a discoverability graph that helps an
operator, founder, client, or AI agent answer four practical questions:

1. what exists
2. why it matters
3. what it impacts
4. what to fix next

## Views

- Site structure graph: homepage, sections, money pages, hubs, case studies,
  and trust pages
- Discoverability surface graph: `robots.txt`, `sitemap.xml`, `llms.txt`,
  `ai.txt`, schema, FAQ, and social metadata
- Issue dependency graph: blockers, easy wins, and fix-pack sequencing
- Entity and trust graph: organization, services, authors, legal pages, and
  external corroboration

## Product surface

- UI: `app/frontend/graph.html`
- Logic: `app/frontend/graph.js`
- Export: JSON download from the graph page
- Command surface: `/geo graph`

## Why this helps commercially

- Sales calls become easier because the problem can be shown, not only
  described
- Client delivery improves because issue relationships are visible
- Founders can see where trust and proof are weak without reading long reports
- AI agents can explain the remediation path in human language

## Recommended flow

1. run `/geo audit`
2. run `/geo graph`
3. open the issue dependency view
4. export the graph JSON
5. attach it to the executive summary and fix pack

## Honest boundary

The graph is an explainability layer over the current platform. It is not
pretending to be an enterprise crawler or a full knowledge graph platform.
