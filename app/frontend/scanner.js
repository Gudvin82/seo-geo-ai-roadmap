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
  const siteTypeInput = document.getElementById("scanner-site-type");
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
  const resultSummary = document.getElementById("scanner-result-summary");
  const resultRecommendations = document.getElementById("scanner-result-recommendations");
  const resultIssues = document.getElementById("scanner-result-issues");
  const resultTasksLink = document.getElementById("scanner-result-tasks");
  const resultGraphLink = document.getElementById("scanner-result-graph");
  const progressShell = document.getElementById("scanner-job-progress");
  const progressBar = document.getElementById("scanner-job-progress-bar");
  const cancelButton = document.getElementById("scanner-cancel-job");

  function sessionStoreGet(key) {
    try {
      return sessionStorage.getItem(key);
    } catch (_error) {
      return null;
    }
  }

  function sessionStoreSet(key, value) {
    try {
      sessionStorage.setItem(key, value);
    } catch (_error) {}
  }

  function resetNode(node, className = "", text = "") {
    node.replaceChildren();
    if (text) {
      const child = document.createElement("div");
      if (className) child.className = className;
      child.textContent = text;
      node.appendChild(child);
    }
  }

  function appendLine(node, text, strongLabel = "") {
    const row = document.createElement("div");
    if (strongLabel) {
      const strong = document.createElement("strong");
      strong.textContent = strongLabel;
      row.appendChild(strong);
      row.append(` ${text}`);
    } else {
      row.textContent = text;
    }
    node.appendChild(row);
  }

  function renderList(node, items, mapper) {
    node.replaceChildren();
    items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = mapper(item);
      node.appendChild(li);
    });
  }

  function scannerSession() {
    let value = sessionStoreGet(sessionKey);
    if (!value) {
      value = crypto.randomUUID();
      sessionStoreSet(sessionKey, value);
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
    renderList(checkedList, meta.checked, (item) => item);
    renderList(notCheckedList, meta.notChecked, (item) => item);
    const activeLike = mode !== "passive";
    verificationMethodField.classList.toggle("scanner-hidden", !activeLike);
    createVerificationButton.classList.toggle("scanner-hidden", !activeLike);
    checkVerificationButton.classList.toggle("scanner-hidden", !activeLike);
    ownershipWrap.classList.toggle("scanner-hidden", !activeLike);
    loadWrap.classList.toggle("scanner-hidden", !activeLike);
  }

  function renderConfig() {
    if (!state.config) return;
    limitationsBox.replaceChildren();
    const title = document.createElement("strong");
    title.textContent = "Configured modes";
    limitationsBox.appendChild(title);
    appendLine(
      limitationsBox,
      state.config.allow_public_intake ? "enabled" : "disabled",
      "Public intake:",
    );
    appendLine(
      limitationsBox,
      state.config.allow_active_scan ? "enabled" : "disabled",
      "Active scan:",
    );
    appendLine(
      limitationsBox,
      state.config.allow_anonymous_submission ? "enabled" : "disabled",
      "Anonymous submission:",
    );
    appendLine(
      limitationsBox,
      state.config.allow_full_scan ? "enabled" : "disabled",
      "Full scan:",
    );
    appendLine(
      limitationsBox,
      state.config.allowed_schemes.join(", "),
      "Allowed schemes:",
    );
    appendLine(
      limitationsBox,
      String(state.config.max_url_length),
      "Max URL length:",
    );
    appendLine(
      limitationsBox,
      String(state.config.max_concurrent_submissions_per_ip),
      "Concurrent submissions per IP:",
    );
    const limitationsTitle = document.createElement("strong");
    limitationsTitle.textContent = "Limitations";
    limitationsBox.appendChild(limitationsTitle);
    const list = document.createElement("ul");
    (state.config.limitations || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      list.appendChild(li);
    });
    limitationsBox.appendChild(list);
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
      verificationBox.replaceChildren();
      const title = document.createElement("strong");
      title.textContent = "Verification challenge created";
      verificationBox.appendChild(title);
      appendLine(verificationBox, payload.method, "Method:");
      if (payload.verification_path) {
        appendLine(
          verificationBox,
          payload.verification_path,
          "Place this file on the target:",
        );
      }
      if (payload.verification_meta_tag) {
        appendLine(
          verificationBox,
          payload.verification_meta_tag,
          "Add this meta tag:",
        );
      }
      if (payload.verification_dns_name) {
        appendLine(
          verificationBox,
          `${payload.verification_dns_name} = ${payload.challenge_value}`,
          "Add TXT record:",
        );
      }
      appendLine(verificationBox, payload.challenge_value, "Challenge value:");
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
      appendLine(verificationBox, payload.status, "Status:");
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
    jobStatusBox.replaceChildren();
    appendLine(jobStatusBox, job.status, "Status:");
    appendLine(jobStatusBox, job.current_stage, "Stage:");
    appendLine(jobStatusBox, `${job.progress_percent}%`, "Progress:");
    if (job.error_summary) {
      appendLine(jobStatusBox, job.error_summary, "Error:");
    }
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
      renderList(
        jobEvents,
        events,
        (item) => `${item.status} · ${item.stage} · ${item.message}`,
      );
      const artifacts = await fetchJson(`/scan-jobs/${jobId}/artifacts`, {
        headers: apiHeaders(),
      });
      jobArtifacts.replaceChildren();
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
        if (["completed", "partial_success"].includes(job.status)) {
          await loadJobResult(jobId);
        }
      }
    } catch (error) {
      setFormMessage(`Status polling failed: ${error.message}`, true);
      clearInterval(state.pollTimer);
    }
  }

  async function loadJobResult(jobId) {
    try {
      const payload = await fetchJson(`/scan-jobs/${jobId}/result`, {
        headers: apiHeaders(),
      });
      resultSummary.replaceChildren();
      const title = document.createElement("strong");
      title.textContent = payload.target_domain;
      resultSummary.appendChild(title);
      appendLine(resultSummary, payload.executive_summary);
      if (siteTypeInput.value.trim()) {
        appendLine(resultSummary, siteTypeInput.value.trim(), "Site type hint:");
      }
      appendLine(resultSummary, payload.scan_mode, "Mode:");
      renderList(resultRecommendations, payload.recommendations || [], (item) => item);
      renderList(
        resultIssues,
        payload.issues || [],
        (item) => `${item.severity} · ${item.title}`,
      );
      resultTasksLink.href = `${apiBaseInput.value}${payload.tasks_endpoint}`;
      resultGraphLink.href = `./graph.html?api=${encodeURIComponent(apiBaseInput.value)}&source=scan_job&id=${jobId}`;
      resultTasksLink.classList.remove("scanner-hidden");
      resultGraphLink.classList.remove("scanner-hidden");
    } catch (error) {
      setFormMessage(`Result loading failed: ${error.message}`, true);
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
