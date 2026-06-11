from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check-llms-txt.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_valid_llms_file_passes(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text(
        """# Example
> https://example.com/ - Homepage
> https://example.com/faq - FAQ
> https://example.com/about - About
""",
        encoding="utf-8",
    )
    result = run_command("--file", str(llms_file))
    assert result.returncode == 0
    assert "PASS" in result.stdout


def test_missing_required_sections_fails(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text(
        "# Example\n> https://example.com/ - Homepage\n", encoding="utf-8"
    )
    result = run_command("--file", str(llms_file))
    assert result.returncode == 1
    assert "faq" in result.stdout.lower()
    assert "about" in result.stdout.lower()


def test_malformed_structure_fails(tmp_path: Path) -> None:
    llms_file = tmp_path / "llms.txt"
    llms_file.write_text("homepage\nfaq\nabout\n", encoding="utf-8")
    result = run_command("--file", str(llms_file))
    assert result.returncode == 1
    assert (
        "top-level heading" in result.stdout.lower()
        or "structured entries" in result.stdout.lower()
    )
