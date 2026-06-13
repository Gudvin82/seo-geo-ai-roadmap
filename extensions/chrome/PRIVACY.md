# Privacy Notes

The extension reads the active tab URL only when the operator clicks **Audit
current tab**.

It sends that URL to the configured self-hosted backend endpoint:

- `POST /api/v1/scanner/url-audit`

The extension does not ship analytics, ad trackers, or third-party telemetry.

Operators are responsible for pointing the extension at an environment they
control and for disclosing any downstream logging or retention in their own
deployment.
