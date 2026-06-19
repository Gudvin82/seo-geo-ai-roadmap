# AI Task Packs

Use this file when you want an AI coding agent to do real work instead of
guessing what prompt might help.

These task packs are intentionally explicit, approval-first, and aligned with
what the repository actually supports today.

## Pack 1. Audit a website by the repo methodology

Best when:

- you want a bounded SEO + GEO + AI audit
- you need a client-ready report
- you want the AI to use repo scripts instead of inventing a new framework

Read first:

1. [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
2. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
3. [REAL_CASES.md](./REAL_CASES.md)

Prompt:

```text
Use this repository as the operating framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Task:
1. Evaluate the repository first so you do not overclaim what it does.
2. Audit this site by the repository methodology: {{TARGET_URL}}
3. Use repo-native scripts, docs, and scoring logic where relevant.
4. Separate:
   - verified observations
   - heuristic findings
   - assumptions
5. Deliver:
   - executive summary
   - score breakdown
   - strongest positives
   - top weaknesses
   - prioritized actions by impact, effort, confidence
   - quick wins for 7 days
   - deeper fixes for 30 days
   - what should be implemented only after human approval
6. If a script result conflicts with visible site reality, explain the likely cause.
7. End with a client-safe report and an operator backlog.
```

## Pack 2. Deploy the platform locally or on a server

Best when:

- you want a self-hosted stack
- you want a demo or internal operator install
- you want the AI to stop at a safe, verifiable deployment

Read first:

1. [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
2. [ONE_CLICK_DEPLOY_OPTIONS.md](./ONE_CLICK_DEPLOY_OPTIONS.md)
3. [DEPLOYMENT.md](./DEPLOYMENT.md)

Prompt:

```text
Use this repository as the base:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Task:
1. Deploy the repository with the fastest safe self-hosted path.
2. Keep the public promise honest:
   - self-hosted
   - open-source
   - AI-agent-ready
   - foundation for a scanner or audit service
3. Set up:
   - app stack
   - login
   - workspace
   - one demo project
   - scanner intake
   - report export
4. Verify:
   - frontend loads
   - API docs load
   - demo login works
   - one audit path works
5. Return:
   - deployment URL
   - credentials
   - what is production-ready
   - what still requires operator setup
   - exact next steps
```

## Pack 3. Improve an existing site after audit approval

Best when:

- an audit already exists
- the user wants implementation planning or execution
- changes must remain controlled

Read first:

1. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
2. [docs/en/technical-seo-deep-playbook.md](./docs/en/technical-seo-deep-playbook.md)
3. [docs/en/geo-ai-operations-playbook.md](./docs/en/geo-ai-operations-playbook.md)

Prompt:

```text
Use this repository as the framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Task:
1. Review the existing audit findings for {{TARGET_URL}}.
2. Group work into:
   - quick wins
   - medium effort changes
   - strategic architecture work
3. Prioritize by impact, effort, confidence, and proof level.
4. Produce:
   - implementation backlog
   - page-level change plan
   - schema / facts / FAQ / technical fixes
   - approval gates before deployment
5. Do not silently publish risky changes.
6. If access is available, prepare patches or implementation-ready payloads after approval.
```

## Pack 4. Turn the repo into a client-facing service foundation

Best when:

- you want a branded scanner or audit service
- you need deployment plus operating boundaries
- you need honest SaaS positioning

Read first:

1. [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
2. [ONE_DAY_SERVICE_BLUEPRINT.md](./ONE_DAY_SERVICE_BLUEPRINT.md)
3. [BUILD_WITH_THIS_PLATFORM.md](./BUILD_WITH_THIS_PLATFORM.md)

Prompt:

```text
Use this repository as the base for a branded scanner or audit service.

Task:
1. Treat the repo as a self-hosted foundation, not a finished hosted SaaS.
2. Propose the safest branded setup for:
   - intake
   - audit workflow
   - reporting
   - task export
   - operator review
3. Configure one demo workspace and one demo project.
4. Show what needs extra work for:
   - public intake
   - abuse control
   - queue policy
   - notifications
   - tenant operations
5. Return:
   - architecture summary
   - deployment path
   - client-safe promise
   - missing layers for hosted-SaaS maturity
```

## Pack 5. Evaluate the repo honestly before a public post

Best when:

- you want to publish a post or launch note
- you want the AI to challenge overclaiming
- you want a reality check

Read first:

1. [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
2. [METHODOLOGY.md](./METHODOLOGY.md)
3. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)

Prompt:

```text
Review this repository as a skeptical but fair evaluator.

Task:
1. Separate what is:
   - production-ready today
   - strong but foundation-level
   - still starter or scaffold
2. Identify any wording in my public post that overclaims the repo.
3. Rewrite the post so it stays strong but fully honest.
4. Explain what an SEO specialist, developer, founder, and AI agent would each think after reading it.
5. End with:
   - safe public wording
   - risky wording to avoid
   - the next three improvements that would increase trust fastest
```
