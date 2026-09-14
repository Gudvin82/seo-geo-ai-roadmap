# Scoring Calibration

The GEO score is an explainable readiness score for prioritization. It is not
a prediction of rankings, AI citations, traffic, leads, or revenue.

Use `scripts/scoring_calibration.py` only with consented, dated evidence:

```csv
case_id,heuristic_score,observed_outcome,outcome_definition,observed_at,observation_window_days,evidence_reference
site-001,62,14,organic_click_change_percent,2026-09-01,28,docs/en/proof-pack-site-001.md
```

Start from [the template](../../examples/scoring-calibration-template.csv):

```bash
python scripts/scoring_calibration.py examples/scoring-calibration-template.csv
```

The tool reports `insufficient_evidence` unless it has at least 30 independent
cases, one comparable outcome definition, dated observations, and a proof
reference per record. A reported correlation is a calibration signal only; it
does not prove causation. Publish negative and null findings with positive
ones, retain raw provider exports where consent permits, and segment results
by market or site type before changing score weights.
