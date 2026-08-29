/**
 * PhishScope Warning Page Logic.
 * 
 * "Continue Anyway" sends a message to background.js which manages
 * the in-memory TEMP_WHITELIST. This page NEVER writes to storage directly.
 * 
 * "Go Back" sends a message to background.js to close the tab.
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const targetUrl = urlParams.get('url');

  if (!targetUrl) {
    document.getElementById('target-url').textContent = "Unknown URL";
    return;
  }

  document.getElementById('target-url').textContent = targetUrl;

  // Load cached warning data from background.js
  chrome.storage.local.get(['phishscope_last_warning'], (res) => {
    const data = res.phishscope_last_warning;
    if (data && data.url === targetUrl) {
      // Confidence
      document.getElementById('target-confidence').textContent =
        (data.confidence || "HIGH").replace(/_/g, ' ');

      // Risk level
      const riskEl = document.getElementById('risk-level');
      if (riskEl) {
        const conf = data.confidence || "HIGH";
        if (conf === "VERY_HIGH") riskEl.textContent = "CRITICAL";
        else if (conf === "HIGH") riskEl.textContent = "HIGH";
        else riskEl.textContent = "MODERATE";
      }

      // Reasons list
      const reasonsList = document.getElementById('reasons-list');
      reasonsList.innerHTML = '';

      if (data.reasons && data.reasons.length > 0) {
        data.reasons.forEach(r => {
          const li = document.createElement('li');
          li.textContent = r.feature || r;
          reasonsList.appendChild(li);
        });
      } else if (data.summary) {
        const li = document.createElement('li');
        li.textContent = data.summary;
        reasonsList.appendChild(li);
      } else {
        const li = document.createElement('li');
        li.textContent = "Multiple phishing indicators were detected.";
        reasonsList.appendChild(li);
      }
    }
  });

  // ── Continue Anyway ──
  // Sends message to background.js to add URL to in-memory TEMP_WHITELIST
  document.getElementById('btn-continue').addEventListener('click', () => {
    console.log("Continue Anyway clicked for:", targetUrl);
    chrome.runtime.sendMessage({
      action: "whitelist_url",
      url: targetUrl
    });
  });

  // ── Go Back ──
  // Sends message to background.js to close this tab
  document.getElementById('btn-back').addEventListener('click', () => {
    console.log("Go Back clicked.");
    chrome.runtime.sendMessage({ action: "go_back" });
  });
});
