const DEFAULT_API_BASE = "http://localhost:8000/api/v1";

async function getActiveTabUrl() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.url || "";
}

async function loadSettings() {
  const stored = await chrome.storage.local.get(["apiBase"]);
  document.getElementById("api").value = stored.apiBase || DEFAULT_API_BASE;
}

async function saveSettings() {
  const apiBase = document.getElementById("api").value.trim().replace(/\/$/, "");
  await chrome.storage.local.set({ apiBase });
  return apiBase;
}

function renderStatus(message, kind = "info") {
  const status = document.getElementById("status");
  status.dataset.kind = kind;
  status.textContent = message;
}

function renderResult(payload) {
  const links = [];
  if (payload.status_endpoint) {
    links.push(`status: ${payload.status_endpoint}`);
  }
  if (payload.result_endpoint) {
    links.push(`result: ${payload.result_endpoint}`);
  }
  if (payload.tasks_endpoint) {
    links.push(`tasks: ${payload.tasks_endpoint}`);
  }
  renderStatus(
    [
      `scan_job_id: ${payload.scan_job_id || "n/a"}`,
      `status: ${payload.initial_status || payload.status || "queued"}`,
      ...links,
    ].join("\n"),
    "success",
  );
}

document.getElementById("audit").addEventListener("click", async () => {
  try {
    const apiBase = await saveSettings();
    const url = await getActiveTabUrl();
    if (!url) {
      renderStatus("No active tab URL found.", "error");
      return;
    }
    renderStatus("Starting passive audit...", "info");
    const response = await fetch(`${apiBase}/scanner/url-audit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Scanner-Session": crypto.randomUUID(),
      },
      body: JSON.stringify({
        url,
        mode: "passive",
        site_type: "browser_extension",
        limitations_accepted: true,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      renderStatus(payload.detail || JSON.stringify(payload, null, 2), "error");
      return;
    }
    renderResult(payload);
  } catch (error) {
    renderStatus(error.message, "error");
  }
});

document.getElementById("save").addEventListener("click", async () => {
  const apiBase = await saveSettings();
  renderStatus(`Saved API base: ${apiBase}`, "success");
});

loadSettings().catch((error) => renderStatus(error.message, "error"));
