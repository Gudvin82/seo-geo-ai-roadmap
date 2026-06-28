from pathlib import Path


def test_docs_foundation_assets_exist() -> None:
    required_paths = [
        Path("README_EN.md"),
        Path("SUPPORT.md"),
        Path("SECURITY.md"),
        Path("docs/i18n-status.md"),
        Path("assets/roadmap-visual.svg"),
        Path("docs/en/v670-release.md"),
        Path("docs/ru/v670-release.md"),
    ]
    for path in required_paths:
        assert path.exists(), f"Missing docs foundation asset: {path}"


def test_root_readmes_include_quick_start_and_learning_paths() -> None:
    for path in [Path("README.md"), Path("README_RU.md")]:
        text = path.read_text(encoding="utf-8")
        assert "Quick Start" in text or "Быстрый Старт" in text
        assert "Learning Paths" in text or "Пути Обучения" in text
        assert "roadmap-visual.svg" in text
