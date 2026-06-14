# Scripts Reference

## Overview

| Script | Purpose | Example |
|---|---|---|
| `generate_llms_txt.py` | Generate `llms.txt` from a sitemap | `python scripts/generate_llms_txt.py --sitemap-url https://example.com/sitemap.xml` |
| `check-llms-txt.py` | Validate `llms.txt` structure from file or URL | `python scripts/check-llms-txt.py --file examples/sample-llms.txt` |
| `check-robots-ai-bots.py` | Check AI/search bot access in `robots.txt` | `python scripts/check-robots-ai-bots.py --url https://example.com` |
| `check-ai-txt.py` | Validate `ai.txt` and review contradictions with `robots.txt` / `llms.txt` | `python scripts/check-ai-txt.py --url https://example.com` |
| `sitemap-checker.py` | Fetch a sitemap and count entries | `python scripts/sitemap-checker.py --url https://example.com/sitemap.xml` |
| `schema-validator.py` | Validate JSON schema files | `python scripts/schema-validator.py --file templates/schema/service-schema.json` |
| `schema-coverage-checker.py` | Audit JSON-LD schema coverage on a real page | `python scripts/schema-coverage-checker.py --url https://example.com --site-type service` |
| `faq-detector.py` | Detect FAQ and answer-ready patterns in page HTML | `python scripts/faq-detector.py --url https://example.com` |
| `open-graph-checker.py` | Check Open Graph and Twitter Card completeness | `python scripts/open-graph-checker.py --url https://example.com` |
| `ai_readability_audit.py` | Audit AI readability layers such as visible structure, schema, FAQ, and guidance files | `python scripts/ai_readability_audit.py --url https://example.com` |
| `citability_score.py` | Score heuristic citation readiness and list quick wins | `python scripts/citability_score.py --url https://example.com --site-type service` |
| `check_cdn_blocking.py` | Probe whether edge rules block major AI bots | `python scripts/check_cdn_blocking.py --url https://example.com` |
| `rag_chunk_audit.py` | Check whether content is segmented cleanly for RAG pipelines | `python scripts/rag_chunk_audit.py --url https://example.com/article` |
| `crux_field_data.py` | Fetch or validate CrUX field-data payloads | `python scripts/crux_field_data.py --url https://example.com` |
| `integration_verification_matrix.py` | Render the integration and CMS verification matrix | `python scripts/integration_verification_matrix.py --json` |
| `robots-sitemap-link-checker.py` | Verify robots.txt and sitemap linkage together | `python scripts/robots-sitemap-link-checker.py --url https://example.com` |
| `ai-share-of-voice-tracker.py` | Create AI Share of Voice tracking scaffolds | `python scripts/ai-share-of-voice-tracker.py "Example AI Agency" --queries "best GEO agency,ai visibility audit"` |
| `serp-intent-cluster-helper.py` | Group keywords by rough search intent | `python scripts/serp-intent-cluster-helper.py "best ai agency" "what is geo"` |
| `content-inventory-helper.py` | Create a markdown content inventory table from URLs | `python scripts/content-inventory-helper.py https://example.com/ https://example.com/faq` |
| `roi_calculator.py` | Estimate business ROI / ROMI for SEO and AI traffic | `python scripts/roi_calculator.py --traffic 5000 --conversion-rate 0.03 --lead-to-sale-rate 0.2 --average-check 1200 --margin-rate 0.45 --seo-cost 1500` |
| `content_freshness_checker.py` | Classify sitemap URLs as fresh, stale, or unknown | `python scripts/content_freshness_checker.py --sitemap-url https://example.com/sitemap.xml --days-stale 180 --output-file freshness.md` |
| `check_hallucinations.py` | Create a starter hallucination-checking report from brand facts and questions | `python scripts/check_hallucinations.py --brand-facts-file examples/brand-facts-example.md --questions-file examples/hallucination-questions-example.md --output-file hallucination-report.md` |
| `gsc_data_stub.py` | Emit a Google Search Console shaped starter payload | `python scripts/gsc_data_stub.py` |
| `yandex_data_stub.py` | Emit a Yandex shaped starter payload | `python scripts/yandex_data_stub.py` |
| `x_ads_stub.py` | Emit a starter X Ads payload | `python scripts/x_ads_stub.py` |
| `x_organic_stub.py` | Emit a starter X organic intelligence payload | `python scripts/x_organic_stub.py` |
| `threads_stub.py` | Emit a starter Threads payload | `python scripts/threads_stub.py` |
| `reddit_mentions_stub.py` | Emit a starter Reddit mentions payload | `python scripts/reddit_mentions_stub.py` |
| `tiktok_organic_stub.py` | Emit a starter TikTok organic payload | `python scripts/tiktok_organic_stub.py` |
| `provider_benchmark_stub.py` | Print a provider benchmark rubric scaffold | `python scripts/provider_benchmark_stub.py` |
| `fact_drift_checker.py` | Compare brand facts across surfaces and flag drift patterns | `python scripts/fact_drift_checker.py --surface website=./website.md --surface schema=./schema.md` |
| `scheduled_check_runner.py` | Print the execution plan for a recurring check | `python scripts/scheduled_check_runner.py --project-id 1 --check-type llms --frequency weekly --schedule-mode github_actions` |
| `geo_command_surface.py` | Route GEO/SEO/AI tasks to the right scripts, docs, and API routes | `python scripts/geo_command_surface.py audit --format json` |
| `bootstrap_self_hosted.py` | Print the bootstrap plan for demo or production-like self-hosted setup | `python scripts/bootstrap_self_hosted.py --mode demo --format markdown` |

