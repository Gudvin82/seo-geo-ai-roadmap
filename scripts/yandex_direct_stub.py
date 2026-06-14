from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "yandex-direct-stub",
        "note": "Starter ads payload. Replace with a real Yandex Direct connector.",
        "campaigns": [
            {
                "campaign": "Brand Search",
                "impressions": 12400,
                "clicks": 811,
                "ctr": 0.065,
                "avg_cpc": 21.4,
            },
            {
                "campaign": "Service Intent",
                "impressions": 8700,
                "clicks": 462,
                "ctr": 0.053,
                "avg_cpc": 28.9,
            },
        ],
        "metrics": {
            "spend": 35720,
            "clicks": 1273,
            "conversions": 46,
            "cost_per_conversion": 776.5,
        },
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
