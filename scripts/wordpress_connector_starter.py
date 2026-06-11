from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request


def fetch_collection(base_url: str, resource: str) -> list[dict]:
    endpoint = urllib.parse.urljoin(
        base_url.rstrip("/") + "/", f"wp-json/wp/v2/{resource}"
    )
    with urllib.request.urlopen(endpoint, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="WordPress REST inventory starter")
    parser.add_argument("--base-url", required=True, help="Site base URL")
    args = parser.parse_args()

    pages = fetch_collection(args.base_url, "pages")
    posts = fetch_collection(args.base_url, "posts")
    payload = {
        "base_url": args.base_url,
        "pages": [
            {
                "id": item["id"],
                "slug": item["slug"],
                "status": item["status"],
                "link": item["link"],
            }
            for item in pages
        ],
        "posts": [
            {
                "id": item["id"],
                "slug": item["slug"],
                "status": item["status"],
                "link": item["link"],
            }
            for item in posts
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
