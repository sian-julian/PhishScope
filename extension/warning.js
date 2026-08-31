/**
 * PhishScope DANGEROUS Warning Page Logic.
 * 
 * "Continue Anyway" requires THREE explicit confirmations before navigating.
 * Each confirmation step shows an inline warning — not a browser dialog.
 * "Go Back" / "Cancel" is available at every stage.
 * Enter key is blocked from advancing confirmations.
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const targetUrl = urlParams.get('url');
  let confirmationStep = 0; // 0 = initial, 1-3 = confirmation stages

  if (!targetUrl) {
    document.getElementById('target-url').textContent = "Unknown URL";
    return;
  }

  document.getElementById('target-url').textContent = targetUrl;

  // Load cached warning data from background.js
  chrome.storage.local.get(['phishscope_last_warning'], (res) => {
    const data = res.phishscope_last_warning;
    if (data && data.url === targetUrl) {
      document.getElementById('target-confidence').textContent =
        (data.confidence || "HIGH").replace(/_/g, ' ');

      const riskEl = document.getElementById('risk-level');
      if (riskEl) {
        const conf = data.confidence || "HIGH";
        if (conf === "VERY_HIGH") riskEl.textContent = "CRITICAL";
        else if (conf === "HIGH") riskEl.textContent = "HIGH";
        else riskEl.textContent = "MODERATE";
      }

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

  // ── Block Enter key from advancing confirmations ──
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      e.stopPropagation();
    }
  });

  const btnContinue = document.getElementById('btn-continue');
  const btnBack = document.getElementById('btn-back');
  const actionsDiv = document.querySelector('.actions');

  // ── Continue Anyway — 3x confirmation flow ──
  btnContinue.addEventListener('click', (e) => {
    e.preventDefault();
    confirmationStep++;
    console.log(`[PhishScope] Dangerous confirmation step ${confirmationStep}/3 for:`, targetUrl);

    if (confirmationStep < 3) {
      // Show inline confirmation overlay
      showConfirmation(confirmationStep);
    } else {
      // Third confirmation — actually navigate
      console.log("[PhishScope] All 3 confirmations complete. Whitelisting:", targetUrl);
      chrome.runtime.sendMessage({
        action: "whitelist_url",
        url: targetUrl
      });
    }
  });

  // ── Go Back ──
  btnBack.addEventListener('click', (e) => {
    e.preventDefault();
    if (confirmationStep > 0) {
      // If in a confirmation step, go back to previous step
      confirmationStep = 0;
      hideConfirmation();
      console.log("[PhishScope] Confirmation cancelled. Back to warning page.");
    } else {
      console.log("[PhishScope] Go Back clicked.");
      if (window.history.length > 1) {
        window.history.back();
      } else {
        chrome.runtime.sendMessage({ action: "go_back" });
      }
    }
  });

  function showConfirmation(step) {
    // Remove existing confirmation overlay if any
    const existing = document.getElementById('confirmation-overlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'confirmation-overlay';
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.7); display: flex; justify-content: center;
      align-items: center; z-index: 10000;
    `;
    overlay.innerHTML = `
      <div style="
        background: #1F2937; border: 1px solid rgba(239,68,68,0.5);
        border-radius: 16px; padding: 32px; max-width: 420px; width: 90%;
        text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.8);
      ">
        <div style="font-size: 40px; margin-bottom: 12px;">🛑</div>
        <h2 style="color: #EF4444; margin: 0 0 12px 0; font-size: 20px;">
          Confirmation ${step} of 3
        </h2>
        <p style="color: #D1D5DB; font-size: 15px; margin-bottom: 24px; line-height: 1.5;">
          Do you really want to continue to this <strong style="color: #EF4444;">dangerous</strong> website?
        </p>
        <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 20px;">
          ${step < 2 ? `You must confirm ${3 - step} more time${3 - step > 1 ? 's' : ''} to proceed.` : 'This is your final confirmation.'}
        </p>
        <div style="display: flex; gap: 12px; justify-content: center;">
          <button id="confirm-cancel" style="
            padding: 12px 24px; border-radius: 8px; font-weight: bold;
            cursor: pointer; border: none; font-size: 14px;
            background: #2563EB; color: white;
            box-shadow: 0 4px 12px rgba(37,99,235,0.3);
          ">Cancel</button>
          <button id="confirm-continue" style="
            padding: 12px 24px; border-radius: 8px; font-weight: bold;
            cursor: pointer; font-size: 13px;
            background: transparent; color: #6B7280;
            border: 1px solid #374151;
          ">Continue Anyway</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Prevent Enter key on the overlay
    overlay.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        e.stopPropagation();
      }
    });

    // Cancel button — go back to the warning page
    document.getElementById('confirm-cancel').addEventListener('click', (e) => {
      e.preventDefault();
      confirmationStep = 0;
      hideConfirmation();
      console.log("[PhishScope] Confirmation cancelled at step", step);
    });

    // Continue button — advance to next confirmation
    document.getElementById('confirm-continue').addEventListener('click', (e) => {
      e.preventDefault();
      confirmationStep++;
      console.log(`[PhishScope] Dangerous confirmation step ${confirmationStep}/3`);

      if (confirmationStep >= 3) {
        // Third confirmation — actually navigate
        hideConfirmation();
        console.log("[PhishScope] All 3 confirmations complete. Whitelisting:", targetUrl);
        chrome.runtime.sendMessage({
          action: "whitelist_url",
          url: targetUrl
        });
      } else {
        // Show next confirmation
        hideConfirmation();
        showConfirmation(confirmationStep);
      }
    });
  }

  function hideConfirmation() {
    const overlay = document.getElementById('confirmation-overlay');
    if (overlay) overlay.remove();
  }
});
