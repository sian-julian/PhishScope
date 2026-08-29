# Phase 9: Extension Manual Testing Guide

Since this is a Chrome Extension, automated testing requires heavy frameworks like Puppeteer or Selenium. For Phase 9, manual testing is the most effective way to verify the `chrome.*` API integrations, permissions, and popup rendering.

## Setup
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top right.
3. Click **Load unpacked**.
4. Select the `phishscope/extension/` directory.
5. Ensure the Flask backend is running (`python backend/app.py`).

## Test Cases

### 1. Legitimate URL Test (SAFE)
1. Open a new tab and navigate to `https://google.com` or `https://github.com`.
2. Click the PhishScope extension icon.
3. **Expected Results:**
   - URL matches the active tab.
   - Verdict displays as **SAFE** (Green badge).
   - Summary indicates the site appears legitimate.
   - No Chrome notification is triggered.

### 2. Phishing URL Test (DANGEROUS)
1. Open a new tab and navigate to `https://g00gle.xyz` or `http://paypal-login.tk`.
2. Click the PhishScope extension icon.
3. **Expected Results:**
   - Verdict displays as **DANGEROUS** (Red badge).
   - High Hybrid Score and Confidence.
   - Summary lists the primary reasons (e.g., lookalike domain, suspicious TLD).
   - **Notification:** A Chrome system notification titled "⚠ WARNING" should appear.

### 3. Local Storage / History Test
1. After running the above two tests, close and reopen the extension popup.
2. **Expected Results:**
   - The "Recently Analyzed" section at the bottom of the popup should display the last two URLs tested along with their color-coded verdicts.

### 4. Error Handling Test (Backend Offline)
1. Stop the Flask backend server.
2. Open the extension and click a URL.
3. **Expected Results:**
   - The loading spinner appears briefly.
   - An error message "Unable to connect to the PhishScope API." is displayed in a red box.
   - No verdict or stats are shown.
