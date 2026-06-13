const graphModes = {
  site: {
    title: "Site structure graph",
    subtitle:
      "Homepage, key sections, money pages, and supporting hubs connected as one crawlable and explainable map.",
    nodes: [
      {
        id: "home",
        label: "Homepage",
        tone: "accent",
        x: 42,
        y: 10,
        what: "The main entry point and routing surface for users, crawlers, and AI systems.",
        why: "Weak homepage framing makes every downstream section harder to understand.",
        impact: "Sections, navigation clarity, crawl depth, brand positioning.",
        next: "Clarify positioning, key service links, and trust blocks above the fold.",
      },
      {
        id: "services",
        label: "Service cluster",
        tone: "neutral",
        x: 14,
        y: 38,
        what: "Commercial pages describing offers, capabilities, and conversion intent.",
        why: "These are usually the most valuable pages for both ranking and AI citations.",
        impact: "Leads, case studies, local pages, schema coverage.",
        next: "Add stronger proof, FAQ blocks, and service schema coverage.",
      },
      {
        id: "blog",
        label: "Content hub",
        tone: "neutral",
        x: 68,
        y: 36,
        what: "Supporting educational or comparison content that expands discoverability.",
        why: "This cluster creates answer-ready inventory and internal linking support.",
        impact: "Citation readiness, freshness, topic breadth, long-tail coverage.",
        next: "Refresh stale posts and link them to commercial pages with explicit next steps.",
      },
      {
        id: "cases",
        label: "Case studies",
        tone: "warning",
        x: 20,
        y: 72,
        what: "Proof-heavy pages showing outcomes, examples, and trust signals.",
        why: "AI and humans both look for evidence, not only claims.",
        impact: "Trust, conversion, founder credibility, sales handoff.",
        next: "Standardize proof blocks, dates, and measurable outcomes.",
      },
      {
        id: "legal",
        label: "Legal / trust",
        tone: "neutral",
        x: 72,
        y: 74,
        what: "About, policy, contact, and legal pages that confirm organizational legitimacy.",
        why: "Missing trust surfaces weaken both SEO trust and AI reusability.",
        impact: "Entity validation, brand confidence, YMYL-style trust review.",
        next: "Ensure ownership, editorial policy, and contact facts stay consistent.",
      },
    ],
    edges: [
      ["home", "services"],
      ["home", "blog"],
      ["services", "cases"],
      ["blog", "services"],
      ["home", "legal"],
      ["cases", "legal"],
    ],
  },
  surface: {
    title: "Discoverability surface graph",
    subtitle:
      "Public machine-readable surfaces that influence how search engines and AI systems discover and interpret the site.",
    nodes: [
      {
        id: "robots",
        label: "robots.txt",
        tone: "accent",
        x: 14,
        y: 16,
        what: "Crawler policy rules for search and AI bots.",
        why: "One bad rule can block the exact pages you want indexed or cited.",
        impact: "Crawl access, AI bot policy, sitemap discovery.",
        next: "Re-check allow and disallow rules for Googlebot, YandexBot, and YandexAdditional.",
      },
      {
        id: "sitemap",
        label: "sitemap.xml",
        tone: "neutral",
        x: 42,
        y: 18,
        what: "Canonical list of discoverable URLs and recrawl hints.",
        why: "It reduces ambiguity and speeds up discovery of important pages.",
        impact: "Coverage, freshness, canonical clarity.",
        next: "List only live canonical URLs and reference the sitemap in robots.txt.",
      },
      {
        id: "llmstxt",
        label: "llms.txt",
        tone: "accent",
        x: 72,
        y: 16,
        what: "AI-facing guidance file describing important public URLs and intent.",
        why: "It gives AI systems a cleaner route into the site than random crawling alone.",
        impact: "AI discoverability, content routing, operator transparency.",
        next: "Publish a clean draft and keep it synchronized with real sections and brand facts.",
      },
      {
        id: "aitxt",
        label: "ai.txt",
        tone: "warning",
        x: 12,
        y: 62,
        what: "Supplementary AI guidance file used by some operators and ecosystems.",
        why: "It can reinforce policy and public guidance if used consistently.",
        impact: "AI access expectations, consistency with llms.txt and robots.txt.",
        next: "Check for contradictions and avoid claiming permissions that robots.txt blocks.",
      },
      {
        id: "schema",
        label: "JSON-LD schema",
        tone: "accent",
        x: 42,
        y: 62,
        what: "Structured data carrying organization, service, website, and FAQ facts.",
        why: "It makes entities and trust surfaces machine-readable.",
        impact: "Entity understanding, trust, rich results, AI fact extraction.",
        next: "Cover Organization, WebSite, Service, and FAQ where appropriate.",
      },
      {
        id: "social",
        label: "OG / Twitter",
        tone: "neutral",
        x: 74,
        y: 60,
        what: "Social metadata that shapes previews and machine-readable content packaging.",
        why: "Clean metadata improves how pages are represented outside classic search.",
        impact: "Previews, shareability, lightweight entity clarity.",
        next: "Make title, description, and image complete for high-value URLs.",
      },
    ],
    edges: [
      ["robots", "sitemap"],
      ["robots", "llmstxt"],
      ["llmstxt", "aitxt"],
      ["llmstxt", "schema"],
      ["schema", "social"],
      ["sitemap", "schema"],
    ],
  },
  issues: {
    title: "Issue dependency graph",
    subtitle:
      "Prioritize blockers, easy wins, and fix packs by understanding which surfaces depend on each other.",
    nodes: [
      {
        id: "blocked-bots",
        label: "Blocked AI bots",
        tone: "warning",
        x: 18,
        y: 18,
        what: "Important AI bots cannot access the site or selected public surfaces.",
        why: "Access failures suppress AI discoverability before content quality even matters.",
        impact: "AI visibility, llms.txt usefulness, answer reuse.",
        next: "Fix crawler policies before rewriting pages.",
      },
      {
        id: "missing-schema",
        label: "Missing schema",
        tone: "warning",
        x: 64,
        y: 18,
        what: "Key entity pages lack structured data or carry weak machine-readable facts.",
        why: "Entity ambiguity makes citation trust worse.",
        impact: "Trust surfaces, AI fact extraction, rich results.",
        next: "Ship minimum Organization, WebSite, Service, and FAQ schema.",
      },
      {
        id: "stale-content",
        label: "Stale service pages",
        tone: "neutral",
        x: 22,
        y: 66,
        what: "Commercial pages are old, vague, or proof-light.",
        why: "Even if technically crawlable, stale pages are weak evidence sources.",
        impact: "Conversion, AI quoting, sales confidence.",
        next: "Refresh high-intent pages and add proof-led blocks.",
      },
      {
        id: "thin-trust",
        label: "Thin trust layer",
        tone: "warning",
        x: 66,
        y: 66,
        what: "About, contact, legal, authorship, and case-study signals are thin or inconsistent.",
        why: "Trust gaps reduce willingness to rank, cite, and convert.",
        impact: "Entity confidence, founder credibility, lead quality.",
        next: "Strengthen organization facts, policies, credentials, and case-study evidence.",
      },
    ],
    edges: [
      ["blocked-bots", "stale-content"],
      ["blocked-bots", "missing-schema"],
      ["missing-schema", "thin-trust"],
      ["stale-content", "thin-trust"],
    ],
  },
  trust: {
    title: "Entity, fact, and trust graph",
    subtitle:
      "Track how organization facts, services, authors, legal pages, and external references support one another.",
    nodes: [
      {
        id: "org",
        label: "Organization",
        tone: "accent",
        x: 44,
        y: 12,
        what: "The canonical business entity that all site facts should resolve to.",
        why: "Without one stable entity, AI systems see fragmented or conflicting signals.",
        impact: "Brand facts, schema, legal pages, external references.",
        next: "Make the organization name, description, contacts, and offerings consistent.",
      },
      {
        id: "services",
        label: "Services",
        tone: "neutral",
        x: 16,
        y: 42,
        what: "Commercial capabilities and offers linked to the organization.",
        why: "Services show what the entity actually does, not only what it claims.",
        impact: "Commercial intent, schema, client delivery narratives.",
        next: "Align service naming across pages, schema, and reporting packs.",
      },
      {
        id: "authors",
        label: "Authors / experts",
        tone: "neutral",
        x: 72,
        y: 42,
        what: "Named humans, authorship surfaces, and expert attribution.",
        why: "Expert visibility raises trust in both search and AI summaries.",
        impact: "E-E-A-T, proof density, fact confidence.",
        next: "Add authorship, credentials, and links to supporting case studies.",
      },
      {
        id: "legal",
        label: "Legal / policy",
        tone: "warning",
        x: 20,
        y: 76,
        what: "Policy, privacy, editorial, and ownership surfaces.",
        why: "These surfaces validate legitimacy and clarify governance.",
        impact: "Trust, compliance, risk review, scanner export safety.",
        next: "Keep policy and ownership details current and publicly reachable.",
      },
      {
        id: "external",
        label: "External profiles",
        tone: "neutral",
        x: 68,
        y: 76,
        what: "Citations, profiles, directories, or other references outside the main site.",
        why: "External corroboration reduces single-source fragility.",
        impact: "Entity confirmation, brand consistency, referral trust.",
        next: "Align core facts across LinkedIn, maps, directories, and market profiles.",
      },
    ],
    edges: [
      ["org", "services"],
      ["org", "authors"],
      ["org", "legal"],
      ["org", "external"],
      ["authors", "external"],
      ["services", "legal"],
    ],
  },
};

