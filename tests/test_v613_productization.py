from __future__ import annotations

from scripts._runtime_bootstrap import bootstrap_backend_imports

bootstrap_backend_imports()

from app.services.geo_intelligence import (  # noqa: E402
    build_unified_report,
    normalize_scan_issue,
)


def test_scanner_issue_adapts_to_canonical_unified_report() -> None:
    finding = normalize_scan_issue(
        {
            "issue_id": "missing_canonical",
            "severity": "high",
            "title": "Canonical is missing",
            "recommended_action": "Add a canonical URL.",
        },
        "https://example.com",
    )
    report = build_unified_report(target_url="https://example.com", findings=[finding])
    assert report["report_type"] == "geo_intelligence_unified"
    assert (
        report["technical_seo"][0]["evidence"][0]["source"] == "scanner_machine_report"
    )
    assert report["roadmap"][0]["action"] == "Add a canonical URL."
