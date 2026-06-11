from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = os.getenv("VERIFY_API_BASE", "http://localhost:8000/api/v1")
APP_BASE = API_BASE.rsplit("/api/v1", 1)[0]
DEMO_EMAIL = os.getenv("VERIFY_DEMO_EMAIL", "demo@example.com")
DEMO_PASSWORD = os.getenv("VERIFY_DEMO_PASSWORD", "DemoPlatform123")


def get_json(url: str, headers: dict[str, str] | None = None) -> dict | list:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(
    url: str, payload: dict, headers: dict[str, str] | None = None
) -> dict | list:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    try:
        health = get_json(f"{APP_BASE}/healthz")
        ready = get_json(f"{APP_BASE}/readyz")
        with urllib.request.urlopen(f"{APP_BASE}/docs", timeout=20) as docs_response:
            docs_ok = docs_response.status == 200
        login = post_json(
            f"{API_BASE}/auth/login",
            {"email": DEMO_EMAIL, "password": DEMO_PASSWORD},
        )
        token = login["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        workspaces = get_json(f"{API_BASE}/workspaces", headers=headers)
        if not workspaces:
            raise RuntimeError("No demo workspaces found.")
        workspace_id = workspaces[0]["id"]
        projects = get_json(
            f"{API_BASE}/projects?workspace_id={workspace_id}", headers=headers
        )
        if not projects:
            raise RuntimeError("No demo projects found.")
        project_id = projects[0]["id"]
        audit = post_json(
            f"{API_BASE}/audit-runs/run",
            {
                "workspace_id": workspace_id,
                "project_id": project_id,
                "domain_or_url": projects[0]["website_url"],
                "selected_checks": ["factual_consistency"],
                "selected_providers": [],
                "report_language": "en",
                "mode": "quick",
            },
            headers=headers,
        )
        reports = get_json(
            f"{API_BASE}/reports?project_id={project_id}", headers=headers
        )
        artifacts = get_json(
            f"{API_BASE}/artifacts?project_id={project_id}", headers=headers
        )
        result = {
            "healthz": health,
            "readyz": ready,
            "docs_ok": docs_ok,
            "workspace_id": workspace_id,
            "project_id": project_id,
            "audit_job_id": audit["audit_job_id"],
            "report_count": len(reports),
            "artifact_count": len(artifacts),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        print(f"HTTP verification failed: {exc}", file=sys.stderr)
    except urllib.error.URLError as exc:
        print(f"Network verification failed: {exc}", file=sys.stderr)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"Verification failed: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
