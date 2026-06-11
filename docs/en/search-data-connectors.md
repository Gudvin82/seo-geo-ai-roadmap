# Search Data Connectors

This repository ships starter connectors for teams that want to enrich audits
with Google Search Console or Yandex data later.

## Included starters

- `scripts/gsc_data_stub.py`
- `scripts/yandex_data_stub.py`

## Expected future data

- clicks
- impressions
- average position
- top queries
- top landing pages
- geo split or market split where available

## Recommended usage

1. Keep the core audit usable without any third-party API.
2. Add GSC and Yandex only after the base workflow is stable.
3. Store imported data as an explicit evidence layer, not as hidden scoring.
4. Let operators compare API evidence with AI SoV and brand-facts output.
