/**
 * PhishScope Suspicious Warning Page Logic.
 * 
 * "Continue" sends a message to background.js to whitelist and navigate.
 * "Go Back" sends a message to background.js to close the tab.
 * 
 * Single confirmation — this is NOT the Dangerous flow.
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const targetUrl = urlParams.get('url');

  if (!targetUrl) {
    document.getElementById('target-url').textContent = "Unknown URL";
    return;
  }

  document.getElementById('target-url').textContent = targetUrl;

  // Load cached warning data
  chrome.storage.local.get(['phishscope_last_suspicious'], (res) => {
    const data = res.phishscope_last_suspicious;
    if (data && data.url === targetUrl) {
      document.getElementById('target-confidence').textContent =
        (data.confidence || "MEDIUM").replace(/_/g, ' ');

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
        li.textContent = "Some suspicious indicators were detected.";
        reasonsList.appendChild(li);
      }
    }
  });

  // ── Continue ──
  document.getElementById('btn-continue').addEventListener('click', () => {
    console.log("[PhishScope] Continue clicked on suspicious page for:", targetUrl);
    chrome.runtime.sendMessage({
      action: "whitelist_url",
      url: targetUrl
    });
  });

  // ── Go Back ──
  document.getElementById('btn-back').addEventListener('click', () => {
    console.log("[PhishScope] Go Back clicked on suspicious page.");
    if (window.history.length > 1) {
      window.history.back();
    } else {
      chrome.runtime.sendMessage({ action: "go_back" });
    }
  });
});
