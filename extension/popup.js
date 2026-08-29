import { analyzeURL } from './utils/api.js';

document.addEventListener('DOMContentLoaded', async () => {
  const urlText = document.getElementById('active-url');
  const loadingState = document.getElementById('loading');
  const errorState = document.getElementById('error-state');
  const resultsState = document.getElementById('results');
  
  loadHistory();

  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tabs || tabs.length === 0) {
      throw new Error("No active tab found");
    }
    
    const url = tabs[0].url;
    console.log("[PhishScope Popup] Analyzing current tab:", url);
    
    // Ignore chrome:// or internal URLs
    if (url.startsWith('chrome://') || url.startsWith('chrome-extension://') || url.startsWith('edge://') || url.startsWith('about:')) {
      urlText.textContent = "Internal Browser Page";
      showError("Cannot analyze internal browser pages.");
      return;
    }
    
    urlText.textContent = url;
    loadingState.classList.remove('hidden');

    const result = await analyzeURL(url);
    
    console.log("[PhishScope Popup] API result:", result.hybrid.verdict);
    console.log("[PhishScope Popup] Decision source:", result.hybrid.decision_source || "hybrid");
    
    loadingState.classList.add('hidden');
    renderResults(result);
    saveToHistory(url, result.hybrid.verdict);

  } catch (error) {
    loadingState.classList.add('hidden');
    showError(error.message);
  }
});

function renderResults(result) {
  const resultsState = document.getElementById('results');
  const verdictBanner = document.getElementById('verdict-banner');
  const verdictText = document.getElementById('verdict-text');
  
  resultsState.classList.remove('hidden');
  
  const hybrid = result.hybrid;
  const verdict = hybrid.verdict;
  const isTrustedDomain = hybrid.trusted_domain === true;
  const decisionSource = hybrid.decision_source || 'hybrid';
  
  // Set Verdict
  verdictText.textContent = verdict;
  verdictBanner.className = 'verdict-banner'; // reset
  if (verdict === 'SAFE') verdictBanner.classList.add('verdict-safe');
  else if (verdict === 'SUSPICIOUS') verdictBanner.classList.add('verdict-suspicious');
  else verdictBanner.classList.add('verdict-dangerous');

  // Show trusted domain badge
  const trustedBadge = document.getElementById('trusted-badge');
  if (trustedBadge) {
    if (isTrustedDomain) {
      trustedBadge.classList.remove('hidden');
    } else {
      trustedBadge.classList.add('hidden');
    }
  }

  // Trigger Notification for Dangerous
  if (verdict === 'DANGEROUS') {
    chrome.runtime.sendMessage({
      action: "show_notification",
      message: `DANGEROUS SITE DETECTED: The site you are visiting matches known phishing signatures.`
    });
  }
  
  // Set Stats
  document.getElementById('confidence-val').textContent = hybrid.confidence.replace('_', ' ');
  document.getElementById('hybrid-val').textContent = hybrid.score;

  // Set Explanation
  if (result.explanation && !result.explanation.error) {
    document.getElementById('summary-text').textContent = result.explanation.summary;
    
    if (result.explanation.top_features && result.explanation.top_features.length > 0) {
      document.getElementById('features-container').classList.remove('hidden');
      const list = document.getElementById('features-list');
      list.innerHTML = '';
      
      result.explanation.top_features.forEach(feat => {
        const li = document.createElement('li');
        li.className = 'feature-item';
        
        const isPos = feat.impact.startsWith('+');
        const impactClass = isPos ? 'impact-pos' : 'impact-neg';
        
        li.innerHTML = `<span>${feat.feature}</span><span class="${impactClass}">${feat.impact}</span>`;
        list.appendChild(li);
      });
    }
  }
}

function showError(msg) {
  const errState = document.getElementById('error-state');
  errState.classList.remove('hidden');
  document.getElementById('error-message').textContent = msg;
}

function loadHistory() {
  chrome.storage.local.get(['phishscope_history'], (result) => {
    const history = result.phishscope_history || [];
    renderHistory(history);
  });
}

function saveToHistory(url, verdict) {
  chrome.storage.local.get(['phishscope_history'], (result) => {
    let history = result.phishscope_history || [];
    
    // Remove if already exists to move to top
    history = history.filter(h => h.url !== url);
    
    history.unshift({ url, verdict });
    
    // Keep last 50
    if (history.length > 50) {
      history.pop();
    }
    
    chrome.storage.local.set({ phishscope_history: history });
    renderHistory(history);
  });
}

function renderHistory(history) {
  const list = document.getElementById('history-list');
  list.innerHTML = '';
  
  history.forEach(item => {
    const li = document.createElement('li');
    li.className = 'history-item';
    
    let colorClass = 'text-gray-400';
    if (item.verdict === 'SAFE') colorClass = 'color: var(--accent);';
    if (item.verdict === 'SUSPICIOUS') colorClass = 'color: var(--warning);';
    if (item.verdict === 'DANGEROUS') colorClass = 'color: var(--danger);';
    
    li.innerHTML = `
      <span class="history-url">${item.url}</span>
      <span style="${colorClass} font-weight: bold;">${item.verdict}</span>
    `;
    list.appendChild(li);
  });
}
