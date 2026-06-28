from __future__ import annotations

from fastapi.testclient import TestClient

TEST_PASSWORD = "Demo-password-123A"


def _headers_for(client: TestClient, email: str) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": TEST_PASSWORD},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": TEST_PASSWORD},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_workspace_invite_and_role_access(client: TestClient) -> None:
    owner_headers = _headers_for(client, "owner2@example.com")
    viewer_headers = _headers_for(client, "viewer@example.com")

    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Team Workspace", "slug": "team-workspace"},
        headers=owner_headers,
    )
    workspace_id = workspace.json()["id"]

    invite = client.post(
        f"/api/v1/workspaces/{workspace_id}/invites",
        json={"email": "viewer@example.com", "role": "viewer"},
        headers=owner_headers,
    )
    assert invite.status_code == 200
    invite_token = invite.json()["invite_token"]

    accepted = client.post(
        "/api/v1/workspaces/invites/accept",
        json={"invite_token": invite_token},
        headers=viewer_headers,
    )
    assert accepted.status_code == 200
    assert accepted.json()["role"] == "viewer"

    forbidden_update = client.put(
        f"/api/v1/workspaces/{workspace_id}",
        json={"client_report_title": "Should fail"},
        headers=viewer_headers,
    )
    assert forbidden_update.status_code == 403


def test_invite_resend_revoke_update_and_role_change(client: TestClient) -> None:
    owner_headers = _headers_for(client, "owner3@example.com")
    editor_headers = _headers_for(client, "editor@example.com")

    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Ops Workspace", "slug": "ops-workspace"},
        headers=owner_headers,
    )
    workspace_id = workspace.json()["id"]

    invite = client.post(
        f"/api/v1/workspaces/{workspace_id}/invites",
        json={"email": "editor@example.com", "role": "viewer"},
        headers=owner_headers,
    ).json()

    updated = client.put(
        f"/api/v1/workspaces/{workspace_id}/invites/{invite['id']}",
        json={"email": "editor@example.com", "role": "editor"},
        headers=owner_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["role"] == "editor"

    resent = client.post(
        f"/api/v1/workspaces/{workspace_id}/invites/{invite['id']}/resend",
        headers=owner_headers,
    )
    assert resent.status_code == 200
    assert resent.json()["sent_count"] >= 2

    accepted = client.post(
        "/api/v1/workspaces/invites/accept",
        json={"invite_token": invite["invite_token"]},
        headers=editor_headers,
    )
    assert accepted.status_code == 200
    member_id = accepted.json()["id"]

    role_changed = client.put(
        f"/api/v1/workspaces/{workspace_id}/members/{member_id}",
        json={"role": "admin"},
        headers=owner_headers,
    )
    assert role_changed.status_code == 200
    assert role_changed.json()["role"] == "admin"

    second_invite = client.post(
        f"/api/v1/workspaces/{workspace_id}/invites",
        json={"email": "temp@example.com", "role": "viewer"},
        headers=owner_headers,
    ).json()
    revoked = client.post(
        f"/api/v1/workspaces/{workspace_id}/invites/{second_invite['id']}/revoke",
        headers=owner_headers,
    )
    assert revoked.status_code == 200
    assert revoked.json()["status"] == "revoked"
