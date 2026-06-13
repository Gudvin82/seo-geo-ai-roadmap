async function activeTabUrl() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.url || "";
}

document.getElementById("audit").addEventListener("click", async () => {
  const api = document.getElementById("api").value.replace(/\/$/, "");
  const url = await activeTabUrl();
  const response = await fetch(`${api}/scanner/url-audit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Scanner-Session": crypto.randomUUID()
    },
    body: JSON.stringify({
      url,
      mode: "passive",
      limitations_accepted: true
    })
  });
  document.getElementById("status").textContent = await response.text();
});
