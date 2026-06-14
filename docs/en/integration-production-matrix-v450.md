# Integration Production Matrix v4.5.x

This is the shortest operational view of the integration layer.

## Current first-class integrations

| Integration | Layer | Contract status | Proof surface | Best next step |
| --- | --- | --- | --- | --- |
| GSC | search visibility | `production_guided` | env-aware verification matrix | connect service account and schedule recurring sync |
| GA4 | outcome and engagement | `production_guided` | env-aware verification matrix | validate imported baseline and use it in executive mode |
| Google Ads | paid search demand | `production_guided` | env-aware verification matrix | connect credentials and compare brand/non-brand demand with GSC and GA4 |
| Yandex Webmaster | RU search visibility | `production_guided` | env-aware verification matrix | connect token and keep it in the same compare loop as GSC |
| Yandex Metrica | RU analytics | `production_guided` | env-aware verification matrix | pair with Webmaster for RU diagnostics plus conversion context |
| Yandex Direct | RU paid demand and landing alignment | `production_guided` | env-aware verification matrix | connect token and compare spend plus demand shifts with organic and AI visibility |
| CrUX | field data | `production_guided` | env-aware verification matrix | combine real-user CWV with synthetic checks and CI gating |
| IndexNow | fast indexation signal | `production_guided` | env-aware verification matrix | configure push path for fresh URLs |
| Google Business Profile | local trust and maps demand | `production_guided` | env-aware verification matrix | connect profile and review local actions |
| Yandex Business | RU local trust and maps demand | `production_guided` | env-aware verification matrix | connect profile and compare with RU local landing performance |
| Merchant Center | commerce feed health | `production_guided` | env-aware verification matrix | track approvals and product feed issues |
| Meta Ads | paid distribution | `distribution_guided` | env-aware verification matrix | use as amplification and remarketing context |
| VK Ads | RU paid distribution | `distribution_guided` | env-aware verification matrix | compare with RU search demand and conversions |
| Telegram ads or channel analytics | community distribution | `distribution_guided` | env-aware verification matrix | use for channel-demand validation |
| YouTube Analytics | media distribution | `distribution_guided` | env-aware verification matrix | compare video demand with branded search and site clicks |
| LinkedIn Ads | B2B paid distribution | `distribution_guided` | env-aware verification matrix | use for B2B demand amplification |
| Instagram or Facebook organic | social distribution | `distribution_guided` | env-aware verification matrix | use as a supporting distribution signal |
| WordPress | governed CMS | `production_guided` | CMS contract plus inventory flow | move from inventory to reviewed patch bundles |
| Webflow | governed CMS | `production_guided` | CMS contract plus export-first flow | keep publish behind review |
| Bitrix | governed CMS | `production_guided` | CMS contract plus mapping validation | validate field mapping before automation |
| Tilda | governed CMS | `production_guided` | CMS contract plus manual-apply flow | treat it as re-audit-backed delivery |

## What changed in v4.5.x

- the integration verification layer now reports required, present, and missing
  environment variables
- readiness can show `configured` based on live env state, not only static row
  metadata
- scanner, dashboard, and CI-oriented flows now align more clearly around the
  same proof surfaces
- the RU stack now explicitly includes Yandex Direct in addition to Webmaster
  and Metrica

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
