const state = {
  token: localStorage.getItem("discoverability-token") || "",
  language: localStorage.getItem("discoverability-language") || "en",
  workspaces: [],
  projects: [],
  providerConfigs: [],
  auditRuns: [],
  reports: [],
  artifacts: [],
  presets: {},
  selectedWorkspaceId: "",
  selectedProjectId: "",
};

const translations = {
  en: {
    appTitle: "Discoverability OS App",
    appSubtitle:
      "Free and transparent self-hosted control panel for discoverability audits, multi-provider AI, and bilingual reporting.",
    apiBase: "API base",
    language: "Language",
    navAuth: "Auth",
    navWorkspaces: "Workspaces",
    navProjects: "Projects",
    navFacts: "Brand facts",
    navProviders: "Providers",
    navAudits: "Audit runs",
    navReports: "Reports",
    quickChecks: "Audit presets",
    demoAccess: "Demo access",
    releaseBadge: "v2.1.0 self-hosted hardening",
    heroTitle:
      "Free and transparent self-hosted platform on top of the methodology repo",
    heroCopy: "Create workspaces, onboard projects, run discoverability checks, store evidence, and ship bilingual reports with multi-provider AI support.",
    badgeRepo: "Repo methodology",
    badgeApp: "App workflow",
    badgeProviders: "OpenAI / Claude / Gemini / Perplexity",
    metricAuth: "Auth status",
    metricWorkspace: "Active workspace",
    metricProject: "Active project",
    metricReports: "Latest report language",
    authTitle: "Sign in / sign up",
    signOut: "Sign out",
    registerTitle: "Create account",
    password: "Password",
    registerAction: "Register",
    loginTitle: "Sign in",
    loginAction: "Log in",
    workspaceTitle: "Workspaces",
    refresh: "Refresh",
    createWorkspace: "Create workspace",
    name: "Name",
    defaultReportLanguage: "Default report language",
    reportTitle: "Client report title",
    reportSubtitle: "Client report subtitle",
    saveWorkspace: "Save workspace",
    workspaceList: "Workspace list",
    projectTitle: "Projects and sites",
    createProject: "Create project",
    workspaceId: "Workspace ID",
    websiteUrl: "Website URL",
    market: "Market",
    projectLanguage: "Language",
    projectType: "Project type",
    auditPreset: "Audit preset",
    saveProject: "Save project",
    projectList: "Project list",
    factsTitle: "Brand truth center",
    createFacts: "Create facts profile",
    projectId: "Project ID",
    profileName: "Profile name",
    factsMarkdown: "Facts markdown",
    approvedClaims: "Approved claims",
    forbiddenClaims: "Forbidden claims",
    numericFacts: "Numeric facts, comma-separated",
    markets: "Markets, comma-separated",
    languages: "Languages, comma-separated",
    saveFacts: "Save facts profile",
    factsList: "Facts profiles",
    providersTitle: "Provider settings",
    createProvider: "Create provider config",
    providerName: "Provider",
    label: "Label",
    model: "Model",
    apiEnv: "API key env var",
    saveProvider: "Save provider config",
    providerList: "Provider list",
    auditsTitle: "Structured audit runs",
    createAudit: "Create audit run",
    reportLanguage: "Report language",
    providerConfig: "Provider config ID",
    checks: "Checks",
    runAudit: "Run audit",
    auditList: "Audit runs",
    reportsTitle: "Reports and artifacts",
    reportList: "Reports",
    artifactList: "Artifacts",
    repoAssets: "Repo assets reused by the app",
    activityLog: "Activity log",
  },
  ru: {
    appTitle: "Discoverability OS App",
    appSubtitle:
      "Бесплатная и прозрачная self-hosted панель для discoverability-аудитов, мультипровайдерного AI и двуязычной отчетности.",
    apiBase: "База API",
    language: "Язык",
    navAuth: "Авторизация",
    navWorkspaces: "Воркспейсы",
    navProjects: "Проекты",
    navFacts: "Бренд-факты",
    navProviders: "Провайдеры",
    navAudits: "Аудиты",
    navReports: "Отчеты",
    quickChecks: "Audit presets",
    demoAccess: "Demo access",
    releaseBadge: "v2.1.0 self-hosted hardening",
    heroTitle:
      "Бесплатная и прозрачная self-hosted платформа поверх методологического репозитория",
    heroCopy: "Создавайте воркспейсы, онбордите проекты, запускайте discoverability-проверки, храните evidence и выпускайте двуязычные отчеты с multi-provider AI.",
    badgeRepo: "Методология репо",
    badgeApp: "Продуктовый workflow",
    badgeProviders: "OpenAI / Claude / Gemini / Perplexity",
    metricAuth: "Статус авторизации",
    metricWorkspace: "Активный воркспейс",
    metricProject: "Активный проект",
    metricReports: "Язык последнего отчета",
    authTitle: "Вход / регистрация",
    signOut: "Выйти",
    registerTitle: "Создать аккаунт",
    password: "Пароль",
    registerAction: "Зарегистрироваться",
    loginTitle: "Войти",
    loginAction: "Войти",
    workspaceTitle: "Воркспейсы",
    refresh: "Обновить",
    createWorkspace: "Создать воркспейс",
    name: "Название",
    defaultReportLanguage: "Язык отчетов по умолчанию",
    reportTitle: "Заголовок клиентского отчета",
    reportSubtitle: "Подзаголовок клиентского отчета",
    saveWorkspace: "Сохранить воркспейс",
    workspaceList: "Список воркспейсов",
    projectTitle: "Проекты и сайты",
    createProject: "Создать проект",
    workspaceId: "ID воркспейса",
    websiteUrl: "URL сайта",
    market: "Рынок",
    projectLanguage: "Язык",
    projectType: "Тип проекта",
    auditPreset: "Audit preset",
    saveProject: "Сохранить проект",
    projectList: "Список проектов",
    factsTitle: "Brand truth center",
    createFacts: "Создать facts profile",
    projectId: "ID проекта",
    profileName: "Название профиля",
    factsMarkdown: "Facts markdown",
    approvedClaims: "Разрешенные claims",
    forbiddenClaims: "Запрещенные claims",
    numericFacts: "Числовые факты через запятую",
    markets: "Рынки через запятую",
    languages: "Языки через запятую",
    saveFacts: "Сохранить facts profile",
    factsList: "Профили фактов",
    providersTitle: "Настройки провайдеров",
    createProvider: "Создать конфиг провайдера",
    providerName: "Провайдер",
    label: "Label",
    model: "Модель",
    apiEnv: "Переменная окружения для API ключа",
    saveProvider: "Сохранить конфиг провайдера",
    providerList: "Список провайдеров",
    auditsTitle: "Структурированные audit runs",
    createAudit: "Создать audit run",
    reportLanguage: "Язык отчета",
    providerConfig: "ID конфигурации провайдера",
    checks: "Проверки",
    runAudit: "Запустить аудит",
    auditList: "Список audit runs",
    reportsTitle: "Отчеты и артефакты",
    reportList: "Отчеты",
    artifactList: "Артефакты",
    repoAssets: "Репозиторные assets, которые переиспользует приложение",
    activityLog: "Журнал активности",
  },
};

