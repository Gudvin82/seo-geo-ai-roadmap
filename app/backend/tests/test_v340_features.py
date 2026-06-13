from __future__ import annotations


def test_command_catalog_endpoint_lists_routes(client) -> None:
    response = client.get("/api/v1/tools/command-catalog")
    assert response.status_code == 200
    payload = response.json()
    assert payload["routes"]
    commands = {item["command"] for item in payload["routes"]}
    assert {"audit", "llmstxt", "compare"}.issubset(commands)


def test_command_router_returns_specific_route(client) -> None:
    response = client.post("/api/v1/tools/command-router", json={"command": "report"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["command"] == "report"
    assert "client-delivery" in " ".join(payload["recommended_docs"])


def test_command_router_rejects_unknown_command(client) -> None:
    response = client.post(
        "/api/v1/tools/command-router",
        json={"command": "unknown-surface"},
    )
    assert response.status_code == 400
    assert "Unsupported command" in response.json()["detail"]
