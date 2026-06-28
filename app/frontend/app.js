function readSessionValue(key) {
  try {
    return sessionStorage.getItem(key) || "";
  } catch (_error) {
    return "";
  }
}

function writeSessionValue(key, value) {
  try {
    sessionStorage.setItem(key, value);
  } catch (_error) {}
}

function removeSessionValue(key) {
  try {
    sessionStorage.removeItem(key);
  } catch (_error) {}
}

function readLocalValue(key, fallback = "") {
  try {
    return localStorage.getItem(key) || fallback;
  } catch (_error) {
    return fallback;
  }
}

const state = {
  token: readSessionValue("discoverability-token"),
  language: readLocalValue("discoverability-language", "en"),
  workspaces: [],
  projects: [],
  providerConfigs: [],
  integrationConnections: [],
  cmsConnectors: [],
  promptSets: [],
  auditRuns: [],
  reports: [],
  artifacts: [],
  sovRuns: [],
  notificationEndpoints: [],
  productModes: [],
  ciGating: {},
  executiveDashboard: null,
  organizations: [],
  organizationSwitcher: {},
  saasCatalog: [],
  tenantOverview: null,
  portfolioDashboard: {},
  demoCenter: {},
  productizationCenter: {},
  saasGrowthCenter: {},
  saasReadinessCenter: {},
  deploymentPosture: {},
  runtimeOpsCenter: {},
  seoMaturityCenter: {},
  evidenceLab: {},
  proofTimeline: [],
  proofEvidence: [],
  proofExperiments: [],
  proofOpsCenter: {},
  proofKit: {},
  proofExportPack: {},
  mentionReputationCenter: {},
  operatorBoard: {},
  generationContracts: {},
  generationManifests: [],
  generationOutput: null,
  oneLinkBuilder: {},
  repoUnderstanding: {},
  deployWizard: {},
  promptPacks: {},
  socialDistributionCenter: {},
  socialIntelligenceCenter: {},
  socialCommandCenter: {},
  socialParserOutput: {},
  localEntityCenter: {},
  ruMarketCommandCenter: {},
  providerHealthCenter: {},
  providerModelRegistry: {},
  providerOperatingCenter: {},
  integrationRuntimeCenter: {},
  integrationHealthCenter: {},
  integrationContracts: [],
  cmsContracts: [],
  reportAssistant: null,
  presets: {},
  selectedWorkspaceId: "",
  selectedProjectId: "",
};

