# Start Here For AI

If a user says:

- "deploy this for me"
- "set this up under key"
- "use this as the base for my SEO / GEO / AI service"
- "adapt this for my own site or client sites"

start here.

## What this repository is

This is a free, transparent, open-source, self-hosted platform and methodology
for:

- discoverability audits
- SEO + GEO + AI operator workflows
- brand facts and factual consistency management
- bilingual reporting and artifact delivery

## For AI agents: deploy this project from scratch

If a user asks you to deploy this project:

1. run `git clone ...`
2. run `cd seo-geo-ai-roadmap`
3. run `cp .env.example .env` and help the user fill required keys
4. run `make up`
5. run `make migrate`
6. run `make seed` if demo data is needed
7. output `http://localhost:3000` and the demo credentials

## If the user wants a ready-made prompt instead of writing one

Use the built-in task pack generator:

- `python scripts/agent_handoff_pack.py --task deploy-demo --language en`
- `python scripts/agent_handoff_pack.py --task audit-site --language en --target-url https://example.com`
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language en`

## Ideal path

1. Read [README.md](./README.md)
2. Read [AGENTS.md](./AGENTS.md)
3. Run `make turnkey-demo`
4. Run `make verify-demo`
5. Run `make agent-self-check`
6. Create a workspace
7. Create a project
8. Fill brand facts
9. Connect providers
10. Run one audit and one AI SoV check

## Expected outputs

- frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- demo user: `demo@example.com`
- demo password: `DemoPlatform123`

## If the user wants a client-ready setup

1. Use [CLIENT_SETUP_PLAYBOOK.md](./CLIENT_SETUP_PLAYBOOK.md)
2. Create one workspace per client
3. Create one project per website
4. Fill brand facts before serious audits
5. Export reports and artifacts for delivery

## If the user wants full takeover

Use [AI_HANDOFF_PROMPT.md](./AI_HANDOFF_PROMPT.md) as the operating contract and
report clearly what was verified, what was heuristic, and what still needs human
review.

If the user wants to turn the repo into a reusable scanner, read
[ARCHITECTURE_NOTE.md](./ARCHITECTURE_NOTE.md) before proposing a public intake
surface.
