/**
 * PhishScope Background Service Worker (Manifest V3)
 * 
 * Always-on browser security assistant.
 * Intercepts ALL navigations, analyzes them via the Flask API,
 * and redirects dangerous URLs to the warning page.
 * 
 * ARCHITECTURE: This script does NOT maintain its own trusted domain list.
 * The single source of truth is backend/data/trusted_domains.txt, which is
 * checked by hybrid/engine.py. Every URL is sent to POST /analyze.
 * 
 * The user NEVER needs to click the extension icon.
 */

import { analyzeURL } from './utils/api.js';

// ─── In-Memory Temporary Whitelist ────────────────────────────────
// Lives ONLY in service worker memory. Cleared on browser restart.
// URLs are ONLY added when the user clicks "Continue Anyway".
const TEMP_WHITELIST = new Set();

// ─── Lifecycle ────────────────────────────────────────────────────
chrome.runtime.onInstalled.addListener(() => {
  console.log("[PhishScope] Installed. Always-on protection is active.");
  chrome.storage.local.remove('phishscope_whitelist');
  chrome.storage.local.get(['phishscope_history'], (res) => {
    if (!res.phishscope_history) {
      chrome.storage.local.set({ phishscope_history: [] });
    }
  });
});

console.log("[PhishScope] Started.");
console.log("[PhishScope] Waiting for navigation...");

// ─── Message handler ──────────────────────────────────────────────
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "show_notification") {
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/48.png",
      title: "⚠ PhishScope Warning",
      message: request.message || "This website may be unsafe.",
      priority: 2
    });
  }

  if (request.action === "whitelist_url" && request.url) {
    TEMP_WHITELIST.add(request.url);
    console.log("[PhishScope] Continue Anyway clicked. Whitelisted:", request.url);
    if (sender.tab && sender.tab.id) {
      chrome.tabs.update(sender.tab.id, { url: request.url });
    }
    sendResponse({ success: true });
  }

  if (request.action === "go_back") {
    console.log("[PhishScope] Go Back clicked.");
    if (sender.tab && sender.tab.id) {
      chrome.tabs.remove(sender.tab.id);
    }
    sendResponse({ success: true });
  }

  return true;
});

// ─── Save to history ──────────────────────────────────────────────
async function saveToHistory(url, verdict) {
  const res = await chrome.storage.local.get(['phishscope_history']);
  let history = res.phishscope_history || [];
  history = history.filter(h => h.url !== url);
  history.unshift({
    url,
    verdict,
    timestamp: new Date().toISOString()
  });
  if (history.length > 50) history.pop();
  await chrome.storage.local.set({ phishscope_history: history });
}