const translations = {
  en: {
    navOverview: "Overview",
    navExecutive: "Executive",
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
    navIntegrations: "Integrations",
    navCms: "CMS",
    navPrompts: "Prompt library",
    navAudits: "Audit runs",
    navSov: "AI SoV",
    navNotifications: "Notifications",
    navDeliverables: "Deliverables",
    navReports: "Reports",
    quickChecks: "Audit presets",
    demoAccess: "Demo access",
    releaseBadge:
      "v6.5.0 runtime ops, SEO maturity, and evidence lab delivery",
    heroTitle:
      "Self-hosted daily operating system for SEO, GEO, and AI discoverability",
    heroCopy:
      "Give the repo to a human operator or an AI coding agent, deploy it, connect providers, run audits, collect evidence, and re-run on the same sites with measurable deltas.",
    badgeRepo: "Repo methodology",
    badgeApp: "App workflow",
    badgeProviders:
      "OpenAI / Claude / Gemini / Google Ads / Yandex / CrUX / Meta / VK / Ollama / LM Studio",
    metricAuth: "Auth status",
    metricWorkspace: "Active workspace",
    metricProject: "Active project",
    metricReports: "Latest report language",
    metricCitation: "Latest AI citation signal",
    overviewTitle: "Operator overview",
    first15Title: "First result in 15 minutes",
    first15Step1: "Sign in and create one workspace.",
    first15Step2: "Create one project and fill brand facts.",
    first15Step3: "Connect one provider or stay in transparent starter mode.",
    first15Step4: "Run one audit and one AI SoV check.",
    first15Step5: "Open reports, artifacts, and export package.",
    day30Title: "What changes in 30 days",
    day30Item1: "You have a repeatable audit rhythm, not one-off checklists.",
    day30Item2: "Facts, prompts, and reports stay in one operator system.",
    day30Item3: "You can show deltas in score, evidence, and AI visibility.",
    day90Title: "What changes in 90 days",
    day90Item1: "Agency, in-house, and founder workflows become reusable.",
    day90Item2: "You have a bilingual evidence base for fixes and client delivery.",
    day90Item3: "AI SoV, audits, and truth-center governance start compounding.",
    fitTitle: "Who this is for / not for",
    fitFor: "For",
    fitFor1: "Agencies running recurring audits and client reports.",
    fitFor2: "In-house teams that need one SEO + GEO + AI operating layer.",
    fitFor3: "Founders and expert operators shipping their own sites.",
    fitNotFor: "Not for",
    fitNotFor1: "Teams expecting a black-box crawler with no review.",
    fitNotFor2: "Users who want a mandatory hosted SaaS.",
    fitNotFor3: "Anyone looking for GEO snake-oil without technical SEO discipline.",
    chartAudits: "Audit history",
    chartAuditsCopy: "Recent summary scores for the active project.",
    chartReports: "Report history",
    chartReportsCopy: "Recent report outputs ready for client delivery.",
    chartProviders: "Provider reliability view",
    chartProvidersCopy: "Enabled configs in UI, failures and latency in `/metrics`.",
    chartSov: "AI SoV history",
    chartSovCopy: "Latest mention rate and AI Citation Score snapshots.",
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
    reportFooter: "Client report footer",
    logoUrl: "Logo URL",
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
    integrationsTitle: "Search and analytics integrations",
    createIntegration: "Create integration",
    integrationSource: "Source",
    propertyId: "Property / counter ID",
    saveIntegration: "Save integration",
    integrationList: "Integration list",
    cmsTitle: "CMS connectors and writeback gates",
    createCms: "Create CMS connector",
    cmsType: "CMS type",
    writebackMode: "Writeback mode",
    saveCms: "Save CMS connector",
    cmsList: "CMS connector list",
    label: "Label",
    model: "Model",
    apiEnv: "API key env var",
    saveProvider: "Save provider config",
    providerList: "Provider list",
    promptsTitle: "Prompt library and agent handoff",
    createPromptSet: "Create prompt set",
    promptPurpose: "Purpose",
    outputFormat: "Output format",
    modelRecommendation: "Model recommendation",
    riskNotes: "Risk notes",
    promptItems: "Prompt items, one per line",
    savePromptSet: "Save prompt set",
    promptSetList: "Workspace prompt sets",
    repoPromptLibrary: "Bundled repo prompt library",
    auditsTitle: "Structured audit runs",
    createAudit: "Create audit run",
    reportLanguage: "Report language",
    providerConfig: "Provider config ID",
    checks: "Checks",
    runAudit: "Run audit",
    auditList: "Audit runs",
    sovTitle: "AI Share of Voice",
    createSov: "Run SoV check",
    brandName: "Brand name",
    queryList: "Queries, comma-separated",
    providerListInline: "Providers, comma-separated",
    notesLabel: "Notes",
    runSov: "Run SoV",
    sovHistory: "SoV history",
    notificationsTitle: "Notifications and webhooks",
    createNotification: "Create notification endpoint",
    channelType: "Channel type",
    targetUrl: "Target URL",
    eventList: "Events, comma-separated",
    saveNotification: "Save endpoint",
    notificationList: "Configured endpoints",
    deliverablesTitle: "Patch flows and client delivery",
    createPatchPack: "Generate patch pack",
    createClientPack: "Generate client delivery pack",
    audience: "Audience",
    generatePatchPack: "Generate patch pack",
    generateClientPack: "Generate client pack",
    patchPackOutput: "Patch pack output",
    clientPackOutput: "Client pack output",
    reportsTitle: "Reports and artifacts",
    reportList: "Reports",
    artifactList: "Artifacts",
    projectExport: "Project export package",
    exportProject: "Export active project",
    integrationStarters: "Integration starters",
    repoAssets: "Repo assets reused by the app",
    activityLog: "Activity log",
    modeSurfaceTitle: "Product modes",
    ciGatingTitle: "CI gating path",
    executiveTitle: "Executive dashboard",
    executiveScoreLabel: "Executive score",
    executiveHealthLabel: "Health band",
    integrationCountLabel: "Connected integrations",
    cmsCountLabel: "Connected CMS",
    executiveNarrativeTitle: "Narrative",
    executivePrioritiesTitle: "Top priorities",
    executiveMetricsTitle: "Machine-readable dashboard",
    integrationContractsTitle: "Integration contracts",
    cmsContractsTitle: "CMS contracts",
  },
  ru: {
    navOverview: "Обзор",
    navExecutive: "Executive",
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
    navIntegrations: "Интеграции",
    navCms: "CMS",
    navPrompts: "Промпты",
    navAudits: "Аудиты",
    navSov: "AI SoV",
    navNotifications: "Уведомления",
    navDeliverables: "Выдача",
    navReports: "Отчеты",
    quickChecks: "Audit presets",
    demoAccess: "Demo access",
    releaseBadge:
      "v6.5.0 runtime ops, SEO maturity и evidence lab delivery",
    heroTitle:
      "Self-hosted операционная система для ежедневной работы с SEO, GEO и AI discoverability",
    heroCopy:
      "Передайте репозиторий человеку-оператору или AI coding agent, разверните стек, подключите провайдеров, запускайте аудиты, собирайте evidence и сравнивайте повторы по тем же сайтам.",
    badgeRepo: "Методология репо",
    badgeApp: "Продуктовый workflow",
    badgeProviders:
      "OpenAI / Claude / Gemini / Google Ads / Yandex / CrUX / Meta / VK / Ollama / LM Studio",
    metricAuth: "Статус авторизации",
    metricWorkspace: "Активный воркспейс",
    metricProject: "Активный проект",
    metricReports: "Язык последнего отчета",
    metricCitation: "Последний AI citation сигнал",
    overviewTitle: "Операторский обзор",
    first15Title: "Первый результат за 15 минут",
    first15Step1: "Войдите и создайте один workspace.",
    first15Step2: "Создайте один проект и заполните brand facts.",
    first15Step3: "Подключите одного провайдера или оставьте прозрачный starter-режим.",
    first15Step4: "Запустите один аудит и одну AI SoV-проверку.",
    first15Step5: "Откройте reports, artifacts и export package.",
    day30Title: "Что меняется за 30 дней",
    day30Item1: "У вас появляется повторяемый audit-ритм вместо разовых чеклистов.",
    day30Item2: "Факты, промпты и отчеты живут в одной операторской системе.",
    day30Item3: "Можно показывать дельты в score, evidence и AI visibility.",
    day90Title: "Что меняется за 90 дней",
    day90Item1: "Agency, in-house и founder workflows становятся переиспользуемыми.",
    day90Item2: "Появляется двуязычная evidence-база для fixes и client delivery.",
    day90Item3: "AI SoV, аудиты и truth-center governance начинают накапливать эффект.",
    fitTitle: "Для кого / не для кого",
    fitFor: "Для кого",
    fitFor1: "Агентства с регулярными аудитами и клиентской отчетностью.",
    fitFor2: "In-house команды, которым нужен единый SEO + GEO + AI слой.",
    fitFor3: "Фаундеры и экспертные операторы, ведущие свои сайты.",
    fitNotFor: "Не для кого",
    fitNotFor1: "Команды, которым нужен black-box crawler без ревью.",
    fitNotFor2: "Пользователи, которым нужен только обязательный hosted SaaS.",
    fitNotFor3: "Те, кто ищет GEO snake-oil без технической SEO-дисциплины.",
    chartAudits: "История аудитов",
    chartAuditsCopy: "Последние summary scores по активному проекту.",
    chartReports: "История отчетов",
    chartReportsCopy: "Последние report outputs, готовые к клиентской выдаче.",
    chartProviders: "Обзор надежности провайдеров",
    chartProvidersCopy: "В UI видны конфиги, а реальные failures и latency идут в `/metrics`.",
    chartSov: "История AI SoV",
    chartSovCopy: "Последние срезы mention rate и AI Citation Score.",
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
    reportFooter: "Футер клиентского отчета",
    logoUrl: "URL логотипа",
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
    integrationsTitle: "Поисковые и аналитические интеграции",
    createIntegration: "Создать интеграцию",
    integrationSource: "Источник",
    propertyId: "Property / counter ID",
    saveIntegration: "Сохранить интеграцию",
    integrationList: "Список интеграций",
    cmsTitle: "CMS connectors и writeback-gates",
    createCms: "Создать CMS connector",
    cmsType: "Тип CMS",
    writebackMode: "Режим writeback",
    saveCms: "Сохранить CMS connector",
    cmsList: "Список CMS connectors",
    label: "Label",
    model: "Модель",
    apiEnv: "Переменная окружения для API ключа",
    saveProvider: "Сохранить конфиг провайдера",
    providerList: "Список провайдеров",
    promptsTitle: "Prompt library и AI handoff",
    createPromptSet: "Создать prompt set",
    promptPurpose: "Назначение",
    outputFormat: "Формат вывода",
    modelRecommendation: "Рекомендуемая модель",
    riskNotes: "Risk notes",
    promptItems: "Элементы промпта, по одному на строку",
    savePromptSet: "Сохранить prompt set",
    promptSetList: "Workspace prompt sets",
    repoPromptLibrary: "Встроенная prompt library репозитория",
    auditsTitle: "Структурированные audit runs",
    createAudit: "Создать audit run",
    reportLanguage: "Язык отчета",
    providerConfig: "ID конфигурации провайдера",
    checks: "Проверки",
    runAudit: "Запустить аудит",
    auditList: "Список audit runs",
    sovTitle: "AI Share of Voice",
    createSov: "Запустить SoV-проверку",
    brandName: "Название бренда",
    queryList: "Запросы через запятую",
    providerListInline: "Провайдеры через запятую",
    notesLabel: "Заметки",
    runSov: "Запустить SoV",
    sovHistory: "История SoV",
    notificationsTitle: "Уведомления и webhooks",
    createNotification: "Создать notification endpoint",
    channelType: "Тип канала",
    targetUrl: "Target URL",
    eventList: "События через запятую",
    saveNotification: "Сохранить endpoint",
    notificationList: "Настроенные endpoints",
    deliverablesTitle: "Patch flows и client delivery",
    createPatchPack: "Сгенерировать patch pack",
    createClientPack: "Сгенерировать client delivery pack",
    audience: "Аудитория",
    generatePatchPack: "Сгенерировать patch pack",
    generateClientPack: "Сгенерировать client pack",
    patchPackOutput: "Вывод patch pack",
    clientPackOutput: "Вывод client pack",
    reportsTitle: "Отчеты и артефакты",
    reportList: "Отчеты",
    artifactList: "Артефакты",
    projectExport: "Экспорт project package",
    exportProject: "Экспортировать активный проект",
    integrationStarters: "Стартовые интеграции",
    repoAssets: "Репозиторные assets, которые переиспользует приложение",
    activityLog: "Журнал активности",
    modeSurfaceTitle: "Режимы продукта",
    ciGatingTitle: "Путь CI gating",
    executiveTitle: "Executive dashboard",
    executiveScoreLabel: "Executive score",
    executiveHealthLabel: "Health band",
    integrationCountLabel: "Подключенные интеграции",
    cmsCountLabel: "Подключенные CMS",
    executiveNarrativeTitle: "Narrative",
    executivePrioritiesTitle: "Главные приоритеты",
    executiveMetricsTitle: "Machine-readable dashboard",
    integrationContractsTitle: "Контракты интеграций",
    cmsContractsTitle: "Контракты CMS",
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
  const lastSov = state.sovRuns[0];
  $("#citation-status").textContent = lastSov ? sovLabel(lastSov) : "n/a";
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

function clampPercent(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return 0;
  }
  if (number <= 1) {
    return Math.max(0, Math.min(100, Math.round(number * 100)));
  }
  return Math.max(0, Math.min(100, Math.round(number)));
}

function parseCitationScore(row) {
  const summary = row?.mention_summary || "";
  const match = summary.match(/AI Citation Score:\s*(\d+)/i);
  return match ? Number(match[1]) : null;
}

function sovLabel(row) {
  const citation = parseCitationScore(row);
  if (citation !== null) {
    return `${citation}/100`;
  }
  if (row?.share_estimate !== null && row?.share_estimate !== undefined) {
    return `${clampPercent(row.share_estimate)}%`;
  }
  return "tracked";
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
  presetList.replaceChildren();
  projectPreset.replaceChildren();
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
  node.replaceChildren();
  if (!rows.length) {
    const empty = document.createElement("div");
    empty.className = "entity-card";
    empty.textContent = "No data yet.";
    node.append(empty);
    return;
  }
  rows.forEach((row) => node.append(mapper(row)));
}

function renderMiniChart(target, items) {
  const node = $(target);
  node.replaceChildren();
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "chart-empty";
    empty.textContent = "No project data yet.";
    node.append(empty);
    return;
  }
  items.forEach((item) => {
    const bar = document.createElement("div");
    bar.className = "chart-bar";
    const value = document.createElement("div");
    value.className = "chart-bar-value";
    value.textContent = item.valueLabel;
    const fill = document.createElement("div");
    fill.className = "chart-bar-fill";
    fill.style.height = `${Math.max(22, item.value)}%`;
    const label = document.createElement("div");
    label.className = "chart-bar-label";
    label.textContent = item.label;
    bar.append(value, fill, label);
    node.append(bar);
  });
}

