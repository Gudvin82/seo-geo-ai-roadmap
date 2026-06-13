(function () {
  const sessionKey = "discoverability-scanner-session";
  const state = {
    config: null,
    verificationRequestId: null,
    verificationVerified: false,
    verificationPayload: null,
    jobId: null,
    pollTimer: null,
  };

  const modeMeta = {
    passive: {
      summary:
        "Passive audit runs the safest public-surface review without ownership-gated active probing.",
      checked: [
        "Public URL normalization and SSRF-safe target validation",
        "Heuristic discoverability and crawlability review",
        "Stable export artifacts for operator follow-up",
      ],
      notChecked: [
        "Ownership-gated active interaction",
        "Authenticated surfaces or private networks",
        "Exploit-oriented or pentest behavior",
      ],
    },
    active: {
      summary:
        "Active scan extends the review path, but only after ownership verification and explicit consent.",
      checked: [
        "Ownership-gated active verification path",
        "Extended public-surface checks",
        "Event timeline, artifacts, and optional notifications",
      ],
      notChecked: [
        "Private network access",
        "Pentest-style exploitation",
        "Unlimited or anonymous probing outside configured limits",
      ],
    },
    full: {
      summary:
        "Full scan is the broadest configured mode and remains feature-flagged by default.",
      checked: [
        "Ownership-gated active verification path",
        "Extended public-surface checks",
        "Expanded export and notification flow",
      ],
      notChecked: [
        "Private network access",
        "Pentest-style exploitation",
        "Unbounded multi-tenant public scanning",
      ],
    },
  };

  const apiBaseInput = document.getElementById("scanner-api-base");
  const urlInput = document.getElementById("scanner-url");
  const modeSelect = document.getElementById("scanner-mode");
  const verificationMethodField = document.getElementById("verification-method-field");
  const verificationMethodSelect = document.getElementById("scanner-verification-method");
  const createVerificationButton = document.getElementById("scanner-create-verification");
  const checkVerificationButton = document.getElementById("scanner-check-verification");
  const ownershipWrap = document.getElementById("scanner-ownership-wrap");
  const loadWrap = document.getElementById("scanner-load-wrap");
  const ownershipCheckbox = document.getElementById("scanner-ownership-confirmed");
  const loadCheckbox = document.getElementById("scanner-load-accepted");
  const limitationsCheckbox = document.getElementById("scanner-limitations-accepted");
  const webhookInput = document.getElementById("scanner-webhook-url");
  const emailInput = document.getElementById("scanner-notification-email");
  const telegramInput = document.getElementById("scanner-telegram-chat-id");
  const formMessage = document.getElementById("scanner-form-message");
  const verificationBox = document.getElementById("scanner-verification-box");
  const limitationsBox = document.getElementById("scanner-limitations-box");
  const modeSummary = document.getElementById("scanner-mode-summary");
  const checkedList = document.getElementById("scanner-checked-list");
  const notCheckedList = document.getElementById("scanner-not-checked-list");
  const jobStatusBox = document.getElementById("scanner-job-status");
  const jobEvents = document.getElementById("scanner-job-events");
  const jobArtifacts = document.getElementById("scanner-job-artifacts");
  const progressShell = document.getElementById("scanner-job-progress");
  const progressBar = document.getElementById("scanner-job-progress-bar");
  const cancelButton = document.getElementById("scanner-cancel-job");

  function scannerSession() {
    let value = localStorage.getItem(sessionKey);
    if (!value) {
      value = crypto.randomUUID();
      localStorage.setItem(sessionKey, value);
    }
    return value;
  }

  function apiHeaders() {
    return {
      "Content-Type": "application/json",
      "X-Scanner-Session": scannerSession(),
    };
  }

  async function fetchJson(path, options = {}) {
    const response = await fetch(`${apiBaseInput.value}${path}`, options);
    if (!response.ok) {
      let detail = response.statusText;
      try {
        const payload = await response.json();
        detail = payload.detail || JSON.stringify(payload);
      } catch (_error) {
        detail = await response.text();
      }
      throw new Error(detail);
    }
    return response.json();
  }

  function renderModeMeta() {
    const mode = modeSelect.value;
    const meta = modeMeta[mode];
    modeSummary.textContent = meta.summary;
    checkedList.innerHTML = meta.checked.map((item) => `<li>${item}</li>`).join("");
    notCheckedList.innerHTML = meta.notChecked.map((item) => `<li>${item}</li>`).join("");
    const activeLike = mode !== "passive";
    verificationMethodField.classList.toggle("scanner-hidden", !activeLike);
    createVerificationButton.classList.toggle("scanner-hidden", !activeLike);
    checkVerificationButton.classList.toggle("scanner-hidden", !activeLike);
    ownershipWrap.classList.toggle("scanner-hidden", !activeLike);
    loadWrap.classList.toggle("scanner-hidden", !activeLike);
  }

  function renderConfig() {
    if (!state.config) return;
    limitationsBox.innerHTML = [
      `<strong>Configured modes</strong>`,
      `<div>Public intake: ${state.config.allow_public_intake ? "enabled" : "disabled"}</div>`,
      `<div>Active scan: ${state.config.allow_active_scan ? "enabled" : "disabled"}</div>`,
      `<div>Anonymous submission: ${state.config.allow_anonymous_submission ? "enabled" : "disabled"}</div>`,
      `<div>Full scan: ${state.config.allow_full_scan ? "enabled" : "disabled"}</div>`,
      `<div>Allowed schemes: ${state.config.allowed_schemes.join(", ")}</div>`,
      `<div>Max URL length: ${state.config.max_url_length}</div>`,
      `<div>Concurrent submissions per IP: ${state.config.max_concurrent_submissions_per_ip}</div>`,
      `<strong>Limitations</strong>`,
      `<ul>${state.config.limitations.map((item) => `<li>${item}</li>`).join("")}</ul>`,
    ].join("");
    const fullOption = modeSelect.querySelector('option[value="full"]');
    if (fullOption) {
      fullOption.disabled = !state.config.allow_full_scan;
    }
    const activeOption = modeSelect.querySelector('option[value="active"]');
    if (activeOption) {
      activeOption.disabled = !state.config.allow_active_scan;
    }
  }

  function setFormMessage(message, isError = false) {
    formMessage.textContent = message;
    formMessage.classList.toggle("error-box", isError);
  }

  function validateBeforeSubmit() {
    const mode = modeSelect.value;
    try {
      const parsed = new URL(urlInput.value.trim());
      if (!["http:", "https:"].includes(parsed.protocol)) {
        throw new Error("Only http and https targets are supported.");
      }
    } catch (error) {
      throw new Error("A valid absolute URL is required.");
    }
    if (!limitationsCheckbox.checked) {
      throw new Error("You must accept the scanner limitations.");
    }
    if (mode !== "passive") {
      if (!ownershipCheckbox.checked) {
        throw new Error("Ownership or authorization confirmation is required.");
      }
      if (!loadCheckbox.checked) {
        throw new Error("Active and full scans require load warning acceptance.");
      }
      if (!state.verificationVerified || !state.verificationRequestId) {
        throw new Error("Active and full scans require a verified ownership challenge.");
      }
    }
  }

  async function loadConfig() {
    try {
      state.config = await fetchJson("/scanner/config");
      renderConfig();
    } catch (error) {
      setFormMessage(`Unable to load scanner config: ${error.message}`, true);
    }
  }

  async function createVerificationChallenge() {
    setFormMessage("");
    try {
      const payload = await fetchJson("/scanner/verification-requests", {
        method: "POST",
        headers: apiHeaders(),
        body: JSON.stringify({
          url: urlInput.value.trim(),
          scan_mode: modeSelect.value,
          method: verificationMethodSelect.value,
        }),
      });
      state.verificationRequestId = payload.id;
      state.verificationPayload = payload;
      state.verificationVerified = false;
      verificationBox.classList.remove("scanner-hidden");
      verificationBox.innerHTML = [
        `<strong>Verification challenge created</strong>`,
        `<div>Method: ${payload.method}</div>`,
        payload.verification_path
          ? `<div>Place this file on the target: <code>${payload.verification_path}</code></div>`
          : "",
        payload.verification_meta_tag
          ? `<div>Add this meta tag: <code>${payload.verification_meta_tag}</code></div>`
          : "",
        payload.verification_dns_name
          ? `<div>Add TXT record on <code>${payload.verification_dns_name}</code> with value <code>${payload.challenge_value}</code></div>`
          : "",
        `<div>Challenge value: <code>${payload.challenge_value}</code></div>`,
      ].join("");
      setFormMessage("Verification challenge created. Publish it on the target, then verify.");
    } catch (error) {
      setFormMessage(error.message, true);
    }
  }

  async function verifyOwnershipChallenge() {
    if (!state.verificationRequestId) {
      setFormMessage("Create a verification challenge first.", true);
      return;
    }
    try {
      const payload = await fetchJson(
        `/scanner/verification-requests/${state.verificationRequestId}/verify`,
        {
          method: "POST",
          headers: apiHeaders(),
        },
      );
      state.verificationVerified = payload.status === "verified";
      verificationBox.classList.remove("scanner-hidden");
      verificationBox.innerHTML += `<div><strong>Status:</strong> ${payload.status}</div>`;
      setFormMessage(
        state.verificationVerified
          ? "Ownership verification succeeded."
          : "Ownership verification is still pending.",
        !state.verificationVerified,
      );
    } catch (error) {
      setFormMessage(error.message, true);
    }
  }

  async function createConsentRecord() {
    const mode = modeSelect.value;
    return fetchJson("/scanner/consent-records", {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({
        url: urlInput.value.trim(),
        scan_mode: mode,
        consent_scope: mode === "passive" ? "passive_ack" : "active_authorized",
        ownership_confirmed: ownershipCheckbox.checked,
        load_warning_accepted: loadCheckbox.checked,
        limitations_accepted: limitationsCheckbox.checked,
        verification_request_id: state.verificationRequestId,
      }),
    });
  }

  function renderJobStatus(job) {
    jobStatusBox.innerHTML = [
      `<strong>Status:</strong> ${job.status}`,
      `<div>Stage: ${job.current_stage}</div>`,
      `<div>Progress: ${job.progress_percent}%</div>`,
      job.error_summary ? `<div>Error: ${job.error_summary}</div>` : "",
    ].join("");
    progressShell.classList.remove("scanner-hidden");
    progressBar.style.width = `${job.progress_percent}%`;
    cancelButton.classList.toggle(
      "scanner-hidden",
      ["completed", "partial_success", "failed", "cancelled", "expired"].includes(job.status),
    );
  }

  async function fetchArtifact(artifact) {
    const response = await fetch(`${apiBaseInput.value}${artifact.download_endpoint}`, {
      headers: apiHeaders(),
    });
    if (!response.ok) {
      throw new Error("Artifact download failed.");
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = artifact.path.split("/").pop();
    anchor.click();
    URL.revokeObjectURL(url);
  }

  async function pollJob(jobId) {
    try {
      const job = await fetchJson(`/scan-jobs/${jobId}`, {
        headers: apiHeaders(),
      });
      renderJobStatus(job);
      const events = await fetchJson(`/scan-jobs/${jobId}/events`, {
        headers: apiHeaders(),
      });
      jobEvents.innerHTML = events
        .map((item) => `<li><strong>${item.status}</strong> · ${item.stage} · ${item.message}</li>`)
        .join("");
      const artifacts = await fetchJson(`/scan-jobs/${jobId}/artifacts`, {
        headers: apiHeaders(),
      });
      jobArtifacts.innerHTML = "";
      artifacts.forEach((artifact) => {
        const li = document.createElement("li");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "ghost-button";
        button.textContent = `${artifact.kind} (${artifact.format})`;
        button.addEventListener("click", async () => {
          try {
            await fetchArtifact(artifact);
          } catch (error) {
            setFormMessage(error.message, true);
          }
        });
        li.appendChild(button);
        jobArtifacts.appendChild(li);
      });
      if (["completed", "partial_success", "failed", "cancelled", "expired"].includes(job.status)) {
        clearInterval(state.pollTimer);
      }
    } catch (error) {
      setFormMessage(`Status polling failed: ${error.message}`, true);
      clearInterval(state.pollTimer);
    }
  }

  async function startScan(event) {
    event.preventDefault();
    setFormMessage("");
    try {
      validateBeforeSubmit();
      const consent = await createConsentRecord();
      const accepted = await fetchJson("/scan-jobs", {
        method: "POST",
        headers: apiHeaders(),
        body: JSON.stringify({
          url: urlInput.value.trim(),
          scan_mode: modeSelect.value,
          consent_record_id: consent.id,
          verification_request_id: state.verificationRequestId,
          callback_webhook_url: webhookInput.value.trim() || null,
          notification_email: emailInput.value.trim() || null,
          telegram_chat_id: telegramInput.value.trim() || null,
        }),
      });
      state.jobId = accepted.scan_job_id;
      setFormMessage(`Scan job ${accepted.scan_job_id} created.`);
      clearInterval(state.pollTimer);
      await pollJob(state.jobId);
      state.pollTimer = setInterval(() => pollJob(state.jobId), 2500);
    } catch (error) {
      setFormMessage(error.message, true);
    }
  }

  async function cancelCurrentJob() {
    if (!state.jobId) return;
    try {
      await fetchJson(`/scan-jobs/${state.jobId}/cancel`, {
        method: "POST",
        headers: apiHeaders(),
      });
      setFormMessage(`Cancellation requested for job ${state.jobId}.`);
      await pollJob(state.jobId);
    } catch (error) {
      setFormMessage(error.message, true);
    }
  }

  document.getElementById("scanner-intake-form").addEventListener("submit", startScan);
  modeSelect.addEventListener("change", renderModeMeta);
  createVerificationButton.addEventListener("click", createVerificationChallenge);
  checkVerificationButton.addEventListener("click", verifyOwnershipChallenge);
  cancelButton.addEventListener("click", cancelCurrentJob);

  renderModeMeta();
  loadConfig();
})();
