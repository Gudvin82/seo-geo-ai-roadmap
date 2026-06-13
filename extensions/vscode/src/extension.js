function activate(context) {
  const vscode = require("vscode");
  const makeCommand = (title, body) =>
    vscode.commands.registerCommand(title, async () => {
      const panel = vscode.window.createWebviewPanel(
        "seoGeoAi",
        "SEO GEO AI",
        vscode.ViewColumn.One,
        {}
      );
      panel.webview.html = `<html><body><h1>${body.heading}</h1><p>${body.copy}</p></body></html>`;
    });

  context.subscriptions.push(
    makeCommand("seoGeoAi.audit", {
      heading: "Run Audit",
      copy: "Connect this extension to a local or self-hosted backend and trigger /geo audit flows."
    }),
    makeCommand("seoGeoAi.summary", {
      heading: "Open Summary",
      copy: "Use the report and executive endpoints to view outputs without leaving the editor."
    }),
    makeCommand("seoGeoAi.agentMode", {
      heading: "Start Agent Mode",
      copy: "Launch agent-plan or agent-review flows against the active project."
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
