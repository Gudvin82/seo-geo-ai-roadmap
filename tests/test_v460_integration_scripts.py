import contextlib
import io
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(script_name: str) -> dict:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        try:
            runpy.run_path(str(ROOT / "scripts" / script_name), run_name="__main__")
        except SystemExit as error:
            if error.code not in (0, None):
                raise
    return json.loads(stdout.getvalue())


def test_google_ads_stub_outputs_metrics() -> None:
    payload = _run("google_ads_stub.py")
    assert payload["source"] == "google-ads-stub"
    assert payload["metrics"]["conversions"] > 0


def test_indexnow_stub_outputs_submission_data() -> None:
    payload = _run("indexnow_stub.py")
    assert payload["source"] == "indexnow-stub"
    assert payload["metrics"]["accepted_urls"] >= 0


def test_business_and_distribution_stubs_output_metrics() -> None:
    for script_name, source in [
        ("google_business_profile_stub.py", "google-business-profile-stub"),
        ("yandex_business_stub.py", "yandex-business-stub"),
        ("merchant_center_stub.py", "merchant-center-stub"),
        ("meta_ads_stub.py", "meta-ads-stub"),
        ("vk_ads_stub.py", "vk-ads-stub"),
        ("telegram_ads_stub.py", "telegram-ads-stub"),
        ("youtube_analytics_stub.py", "youtube-analytics-stub"),
        ("linkedin_ads_stub.py", "linkedin-ads-stub"),
        (
            "instagram_facebook_organic_stub.py",
            "instagram-facebook-organic-stub",
        ),
    ]:
        payload = _run(script_name)
        assert payload["source"] == source
        assert payload["metrics"]
