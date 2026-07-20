# Phase 2

- Heuristic Scoring Engine
- Risk Score Generation (0–100)
- Verdict Generation (SAFE / SUSPICIOUS / DANGEROUS)
- Confidence Levels (LOW / MEDIUM / HIGH)
- Triggered Rule Count
- Human-Readable Reasons
- Score Capping (Max: 100)
- Config-Driven Risk Weights
- Logging Support
- Benchmarking Support
- Optional HTTPS Penalty
- Phase 1 Integration
- JSON-Compatible Response Structure

Scoring Rules:

- IP Address (+25)
- High Entropy (+20)
- Brand Mismatch (+20)
- Suspicious TLD (+15)
- Lookalike Detection (+15)
- 3+ Hyphens (+10)
- 4+ Subdomains (+10)
- URL Contains @ (+10)
- URL Length > 75 (+5)

Tests:

- Phase 2: 32/32 Passed
- Total Project Tests: 82/82 Passed

Status:

COMPLETED