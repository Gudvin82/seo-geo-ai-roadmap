# Case Study: auditguard.ru and sitepravo.ru — AI crawler access, public before / after, and bounded score interpretation

Date: 2026-06-14
Methodology source: <https://github.com/Gudvin82/seo-geo-ai-roadmap>

## Why these two sites matter

These two sites show a useful pattern:

- `auditguard.ru` shows a measurable score and findings improvement
- `sitepravo.ru` shows a real AI discoverability improvement even when the product score barely moves

That distinction matters. Not every real discoverability gain should be forced
into a vanity metric.

## Current public verification

Publicly verifiable now:

- both sites expose public `robots.txt`
- both sites explicitly allow the target AI crawler set including:
  - `GPTBot`
  - `ChatGPT-User`
  - `PerplexityBot`
  - `ClaudeBot`
  - `Google-Extended`
  - `Applebot-Extended`
  - `YandexAdditional`
  - plus additional commercial or research crawlers such as `Amazonbot`, `Diffbot`, and `cohere-ai`
- `auditguard.ru` also exposes a detailed public `llms.txt`
- `sitepravo.ru` exposes a detailed public `llms.txt`

Important nuance:

- current public files prove the after-state
- the before-state is an implementation record from the rollout process

## auditguard.ru

### Before

- quality `llms.txt` and `ai.txt` already existed
- only `6/14` key AI bots had explicit allow rules in rollout records
- several meaningful bots were still `unspecified`
- a detector also produced false-positive “leak” findings around the public AI-facing files

### After

- all `14/14` target AI bots became explicitly allowed in rollout records
- the false-positive leak interpretation was removed
- the current public `robots.txt` reflects the stronger AI crawler policy

### Bounded before / after

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Overall score | 92 | 94 | +2 |
| Total findings | 13 | 11 | -2 |
| `robots.txt`: explicit AI-bot allow coverage | 6/14 | 14/14 | +8 bots |

### Interpretation

This is a good example of a real GEO-layer improvement that is not just
content-deep:

- the site already had strong trust and public-product framing
- the delta came from clearer crawler policy and cleaner interpretation
- public AI discoverability became more explicit and less ambiguous

## sitepravo.ru

### Before

- for this legal-first surface, the GEO block was not strongly reflected in the product score
- rollout records still showed only `6/14` key AI bots as explicitly allowed

### After

- explicit AI crawler coverage reached `14/14` in rollout records
- current public `robots.txt` confirms clear allows for the target AI set
- total findings decreased by one in the bounded rollout record

### Bounded before / after

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Overall score | 88 | 88 | 0 |
| Total findings | 15 | 14 | -1 |
| `robots.txt`: explicit AI-bot allow coverage | 6/14 | 14/14 | +8 bots |

### Interpretation

This is the more subtle case:

- the real AI discoverability layer improved
- the visible top-line score did not change
- this is not a failure; it shows that a scoring model must not be confused with the whole system reality

## Cross-case conclusion

Together these two sites show the same practical lesson:

- explicit AI crawler policy matters
- `robots.txt` ambiguity can be a real operational gap
- public AI-facing files should not be mislabeled as leaks
- some improvements will raise the product score directly
- some improvements will strengthen real discoverability before the score catches up

## Public URLs used in this case

- <https://auditguard.ru/robots.txt>
- <https://auditguard.ru/llms.txt>
- <https://sitepravo.ru/robots.txt>
- <https://sitepravo.ru/llms.txt>
