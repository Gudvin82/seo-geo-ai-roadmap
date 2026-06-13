# AI Handoff Prompt

Use this prompt when you want another AI to take the repository and execute the
setup or audit flow end to end.

If you want a task-specific version, generate it from the repo:

- `python scripts/agent_handoff_pack.py --task audit-site --language en --target-url https://example.com`
- `python scripts/agent_handoff_pack.py --task deploy-demo --language en`
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language en`

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

If the task is to deploy or operate a public scanner flow:
11. Open `app/frontend/scanner.html` and read `docs/en/public-scanner-v360.md`.
12. Call `GET /api/v1/scanner/config` and respect feature flags before exposing modes.
13. For `active` or `full` scan modes, require ownership verification by HTML file, meta tag, or DNS TXT before job submission.
14. Create a scan job with `POST /api/v1/scan-jobs`, then track it with `GET /api/v1/scan-jobs/{id}` and `GET /api/v1/scan-jobs/{id}/events`.
15. Return artifact links, notification behavior, and public-service limitations together with the scan result.

Rules:
- Do not claim done without verification.
- If you changed user-facing scope, confirm EN and RU layers are aligned.
- If you changed code, run tests and lint checks.
- Prefer the repository’s built-in workflows instead of inventing your own.
```
