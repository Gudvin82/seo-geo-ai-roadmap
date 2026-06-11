# Shared Layer

The `shared/` directory is reserved for code and schemas that can be reused
across:

- repository scripts
- backend services
- future frontend clients
- future workers or SDK layers

In `v2.0.0`, the main reuse strategy is script-to-service wrapping from the
backend so the same methodology layer remains usable through CLI and API.
