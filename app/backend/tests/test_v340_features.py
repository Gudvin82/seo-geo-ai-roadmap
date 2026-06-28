from __future__ import annotations


def test_command_catalog_endpoint_lists_routes(client) -> None:
    response = client.get("/api/v1/tools/command-catalog")
    assert response.status_code == 200
    payload = response.json()
    assert payload["routes"]
    commands = {item["command"] for item in payload["routes"]}
    assert {
        "audit",
        "llmstxt",
        "compare",
        "deploy",
        "scanner",
        "graph",
        "semantic",
        "proofpack",
    }.issubset(commands)
    audit = next(item for item in payload["routes"] if item["command"] == "audit")
    assert "scan" in audit["aliases"]
    assert "/geo audit" in audit["example_invocations"]


def test_command_router_returns_specific_route(client) -> None:
    response = client.post("/api/v1/tools/command-router", json={"command": "report"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["command"] == "report"
    assert "client-delivery" in " ".join(payload["recommended_docs"])
    assert payload["output_artifacts"]


def test_command_router_rejects_unknown_command(client) -> None:
    response = client.post(
        "/api/v1/tools/command-router",
        json={"command": "unknown-surface"},
    )
    assert response.status_code == 400
    assert "Unsupported command" in response.json()["detail"]


def test_command_router_supports_geo_prefix_and_alias(client) -> None:
    response = client.post(
        "/api/v1/tools/command-router", json={"command": "/geo scan"}
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["command"] == "audit"


def test_command_router_supports_new_semantic_and_proofpack_routes(client) -> None:
    semantic = client.post(
        "/api/v1/tools/command-router", json={"command": "semantics"}
    )
    assert semantic.status_code == 200
    assert semantic.json()["command"] == "semantic"

    proofpack = client.post(
        "/api/v1/tools/command-router", json={"command": "proof-pack"}
    )
    assert proofpack.status_code == 200
    assert proofpack.json()["command"] == "proofpack"
