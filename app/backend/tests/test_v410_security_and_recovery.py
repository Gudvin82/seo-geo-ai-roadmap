from __future__ import annotations

from io import BytesIO

from app.database import create_session
from app.models import ScanJob
from app.services import scan_jobs
from app.services.scan_security import _read_limited_response
from fastapi import HTTPException


def _scanner_headers() -> dict[str, str]:
    return {"X-Scanner-Session": "scanner-test-session"}


def test_scan_results_require_matching_scanner_session(
    client, settings, monkeypatch
) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    monkeypatch.setattr(
        scan_jobs,
        "_launch_scan_job",
        lambda local_settings, job_id: scan_jobs._run_scan_job(local_settings, job_id),
    )
    monkeypatch.setattr(
        scan_jobs, "_deliver_notifications", lambda local_settings, row, artifacts: []
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
    scan_job_id = accepted.json()["scan_job_id"]

    tasks = client.get(f"/api/v1/tasks/scan-job/{scan_job_id}")
    assert tasks.status_code == 403

    graph = client.get(f"/api/v1/graph-runtime/scan-job/{scan_job_id}")
    assert graph.status_code == 403


def test_response_size_limit_is_enforced() -> None:
    oversized_payload = BytesIO(b"a" * 11)

    try:
        _read_limited_response(oversized_payload, max_bytes=10)
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "size limit" in exc.detail.lower()
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("Expected an HTTPException for oversized response body.")


def test_recover_incomplete_scan_jobs_requeues_running_work(settings, app) -> None:
    del settings, app
    db = create_session()
    try:
        first = ScanJob(
            submitted_url="https://example.com",
            normalized_url="https://example.com/",
            target_domain="example.com",
            scan_mode="passive",
            status="running",
            progress_percent=60,
            current_stage="reporting",
            requester_session_id="scanner-test-session",
        )
        second = ScanJob(
            submitted_url="https://example.org",
            normalized_url="https://example.org/",
            target_domain="example.org",
            scan_mode="passive",
            status="verifying",
            progress_percent=15,
            current_stage="verification",
            requester_session_id="scanner-test-session",
        )
        db.add(first)
        db.add(second)
        db.commit()
        db.refresh(first)
        db.refresh(second)
    finally:
        db.close()

    recovered = scan_jobs.recover_incomplete_scan_jobs()
    assert recovered == 2

    db = create_session()
    try:
        first_row = db.get(ScanJob, first.id)
        second_row = db.get(ScanJob, second.id)
        assert first_row is not None
        assert second_row is not None
        assert first_row.status == "queued"
        assert first_row.current_stage == "recovered_after_restart"
        assert first_row.progress_percent == 5
        assert second_row.status == "queued"
        assert second_row.current_stage == "recovered_after_restart"
        assert second_row.progress_percent == 5

        events = scan_jobs.list_scan_job_events(db, first.id)
        assert any(event["stage"] == "recovered_after_restart" for event in events)
    finally:
        db.close()
