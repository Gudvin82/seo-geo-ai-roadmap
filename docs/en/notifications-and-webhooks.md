# Notifications and Webhooks

`v2.3.0` introduces starter notification endpoints for webhook-style operator
flows.

## Current scope

- create endpoints per workspace
- scope endpoints to specific events
- send JSON payloads to Slack-style, Telegram-style, or generic webhooks

## Good first events

- `audit.run_requested`
- `sov.completed`
- `project.package_exported`

## Current limitations

- no durable retry queue yet
- no secret rotation UI yet
- no delivery dashboard yet

Use this layer for lightweight operator awareness, not for guaranteed incident
delivery.
