# Search Data Connectors

`v3.1.0` upgrades search and analytics connectors from simple examples into a
starter operator layer with persisted connections, sync endpoints, explicit
evidence snapshots, and EN/RU documentation.

## Supported starter sources

- Google Search Console
- Google Analytics 4
- Yandex Webmaster
- Yandex Metrica

## Minimum useful setup

1. Create one integration per project.
2. Keep credentials in environment variables instead of inline secrets.
3. Store the external property ID, domain, or counter ID in the connection.
4. Sync explicitly and treat imported data as evidence, not as hidden scoring.

## What is imported

- clicks
- impressions
- CTR
- average position
- top pages
- top queries
- visit or engagement signals where relevant
- compact sync summary for operator review

## Credentials and scopes

- GSC: service account or delegated credentials managed outside the repo
- GA4: API credentials managed outside the repo
- Yandex Webmaster: operator-managed token flow outside the repo
- Yandex Metrica: operator-managed token flow outside the repo

This release intentionally keeps credential management transparent. The app
stores a reference to an environment variable, not the secret itself.

## Current API flow

1. `POST /api/v1/integrations`
2. `POST /api/v1/integrations/{id}/sync`
3. `GET /api/v1/integrations?project_id=...`

## Privacy notes

- imported snapshots may contain commercially sensitive performance data
- operators should keep environment variables and database backups protected
- imported evidence should be shared with clients only through reviewed outputs

## Current limitations

- `v3.1.0` ships starter-grade sync flows, not full OAuth automation
- imported metrics are structured for operator review, not direct billing logic
- source APIs still require project-specific validation before production use
