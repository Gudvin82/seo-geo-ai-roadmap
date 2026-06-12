from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FactSurface:
    name: str
    content: str


@dataclass
class DriftItem:
    drift_type: str
    severity: str
    observed: str
    inferred_issue: str
    recommended_next_step: str


@dataclass
class FactDriftResult:
    status: str
    surface_count: int
    drift_items: list[DriftItem]
    detected_types: list[str]
    limitations: list[str]


KEYWORD_GROUPS = {
    "phone": ["phone", "telephone", "tel", "+7", "+1"],
    "pricing": ["price", "pricing", "cost", "from ", "usd", "rub", "eur"],
    "address": ["address", "office", "street", "city", "moscow", "new york"],
    "founder": ["founder", "ceo", "author", "expert", "dr.", "doctor", "lawyer"],
}


def _contains_any(content: str, values: list[str]) -> bool:
    lowered = content.lower()
    return any(value in lowered for value in values)


def detect_fact_drift(surfaces: list[FactSurface]) -> FactDriftResult:
    drift_items: list[DriftItem] = []

    if len(surfaces) < 2:
        return FactDriftResult(
            status="insufficient_input",
            surface_count=len(surfaces),
            drift_items=[],
            detected_types=[],
            limitations=[
                "Provide at least two surfaces to compare fact drift.",
            ],
        )

    for drift_type, keywords in KEYWORD_GROUPS.items():
        present = [surface.name for surface in surfaces if _contains_any(surface.content, keywords)]
        absent = [surface.name for surface in surfaces if surface.name not in present]
        if present and absent:
            drift_items.append(
                DriftItem(
                    drift_type=drift_type,
                    severity="medium" if len(present) >= len(absent) else "high",
                    observed=(
                        f"{drift_type} signals appear on {', '.join(present)} but not on "
                        f"{', '.join(absent)}."
                    ),
                    inferred_issue=(
                        f"Cross-surface entity or trust information is inconsistent for {drift_type}."
                    ),
                    recommended_next_step=(
                        f"Review canonical {drift_type} facts and align website, schema, llms.txt, "
                        "and AI-facing surfaces."
                    ),
                )
            )

    status = "drift_detected" if drift_items else "no_strong_drift_detected"
    return FactDriftResult(
        status=status,
        surface_count=len(surfaces),
        drift_items=drift_items,
        detected_types=sorted({item.drift_type for item in drift_items}),
        limitations=[
            "Current detection is keyword- and pattern-based, not a full semantic verifier.",
            "False positives are possible when surfaces intentionally omit low-priority facts.",
            "Human review is required before treating drift as a publishing bug.",
        ],
    )
