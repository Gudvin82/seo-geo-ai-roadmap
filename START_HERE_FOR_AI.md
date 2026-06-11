# Start Here For AI

If you are an AI agent and the user says something like:

- "deploy this for me"
- "set this up under key"
- "use this as the base for my SEO / GEO / AI service"
- "adapt this for my own site or client sites"

start here.

## What this repository is

This is a free, transparent, open-source, self-hosted platform and methodology
layer for:

- SEO audits
- GEO / AI visibility workflows
- report generation
- brand facts and truth-center management
- operator workflows for personal and client projects

## Fastest path

1. Read [README.md](./README.md)
1. Read [AGENTS.md](./AGENTS.md)
1. Clone the repository
1. Copy `.env.example` to `.env`
1. Run `make up`
1. Run `make migrate`
1. Run `make seed`
1. Run `make verify-demo`
1. Run `make agent-self-check`

## Expected outputs

- frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- demo user: `demo@example.com`
- demo password: `DemoPlatform123`

## If the user wants a client-ready setup

1. Use [CLIENT_SETUP_PLAYBOOK.md](./CLIENT_SETUP_PLAYBOOK.md)
1. Create a workspace per client
1. Create a project per website
1. Fill brand facts before running a serious audit
1. Connect cloud or local AI providers
1. Export reports and artifacts for review

## If the user wants you to take over

Use [AI_HANDOFF_PROMPT.md](./AI_HANDOFF_PROMPT.md) as the operating contract.
