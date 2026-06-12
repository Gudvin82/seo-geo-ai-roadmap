from __future__ import annotations


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
