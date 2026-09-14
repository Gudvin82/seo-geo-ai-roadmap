# Product Capability Matrix

Generated from the canonical runtime registry. A maturity label is an evidence-bound operational status, not a marketing claim.

## Levels

- `production_ready`: Implemented, tested in the self-hosted runtime, and safe to operate within documented limits.
- `connected`: Uses the running application runtime but still depends on operator configuration or an external service.
- `foundation`: Contracts and controlled paths exist; operator-owned end-to-end proof is still required.
- `stub`: Shape-only starter payload or scaffold. It is not live data or a production connector.

## Surfaces

| Surface | Capability | Status | Evidence | Boundary |
| --- | --- | --- | --- | --- |
| cli | geo audit / score / roadmap / monitor CLI | `connected` | CLI smoke test plus API-backed endpoint tests | Requires a running self-hosted app and the appropriate scanner session or API token. |
| integration | Alice AI Visibility in Yandex Search | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Backlink and Authority Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Chrome UX Report | `foundation` | Runtime connector and credential-gated path exist. | Do not claim a connected or production-ready integration without an operator-owned E2E proof record. |
| integration | Competitor Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Dzen Distribution Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Google Ads | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Google Analytics 4 | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Google Business Profile | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Google Merchant Center | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Google Search Console | `foundation` | Runtime connector and credential-gated path exist. | Do not claim a connected or production-ready integration without an operator-owned E2E proof record. |
| integration | IndexNow | `foundation` | Runtime connector and credential-gated path exist. | Do not claim a connected or production-ready integration without an operator-owned E2E proof record. |
| integration | Instagram or Facebook Organic | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Keyword Research Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | LinkedIn Ads | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Meta Ads | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Rank Tracking and SERP Visibility | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Reddit Mentions | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | RuTube Analytics | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Telegram Ads or Channel Analytics | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Telegram Channel Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Threads Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | TikTok Organic | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | VK Ads | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | VK Organic Community Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | X Ads | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | X Organic Intelligence | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Yandex Business | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Yandex Direct | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Yandex Metrica | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Yandex Neuro and AI Readiness | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| integration | Yandex Webmaster | `foundation` | Runtime connector and credential-gated path exist. | Do not claim a connected or production-ready integration without an operator-owned E2E proof record. |
| integration | YouTube Analytics | `stub` | Starter payload or operator-guided import path is shipped. | No live provider data is returned by this repository without a future connector implementation. |
| methodology | Readiness-score calibration | `foundation` | dated consented-data calibration utility and validation tests | No validated external benchmark exists until an adequate independent dataset is supplied. |
| runtime | AI visibility history | `foundation` | provider evidence snapshot contracts and history storage | Provider-derived observations must be collected with an operator-authorized provider path. |
| runtime | Canonical Finding/Evidence model | `production_ready` | GEO runtime, report, task, graph, and API integration tests | Evidence types preserve provenance; heuristic evidence is not provider verification. |
| runtime | Self-hosted URL scanner | `production_ready` | scanner job tests and authenticated result access controls | A self-hosted operator owns deployment, rate limits, and target authorization. |
| runtime | Unified GEO Intelligence Report | `production_ready` | project-audit and scanner adapter report tests | The report explains readiness and evidence; it does not guarantee rankings or AI citations. |
