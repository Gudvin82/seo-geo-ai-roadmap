from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Optional

CHECKER_USER_AGENT = "Discoverability-Checks/3.7.0"
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
    request = urllib.request.Request(url, headers={"User-Agent": CHECKER_USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_url_bytes(
    url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": CHECKER_USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        return response.read(), content_type


def try_fetch_url_text(url: str) -> tuple[Optional[str], Optional[str]]:
    try:
        return fetch_url_text(url), None
    except (urllib.error.URLError, ValueError) as exc:
        return None, str(exc)


@dataclass
class HtmlAnalysis:
    title: str
    meta_tags: dict[str, str]
    headings: list[str]
    text_blocks: list[str]
    section_markers: list[str]
    json_ld_nodes: list[dict | list]
    question_like_headings: list[str]


class _HTMLSignalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_tags: dict[str, str] = {}
        self.headings: list[str] = []
        self.text_blocks: list[str] = []
        self.section_markers: list[str] = []
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
        headings=parser.headings,
        text_blocks=parser.text_blocks,
        section_markers=parser.section_markers,
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


def parse_robots_groups(content: str) -> list[dict[str, list[str] | str]]:
    groups: list[dict[str, list[str] | str]] = []
    current: Optional[dict[str, list[str] | str]] = None
    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        key_lower = key.lower()
        if key_lower == "user-agent":
            current = {"agent": value, "allow": [], "disallow": []}
            groups.append(current)
            continue
        if current is None:
            continue
        if key_lower == "allow":
            cast = current["allow"]
            assert isinstance(cast, list)
            cast.append(value)
        elif key_lower == "disallow":
            cast = current["disallow"]
            assert isinstance(cast, list)
            cast.append(value)
    merged: dict[str, dict[str, list[str] | str]] = {}
    for group in groups:
        agent = str(group["agent"])
        bucket = merged.setdefault(agent, {"agent": agent, "allow": [], "disallow": []})
        for key in ["allow", "disallow"]:
            source = group[key]
            target = bucket[key]
            assert isinstance(source, list) and isinstance(target, list)
            target.extend(source)
    return list(merged.values())


def evaluate_bot_policy(
    groups: list[dict[str, list[str] | str]], bot_name: str
) -> dict:
    exact = next(
        (group for group in groups if str(group["agent"]).lower() == bot_name.lower()),
        None,
    )
    wildcard = next((group for group in groups if str(group["agent"]) == "*"), None)
    target = exact or wildcard
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
    if "/" in disallows and "/" not in allows:
        status = "blocked"
    elif "/" in allows:
        status = "allowed"
    return {
        "bot": bot_name,
        "status": status,
        "matched_group": target["agent"],
        "detected_in": f"robots group for {target['agent']}",
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


def classify_finding_status(status: str) -> str:
    if status in {"pass", "info", "warn", "fail", "needs-review"}:
        return status
    return "needs-review"
