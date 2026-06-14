from __future__ import annotations

from app.services import discoverability_checks, scan_jobs


def test_yandex_additional_is_distinct_from_yandexbot() -> None:
    robots = """
User-agent: YandexBot
Allow: /

User-agent: YandexAdditional
Disallow: /
"""
    groups = discoverability_checks.parse_robots_groups(robots)
    yandex_bot = discoverability_checks.evaluate_bot_policy(groups, "YandexBot")
    yandex_additional = discoverability_checks.evaluate_bot_policy(
        groups, "YandexAdditional"
    )
    assert yandex_bot["status"] == "allowed"
    assert yandex_additional["status"] == "blocked"
    assert yandex_bot["matched_group"] != yandex_additional["matched_group"]


def test_ai_txt_report_warns_on_robot_contradiction() -> None:
    ai_content = """
policy: allow-public-facts
summary: Keep AI guidance aligned with public facts.
allow: /
llms: https://example.com/llms.txt
"""
    robots = """
User-agent: GPTBot
Disallow: /

User-agent: YandexAdditional
Disallow: /
"""
    report = discoverability_checks.ai_txt_report(
        ai_content,
        robots_content=robots,
        llms_content="# Example llms.txt\n> https://example.com/ - Home\n",
    )
    assert report["status"] == "warn"
    assert any("robots.txt blocks" in item for item in report["contradictions"])


def test_schema_coverage_report_detects_missing_website_schema() -> None:
    html = """
    <html><head>
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Organization","name":"Example"}
    </script>
    </head><body></body></html>
    """
    report = discoverability_checks.schema_coverage_report(html, site_type="service")
    assert report["status"] == "warn"
    assert "WebSite" in report["missing_types"]
    assert "Service" in report["missing_types"]


def test_faq_detection_distinguishes_visible_and_schema_only_faq() -> None:
    html = """
    <html><head>
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"FAQPage"}
    </script>
    </head><body><p>No FAQ section visible.</p></body></html>
    """
    report = discoverability_checks.faq_detection_report(html)
    assert report["faq_schema_present"] is True
    assert report["status"] in {"warn", "needs-review"}
    assert any("visible FAQ" in item for item in report["warnings"])


def test_open_graph_report_flags_missing_and_generic_fields() -> None:
    html = """
    <html><head>
    <title>Home</title>
    <meta property="og:title" content="Home" />
    <meta property="og:description" content="Welcome" />
    <meta name="twitter:title" content="Home" />
    </head><body></body></html>
    """
    report = discoverability_checks.open_graph_report(html)
    assert report["status"] == "fail"
    assert "og:image" in report["missing_fields"]
    assert report["warnings"]


def test_technical_seo_report_detects_missing_signals() -> None:
    html = """
    <html><head>
    <title>Example</title>
    <meta name="description" content="Short example description" />
    <meta name="robots" content="index,follow" />
    </head><body><p>Example body copy only.</p></body></html>
    """
    report = discoverability_checks.technical_seo_report(
        html, "https://example.com/page"
    )
    assert report["status"] == "warn"
    assert any("Canonical URL is missing" in item for item in report["warnings"])


def test_robots_sitemap_report_warns_when_sitemap_exists_but_not_declared(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        discoverability_checks,
        "fetch_url_text",
        lambda url, timeout=15: (
            "User-agent: *\nAllow: /\n" if url.endswith("/robots.txt") else ""
        ),
    )
    monkeypatch.setattr(
        discoverability_checks,
        "fetch_url_bytes",
        lambda url, timeout=15: (
            b"<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'><url><loc>https://example.com/</loc></url></urlset>",
            "application/xml",
        ),
    )
    report = discoverability_checks.robots_sitemap_report(
        "https://example.com", sitemap_url="https://example.com/sitemap.xml"
    )
    assert report["status"] == "warn"
    assert any("not declared in robots.txt" in item for item in report["warnings"])


def test_scanner_summary_includes_v370_module_results(monkeypatch) -> None:
    class Row:
        id = 1
        normalized_url = "https://example.com"
        target_domain = "example.com"
        scan_mode = "passive"

    monkeypatch.setattr(
        scan_jobs,
        "_try_fetch_scanner_text",
        lambda url, settings: (
            "<html><head><title>Example</title>"
            '<meta property="og:title" content="Example" />'
            '<meta property="og:description" content="Example description" />'
            '<meta property="og:image" content="https://example.com/image.png" />'
            '<meta property="og:type" content="website" />'
            '<meta property="og:url" content="https://example.com" />'
            '<meta name="twitter:card" content="summary_large_image" />'
            '<meta name="twitter:title" content="Example" />'
            '<meta name="twitter:description" content="Example description" />'
            '<meta name="twitter:image" content="https://example.com/image.png" />'
            '<link rel="canonical" href="https://example.com/" />'
            '<link rel="alternate" hreflang="en" href="https://example.com/" />'
            '<script type="application/ld+json">{"@context":"https://schema.org","@type":["Organization","WebSite","BreadcrumbList"]}</script>'
            "</head><body><section id='faq'><h2>FAQ</h2><h3>What is this?</h3></section></body></html>",
            None,
        ),
    )
    monkeypatch.setattr(
        scan_jobs,
        "bots_report",
        lambda url: {
            "robots_url": f"{url}/robots.txt",
            "results": [
                {
                    "bot": "YandexBot",
                    "status": "allowed",
                    "matched_group": "YandexBot",
                    "detected_in": "robots group for YandexBot",
                    "recommendation": "Keep the policy explicit and documented.",
                    "kind": "search",
                    "why_it_matters": "search",
                },
                {
                    "bot": "YandexAdditional",
                    "status": "allowed",
                    "matched_group": "YandexAdditional",
                    "detected_in": "robots group for YandexAdditional",
                    "recommendation": "Keep the policy explicit and documented.",
                    "kind": "ai",
                    "why_it_matters": "ai",
                },
            ],
        },
    )
    monkeypatch.setattr(
        scan_jobs,
        "robots_sitemap_report",
        lambda url, sitemap_url=None: {
            "status": "pass",
            "robots_url": f"{url}/robots.txt",
            "declared_sitemaps": [sitemap_url or f"{url}/sitemap.xml"],
            "sitemap_results": [],
            "warnings": [],
        },
    )

    settings = type(
        "Settings",
        (),
        {
            "allow_public_intake": True,
            "allow_active_scan": True,
            "allow_anonymous_submission": True,
            "allow_full_scan": False,
            "scanner_allowed_scheme_list": lambda self: ["https"],
            "scanner_max_url_length": 2048,
            "scanner_max_concurrent_submissions_per_ip": 3,
        },
    )()
    summary = scan_jobs._build_summary(Row(), settings)
    monkeypatch.setattr(
        scan_jobs,
        "_scanner_runtime_settings",
        lambda: settings,
    )
    assert summary["schema_version"] == "v5.1.0"
    module_ids = {item["id"] for item in summary["module_results"]}
    assert {
        "ru_ai_bots",
        "robots_sitemap_linkage",
        "ai_txt",
        "ai_readability",
        "schema_coverage",
        "faq_answer_ready",
        "citability_score",
        "social_meta",
        "rag_chunk_readiness",
        "cdn_ai_bot_blocking",
        "technical_seo_basics",
    } <= module_ids
