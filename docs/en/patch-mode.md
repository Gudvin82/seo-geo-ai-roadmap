# Patch Mode

Patch mode in `v3.1.0` moves the platform from "find issues" to "prepare
implementation work".

## Output types

- issue-ready backlog items
- developer-ready implementation briefs
- content briefs
- schema patch suggestions
- llms.txt and AI visibility suggestions
- client-safe patch pack artifacts

## Review stance

- outputs are explicit artifacts
- review mode is always visible
- CMS writeback is governed by `read_only`, `draft`, or
  `human_approved_publish`

## Current API flow

- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/cms/{connector_id}/patch-package`
