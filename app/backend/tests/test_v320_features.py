from __future__ import annotations

from pathlib import Path

from app.services.llms_validator import validate_llms_text


def test_llms_validator_accepts_good_content(client) -> None:
    response = client.post(
        "/api/v1/tools/llms-validator",
        json={
            "content": "# Example llms.txt\n- Home: https://example.com/\n- FAQ: https://example.com/faq\n- About: https://example.com/about\n"
        },
    )
    assert response.status_code == 200
    assert response.json()["is_valid"] is True
    assert response.json()["warnings"] == []


def test_llms_validator_flags_missing_structure(client) -> None:
    response = client.post(
        "/api/v1/tools/llms-validator",
        json={"content": "Example plain text with no structure"},
    )
    assert response.status_code == 200
    assert response.json()["is_valid"] is False
    assert response.json()["warnings"]


def test_llms_examples_and_templates_pass_validator() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    sample_content = (repo_root / "examples" / "sample-llms.txt").read_text(
        encoding="utf-8"
    )
    template_content = (repo_root / "templates" / "llms.txt.example").read_text(
        encoding="utf-8"
    )
    assert validate_llms_text(sample_content, checked_source="sample").is_valid is True
    assert (
        validate_llms_text(template_content, checked_source="template").is_valid is True
    )
