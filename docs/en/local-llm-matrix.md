# Local LLM Matrix

This matrix is a practical starter for teams that want a self-hosted or
privacy-first AI layer behind the platform.

## Top 20 local-ready models to consider

| Model | Typical role | Strength | Notes |
|---|---|---|---|
| Llama 3.1 8B | general audit assistant | balanced cost/performance | strong starter for small nodes |
| Llama 3.1 70B | premium reasoning | better long-form analysis | needs serious GPU budget |
| Llama 3.3 70B | premium reasoning | newer instruction tuning | useful for report drafting |
| Qwen 2.5 7B | compact bilingual work | EN/RU flexibility | good for utility flows |
| Qwen 2.5 14B | content and audit support | strong multilingual quality | good mid-tier default |
| Qwen 2.5 32B | deeper analysis | better synthesis | heavier infra requirement |
| Qwen 2.5 72B | flagship local reasoning | broad capability | premium self-hosted tier |
| Mistral 7B | lightweight helper | fast response | good for triage jobs |
| Mixtral 8x7B | MoE analysis | strong structured output | reliable for audit plans |
| Mixtral 8x22B | premium MoE | better depth | more expensive to run |
| DeepSeek R1 Distill 8B | reasoning | efficient chain-style work | good test-bed model |
| DeepSeek R1 Distill 32B | reasoning | stronger problem solving | useful for benchmark lane |
| Phi-4 | compact assistant | efficient on smaller hardware | good internal helper |
| Gemma 2 9B | utility generation | clean instruction following | practical draft model |
| Gemma 2 27B | richer output | better for long responses | moderate GPU need |
| Command R | retrieval-heavy operations | operator guidance | validate licensing before use |
| Command R+ | premium retrieval | long-context workflows | good for document QA |
| Yi 34B | long-form drafting | strong context handling | depends on your runtime support |
| Nous Hermes 2 | instruction roleplay | operator prompt workflows | good fallback model |
| Solar 10.7B | compact reasoning | good multilingual drafting | solid midweight option |

## Recommended deployment lanes

- Demo or small VPS lab: `llama3.1:8b`, `qwen2.5:7b`, `mistral:7b`
- Agency default lane: `qwen2.5:14b`, `mixtral`, `gemma2:27b`
- Premium local lane: `llama3.1:70b`, `qwen2.5:72b`, `deepseek-r1-distill:32b`

## What to benchmark

- factual consistency against your brand facts
- EN and RU output quality
- structured report formatting stability
- response time under concurrent operator load
- cost per audit or per report batch

See also [provider-benchmarks.md](./provider-benchmarks.md) and
[provider-matrix.md](./provider-matrix.md).
