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


def test_frontend_mentions_required_workflows() -> None:
    html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    required_sections = [
        "Workspaces",
        "Projects and sites",
        "Brand truth center",
        "Provider settings",
        "Structured audit runs",
        "Reports and artifacts",
        "Graph Intelligence",
    ]
    for section in required_sections:
        assert section in html
