from pathlib import Path


def test_frontend_shell_exists() -> None:
    frontend_root = Path("app/frontend")
    for file_name in [
        "index.html",
        "styles.css",
        "app.js",
        "graph.html",
        "repo-understanding.html",
        "integration-health.html",
        "graph.js",
        "nginx.conf",
        "Dockerfile",
    ]:
        assert (frontend_root / file_name).exists(), (
            f"Missing frontend asset: {file_name}"
        )


def test_extension_and_contract_assets_exist() -> None:
    required_paths = [
        Path(".github/actions/ai-visibility-check/action.yml"),
        Path("examples/github-actions/ai-visibility-check.yml"),
        Path("extensions/vscode/package.json"),
        Path("extensions/vscode/src/extension.js"),
        Path("extensions/vscode/README.md"),
        Path("extensions/chrome/manifest.json"),
        Path("extensions/chrome/popup.html"),
        Path("extensions/chrome/popup.js"),
        Path("extensions/chrome/README.md"),
        Path("integrations/telegram/bot_stub.py"),
        Path("infra/k8s/backend-deployment.yaml"),
        Path("docs/en/telegram-bot-v410.md"),
        Path("docs/ru/telegram-bot-v410.md"),
        Path("contracts/audit-run.schema.json"),
        Path("contracts/task-bundle.schema.json"),
        Path("contracts/graph-snapshot.schema.json"),
        Path("contracts/project-blueprint.schema.json"),
        Path("contracts/integration-bundle.schema.json"),
        Path("contracts/site-shell.schema.json"),
        Path("contracts/admin-shell.schema.json"),
        Path("contracts/scanner-config.schema.json"),
        Path("contracts/dashboard-config.schema.json"),
        Path("contracts/tenant-setup.schema.json"),
        Path("contracts/operator-handoff.schema.json"),
        Path("BUILD_WITH_THIS_PLATFORM.md"),
        Path("BUILD_WITH_THIS_PLATFORM_RU.md"),
        Path("GENERATE_PROJECT_FROM_URL.md"),
        Path("GENERATE_PROJECT_FROM_URL_RU.md"),
        Path("docs_site/assets/screenshots/project-badge-v530.png"),
    ]
    for path in required_paths:
        assert path.exists(), f"Missing v4.0.0 asset: {path}"


def test_frontend_mentions_required_workflows() -> None:
    html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    required_sections = [
        "Workspaces",
        "Projects and sites",
        "Brand truth center",
        "Provider settings",
        "Executive dashboard",
        "Structured audit runs",
        "Reports and artifacts",
        "Graph Intelligence",
        "provider-health-center",
        "social-command-center",
        "saas-readiness-center",
        "integration-runtime-center",
        "ru-market-command-center",
    ]
    for section in required_sections:
        assert section in html


def test_scanner_result_surface_exists() -> None:
    html = Path("app/frontend/scanner.html").read_text(encoding="utf-8")
    assert "One-Click Audit Result" in html
    assert "scanner-result-summary" in html
