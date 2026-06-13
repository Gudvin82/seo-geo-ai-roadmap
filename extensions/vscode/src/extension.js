const vscode = require("vscode");
const crypto = require("crypto");

function settings() {
  const config = vscode.workspace.getConfiguration("seoGeoAi");
  return {
    apiBase: (config.get("apiBase") || "http://localhost:8000/api/v1").replace(/\/$/, ""),
    authToken: config.get("authToken") || "",
  };
}

function headers() {
  const { authToken } = settings();
  const baseHeaders = { "Content-Type": "application/json" };
  if (authToken) {
    baseHeaders.Authorization = `Bearer ${authToken}`;
  }
  return baseHeaders;
}

async function request(path, options = {}) {
  const { apiBase } = settings();
  const response = await fetch(`${apiBase}${path}`, {
    ...options,
    headers: {
      ...headers(),
      ...(options.headers || {}),
    },
  });
  const text = await response.text();
  try {
    const payload = JSON.parse(text);
    if (!response.ok) {
      throw new Error(payload.detail || JSON.stringify(payload, null, 2));
    }
    return payload;
  } catch (error) {
    if (!response.ok) {
      throw new Error(text || response.statusText);
    }
    throw error;
  }
}

async function showJsonPanel(title, payload) {
  const panel = vscode.window.createWebviewPanel(
    "seoGeoAi",
    title,
    vscode.ViewColumn.One,
    {},
  );
  panel.webview.html = `
    <html>
      <body>
        <h1>${title}</h1>
        <pre>${JSON.stringify(payload, null, 2)}</pre>
      </body>
    </html>
  `;
}

async function runAudit() {
  const url = await vscode.window.showInputBox({
    prompt: "Enter the public URL to audit",
    placeHolder: "https://example.com",
  });
  if (!url) {
    return;
  }
  const payload = await request("/scanner/url-audit", {
    method: "POST",
    headers: {
      "X-Scanner-Session": crypto.randomUUID(),
    },
    body: JSON.stringify({
      url,
      mode: "passive",
      site_type: "vscode_extension",
      limitations_accepted: true,
    }),
  });
  await showJsonPanel("SEO GEO AI Audit", payload);
}

async function openSummary() {
  const projectId = await vscode.window.showInputBox({
    prompt: "Enter project id for executive dashboard",
    placeHolder: "1",
  });
  if (!projectId) {
    return;
  }
  const payload = await request(`/settings/executive-dashboard?project_id=${projectId}`);
  await showJsonPanel("SEO GEO AI Executive Dashboard", payload);
}

async function startAgentMode() {
  const projectId = await vscode.window.showInputBox({
    prompt: "Enter project id for agent mode",
    placeHolder: "1",
  });
  if (!projectId) {
    return;
  }
  const payload = await request("/agent-mode/runs", {
    method: "POST",
    body: JSON.stringify({
      project_id: Number(projectId),
      mode: "agent-plan",
      source_type: "audit_run",
    }),
  });
  await showJsonPanel("SEO GEO AI Agent Mode", payload);
}

function registerCommand(context, command, handler) {
  context.subscriptions.push(
    vscode.commands.registerCommand(command, async () => {
      try {
        await handler();
      } catch (error) {
        vscode.window.showErrorMessage(error.message);
      }
    }),
  );
}

function activate(context) {
  registerCommand(context, "seoGeoAi.audit", runAudit);
  registerCommand(context, "seoGeoAi.summary", openSummary);
  registerCommand(context, "seoGeoAi.agentMode", startAgentMode);
}

function deactivate() {}

module.exports = { activate, deactivate };
