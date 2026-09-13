"""Decision tree logic for the Hybrid Detection Engine."""

def apply_rules(heuristic_verdict: str, ml_prediction: str, confidence: str, heuristic_score: int = 0) -> tuple[str | None, str | None, list[str]]:
    """
    Apply hardcoded override rules.
    Returns (override_verdict, override_confidence, reasons).
    If no rule matched, returns (None, None, []).

    Threshold guide:
      CORROBORATION_THRESHOLD = 15  — minimum score to treat as a meaningful signal.
      HIGH_CORROBORATION_THRESHOLD = 35 — strong heuristic evidence, escalate verdict.

    Heuristic score bands (config.py):
      0–30   → SAFE
      31–60  → SUSPICIOUS
      61–100 → DANGEROUS
    """
    reasons = []
    CORROBORATION_THRESHOLD = 15      # meaningful heuristic signal
    HIGH_CORROBORATION_THRESHOLD = 35  # strong heuristic signal — escalate to DANGEROUS

    # ── Rule 1: Both engines agree — dangerous ──────────────────────────────
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "PHISHING":
        reasons.append("Both heuristic and ML engines strongly indicate phishing.")
        return "DANGEROUS", "VERY_HIGH", reasons

    # ── Rule 2: Both engines agree — safe ───────────────────────────────────
    if heuristic_verdict == "SAFE" and ml_prediction == "SAFE":
        reasons.append("Both engines indicate the URL is safe.")
        return "SAFE", "HIGH", reasons

    # ── Rule 3: Heuristic SAFE + ML PHISHING ────────────────────────────────
    if heuristic_verdict == "SAFE" and ml_prediction == "PHISHING":
        if heuristic_score <= CORROBORATION_THRESHOLD:
            # Heuristic sees nothing meaningful — trust the heuristic.
            reasons.append("ML flagged as phishing but heuristic score is low. No meaningful indicators found. Treating as safe.")
            return "SAFE", "MEDIUM", reasons
        elif heuristic_score <= HIGH_CORROBORATION_THRESHOLD:
            if confidence in ("VERY_HIGH", "HIGH"):
                reasons.append("ML identified phishing with corroborating heuristic signals.")
                return "SUSPICIOUS", "MEDIUM", reasons
            else:
                reasons.append("ML flagged phishing but confidence is moderate and heuristic signals are minor. Treating as safe.")
                return "SAFE", "LOW", reasons
        else:
            # Strong heuristic evidence + ML agrees → escalate to DANGEROUS
            reasons.append("Strong heuristic evidence combined with ML phishing prediction.")
            return "DANGEROUS", "HIGH", reasons

    # ── Rule 4: Heuristic DANGEROUS + ML SAFE ───────────────────────────────
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "SAFE":
        # ML hasn't seen this novel pattern — trust the heuristic when score is high
        if heuristic_score >= HIGH_CORROBORATION_THRESHOLD:
            reasons.append("Heuristic strongly flagged as dangerous. ML may not recognise this novel pattern.")
            return "DANGEROUS", "MEDIUM", reasons
        else:
            reasons.append("Heuristic flagged as dangerous despite safe ML prediction.")
            return "SUSPICIOUS", "MEDIUM", reasons

    # ── Rule 5: Heuristic SUSPICIOUS + ML PHISHING ──────────────────────────
    if heuristic_verdict == "SUSPICIOUS" and ml_prediction == "PHISHING":
        reasons.append("Suspicious heuristics corroborated by ML phishing prediction.")
        return "DANGEROUS", "HIGH", reasons

    # ── Rule 6: Heuristic SUSPICIOUS + ML SAFE ──────────────────────────────
    if heuristic_verdict == "SUSPICIOUS" and ml_prediction == "SAFE":
        # Heuristic has a signal but ML disagrees — keep as suspicious, don't escalate
        reasons.append("Heuristic indicators present but ML predicts safe. Proceeding with caution.")
        return "SUSPICIOUS", "LOW", reasons

    return None, None, []
