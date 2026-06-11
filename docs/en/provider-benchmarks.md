# Provider Benchmarks

Use this document when you want a repeatable benchmark lane for cloud and local
providers before rolling them into client work.

## Benchmark dimensions

- factual consistency against a known brand-facts file
- EN and RU answer quality
- structured output stability
- citation discipline
- latency
- cost
- operator edit burden after generation

## Practical benchmark flow

1. Pick one project and one approved brand-facts profile.
2. Run the same audit or prompt set through at least three providers.
3. Save the output, time-to-first-token, total duration, and human review notes.
4. Score each provider on a simple 1-5 rubric per category.
5. Re-run monthly or after a model upgrade.

## Starter tooling

- app provider configurations in the UI
- `scripts/provider_benchmark_stub.py`
- `docs/en/local-llm-matrix.md`
- `docs/en/provider-matrix.md`

## Recommendation

Do not choose a provider only by raw output quality. For self-hosted SEO, GEO,
and AI visibility work, the winning provider is usually the one that gives the
best blend of transparency, consistency, EN/RU coverage, speed, and review
burden.