const modeSelect = document.querySelector("#graph-mode");
const graphCanvas = document.querySelector("#graph-canvas");
const graphTitle = document.querySelector("#graph-title");
const graphSubtitle = document.querySelector("#graph-subtitle");
const graphNodeCard = document.querySelector("#graph-node-card");
const graphAnswer = document.querySelector("#graph-answer");
const exportButton = document.querySelector("#graph-export");
const questionButtons = document.querySelectorAll(".graph-question");

let currentMode = "site";
let activeNode = null;
const query = new URLSearchParams(window.location.search);

function toneClass(tone) {
  if (tone === "warning") return "graph-node warning";
  if (tone === "accent") return "graph-node accent";
  return "graph-node";
}

function renderGraph(modeKey) {
  currentMode = modeKey;
  const mode = graphModes[modeKey];
  graphTitle.textContent = mode.title;
  graphSubtitle.textContent = mode.subtitle;
  graphCanvas.innerHTML = "";

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 100 100");
  svg.setAttribute("class", "graph-edges");

  mode.edges.forEach(([fromId, toId]) => {
    const from = mode.nodes.find((node) => node.id === fromId);
    const to = mode.nodes.find((node) => node.id === toId);
    if (!from || !to) return;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", String(from.x + 8));
    line.setAttribute("y1", String(from.y + 5));
    line.setAttribute("x2", String(to.x + 8));
    line.setAttribute("y2", String(to.y + 5));
    line.setAttribute("class", "graph-line");
    svg.appendChild(line);
  });

  graphCanvas.appendChild(svg);

  mode.nodes.forEach((node) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = toneClass(node.tone);
    button.style.left = `${node.x}%`;
    button.style.top = `${node.y}%`;
    button.textContent = node.label;
    button.addEventListener("click", () => selectNode(node));
    graphCanvas.appendChild(button);
  });

  selectNode(mode.nodes[0]);
}

