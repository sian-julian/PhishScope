import FeatureCard from './FeatureCard';

const ExplanationCard = ({ explanation }) => {
  if (!explanation) return null;

  return (
    <div className="surface-card p-8">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div
          className="w-8 h-8 rounded-card-sm flex items-center justify-center shrink-0"
          style={{ background: 'rgba(107,43,234,0.1)' }}
          aria-hidden="true"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b2bea" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </div>
        <h3 className="text-h-sm font-semibold text-si">Security Intelligence Report</h3>
      </div>

      {/* Summary — in a distinct inset block */}
      {explanation.summary && (
        <div
          className="rounded-card-sm px-5 py-4 mb-8 text-body text-cg leading-relaxed border-l-4"
          style={{ background: '#f6f7fc', borderLeftColor: '#6b2bea' }}
        >
          {explanation.summary}
        </div>
      )}

      {/* Top Features — sorted by impact */}
      {explanation.top_features && explanation.top_features.length > 0 && (
        <div>
          <p className="label-caps mb-5">Top Impacting Features</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {explanation.top_features.map((feat, idx) => (
              <FeatureCard key={idx} feature={feat.feature} impact={feat.impact} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ExplanationCard;
