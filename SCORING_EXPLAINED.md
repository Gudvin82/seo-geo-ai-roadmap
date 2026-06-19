# Scoring Explained

This file exists so the repository cannot be accused of hiding its scoring
logic.

## What is scored today

The repository does not produce one magical universal SEO score.

It uses several bounded scores:

- `overall_score` for audit finding pressure
- `priority_score` for what to fix first
- `AI Citation Score` for current mention-plus-citation visibility in tracked AI results
- benchmark statuses for selected metrics such as LCP, CLS, INP, schema coverage, AI visibility readiness, and factual consistency
- heuristic scores such as citability or AI readability in scripts

## 1. Audit overall score

Code source:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Current logic:

- each finding has a severity
- severities map to penalty points
- high-priority findings add extra penalty through their priority score
- final score starts from `100` and subtracts the accumulated penalty

Current severity weights:

- `critical = 30`
- `high = 18`
- `medium = 9`
- `low = 4`

Current overall formula:

```text
overall_score = max(0, 100 - severity_penalty_sum - priority_penalty_sum)
priority_penalty_sum = sum(priority_score / 20)
```

Interpretation:

- this is an operator score, not a market truth score
- a lower score means the current backlog is heavy, not that the site is “dead”
- some real improvements may happen before this score moves materially

## 2. Priority score

Code source:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Inputs:

- severity
- impact
- effort
- confidence
- benchmark status

Current formula:

```text
raw = severity_points + (impact * 8) + (confidence * 6) - (effort * 4)
score = clamp(raw + benchmark_modifier, 0, 100)
```

Benchmark modifiers:

- `urgent_fix = +18`
- `worse_than_baseline = +8`
- `better_than_baseline = -8`
- `insufficient_data = 0`

Priority labels:

- `80-100 = fix_now`
- `60-79 = next_batch`
- `40-59 = planned`
- `0-39 = observe`

Interpretation:

- the score is designed to help sequencing
- it is transparent but intentionally simple
- it does not replace operator judgment for revenue, legal risk, or brand risk

## 3. AI Citation Score

Code source:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Current logic:

- each tracked result gets a `mentioned` boolean
- each tracked result gets a `citation_count`
- mention status contributes `70%`
- citation count contributes `30%`
- citation count is capped at `3`

Current formula:

```text
per_result = (mentioned ? 1.0 : 0.0) * 0.7 + (min(citation_count, 3) / 3) * 0.3
AI Citation Score = average(per_result) * 100
```

Interpretation:

- this is a directional visibility proxy
- it is useful for trend comparison
- it is not a promise of rankings, leads, or commercial success
- it is not stable across providers forever

## 4. Benchmark statuses

Code source:

- [app/backend/app/services/scoring.py](./app/backend/app/services/scoring.py)

Tracked benchmark families today:

- `lcp_seconds`
- `cls`
- `inp_ms`
- `schema_coverage`
- `ai_visibility_readiness`
- `factual_consistency`

Every benchmark becomes one of:

- `better_than_baseline`
- `worse_than_baseline`
- `urgent_fix`
- `insufficient_data`

Interpretation:

- benchmark status is easier to explain than raw numbers alone
- it should be read next to evidence, not as a stand-alone truth claim

## 5. Heuristic script scores

Some repo scripts intentionally return heuristic rather than fully deterministic
scores:

- `scripts/citability_score.py`
- `scripts/ai_readability_audit.py`
- `scripts/rag_chunk_audit.py`
- `scripts/schema-coverage-checker.py`
- `scripts/faq-detector.py`

These are useful because they surface real weak spots quickly.

They are limited because:

- HTML parsing is not the same as live model behavior
- client-side rendering can hide content from simple detectors
- provider behavior can change
- a page can be strong commercially while still looking weak to a bounded detector

## What to say publicly

Safe wording:

- “transparent, bounded scoring for prioritization”
- “directional proxy for AI citation readiness”
- “evidence-backed audit scoring”

Avoid:

- “proprietary AI score that predicts rankings”
- “guaranteed citation score”
- “one number that proves SEO success”

## How to use the scores correctly

Use scores to:

- compare before vs after
- sort backlog
- explain why something moved up or down
- create a repeatable operator rhythm

Do not use scores to:

- promise outcomes by themselves
- hide weak evidence
- collapse every business model into one number

## What v6 improves

`v6.0.0` does not pretend the scoring is perfect.

It makes the scoring:

- explicit
- code-linked
- explainable to humans
- easier for AI agents to summarize without overclaiming
