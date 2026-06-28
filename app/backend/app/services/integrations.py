from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .script_runner import run_script

CONTRACT_VERSION = "v6.7.0"

INTEGRATION_CONTRACTS: dict[str, dict[str, Any]] = {
    "gsc": {
        "source_type": "gsc",
        "label": "Google Search Console",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GSC_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "scheduled sync",
            "artifact export",
            "drift comparison",
            "report regeneration",
        ],
        "production_flow": [
            "connect service account secret",
            "run first manual sync",
            "review imported snapshot",
            "promote to scheduled GitHub Action or scheduled check",
            "use executive dashboard and compare flows for regression gating",
        ],
        "capabilities": [
            "top queries import",
            "top pages import",
            "search visibility baseline",
            "report attachment",
        ],
        "next_step": "Connect a service account secret, sync manually once, then move it into GitHub Actions or scheduled checks.",
    },
    "ga4": {
        "source_type": "ga4",
        "label": "Google Analytics 4",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GA4_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "landing-page validation",
            "engagement trend export",
            "delivery pack regeneration",
        ],
        "production_flow": [
            "connect GA4 credential secret",
            "validate baseline metrics import",
            "bind to project executive dashboard",
            "re-run after major content or release changes",
        ],
        "capabilities": [
            "sessions import",
            "engagement import",
            "top-page metrics",
            "executive dashboard rollup",
        ],
        "next_step": "Use GA4 as the executive outcome layer after core crawlability and discoverability signals are stable.",
    },
    "google_ads": {
        "source_type": "google_ads",
        "label": "Google Ads",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "campaign baseline refresh",
            "search-term drift review",
            "brand vs non-brand split review",
            "cost-to-conversion validation",
        ],
        "production_flow": [
            "connect Google Ads credentials",
            "sync campaigns, ad groups, and search terms",
            "separate brand and non-brand demand",
            "compare paid demand with organic and AI visibility",
        ],
        "capabilities": [
            "campaign import",
            "ad group import",
            "search terms import",
            "cost and conversion tracking",
            "brand vs non-brand demand context",
        ],
        "next_step": "Use Google Ads as the paid-demand layer paired with GSC and GA4 for full-funnel search interpretation.",
    },
    "yandex_webmaster": {
        "source_type": "yandex_webmaster",
        "label": "Yandex Webmaster",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_WEBMASTER_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "RU indexation baseline",
            "regional diagnostics refresh",
            "artifact export",
        ],
        "production_flow": [
            "connect Yandex Webmaster token",
            "validate RU property mapping",
            "schedule recurring sync for regional visibility checks",
            "attach RU findings to deliverables and dashboard",
        ],
        "capabilities": [
            "top queries import",
            "top pages import",
            "regional discoverability baseline",
            "RU deliverable support",
        ],
        "next_step": "Treat Yandex Webmaster as a first-class RU market source and keep it in the same recurring comparison loop as GSC.",
    },
    "yandex_metrica": {
        "source_type": "yandex_metrica",
        "label": "Yandex Metrica",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_METRICA_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "traffic sanity checks",
            "goal trend export",
            "executive dashboard refresh",
        ],
        "production_flow": [
            "connect Yandex Metrica token",
            "verify visits and goals import",
            "pair analytics with Yandex Webmaster diagnostics",
            "track post-fix performance deltas in executive mode",
        ],
        "capabilities": [
            "visit import",
            "goal conversion import",
            "top-page metrics",
            "RU executive dashboard support",
        ],
        "next_step": "Use Metrica as the RU engagement and conversion layer paired with Yandex Webmaster for indexation and diagnostics.",
    },
    "yandex_direct": {
        "source_type": "yandex_direct",
        "label": "Yandex Direct",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_DIRECT_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "campaign baseline refresh",
            "brand-demand drift review",
            "landing-page alignment check",
            "cost-to-discoverability comparison",
        ],
        "production_flow": [
            "connect Yandex Direct token",
            "pull campaign and ad-group baseline",
            "compare paid demand with organic and AI discoverability shifts",
            "use spend and conversion context in executive and delivery packs",
        ],
        "capabilities": [
            "campaign baseline import",
            "brand-demand context",
            "paid-vs-organic comparison",
            "landing-page alignment support",
        ],
        "next_step": "Use Yandex Direct as the paid-demand companion to Yandex Webmaster and Metrica when RU acquisition quality matters.",
    },
    "indexnow": {
        "source_type": "indexnow",
        "label": "IndexNow",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_push",
        "required_env_vars": ["INDEXNOW_KEY"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "fresh-url push",
            "submission success review",
            "indexation delta verification",
        ],
        "production_flow": [
            "configure IndexNow key",
            "submit changed URLs in batches",
            "verify acceptance rate",
            "compare post-submit indexation with GSC and Webmaster",
        ],
        "capabilities": [
            "fresh URL submission",
            "batch diagnostics",
            "indexation acceleration support",
        ],
        "next_step": "Use IndexNow as the fast-change distribution layer for pages that need fresher discovery signals.",
    },
    "google_business_profile": {
        "source_type": "google_business_profile",
        "label": "Google Business Profile",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GBP_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "rating refresh",
            "review trend review",
            "local action validation",
        ],
        "production_flow": [
            "connect profile credentials",
            "sync ratings, reviews, and local actions",
            "compare profile demand with local landing performance",
            "attach local proof to executive and client outputs",
        ],
        "capabilities": [
            "ratings and reviews import",
            "calls and direction-request context",
            "local SEO proof support",
        ],
        "next_step": "Use Google Business Profile whenever local intent, maps demand, or trust signals affect conversion.",
    },
    "yandex_business": {
        "source_type": "yandex_business",
        "label": "Yandex Business",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_BUSINESS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "map visibility refresh",
            "review trend review",
            "route-build and click validation",
        ],
        "production_flow": [
            "connect Yandex Business token",
            "sync maps reviews and local actions",
            "compare local RU demand with landing-page performance",
            "use results in RU executive and local-service delivery",
        ],
        "capabilities": [
            "rating and review import",
            "maps action context",
            "RU local SEO proof support",
        ],
        "next_step": "Use Yandex Business alongside Webmaster and Metrica when local RU intent matters.",
    },
    "merchant_center": {
        "source_type": "merchant_center",
        "label": "Google Merchant Center",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["MERCHANT_CENTER_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "feed health review",
            "product approval-rate review",
            "top issue export",
        ],
        "production_flow": [
            "connect Merchant Center credentials",
            "sync product feed diagnostics",
            "compare feed health with landing and conversion performance",
            "track approval-rate regressions over time",
        ],
        "capabilities": [
            "feed diagnostics import",
            "product approval tracking",
            "e-commerce issue visibility",
        ],
        "next_step": "Use Merchant Center for e-commerce properties where feed health affects discoverability and conversions.",
    },
    "keyword_research": {
        "source_type": "keyword_research",
        "label": "Keyword Research Intelligence",
        "readiness_tier": "seo_intelligence_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["KEYWORD_RESEARCH_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "demand snapshot refresh",
            "brand vs non-brand split review",
            "query-cluster coverage review",
        ],
        "production_flow": [
            "connect keyword research export or provider token",
            "group demand by brand, non-brand, and high-intent clusters",
            "compare market demand with content and landing coverage",
            "feed gaps into roadmap, generation, and executive reporting",
        ],
        "capabilities": [
            "keyword snapshot import",
            "intent cluster coverage",
            "brand vs non-brand demand baseline",
            "opportunity keyword review",
        ],
        "next_step": "Use keyword research as the demand map that drives landing priorities, content briefs, and executive opportunity framing.",
    },
    "competitor_intelligence": {
        "source_type": "competitor_intelligence",
        "label": "Competitor Intelligence",
        "readiness_tier": "seo_intelligence_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["COMPETITOR_INTELLIGENCE_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "competitor gap refresh",
            "trust and proof gap review",
            "GEO content gap review",
        ],
        "production_flow": [
            "connect competitor export or provider token",
            "map content, trust, and GEO gaps by competitor",
            "separate gaps that affect rankings from gaps that affect citations and conversion trust",
            "attach top competitor gaps to the operating queue",
        ],
        "capabilities": [
            "content gap import",
            "trust and proof gap detection",
            "GEO surface gap detection",
            "authority overlap support",
        ],
        "next_step": "Use competitor intelligence to decide where to build proof, answer-ready pages, and comparison assets first.",
    },
    "backlink_intelligence": {
        "source_type": "backlink_intelligence",
        "label": "Backlink and Authority Intelligence",
        "readiness_tier": "seo_intelligence_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["BACKLINK_INTELLIGENCE_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "referring-domain refresh",
            "lost-link recovery review",
            "authority trend review",
        ],
        "production_flow": [
            "connect backlink export or provider token",
            "review new, lost, and high-trust referring domains",
            "separate entity citations, editorial mentions, and partner proof",
            "route recoverable authority losses into weekly ops",
        ],
        "capabilities": [
            "referring domain baseline",
            "authority trend tracking",
            "lost-link review",
            "entity citation support",
        ],
        "next_step": "Use backlink intelligence to recover trust, authority, and entity signals that support both SEO and GEO performance.",
    },
    "rank_tracking": {
        "source_type": "rank_tracking",
        "label": "Rank Tracking and SERP Visibility",
        "readiness_tier": "seo_intelligence_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["RANK_TRACKING_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "tracked-query refresh",
            "movement review",
            "SERP feature capture review",
        ],
        "production_flow": [
            "connect rank export or provider token",
            "sync tracked queries and SERP feature coverage",
            "prioritize positions 4 through 12 first",
            "separate rank gains from answer-surface gains in the weekly narrative",
        ],
        "capabilities": [
            "tracked-query import",
            "rank movement review",
            "SERP feature coverage",
            "weekly visibility trend support",
        ],
        "next_step": "Use rank tracking to validate whether content, technical, and proof changes are moving important queries into stronger positions.",
    },
    "crux": {
        "source_type": "crux",
        "label": "Chrome UX Report",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["CRUX_API_KEY"],
        "recommended_ci_workflow": ".github/workflows/lighthouse-ci.yml",
        "ci_gates": [
            "field data refresh",
            "core web vitals regression check",
            "executive dashboard refresh",
        ],
        "production_flow": [
            "connect CrUX API key",
            "bind an origin or URL to the integration config",
            "compare field data against synthetic checks",
            "use scheduled refresh for release and post-fix verification",
        ],
        "capabilities": [
            "real-user CWV field data",
            "origin or URL scope tracking",
            "executive dashboard support",
            "release regression context",
        ],
        "next_step": "Use CrUX as the field-data layer that complements synthetic audits and release gating.",
    },
    "meta_ads": {
        "source_type": "meta_ads",
        "label": "Meta Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["META_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "retargeting baseline refresh",
            "lead cost review",
            "landing alignment check",
        ],
        "production_flow": [
            "connect Meta Ads token",
            "sync campaign spend and lead data",
            "compare retargeting efficiency with organic and AI demand",
            "use as a paid amplification layer, not core SEO truth",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "retargeting context",
        ],
        "next_step": "Use Meta Ads as a paid amplification and remarketing layer, not as a substitute for search data.",
    },
    "x_ads": {
        "source_type": "x_ads",
        "label": "X Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["X_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "campaign baseline refresh",
            "thought-leadership amplification review",
            "lead cost review",
        ],
        "production_flow": [
            "connect X Ads token",
            "sync campaign spend clicks and leads",
            "compare amplification demand with branded search and AI mentions",
            "use it for distribution and executive narrative, not core search truth",
        ],
        "capabilities": [
            "campaign spend import",
            "click and CPL tracking",
            "thought-leadership amplification context",
        ],
        "next_step": "Use X Ads where expert distribution and founder-led amplification affect demand generation.",
    },
    "x_organic": {
        "source_type": "x_organic",
        "label": "X Organic Intelligence",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["X_ORGANIC_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "post performance refresh",
            "mention trend review",
            "content opportunity export",
        ],
        "production_flow": [
            "connect X organic analytics or approved export token",
            "sync post performance and mention signals",
            "turn high-engagement posts into site and FAQ opportunities",
            "feed repeated questions into GEO and content planning",
        ],
        "capabilities": [
            "post performance import",
            "mention tracking",
            "content opportunity detection",
            "community demand context",
        ],
        "next_step": "Use X organic as a community and insight layer that feeds content, proof, and founder-brand loops.",
    },
    "threads": {
        "source_type": "threads",
        "label": "Threads Intelligence",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["THREADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "discussion performance refresh",
            "question cluster review",
            "site-click validation",
        ],
        "production_flow": [
            "connect Threads analytics or approved export token",
            "sync views, engagements, replies, and site clicks",
            "cluster repeated questions and objections",
            "reuse strong discussions for answer-ready pages and executive narratives",
        ],
        "capabilities": [
            "discussion performance import",
            "question cluster detection",
            "site-click context",
        ],
        "next_step": "Use Threads where discussion quality and recurring objections inform product messaging and GEO content design.",
    },
    "reddit_mentions": {
        "source_type": "reddit_mentions",
        "label": "Reddit Mentions",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["REDDIT_MONITOR_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "community mention refresh",
            "sentiment review",
            "opportunity export",
        ],
        "production_flow": [
            "connect approved Reddit monitoring token or export",
            "sync communities, mentions, and clicks",
            "separate positive proof from negative objections",
            "feed useful threads into public proof and FAQ planning",
        ],
        "capabilities": [
            "community mention tracking",
            "sentiment context",
            "content opportunity detection",
        ],
        "next_step": "Use Reddit mentions when community trust, objections, and peer recommendations influence buying or citation patterns.",
    },
    "tiktok_organic": {
        "source_type": "tiktok_organic",
        "label": "TikTok Organic",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["TIKTOK_ORGANIC_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "video performance refresh",
            "comment signal review",
            "site-click review",
        ],
        "production_flow": [
            "connect TikTok analytics or approved export token",
            "sync views, watch rate, profile clicks, and site clicks",
            "promote high-retention ideas into site hooks and landing copy",
            "convert top comments into FAQs and objection handling",
        ],
        "capabilities": [
            "video performance import",
            "comment-derived content opportunities",
            "site-click context",
        ],
        "next_step": "Use TikTok organic where short-form demand and creator-style hooks influence acquisition and messaging.",
    },
    "vk_ads": {
        "source_type": "vk_ads",
        "label": "VK Ads",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["VK_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "RU campaign baseline refresh",
            "lead cost review",
            "landing alignment review",
        ],
        "production_flow": [
            "connect VK Ads token",
            "sync spend clicks and leads",
            "compare RU paid demand with Webmaster and Direct",
            "use it as a RU growth layer around the core search stack",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "RU paid distribution context",
        ],
        "next_step": "Use VK Ads when RU paid acquisition and community demand need to be measured next to search channels.",
    },
    "telegram_ads": {
        "source_type": "telegram_ads",
        "label": "Telegram Ads or Channel Analytics",
        "readiness_tier": "managed_runtime_ready",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["TELEGRAM_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "reach baseline refresh",
            "click and lead review",
            "channel demand validation",
        ],
        "production_flow": [
            "connect Telegram ads or channel analytics token",
            "sync channel reach clicks and leads",
            "compare channel demand with landing conversion",
            "use it as a community and distribution signal layer",
        ],
        "capabilities": [
            "channel reach import",
            "click tracking",
            "community demand context",
        ],
        "next_step": "Use Telegram when your distribution model depends on channels, communities, or post-driven demand.",
    },
    "vk_organic": {
        "source_type": "vk_organic",
        "label": "VK Organic Community Intelligence",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["VK_ORGANIC_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "community post refresh",
            "comment and mention review",
            "site-click validation",
        ],
        "production_flow": [
            "connect VK community analytics token or approved export",
            "sync reach, engagement, comments, and site clicks",
            "mine repeated objections and market language",
            "feed winning posts into RU GEO content and local proof packs",
        ],
        "capabilities": [
            "community post performance",
            "comment-derived FAQ mining",
            "RU market messaging context",
            "site-click tracking",
        ],
        "next_step": "Use VK organic as a RU-native community signal layer for messaging, trust, and FAQ discovery.",
    },
    "telegram_channels": {
        "source_type": "telegram_channels",
        "label": "Telegram Channel Intelligence",
        "readiness_tier": "social_intelligence_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["TELEGRAM_CHANNEL_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "channel post refresh",
            "reply trend review",
            "click and lead validation",
        ],
        "production_flow": [
            "connect Telegram channel analytics token or approved export",
            "sync reach, post clicks, forwards, and replies",
            "turn high-signal posts into landing-page hooks and answer-ready sections",
            "use channel demand alongside branded search and Yandex demand",
        ],
        "capabilities": [
            "channel reach import",
            "reply and forward tracking",
            "content opportunity mining",
            "site-click and lead context",
        ],
        "next_step": "Use Telegram channel intelligence when founder-led demand, communities, and post-driven acquisition matter.",
    },
    "yandex_neuro": {
        "source_type": "yandex_neuro",
        "label": "Yandex Neuro and AI Readiness",
        "readiness_tier": "ru_ai_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_NEURO_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "YandexAdditional readiness refresh",
            "RU answer-ready content review",
            "entity and trust block validation",
        ],
        "production_flow": [
            "connect approved RU AI monitoring token or maintain operator-reviewed exports",
            "validate YandexAdditional access, RU trust signals, and answer-ready content",
            "compare Neuro readiness with Webmaster, Metrica, and Business signals",
            "feed RU AI findings into legal, trust, and FAQ upgrades",
        ],
        "capabilities": [
            "YandexAdditional readiness tracking",
            "RU entity readiness review",
            "trust and answer-block diagnostics",
            "AI discoverability narrative support",
        ],
        "next_step": "Use Yandex Neuro readiness as the RU AI layer that complements Webmaster, Metrica, and Business data.",
    },
    "alice_ai_visibility": {
        "source_type": "alice_ai_visibility",
        "label": "Alice AI Visibility in Yandex Search",
        "readiness_tier": "ru_ai_guided",
        "sync_mode": "manual_or_weekly_pull",
        "required_env_vars": ["ALICE_AI_VISIBILITY_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "weekly share-of-voice refresh",
            "query and page example review",
            "competitor-source overlap review",
        ],
        "production_flow": [
            "connect approved Alice AI visibility export or operator token",
            "import weekly SoV, query examples, and competitor examples from Yandex Webmaster",
            "compare Alice AI visibility with Webmaster, Metrica, Direct, and Yandex Neuro signals",
            "convert weak or missing Alice answer coverage into RU answer-ready content tasks",
        ],
        "capabilities": [
            "weekly share-of-voice tracking",
            "query and page example review",
            "competitor/source overlap review",
            "RU executive dashboard support",
        ],
        "next_step": "Use Alice AI visibility as the official RU AI answer-surface metric and review it weekly next to classic Yandex search signals.",
    },
    "dzen": {
        "source_type": "dzen",
        "label": "Dzen Distribution Intelligence",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["DZEN_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "content reach refresh",
            "click-through review",
            "RU content angle export",
        ],
        "production_flow": [
            "connect Dzen analytics token or approved export",
            "sync reach, clicks, and topic demand",
            "route strong content angles into site content and GEO planning",
            "compare Dzen distribution with RU search and AI demand",
        ],
        "capabilities": [
            "reach and click tracking",
            "topic-demand discovery",
            "RU distribution context",
        ],
        "next_step": "Use Dzen when Russian-language editorial distribution shapes awareness and demand capture.",
    },
    "rutube": {
        "source_type": "rutube",
        "label": "RuTube Analytics",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["RUTUBE_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "video performance refresh",
            "site-click review",
            "channel demand validation",
        ],
        "production_flow": [
            "connect RuTube analytics token or approved export",
            "sync video reach, watch metrics, and site clicks",
            "compare video-led RU demand with branded search and Yandex demand",
            "turn strong video topics into FAQ, comparison, and trust assets",
        ],
        "capabilities": [
            "video metrics import",
            "watch-time context",
            "RU audience demand signals",
        ],
        "next_step": "Use RuTube when Russian-speaking audiences discover the brand through local video distribution.",
    },
    "youtube": {
        "source_type": "youtube",
        "label": "YouTube Analytics",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YOUTUBE_ANALYTICS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "video performance refresh",
            "site-click review",
            "channel growth validation",
        ],
        "production_flow": [
            "connect YouTube Analytics token",
            "sync video and channel performance",
            "compare media demand with branded search and citations",
            "use it as a discoverability and content-distribution layer",
        ],
        "capabilities": [
            "video metrics import",
            "watch-time context",
            "site-click tracking",
        ],
        "next_step": "Use YouTube where educational video or branded media affects search and AI demand.",
    },
    "linkedin_ads": {
        "source_type": "linkedin_ads",
        "label": "LinkedIn Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["LINKEDIN_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "B2B campaign refresh",
            "lead cost review",
            "landing alignment review",
        ],
        "production_flow": [
            "connect LinkedIn Ads token",
            "sync spend clicks and lead data",
            "compare B2B demand with branded search and conversion paths",
            "use it as a B2B amplification layer",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "B2B distribution context",
        ],
        "next_step": "Use LinkedIn Ads for B2B acquisition where paid awareness shapes search and conversion demand.",
    },
    "instagram_facebook_organic": {
        "source_type": "instagram_facebook_organic",
        "label": "Instagram or Facebook Organic",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["META_GRAPH_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "reach baseline refresh",
            "engagement trend review",
            "site-click validation",
        ],
        "production_flow": [
            "connect Meta Graph token",
            "sync reach engagement and site-click data",
            "compare organic social demand with brand demand and conversion",
            "use it as a supporting content-distribution signal",
        ],
        "capabilities": [
            "reach import",
            "engagement tracking",
            "site-click context",
        ],
        "next_step": "Use Instagram or Facebook organic data as a supporting distribution signal, not as the core SEO or GEO layer.",
    },
}


