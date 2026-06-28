from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Optional

from .scan_security import safe_fetch_url_bytes, safe_fetch_url_text

CHECKER_USER_AGENT = "Discoverability-Checks/6.9.0"
DEFAULT_TIMEOUT_SECONDS = 15

AI_BOTS = [
    {
        "name": "GPTBot",
        "kind": "ai",
        "why_it_matters": "Controls whether OpenAI training-oriented crawlers can access public content.",
    },
    {
        "name": "ChatGPT-User",
        "kind": "ai",
        "why_it_matters": "Represents user-triggered retrieval and browsing behavior for ChatGPT.",
    },
    {
        "name": "OAI-SearchBot",
        "kind": "ai",
        "why_it_matters": "OpenAI ties this crawler to ChatGPT Search inclusion and publisher controls.",
    },
    {
        "name": "PerplexityBot",
        "kind": "ai",
        "why_it_matters": "Can affect retrieval and citation visibility in answer engines.",
    },
    {
        "name": "ClaudeBot",
        "kind": "ai",
        "why_it_matters": "Affects whether Anthropic crawler/retrieval surfaces can reach public pages.",
    },
    {
        "name": "Google-Extended",
        "kind": "ai",
        "why_it_matters": "Separates Google AI training-use policy from classic Googlebot crawl policy.",
    },
    {
        "name": "Applebot-Extended",
        "kind": "ai",
        "why_it_matters": "Signals Apple extended AI usage control intent for public content.",
    },
    {
        "name": "Googlebot",
        "kind": "search",
        "why_it_matters": "Baseline search crawler policy still affects classic discoverability.",
    },
    {
        "name": "Bingbot",
        "kind": "search",
        "why_it_matters": "Bing crawl access remains part of the discoverability baseline.",
    },
    {
        "name": "YandexBot",
        "kind": "search",
        "why_it_matters": "Primary Yandex search crawler policy affects classic RU search visibility.",
    },
    {
        "name": "YandexAdditional",
        "kind": "ai",
        "why_it_matters": "YandexAdditional is used for Yandex Neuro and additional AI-related services separately from YandexBot.",
    },
]

AI_TXT_ALLOWED_DIRECTIVES = {
    "policy",
    "summary",
    "contact",
    "llms",
    "sitemap",
    "allow",
    "disallow",
    "notes",
    "preferred-agent",
}
AI_TXT_REQUIRED_DIRECTIVES = {"policy", "summary"}
SCHEMA_TEMPLATE_MAP = {
    "Organization": "templates/schema/organization-schema.json",
    "WebSite": "templates/schema/website-schema.json",
    "BreadcrumbList": "templates/schema/breadcrumb-schema.json",
    "FAQPage": "templates/schema/faq-schema.json",
    "Product": "templates/schema/product-schema.json",
    "Service": "templates/schema/service-schema.json",
    "LocalBusiness": "templates/schema/local-business-schema.json",
}
SITE_TYPE_REQUIREMENTS = {
    "saas": ["Organization", "WebSite", "BreadcrumbList", "Product", "Service"],
    "local-business": ["Organization", "WebSite", "BreadcrumbList", "LocalBusiness"],
    "service": ["Organization", "WebSite", "BreadcrumbList", "Service"],
    "ecommerce": ["Organization", "WebSite", "BreadcrumbList", "Product"],
    "content": ["Organization", "WebSite", "BreadcrumbList"],
}


def normalize_public_url(url: str, default_path: str = "") -> str:
    raw = url.strip()
    if not raw:
        raise ValueError("URL is required.")
    parsed = urllib.parse.urlparse(raw)
    if not parsed.scheme:
        raw = f"https://{raw}"
        parsed = urllib.parse.urlparse(raw)
    if not parsed.netloc:
        raise ValueError("URL must include a hostname.")
    normalized = parsed._replace(
        path=parsed.path or default_path, params="", fragment=""
    ).geturl()
    return normalized


def resolve_public_file_url(url: str, filename: str) -> str:
    normalized = normalize_public_url(url)
    parsed = urllib.parse.urlparse(normalized)
    if parsed.path.endswith(f"/{filename}") or parsed.path == f"/{filename}":
        return normalized
    base = (
        parsed._replace(path="", params="", query="", fragment="").geturl().rstrip("/")
    )
    return f"{base}/{filename}"


