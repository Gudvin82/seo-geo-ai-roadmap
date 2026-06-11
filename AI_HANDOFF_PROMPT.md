# AI Handoff Prompt

Use this prompt when you want another AI to take the repository and execute the
setup or audit flow end to end.

```text
You are taking over a free and transparent self-hosted SEO, GEO, and AI discoverability platform.

Repository:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Your job:
1. Read README.md and AGENTS.md first.
2. Deploy the stack locally or self-hosted.
3. Copy .env.example to .env and fill only the minimum required values.
4. Run make up
5. Run make migrate
6. Run make seed if demo data is useful
7. Run make verify-demo
8. Run make agent-self-check
9. If the task is for a real website, create a workspace and project, connect providers, and run a canonical audit job.
10. Return:
   - URLs
   - credentials if demo was used
   - what was verified
   - what is still missing
   - whether the result is demo-ready or production-like self-hosted ready

Rules:
- Do not claim done without verification.
- If you changed user-facing scope, confirm EN and RU layers are aligned.
- If you changed code, run tests and lint checks.
- Prefer the repository’s built-in workflows instead of inventing your own.
```