def integration_contract(source_type: str) -> dict[str, Any]:
    source = source_type.strip().lower()
    if source not in INTEGRATION_CONTRACTS:
        raise ValueError(f"Unsupported integration source '{source_type}'.")
    return {
        **INTEGRATION_CONTRACTS[source],
        "contract_version": CONTRACT_VERSION,
    }


def integration_env_status(contract: dict[str, Any]) -> dict[str, Any]:
    required = contract.get("required_env_vars", [])
    present = [name for name in required if os.getenv(name, "").strip()]
    missing = [name for name in required if name not in present]
    return {
        "required_env_vars": required,
        "present_env_vars": present,
        "missing_env_vars": missing,
        "live_credentials_ready": not missing,
    }


def all_integration_contracts() -> list[dict[str, Any]]:
    return [integration_contract(key) for key in sorted(INTEGRATION_CONTRACTS)]


def integration_runtime_profile(
    source_type: str,
    *,
    config: dict[str, Any] | None = None,
    credentials_env_var: str | None = None,
    latest_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract = integration_contract(source_type)
    env_status = integration_env_status(contract)
    runtime_config = config or {}
    snapshot = latest_snapshot or {}
    snapshot_source = str(snapshot.get("source") or "").lower()
    managed_runtime_enabled = bool(runtime_config.get("managed_runtime_enabled"))
    runtime_owner = str(runtime_config.get("runtime_owner") or "operator")
    refresh_minutes = int(runtime_config.get("refresh_minutes") or 1440)
    retry_backoff_minutes = runtime_config.get("retry_backoff_minutes") or [5, 15, 60]
    token_rotation_days = int(runtime_config.get("token_rotation_days") or 90)
    failure_recovery_mode = str(
        runtime_config.get("failure_recovery_mode") or "retry_then_operator_review"
    )

    runtime_level = "starter_sync"
    if managed_runtime_enabled and (
        credentials_env_var or env_status["live_credentials_ready"]
    ):
        runtime_level = "managed_runtime"
    elif credentials_env_var or env_status["live_credentials_ready"]:
        runtime_level = "live_runtime"
    if snapshot_source and not any(
        token in snapshot_source for token in ["stub", "starter", "fallback"]
    ):
        runtime_level = (
            "managed_runtime" if runtime_level == "managed_runtime" else "live_runtime"
        )

    return {
        "runtime_level": runtime_level,
        "runtime_owner": runtime_owner,
        "managed_runtime_enabled": managed_runtime_enabled,
        "refresh_minutes": refresh_minutes,
        "retry_backoff_minutes": retry_backoff_minutes,
        "token_rotation_days": token_rotation_days,
        "failure_recovery_mode": failure_recovery_mode,
        "credential_ready": bool(
            credentials_env_var or env_status["live_credentials_ready"]
        ),
        "required_env_vars": contract.get("required_env_vars", []),
    }


def integration_sync_diagnostics(
    source_type: str,
    *,
    config: dict[str, Any] | None = None,
    credentials_env_var: str | None = None,
    latest_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract = integration_contract(source_type)
    snapshot = latest_snapshot or {}
    runtime_profile = integration_runtime_profile(
        source_type,
        config=config,
        credentials_env_var=credentials_env_var,
        latest_snapshot=snapshot,
    )
    snapshot_source = str(snapshot.get("source") or "")
    sample_tokens = ("stub", "starter", "fallback")
    snapshot_mode = (
        "starter_or_stub"
        if any(token in snapshot_source.lower() for token in sample_tokens)
        else "live_or_runtime"
        if snapshot_source
        else "not_synced"
    )
    checks = {
        "credentials": "ready" if runtime_profile["credential_ready"] else "missing",
        "runtime": runtime_profile["runtime_level"],
        "snapshot_mode": snapshot_mode,
        "scheduled_refresh": "configured"
        if runtime_profile["refresh_minutes"] <= 1440
        else "manual_or_daily",
        "token_rotation": f"every {runtime_profile['token_rotation_days']} days",
        "failure_recovery": runtime_profile["failure_recovery_mode"],
    }
    actions = [
        f"set refresh cadence to {runtime_profile['refresh_minutes']} minutes",
        f"rotate secrets every {runtime_profile['token_rotation_days']} days",
        f"keep retry backoff at {runtime_profile['retry_backoff_minutes']}",
        contract["next_step"],
    ]
    if snapshot_mode == "starter_or_stub":
        actions.insert(
            0,
            "replace starter payload with a live API token or approved export feed",
        )
    if not runtime_profile["credential_ready"]:
        actions.insert(0, "configure the required env vars and rerun the first sync")
    return {
        "checks": checks,
        "recommended_actions": actions,
    }


def _ga4_stub() -> dict[str, Any]:
    return _run_json_script("ga4_data_stub.py", "GA4 starter import failed.")


def _yandex_metrica_stub() -> dict[str, Any]:
    return _run_json_script(
        "yandex_metrica_stub.py", "Yandex Metrica starter import failed."
    )


def _run_json_script(script_name: str, error_message: str) -> dict[str, Any]:
    code, stdout, stderr = run_script(script_name, [])
    if code != 0:
        raise RuntimeError(stderr or error_message)
    return json.loads(stdout)


def sync_integration_source(
    source_type: str,
    *,
    property_identifier: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = source_type.strip().lower()
    contract = integration_contract(source)
    if source == "gsc":
        payload = _run_json_script("gsc_data_stub.py", "GSC starter import failed.")
    elif source == "ga4":
        payload = _ga4_stub()
    elif source == "google_ads":
        payload = _run_json_script(
            "google_ads_stub.py", "Google Ads starter import failed."
        )
    elif source == "yandex_webmaster":
        payload = _run_json_script(
            "yandex_data_stub.py", "Yandex Webmaster starter import failed."
        )
    elif source == "yandex_metrica":
        payload = _yandex_metrica_stub()
    elif source == "yandex_direct":
        payload = _run_json_script(
            "yandex_direct_stub.py", "Yandex Direct starter import failed."
        )
    elif source == "indexnow":
        payload = _run_json_script("indexnow_stub.py", "IndexNow starter failed.")
    elif source == "google_business_profile":
        payload = _run_json_script(
            "google_business_profile_stub.py",
            "Google Business Profile starter import failed.",
        )
    elif source == "yandex_business":
        payload = _run_json_script(
            "yandex_business_stub.py", "Yandex Business starter import failed."
        )
    elif source == "merchant_center":
        payload = _run_json_script(
            "merchant_center_stub.py", "Merchant Center starter import failed."
        )
    elif source == "keyword_research":
        payload = _run_json_script(
            "keyword_research_stub.py", "Keyword research starter import failed."
        )
    elif source == "competitor_intelligence":
        payload = _run_json_script(
            "competitor_intelligence_stub.py",
            "Competitor intelligence starter import failed.",
        )
    elif source == "backlink_intelligence":
        payload = _run_json_script(
            "backlink_intelligence_stub.py",
            "Backlink intelligence starter import failed.",
        )
    elif source == "rank_tracking":
        payload = _run_json_script(
            "rank_tracking_stub.py", "Rank tracking starter import failed."
        )
    elif source == "crux":
        target_url = (
            (config or {}).get("url") or property_identifier or "https://example.com/"
        )
        api_key = os.environ.get("CRUX_API_KEY", "").strip()
        if api_key:
            code, stdout, stderr = run_script(
                "crux_field_data.py", ["--url", target_url, "--json"]
            )
            if code == 0:
                payload = json.loads(stdout)
            else:
                payload = {
                    "source": "crux-starter-fallback",
                    "note": stderr
                    or "CrUX live import failed; returning starter fallback.",
                    "target_url": target_url,
                    "metrics": {},
                }
        else:
            payload = {
                "source": "crux-starter",
                "note": "CRUX_API_KEY is missing; returning starter payload.",
                "target_url": target_url,
                "metrics": {
                    "largest_contentful_paint": {"p75": 2800},
                    "interaction_to_next_paint": {"p75": 240},
                    "cumulative_layout_shift": {"p75": 0.12},
                },
            }
    elif source == "meta_ads":
        payload = _run_json_script("meta_ads_stub.py", "Meta Ads starter failed.")
    elif source == "x_ads":
        payload = _run_json_script("x_ads_stub.py", "X Ads starter failed.")
    elif source == "x_organic":
        payload = _run_json_script(
            "x_organic_stub.py", "X organic intelligence starter failed."
        )
    elif source == "threads":
        payload = _run_json_script("threads_stub.py", "Threads starter failed.")
    elif source == "reddit_mentions":
        payload = _run_json_script(
            "reddit_mentions_stub.py", "Reddit mentions starter failed."
        )
    elif source == "tiktok_organic":
        payload = _run_json_script(
            "tiktok_organic_stub.py", "TikTok organic starter failed."
        )
    elif source == "vk_ads":
        payload = _run_json_script("vk_ads_stub.py", "VK Ads starter failed.")
    elif source == "telegram_ads":
        payload = _run_json_script(
            "telegram_ads_stub.py", "Telegram ads starter failed."
        )
    elif source == "vk_organic":
        payload = _run_json_script(
            "vk_organic_stub.py", "VK organic intelligence starter failed."
        )
    elif source == "telegram_channels":
        payload = _run_json_script(
            "telegram_channels_stub.py",
            "Telegram channel intelligence starter failed.",
        )
    elif source == "yandex_neuro":
        payload = _run_json_script(
            "yandex_neuro_stub.py", "Yandex Neuro starter failed."
        )
    elif source == "alice_ai_visibility":
        payload = _run_json_script(
            "alice_ai_visibility_stub.py", "Alice AI visibility starter failed."
        )
    elif source == "dzen":
        payload = _run_json_script("dzen_stub.py", "Dzen starter failed.")
    elif source == "rutube":
        payload = _run_json_script("rutube_stub.py", "RuTube starter failed.")
    elif source == "youtube":
        payload = _run_json_script(
            "youtube_analytics_stub.py", "YouTube analytics starter failed."
        )
    elif source == "linkedin_ads":
        payload = _run_json_script(
            "linkedin_ads_stub.py", "LinkedIn Ads starter failed."
        )
    elif source == "instagram_facebook_organic":
        payload = _run_json_script(
            "instagram_facebook_organic_stub.py",
            "Instagram or Facebook organic starter failed.",
        )
    else:
        raise ValueError(f"Unsupported integration source '{source_type}'.")

    payload["contract"] = contract
    payload["sync_mode"] = contract["sync_mode"]
    payload["runtime_profile"] = integration_runtime_profile(
        source,
        config=config,
        latest_snapshot=payload,
    )
    payload["imported_at"] = datetime.utcnow().isoformat() + "Z"
    return payload


def compact_integration_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    rows = snapshot.get("rows") or []
    if rows:
        return {
            "row_count": len(rows),
            "top_queries": [row.get("query") for row in rows[:3]],
            "top_pages": [row.get("page") for row in rows[:3]],
            "imported_at": datetime.utcnow().isoformat() + "Z",
        }
    top_pages = snapshot.get("top_pages") or []
    metrics = snapshot.get("metrics") or {}
    return {
        "row_count": len(top_pages),
        "top_pages": [row.get("page") for row in top_pages[:3]],
        "metrics": metrics,
        "runtime_level": (snapshot.get("runtime_profile") or {}).get("runtime_level"),
        "imported_at": datetime.utcnow().isoformat() + "Z",
    }


def _integration_proof_level(source_type: str, snapshot: dict[str, Any]) -> str:
    source = str(snapshot.get("source") or "").lower()
    if not snapshot:
        return "contract_only"
    if "stub" in source or "starter" in source or "fallback" in source:
        return "starter_or_stub"
    if source_type == "crux" and snapshot.get("metrics"):
        return "live_or_sampled_metrics"
    return "live_api_or_runtime"


def build_integration_verification_row(
    source_type: str,
    *,
    label: str,
    credentials_env_var: str | None = None,
    property_identifier: str | None = None,
    latest_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract = integration_contract(source_type)
    snapshot = latest_snapshot or {}
    proof_level = _integration_proof_level(source_type, snapshot)
    env_status = integration_env_status(contract)
    return {
        "id": source_type,
        "surface_type": "integration",
        "surface_name": label,
        "source_type": source_type,
        "readiness_tier": contract["readiness_tier"],
        "proof_level": proof_level,
        "credentials_status": "configured"
        if credentials_env_var or env_status["live_credentials_ready"]
        else "missing",
        "property_identifier": property_identifier,
        "ci_workflow": contract["recommended_ci_workflow"],
        "ci_gates": contract["ci_gates"],
        "capabilities": contract["capabilities"],
        "production_flow": contract["production_flow"],
        "verification_checks": [
            "credentials configured",
            "manual sync completed",
            "snapshot imported",
            "CI or scheduled refresh defined",
            "evidence attached to executive output",
        ],
        "latest_snapshot_source": snapshot.get("source"),
        "latest_snapshot_summary": compact_integration_summary(snapshot)
        if snapshot
        else {},
        "runtime_profile": integration_runtime_profile(
            source_type,
            credentials_env_var=credentials_env_var,
            latest_snapshot=snapshot,
        ),
        "sync_diagnostics": integration_sync_diagnostics(
            source_type,
            credentials_env_var=credentials_env_var,
            latest_snapshot=snapshot,
        ),
        "env_status": env_status,
        "next_step": contract["next_step"],
    }
