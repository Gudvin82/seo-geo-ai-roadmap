# Walkthrough

## The ideal first run

This is the shortest proof-first path through the project.

1. Read [README.md](./README.md)
2. Run `make turnkey-demo`
3. Open `http://localhost:3000`
4. Sign in with `demo@example.com / DemoPlatform123`
5. Open the overview pane
6. Select the demo workspace and project
7. Open reports and artifacts
8. Run a fresh audit
9. Run AI SoV
10. Export the project package

## What you should see

- a working login flow
- one workspace and one project
- a visible audit history
- a visible report and artifact layer
- prompt library and notification endpoints
- AI SoV history with transparent notes

## After the first visible result

1. Replace the demo site with a real project
2. Fill your own brand facts
3. Connect cloud or local providers
4. Run the first real audit
5. Turn the findings into a fix backlog
6. Re-run after changes and compare deltas

## Human path and AI path

- Human operator path: use this walkthrough plus [DEPLOYMENT.md](./DEPLOYMENT.md)
- AI agent path: use [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md) plus
  [AGENTS.md](./AGENTS.md)

## Proof assets

![Login and dashboard proof](./docs_site/assets/screenshots/app-login-dashboard-proof.png)
![Provider configuration proof](./docs_site/assets/screenshots/app-provider-proof.png)
![Audit run proof](./docs_site/assets/screenshots/app-audit-proof.png)
![Report and artifact proof](./docs_site/assets/screenshots/app-report-proof.png)
