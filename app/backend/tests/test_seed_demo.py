from __future__ import annotations

from app.seed import seed_demo_data


def test_seed_demo_data(settings) -> None:
    result = seed_demo_data(settings)
    assert result["workspace_slug"] == "demo-agency"
    assert result["project_id"] != 0
