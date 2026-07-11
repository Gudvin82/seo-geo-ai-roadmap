# Scoring Calibration

Heuristic scores are useful for triage, not proof of business impact. Use
`scripts/scoring_calibration.py` with a consented CSV containing:

```csv
heuristic_score,observed_outcome
62,14
78,21
```

Keep the same outcome definition and observation window across records. Treat
fewer than 30 independent records as insufficient evidence, and publish
negative or null results beside positive ones.
