import { useState } from 'react';

const sections = [
  { id: 'overview',   label: 'Overview' },
  { id: 'pipeline',   label: 'Detection Pipeline' },
  { id: 'ml',         label: 'Machine Learning' },
  { id: 'heuristic',  label: 'Heuristic Analysis' },
  { id: 'hybrid',     label: 'Hybrid Decision' },
  { id: 'xai',        label: 'Explainable AI' },
  { id: 'verdicts',   label: 'Risk Levels' },
  { id: 'api',        label: 'API Reference' },
];

const Documentation = () => {
  const [active, setActive] = useState('overview');

  return (
    <div className="w-full min-h-screen bg-ms">

      {/* Header */}
      <div className="bg-si border-b border-si-700">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-14">
          <p className="label-caps text-sv-light mb-4">Technical Documentation</p>
          <h1 className="text-h-lg font-semibold text-sw">How PhishScope Works</h1>
        </div>
      </div>

      <div className="max-w-content mx-auto px-5 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">

          {/* Sidebar — desktop */}
          <aside className="lg:w-56 shrink-0">
            <div className="surface-card p-4 lg:sticky lg:top-24">
              <nav aria-label="Documentation sections">
                <ul className="space-y-1">
                  {sections.map((s) => (
                    <li key={s.id}>
                      <button
                        onClick={() => {
                          setActive(s.id);
                          document.getElementById(s.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }}
                        className={`w-full text-left px-3 py-2.5 rounded-card-sm text-body-sm transition-colors ${
                          active === s.id
                            ? 'bg-si text-sw font-medium'
                            : 'text-cg hover:text-si hover:bg-ms'
                        }`}
                        aria-current={active === s.id ? 'true' : undefined}
                      >
                        {s.label}
                      </button>
                    </li>
                  ))}
                </ul>
              </nav>
            </div>
          </aside>

          {/* Content */}
          <main className="flex-1 space-y-10" aria-label="Documentation content">

            <section id="overview" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Overview</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                PhishScope is a hybrid URL analysis platform. It detects phishing and malicious URLs by combining a machine learning model with a heuristic rule engine, arbitrated by a consensus decision layer. Every verdict includes an explainable AI breakdown.
              </p>
              <p className="text-body text-cg leading-relaxed">
                The system is designed to minimize both false positives (flagging safe sites) and false negatives (missing real phishing). The hybrid approach means neither engine can dominate blindly.
              </p>
            </section>

            <section id="pipeline" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Detection Pipeline</h2>
              <ol className="space-y-5">
                {[
                  ['01 URL Input',            'A URL string is submitted via the API or browser extension.'],
                  ['02 Feature Extraction',   'The URL is parsed into 20+ numerical and categorical features: length, entropy, subdomain depth, TLD reputation, lookalike scores, punycode presence, and more.'],
                  ['03 ML Analysis',          'A trained Random Forest model outputs a PHISHING or SAFE prediction with a confidence probability.'],
                  ['04 Heuristic Analysis',   'A rule-based engine scores the URL against known structural threat patterns and returns a 0–100 heuristic score.'],
                  ['05 Hybrid Decision',      'The consensus engine compares ML and heuristic signals. Agreement with high confidence → strong verdict. Disagreement → SUSPICIOUS.'],
                  ['06 Final Verdict',        'Returns SAFE, SUSPICIOUS, or DANGEROUS with hybrid score, confidence level, detection reasons, and XAI feature explanation.'],
                ].map(([title, desc]) => (
                  <li key={title} className="flex gap-4">
                    <span className="text-caption font-semibold text-ag mt-1 shrink-0 w-5">{title.split(' ')[0]}</span>
                    <div>
                      <p className="text-body-sm font-medium text-si mb-1">{title.split(' ').slice(1).join(' ')}</p>
                      <p className="text-body-sm text-cg leading-relaxed">{desc}</p>
                    </div>
                  </li>
                ))}
              </ol>
            </section>

            <section id="ml" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Machine Learning</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                The model is a Random Forest classifier trained on approximately 100,000 labeled URLs from public phishing and legitimate datasets. It outputs a binary prediction (PHISHING / SAFE) and a confidence probability (0.0–1.0).
              </p>
              <p className="text-body text-cg leading-relaxed">
                The model is not retrained at runtime. It is a pre-trained artifact loaded at startup. Predictions are deterministic for any given URL.
              </p>
            </section>

            <section id="heuristic" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Heuristic Analysis</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                The heuristic engine applies rule-based scoring to structural URL properties. Each matched rule contributes to a cumulative score from 0 (very safe) to 100 (very suspicious). Rules include detection of IP-literal hostnames, excessive subdomains, brand lookalike patterns, known malicious TLDs, and encoded URL patterns.
              </p>
            </section>

            <section id="hybrid" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Hybrid Decision Engine</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                The consensus engine combines both signals with confidence-aware logic:
              </p>
              <ul className="space-y-2 text-body-sm text-cg mb-4">
                {[
                  'Both agree SAFE → SAFE with high confidence',
                  'Both agree PHISHING → DANGEROUS with high confidence',
                  'ML says PHISHING, heuristic says SAFE (with non-zero score) → SUSPICIOUS',
                  'ML says PHISHING with VERY_HIGH confidence (even if heuristic score is 0) → DANGEROUS',
                  'ML says SAFE, heuristic flags high → SUSPICIOUS',
                ].map((rule) => (
                  <li key={rule} className="flex gap-2">
                    <span className="text-sv shrink-0 mt-0.5">→</span>
                    {rule}
                  </li>
                ))}
              </ul>
              <p className="text-body text-cg leading-relaxed">
                This prevents either engine from producing false verdicts in isolation and avoids the edge case where a very confident ML prediction is silently overridden.
              </p>
            </section>

            <section id="xai" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Explainable AI (SHAP)</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                SHAP (SHapley Additive exPlanations) values are computed for each prediction to explain which URL features contributed most to the ML model's decision and in which direction.
              </p>
              <p className="text-body text-cg leading-relaxed">
                The API response includes a plain-language <code className="bg-ms px-1.5 py-0.5 rounded text-caption font-mono text-si">summary</code> and a <code className="bg-ms px-1.5 py-0.5 rounded text-caption font-mono text-si">top_features</code> array with feature names and signed impact values.
              </p>
            </section>

            <section id="verdicts" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">Risk Levels</h2>
              <div className="space-y-4">
                <div className="rounded-card-sm p-4 border-l-4" style={{ background: '#f0fdf4', borderLeftColor: '#16a34a' }}>
                  <p className="text-body-sm font-semibold mb-1" style={{ color: '#16a34a' }}>SAFE</p>
                  <p className="text-body-sm" style={{ color: '#166534' }}>No significant phishing indicators detected. Both the ML model and heuristic engine found no strong threat signals. Proceed with normal caution.</p>
                </div>
                <div className="rounded-card-sm p-4 border-l-4" style={{ background: '#fffbeb', borderLeftColor: '#d97706' }}>
                  <p className="text-body-sm font-semibold mb-1" style={{ color: '#d97706' }}>SUSPICIOUS</p>
                  <p className="text-body-sm" style={{ color: '#92400e' }}>Mixed signals — at least one engine flagged the URL but consensus is not definitive. The URL has structural characteristics worth investigating before proceeding.</p>
                </div>
                <div className="rounded-card-sm p-4 border-l-4" style={{ background: '#fef2f2', borderLeftColor: '#dc2626' }}>
                  <p className="text-body-sm font-semibold mb-1" style={{ color: '#dc2626' }}>DANGEROUS</p>
                  <p className="text-body-sm" style={{ color: '#991b1b' }}>Strong phishing indicators detected by both the ML model and heuristic engine. The URL exhibits characteristics consistent with known phishing campaigns. Do not proceed.</p>
                </div>
              </div>
            </section>

            <section id="api" className="surface-card p-8">
              <h2 className="text-h-sm font-semibold text-si mb-5">API Reference</h2>
              <p className="text-body text-cg leading-relaxed mb-4">
                The PhishScope backend exposes a single analysis endpoint.
              </p>
              <div className="code-block">
{`POST /analyze
Content-Type: application/json

{ "url": "https://example.com" }

// Response
{
  "heuristic": {
    "score": 20,
    "verdict": "SAFE"
  },
  "ml": {
    "prediction": "SAFE",
    "confidence": 0.12
  },
  "hybrid": {
    "score": 16,
    "verdict": "SAFE",
    "confidence": "HIGH",
    "reasons": ["Heuristic score is low", "ML model predicts safe"]
  },
  "explanation": {
    "summary": "This URL has no significant phishing indicators.",
    "top_features": [
      { "feature": "url_length", "impact": "-0.14" },
      { "feature": "domain_entropy", "impact": "+0.08" }
    ]
  }
}`}
              </div>
            </section>

          </main>
        </div>
      </div>
    </div>
  );
};

export default Documentation;
