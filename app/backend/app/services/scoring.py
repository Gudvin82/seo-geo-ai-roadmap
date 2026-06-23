from __future__ import annotations

from typing import Any

SEVERITY_POINTS = {"critical": 30, "high": 18, "medium": 9, "low": 4}
PRIORITY_LABELS = (
    (80, "fix_now"),
    (60, "next_batch"),
    (40, "planned"),
    (0, "observe"),
)

BENCHMARKS = {
    "lcp_seconds": {"good": 2.5, "warning": 4.0, "lower_is_better": True},
    "cls": {"good": 0.1, "warning": 0.25, "lower_is_better": True},
    "inp_ms": {"good": 200, "warning": 500, "lower_is_better": True},
    "schema_coverage": {"good": 0.8, "warning": 0.5, "lower_is_better": False},
    "ai_visibility_readiness": {
        "good": 0.75,
        "warning": 0.45,
        "lower_is_better": False,
    },
    "factual_consistency": {"good": 0.85, "warning": 0.55, "lower_is_better": False},
    "alice_ai_sov": {"good": 0.12, "warning": 0.04, "lower_is_better": False},
    "ru_geo_score": {"good": 75, "warning": 45, "lower_is_better": False},
}


def benchmark_status(metric_key: str, value: float | None) -> str:
    if value is None:
        return "insufficient_data"
    benchmark = BENCHMARKS.get(metric_key)
    if not benchmark:
        return "insufficient_data"
    good = benchmark["good"]
    warning = benchmark["warning"]
    lower_is_better = benchmark["lower_is_better"]
    if lower_is_better:
        if value <= good:
            return "better_than_baseline"
        if value >= warning:
            return "urgent_fix"
        return "worse_than_baseline"
    if value >= good:
        return "better_than_baseline"
    if value <= warning:
        return "urgent_fix"
    return "worse_than_baseline"


def ai_citation_score(results: list[dict[str, Any]]) -> float:
    if not results:
        return 0.0
    weighted_points = []
    for row in results:
        mention_score = 1.0 if row.get("mentioned") else 0.0
        citation_count = int(row.get("citation_count") or 0)
        citation_component = min(citation_count, 3) / 3
        weighted_points.append((mention_score * 0.7) + (citation_component * 0.3))
    return round((sum(weighted_points) / len(weighted_points)) * 100, 1)


def finding_priority(
    *,
    severity: str,
    impact: int,
    effort: int,
    confidence: int,
    benchmark: str,
) -> tuple[int, str]:
    severity_points = SEVERITY_POINTS.get(severity, SEVERITY_POINTS["medium"])
    benchmark_modifier = {
        "urgent_fix": 18,
        "worse_than_baseline": 8,
        "better_than_baseline": -8,
        "insufficient_data": 0,
    }.get(benchmark, 0)
    raw = severity_points + (impact * 8) + (confidence * 6) - (effort * 4)
    score = max(0, min(100, raw + benchmark_modifier))
    for threshold, label in PRIORITY_LABELS:
        if score >= threshold:
            return score, label
    return score, "observe"


def overall_score(findings: list[dict[str, Any]]) -> float:
    penalty = sum(
        SEVERITY_POINTS.get(item.get("severity", "medium"), SEVERITY_POINTS["medium"])
        for item in findings
    )
    priority_penalty = sum(
        (item.get("priority_score", 0) or 0) / 20 for item in findings
    )
    return round(max(0, 100 - penalty - priority_penalty), 1)


def ru_geo_score(
    *,
    integration_metrics: dict[str, dict[str, Any]],
) -> tuple[float, dict[str, float]]:
    components: dict[str, float] = {
        "yandex_webmaster": 0.0,
        "yandex_metrica": 0.0,
        "yandex_direct": 0.0,
        "yandex_business": 0.0,
        "yandex_neuro": 0.0,
        "alice_ai_visibility": 0.0,
    }

    if "yandex_webmaster" in integration_metrics:
        components["yandex_webmaster"] = 15.0
    if "yandex_metrica" in integration_metrics:
        components["yandex_metrica"] = 12.0
    if "yandex_direct" in integration_metrics:
        components["yandex_direct"] = 10.0
    if "yandex_business" in integration_metrics:
        metrics = integration_metrics["yandex_business"].get("metrics") or {}
        review_count = float(metrics.get("review_count", 0) or 0)
        components["yandex_business"] = 8.0 if review_count > 0 else 5.0
    if "yandex_neuro" in integration_metrics:
        metrics = integration_metrics["yandex_neuro"].get("metrics") or {}
        access = float(metrics.get("yandex_additional_access", 0) or 0)
        answer_ready_pages = float(metrics.get("ru_answer_ready_pages", 0) or 0)
        trust_blocks = float(metrics.get("trust_blocks_present", 0) or 0)
        legal_blocks = float(metrics.get("legal_blocks_present", 0) or 0)
        components["yandex_neuro"] = min(
            20.0,
            (8.0 * access)
            + min(answer_ready_pages, 8.0)
            + (2.0 * trust_blocks)
            + (2.0 * legal_blocks),
        )
    if "alice_ai_visibility" in integration_metrics:
        metrics = integration_metrics["alice_ai_visibility"].get("metrics") or {}
        sov = float(metrics.get("share_of_voice", 0) or 0)
        query_coverage = float(metrics.get("query_coverage", 0) or 0)
        own_mentions = float(metrics.get("queries_with_own_mentions", 0) or 0)
        insufficient = bool(metrics.get("insufficient_data"))
        if insufficient:
            components["alice_ai_visibility"] = 3.0
        else:
            components["alice_ai_visibility"] = min(
                35.0,
                min(sov / 0.12, 1.0) * 20.0
                + min(query_coverage, 1.0) * 8.0
                + min(own_mentions / 10.0, 1.0) * 7.0,
            )

    score = round(min(100.0, sum(components.values())), 1)
    return score, components
