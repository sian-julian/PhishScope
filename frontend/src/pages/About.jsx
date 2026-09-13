const About = () => (
  <div className="w-full min-h-screen bg-ms">

    {/* Header */}
    <div className="bg-si border-b border-si-700">
      <div className="max-w-content mx-auto px-5 lg:px-8 py-14">
        <p className="label-caps text-sv-light mb-4">About</p>
        <h1 className="text-h-lg font-semibold text-sw mb-4">
          What is PhishScope?
        </h1>
        <p className="text-body-lg text-ag max-w-xl">
          An AI-powered phishing detection platform built as an academic research project.
        </p>
      </div>
    </div>

    <div className="max-w-content mx-auto px-5 lg:px-8 py-12 space-y-8">

      {/* Overview */}
      <div className="surface-card p-8">
        <h2 className="text-h-sm font-semibold text-si mb-5">The Problem</h2>
        <p className="text-body text-cg leading-relaxed mb-4">
          Phishing attacks are responsible for a significant proportion of data breaches and identity theft globally. Attackers craft malicious URLs that closely mimic legitimate sites — often bypassing traditional blocklists within hours of creation.
        </p>
        <p className="text-body text-cg leading-relaxed">
          Basic rule-based detection fails against novel, polymorphic phishing campaigns. Machine learning alone can generate false positives on legitimate sites with unusual structures. PhishScope addresses this with a hybrid approach.
        </p>
      </div>

      {/* Architecture */}
      <div className="surface-card p-8">
        <h2 className="text-h-sm font-semibold text-si mb-5">The Approach</h2>
        <p className="text-body text-cg leading-relaxed mb-6">
          PhishScope layers three detection mechanisms through a consensus engine, so the weaknesses of any single approach are balanced by the others.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {[
            {
              label: 'Machine Learning',
              desc: 'A Random Forest classifier trained on 100,000+ labeled URLs identifies statistical phishing patterns across 20+ URL features.',
            },
            {
              label: 'Heuristic Analysis',
              desc: 'A rule-based engine evaluates structural URL properties: domain entropy, TLD reputation, lookalike patterns, and known abuse signatures.',
            },
            {
              label: 'Hybrid Decision',
              desc: 'A consensus engine weighs both signals. When ML and heuristics agree, confidence is high. Disagreement triggers a SUSPICIOUS verdict for human review.',
            },
          ].map((item) => (
            <div key={item.label} className="rounded-card-sm border border-ch p-5">
              <p className="label-caps-dark mb-3">{item.label}</p>
              <p className="text-body-sm text-cg leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Explainability */}
      <div className="surface-card p-8">
        <h2 className="text-h-sm font-semibold text-si mb-4">Explainable AI</h2>
        <p className="text-body text-cg leading-relaxed mb-4">
          Every PhishScope verdict includes a SHAP-based explanation — showing which specific URL features drove the decision and by how much. This makes results auditable and meaningful, not just a black-box score.
        </p>
        <p className="text-body text-cg leading-relaxed">
          Security teams and researchers can inspect the feature impact breakdown to understand exactly what PhishScope detected and why — supporting informed decision-making rather than blind trust.
        </p>
      </div>

      {/* Tech stack */}
      <div className="surface-card p-8">
        <h2 className="text-h-sm font-semibold text-si mb-5">Technology Stack</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-8 text-body-sm text-cg">
          {[
            ['Frontend', 'React 19, Vite, Tailwind CSS'],
            ['Backend',  'Python, Flask'],
            ['ML Model', 'Scikit-Learn (Random Forest), Joblib'],
            ['XAI',      'SHAP (SHapley Additive exPlanations)'],
            ['Extension','Chrome Manifest V3'],
            ['Dataset',  '~100,000 labeled URLs'],
          ].map(([k, v]) => (
            <div key={k} className="flex gap-3">
              <span className="font-medium text-si shrink-0 w-24">{k}</span>
              <span className="text-cg">{v}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  </div>
);

export default About;
