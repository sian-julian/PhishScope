import VerdictBadge from './VerdictBadge';

const verdictBorderColor = {
  SAFE:      '#16a34a',
  SUSPICIOUS:'#d97706',
  DANGEROUS: '#dc2626',
};

const ResultCard = ({ result }) => {
  const { heuristic, ml, hybrid } = result;
  const verdict = hybrid?.verdict || 'UNKNOWN';
  const borderColor = verdictBorderColor[verdict] || '#e5e7eb';

  return (
    <div
      className="bg-sw rounded-card overflow-hidden border border-ch"
      style={{
        boxShadow: '0px 4px 12px -4px rgba(40,30,93,0.08)',
        borderLeft: `4px solid ${borderColor}`,
      }}
    >
      {/* Verdict — the most prominent element, full-width banner */}
      <div className="flex flex-col items-center py-10 px-6 border-b border-ch bg-ms/40">
        <p className="label-caps mb-5">Security Verdict</p>
        <VerdictBadge verdict={verdict} size="large" />
      </div>

      {/* Metrics row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-ch">
        <div className="px-6 py-6 text-center">
          <p className="label-caps mb-2">Hybrid Score</p>
          <p className="text-h font-semibold text-si">{hybrid?.score ?? '—'}</p>
          <p className="text-caption text-ag mt-1">out of 100</p>
        </div>
        <div className="px-6 py-6 text-center">
          <p className="label-caps mb-2">Confidence Level</p>
          <p className="text-h font-semibold text-si">{hybrid?.confidence ?? '—'}</p>
        </div>
        <div className="px-6 py-6 text-center">
          <p className="label-caps mb-2">ML Confidence</p>
          <p className="text-h font-semibold text-si">
            {ml?.confidence != null ? `${(ml.confidence * 100).toFixed(1)}%` : '—'}
          </p>
        </div>
      </div>

      {/* ML verdict row */}
      {ml?.prediction && (
        <div className="px-6 py-4 border-t border-ch flex items-center justify-between gap-4 flex-wrap">
          <p className="label-caps">ML Model Prediction</p>
          <span className="text-body-sm font-medium text-si">{ml.prediction}</span>
        </div>
      )}

      {/* Heuristic score row */}
      {heuristic?.score != null && (
        <div className="px-6 py-4 border-t border-ch flex items-center justify-between gap-4 flex-wrap">
          <p className="label-caps">Heuristic Score</p>
          <span className="text-body-sm font-medium text-si">{heuristic.score}</span>
        </div>
      )}

      {/* Analysis Reasons — shown as security findings */}
      {hybrid?.reasons && hybrid.reasons.length > 0 && (
        <div className="border-t border-ch px-6 py-6">
          <p className="label-caps mb-4">Detection Signals</p>
          <ul className="space-y-3" role="list">
            {hybrid.reasons.map((reason, idx) => (
              <li
                key={idx}
                className="flex gap-3 items-start text-body-sm text-cg leading-relaxed"
              >
                <span
                  className="mt-1.5 w-1.5 h-1.5 rounded-full shrink-0"
                  style={{ background: borderColor }}
                  aria-hidden="true"
                />
                {reason}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResultCard;
