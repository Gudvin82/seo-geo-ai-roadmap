import fs from "node:fs/promises";
import path from "node:path";

const playwrightModulePath =
  process.env.PLAYWRIGHT_MODULE_PATH || "playwright";
const { chromium } = await import(playwrightModulePath);

const outDir =
  process.argv[2] ||
  "/Users/macbook/Documents/New project/seo-geo-ai-roadmap/docs_site/assets/screenshots";

await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1400 } });

async function saveShot(name) {
  await page.screenshot({ path: path.join(outDir, name), fullPage: true });
}

async function apiCall(pathname, body) {
  return await page.evaluate(
    async ({ pathname, body }) => {
      const token =
        sessionStorage.getItem("discoverability-token") ||
        localStorage.getItem("discoverability-token");
      const response = await fetch(`http://127.0.0.1:8000/api/v1${pathname}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });
      const text = await response.text();
      return { ok: response.ok, status: response.status, text };
    },
    { pathname, body },
  );
}

await page.goto("http://127.0.0.1:3000", { waitUntil: "networkidle" });
await page.click('[data-pane-target="auth-pane"]');
await page.fill('#login-form input[name="email"]', "demo@example.com");
await page.fill('#login-form input[name="password"]', "DemoPlatform123");
await page.click('#login-form button[type="submit"]');
await page.waitForTimeout(2500);

await page.click('[data-pane-target="overview-pane"]');
await page.waitForTimeout(1000);
await saveShot("app-login-dashboard-proof.png");

await apiCall("/providers", {
  workspace_id: 1,
  provider_name: "openai",
  label: "Primary OpenAI",
  model: "gpt-4.1-mini",
  api_key_env_var: "OPENAI_API_KEY",
  is_enabled: true,
});

await page.click('[data-pane-target="providers-pane"]');
await page.click("#refresh-providers");
await page.waitForTimeout(1200);
await saveShot("app-provider-proof.png");

await apiCall("/audit-runs", {
  workspace_id: 1,
  project_id: 1,
  report_language: "en",
  provider_config_id: 1,
  selected_checks: [
    "robots_ai_bots",
    "llms_txt",
    "factual_consistency",
    "content_freshness",
  ],
});

await page.click('[data-pane-target="audits-pane"]');
await page.click("#refresh-audits");
await page.waitForTimeout(2500);
await saveShot("app-audit-proof.png");

await apiCall("/sov/check", {
  workspace_id: 1,
  project_id: 1,
  brand: "Demo Self-Hosted Site",
  queries: ["self-hosted SEO audit platform", "AI visibility workflow"],
  providers: ["openai", "perplexity"],
  language: "en",
});

await page.click('[data-pane-target="reports-pane"]');
await page.click("#refresh-reports");
await page.waitForTimeout(1500);
await saveShot("app-report-proof.png");

await browser.close();
console.log(JSON.stringify({ ok: true, outDir }, null, 2));