// ─── Show toast via content script injection ──────────────────────
async function showToast(tabId, type, hostname) {
  const isTrusted = type === 'trusted';
  const isSafe = type === 'safe';
  
  const title = isTrusted ? 'TRUSTED WEBSITE' : 'PHISHSCOPE CHECK PASSED';
  const subtitle = isTrusted
    ? 'This domain is recognized by PhishScope.'
    : 'No phishing indicators were detected.';
  const color = '#22C55E';

  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      func: (title, subtitle, hostname, color) => {
        const existing = document.getElementById('phishscope-safe-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'phishscope-safe-toast';
        toast.innerHTML = `
          <div style="
            position:fixed;top:20px;right:20px;z-index:2147483647;
            background:rgba(17,24,39,0.95);
            border:1px solid ${color}80;
            border-radius:12px;padding:16px 24px;
            display:flex;align-items:center;gap:12px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);
            font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
            animation:phishscope-fadein 0.3s ease-out;max-width:340px;
          ">
            <div style="width:36px;height:36px;background:${color}33;border-radius:50%;
              display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <span style="color:${color};font-size:20px;">✓</span>
            </div>
            <div>
              <div style="color:${color};font-weight:bold;font-size:13px;letter-spacing:0.5px;">${title}</div>
              <div style="color:#9CA3AF;font-size:12px;margin-top:2px;">${subtitle}</div>
              <div style="color:#D1D5DB;font-size:11px;margin-top:2px;opacity:0.8;">${hostname}</div>
            </div>
          </div>
          <style>
            @keyframes phishscope-fadein {
              from { opacity:0; transform:translateY(-10px); }
              to { opacity:1; transform:translateY(0); }
            }
          </style>
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
          toast.style.transition = 'opacity 0.5s ease-out';
          toast.style.opacity = '0';
          setTimeout(() => toast.remove(), 500);
        }, 2500);
      },
      args: [title, subtitle, hostname, color]
    });
    console.log(`[PhishScope] ${title} toast displayed for:`, hostname);
  } catch (err) {
    console.log("[PhishScope] Could not inject toast (restricted page):", err.message);
  }
}

// ─── Schedule toast after page load ───────────────────────────────
function scheduleToast(tabId, type, url) {
  chrome.webNavigation.onCompleted.addListener(
    function onComplete(completedDetails) {
      if (completedDetails.tabId === tabId && completedDetails.frameId === 0) {
        chrome.webNavigation.onCompleted.removeListener(onComplete);
        try {
          const hostname = new URL(url).hostname;
          showToast(tabId, type, hostname);
        } catch {}
      }
    }
  );
}

// ─── CORE: Navigation Interception ───────────────────────────────
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return;

  const url = details.url;

  // Skip internal/extension pages
  if (
    url.startsWith('chrome://') ||
    url.startsWith('chrome-extension://') ||
    url.startsWith('edge://') ||
    url.startsWith('about:') ||
    url.startsWith('data:') ||
    url.startsWith('blob:') ||
    url.startsWith('file://')
  ) {
    return;
  }

  console.log("[PhishScope] URL intercepted:", url);

  // Check in-memory whitelist (Continue Anyway ONLY)
  if (TEMP_WHITELIST.has(url)) {
    console.log("[PhishScope] Whitelisted (Continue Anyway), allowing:", url);
    return;
  }

  // ── Analyze via Flask API (single source of truth) ──
  try {
    console.log("[PhishScope] Analyzing URL:", url);
    const result = await analyzeURL(url);

    if (!result || !result.hybrid) {
      console.warn("[PhishScope] No hybrid result for:", url);
      return;
    }

    const verdict = result.hybrid.verdict;
    const isTrustedDomain = result.hybrid.trusted_domain === true;
    const decisionSource = result.hybrid.decision_source || "hybrid";
    
    console.log("[PhishScope] Verdict:", verdict);
    console.log("[PhishScope] Trusted domain:", isTrustedDomain);
    console.log("[PhishScope] Decision source:", decisionSource);

    await saveToHistory(url, verdict);

    if (verdict === "DANGEROUS") {
      // ── DANGEROUS: Redirect to warning page ──
      await chrome.storage.local.set({
        phishscope_last_warning: {
          url: url,
          confidence: result.hybrid.confidence || "HIGH",
          score: result.hybrid.score || 0,
          reasons: result.explanation ? result.explanation.top_features : [],
          summary: result.explanation ? result.explanation.summary : "This URL appears dangerous."
        }
      });

      const warningUrl = chrome.runtime.getURL(
        `warning.html?url=${encodeURIComponent(url)}`
      );
      chrome.tabs.update(details.tabId, { url: warningUrl });
      console.log("[PhishScope] WARNING displayed. BLOCKED:", url);

      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/48.png",
        title: "⚠ PhishScope Warning",
        message: `Dangerous website blocked: ${new URL(url).hostname}`,
        priority: 2
      });

    } else if (verdict === "SAFE") {
      // ── SAFE: Show appropriate toast ──
      const toastType = isTrustedDomain ? 'trusted' : 'safe';
      console.log("[PhishScope] SAFE, allowing:", url);
      scheduleToast(details.tabId, toastType, url);

    } else {
      // ── SUSPICIOUS or other: Allow navigation, no toast ──
      // The popup will show the real verdict if the user clicks the icon
      console.log("[PhishScope] SUSPICIOUS, allowing without toast:", url);
    }

  } catch (err) {
    console.error("[PhishScope] Auto-scan error:", err.message);
    // On API failure, allow navigation (fail open)
  }
});
