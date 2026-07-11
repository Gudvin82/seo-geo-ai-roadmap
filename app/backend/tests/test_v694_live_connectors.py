from __future__ import annotations

from app.services import live_connectors


class _Response:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def test_gsc_live_connector_uses_read_only_snapshot(monkeypatch) -> None:
    monkeypatch.setenv("GSC_ACCESS_TOKEN", "token")
    monkeypatch.setattr(
        live_connectors.httpx,
        "post",
        lambda *args, **kwargs: _Response(
            {
                "rows": [
                    {
                        "keys": ["seo audit", "https://example.com/"],
                        "clicks": 5,
                        "impressions": 20,
                        "ctr": 0.25,
                        "position": 3.2,
                    }
                ]
            }
        ),
    )
    payload = live_connectors.fetch_gsc_snapshot("sc-domain:example.com")
    assert payload["source"] == "gsc-live-api"
    assert payload["read_only"] is True
    assert payload["rows"][0]["query"] == "seo audit"


def test_yandex_webmaster_live_connector_fetches_host_summary(monkeypatch) -> None:
    monkeypatch.setenv("YANDEX_WEBMASTER_TOKEN", "token")
    responses = iter(
        [
            _Response({"user_id": 42}),
            _Response({"hosts": [{"host_id": "7", "host_url": "https://example.com"}]}),
            _Response({"site_problem_count": 0}),
        ]
    )
    monkeypatch.setattr(
        live_connectors.httpx, "get", lambda *args, **kwargs: next(responses)
    )
    payload = live_connectors.fetch_yandex_webmaster_snapshot("7")
    assert payload["source"] == "yandex-webmaster-live-api"
    assert payload["selected_host"]["host_id"] == "7"
    assert payload["summary"]["site_problem_count"] == 0