function renderOverview() {
  renderMiniChart(
    "#audit-history-chart",
    state.auditRuns.slice(0, 6).map((row, index) => ({
      label: `#${row.id || index + 1}`,
      value: clampPercent(row.summary_score ?? 0),
      valueLabel: row.summary_score !== null && row.summary_score !== undefined ? `${Math.round(row.summary_score)}` : "pending",
    })),
  );
  renderMiniChart(
    "#report-history-chart",
    state.reports.slice(0, 6).map((row, index) => ({
      label: row.language || `r${index + 1}`,
      value: Math.max(30, 100 - index * 12),
      valueLabel: row.format || "report",
    })),
  );
  renderMiniChart(
    "#provider-failure-chart",
    state.providerConfigs.slice(0, 6).map((row) => ({
      label: row.provider_name,
      value: row.is_enabled ? 92 : 35,
      valueLabel: row.is_enabled ? "enabled" : "disabled",
    })),
  );
  renderMiniChart(
    "#sov-history-chart",
    state.sovRuns.slice(0, 6).map((row, index) => {
      const citation = parseCitationScore(row);
      const mentionRate = clampPercent(row.share_estimate ?? 0);
      return {
        label: `#${row.id || index + 1}`,
        value: citation !== null ? citation : mentionRate,
        valueLabel: citation !== null ? `${citation}` : `${mentionRate}%`,
      };
    }),
  );
}

function renderProductModes() {
  renderCards("#product-modes", state.productModes, (row) =>
    simpleCard(row.title, [
      row.primary_user,
      row.purpose,
      `Best for: ${(row.best_for || []).join(", ")}`,
    ]),
  );
  $("#ci-gating").textContent = state.ciGating.first_class_path
    ? JSON.stringify(state.ciGating, null, 2)
    : "";
}