## `generate_llms_txt.py`

- Purpose: generate a draft `llms.txt` from a sitemap URL or local sitemap file.
- Input parameters:
  - `--sitemap-url`
  - `--sitemap-file`
  - `--output-file`
- Example command:

```bash
python scripts/generate_llms_txt.py \
  --sitemap-url https://example.com/sitemap.xml \
  --output-file ./llms.txt
```

- Expected output:
  - source used
  - number of processed / included / skipped URLs
  - destination output file
  - warnings for URLs with generic descriptions
- Common failure cases:
  - missing `--sitemap-url` and `--sitemap-file`
  - unreadable local file
  - network failure
  - invalid XML
  - zero URLs parsed
- Notes / limitations:
  - path descriptions are inferred by heuristics
  - archive-like paths such as `/tag/` and `/author/` are skipped by default

## `check-llms-txt.py`

- Purpose: validate whether `llms.txt` contains basic expected sections.
- Input parameters:
  - `--url`
  - `--file`
- Example command:

```bash
python scripts/check-llms-txt.py --file examples/sample-llms.txt
```

- Expected output:
  - number of non-empty lines checked
  - `PASS` or `FAIL`
  - missing sections when validation fails
- Common failure cases:
  - file not found
  - URL fetch error
  - missing `faq` or `about` references
- Notes / limitations:
  - this is a lightweight structure check, not a semantic audit

## `check-robots-ai-bots.py`

- Purpose: inspect `robots.txt` and summarize access for major AI/search bots.
- Input parameters:
  - `--url`
- Example command:

```bash
python scripts/check-robots-ai-bots.py --url https://example.com
```

- Expected output:
  - robots URL used
  - markdown table with bot, status, and recommendation
- Common failure cases:
  - `robots.txt` missing or unreachable
  - malformed or incomplete robots rules
- Notes / limitations:
  - partial path rules still require manual review

## `sitemap-checker.py`

- Purpose: fetch a sitemap and count XML URL entries.
- Input parameters:
  - `--url`
- Example command:

```bash
python scripts/sitemap-checker.py --url https://example.com/sitemap.xml
```

- Expected output:
  - total URL count
- Common failure cases:
  - network error
  - invalid sitemap XML
- Notes / limitations:
  - does not validate sitemap quality, only accessibility and count

## `schema-validator.py`

- Purpose: verify that a JSON schema file can be parsed.
- Input parameters:
  - `--file`
- Example command:

```bash
python scripts/schema-validator.py --file templates/schema/service-schema.json
```

- Expected output:
  - `Valid JSON`
- Common failure cases:
  - file missing
  - invalid JSON syntax
- Notes / limitations:
  - validates JSON syntax, not external schema correctness

## `ai-share-of-voice-tracker.py`

- Purpose: create markdown or CSV scaffolds for manual AI Share of Voice tracking.
- Input parameters:
  - positional `brand`
  - `--queries`
  - `--format`
  - `--output`
