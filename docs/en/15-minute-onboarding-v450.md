# 15-Minute Onboarding v4.5.0

This is the fastest low-friction path for a new operator or AI coding agent.

## Goal

In about 15 minutes you should be able to:

1. start the stack
2. open the app
3. create a workspace and project
4. connect one provider or stay in starter mode
5. run one audit or scanner job
6. open one report or machine-readable artifact

## Fast path

1. Clone the repo.
2. Copy `.env.example` to `.env`.
3. Run `make up`.
4. Run `make migrate`.
5. Run `make seed` if you want demo data.
6. Open the app and sign in.
7. Create one workspace and one project.
8. Add one provider config or stay in transparent starter mode.
9. Run one audit or use the scanner intake page.
10. Export one report or task bundle.

## If you are using an AI coding agent

Give it these files first:

- [START_HERE_FOR_AI.md](../../START_HERE_FOR_AI.md)
- [AGENTS.md](../../AGENTS.md)
- [DOCS_INDEX.md](../../DOCS_INDEX.md)

Then ask it to:

`Deploy this repository, create one project, run one audit, and return an executive summary plus the top fixes.`

## If you are building a client-facing scanner

Go next to:

- [ONE_DAY_SERVICE_BLUEPRINT.md](../../ONE_DAY_SERVICE_BLUEPRINT.md)
- [docs/en/integration-production-matrix-v450.md](./integration-production-matrix-v450.md)

## Proof that this path is stable

The root and backend test path for `v4.5.0` is green end to end.