function $(selector) {
  return document.querySelector(selector);
}

function currentDictionary() {
  return translations[state.language] || translations.en;
}

function apiBase() {
  return $("#api-base").value.replace(/\/$/, "");
}

function authHeaders() {
  return state.token ? { Authorization: `Bearer ${state.token}` } : {};
}

function log(message, tone = "") {
  const entry = document.createElement("div");
  entry.className = `log-entry ${tone}`.trim();
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  $("#activity-log").prepend(entry);
}

function setStatus() {
  $("#auth-status").textContent = state.token ? "Signed in" : "Signed out";
  $("#workspace-status").textContent = state.selectedWorkspaceId || "n/a";
  $("#project-status").textContent = state.selectedProjectId || "n/a";
  const lastReport = state.reports[0];
  $("#report-language-status").textContent = lastReport ? lastReport.language : "n/a";
}

function switchPane(paneId) {
  document.querySelectorAll(".pane").forEach((pane) => pane.classList.toggle("is-active", pane.id === paneId));
  document.querySelectorAll(".nav-link").forEach((button) => button.classList.toggle("is-active", button.dataset.paneTarget === paneId));
}

function applyTranslations() {
  const dict = currentDictionary();
  document.documentElement.lang = state.language;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.dataset.i18n;
    if (dict[key]) {
      node.textContent = dict[key];
    }
  });
}

function splitCsv(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${apiBase()}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const payload = await response.text();
    throw new Error(payload || `Request failed with ${response.status}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

function renderPresets() {
  const presetList = $("#preset-list");
  const projectPreset = $("#project-preset");
  presetList.innerHTML = "";
  projectPreset.innerHTML = "";
  Object.entries(state.presets).forEach(([name, checks]) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = `${name} (${checks.length})`;
    projectPreset.append(option);

    const item = document.createElement("li");
    item.textContent = `${name}: ${checks.join(", ")}`;
    presetList.append(item);
  });
}

function renderCards(target, rows, mapper) {
  const node = $(target);
  node.innerHTML = "";
  if (!rows.length) {
    node.innerHTML = `<div class="entity-card">No data yet.</div>`;
    return;
  }
  rows.forEach((row) => node.append(mapper(row)));
}

function workspaceCard(workspace) {
  const card = document.createElement("article");
  card.className = "entity-card";
  card.innerHTML = `
    <strong>${workspace.name}</strong>
    <div class="workspace-meta">#${workspace.id} · ${workspace.slug} · ${workspace.default_report_language}</div>
    <div class="workspace-meta">${workspace.client_report_title || "No white-label title yet."}</div>
  `;
  card.addEventListener("click", () => {
    state.selectedWorkspaceId = String(workspace.id);
    document.querySelectorAll("input[name='workspace_id']").forEach((input) => {
      input.value = workspace.id;
    });
    setStatus();
    log(`Workspace #${workspace.id} selected.`);
  });
  return card;
}