- Example command:

```bash
python scripts/ai-share-of-voice-tracker.py \
  "Example AI Agency" \
  --queries "best GEO agency,ai visibility audit" \
  --format markdown
```

- Expected output:
  - markdown table or CSV rows for repeated tracking
- Common failure cases:
  - empty query list
  - missing `--output` for CSV mode
- Notes / limitations:
  - designed for manual or semi-manual collection

## `serp-intent-cluster-helper.py`

- Purpose: group keywords by rough intent labels.
- Input parameters:
  - positional keywords
- Example command:

```bash
python scripts/serp-intent-cluster-helper.py \
  "best ai agency" \
  "what is geo" \
  "ai visibility price"
```

- Expected output:
  - markdown table with intent clusters
- Common failure cases:
  - no keywords provided
- Notes / limitations:
  - heuristic only; always review with SERP context

## `content-inventory-helper.py`

- Purpose: create a markdown inventory table from a URL list.
- Input parameters:
  - positional URLs
- Example command:

```bash
python scripts/content-inventory-helper.py \
  https://example.com/ \
  https://example.com/faq \
  https://example.com/services/ai-visibility
```

- Expected output:
  - markdown table ready for content inventory work
- Common failure cases:
  - no URLs provided
- Notes / limitations:
  - fills structure only; humans still need to classify intent and ownership

## `roi_calculator.py`

- Purpose: estimate visits, leads, sales, revenue, gross margin, and ROI / ROMI.
- Input parameters:
  - `--traffic`
  - `--conversion-rate`
  - `--lead-to-sale-rate`
  - `--average-check`
  - `--margin-rate`
  - `--seo-cost`
  - `--ai-referred-share`
  - `--period`
- Example command:

```bash
python scripts/roi_calculator.py \
  --traffic 5000 \
  --conversion-rate 0.03 \
  --lead-to-sale-rate 0.2 \
  --average-check 1200 \
  --margin-rate 0.45 \
  --seo-cost 1500 \
  --ai-referred-share 0.1 \
  --period monthly
```

- Expected output:
  - visits
  - AI-referred visits
  - leads
  - sales
  - revenue
  - gross margin
  - cost
  - estimated ROI / ROMI
- Common failure cases:
  - missing required numeric inputs
  - unrealistic rate values supplied by the user
- Notes / limitations:
  - this is a simple planning tool, not an attribution model
  - pair it with [templates/roi-model-template.md](../templates/roi-model-template.md)
    for documented assumptions

## `content_freshness_checker.py`

- Purpose: classify sitemap URLs as fresh, stale, or unknown freshness.
- Input parameters:
  - `--sitemap-url`
  - `--sitemap-file`
  - `--days-stale`
  - `--output-file`
  - `--format markdown|csv|json`
- Example command:

```bash
python scripts/content_freshness_checker.py \
  --sitemap-url https://example.com/sitemap.xml \
  --days-stale 180 \
  --output-file ./freshness-report.md \
  --format markdown
```

- Expected output:
  - URL
  - detected `lastmod`
  - status
  - recommendation
- Common failure cases:
  - unreadable sitemap
  - invalid XML
  - zero URLs parsed
  - CSV mode without `--output-file`
- Notes / limitations:
  - depends on sitemap `lastmod` quality
  - see [examples/content-freshness-report-example.md](../examples/content-freshness-report-example.md)

## `check_hallucinations.py`

- Purpose: create a starter hallucination-checking report from canonical brand
  facts and a question set.
- Input parameters:
  - `--brand-facts-file`
  - `--questions-file`
  - `--output-file`
  - `--format markdown|csv|json`
  - optional `--provider`
  - optional `--model`
- Example command:

```bash
python scripts/check_hallucinations.py \
  --brand-facts-file examples/brand-facts-example.md \
  --questions-file examples/hallucination-questions-example.md \
  --output-file ./hallucination-report.md \
  --format markdown
```

- Expected output:
  - question
  - expected facts
  - answer placeholder
  - discrepancy status
  - next action
- Common failure cases:
  - missing inputs
  - no questions parsed
  - unreadable JSON or markdown files
- Notes / limitations:
  - provider integration is optional and intentionally lightweight
  - works well with [templates/brand-facts-template.md](../templates/brand-facts-template.md)
