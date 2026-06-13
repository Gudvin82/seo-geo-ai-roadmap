from __future__ import annotations

import contextlib
import io
import json
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(script_name: str, *args: str) -> tuple[int, str, str]:
    script = REPO_ROOT / "scripts" / script_name
    stdout = io.StringIO()
    stderr = io.StringIO()
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(script), *args]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 0
            else:
                code = 0
    finally:
        sys.argv = original_argv
    return code, stdout.getvalue(), stderr.getvalue()


def test_ai_readability_audit_warns_on_missing_layers(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        "<html><head><title>Home</title></head><body><p>Short text.</p></body></html>",
        encoding="utf-8",
    )
    code, stdout, _stderr = _run("ai_readability_audit.py", "--file", str(html_file))
    assert code == 1
    assert "Missing layers" in stdout


def test_citability_score_reports_breakdown(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        """
        <html><head>
        <title>AI discoverability consulting</title>
        <meta name="description" content="A detailed service page." />
        <meta property="og:title" content="AI discoverability consulting" />
        <meta property="og:description" content="A detailed service page." />
        <meta property="og:image" content="https://example.com/og.png" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://example.com/service" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="AI discoverability consulting" />
        <meta name="twitter:description" content="A detailed service page." />
        <meta name="twitter:image" content="https://example.com/og.png" />
        <link rel="canonical" href="https://example.com/service" />
        <script type="application/ld+json">{"@context":"https://schema.org","@type":["Organization","WebSite","Service"]}</script>
        </head><body>
        <section class="faq sr-only"><h2>FAQ</h2><h3>What is GEO?</h3></section>
        <h1>AI discoverability consulting</h1>
        <p>GEO is the practice of making structured answers easy to cite.</p>
        </body></html>
        """,
        encoding="utf-8",
    )
    code, stdout, _stderr = _run(
        "citability_score.py",
        "--file",
        str(html_file),
        "--site-type",
        "service",
    )
    assert code in {0, 1}
    assert "Citability score" in stdout
    assert "Breakdown" in stdout


def test_rag_chunk_audit_detects_long_blocks(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        "<html><body><h1>Guide</h1><p>"
        + ("Long section. " * 150)
        + "</p></body></html>",
        encoding="utf-8",
    )
    code, stdout, _stderr = _run("rag_chunk_audit.py", "--file", str(html_file))
    assert code == 1
    assert "Long blocks" in stdout


def test_crux_field_data_uses_sample_file(tmp_path: Path) -> None:
    sample = tmp_path / "crux.json"
    sample.write_text(
        json.dumps(
            {
                "record": {
                    "urlNormalizationDetails": {"originalUrl": "https://example.com"},
                    "metrics": {
                        "largest_contentful_paint": {"percentiles": {"p75": 2100}},
                        "interaction_to_next_paint": {"percentiles": {"p75": 180}},
                        "cumulative_layout_shift": {"percentiles": {"p75": 0.08}},
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    code, stdout, _stderr = _run("crux_field_data.py", "--sample-file", str(sample))
    assert code == 0
    assert "Metrics" in stdout


def test_integration_verification_matrix_json_renders() -> None:
    code, stdout, _stderr = _run("integration_verification_matrix.py", "--json")
    assert code == 0
    payload = json.loads(stdout)
    assert payload["rows"]
    assert any(row["source_type"] == "gsc" for row in payload["rows"])