function renderExecutiveDashboard() {
  const dashboard = state.executiveDashboard;
  if (!dashboard) {
    $("#executive-score").textContent = "n/a";
    $("#executive-health").textContent = "n/a";
    $("#executive-integrations-count").textContent = "0";
    $("#executive-cms-count").textContent = "0";
    $("#executive-narrative").textContent =
      "Select a project and run an audit first.";
    $("#executive-weekly-narrative").textContent = "";
    $("#executive-priorities").replaceChildren();
    $("#executive-anomalies").replaceChildren();
    $("#executive-owners").replaceChildren();
    $("#executive-portfolio").textContent = "";
    $("#executive-benchmarks").textContent = "";
    $("#runtime-ops-cards").replaceChildren();
    $("#runtime-ops-json").textContent = "";
    $("#seo-maturity-cards").replaceChildren();
    $("#seo-maturity-json").textContent = "";
    $("#executive-dashboard-json").textContent = "";
    return;
  }
  $("#executive-score").textContent = String(dashboard.executive_score);
  $("#executive-health").textContent = dashboard.health_band;
  $("#executive-integrations-count").textContent = String(
    (dashboard.integrations || []).length,
  );
  $("#executive-cms-count").textContent = String((dashboard.cms || []).length);
  $("#executive-narrative").textContent = dashboard.narrative;
  $("#executive-weekly-narrative").textContent =
    dashboard.weekly_narrative || "";
  renderCards("#executive-priorities", dashboard.priorities || [], (row) =>
    simpleCard(row.title || "Priority", [
      `Priority score: ${row.priority_score ?? "n/a"}`,
      row.recommendation || "No recommendation yet.",
    ]),
  );
  renderCards("#executive-anomalies", dashboard.anomalies || [], (row) =>
    simpleCard(row.surface || "anomaly", [
      `${row.severity || "watch"} · ${row.message || "No anomaly details"}`,
      `Likely cause: ${row.likely_cause || "unknown"}`,
    ]),
  );
  renderCards("#executive-owners", dashboard.owner_suggestions || [], (row) =>
    simpleCard(row.owner || "owner", [
      row.focus || "No focus",
      `Priority: ${row.priority || "n/a"}`,
    ]),
  );
  $("#executive-portfolio").textContent = JSON.stringify(
    dashboard.portfolio_view || {},
    null,
    2,
  );
  $("#executive-benchmarks").textContent = JSON.stringify(
    dashboard.benchmark_overlays || {},
    null,
    2,
  );
  renderCards(
    "#runtime-ops-cards",
    (state.runtimeOpsCenter && state.runtimeOpsCenter.managed_runtime_matrix) || [],
    (row) =>
      simpleCard(row.label || row.source_type || "runtime", [
        `${row.runtime_level || "contract_only"} · ${row.status || "unknown"}`,
        `Refresh: ${row.refresh_minutes ?? "n/a"} min · Rotation: ${row.token_rotation_days ?? "n/a"}d`,
        `Action: ${row.next_operator_action || "monitor"}`,
      ]),
  );
  $("#runtime-ops-json").textContent = JSON.stringify(
    state.runtimeOpsCenter || {},
    null,
    2,
  );
  renderCards(
    "#seo-maturity-cards",
    (state.seoMaturityCenter && state.seoMaturityCenter.tracks) || [],
    (row) =>
      simpleCard(row.track || "track", [
        `${row.status || "unknown"} · score ${row.score ?? "n/a"}`,
        (row.next_steps || [])[0] || "No next step",
      ]),
  );
  $("#seo-maturity-json").textContent = JSON.stringify(
    state.seoMaturityCenter || {},
    null,
    2,
  );
  $("#executive-dashboard-json").textContent = JSON.stringify(
    dashboard,
    null,
    2,
  );
}

function renderSaasCenter() {
  renderCards(
    "#organization-switcher-list",
    state.organizationSwitcher.organizations || [],
    (row) =>
      simpleCard(row.name || row.slug || "organization", [
        `Org #${row.organization_id} · ${row.slug || "n/a"}`,
        `Workspaces: ${row.workspace_count ?? 0}`,
        `IDs: ${(row.active_workspace_ids || []).join(", ") || "n/a"}`,
      ]),
  );
  renderCards(
    "#workspace-catalog-cards",
    state.saasCatalog || [],
    (row) =>
      simpleCard(row.workspace_name || row.workspace_slug || "workspace", [
        `Org: ${row.organization_name || "unassigned"}`,
        `Tenant: ${row.tenant_name || "none"}`,
        `Plan: ${row.plan_code || "n/a"} · ${row.plan_status || "n/a"}`,
      ]),
  );
  renderCards(
    "#tenant-usage-alerts",
    (state.tenantOverview && state.tenantOverview.quota_alerts) || [],
    (row) =>
      simpleCard(row.metric || "quota", [
        `Used: ${row.used ?? 0} / ${row.limit ?? 0}`,
        `Status: ${row.status || "unknown"} · ratio ${row.ratio ?? "n/a"}`,
      ]),
  );
  $("#saas-catalog").textContent = JSON.stringify(
    state.saasCatalog || [],
    null,
    2,
  );
  $("#saas-overview").textContent = JSON.stringify(
    state.tenantOverview || {},
    null,
    2,
  );
  $("#portfolio-dashboard").textContent = JSON.stringify(
    state.portfolioDashboard || {},
    null,
    2,
  );
  $("#demo-center").textContent = JSON.stringify(state.demoCenter || {}, null, 2);
  $("#productization-center").textContent = JSON.stringify(
    state.productizationCenter || {},
    null,
    2,
  );
  $("#saas-growth-center").textContent = JSON.stringify(
    state.saasGrowthCenter || {},
    null,
    2,
  );
  $("#saas-readiness-center").textContent = JSON.stringify(
    state.saasReadinessCenter || {},
    null,
    2,
  );
  $("#deployment-posture").textContent = JSON.stringify(
    state.deploymentPosture || {},
    null,
    2,
  );
}

function renderProofCenter() {
  renderCards("#proof-timeline", state.proofTimeline || [], (row) =>
    simpleCard(row.title || row.item_type, [
      `${row.item_type} · ${row.source_id}`,
      row.summary || "No summary",
      row.confidence_label ? `Confidence: ${row.confidence_label}` : "",
    ].filter(Boolean)),
  );
  renderCards("#evidence-list", state.proofEvidence || [], (row) =>
    simpleCard(row.title || "evidence", [
      `${row.label_type || "evidence"} · #${row.id}`,
      row.summary || "No summary",
    ]),
  );
  renderCards("#experiment-list", state.proofExperiments || [], (row) =>
    simpleCard(row.source_type || "experiment", [
      `#${row.id} · ${row.confidence_label || "partial"}`,
      row.change_summary || "No change summary",
    ]),
  );
  $("#proof-kit").textContent = JSON.stringify(state.proofKit || {}, null, 2);
  $("#proof-ops-center").textContent = JSON.stringify(
    state.proofOpsCenter || {},
    null,
    2,
  );
  $("#proof-export-pack").textContent = JSON.stringify(
    state.proofExportPack || {},
    null,
    2,
  );
  $("#evidence-lab").textContent = JSON.stringify(state.evidenceLab || {}, null, 2);
  $("#mention-reputation-center").textContent = JSON.stringify(
    state.mentionReputationCenter || {},
    null,
    2,
  );
  $("#operator-board").textContent = JSON.stringify(
    state.operatorBoard || {},
    null,
    2,
  );
}

