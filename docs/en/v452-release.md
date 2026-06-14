# v4.5.2 Release Summary

`v4.5.2` is the packaging and product-foundation patch on top of `v4.5.0`.

## What changed

- Added 10 more hosted or online providers:
  Hugging Face, Novita, Nebius, Zhipu, Moonshot, DashScope, Qianfan,
  Friendli, Inference.net, and a generic OpenAI-compatible gateway
- Added 10 more local or self-hosted runtimes:
  LiteLLM, Llamafile, GPT4All, AnythingLLM, Xinference, LlamaSwap, Exo,
  FastChat, H2O.ai h2oGPT, and MLX-LM
- Added `yandex_direct` as a first-class production-guided integration
- Added a service-foundation API surface for teams building a branded scanner
  or audit service on top of the repo
- Updated active app and contract versions to `v4.5.2`

## Why this matters

- The provider story is now much closer to "bring the AI you already use"
- RU-market operators now have a clearer Yandex stack:
  Webmaster, Metrica, and Direct
- The repo is stronger as a product foundation, not only a methodology layer
- AI agents now have a machine-readable path for service-builder decisions

## Product-foundation interpretation

This patch does not claim that the repository is a maintainer-operated SaaS.
What it does claim:

- you can self-host the platform
- you can connect a wider provider matrix
- you can use a real scanner and reporting foundation
- you can turn it into your own branded service with explicit service-builder
  guidance for deployment, SSO planning, billing planning, and public intake

## Recommended next operator steps

1. Pick one hosted provider and one local fallback
2. Connect GSC or Yandex Webmaster first
3. Add GA4, Metrica, or Yandex Direct as the outcome layer
4. Use service-builder mode if the target is a client-facing branded scanner
