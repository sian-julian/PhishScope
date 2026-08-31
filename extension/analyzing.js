/**
 * PhishScope Analyzing Page Logic
 * 
 * Extracts the target URL from the query string and requests analysis
 * from the background script. Then redirects appropriately based on the result.
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const targetUrl = urlParams.get('url');

  if (!targetUrl) {
    document.getElementById('target-url').textContent = "Unknown URL";
    return;
  }

  document.getElementById('target-url').textContent = targetUrl;

  console.log("[PhishScope] Requesting analysis for:", targetUrl);

  // Ask background script to analyze the URL
  chrome.runtime.sendMessage({
    action: "analyze_url_blocking",
    url: targetUrl
  }, (response) => {
    if (chrome.runtime.lastError) {
      console.error("[PhishScope] Error from background script:", chrome.runtime.lastError.message);
      // On error, fail open and navigate
      window.location.replace(targetUrl);
      return;
    }

    if (!response || !response.success) {
      console.warn("[PhishScope] Analysis failed, allowing navigation.");
      window.location.replace(targetUrl);
      return;
    }

    const { verdict, redirectUrl } = response;
    
    console.log("[PhishScope] Analysis complete. Verdict:", verdict);

    if (verdict === 'SAFE') {
      // Navigate to original URL. The background script has added it to the whitelist.
      window.location.replace(targetUrl);
    } else {
      // Redirect to the appropriate warning page (suspicious or dangerous)
      if (redirectUrl) {
        window.location.replace(redirectUrl);
      } else {
        console.error("[PhishScope] Missing redirect URL for blocked site.");
        window.location.replace(targetUrl);
      }
    }
  });
});
