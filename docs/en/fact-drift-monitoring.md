# Fact Drift Monitoring

## First implementation in `v3.3.0`

The repository now includes a first practical drift detector that compares text
across multiple surfaces and flags strong inconsistencies.

## Recommended surfaces

- website pages
- schema blocks
- `llms.txt` or `ai.txt`
- provider or AI-generated answer samples

## What is detectable now

- conflicting locations
- conflicting support availability windows
- obvious contradictions in canonical brand facts

## What remains manual

- nuanced legal wording
- subtle offer or pricing differences
- citation-quality review in live LLM outputs

## False-positive risk

Heuristic matching may overflag summary pages, archived text, or market-specific
variants. Treat drift findings as review cues, not automated truth.
