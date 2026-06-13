from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandRoute:
    command: str
    title: str
    summary: str
    recommended_scripts: list[str]
    recommended_docs: list[str]
    api_routes: list[str]
    next_step: str


COMMAND_CATALOG: dict[str, CommandRoute] = {
    "audit": CommandRoute(
        command="audit",
        title="Full GEO and SEO audit",
        summary="Run the core multi-step audit flow for one site or project.",
        recommended_scripts=[
            "scripts/check-robots-ai-bots.py",
            "scripts/sitemap-checker.py",
            "scripts/check_hallucinations.py",
        ],
        recommended_docs=[
            "docs/en/01-audit.md",
            "docs/en/08-geo-ai-search.md",
            "docs/en/how-it-works-v340.md",
        ],
        api_routes=["POST /api/v1/audit-runs/run", "GET /api/v1/reports"],
        next_step="Create or select a project, then run an audit and review the generated report plus artifacts.",
    ),
    "quick": CommandRoute(
        command="quick",
        title="Quick AI visibility snapshot",
        summary="Get a fast starter review when a full audit is too heavy for the first pass.",
        recommended_scripts=[
            "scripts/check-llms-txt.py",
            "scripts/check-robots-ai-bots.py",
        ],
        recommended_docs=[
            "docs/en/08-geo-ai-search.md",
            "docs/en/command-catalog-v340.md",
        ],
        api_routes=["POST /api/v1/tools/command-router"],
        next_step="Use the quick route to find the first obvious blockers, then escalate to a full audit if needed.",
    ),
    "citability": CommandRoute(
        command="citability",
        title="Citation readiness review",
        summary="Evaluate whether content blocks look extractable, trustable, and usable in AI answers.",
        recommended_scripts=[
            "scripts/check_hallucinations.py",
            "scripts/content-inventory-helper.py",
        ],
        recommended_docs=[
            "docs/en/answer-ready-patterns.md",
            "docs/en/geo-cro-bridge-v340.md",
        ],
        api_routes=["POST /api/v1/tools/fact-drift"],
        next_step="Focus on answer-ready blocks, proof density, and expert attribution before chasing volume.",
    ),
    "crawlers": CommandRoute(
        command="crawlers",
        title="AI crawler access analysis",
        summary="Check whether robots rules help or hurt discovery by AI and search crawlers.",
        recommended_scripts=["scripts/check-robots-ai-bots.py"],
        recommended_docs=[
            "docs/en/ai-bots-and-robots.md",
            "docs/en/geo-ai-surfaces.md",
        ],
        api_routes=[],
        next_step="Review robots access first, then confirm the intended public surfaces remain reachable.",
    ),
    "llmstxt": CommandRoute(
        command="llmstxt",
        title="llms.txt analysis and generation",
        summary="Generate, validate, and improve llms.txt for AI-facing discoverability.",
        recommended_scripts=[
            "scripts/generate_llms_txt.py",
            "scripts/check-llms-txt.py",
        ],
        recommended_docs=[
            "docs/en/llms-validator.md",
            "docs/en/08-geo-ai-search.md",
        ],
        api_routes=["POST /api/v1/tools/llms-validator"],
        next_step="Generate a first llms.txt draft, validate it, then publish and re-check the live file.",
    ),
    "brands": CommandRoute(
        command="brands",
        title="Brand and fact consistency review",
        summary="Look for mismatches across brand facts, entity signals, and AI-facing surfaces.",
        recommended_scripts=["scripts/fact_drift_checker.py"],
        recommended_docs=[
            "docs/en/canonical-facts-and-entity-consistency.md",
            "docs/en/fact-drift-monitoring.md",
            "docs/en/trust-surface-mapping.md",
        ],
        api_routes=[
            "POST /api/v1/tools/fact-drift",
            "GET /api/v1/brand-facts/{project_id}",
        ],
        next_step="Use the truth center as the canonical source, then align website, schema, and llms.txt surfaces.",
    ),
    "platforms": CommandRoute(
        command="platforms",
        title="Platform-specific optimization",
        summary="Translate one site into ChatGPT, Perplexity, Gemini, and AI Overview-friendly improvements.",
        recommended_scripts=[
            "scripts/provider_benchmark_stub.py",
            "scripts/ai-share-of-voice-tracker.py",
        ],
        recommended_docs=[
            "docs/en/provider-matrix.md",
            "docs/en/provider-benchmarks.md",
            "docs/en/geo-ai-surfaces.md",
        ],
        api_routes=["POST /api/v1/sov/check", "GET /api/v1/sov/history"],
        next_step="Treat each AI surface as a distribution layer with different evidence and entity expectations.",
    ),
    "schema": CommandRoute(
        command="schema",
        title="Structured data analysis",
        summary="Review JSON-LD quality and connect it to entity clarity and trust surfaces.",
        recommended_scripts=["scripts/schema-validator.py"],
        recommended_docs=[
            "docs/en/json-ld-templates.md",
            "docs/en/entity-seo-and-kg.md",
        ],
        api_routes=[],
        next_step="Validate syntax first, then strengthen the business and entity meaning carried by the schema.",
    ),
    "technical": CommandRoute(
        command="technical",
        title="Technical SEO foundations",
        summary="Check accessibility, sitemap, crawlability, and core technical discoverability signals.",
        recommended_scripts=[
            "scripts/sitemap-checker.py",
            "scripts/check-robots-ai-bots.py",
        ],
        recommended_docs=[
            "docs/en/05-technical-seo.md",
            "docs/en/geo-measurement-maturity.md",
        ],
        api_routes=["POST /api/v1/audit-runs/run"],
        next_step="Treat technical SEO as the floor. GEO improvements compound only when the floor is solid.",
    ),
    "content": CommandRoute(
        command="content",
        title="Content quality and freshness",
        summary="Review whether content is current, answer-ready, and believable for both humans and LLMs.",
        recommended_scripts=[
            "scripts/content_freshness_checker.py",
            "scripts/content-inventory-helper.py",
        ],
        recommended_docs=[
            "docs/en/07-content-eeat.md",
            "docs/en/answer-ready-patterns.md",
        ],
        api_routes=[],
        next_step="Refresh stale high-intent pages first, then add clearer answers and proof blocks.",
    ),
    "report": CommandRoute(
        command="report",
        title="Executive and client reporting",
        summary="Turn audit outputs into stakeholder-ready summaries, priorities, and delivery packs.",
        recommended_scripts=["scripts/roi_calculator.py"],
        recommended_docs=[
            "docs/en/executive-dashboards.md",
            "docs/en/roi-summary-template.md",
            "docs/en/client-delivery.md",
        ],
        api_routes=["GET /api/v1/reports", "POST /api/v1/deliverables/client-pack"],
        next_step="Translate operator evidence into owner, founder, or client language before presenting the work.",
    ),
    "compare": CommandRoute(
        command="compare",
        title="Recurring comparison and delta tracking",
        summary="Plan repeated audits, SoV snapshots, and validator checks so progress can be shown over time.",
        recommended_scripts=[
            "scripts/scheduled_check_runner.py",
            "scripts/ai-share-of-voice-tracker.py",
        ],
        recommended_docs=[
            "docs/en/scheduled-operations.md",
            "docs/en/competitive-geo-gap-examples.md",
        ],
        api_routes=["GET /api/v1/scheduled-checks", "POST /api/v1/scheduled-checks"],
        next_step="Define the recurring schedule, artifact expectations, and the comparison questions before the next run.",
    ),
}


def resolve_command_route(command: str) -> CommandRoute:
    key = command.strip().lower()
    if key not in COMMAND_CATALOG:
        supported = ", ".join(sorted(COMMAND_CATALOG))
        raise ValueError(f"Unsupported command '{command}'. Supported: {supported}.")
    return COMMAND_CATALOG[key]


def command_catalog() -> list[CommandRoute]:
    return [COMMAND_CATALOG[key] for key in sorted(COMMAND_CATALOG)]