function projectCard(project) {
  const card = document.createElement("article");
  card.className = "entity-card";
  card.innerHTML = `
    <strong>${project.name}</strong>
    <div class="project-meta">#${project.id} · ${project.website_url}</div>
    <div class="project-meta">${project.market} · ${project.language} · ${project.project_type}</div>
  `;
  card.addEventListener("click", async () => {
    state.selectedProjectId = String(project.id);
    document.querySelectorAll("input[name='project_id']").forEach((input) => {
      input.value = project.id;
    });
    setStatus();
    log(`Project #${project.id} selected.`);
    await refreshReportsAndArtifacts();
  });
  return card;
}

function simpleCard(title, lines) {
  const card = document.createElement("article");
  card.className = "entity-card";
  card.innerHTML = `<strong>${title}</strong>${lines.map((line) => `<div class="project-meta">${line}</div>`).join("")}`;
  return card;
}

async function refreshPresets() {
  const payload = await apiRequest("/audit-runs/presets", { headers: {} });
  state.presets = payload.presets || {};
  renderPresets();
}

async function refreshWorkspaces() {
  if (!state.token) {
    return;
  }
  state.workspaces = await apiRequest("/workspaces");
  renderCards("#workspace-list", state.workspaces, workspaceCard);
}

async function refreshProjects() {
  if (!state.token || !state.selectedWorkspaceId) {
    return;
  }
  state.projects = await apiRequest(`/projects?workspace_id=${state.selectedWorkspaceId}`);
  renderCards("#project-list", state.projects, projectCard);
}

async function refreshFacts() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const rows = await apiRequest(`/brand-facts/${state.selectedProjectId}`);
  renderCards("#facts-list", rows, (row) =>
    simpleCard(row.name, [
      `Project #${row.project_id}`,
      `Markets: ${(row.markets || []).join(", ") || "n/a"}`,
      `Languages: ${(row.languages || []).join(", ") || "n/a"}`,
    ]),
  );
}

async function refreshProviders() {
  if (!state.token || !state.selectedWorkspaceId) {
    return;
  }
  state.providerConfigs = await apiRequest(`/providers?workspace_id=${state.selectedWorkspaceId}`);
  renderCards("#provider-list", state.providerConfigs, (row) =>
    simpleCard(row.label, [`#${row.id}`, `${row.provider_name} · ${row.model}`, row.api_key_env_var || "default env routing"]),
  );
}

async function refreshAudits() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  state.auditRuns = await apiRequest(`/audit-runs?project_id=${state.selectedProjectId}`);
  renderCards("#audit-list", state.auditRuns, (row) =>
    simpleCard(`Audit #${row.id}`, [
      `${row.status} · score: ${row.summary_score ?? "pending"}`,
      `Checks: ${(row.selected_checks || []).join(", ")}`,
      `Language: ${row.report_language}`,
    ]),
  );
}

async function refreshReportsAndArtifacts() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const [reports, artifacts, repoAssets] = await Promise.all([
    apiRequest(`/reports?project_id=${state.selectedProjectId}`),
    apiRequest(`/artifacts?project_id=${state.selectedProjectId}`),
    apiRequest("/settings/repo-assets"),
  ]);
  state.reports = reports;
  state.artifacts = artifacts;
  renderCards("#report-list", reports, (row) =>
    simpleCard(`Report #${row.id}`, [`${row.language} · ${row.format}`, `Audit run #${row.audit_run_id}`, `${row.summary_markdown.slice(0, 110)}...`]),
  );
  renderCards("#artifact-list", artifacts, (row) =>
    simpleCard(`${row.artifact_type}`, [`#${row.id} · ${row.format}`, row.file_path, `Audit run #${row.audit_run_id}`]),
  );
  $("#repo-assets").textContent = JSON.stringify(repoAssets, null, 2);
  setStatus();
}

function formPayload(form) {
  return Object.fromEntries(new FormData(form).entries());
}

async function handleRegister(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  await apiRequest("/auth/register", { method: "POST", body: JSON.stringify(payload) });
  log(`Registered ${payload.email}.`);
  event.currentTarget.reset();
}

