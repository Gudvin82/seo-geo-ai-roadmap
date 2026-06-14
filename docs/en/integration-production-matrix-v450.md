# Integration Production Matrix v4.5.0

This is the shortest operational view of the integration layer.

## Current first-class integrations

| Integration | Layer | Contract status | Proof surface | Best next step |
| --- | --- | --- | --- | --- |
| GSC | search visibility | `production_guided` | env-aware verification matrix | connect service account and schedule recurring sync |
| GA4 | outcome and engagement | `production_guided` | env-aware verification matrix | validate imported baseline and use it in executive mode |
| Yandex Webmaster | RU search visibility | `production_guided` | env-aware verification matrix | connect token and keep it in the same compare loop as GSC |
| Yandex Metrica | RU analytics | `production_guided` | env-aware verification matrix | pair with Webmaster for RU diagnostics plus conversion context |
| CrUX | field data | `production_guided` | env-aware verification matrix | combine real-user CWV with synthetic checks and CI gating |
| WordPress | governed CMS | `production_guided` | CMS contract plus inventory flow | move from inventory to reviewed patch bundles |
| Webflow | governed CMS | `production_guided` | CMS contract plus export-first flow | keep publish behind review |
| Bitrix | governed CMS | `production_guided` | CMS contract plus mapping validation | validate field mapping before automation |
| Tilda | governed CMS | `production_guided` | CMS contract plus manual-apply flow | treat it as re-audit-backed delivery |

## What changed in v4.5.0

- the integration verification layer now reports required, present, and missing
  environment variables
- readiness can show `configured` based on live env state, not only static row
  metadata
- scanner, dashboard, and CI-oriented flows now align more clearly around the
  same proof surfaces

## Production interpretation

- `production_guided` means the repo contains the contract, workflow shape,
  verification path, and operator routing
- it does not mean the maintainers run a hosted managed service for you
- the intended model is self-hosted ownership with explicit credentials and
  review

## Best operator sequence

1. connect one search or analytics integration
2. verify environment readiness
3. run one manual import
4. review the imported baseline
5. promote it into scheduled checks or CI gating
6. compare deltas after fixes
