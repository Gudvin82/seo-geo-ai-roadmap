# DataForSEO Classic SEO Integration

The app can use an operator-owned DataForSEO account for four bounded,
read-only research flows:

- `keyword_research`: Google Ads search volume and competition for supplied keywords
- `rank_tracking`: a Google organic live SERP snapshot for one configured query
- `competitor_intelligence`: domain competitors for the project's market
- `backlink_intelligence`: a domain backlink summary

DataForSEO charges for live API requests. This connector is optional and is
disabled until the operator explicitly enables billable requests on each
integration connection. The app does not save the provider login or password.

This initial implementation uses Google's search-volume, organic SERP, domain
competitor, and backlink-summary endpoints; it does not provide Yandex keyword
volume or Yandex SERP data. See the provider references for [search volume](https://docs.dataforseo.com/v3/keywords_data-google_ads-search_volume-live/),
[Google organic SERP](https://docs.dataforseo.com/v3/serp-se-type-live-advanced/),
[domain competitors](https://docs.dataforseo.com/v3/dataforseo_labs-google-competitors_domain-live/),
[backlink summary](https://docs.dataforseo.com/v3/backlinks-summary-live/),
and [pricing](https://dataforseo.com/pricing).

## Setup

Set these environment variables in the backend runtime:

```dotenv
DATAFORSEO_LOGIN=your-api-login
DATAFORSEO_PASSWORD=your-api-password
```

Create one integration connection per flow through the Integrations UI or
`POST /api/v1/integrations`.
Use the matching source type and set `credentials_env_var` to
`DATAFORSEO_LOGIN,DATAFORSEO_PASSWORD` as an operator-facing reference. Set the
project domain as `property_identifier` for competitor and backlink flows.

Every connection config must explicitly include:

```json
{
  "allow_billable_requests": true,
  "approved_daily_budget_usd": 2.0,
  "max_requests_per_day": 5,
  "cache_ttl_seconds": 21600,
  "location_name": "Russia",
  "language_code": "ru"
}
```

Flow-specific configuration:

- `keyword_research`: provide `keywords` (1 to 30 strings), or save `seed_keywords` in project research context.
- `rank_tracking`: provide `keyword`; `depth` is limited to 10 to 30 and requires an explicit location.
- `competitor_intelligence`: use the project domain as the connection property; `limit` is capped at 100.
- `backlink_intelligence`: use the project domain as the connection property.

The daily budget is a local best-effort guard per connection, not a hard cap
enforced by DataForSEO. The provider charges per request; its exact charge is
not guaranteed in advance, and parallel requests may race past the local guard.
Check the provider's current pricing and account balance before enabling calls.
The UI asks for explicit approval when creating the connection and again before
each manual paid sync. Automatic retries are disabled to avoid duplicate
billable POSTs. If a request's billing outcome is unknown after a transport
failure, further paid calls for that connection are blocked for the UTC day
until the operator checks the provider account.

## Evidence, cache, and history

Successful responses include provider, market, language, observed time, task
reference, actual reported cost, request count, cache TTL, and provenance. Rows
are wrapped in the canonical Finding/Evidence contract with
`provider-derived` evidence. The integration snapshot is persisted and a
compact evidence record is written for history. A fresh snapshot is served from
cache without another billable call.

Use the project pane's **Reusable research context** editor or the project
endpoints to save reusable context:

- `GET /api/v1/projects/{project_id}/research-context`
- `PUT /api/v1/projects/{project_id}/research-context`

The context stores competitors, goals, key pages, and seed keywords. The
project's existing market and language remain the source for those fields.

## MCP

The stateless Streamable HTTP MCP endpoint is `/api/v1/mcp`. Configure the MCP
client with the self-hosted app URL and an existing bearer access token. All
tools enforce project membership and read only saved records:

- `get_project_context`
- `get_latest_unified_report` (including findings, graph, and task bundle)
- `list_project_evidence`
- `list_connected_sources`
- `list_ai_visibility_history`

MCP tools never start a DataForSEO request and therefore cannot incur provider
charges. Use the authenticated integration sync API when an operator wants to
refresh a connector.

The endpoint currently advertises the `2025-03-26` handshake-era protocol. This
is a bounded compatibility surface, not a claim that every current MCP client
or newer protocol revision is supported. Check the [MCP transport version](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
supported by your client.

## Provider boundaries

DataForSEO's documented endpoints are paid and market-scoped. Keyword volume is
provider-estimated demand, rank tracking is a dated SERP observation, backlink
metrics are third-party index data, and competitor overlap is not proof of
business equivalence. These signals do not establish ranking causality or
guarantee AI citations.
