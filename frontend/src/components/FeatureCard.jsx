const FeatureCard = ({ feature, impact }) => {
  const isPositive = impact && impact.toString().startsWith('+');
  const impactColor = isPositive ? '#dc2626' : '#16a34a';
  const impactBg   = isPositive ? '#fef2f2' : '#f0fdf4';

  return (
    <div className="surface-card p-4 surface-card-hover">
      <p className="text-body-sm font-medium text-si mb-3 leading-snug">{feature}</p>
      <div
        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-card-sm text-caption font-semibold"
        style={{ background: impactBg, color: impactColor }}
        aria-label={`Impact: ${impact}`}
      >
        {isPositive ? (
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" aria-hidden="true">
            <polyline points="18 15 12 9 6 15" />
          </svg>
        ) : (
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" aria-hidden="true">
            <polyline points="6 9 12 15 18 9" />
          </svg>
        )}
        {impact}
      </div>
    </div>
  );
};

export default FeatureCard;
