# Client Delivery

`v3.1.0` adds a stronger delivery layer for agencies, in-house teams, and
founders.

## Delivery pack audiences

- agency
- in_house
- founder

## One-click deliverables

- audit export
- patch pack
- client delivery pack
- llms.txt improvement suggestions
- AI visibility report starter
- reusable operator-ready JSON payloads

## Current API flow

- `GET /api/v1/exports/project-package`
- `POST /api/v1/exports/project-package/import`
- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/deliverables/client-pack`

## What a delivery pack is meant to include

- delivery summary
- report pack summary
- artifact pack summary
- latest SoV summary when available
- audience-aware one-click deliverables for agency, in-house, or founder use

## White-label expectations

Client delivery may use workspace branding fields for title, subtitle, footer,
and logo placeholder. Operators should still review every client-facing output
before sending it.
