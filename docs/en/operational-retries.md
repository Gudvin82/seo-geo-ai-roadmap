# Operational Retries

## What retries exist in `v3.3.0`

The platform now exposes a starter retry model for:

- provider-backed commentary and AI SoV provider calls
- webhook and notification delivery
- governed CMS writeback preparation

The goal is not to fake durable job orchestration. The goal is to make failure
states visible, bounded, and reviewable.

## Retry policy

- max attempts: `3`
- initial delay: `0.5s`
- backoff model: bounded exponential (`0.5s`, `1.0s`, `2.0s`)
- terminal state: `dead`

## Status labels

- `queued`: accepted but not yet executed
- `retrying`: at least one attempt failed and the system is trying again
- `failed`: the current execution failed but has not yet reached the terminal state
- `dead`: retries are exhausted and a human must intervene
- `completed`: execution finished successfully
- `awaiting_human_approval`: a governed CMS package is ready but blocked from live publish

## Human intervention rules

Human review is required when:

- provider credentials are wrong or missing
- a webhook target is down or returns repeated errors
- no recent audit exists for a CMS writeback preparation flow
- a CMS connector is set to `read_only`

## Current boundary

`v3.3.0` does not claim a durable queue or exactly-once execution. Retries are
process-level safeguards plus auditability, not a full workflow engine.
