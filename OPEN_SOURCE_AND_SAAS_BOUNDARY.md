# Open-Source vs SaaS Boundary

## What remains open-source

The repository methodology remains fully visible and reusable:

- docs
- checklists
- prompts
- templates
- scripts
- examples
- docs-site distribution

## What the app layer adds

`v2.2.0` adds an operator-ready product foundation:

- authentication
- workspaces and projects
- structured audit runs
- evidence storage
- EN/RU report generation
- provider configuration
- self-hosted deployment foundation
- expiring auth tokens and stronger password handling
- migrations, demo seed data, and observability basics
- workspace roles, invites, audit logs, and a canonical audit API
- local LLM support for Ollama, LocalAI, and vLLM-style endpoints

## Explicit platform promise

This platform is:

- free
- transparent
- self-hosted first
- compatible with your own cloud AI providers or local LLM runtimes
- exportable by design

## How self-hosting works

You can self-host the app layer with:

- local SQLite backend
- Docker Compose
- PostgreSQL-backed container stack

The repo is intentionally designed so self-hosting does not require a future
managed SaaS plan.

## What a future managed SaaS may add later

- billing
- managed team access
- stronger tenancy
- hosted analytics
- job scheduling at scale
- managed reliability and support

## Not implemented yet in v2.0.0

- billing and payments
- enterprise SSO
- advanced permissions matrix
- usage metering
- analytics warehouse
- production SLA

The goal is trust: document the boundary clearly rather than pretend these
features already exist.
