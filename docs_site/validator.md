# Hosted Validator

<!-- markdownlint-disable MD033 -->

This page is the public `llms.txt` validator surface for `v3.3.0`.

- If GitHub Pages is enabled for the repository, this page becomes the public validator URL.
- It validates pasted `llms.txt` content fully in the browser.
- It can also try to fetch a public URL, but remote fetches may fail when the target blocks cross-origin access.

<div class="admonition note">
<p><strong>Honest status:</strong> this is a real public utility for pasted content and a best-effort URL checker for CORS-friendly targets. For sites that block browser fetches, use the repository API or paste the file contents.</p>
</div>

<section class="md-typeset">
  <label for="validator-url">Public URL</label>
  <input id="validator-url" type="url" placeholder="https://example.com/llms.txt" style="width: 100%; margin-bottom: 12px;" />
  <label for="validator-content">Or paste llms.txt</label>
  <textarea id="validator-content" rows="14" style="width: 100%; margin-bottom: 12px;" placeholder="# Example llms.txt&#10;- Home: https://example.com/&#10;- FAQ: https://example.com/faq&#10;- About: https://example.com/about"></textarea>
  <button id="validator-run">Run validation</button>
  <pre id="validator-output" style="margin-top: 16px; white-space: pre-wrap;">No validation run yet.</pre>
</section>

<script>
  const requiredHints = ["/", "faq", "about"];

  function validateText(content, checkedSource) {
    const lines = content.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
    const warnings = [];
    const recommendations = [];
    const bulletLike = lines.filter((line) => line.startsWith("-") || line.startsWith("*") || line.startsWith(">") || line.includes(" - "));
    const hasHeader = lines.some((line) => line.startsWith("#"));
    const hasUrl = lines.some((line) => /https?:\/\//i.test(line));
    const missing = requiredHints.filter((hint) => !lines.some((line) => line.toLowerCase().includes(hint)));

    if (!hasHeader) {
      warnings.push("Missing top-level heading.");
      recommendations.push("Add a top-level heading that explains what the file covers.");
    }
    if (!bulletLike.length) {
      warnings.push("Missing structured entries or bullet-like lines.");
      recommendations.push("List key pages, offers, policies, or fact hubs in a structured bullet format.");
    }
    if (!hasUrl) {
      warnings.push("No explicit absolute URLs detected.");
      recommendations.push("Add canonical URLs for priority pages.");
    }
    if (lines.length < 4) {
      warnings.push("The file is very short and may be under-specified.");
      recommendations.push("Expand the file with homepage, about, FAQ, contact, and trust pages.");
    }
    if (missing.length) {
      warnings.push(`Missing common hints: ${missing.join(", ")}.`);
      recommendations.push("Mention homepage, about/trust material, and FAQ or answer-ready sections explicitly.");
    }

    return {
      isValid: warnings.length === 0,
      checkedSource,
      lineCount: lines.length,
      warnings,
      recommendations,
    };
  }

  async function loadContent(urlValue, textValue) {
    if (textValue.trim()) return { content: textValue, source: "inline" };
    if (!urlValue.trim()) throw new Error("Paste llms.txt or provide a public URL.");
    const response = await fetch(urlValue);
    if (!response.ok) throw new Error(`Unable to fetch URL: ${response.status}`);
    return { content: await response.text(), source: urlValue };
  }

  document.getElementById("validator-run").addEventListener("click", async () => {
    const url = document.getElementById("validator-url").value;
    const content = document.getElementById("validator-content").value;
    const output = document.getElementById("validator-output");
    output.textContent = "Running validation...";
    try {
      const payload = await loadContent(url, content);
      const result = validateText(payload.content, payload.source);
      const parts = [
        `Status: ${result.isValid ? "PASS" : "FAIL"}`,
        `Checked source: ${result.checkedSource}`,
        `Non-empty lines: ${result.lineCount}`,
      ];
      if (result.warnings.length) {
        parts.push("", "Warnings:");
        for (const item of result.warnings) parts.push(`- ${item}`);
      }
      if (result.recommendations.length) {
        parts.push("", "Recommendations:");
        for (const item of result.recommendations) parts.push(`- ${item}`);
      }
      output.textContent = parts.join("\n");
    } catch (error) {
      output.textContent = `Error: ${error.message}\nTip: if the URL blocks browser fetches, paste the file contents instead.`;
    }
  });
</script>

<!-- markdownlint-enable MD033 -->
