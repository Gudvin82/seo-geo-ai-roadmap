from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandRoute:
    command: str
    title: str
    summary: str
    intent: str
    aliases: list[str]
    recommended_scripts: list[str]
    recommended_docs: list[str]
    api_routes: list[str]
    example_invocations: list[str]
    output_artifacts: list[str]
    use_cases: list[str]
    next_step: str


COMMAND_CATALOG: dict[str, CommandRoute] = {
    "audit": CommandRoute(
        command="audit",
        title="Full GEO and SEO audit",
        summary="Run the core multi-step audit flow for one site or project.",
        intent="Create a complete baseline across technical SEO, GEO, trust, and AI discoverability.",
        aliases=["scan", "full-audit", "baseline"],
        recommended_scripts=[
            "scripts/check-robots-ai-bots.py",
            "scripts/sitemap-checker.py",
            "scripts/check_hallucinations.py",
        ],
        recommended_docs=[
            "docs/en/01-audit.md",
            "docs/en/08-geo-ai-search.md",
            "docs/en/how-it-works-v340.md",
            "docs/en/research-build-improve-repeat-v380.md",
        ],
        api_routes=["POST /api/v1/audit-runs/run", "GET /api/v1/reports"],
        example_invocations=[
            "/geo audit",
            "/geo scan",
            "/geo audit https://example.com",
        ],
        output_artifacts=[
            "audit run",
            "issue clusters",
            "report package",
            "remediation backlog",
        ],
        use_cases=["client baseline", "relaunch audit", "quarterly re-measurement"],
        next_step="Create or select a project, then run an audit and review the generated report plus artifacts.",
    ),
    "brands": CommandRoute(
        command="brands",
        title="Brand and fact consistency review",
        summary="Look for mismatches across brand facts, entity signals, and AI-facing surfaces.",
        intent="Keep one truth layer across website, schema, reports, and AI-facing content.",
        aliases=["facts", "truth", "entity", "brand-facts"],
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
        example_invocations=[
            "/geo brands",
            "/geo facts",
            "/geo truth",
        ],
        output_artifacts=[
            "fact drift review",
            "truth center alignment notes",
            "entity cleanup tasks",
        ],
        use_cases=[
            "brand governance",
            "legal/trust review",
            "multi-market consistency",
        ],
        next_step="Use the truth center as the canonical source, then align website, schema, and llms.txt surfaces.",
    ),
    "citability": CommandRoute(
        command="citability",
        title="Citation readiness review",
        summary="Evaluate whether content blocks look extractable, trustable, and usable in AI answers.",
        intent="Check whether the site is shaped for answer extraction, quoting, and AI reuse.",
        aliases=["citation", "answer-ready", "answers"],
        recommended_scripts=[
            "scripts/check_hallucinations.py",
            "scripts/content-inventory-helper.py",
        ],
        recommended_docs=[
            "docs/en/answer-ready-patterns.md",
            "docs/en/geo-cro-bridge-v340.md",
            "docs/en/distribution-and-gtm-v380.md",
        ],
        api_routes=["POST /api/v1/tools/fact-drift"],
        example_invocations=[
            "/geo citability",
            "/geo citation",
            "/geo answer-ready",
        ],
        output_artifacts=[
            "citation readiness notes",
            "proof gaps",
            "content block recommendations",
        ],
        use_cases=["content upgrade", "AI answer optimization", "proof-led rewriting"],
        next_step="Focus on answer-ready blocks, proof density, and expert attribution before chasing volume.",
    ),
    "compare": CommandRoute(
        command="compare",
        title="Recurring comparison and delta tracking",
        summary="Plan repeated audits, SoV snapshots, and validator checks so progress can be shown over time.",
        intent="Make improvement measurable through history, drift, regression, and re-measurement.",
        aliases=["measure", "delta", "history", "drift"],
        recommended_scripts=[
            "scripts/scheduled_check_runner.py",
            "scripts/ai-share-of-voice-tracker.py",
        ],
        recommended_docs=[
            "docs/en/scheduled-operations.md",
            "docs/en/competitive-geo-gap-examples.md",
            "docs/en/research-build-improve-repeat-v380.md",
        ],
        api_routes=["GET /api/v1/scheduled-checks", "POST /api/v1/scheduled-checks"],
        example_invocations=[
            "/geo compare",
            "/geo measure",
            "/geo drift",
        ],
        output_artifacts=[
            "before/after deltas",
            "history view",
            "recurring ops cadence",
        ],
        use_cases=[
            "retainer reporting",
            "regression detection",
            "proof of improvement",
        ],
        next_step="Define the recurring schedule, artifact expectations, and the comparison questions before the next run.",
    ),
    "cases": CommandRoute(
        command="cases",
        title="Case-library and proof operations",
        summary="Review bounded public cases, synthetic training cases, and evidence-pack paths.",
        intent="Keep case publication, proof boundaries, and implementation handoff explicit.",
        aliases=["case-library", "proof-library", "synthetic-cases"],
        recommended_scripts=[
            "scripts/case_library_builder.py",
            "scripts/synthetic_case_builder.py",
            "scripts/proof_pack_builder.py",
            "scripts/issue_pack_generator.py",
        ],
        recommended_docs=[
            "REAL_CASES.md",
            "docs/en/case-library.md",
            "docs/en/synthetic-cases.md",
            "docs/en/issue-pack-workflow.md",
        ],
        api_routes=[
            "GET /api/v1/settings/proof-kit",
            "GET /api/v1/settings/evidence-lab",
            "GET /api/v1/proof/timeline",
        ],
        example_invocations=[
            "/geo cases",
            "/geo case-library",
            "/geo synthetic-cases",
        ],
        output_artifacts=[
            "case-library index",
            "synthetic training case",
            "issue pack",
            "bounded proof export",
        ],
        use_cases=[
            "public proof review",
            "team training",
            "implementation handoff",
        ],
        next_step="Separate bounded public evidence from synthetic training material before publishing or handing off any case output.",
    ),
    "content": CommandRoute(
        command="content",
        title="Content quality and freshness",
        summary="Review whether content is current, answer-ready, and believable for both humans and LLMs.",
        intent="Prioritize visible content upgrades that improve factuality, freshness, and answerability.",
        aliases=["freshness", "content-audit", "faq"],
        recommended_scripts=[
            "scripts/content_freshness_checker.py",
            "scripts/content-inventory-helper.py",
        ],
        recommended_docs=[
            "docs/en/07-content-eeat.md",
            "docs/en/answer-ready-patterns.md",
            "docs/en/distribution-and-gtm-v380.md",
        ],
        api_routes=[],
        example_invocations=[
            "/geo content",
            "/geo freshness",
            "/geo faq",
        ],
        output_artifacts=[
            "content refresh list",
            "answer-ready opportunities",
            "priority rewrite queue",
        ],
        use_cases=["editorial planning", "service page upgrades", "FAQ expansion"],
        next_step="Refresh stale high-intent pages first, then add clearer answers and proof blocks.",
    ),
    "crawlers": CommandRoute(
        command="crawlers",
        title="AI crawler access analysis",
        summary="Check whether robots rules help or hurt discovery by AI and search crawlers.",
        intent="Verify crawler policies for Google, Yandex, and AI bots without blocking intended visibility.",
        aliases=["bots", "robots", "ai-bots"],
        recommended_scripts=["scripts/check-robots-ai-bots.py"],
        recommended_docs=[
            "docs/en/ai-bots-and-robots.md",
            "docs/en/geo-ai-surfaces.md",
            "docs/en/discoverability-coverage-v370.md",
        ],
        api_routes=[],
        example_invocations=[
            "/geo crawlers",
            "/geo bots",
            "/geo robots",
        ],
        output_artifacts=[
            "robots policy review",
            "AI bot access notes",
            "block or allow recommendations",
        ],
        use_cases=["technical hygiene", "RU/Yandex review", "AI bot policy review"],
        next_step="Review robots access first, then confirm the intended public surfaces remain reachable.",
    ),
    "deploy": CommandRoute(
        command="deploy",
        title="Turnkey deployment and environment bootstrap",
        summary="Pick the right self-hosted path for demo, production-like setup, or client delivery.",
        intent="Deploy the product, verify it, and hand off a stable operating surface.",
        aliases=["setup", "bootstrap", "launch"],
        recommended_scripts=[
            "scripts/bootstrap_self_hosted.py",
            "scripts/agent_handoff_pack.py",
        ],
        recommended_docs=[
            "DEPLOYMENT.md",
            "VERIFY_DEPLOYMENT.md",
            "ARCHITECTURE_NOTE.md",
            "docs/en/framework-integrations-v380.md",
        ],
        api_routes=["GET /healthz", "GET /readyz"],
        example_invocations=[
            "/geo deploy",
            "/geo deploy demo",
            "/geo deploy scanner",
        ],
        output_artifacts=[
            "deployment checklist",
            "verification summary",
            "demo credentials or production handoff notes",
        ],
        use_cases=["agency setup", "founder stack", "internal operator deployment"],
        next_step="Choose the deployment mode first, then run the matching bootstrap and verification flow before claiming success.",
    ),
    "graph": CommandRoute(
        command="graph",
        title="Graph intelligence and explainability",
        summary="Visualize site structure, discoverability surfaces, issue dependencies, and trust relationships.",
        intent="Explain what matters, what connects, and what to fix next through interactive graph views.",
        aliases=["map", "graph-intelligence", "dependencies", "explain"],
        recommended_scripts=["scripts/geo_command_surface.py"],
        recommended_docs=[
            "docs/en/graph-intelligence-v380.md",
            "docs/en/distribution-and-gtm-v380.md",
        ],
        api_routes=["GET /graph.html"],
        example_invocations=[
            "/geo graph",
            "/geo map",
            "/geo dependencies",
        ],
        output_artifacts=[
            "graph JSON export",
            "issue dependency map",
            "surface relationship explanation",
        ],
        use_cases=[
            "client explanation",
            "operator prioritization",
            "sales walkthrough",
        ],
        next_step="Open the graph view, switch between site, surface, issue, and trust modes, then export the graph snapshot with the recommended fix order.",
    ),
    "llmstxt": CommandRoute(
        command="llmstxt",
        title="llms.txt analysis and generation",
        summary="Generate, validate, and improve llms.txt for AI-facing discoverability.",
        intent="Turn AI-readable guidance files into an explicit public distribution layer.",
        aliases=["llms", "llms.txt", "ai-guidance", "aitxt"],
        recommended_scripts=[
            "scripts/generate_llms_txt.py",
            "scripts/check-llms-txt.py",
        ],
        recommended_docs=[
            "docs/en/llms-validator.md",
            "docs/en/08-geo-ai-search.md",
            "docs/en/distribution-and-gtm-v380.md",
        ],
        api_routes=["POST /api/v1/tools/llms-validator"],
        example_invocations=[
            "/geo llmstxt",
            "/geo llms",
            "/geo ai-guidance",
        ],
        output_artifacts=[
            "llms.txt draft",
            "validation report",
            "publish checklist",
        ],
        use_cases=[
            "AI discoverability hygiene",
            "content access guidance",
            "operator onboarding",
        ],
        next_step="Generate a first llms.txt draft, validate it, then publish and re-check the live file.",
    ),
    "platforms": CommandRoute(
        command="platforms",
        title="Platform-specific optimization",
        summary="Translate one site into ChatGPT, Perplexity, Gemini, and AI Overview-friendly improvements.",
        intent="Map the same website into multiple answer engines and compare where evidence is weak.",
        aliases=["providers", "sov", "ai-surfaces"],
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
        example_invocations=[
            "/geo platforms",
            "/geo providers",
            "/geo sov",
        ],
        output_artifacts=[
            "provider comparison",
            "AI share of voice snapshot",
            "surface-specific recommendations",
        ],
        use_cases=["competitive monitoring", "provider comparison", "channel planning"],
        next_step="Treat each AI surface as a distribution layer with different evidence and entity expectations.",
    ),
    "quick": CommandRoute(
        command="quick",
        title="Quick AI visibility snapshot",
        summary="Get a fast starter review when a full audit is too heavy for the first pass.",
        intent="Triage obvious blockers fast before spending time on full operator work.",
        aliases=["snapshot", "triage", "quick-audit"],
        recommended_scripts=[
            "scripts/check-llms-txt.py",
            "scripts/check-robots-ai-bots.py",
        ],
        recommended_docs=[
            "docs/en/08-geo-ai-search.md",
            "docs/en/command-catalog-v380.md",
        ],
        api_routes=["POST /api/v1/tools/command-router"],
        example_invocations=[
            "/geo quick",
            "/geo snapshot",
            "/geo triage https://example.com",
        ],
        output_artifacts=[
            "starter findings",
            "first blockers list",
            "escalation recommendation",
        ],
        use_cases=[
            "pre-sales discovery",
            "lightweight founder check",
            "first-call audit",
        ],
        next_step="Use the quick route to find the first obvious blockers, then escalate to a full audit if needed.",
    ),
    "report": CommandRoute(
        command="report",
        title="Executive and client reporting",
        summary="Turn audit outputs into stakeholder-ready summaries, priorities, and delivery packs.",
        intent="Translate operator evidence into founder, executive, and client language.",
        aliases=["deliverables", "client-pack", "executive", "export"],
        recommended_scripts=["scripts/roi_calculator.py"],
        recommended_docs=[
            "docs/en/executive-dashboards.md",
            "docs/en/roi-summary-template.md",
            "docs/en/client-delivery.md",
            "REPORTING_PACKS.md",
        ],
        api_routes=["GET /api/v1/reports", "POST /api/v1/deliverables/client-pack"],
        example_invocations=[
            "/geo report",
            "/geo deliverables",
            "/geo executive",
        ],
        output_artifacts=[
            "executive summary",
            "client delivery pack",
            "fix pack",
            "ROI framing",
        ],
        use_cases=["monthly reporting", "sales support", "client handoff"],
        next_step="Translate operator evidence into owner, founder, or client language before presenting the work.",
    ),
    "proofpack": CommandRoute(
        command="proofpack",
        title="Proof-pack and case evidence builder",
        summary="Turn before/after work into a reusable, bounded, and publishable proof artifact.",
        intent="Separate safe facts from inferences and keep evidence links explicit.",
        aliases=["proof-pack", "case-pack", "evidence-pack"],
        recommended_scripts=["scripts/proof_pack_builder.py"],
        recommended_docs=[
            "docs/en/proof-pack-playbook.md",
            "docs/en/case-library.md",
            "docs/en/v420-production-proof.md",
        ],
        api_routes=["GET /api/v1/proof/timeline", "GET /api/v1/proof/evidence"],
        example_invocations=[
            "/geo proofpack",
            "/geo proof-pack",
            "/geo case-pack",
        ],
        output_artifacts=[
            "proof pack",
            "client-safe case summary",
            "bounded evidence notes",
        ],
        use_cases=[
            "case publication",
            "client reporting",
            "public proof hygiene",
        ],
        next_step="Collect facts, score deltas, and evidence links first, then build a proof pack before making public claims.",
    ),
    "scanner": CommandRoute(
        command="scanner",
        title="Public or client-facing scanner deployment",
        summary="Plan the intake flow, verification model, and delivery surface for a reusable site scanner.",
        intent="Package the audit core into a reusable intake, queue, and export experience.",
        aliases=["intake", "public-scanner", "scan-service"],
        recommended_scripts=[
            "scripts/bootstrap_self_hosted.py",
            "scripts/agent_handoff_pack.py",
        ],
        recommended_docs=[
            "ARCHITECTURE_NOTE.md",
            "docs/en/bootstrap-guide-v340.md",
            "docs/en/api-reference.md",
            "docs/en/framework-integrations-v380.md",
        ],
        api_routes=[
            "POST /api/v1/tools/command-router",
            "POST /api/v1/audit-runs/run",
            "GET /api/v1/reports",
        ],
        example_invocations=[
            "/geo scanner",
            "/geo intake",
            "/geo public-scanner",
        ],
        output_artifacts=[
            "scanner flow plan",
            "verification model",
            "job and export delivery pattern",
        ],
        use_cases=["lead magnet", "internal intake", "client self-serve triage"],
        next_step="Decide whether the scanner is internal, client-gated, or public, then add verification, queueing, and report delivery around the existing audit core.",
    ),
    "schema": CommandRoute(
        command="schema",
        title="Structured data analysis",
        summary="Review JSON-LD quality and connect it to entity clarity and trust surfaces.",
        intent="Audit structured data as a discoverability, entity, and trust acceleration layer.",
        aliases=["jsonld", "structured-data", "markup"],
        recommended_scripts=["scripts/schema-validator.py"],
        recommended_docs=[
            "docs/en/json-ld-templates.md",
            "docs/en/entity-seo-and-kg.md",
            "docs/en/discoverability-coverage-v370.md",
        ],
        api_routes=[],
        example_invocations=[
            "/geo schema",
            "/geo jsonld",
            "/geo structured-data",
        ],
        output_artifacts=[
            "schema coverage summary",
            "missing entity fields list",
            "recommended markup pack",
        ],
        use_cases=[
            "entity SEO",
            "service schema upgrade",
            "trust-surface reinforcement",
        ],
        next_step="Validate syntax first, then strengthen the business and entity meaning carried by the schema.",
    ),
    "semantic": CommandRoute(
        command="semantic",
        title="Semantic demand and page mapping",
        summary="Cluster keyword demand into page types, intent lanes, and execution priorities.",
        intent="Translate search demand into a practical page architecture instead of disconnected keyword lists.",
        aliases=["semantics", "intent", "keyword-map"],
        recommended_scripts=[
            "scripts/semantic_gap_mapper.py",
            "scripts/serp-intent-cluster-helper.py",
            "scripts/content-inventory-helper.py",
        ],
        recommended_docs=[
            "docs/en/semantic-core-and-intent-playbook.md",
            "docs/en/06-semantics-onpage.md",
            "docs/en/checklist-generator.md",
        ],
        api_routes=["GET /api/v1/settings/seo-maturity-center"],
        example_invocations=[
            "/geo semantic",
            "/geo semantics",
            "/geo intent",
        ],
        output_artifacts=[
            "semantic cluster map",
            "recommended page types",
            "content backlog inputs",
        ],
        use_cases=[
            "new page planning",
            "content strategy",
            "demand-to-page mapping",
        ],
        next_step="Cluster intent first, then connect each cluster to one owned page type and a proof requirement.",
    ),
    "technical": CommandRoute(
        command="technical",
        title="Technical SEO foundations",
        summary="Check accessibility, sitemap, crawlability, and core technical discoverability signals.",
        intent="Secure the technical floor so higher-layer GEO and AI signals can compound.",
        aliases=["tech", "crawlability", "foundations"],
        recommended_scripts=[
            "scripts/sitemap-checker.py",
            "scripts/check-robots-ai-bots.py",
        ],
        recommended_docs=[
            "docs/en/05-technical-seo.md",
            "docs/en/geo-measurement-maturity.md",
            "docs/en/discoverability-coverage-v370.md",
        ],
        api_routes=["POST /api/v1/audit-runs/run"],
        example_invocations=[
            "/geo technical",
            "/geo tech",
            "/geo crawlability",
        ],
        output_artifacts=[
            "technical findings",
            "crawlability review",
            "fix-first checklist",
        ],
        use_cases=["migration QA", "foundation cleanup", "technical backlog creation"],
        next_step="Treat technical SEO as the floor. GEO improvements compound only when the floor is solid.",
    ),
}


COMMAND_ALIAS_INDEX: dict[str, str] = {}
for route in COMMAND_CATALOG.values():
    COMMAND_ALIAS_INDEX[route.command] = route.command
    for alias in route.aliases:
        COMMAND_ALIAS_INDEX[alias.lower()] = route.command


def normalize_command(command: str) -> str:
    cleaned = command.strip().strip("`").lower()
    if not cleaned:
        return cleaned
    tokens = cleaned.split()
    if tokens[0] in {"/geo", "geo"}:
        return "catalog" if len(tokens) == 1 else tokens[1]
    if cleaned.startswith("/geo/"):
        return cleaned.removeprefix("/geo/").split()[0]
    return tokens[0]


def resolve_command_route(command: str) -> CommandRoute:
    key = normalize_command(command)
    if key not in COMMAND_ALIAS_INDEX:
        supported = ", ".join(sorted(COMMAND_ALIAS_INDEX))
        raise ValueError(f"Unsupported command '{command}'. Supported: {supported}.")
    return COMMAND_CATALOG[COMMAND_ALIAS_INDEX[key]]


def command_catalog() -> list[CommandRoute]:
    return [COMMAND_CATALOG[key] for key in sorted(COMMAND_CATALOG)]
