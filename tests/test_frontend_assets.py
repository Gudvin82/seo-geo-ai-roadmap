from pathlib import Path


def test_frontend_shell_exists() -> None:
    frontend_root = Path("app/frontend")
    for file_name in [
        "index.html",
        "styles.css",
        "app.js",
        "graph.html",
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
        Path("extensions/chrome/manifest.json"),
        Path("extensions/chrome/popup.html"),
        Path("extensions/chrome/popup.js"),
        Path("integrations/telegram/bot_stub.py"),
        Path("contracts/audit-run.schema.json"),
        Path("contracts/task-bundle.schema.json"),
        Path("contracts/graph-snapshot.schema.json"),
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
    ]
    for section in required_sections:
        assert section in html


def test_scanner_result_surface_exists() -> None:
    html = Path("app/frontend/scanner.html").read_text(encoding="utf-8")
    assert "One-Click Audit Result" in html
    assert "scanner-result-summary" in html
