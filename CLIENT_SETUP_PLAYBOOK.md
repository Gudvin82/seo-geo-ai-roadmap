# Client Setup Playbook

Use this flow when the repository must become a real operator environment for a
client website.

## 1. Deploy the platform

1. `cp .env.example .env`
1. `make up`
1. `make migrate`
1. `make seed` if you want a demo baseline first

## 2. Create the client workspace

Set:

- client or brand name
- reporting language
- white-label report title
- white-label report subtitle

## 3. Create the client project

Set:

- website URL
- market
- language
- project type
- audit preset

## 4. Fill the truth center

Before a serious audit, define:

- brand facts
- approved claims
- forbidden claims
- numeric facts
- primary CTA

## 5. Connect providers

Choose one or more:

- OpenAI
- Anthropic / Claude
- Gemini
- Perplexity
- Ollama
- LocalAI
- vLLM-compatible endpoint

## 6. Run the first audit

Use:

- UI flow
- or `POST /api/v1/audit-runs/run`

## 7. Review outputs

Check:

- report summary
- artifacts
- audit logs
- gaps in facts, pages, or visibility structure

## 8. Turn outputs into work

Produce:

- implementation backlog
- page update tasks
- FAQ / schema / `llms.txt` drafts
- client-facing report pack

## 9. Verify before handoff

Run:

- `make verify-demo` if demo stack is active
- `make agent-self-check`
- test and lint commands if code was changed
