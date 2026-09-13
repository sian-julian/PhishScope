import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/PhishScope-logo.png';

/* ============================================================
   Pipeline steps — genuinely sequential so numbered is correct
   ============================================================ */
const pipeline = [
  { num: '01', label: 'URL Input',          desc: 'A URL is submitted for evaluation.' },
  { num: '02', label: 'Feature Extraction', desc: 'Length, entropy, domain structure, TLD reputation, and 20+ signals extracted.' },
  { num: '03', label: 'ML Analysis',        desc: 'Random Forest model assesses phishing probability across all features.' },
  { num: '04', label: 'Heuristic Analysis', desc: 'Rule-based engine scores known threat patterns and structural anomalies.' },
  { num: '05', label: 'Hybrid Decision',    desc: 'Consensus engine weighs ML and heuristic outputs into a single verdict.' },
  { num: '06', label: 'Final Verdict',      desc: 'SAFE, SUSPICIOUS, or DANGEROUS — with confidence and XAI explanation.' },
];

/* Feature cards — not a sequence, so not numbered */
const capabilities = [
  {
    eyebrow: 'Machine Learning',
    title: 'Random Forest Model',
    desc: 'Trained on 100,000+ labeled URLs, our model surfaces phishing patterns invisible to static rule sets.',
  },
  {
    eyebrow: 'Heuristic Analysis',
    title: 'Rule-Based Evaluation',
    desc: 'Structural URL analysis: entropy, lookalike domains, brand impersonation, and TLD reputation scoring.',
  },
  {
    eyebrow: 'Explainable AI',
    title: 'SHAP-Powered Insights',
    desc: 'Every verdict is explained in plain language — you see exactly which features drove the decision.',
  },
];

