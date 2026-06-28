from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass

REQUIRED_HINTS = ["/", "faq", "about"]


@dataclass
class LlmsValidationResult:
    is_valid: bool
    line_count: int
    checked_source: str
    warnings: list[str]
    recommendations: list[str]
    observed_facts: list[str]


def load_llms_text_from_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def normalize_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def line_contains_absolute_url(line: str) -> bool:
    lowered = line.lower()
    return "http://" in lowered or "https://" in lowered


def validate_llms_text(
    content: str, *, checked_source: str = "inline"
) -> LlmsValidationResult:
    lines = normalize_lines(content)
    warnings: list[str] = []
    recommendations: list[str] = []
    observed_facts: list[str] = [f"Checked {len(lines)} non-empty lines."]

    missing = [
        hint
        for hint in REQUIRED_HINTS
        if not any(hint in line.lower() for line in lines)
    ]
    has_header = any(line.startswith("#") for line in lines)
    bullet_like = [
        line for line in lines if line.startswith(("-", "*", ">")) or " - " in line
    ]
    has_url = any(line_contains_absolute_url(line) for line in lines)

    if not has_header:
        warnings.append("Missing top-level heading.")
        recommendations.append(
            "Add a top-level heading that explains what the file covers if you intentionally use llms.txt as an optional AI-routing file."
        )
    if not bullet_like:
        warnings.append("Missing structured entries or bullet-like lines.")
        recommendations.append(
            "List key pages, offers, policies, or fact hubs in a structured bullet format if this file is part of your agent or AI-discovery workflow."
        )
    if not has_url:
        warnings.append("No explicit absolute URLs detected.")
        recommendations.append(
            "Add canonical URLs for priority pages so agent-style or AI consumers can resolve the right destinations."
        )
    if len(lines) < 4:
        warnings.append("The file is very short and may be under-specified.")
        recommendations.append(
            "Expand the file with core sections for homepage, about, FAQ, contact, and trust pages if you choose to maintain llms.txt at all."
        )
    if missing:
        warnings.append(f"Missing common hints: {', '.join(missing)}.")
        recommendations.append(
            "Mention homepage, about/trust material, and FAQ or answer-ready sections explicitly if the file is part of your operating model."
        )

    observed_facts.extend(
        [
            "Top-level heading detected."
            if has_header
            else "Top-level heading not detected.",
            "Structured bullet-like entries detected."
            if bullet_like
            else "Structured bullet-like entries not detected.",
            "At least one absolute URL detected."
            if has_url
            else "No absolute URLs detected.",
            "llms.txt is treated here as an optional AI-routing surface, not a Google ranking requirement.",
        ]
    )

    return LlmsValidationResult(
        is_valid=not warnings,
        line_count=len(lines),
        checked_source=checked_source,
        warnings=warnings,
        recommendations=recommendations,
        observed_facts=observed_facts,
    )


def validate_llms_url(url: str) -> LlmsValidationResult:
    try:
        content = load_llms_text_from_url(url)
    except (
        urllib.error.URLError
    ) as exc:  # pragma: no cover - exercised through API tests
        return LlmsValidationResult(
            is_valid=False,
            line_count=0,
            checked_source=url,
            warnings=[f"Unable to load llms.txt: {exc}"],
            recommendations=[
                "Check that the URL is public, reachable, and returns plain text.",
            ],
            observed_facts=["The remote file could not be fetched."],
        )
    return validate_llms_text(content, checked_source=url)