async function handleLogin(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  const data = await apiRequest("/auth/login", { method: "POST", body: JSON.stringify(payload) });
  state.token = data.access_token;
  localStorage.setItem("discoverability-token", state.token);
  log(`Signed in as ${payload.email}.`);
  setStatus();
  await bootstrapAuthedState();
}

async function handleWorkspaceCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  const workspace = await apiRequest("/workspaces", { method: "POST", body: JSON.stringify(payload) });
  state.selectedWorkspaceId = String(workspace.id);
  log(`Workspace ${workspace.name} created.`);
  event.currentTarget.reset();
  await refreshWorkspaces();
  setStatus();
}

async function handleProjectCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  const project = await apiRequest("/projects", { method: "POST", body: JSON.stringify(payload) });
  state.selectedProjectId = String(project.id);
  log(`Project ${project.name} created.`);
  event.currentTarget.reset();
  await refreshProjects();
  setStatus();
}

async function handleFactsCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.project_id = Number(payload.project_id);
  payload.numeric_facts = splitCsv(payload.numeric_facts);
  payload.markets = splitCsv(payload.markets);
  payload.languages = splitCsv(payload.languages);
  await apiRequest("/brand-facts", { method: "POST", body: JSON.stringify(payload) });
  log(`Brand facts profile saved for project #${payload.project_id}.`);
  event.currentTarget.reset();
  await refreshFacts();
}

async function handleProviderCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.is_enabled = true;
  await apiRequest("/providers", { method: "POST", body: JSON.stringify(payload) });
  log(`Provider config ${payload.label} saved.`);
  event.currentTarget.reset();
  await refreshProviders();
}

async function handleAuditCreate(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = formPayload(form);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  payload.provider_config_id = payload.provider_config_id ? Number(payload.provider_config_id) : null;
  payload.selected_checks = [...form.querySelectorAll("input[type='checkbox']:checked")].map((input) => input.value);
  const audit = await apiRequest("/audit-runs", { method: "POST", body: JSON.stringify(payload) });
  log(`Audit run #${audit.id} queued.`);
  await refreshAudits();
  await refreshReportsAndArtifacts();
}

async function bootstrapAuthedState() {
  if (!state.token) {
    return;
  }
  await refreshWorkspaces();
  if (!state.selectedWorkspaceId && state.workspaces[0]) {
    state.selectedWorkspaceId = String(state.workspaces[0].id);
  }
  if (state.selectedWorkspaceId) {
    await refreshProjects();
  }
  if (!state.selectedProjectId && state.projects[0]) {
    state.selectedProjectId = String(state.projects[0].id);
  }
  if (state.selectedProjectId) {
    await Promise.all([refreshFacts(), refreshProviders(), refreshAudits(), refreshReportsAndArtifacts()]);
  }
  setStatus();
}

function installEventListeners() {
  document.querySelectorAll(".nav-link").forEach((button) =>
    button.addEventListener("click", () => switchPane(button.dataset.paneTarget)),
  );
  $("#language-switcher").value = state.language;
  $("#language-switcher").addEventListener("change", (event) => {
    state.language = event.target.value;
    localStorage.setItem("discoverability-language", state.language);
    applyTranslations();
  });
  $("#register-form").addEventListener("submit", handleRegister);
  $("#login-form").addEventListener("submit", handleLogin);
  $("#workspace-form").addEventListener("submit", handleWorkspaceCreate);
  $("#project-form").addEventListener("submit", handleProjectCreate);
  $("#facts-form").addEventListener("submit", handleFactsCreate);
  $("#provider-form").addEventListener("submit", handleProviderCreate);
  $("#audit-form").addEventListener("submit", handleAuditCreate);
  $("#refresh-workspaces").addEventListener("click", () => refreshWorkspaces().catch((error) => log(error.message, "warning")));
  $("#refresh-projects").addEventListener("click", () => refreshProjects().catch((error) => log(error.message, "warning")));
  $("#refresh-facts").addEventListener("click", () => refreshFacts().catch((error) => log(error.message, "warning")));
  $("#refresh-providers").addEventListener("click", () => refreshProviders().catch((error) => log(error.message, "warning")));
  $("#refresh-audits").addEventListener("click", () => refreshAudits().catch((error) => log(error.message, "warning")));
  $("#refresh-reports").addEventListener("click", () => refreshReportsAndArtifacts().catch((error) => log(error.message, "warning")));
  $("#sign-out").addEventListener("click", () => {
    state.token = "";
    localStorage.removeItem("discoverability-token");
    log("Signed out.");
    setStatus();
  });
}

async function init() {
  installEventListeners();
  applyTranslations();
  setStatus();
  try {
    await refreshPresets();
    await bootstrapAuthedState();
  } catch (error) {
    log(`Startup warning: ${error.message}`, "warning");
  }
}

init();