const Hero = () => {
  const [url, setUrl] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim()) return;
    navigate(`/analyzer?url=${encodeURIComponent(url.trim())}`);
  };

  return (
    <div className="w-full">

      {/* ── Hero ── */}
      <section className="relative bg-si overflow-hidden hero-grid hero-scan-line">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-20 lg:py-28">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">

            {/* LEFT — text + input */}
            <div>
              <p className="label-caps text-sv-light mb-5 animate-ps-enter">
                AI-Powered URL Security
              </p>

              <h1 className="text-display lg:text-display text-sw font-semibold leading-tight mb-6 animate-ps-enter-1">
                Know what's<br />
                behind every URL.
              </h1>

              <p className="text-body-lg text-ag leading-relaxed mb-10 max-w-md animate-ps-enter-2">
                PhishScope combines machine learning, heuristic analysis, and a hybrid decision engine to detect phishing URLs — with full AI explainability.
              </p>

              {/* URL input */}
              <form onSubmit={handleSubmit} className="animate-ps-enter-3" aria-label="URL analysis form">
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="flex-1 relative">
                    <label htmlFor="hero-url-input" className="sr-only">Enter a URL to analyze</label>
                    <input
                      id="hero-url-input"
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://example.com"
                      className="w-full bg-sw/10 border border-sw/20 text-sw placeholder-ag rounded-pill px-5 py-3.5 text-body outline-none focus:border-sv-light focus:bg-sw/15 transition-all"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={!url.trim()}
                    className="btn-violet shrink-0"
                  >
                    Analyze URL
                  </button>
                </div>
              </form>

              {/* Verdict legend */}
              <div className="flex items-center gap-6 mt-8 animate-ps-enter-4">
                <span className="flex items-center gap-2 text-caption text-ag">
                  <span className="w-2 h-2 rounded-full bg-verdict-safe inline-block" aria-hidden="true"></span>
                  SAFE
                </span>
                <span className="flex items-center gap-2 text-caption text-ag">
                  <span className="w-2 h-2 rounded-full bg-verdict-warn inline-block" aria-hidden="true"></span>
                  SUSPICIOUS
                </span>
                <span className="flex items-center gap-2 text-caption text-ag">
                  <span className="w-2 h-2 rounded-full bg-verdict-danger inline-block" aria-hidden="true"></span>
                  DANGEROUS
                </span>
              </div>
            </div>

            {/* RIGHT — illustrative analysis panel */}
            <div className="hidden lg:flex items-center justify-center animate-ps-enter-2">
              <div
                className="w-full max-w-sm rounded-card-lg border border-sw/10 bg-sw/5 backdrop-blur-sm"
                style={{ boxShadow: '0px 30px 45px -30px rgba(40,30,93,0.40)' }}
                aria-label="Example analysis result (illustrative)"
              >
                {/* Card header */}
                <div className="px-6 py-5 border-b border-sw/10">
                  <p className="label-caps text-ag/60 mb-1">Example Result</p>
                  <p className="text-body-sm font-medium text-ag truncate">https://paypa1-secure-login.xyz</p>
                </div>

                {/* Verdict */}
                <div className="px-6 py-8 text-center border-b border-sw/10">
                  <p className="label-caps text-ag/60 mb-4">Security Verdict</p>
                  <div className="inline-flex flex-col items-center gap-3">
                    <span className="text-h font-semibold" style={{ color: '#dc2626' }}>DANGEROUS</span>
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-verdict-danger inline-block" aria-hidden="true"></span>
                      <span className="text-caption text-ag">Confidence: VERY HIGH</span>
                    </div>
                  </div>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-2 divide-x divide-sw/10">
                  <div className="px-6 py-5 text-center">
                    <p className="label-caps text-ag/60 mb-2">Hybrid Score</p>
                    <p className="text-h-sm font-semibold text-sw">91</p>
                  </div>
                  <div className="px-6 py-5 text-center">
                    <p className="label-caps text-ag/60 mb-2">ML Confidence</p>
                    <p className="text-h-sm font-semibold text-sw">98.5%</p>
                  </div>
                </div>

                {/* XAI signal */}
                <div className="px-6 py-5 border-t border-sw/10">
                  <p className="label-caps text-ag/60 mb-3">Top Signal</p>
                  <div className="flex items-center gap-2">
                    <span className="w-1 h-1 rounded-full bg-sv-light" aria-hidden="true"></span>
                    <p className="text-caption text-ag">Lookalike brand domain detected</p>
                  </div>
                </div>

                <div className="px-6 py-3 border-t border-sw/10">
                  <p className="text-caption text-ag/40 text-center italic">Illustrative example only</p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* ── Core Capabilities ── */}
      <section className="bg-ms border-b border-ch">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-20">
          <div className="text-center mb-14">
            <h2 className="text-h font-semibold text-si mb-4">
              How PhishScope Protects You
            </h2>
            <p className="text-body-lg text-cg max-w-xl mx-auto">
              A multi-layered detection system. No single technique is reliable alone — we combine all three.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {capabilities.map((cap) => (
              <div key={cap.title} className="surface-card surface-card-hover p-8">
                <p className="label-caps-dark mb-3">{cap.eyebrow}</p>
                <h3 className="text-h-sm font-semibold text-si mb-3">{cap.title}</h3>
                <p className="text-body-sm text-cg leading-relaxed">{cap.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Detection Pipeline — numbered because it IS sequential ── */}
      <section className="bg-sw border-b border-ch">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-20">
          <div className="text-center mb-14">
            <h2 className="text-h font-semibold text-si mb-4">The Detection Pipeline</h2>
            <p className="text-body-lg text-cg max-w-xl mx-auto">
              Every URL passes through six sequential stages before a verdict is reached.
            </p>
          </div>

          {/* Horizontal on desktop */}
          <div className="hidden lg:grid grid-cols-6 gap-0">
            {pipeline.map((step, idx) => (
              <div key={step.num} className="relative flex flex-col items-center text-center px-2">
                {/* Connector line */}
                {idx < pipeline.length - 1 && (
                  <div
                    className="absolute top-5 left-1/2 w-full h-px bg-ch"
                    aria-hidden="true"
                    style={{ left: '50%' }}
                  />
                )}
                {/* Circle */}
                <div className={`relative w-10 h-10 rounded-full flex items-center justify-center text-caption font-semibold mb-4 shrink-0 ${
                  idx === pipeline.length - 1
                    ? 'bg-sv text-sw'
                    : 'bg-ms border border-ch text-cg'
                }`}>
                  {step.num}
                </div>
                <p className="text-body-sm font-medium text-si mb-1">{step.label}</p>
                <p className="text-caption text-ag leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>

          {/* Vertical on mobile */}
          <div className="lg:hidden space-y-6">
            {pipeline.map((step) => (
              <div key={step.num} className="flex gap-5">
                <div className={`w-9 h-9 rounded-full shrink-0 flex items-center justify-center text-caption font-semibold ${
                  step.num === '06' ? 'bg-sv text-sw' : 'bg-ms border border-ch text-cg'
                }`}>
                  {step.num}
                </div>
                <div className="pt-1">
                  <p className="text-body-sm font-medium text-si mb-1">{step.label}</p>
                  <p className="text-caption text-ag leading-relaxed">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA Strip ── */}
      <section className="bg-si">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-16 text-center">
          <h2 className="text-h font-semibold text-sw mb-4">
            Ready to check a URL?
          </h2>
          <p className="text-body-lg text-ag mb-8 max-w-md mx-auto">
            Submit any link to the PhishScope engine and receive a full hybrid analysis.
          </p>
          <a href="/analyzer" className="btn-violet">
            Open Analyzer
          </a>
        </div>
      </section>
    </div>
  );
};

export default Hero;
