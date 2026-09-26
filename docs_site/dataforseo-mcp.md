# DataForSEO and MCP (v6.15.0)

v6.15.0 adds four optional, read-only Google search data flows using the
operator's DataForSEO account: keyword metrics, a one-query live SERP snapshot,
domain competitor candidates, and an aggregate backlink summary. These are
provider-derived observations, not Yandex data, ranking guarantees, or proof of
causality.

Live calls are billable. Configure `DATAFORSEO_LOGIN` and
`DATAFORSEO_PASSWORD` on the backend, opt into paid calls in the integration
form, and review the provider's current [pricing](https://dataforseo.com/pricing).
The local daily budget is best-effort, not a provider-enforced cap. The app does
not automatically retry billable POST requests; uncertain billing outcomes
block additional calls on that connection for the UTC day pending operator
review.

The authenticated `POST /api/v1/mcp` endpoint provides read-only,
project-scoped tools for saved project context, the latest unified report,
evidence, connector snapshots, and AI visibility history. MCP tools never start
provider requests.

Implementation and operator setup: [English](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/docs/en/dataforseo-integration.md) · [Русский](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/docs/ru/dataforseo-integration.md).
