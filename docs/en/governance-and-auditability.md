# Governance and Auditability

## Current auditability boundary

The repository now logs or exposes events around:

- provider configuration changes
- audit requests, retries, starts, failures, and completions
- workspace role and invite lifecycle actions
- notification endpoint creation and delivery outcomes
- artifact downloads
- governed CMS writeback attempts

## Workspace governance assumption

`v3.3.0` assumes a trusted workspace administrator model. It is suitable for
self-hosted teams that need traceability, but it is not a finished enterprise
identity platform.

## Future boundary

Future work may add:

- SSO
- SCIM
- stronger approval chains
- durable policy engines

Those are direction signals, not implemented promises.
