# GEO Measurement Maturity

## Reliability ladder

| Metric class | Examples | Reliability | How to talk about it |
|---|---|---|---|
| Reliable operational metrics | crawlability, CWV, indexation, schema coverage | High | treat as decision-grade |
| Search performance metrics | rankings, impressions, CTR, landing-page clicks | Medium to high | explain seasonality and query-mix effects |
| GEO/AI proxy metrics | AI SoV, AI Citation Score, answer-surface coverage | Medium to low | treat as proxies, not guarantees |
| Experimental signals | prompt win-rate snapshots, one-off citation counts | Low | use as exploration, not executive truth |

## Metric-by-metric discipline

| Metric | Stability | Main limitation | Safer wording |
|---|---|---|---|
| Technical SEO issues | Stable | may not explain business impact alone | “observed issue” |
| Core Web Vitals | Stable enough | field data may lag | “reliable web-performance signal” |
| Schema coverage | Stable | coverage does not guarantee rich results or citations | “implementation signal” |
| AI SoV | Volatile | depends on prompts, vendor behavior, freshness | “directional visibility proxy” |
| AI Citation Score | Volatile | depends on answer surface and attribution style | “transparent proxy based on current monitored outputs” |

## Classification labels

Use these labels in reports:

- `observed_fact`: directly measured or visible
- `inferred_issue`: likely problem inferred from evidence
- `hypothesis`: plausible but not proven explanation
- `recommended_action`: next step with business rationale

## Anti-hype rule

Do not present AI visibility metrics as:

- guaranteed demand
- guaranteed lead lift
- stable benchmarking truth across all LLMs
- a replacement for analytics or CRM evidence
