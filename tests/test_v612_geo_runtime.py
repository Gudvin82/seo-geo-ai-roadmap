from __future__ import annotations

from scripts._runtime_bootstrap import bootstrap_backend_imports

bootstrap_backend_imports()

from app.services.geo_intelligence import (  # noqa: E402
    build_geo_runtime,
    evidence,
    finding,
)


def test_score_does_not_turn_missing_components_into_zero() -> None:
    row = finding(
        category="entity_hierarchy_review",
        observation="Entity evidence is available.",
        recommendation="Keep entity facts current.",
        priority={"impact": 3, "effort": 2, "score": 20, "label": "P1"},
        evidence_items=[
            evidence(
                observation="Verified profile",
                source="fixture",
                evidence_type="verified",
                confidence=1,
            )
        ],
    )
    runtime = build_geo_runtime([row])
    assert runtime["scorecard"]["status"] == "partial"
    assert runtime["scorecard"]["score"] == 80
    assert runtime["scorecard"]["coverage"] == 0.25


def test_invalid_weight_shape_is_rejected() -> None:
    try:
        build_geo_runtime([], weights={"entity": 1})
    except ValueError as exc:
        assert "weights" in str(exc).lower()
    else:  # pragma: no cover - assertion branch
        raise AssertionError("invalid score weights must be rejected")