function renderBuildCenter() {
  $("#generation-contracts").textContent = JSON.stringify(
    state.generationContracts || {},
    null,
    2,
  );
  $("#generation-output").textContent = JSON.stringify(
    {
      latest_scaffold: state.generationOutput,
      manifests: state.generationManifests,
    },
    null,
    2,
  );
  $("#one-link-builder").textContent = JSON.stringify(
    state.oneLinkBuilder || {},
    null,
    2,
  );
  $("#repo-understanding").textContent = JSON.stringify(
    state.repoUnderstanding || {},
    null,
    2,
  );
  $("#deploy-wizard").textContent = JSON.stringify(
    state.deployWizard || {},
    null,
    2,
  );
  $("#prompt-packs").textContent = JSON.stringify(
    state.promptPacks || {},
    null,
    2,
  );
  $("#social-distribution-center").textContent = JSON.stringify(
    state.socialDistributionCenter || {},
    null,
    2,
  );
  $("#social-intelligence-center").textContent = JSON.stringify(
    state.socialIntelligenceCenter || {},
    null,
    2,
  );
  $("#social-command-center").textContent = JSON.stringify(
    state.socialCommandCenter || {},
    null,
    2,
  );
  $("#social-parser-output").textContent = JSON.stringify(
    state.socialParserOutput || {},
    null,
    2,
  );
  $("#local-entity-center").textContent = JSON.stringify(
    state.localEntityCenter || {},
    null,
    2,
  );
  $("#ru-market-command-center").textContent = JSON.stringify(
    state.ruMarketCommandCenter || {},
    null,
    2,
  );
}

function workspaceCard(workspace) {
  const card = document.createElement("article");
  card.className = "entity-card";
  const branding = [
    workspace.client_report_title || "No white-label title yet.",
    workspace.client_report_subtitle || "No client subtitle yet.",
    workspace.client_report_footer || "No client footer yet.",
  ];
  const title = document.createElement("strong");
  title.textContent = workspace.name;
  const metaOne = document.createElement("div");
  metaOne.className = "workspace-meta";
  metaOne.textContent = `#${workspace.id} · ${workspace.slug} · ${workspace.default_report_language}`;
  const metaTwo = document.createElement("div");
  metaTwo.className = "workspace-meta";
  metaTwo.textContent = branding.join(" · ");
  const metaThree = document.createElement("div");
  metaThree.className = "workspace-meta";
  metaThree.textContent = workspace.branding_logo_url || "No logo URL yet.";
  card.append(title, metaOne, metaTwo, metaThree);
  card.addEventListener("click", async () => {
    state.selectedWorkspaceId = String(workspace.id);
    document.querySelectorAll("input[name='workspace_id']").forEach((input) => {
      input.value = workspace.id;
    });
    setStatus();
    log(`Workspace #${workspace.id} selected.`);
    await refreshProjects();
    await Promise.all([refreshPromptSets(), refreshNotifications()]);
  });
  return card;
}

function projectCard(project) {
  const card = document.createElement("article");
  card.className = "entity-card";
  const title = document.createElement("strong");
  title.textContent = project.name;
  const metaOne = document.createElement("div");
  metaOne.className = "project-meta";
  metaOne.textContent = `#${project.id} · ${project.website_url}`;
  const metaTwo = document.createElement("div");
  metaTwo.className = "project-meta";
  metaTwo.textContent = `${project.market} · ${project.language} · ${project.project_type}`;
  card.append(title, metaOne, metaTwo);
  card.addEventListener("click", async () => {
    state.selectedProjectId = String(project.id);
    document.querySelectorAll("input[name='project_id']").forEach((input) => {
      input.value = project.id;
    });
    setStatus();
    log(`Project #${project.id} selected.`);
    await Promise.all([
      refreshReportsAndArtifacts(),
      refreshIntegrations(),
      refreshCmsConnectors(),
      refreshExecutiveDashboard(),
    ]);
  });
  return card;
}

function simpleCard(title, lines) {
  const card = document.createElement("article");
  card.className = "entity-card";
  const heading = document.createElement("strong");
  heading.textContent = title;
  card.append(heading);
  lines.forEach((line) => {
    const meta = document.createElement("div");
    meta.className = "project-meta";
    meta.textContent = line;
    card.append(meta);
  });
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
  renderOverview();
}

async function refreshProjects() {
  if (!state.token || !state.selectedWorkspaceId) {
    return;
  }
  state.projects = await apiRequest(`/projects?workspace_id=${state.selectedWorkspaceId}`);
  renderCards("#project-list", state.projects, projectCard);
  renderOverview();
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
  const [configs, healthCenter, modelRegistry, operatingCenter] = await Promise.all([
    apiRequest(`/providers?workspace_id=${state.selectedWorkspaceId}`),
    apiRequest(`/providers/health?workspace_id=${state.selectedWorkspaceId}`),
    apiRequest("/providers/model-registry"),
    apiRequest(`/providers/operating-center?workspace_id=${state.selectedWorkspaceId}`),
  ]);
  state.providerConfigs = configs;
  state.providerHealthCenter = healthCenter || {};
  state.providerModelRegistry = modelRegistry || {};
  state.providerOperatingCenter = operatingCenter || {};
  renderCards("#provider-list", state.providerConfigs, (row) =>
    simpleCard(row.label, [`#${row.id}`, `${row.provider_name} · ${row.model}`, row.api_key_env_var || "default env routing"]),
  );
  $("#provider-health-center").textContent = JSON.stringify(
    state.providerHealthCenter || {},
    null,
    2,
  );
  $("#provider-model-registry").textContent = JSON.stringify(
    state.providerModelRegistry || {},
    null,
    2,
  );
  $("#provider-operating-center").textContent = JSON.stringify(
    state.providerOperatingCenter || {},
    null,
    2,
  );
  renderOverview();
}

async function refreshIntegrations() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const [rows, contracts, runtimeCenter, healthCenter] = await Promise.all([
    apiRequest(`/integrations?project_id=${state.selectedProjectId}`),
    apiRequest("/integrations/contracts"),
    apiRequest(`/integrations/runtime-center?project_id=${state.selectedProjectId}`),
    apiRequest(`/integrations/health-center?project_id=${state.selectedProjectId}`),
  ]);
  state.integrationConnections = rows;
  state.integrationContracts = contracts.contracts || [];
  state.integrationRuntimeCenter = runtimeCenter || {};
  state.integrationHealthCenter = healthCenter || {};
  renderCards("#integration-list", state.integrationConnections, (row) =>
    simpleCard(row.label, [
      `${row.source_type} · #${row.id}`,
      row.property_identifier || "starter property",
      row.last_sync_status || "not synced yet",
      `${row.readiness_tier} · ${row.credential_status}`,
    ]),
  );
  $("#integration-contracts").textContent = JSON.stringify(
    state.integrationContracts,
    null,
    2,
  );
  $("#integration-runtime-center").textContent = JSON.stringify(
    {
      runtime_center: state.integrationRuntimeCenter || {},
      health_center: state.integrationHealthCenter || {},
    },
    null,
    2,
  );
}

