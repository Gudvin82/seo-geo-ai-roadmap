# Privacy Notes

The extension sends operator-entered data to the configured self-hosted backend.

Possible requests include:

- `POST /api/v1/scanner/url-audit`
- `GET /api/v1/settings/executive-dashboard`
- `POST /api/v1/agent-mode/runs`

No third-party telemetry is bundled in this package. Any retention, logging, or
analytics is controlled by the backend you connect.
