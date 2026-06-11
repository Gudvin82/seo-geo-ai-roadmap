# Observability and Logging

## Built-in visibility

- `/healthz` for basic health
- `/readyz` for readiness
- `/metrics` for Prometheus-style counters

## What is counted

- auth requests
- audit runs
- provider calls
- provider failures
- report generation events

## Debugging basics

- review backend logs for request failures
- inspect artifact outputs for audit-specific issues
- inspect provider metadata in report artifacts for missing-key or timeout failures