def fetch_url_text(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    settings = _runtime_settings()
    content, _final_url, _redirect_chain = safe_fetch_url_text(
        url,
        settings,
        timeout=timeout,
        headers={"User-Agent": CHECKER_USER_AGENT},
    )
    return content


def fetch_url_bytes(
    url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> tuple[bytes, str]:
    settings = _runtime_settings()
    body, content_type, _final_url, _redirect_chain = safe_fetch_url_bytes(
        url,
        settings,
        timeout=timeout,
        headers={"User-Agent": CHECKER_USER_AGENT},
    )
    return body, content_type


def try_fetch_url_text(url: str) -> tuple[Optional[str], Optional[str]]:
    try:
        return fetch_url_text(url), None
    except (urllib.error.URLError, ValueError, RuntimeError) as exc:
        return None, str(exc)


def _runtime_settings():
    from ..config import load_settings

    return load_settings()


@dataclass
class HtmlAnalysis:
    title: str
    meta_tags: dict[str, str]
    link_tags: list[dict[str, str]]
    headings: list[str]
    text_blocks: list[str]
    section_markers: list[str]
    visibility_markers: list[str]
    json_ld_nodes: list[dict | list]
    question_like_headings: list[str]


class _HTMLSignalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_tags: dict[str, str] = {}
        self.link_tags: list[dict[str, str]] = []
        self.headings: list[str] = []
        self.text_blocks: list[str] = []
        self.section_markers: list[str] = []
        self.visibility_markers: list[str] = []
        self.json_ld_nodes: list[dict | list] = []
        self.question_like_headings: list[str] = []
        self._ignored_depth = 0
        self._current_title: list[str] = []
        self._current_heading_tag: Optional[str] = None
        self._current_heading_text: list[str] = []
        self._current_script_type: Optional[str] = None
        self._current_script: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attrs_map = {key.lower(): (value or "") for key, value in attrs}
        if tag in {"script", "style", "noscript"}:
            if (
                tag == "script"
                and attrs_map.get("type", "").lower() == "application/ld+json"
            ):
                self._current_script_type = "application/ld+json"
                self._current_script = []
            else:
                self._ignored_depth += 1
        if tag == "title":
            self._current_title = []
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._current_heading_tag = tag
            self._current_heading_text = []
        if tag == "meta":
            key = attrs_map.get("property") or attrs_map.get("name")
            value = attrs_map.get("content", "").strip()
            if key and value:
                self.meta_tags[key.lower()] = value
        if tag == "link":
            rel = attrs_map.get("rel", "").strip().lower()
            href = attrs_map.get("href", "").strip()
            hreflang = attrs_map.get("hreflang", "").strip().lower()
            if rel and href:
                self.link_tags.append({"rel": rel, "href": href, "hreflang": hreflang})
        marker = " ".join(
            part
            for part in [attrs_map.get("id", ""), attrs_map.get("class", "")]
            if part
        ).lower()
        if marker and any(
            token in marker
            for token in ["faq", "accordion", "question", "answer", "qa"]
        ):
            self.section_markers.append(marker)
        if marker and any(
            token in marker
            for token in [
                "sr-only",
                "sronly",
                "visually-hidden",
                "screen-reader",
                "screenreader",
                "sr_only",
            ]
        ):
            self.visibility_markers.append(marker)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "title":
            self.title = " ".join(
                part.strip() for part in self._current_title if part.strip()
            ).strip()
            self._current_title = []
        if tag == self._current_heading_tag:
            heading = " ".join(
                part.strip() for part in self._current_heading_text if part.strip()
            ).strip()
            if heading:
                self.headings.append(heading)
                if "?" in heading or heading.lower().startswith(
                    ("what ", "how ", "why ", "when ", "can ", "is ", "are ")
                ):
                    self.question_like_headings.append(heading)
            self._current_heading_tag = None
            self._current_heading_text = []
        if tag == "script" and self._current_script_type == "application/ld+json":
            raw = "".join(self._current_script).strip()
            if raw:
                try:
                    self.json_ld_nodes.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
            self._current_script_type = None
            self._current_script = []

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._current_script_type == "application/ld+json":
            self._current_script.append(data)
            return
        if self._current_heading_tag:
            self._current_heading_text.append(text)
        elif self.lasttag == "title":
            self._current_title.append(text)
        elif len(text) > 20:
            self.text_blocks.append(text)


def analyze_html(html: str) -> HtmlAnalysis:
    parser = _HTMLSignalParser()
    parser.feed(html)
    return HtmlAnalysis(
        title=parser.title,
        meta_tags=parser.meta_tags,
        link_tags=parser.link_tags,
        headings=parser.headings,
        text_blocks=parser.text_blocks,
        section_markers=parser.section_markers,
        visibility_markers=parser.visibility_markers,
        json_ld_nodes=parser.json_ld_nodes,
        question_like_headings=parser.question_like_headings,
    )


def _flatten_schema_types(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        value = node.get("@type")
        if isinstance(value, str):
            found.append(value)
        elif isinstance(value, list):
            found.extend(item for item in value if isinstance(item, str))
        for nested in node.values():
            found.extend(_flatten_schema_types(nested))
    elif isinstance(node, list):
        for item in node:
            found.extend(_flatten_schema_types(item))
    return found


def schema_coverage_report(
    html: str,
    *,
    site_type: Optional[str] = None,
) -> dict:
    analysis = analyze_html(html)
    found_types = sorted(
        {
            item
            for node in analysis.json_ld_nodes
            for item in _flatten_schema_types(node)
        }
    )
    baseline = ["Organization", "WebSite", "BreadcrumbList"]
    required = baseline.copy()
    if site_type in SITE_TYPE_REQUIREMENTS:
        required = SITE_TYPE_REQUIREMENTS[site_type]
    missing = [item for item in required if item not in found_types]
    warnings: list[str] = []
    if not found_types:
        warnings.append("No JSON-LD schema was detected in the page source.")
    elif (
        "FAQPage" in found_types
        and not any(
            "faq" in marker or "question" in marker
            for marker in analysis.section_markers
        )
        and not analysis.question_like_headings
    ):
        warnings.append(
            "FAQPage schema exists but visible FAQ or Q&A evidence is weak."
        )
    recommendations = []
    for item in missing:
        recommendations.append(
            {
                "schema_type": item,
                "template": SCHEMA_TEMPLATE_MAP[item],
                "message": f"Add or improve {item} schema coverage for this page/site type.",
            }
        )
    return {
        "status": "pass"
        if not missing and not warnings
        else "warn"
        if found_types
        else "fail",
        "site_type": site_type or "unspecified",
        "found_types": found_types,
        "missing_types": missing,
        "warnings": warnings,
        "recommendations": recommendations,
    }


def faq_detection_report(html: str) -> dict:
    analysis = analyze_html(html)
    question_like = analysis.question_like_headings
    faq_markers = [
        marker
        for marker in analysis.section_markers
        if any(
            token in marker
            for token in ["faq", "accordion", "question", "answer", "qa"]
        )
    ]
    faq_headings = [
        heading
        for heading in analysis.headings
        if any(
            token in heading.lower()
            for token in ["faq", "frequently asked", "вопрос", "ответ"]
        )
    ]
    schema_types = {
        item for node in analysis.json_ld_nodes for item in _flatten_schema_types(node)
    }
    visible_count = len(faq_headings) + len(question_like) + len(faq_markers)
    warnings: list[str] = []
    if "FAQPage" in schema_types and visible_count == 0:
        warnings.append(
            "FAQPage schema exists but visible FAQ/Q&A content was not detected."
        )
    if visible_count == 0:
        warnings.append("No strong FAQ or answer-ready pattern was detected.")
    confidence = (
        "high" if visible_count >= 3 else "medium" if visible_count >= 1 else "low"
    )
    return {
        "status": "pass"
        if visible_count >= 2
        else "needs-review"
        if visible_count == 1
        else "warn",
        "confidence": confidence,
        "visible_faq_headings": faq_headings,
        "question_like_headings": question_like,
        "accordion_markers": faq_markers,
        "faq_schema_present": "FAQPage" in schema_types,
        "warnings": warnings,
        "recommendation": (
            "Add or strengthen visible FAQ or answer-ready blocks on high-value pages."
            if visible_count == 0
            else "Review whether the detected Q&A pattern is strong enough for citation-oriented surfaces."
        ),
        "limitation": "This detector is heuristic and may miss custom UI patterns or generate false positives.",
    }


def ai_readability_report(html: str, *, page_url: Optional[str] = None) -> dict:
    analysis = analyze_html(html)
    warnings: list[str] = []
    experimental_notes: list[str] = []
    detected_layers: list[str] = []
    quick_wins: list[str] = []

    if analysis.title:
        detected_layers.append("descriptive_title")
    else:
        warnings.append("Page title is missing.")
        quick_wins.append("Add a specific, descriptive page title.")

    if analysis.meta_tags.get("description"):
        detected_layers.append("meta_description")
    else:
        warnings.append("Meta description is missing.")
        quick_wins.append("Add a concise meta description with the page promise.")

    if analysis.visibility_markers:
        detected_layers.append("screen_reader_support")
    else:
        experimental_notes.append(
            "No sr-only or visually-hidden support markers were detected. This is an optional accessibility or parsing signal, not a standard search requirement."
        )

    schema = schema_coverage_report(html)
    if schema["found_types"]:
        detected_layers.append("structured_data")
    else:
        warnings.append("No structured data was detected.")
        quick_wins.append("Publish baseline JSON-LD such as Organization and WebSite.")

    faq = faq_detection_report(html)
    if faq["status"] in {"pass", "needs-review"}:
        detected_layers.append("answer_ready_blocks")
    else:
        warnings.append("Visible FAQ or answer-ready formatting is weak.")
        quick_wins.append("Add visible Q&A or answer-ready blocks on important pages.")

    remote_assets: dict[str, str] = {}
    if page_url:
        reasoning_url = resolve_public_file_url(page_url, "reasoning.json")
        manifest_url = resolve_public_file_url(
            f"{normalize_public_url(page_url).rstrip('/')}/.well-known/ai-manifest.json",
            "ai-manifest.json",
        )
        reasoning_body, reasoning_error = try_fetch_url_text(reasoning_url)
        manifest_body, manifest_error = try_fetch_url_text(manifest_url)
        remote_assets["reasoning_json"] = "present" if reasoning_body else "missing"
        remote_assets["ai_manifest"] = "present" if manifest_body else "missing"
        if reasoning_body:
            detected_layers.append("reasoning_json")
        else:
            experimental_notes.append(
                f"reasoning.json is not publicly available: {reasoning_error or 'missing'}"
            )
            quick_wins.append(
                "Consider publishing reasoning.json only if your operating model depends on explicit non-standard AI guidance."
            )
        if manifest_body:
            detected_layers.append("ai_manifest")
        else:
            experimental_notes.append(
                f".well-known/ai-manifest.json is not publicly available: {manifest_error or 'missing'}"
            )
            quick_wins.append(
                "Consider publishing .well-known/ai-manifest.json only if your workflow needs extra machine-readable AI guidance."
            )

    score = 0
    score += 20 if analysis.title else 0
    score += 15 if analysis.meta_tags.get("description") else 0
    score += 5 if analysis.visibility_markers else 0
    score += 25 if schema["found_types"] else 0
    score += 20 if faq["status"] in {"pass", "needs-review"} else 0
    score += 5 if remote_assets.get("reasoning_json") == "present" else 0
    score += 5 if remote_assets.get("ai_manifest") == "present" else 0

    status = (
        "pass"
        if score >= 75 and not warnings[:2]
        else "warn"
        if score >= 45
        else "fail"
    )
    return {
        "status": status,
        "score": score,
        "detected_layers": detected_layers,
        "missing_layers": [
            layer
            for layer in [
                "descriptive_title",
                "meta_description",
                "screen_reader_support",
                "structured_data",
                "answer_ready_blocks",
                "reasoning_json",
                "ai_manifest",
            ]
            if layer not in detected_layers
        ],
        "warnings": warnings,
        "experimental_notes": experimental_notes,
        "quick_wins": quick_wins[:5],
        "remote_assets": remote_assets,
        "recommendation": "Tighten page structure, schema, and visible answer-ready formatting first; treat non-standard AI guidance files as optional extras rather than universal ranking signals.",
        "limitation": "This audit is heuristic and cannot prove how a specific model, search engine, or retrieval stack will parse the page.",
    }


def open_graph_report(html: str) -> dict:
    analysis = analyze_html(html)
    meta = analysis.meta_tags
    required = {
        "og:title": meta.get("og:title"),
        "og:description": meta.get("og:description"),
        "og:image": meta.get("og:image"),
        "og:type": meta.get("og:type"),
        "og:url": meta.get("og:url"),
        "twitter:card": meta.get("twitter:card"),
        "twitter:title": meta.get("twitter:title"),
        "twitter:description": meta.get("twitter:description"),
        "twitter:image": meta.get("twitter:image"),
    }
    missing = [key for key, value in required.items() if not value]
    warnings: list[str] = []
    generic_markers = ["home", "welcome", "default", "untitled", "page"]
    for key, value in required.items():
        if not value:
            continue
        lowered = value.lower()
        if len(value.strip()) < 5:
            warnings.append(f"{key} looks too short to be useful.")
        if any(
            marker == lowered.strip() or lowered.startswith(f"{marker} ")
            for marker in generic_markers
        ):
            warnings.append(f"{key} looks generic and may weaken preview quality.")
    if meta.get("og:title") and analysis.title:
        if meta["og:title"].strip() == analysis.title.strip():
            warnings.append(
                "og:title is identical to the page <title>; review whether it is too generic."
            )
    status = (
        "pass" if not missing and not warnings else "warn" if not missing else "fail"
    )
    return {
        "status": status,
        "fields": required,
        "missing_fields": missing,
        "warnings": warnings,
        "recommendation": "Complete missing Open Graph and Twitter Card fields and review generic previews.",
    }


def rag_chunk_readiness_report(html: str) -> dict:
    analysis = analyze_html(html)
    blocks = [block.strip() for block in analysis.text_blocks if block.strip()]
    long_blocks = [block for block in blocks if len(block) > 1200]
    short_headings = [heading for heading in analysis.headings if len(heading) < 6]
    definition_signals = [
        block
        for block in blocks
        if any(
            token in block.lower()
            for token in [" is ", " means ", " refers to ", " defined as ", " это "]
        )
    ]
    warnings: list[str] = []
    if len(analysis.headings) < 2:
        warnings.append("Heading structure is shallow for chunk-friendly parsing.")
    if long_blocks:
        warnings.append("Some content sections look too long for clean RAG chunking.")
    if short_headings:
        warnings.append("Some headings are too short to anchor semantic chunk titles.")
    if not definition_signals:
        warnings.append("Definition-like explanatory blocks are weak or missing.")

    avg_block_length = (
        int(sum(len(block) for block in blocks) / len(blocks)) if blocks else 0
    )
    status = (
        "pass"
        if not warnings
        else "warn"
        if analysis.headings and avg_block_length < 1400
        else "fail"
    )
    return {
        "status": status,
        "heading_count": len(analysis.headings),
        "text_block_count": len(blocks),
        "average_block_length": avg_block_length,
        "long_block_count": len(long_blocks),
        "definition_signal_count": len(definition_signals),
        "warnings": warnings,
        "recommendation": "Break long sections into tighter heading-led blocks and add explicit definition-style sentences where concepts matter.",
        "limitation": "Chunk readiness is inferred from rendered HTML text, not from your real downstream embedding or retrieval pipeline.",
    }


def citability_score_report(
    html: str,
    *,
    page_url: Optional[str] = None,
    site_type: Optional[str] = None,
) -> dict:
    schema = schema_coverage_report(html, site_type=site_type)
    faq = faq_detection_report(html)
    social = open_graph_report(html)
    technical = technical_seo_report(html, page_url or "https://example.com/")
    readability = ai_readability_report(html, page_url=page_url)

    checks = [
        (
            "title_and_description",
            10,
            bool(technical["title"] and technical["meta_description"]),
        ),
        ("canonical", 10, bool(technical["canonical_url"])),
        ("hreflang_or_locale", 5, bool(technical["hreflang_refs"])),
        ("schema_baseline", 20, bool(schema["found_types"])),
        ("faq_answer_ready", 10, faq["status"] in {"pass", "needs-review"}),
        ("social_metadata", 10, not social["missing_fields"]),
        ("ai_readability", 15, readability["score"] >= 60),
        ("clean_technical_baseline", 10, len(technical["warnings"]) <= 1),
        (
            "definition_and_chunking",
            10,
            rag_chunk_readiness_report(html)["status"] in {"pass", "warn"},
        ),
    ]
    if page_url:
        ai_txt_url = resolve_public_file_url(page_url, "ai.txt")
        llms_url = resolve_public_file_url(page_url, "llms.txt")
        ai_content, _ai_error = try_fetch_url_text(ai_txt_url)
        llms_content, _llms_error = try_fetch_url_text(llms_url)
        checks.append(("ai_guidance_files", 10, bool(ai_content or llms_content)))

    score = sum(weight for _name, weight, passed in checks if passed)
    quick_wins: list[str] = []
    if not technical["canonical_url"]:
        quick_wins.append("Add a canonical URL.")
    if schema["missing_types"]:
        quick_wins.append("Complete missing JSON-LD schema coverage.")
    if social["missing_fields"]:
        quick_wins.append("Fill missing Open Graph and Twitter Card fields.")
    if faq["status"] == "warn":
        quick_wins.append("Add visible Q&A or FAQ formatting.")
    if readability["missing_layers"]:
        quick_wins.append("Improve AI-readable structure and guidance layers.")

    status = "pass" if score >= 75 else "warn" if score >= 45 else "fail"
    return {
        "status": status,
        "score": score,
        "max_score": sum(weight for _name, weight, _passed in checks),
        "breakdown": [
            {"check": name, "weight": weight, "passed": passed}
            for name, weight, passed in checks
        ],
        "quick_wins": quick_wins[:5],
        "recommendation": "Raise citation probability by tightening technical clarity, machine-readable facts, and answer-ready formatting on money pages.",
        "limitation": "This score is a directional proxy for citation readiness, not a guarantee of mentions across volatile AI surfaces.",
    }


def _probe_public_url(url: str, user_agent: str) -> dict:
    from .scan_security import normalize_public_url as secure_normalize_public_url

    settings = _runtime_settings()
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    current_url = secure_normalize_public_url(url, settings)
    request = urllib.request.Request(
        current_url,
        headers={"User-Agent": user_agent},
        method="GET",
    )
    try:
        with opener.open(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            final_url = secure_normalize_public_url(response.geturl(), settings)
            return {
                "status_code": response.getcode(),
                "final_url": final_url,
                "headers": headers,
                "blocked": False,
            }
    except urllib.error.HTTPError as exc:
        headers = {key.lower(): value for key, value in exc.headers.items()}
        return {
            "status_code": exc.code,
            "final_url": current_url,
            "headers": headers,
            "blocked": exc.code in {401, 403, 406, 429, 503},
        }


def _detect_cdn(headers: dict[str, str]) -> str:
    joined = " ".join(f"{key}:{value}" for key, value in headers.items()).lower()
    if "cloudflare" in joined or "cf-ray" in headers:
        return "cloudflare"
    if "cloudfront" in joined or "x-amz-cf-id" in headers:
        return "cloudfront"
    if "fastly" in joined:
        return "fastly"
    if "akamai" in joined:
        return "akamai"
    return "unknown"


def cdn_ai_blocking_report(page_url: str) -> dict:
    probes = []
    for bot in ["GPTBot", "ClaudeBot", "PerplexityBot"]:
        probe = _probe_public_url(page_url, bot)
        probe["bot"] = bot
        probes.append(probe)
    detected_cdn = _detect_cdn(probes[0]["headers"] if probes else {})
    blocked = [probe["bot"] for probe in probes if probe["blocked"]]
    warnings: list[str] = []
    if blocked:
        warnings.append(
            f"Potential CDN or edge blocking detected for: {', '.join(blocked)}."
        )
    if detected_cdn == "unknown":
        warnings.append(
            "Could not confidently identify a CDN or edge layer from response headers."
        )
    return {
        "status": "warn" if blocked or detected_cdn == "unknown" else "pass",
        "detected_cdn": detected_cdn,
        "probes": probes,
        "warnings": warnings,
        "recommendation": "Review CDN, WAF, and bot-management rules to ensure public AI crawlers are not blocked by accident.",
        "limitation": "A successful or blocked probe does not prove long-term bot treatment across every edge path or challenge mode.",
    }


def technical_seo_report(html: str, page_url: str) -> dict:
    analysis = analyze_html(html)
    meta = analysis.meta_tags
    parsed = urllib.parse.urlparse(page_url)
    base_host = parsed.hostname or ""

    canonical_url = (
        next(
            (
                item["href"]
                for item in analysis.link_tags
                if item.get("rel") == "canonical"
            ),
            "",
        )
        or meta.get("canonical")
        or meta.get("og:url")
        or ""
    )
    hreflang_refs = [
        {"lang": item["hreflang"], "href": item["href"]}
        for item in analysis.link_tags
        if item.get("hreflang")
    ] + [
        {
            "lang": key.split(":", 1)[1],
            "href": value,
        }
        for key, value in meta.items()
        if key.startswith("hreflang:")
    ]

    internal_links = [
        block for block in analysis.text_blocks if base_host and base_host in block
    ]
    heading_count = len(analysis.headings)
    h1_count = (
        len(
            [
                heading
                for heading in analysis.headings
                if heading == analysis.headings[0]
            ]
        )
        if analysis.headings
        else 0
    )
    title = analysis.title.strip()
    description = meta.get("description", "").strip()
    warnings: list[str] = []

    if not canonical_url:
        warnings.append("Canonical URL is missing from public metadata.")
    elif base_host and base_host not in canonical_url:
        warnings.append("Canonical URL points to a different host.")
    if not hreflang_refs:
        warnings.append("No hreflang references were detected.")
    if not title:
        warnings.append("Page title is missing.")
    if not description:
        warnings.append("Meta description is missing.")
    if heading_count == 0:
        warnings.append("No visible heading structure was detected.")
    if len(internal_links) == 0:
        warnings.append("Internal linking evidence is weak in the extracted HTML text.")
    if "noindex" in meta.get("robots", "").lower():
        warnings.append("Robots meta includes noindex.")

    return {
        "status": "pass" if not warnings else "warn",
        "canonical_url": canonical_url,
        "hreflang_refs": hreflang_refs,
        "robots_meta": meta.get("robots", ""),
        "title": title,
        "meta_description": description,
        "heading_count": heading_count,
        "h1_count": h1_count,
        "internal_link_count": len(internal_links),
        "warnings": warnings,
        "recommendation": (
            "Tighten canonical, hreflang, metadata, and internal linking signals before treating the page as AI-ready."
        ),
        "limitation": (
            "This lightweight technical SEO pass is heuristic and does not replace a full crawler-based site audit."
        ),
    }


def parse_robots_groups(content: str) -> list[dict[str, list[str] | list[str]]]:
    groups: list[dict[str, list[str] | list[str]]] = []
    current: Optional[dict[str, list[str] | list[str]]] = None
    seen_rules_in_group = False
    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        key_lower = key.lower()
        if key_lower == "user-agent":
            if current is None or seen_rules_in_group:
                current = {"agents": [], "allow": [], "disallow": []}
                groups.append(current)
                seen_rules_in_group = False
            cast_agents = current["agents"]
            assert isinstance(cast_agents, list)
            cast_agents.append(value)
            continue
        if current is None:
            continue
        if key_lower == "allow":
            cast = current["allow"]
            assert isinstance(cast, list)
            cast.append(value)
            seen_rules_in_group = True
        elif key_lower == "disallow":
            cast = current["disallow"]
            assert isinstance(cast, list)
            cast.append(value)
            seen_rules_in_group = True
    merged: dict[str, dict[str, list[str] | list[str]]] = {}
    for group in groups:
        agents = group["agents"]
        assert isinstance(agents, list)
        for agent in agents:
            bucket = merged.setdefault(
                agent,
                {"agents": [agent], "allow": [], "disallow": []},
            )
            for key in ["allow", "disallow"]:
                source = group[key]
                target = bucket[key]
                assert isinstance(source, list) and isinstance(target, list)
                target.extend(source)
    return list(merged.values())


def _bot_matches_agent(bot_name: str, agent: str) -> bool:
    bot = bot_name.lower()
    value = agent.lower()
    return value == "*" or bot == value or bot.startswith(value)


def _matching_group_for_bot(
    groups: list[dict[str, list[str] | list[str]]], bot_name: str
) -> Optional[dict[str, list[str] | list[str]]]:
    matches: list[tuple[int, dict[str, list[str] | list[str]], str]] = []
    for group in groups:
        agents = group["agents"]
        assert isinstance(agents, list)
        for agent in agents:
            if _bot_matches_agent(bot_name, agent):
                matches.append((0 if agent == "*" else len(agent), group, agent))
    if not matches:
        return None
    matches.sort(key=lambda item: item[0], reverse=True)
    best_group = matches[0][1].copy()
    best_group["matched_agent"] = matches[0][2]
    return best_group


def _best_rule_length(paths: list[str], default_when_empty: int = -1) -> int:
    matched = [len(path) for path in paths if path]
    if not matched:
        return default_when_empty
    return max(matched)


def evaluate_bot_policy(
    groups: list[dict[str, list[str] | list[str]]], bot_name: str
) -> dict:
    target = _matching_group_for_bot(groups, bot_name)
    if target is None:
        return {
            "bot": bot_name,
            "status": "unspecified",
            "matched_group": None,
            "detected_in": "no matching group",
            "recommendation": "Add an explicit rule if this bot matters to your discoverability strategy.",
        }
    allows = target["allow"]
    disallows = target["disallow"]
    assert isinstance(allows, list) and isinstance(disallows, list)
    status = "unspecified"
    allow_length = _best_rule_length(allows)
    disallow_length = _best_rule_length(disallows)
    if disallow_length > allow_length and disallow_length >= 0:
        status = "blocked"
    elif allow_length >= 0:
        status = "allowed"
    return {
        "bot": bot_name,
        "status": status,
        "matched_group": target.get("matched_agent"),
        "detected_in": f"robots group for {target.get('matched_agent')}",
        "recommendation": (
            "Keep the policy explicit and documented."
            if status != "unspecified"
            else "Clarify whether this bot should reach public citation and trust surfaces."
        ),
    }


def extract_sitemap_urls(
    robots_content: str, robots_url: Optional[str] = None
) -> list[str]:
    urls: list[str] = []
    base = robots_url or ""
    for raw_line in robots_content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line.lower().startswith("sitemap:"):
            continue
        _, value = line.split(":", 1)
        sitemap = value.strip()
        if sitemap and sitemap.startswith("/"):
            parsed = urllib.parse.urlparse(base)
            sitemap = f"{parsed.scheme}://{parsed.netloc}{sitemap}"
        if sitemap:
            urls.append(sitemap)
    return urls


def analyze_sitemap_url(sitemap_url: str) -> dict:
    try:
        body, content_type = fetch_url_bytes(sitemap_url)
        root = ET.fromstring(body)
        loc_count = len(root.findall(".//{*}loc"))
        root_tag = root.tag.rsplit("}", 1)[-1]
        plausible = root_tag in {"urlset", "sitemapindex"}
        return {
            "url": sitemap_url,
            "status": "pass" if plausible else "warn",
            "content_type": content_type,
            "root_tag": root_tag,
            "loc_count": loc_count,
            "message": (
                "Sitemap is reachable and parseable."
                if plausible
                else "The URL is reachable but does not look like a standard sitemap root."
            ),
        }
    except (urllib.error.URLError, ET.ParseError, ValueError) as exc:
        return {
            "url": sitemap_url,
            "status": "fail",
            "content_type": "",
            "root_tag": None,
            "loc_count": 0,
            "message": f"Sitemap could not be validated: {exc}",
        }


def robots_sitemap_report(site_url: str, *, sitemap_url: Optional[str] = None) -> dict:
    robots_url = resolve_public_file_url(site_url, "robots.txt")
    robots_content = fetch_url_text(robots_url)
    declared = extract_sitemap_urls(robots_content, robots_url)
    sitemap_results = [analyze_sitemap_url(url) for url in declared]
    warnings: list[str] = []
    if not declared:
        warnings.append("No Sitemap: entry was declared in robots.txt.")
    if sitemap_url and sitemap_url not in declared:
        explicit_result = analyze_sitemap_url(sitemap_url)
        sitemap_results.append(explicit_result)
        if explicit_result["status"] == "pass":
            warnings.append(
                "A reachable sitemap exists but is not declared in robots.txt."
            )
    failed = [item for item in sitemap_results if item["status"] == "fail"]
    status = "pass"
    if warnings or failed:
        status = "warn" if sitemap_results else "fail"
    if failed and not declared:
        status = "fail"
    return {
        "status": status,
        "robots_url": robots_url,
        "declared_sitemaps": declared,
        "sitemap_results": sitemap_results,
        "warnings": warnings,
    }


def bots_report(site_url: str) -> dict:
    robots_url = resolve_public_file_url(site_url, "robots.txt")
    content = fetch_url_text(robots_url)
    groups = parse_robots_groups(content)
    results = []
    for bot in AI_BOTS:
        policy = evaluate_bot_policy(groups, bot["name"])
        policy["kind"] = bot["kind"]
        policy["why_it_matters"] = bot["why_it_matters"]
        results.append(policy)
    return {"robots_url": robots_url, "results": results}


def parse_ai_txt(content: str) -> dict:
    directives: dict[str, list[str]] = {}
    warnings: list[str] = []
    unknown_directives: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            warnings.append(f"Malformed line without directive separator: {stripped}")
            continue
        key, value = [part.strip() for part in stripped.split(":", 1)]
        normalized_key = key.lower()
        directives.setdefault(normalized_key, []).append(value)
        if normalized_key not in AI_TXT_ALLOWED_DIRECTIVES:
            unknown_directives.append(normalized_key)
    missing = sorted(AI_TXT_REQUIRED_DIRECTIVES - directives.keys())
    if unknown_directives:
        warnings.append(
            "Unknown directives found: " + ", ".join(sorted(set(unknown_directives)))
        )
    if missing:
        warnings.append("Missing recommended directives: " + ", ".join(missing))
    return {
        "directives": directives,
        "warnings": warnings,
        "missing_directives": missing,
        "unknown_directives": sorted(set(unknown_directives)),
    }


def ai_txt_report(
    content: str,
    *,
    robots_content: Optional[str] = None,
    llms_content: Optional[str] = None,
) -> dict:
    parsed = parse_ai_txt(content)
    directives = parsed["directives"]
    contradictions: list[str] = []
    if robots_content:
        groups = parse_robots_groups(robots_content)
        ai_blocked = [
            policy["bot"]
            for policy in (
                evaluate_bot_policy(groups, bot["name"])
                for bot in AI_BOTS
                if bot["kind"] == "ai"
            )
            if policy["status"] == "blocked"
        ]
        ai_allows = directives.get("allow", [])
        if "/" in ai_allows and ai_blocked:
            contradictions.append(
                "ai.txt suggests broad AI access but robots.txt blocks: "
                + ", ".join(ai_blocked)
            )
    if llms_content is not None:
        llms_refs = directives.get("llms", [])
        if not llms_content.strip():
            contradictions.append(
                "ai.txt references AI guidance but llms.txt is missing or empty."
            )
        elif not llms_refs:
            contradictions.append(
                "ai.txt does not reference llms.txt explicitly; review whether the relationship should be documented."
            )
    status = "pass"
    if parsed["missing_directives"] or contradictions:
        status = "warn"
    if not directives:
        status = "fail"
    return {
        "status": status,
        "directives": directives,
        "warnings": parsed["warnings"],
        "contradictions": contradictions,
        "recommendations": [
            "Keep ai.txt short, explicit, and aligned with robots.txt and llms.txt.",
            "Avoid contradictory access guidance across AI-facing files.",
        ],
    }


def crux_field_data_report(payload: dict) -> dict:
    record = payload.get("record") if isinstance(payload, dict) else {}
    key = "urlNormalizationDetails"
    normalized = (record or {}).get(key) or {}
    metrics = (record or {}).get("metrics") or payload.get("metrics") or {}
    extracted = {}
    warnings: list[str] = []
    for metric_name in [
        "largest_contentful_paint",
        "interaction_to_next_paint",
        "cumulative_layout_shift",
    ]:
        metric_payload = metrics.get(metric_name) or {}
        percentiles = metric_payload.get("percentiles") or {}
        p75 = percentiles.get("p75")
        if p75 is None:
            warnings.append(f"{metric_name} p75 is missing from the CrUX payload.")
        extracted[metric_name] = {
            "p75": p75,
            "good_threshold": (
                2500
                if metric_name == "largest_contentful_paint"
                else 200
                if metric_name == "interaction_to_next_paint"
                else 0.1
            ),
        }
    return {
        "status": "pass"
        if extracted and not warnings
        else "warn"
        if extracted
        else "fail",
        "collection_scope": normalized.get("originalUrl")
        or payload.get("url")
        or "unknown",
        "metrics": extracted,
        "warnings": warnings,
        "recommendation": "Use field data as the real-user performance layer alongside synthetic audits and release gating.",
        "limitation": "CrUX data is aggregated and lagging; it is not a real-time per-release truth source.",
    }


def classify_finding_status(status: str) -> str:
    if status in {"pass", "info", "warn", "fail", "needs-review"}:
        return status
    return "needs-review"