async function refreshCmsConnectors() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const [rows, contracts] = await Promise.all([
    apiRequest(`/cms?project_id=${state.selectedProjectId}`),
    apiRequest("/cms/contracts"),
  ]);
  state.cmsConnectors = rows;
  state.cmsContracts = contracts.contracts || [];
  renderCards("#cms-list", state.cmsConnectors, (row) =>
    simpleCard(row.label, [
      `${row.cms_type} · #${row.id}`,
      row.writeback_mode,
      row.last_sync_status || "not synced yet",
      `${row.readiness_tier} · ${row.credential_status}`,
    ]),
  );
  $("#cms-contracts").textContent = JSON.stringify(state.cmsContracts, null, 2);
}

async function refreshPromptSets() {
  if (!state.token || !state.selectedWorkspaceId) {
    return;
  }
  const [promptSets, promptLibrary] = await Promise.all([
    apiRequest(`/prompt-sets?workspace_id=${state.selectedWorkspaceId}`),
    apiRequest("/settings/prompt-library"),
  ]);
  state.promptSets = promptSets;
  renderCards("#prompt-set-list", promptSets, (row) =>
    simpleCard(row.name, [
      row.purpose || "General-purpose prompt set",
      row.output_format || "Flexible output",
      row.model_recommendation || "Bring your own model",
    ]),
  );
  renderCards("#repo-prompt-library", promptLibrary.prompts || [], (row) =>
    simpleCard(row.id, [row.language, row.purpose, row.path]),
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
  renderOverview();
}

async function refreshReportsAndArtifacts() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const [reports, artifacts, repoAssets, integrationStarters] = await Promise.all([
    apiRequest(`/reports?project_id=${state.selectedProjectId}`),
    apiRequest(`/artifacts?project_id=${state.selectedProjectId}`),
    apiRequest("/settings/repo-assets"),
    apiRequest("/settings/integration-starters"),
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
  $("#integration-starters").textContent = JSON.stringify(integrationStarters, null, 2);
  $("#cms-lifecycle-summary").textContent = JSON.stringify(
    {
      flow: ["preview_ready", "approved", "applied", "verified", "rolled_back"],
      purpose:
        "Govern CMS changes with explicit checkpoints instead of silent live writeback.",
    },
    null,
    2,
  );
  setStatus();
  renderOverview();
}

async function askReportAssistant() {
  if (!state.token || !state.reports.length) {
    log("No report is available for the assistant yet.", "warning");
    return;
  }
  const question = $("#report-assistant-question").value.trim();
  if (!question) {
    log("Enter a report question first.", "warning");
    return;
  }
  const payload = await apiRequest(`/reports/${state.reports[0].id}/assistant`, {
    method: "POST",
    body: JSON.stringify({ question, language: state.language }),
  });
  state.reportAssistant = payload;
  $("#report-assistant-output").textContent = JSON.stringify(payload, null, 2);
}

async function refreshSovRuns() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  state.sovRuns = await apiRequest(`/sov/history?project_id=${state.selectedProjectId}`);
  renderCards("#sov-list", state.sovRuns, (row) =>
    simpleCard(`SoV #${row.id}`, [
      `${row.brand} · ${row.status}`,
      `Share estimate: ${row.share_estimate ?? "n/a"}`,
      `AI Citation Score: ${parseCitationScore(row) ?? "n/a"}`,
      `Queries: ${(row.queries || []).join(", ")}`,
    ]),
  );
  renderOverview();
}

async function refreshNotifications() {
  if (!state.token || !state.selectedWorkspaceId) {
    return;
  }
  state.notificationEndpoints = await apiRequest(
    `/notifications?workspace_id=${state.selectedWorkspaceId}`,
  );
  renderCards("#notification-list", state.notificationEndpoints, (row) =>
    simpleCard(row.label, [
      `${row.channel_type} · ${row.is_enabled ? "enabled" : "disabled"}`,
      row.target_url,
      `Events: ${(row.events || []).join(", ") || "all"}`,
    ]),
  );
  renderOverview();
}

async function refreshModeAndCiSettings() {
  const [productModes, ciGating] = await Promise.all([
    apiRequest("/settings/product-modes", { headers: {} }),
    apiRequest("/settings/ci-gating", { headers: {} }),
  ]);
  state.productModes = productModes.modes || [];
  state.ciGating = ciGating;
  renderProductModes();
}

async function refreshExecutiveDashboard() {
  if (!state.token || !state.selectedProjectId) {
    state.executiveDashboard = null;
    renderExecutiveDashboard();
    return;
  }
  try {
    const [dashboard, runtimeOpsCenter, seoMaturityCenter] = await Promise.all([
      apiRequest(`/settings/executive-dashboard?project_id=${state.selectedProjectId}`),
      apiRequest(`/settings/runtime-ops-center?project_id=${state.selectedProjectId}`),
      apiRequest(`/settings/seo-maturity-center?project_id=${state.selectedProjectId}`),
    ]);
    state.executiveDashboard = dashboard;
    state.runtimeOpsCenter = runtimeOpsCenter || {};
    state.seoMaturityCenter = seoMaturityCenter || {};
  } catch (error) {
    state.executiveDashboard = null;
    state.runtimeOpsCenter = {};
    state.seoMaturityCenter = {};
    log(`Executive dashboard not ready yet: ${error.message}`, "warning");
  }
  renderExecutiveDashboard();
}

async function refreshSaasCenter() {
  if (!state.token) {
    return;
  }
  const requests = [
    apiRequest("/saas/workspace-catalog"),
    apiRequest("/saas/organizations"),
    apiRequest("/saas/organization-switcher"),
    apiRequest("/settings/demo-center", { headers: {} }),
    apiRequest("/settings/productization-center", { headers: {} }),
  ];
  if (state.selectedWorkspaceId) {
    requests.push(
      apiRequest(
        `/settings/portfolio-dashboard?workspace_id=${state.selectedWorkspaceId}`,
      ),
      apiRequest(
        `/settings/saas-growth-center?workspace_id=${state.selectedWorkspaceId}`,
      ),
      apiRequest(
        `/settings/saas-readiness-center?workspace_id=${state.selectedWorkspaceId}`,
      ),
      apiRequest("/settings/deployment-posture"),
    );
  }
  const [
    catalog,
    organizations,
    organizationSwitcher,
    demoCenter,
    productizationCenter,
    portfolioDashboard,
    saasGrowthCenter,
    saasReadinessCenter,
    deploymentPosture,
  ] = await Promise.all(requests);
  state.saasCatalog = catalog.items || [];
  state.organizations = organizations || [];
  state.organizationSwitcher = organizationSwitcher || {};
  state.demoCenter = demoCenter || {};
  state.productizationCenter = productizationCenter || {};
  state.portfolioDashboard = portfolioDashboard || {};
  state.saasGrowthCenter = saasGrowthCenter || {};
  state.saasReadinessCenter = saasReadinessCenter || {};
  state.deploymentPosture = deploymentPosture || {};
  if (state.selectedWorkspaceId) {
    try {
      state.tenantOverview = await apiRequest(
        `/saas/tenant-overview?workspace_id=${state.selectedWorkspaceId}`,
      );
    } catch (error) {
      state.tenantOverview = { warning: error.message };
    }
  }
  renderSaasCenter();
}

async function refreshProofCenter() {
  if (!state.token || !state.selectedProjectId) {
    return;
  }
  const [
    timeline,
    evidence,
    experiments,
    proofOpsCenter,
    proofKit,
    exportPack,
    mentionReputationCenter,
    operatorBoard,
    evidenceLab,
  ] =
    await Promise.all([
      apiRequest(`/proof/timeline?project_id=${state.selectedProjectId}`),
      apiRequest(`/proof/evidence?project_id=${state.selectedProjectId}`),
      apiRequest(`/proof/experiments?project_id=${state.selectedProjectId}`),
      apiRequest(`/settings/proof-ops-center?project_id=${state.selectedProjectId}`),
      apiRequest("/settings/proof-kit", { headers: {} }),
      apiRequest(`/proof/export-pack?project_id=${state.selectedProjectId}`),
      apiRequest(
        `/settings/mention-reputation-center?project_id=${state.selectedProjectId}`,
      ),
      apiRequest(`/settings/operator-board?project_id=${state.selectedProjectId}`),
      apiRequest(`/settings/evidence-lab?project_id=${state.selectedProjectId}`),
    ]);
  state.proofTimeline = timeline.items || [];
  state.proofEvidence = evidence || [];
  state.proofExperiments = experiments || [];
  state.proofOpsCenter = proofOpsCenter || {};
  state.proofKit = proofKit;
  state.proofExportPack = exportPack || {};
  state.mentionReputationCenter = mentionReputationCenter || {};
  state.operatorBoard = operatorBoard || {};
  state.evidenceLab = evidenceLab || {};
  renderProofCenter();
}

async function refreshBuildCenter() {
  if (!state.token) {
    return;
  }
  const socialIntelligenceRequest = state.selectedProjectId
    ? apiRequest(
        `/settings/social-intelligence-center?project_id=${state.selectedProjectId}`,
      )
    : Promise.resolve({});
  const socialCommandRequest = state.selectedProjectId
    ? apiRequest(`/settings/social-command-center?project_id=${state.selectedProjectId}`)
    : Promise.resolve({});
  const ruMarketCommandRequest = state.selectedProjectId
    ? apiRequest(`/settings/ru-market-command-center?project_id=${state.selectedProjectId}`)
    : Promise.resolve({});
  const [
    contracts,
    manifests,
    oneLinkBuilder,
    socialDistributionCenter,
    socialIntelligenceCenter,
    socialCommandCenter,
    repoUnderstanding,
    deployWizard,
    promptPacks,
    localEntityCenter,
    ruMarketCommandCenter,
  ] = await Promise.all([
    apiRequest("/generation/contracts"),
    apiRequest("/generation/manifests"),
    apiRequest("/settings/one-link-builder", { headers: {} }),
    apiRequest("/settings/social-distribution-center", { headers: {} }),
    socialIntelligenceRequest,
    socialCommandRequest,
    apiRequest("/settings/repo-understanding-center", { headers: {} }),
    apiRequest("/settings/deploy-wizard", { headers: {} }),
    apiRequest("/settings/prompt-packs", { headers: {} }),
    apiRequest("/settings/local-entity-center", { headers: {} }),
    ruMarketCommandRequest,
  ]);
  state.generationContracts = contracts;
  state.generationManifests = manifests;
  state.oneLinkBuilder = oneLinkBuilder;
  state.socialDistributionCenter = socialDistributionCenter;
  state.socialIntelligenceCenter = socialIntelligenceCenter;
  state.socialCommandCenter = socialCommandCenter;
  state.repoUnderstanding = repoUnderstanding;
  state.deployWizard = deployWizard;
  state.promptPacks = promptPacks;
  state.localEntityCenter = localEntityCenter;
  state.ruMarketCommandCenter = ruMarketCommandCenter;
  renderBuildCenter();
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
  writeSessionValue("discoverability-token", state.token);
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

async function handleOrganizationCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  await apiRequest("/saas/organizations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  log(`Organization ${payload.name} created.`);
  event.currentTarget.reset();
  await refreshSaasCenter();
}

async function handleTenantProfileCreateV52(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.organization_id = payload.organization_id
    ? Number(payload.organization_id)
    : null;
  payload.plan_status = "active";
  payload.quota = { monthly_syncs: 300, projects: 25 };
  payload.usage = { monthly_syncs_used: state.integrationConnections.length };
  payload.onboarding_state = { auth: "done", deploy: "in_progress" };
  payload.tenant_settings = { ai_to_app: true, managed_runtime_goal: true };
  await apiRequest("/saas/tenant-profiles", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  log(`Tenant profile ${payload.tenant_name} saved.`);
  await refreshSaasCenter();
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

async function handlePromptSetCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.prompt_items = payload.prompt_items
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
  payload.human_review_required = true;
  await apiRequest("/prompt-sets", { method: "POST", body: JSON.stringify(payload) });
  log(`Prompt set ${payload.name} saved.`);
  event.currentTarget.reset();
  await refreshPromptSets();
}

async function handleIntegrationCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  payload.config = {};
  const row = await apiRequest("/integrations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  await apiRequest(`/integrations/${row.id}/sync`, { method: "POST" });
  log(`Integration ${payload.label} created and synced.`);
  event.currentTarget.reset();
  await refreshIntegrations();
}

async function handleCmsCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  const row = await apiRequest("/cms", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  await apiRequest(`/cms/${row.id}/inventory`, { method: "POST" });
  log(`CMS connector ${payload.label} created and inventoried.`);
  event.currentTarget.reset();
  await refreshCmsConnectors();
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

async function handleSovCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  payload.queries = splitCsv(payload.queries);
  payload.providers = splitCsv(payload.providers);
  await apiRequest("/sov/check", { method: "POST", body: JSON.stringify(payload) });
  log(`AI SoV check completed for ${payload.brand}.`);
  event.currentTarget.reset();
  await refreshSovRuns();
}

async function handleNotificationCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.events = splitCsv(payload.events);
  payload.is_enabled = true;
  await apiRequest("/notifications", { method: "POST", body: JSON.stringify(payload) });
  log(`Notification endpoint ${payload.label} saved.`);
  event.currentTarget.reset();
  await refreshNotifications();
}

async function handleGenerationCreateV52(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = payload.workspace_id ? Number(payload.workspace_id) : null;
  payload.project_id = payload.project_id ? Number(payload.project_id) : null;
  payload.required_integrations = splitCsv(payload.required_integrations);
  const manifest = await apiRequest("/generation/manifests/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  const scaffold = await apiRequest(
    `/generation/manifests/${manifest.id}/scaffold`,
    {
      method: "POST",
    },
  );
  state.generationOutput = {
    manifest,
    scaffold,
  };
  log(`Generated scaffold for ${payload.domain_or_url}.`);
  await refreshBuildCenter();
}

async function handleSocialParser(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.project_id = payload.project_id ? Number(payload.project_id) : null;
  state.socialParserOutput = await apiRequest("/settings/social-idea-parser", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  $("#social-parser-output").textContent = JSON.stringify(
    state.socialParserOutput || {},
    null,
    2,
  );
  log(`Parsed social signals from ${payload.source || "social"}.`);
}

async function handleProjectExport() {
  if (!state.token || !state.selectedProjectId) {
    log("Select a project first.", "warning");
    return;
  }
  const payload = await apiRequest(`/exports/project-package?project_id=${state.selectedProjectId}`);
  $("#project-export").textContent = JSON.stringify(payload, null, 2);
  log(`Export package generated for project #${state.selectedProjectId}.`);
}

async function handlePatchPackCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  const pack = await apiRequest("/deliverables/patch-pack", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  $("#patch-pack-output").textContent = JSON.stringify(pack, null, 2);
  log(`Patch pack generated for project #${payload.project_id}.`);
  await refreshReportsAndArtifacts();
}

async function handleClientPackCreate(event) {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  payload.workspace_id = Number(payload.workspace_id);
  payload.project_id = Number(payload.project_id);
  const pack = await apiRequest("/deliverables/client-pack", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  $("#client-pack-output").textContent = JSON.stringify(pack, null, 2);
  log(`Client delivery pack generated for project #${payload.project_id}.`);
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
    await Promise.all([
      refreshPromptSets(),
      refreshNotifications(),
      refreshSaasCenter(),
    ]);
  }
  if (!state.selectedProjectId && state.projects[0]) {
    state.selectedProjectId = String(state.projects[0].id);
  }
  if (state.selectedProjectId) {
    await Promise.all([
      refreshFacts(),
      refreshProviders(),
      refreshIntegrations(),
      refreshCmsConnectors(),
      refreshAudits(),
      refreshSovRuns(),
      refreshReportsAndArtifacts(),
      refreshExecutiveDashboard(),
      refreshProofCenter(),
      refreshBuildCenter(),
    ]);
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
  $("#organization-form").addEventListener("submit", handleOrganizationCreate);
  $("#tenant-profile-form-v52").addEventListener(
    "submit",
    handleTenantProfileCreateV52,
  );
  $("#facts-form").addEventListener("submit", handleFactsCreate);
  $("#provider-form").addEventListener("submit", handleProviderCreate);
  $("#integration-form").addEventListener("submit", handleIntegrationCreate);
  $("#cms-form").addEventListener("submit", handleCmsCreate);
  $("#prompt-set-form").addEventListener("submit", handlePromptSetCreate);
  $("#audit-form").addEventListener("submit", handleAuditCreate);
  $("#sov-form").addEventListener("submit", handleSovCreate);
  $("#notification-form").addEventListener("submit", handleNotificationCreate);
  $("#generation-form-v52").addEventListener(
    "submit",
    handleGenerationCreateV52,
  );
  $("#social-parser-form").addEventListener("submit", handleSocialParser);
  $("#patch-pack-form").addEventListener("submit", handlePatchPackCreate);
  $("#client-pack-form").addEventListener("submit", handleClientPackCreate);
  $("#refresh-workspaces").addEventListener("click", () => refreshWorkspaces().catch((error) => log(error.message, "warning")));
  $("#refresh-projects").addEventListener("click", () => refreshProjects().catch((error) => log(error.message, "warning")));
  $("#refresh-facts").addEventListener("click", () => refreshFacts().catch((error) => log(error.message, "warning")));
  $("#refresh-providers").addEventListener("click", () => refreshProviders().catch((error) => log(error.message, "warning")));
  $("#refresh-integrations").addEventListener("click", () => refreshIntegrations().catch((error) => log(error.message, "warning")));
  $("#refresh-cms").addEventListener("click", () => refreshCmsConnectors().catch((error) => log(error.message, "warning")));
  $("#refresh-prompts").addEventListener("click", () => refreshPromptSets().catch((error) => log(error.message, "warning")));
  $("#refresh-audits").addEventListener("click", () => refreshAudits().catch((error) => log(error.message, "warning")));
  $("#refresh-sov").addEventListener("click", () => refreshSovRuns().catch((error) => log(error.message, "warning")));
  $("#refresh-notifications").addEventListener("click", () => refreshNotifications().catch((error) => log(error.message, "warning")));
  $("#refresh-reports").addEventListener("click", () => refreshReportsAndArtifacts().catch((error) => log(error.message, "warning")));
  $("#ask-report-assistant").addEventListener("click", () => askReportAssistant().catch((error) => log(error.message, "warning")));
  $("#refresh-executive").addEventListener("click", () => refreshExecutiveDashboard().catch((error) => log(error.message, "warning")));
  $("#refresh-saas").addEventListener("click", () => refreshSaasCenter().catch((error) => log(error.message, "warning")));
  $("#refresh-proof").addEventListener("click", () => refreshProofCenter().catch((error) => log(error.message, "warning")));
  $("#refresh-build").addEventListener("click", () => refreshBuildCenter().catch((error) => log(error.message, "warning")));
  $("#export-project").addEventListener("click", () => handleProjectExport().catch((error) => log(error.message, "warning")));
  $("#sign-out").addEventListener("click", () => {
    state.token = "";
    removeSessionValue("discoverability-token");
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
    await refreshModeAndCiSettings();
    await bootstrapAuthedState();
    renderOverview();
    renderExecutiveDashboard();
    renderSaasCenter();
    renderProofCenter();
    renderBuildCenter();
  } catch (error) {
    log(`Startup warning: ${error.message}`, "warning");
  }
}

init();
