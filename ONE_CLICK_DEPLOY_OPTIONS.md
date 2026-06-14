# One-Click Deploy Options

This file collects the easiest deployment paths for teams that want results
quickly.

These are not magical "one vendor button" guarantees.
They are the fastest practical routes already supported by the repository
structure.

## Fastest local proof

Use this if you want the shortest path to a working demo:

1. `cp .env.example .env`
1. `make turnkey-demo`
1. open `http://localhost:3000`

Best for:

- proving the repo works
- showing the app to a client or teammate
- validating AI-agent handoff

## Docker VPS

Use this if you want the most direct self-hosted production-like route:

1. provision a Linux VPS
1. install Docker and Docker Compose
1. clone the repo
1. configure `.env`
1. run `docker compose up --build -d`
1. place it behind Caddy, Nginx, or Traefik

Best for:

- agencies
- consultants
- founders
- teams who want full control

## Coolify

Use this if you want a simpler self-hosted PaaS experience on your own server:

1. install Coolify on your server
1. connect the GitHub repo
1. create services for frontend, backend, and PostgreSQL
1. map the same environment variables from `.env.example`
1. run migrations before serving traffic

Best for:

- teams that want easier app lifecycle management
- users who still want self-hosted ownership

## Railway

Use this if you want a fast managed deployment flow:

1. connect the repo to Railway
1. split backend and frontend services
1. attach PostgreSQL
1. set environment variables
1. expose frontend and backend routes
1. run migrations during release

Best for:

- fast proof-of-concept
- internal deployment
- teams comfortable with a managed runtime

## Render

Use this if you want a similar managed path with clear service separation:

1. connect the repo to Render
1. create a web service for backend
1. create a static or web service for frontend
1. attach PostgreSQL
1. set environment variables and build commands
1. run migrations before first public traffic

Best for:

- low-friction proof
- smaller production rollouts
- teams who want a simpler hosted ops layer

## Kubernetes pack

Use this if you already operate managed Kubernetes:

- DigitalOcean Kubernetes
- GKE
- EKS

The repo already includes starter manifests under `infra/k8s/`.

Best for:

- teams with existing cluster operations
- multi-service or compliance-minded deployments

## Which option should you choose

- fastest demo: `make turnkey-demo`
- fastest self-hosted server: Docker VPS
- easiest self-hosted panel: Coolify
- fastest managed proof: Railway or Render
- existing enterprise infra: Kubernetes pack

## Minimum launch checklist

1. confirm `.env` secrets
1. run migrations
1. verify frontend
1. verify API docs
1. verify login
1. verify one audit run
1. verify one export
1. verify scanner intake if you expose it publicly

## Important boundary

All these options support:

- self-hosted deployment
- product foundation deployment
- scanner or audit service deployment under your own control

They do not turn the repo into:

- maintainer-operated hosted SaaS
- automatic enterprise support contract
- zero-review public multi-tenant service by default