function selectNode(node) {
  activeNode = node;
  graphNodeCard.innerHTML = `
    <strong>${node.label}</strong>
    <p>${node.what}</p>
    <p><strong>Why:</strong> ${node.why}</p>
    <p><strong>Impact:</strong> ${node.impact}</p>
    <p><strong>Next:</strong> ${node.next}</p>
  `;
  graphAnswer.textContent = node.what;
}

function answerQuestion(question) {
  if (!activeNode) return;
  const answerMap = {
    what: activeNode.what,
    why: activeNode.why,
    impact: activeNode.impact,
    next: activeNode.next,
  };
  graphAnswer.textContent = answerMap[question] || activeNode.what;
}

function exportCurrentGraph() {
  const payload = {
    mode: currentMode,
    ...graphModes[currentMode],
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: "application/json",
  });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = `discoverability-graph-${currentMode}.json`;
  link.click();
  URL.revokeObjectURL(href);
}

modeSelect.addEventListener("change", (event) => {
  renderGraph(event.target.value);
});

questionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    answerQuestion(button.dataset.question);
  });
});

exportButton.addEventListener("click", exportCurrentGraph);

async function bootstrapGraph() {
  const source = query.get("source");
  const id = query.get("id");
  const api = query.get("api");
  if (source && id && api) {
    try {
      const endpoint =
        source === "scan_job"
          ? `${api}/graph-runtime/scan-job/${id}`
          : `${api}/graph-runtime/audit-run/${id}`;
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`Unable to load dynamic graph: ${response.status}`);
      }
      const payload = await response.json();
      graphModes.dynamic = {
        title: `Dynamic graph · ${payload.source_type} ${payload.source_id}`,
        subtitle: (payload.change_summary || []).join(" ") || "Dynamic graph loaded from machine-readable runtime data.",
        nodes: (payload.nodes || []).map((node, index) => ({
          id: node.id,
          label: node.label,
          tone:
            node.severity === "high"
              ? "warning"
              : node.node_type === "target" || node.node_type === "audit_run"
                ? "accent"
                : "neutral",
          x: 12 + ((index % 3) * 28),
          y: 12 + (Math.floor(index / 3) * 22),
          what: node.metadata?.recommended_action || node.node_type,
          why: `This ${node.node_type} is part of the live discoverability graph.`,
          impact: node.severity ? `Severity: ${node.severity}` : "Context node",
          next:
            node.metadata?.recommended_action ||
            "Open the task bundle and fix pack to continue.",
        })),
        edges: (payload.edges || []).map((edge) => [edge.source, edge.target]),
      };
      const option = document.createElement("option");
      option.value = "dynamic";
      option.textContent = "Dynamic runtime graph";
      modeSelect.prepend(option);
      modeSelect.value = "dynamic";
      renderGraph("dynamic");
      return;
    } catch (_error) {
      // Fall back to the static teaching modes.
    }
  }
  renderGraph(currentMode);
}

bootstrapGraph();
