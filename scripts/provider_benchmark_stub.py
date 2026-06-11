#!/usr/bin/env python3
"""Print a starter provider benchmark rubric."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "rubric": [
            "factual_consistency",
            "ru_quality",
            "en_quality",
            "structured_output",
            "latency",
            "operator_edit_burden",
        ],
        "scale": "1-5 where 5 is best",
        "examples": [
            {"provider": "openai", "model": "gpt-4.1", "scores": {}},
            {"provider": "anthropic", "model": "claude-sonnet", "scores": {}},
            {"provider": "ollama", "model": "qwen2.5:14b", "scores": {}},
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
