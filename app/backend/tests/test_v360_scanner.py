from __future__ import annotations

from app.services import scan_jobs


def _scanner_headers() -> dict[str, str]:
    return {"X-Scanner-Session": "scanner-test-session"}


def _other_scanner_headers() -> dict[str, str]:
    return {"X-Scanner-Session": "scanner-other-session"}


def test_scanner_blocks_localhost_targets(client, settings) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    response = client.post(
        "/api/v1/scanner/verification-requests",
        json={
            "url": "http://127.0.0.1:8000",
            "scan_mode": "active",
            "method": "html_file",
        },
        headers=_scanner_headers(),
    )
    assert response.status_code == 400
    assert "blocked" in response.json()["detail"].lower()


def test_verification_flow_can_be_completed(client, settings, monkeypatch) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    monkeypatch.setattr(scan_jobs, "_verify_html_file", lambda url, challenge: True)

    created = client.post(
        "/api/v1/scanner/verification-requests",
        json={
            "url": "https://example.com",
            "scan_mode": "active",
            "method": "html_file",
        },
        headers=_scanner_headers(),
    )
    assert created.status_code == 200
    payload = created.json()
    assert payload["status"] == "pending"
    verify = client.post(
        f"/api/v1/scanner/verification-requests/{payload['id']}/verify",
    )
    assert verify.status_code == 200
    assert verify.json()["status"] == "verified"


def test_active_scan_is_blocked_without_verified_ownership(client, settings) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    settings.allow_active_scan = True
    consent = client.post(
        "/api/v1/scanner/consent-records",
        json={
            "url": "https://example.com",
            "scan_mode": "active",
            "consent_scope": "active_authorized",
            "ownership_confirmed": True,
            "load_warning_accepted": True,
            "limitations_accepted": True,
        },
        headers=_scanner_headers(),
    )
    assert consent.status_code == 200
    response = client.post(
        "/api/v1/scan-jobs",
        json={
            "url": "https://example.com",
            "scan_mode": "active",
            "consent_record_id": consent.json()["id"],
        },
        headers=_scanner_headers(),
    )
    assert response.status_code == 400
    assert "ownership verification" in response.json()["detail"].lower()


def test_scan_job_lifecycle_and_artifacts(client, settings, monkeypatch) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    monkeypatch.setattr(
        scan_jobs,
        "_launch_scan_job",
        lambda local_settings, job_id: scan_jobs._run_scan_job(local_settings, job_id),
    )
    monkeypatch.setattr(
        scan_jobs, "_deliver_notifications", lambda settings, row, artifacts: []
    )

    consent = client.post(
        "/api/v1/scanner/consent-records",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_scope": "passive_ack",
            "ownership_confirmed": False,
            "load_warning_accepted": False,
            "limitations_accepted": True,
        },
        headers=_scanner_headers(),
    )
    assert consent.status_code == 200

    accepted = client.post(
        "/api/v1/scan-jobs",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_record_id": consent.json()["id"],
        },
        headers=_scanner_headers(),
    )
    assert accepted.status_code == 200
    payload = accepted.json()
    status = client.get(payload["status_endpoint"], headers=_scanner_headers())
    assert status.status_code == 200
    assert status.json()["status"] == "completed"

    events = client.get(payload["events_endpoint"], headers=_scanner_headers())
    assert events.status_code == 200
    assert len(events.json()) >= 3

    artifacts = client.get(payload["artifacts_endpoint"], headers=_scanner_headers())
    assert artifacts.status_code == 200
    artifact_payload = artifacts.json()
    assert {item["format"] for item in artifact_payload} >= {
        "json",
        "markdown",
        "csv",
        "html",
    }
    assert all(item["schema_version"] == "v4.1.0" for item in artifact_payload)

    result = client.get(
        f"/api/v1/scan-jobs/{payload['scan_job_id']}/result",
        headers=_scanner_headers(),
    )
    assert result.status_code == 200
    assert result.json()["tasks_endpoint"].endswith(
        f"/api/v1/tasks/scan-job/{payload['scan_job_id']}"
    )

    tasks = client.get(
        f"/api/v1/tasks/scan-job/{payload['scan_job_id']}",
        headers=_scanner_headers(),
    )
    assert tasks.status_code == 200
    assert tasks.json()["tasks"]

    graph = client.get(
        f"/api/v1/graph-runtime/scan-job/{payload['scan_job_id']}",
        headers=_scanner_headers(),
    )
    assert graph.status_code == 200
    assert graph.json()["nodes"]

    forbidden_tasks = client.get(
        f"/api/v1/tasks/scan-job/{payload['scan_job_id']}",
        headers=_other_scanner_headers(),
    )
    assert forbidden_tasks.status_code == 403

    forbidden_graph = client.get(
        f"/api/v1/graph-runtime/scan-job/{payload['scan_job_id']}",
        headers=_other_scanner_headers(),
    )
    assert forbidden_graph.status_code == 403


def test_webhook_delivery_mock(client, settings, monkeypatch) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    sent: list[dict] = []
    monkeypatch.setattr(
        scan_jobs,
        "_launch_scan_job",
        lambda local_settings, job_id: scan_jobs._run_scan_job(local_settings, job_id),
    )
    monkeypatch.setattr(
        scan_jobs,
        "_send_webhook",
        lambda url, payload, timeout: sent.append({"url": url, "payload": payload}),
    )

    consent = client.post(
        "/api/v1/scanner/consent-records",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_scope": "passive_ack",
            "ownership_confirmed": False,
            "load_warning_accepted": False,
            "limitations_accepted": True,
        },
        headers=_scanner_headers(),
    )
    accepted = client.post(
        "/api/v1/scan-jobs",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_record_id": consent.json()["id"],
            "callback_webhook_url": "https://hooks.example.test/scanner",
        },
        headers=_scanner_headers(),
    )
    assert accepted.status_code == 200
    assert sent
    assert sent[0]["url"] == "https://hooks.example.test/scanner"
    assert sent[0]["payload"]["status"] == "completed"


def test_scanner_blocks_non_standard_webhook_port(client, settings) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    consent = client.post(
        "/api/v1/scanner/consent-records",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_scope": "passive_ack",
            "ownership_confirmed": False,
            "load_warning_accepted": False,
            "limitations_accepted": True,
        },
        headers=_scanner_headers(),
    )
    response = client.post(
        "/api/v1/scan-jobs",
        json={
            "url": "https://example.com",
            "scan_mode": "passive",
            "consent_record_id": consent.json()["id"],
            "callback_webhook_url": "https://hooks.example.test:8443/scanner",
        },
        headers=_scanner_headers(),
    )
    assert response.status_code == 400
    assert "ports 80 and 443" in response.json()["detail"]


def test_passive_url_audit_shortcut(client, settings, monkeypatch) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    monkeypatch.setattr(
        scan_jobs,
        "_launch_scan_job",
        lambda local_settings, job_id: scan_jobs._run_scan_job(local_settings, job_id),
    )
    accepted = client.post(
        "/api/v1/scanner/url-audit",
        json={
            "url": "https://example.com",
            "mode": "passive",
            "site_type": "b2b_saas",
            "limitations_accepted": True,
        },
        headers=_scanner_headers(),
    )
    assert accepted.status_code == 200
    assert accepted.json()["status_endpoint"].endswith(
        f"/api/v1/scan-jobs/{accepted.json()['scan_job_id']}"
    )
