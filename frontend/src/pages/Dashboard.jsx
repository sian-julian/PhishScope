import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ResultCard from '../components/ResultCard';
import ExplanationCard from '../components/ExplanationCard';
import VerdictBadge from '../components/VerdictBadge';

/* ============================================================
   Dashboard — all existing sessionStorage logic preserved.
   Only visual presentation changed.
   ============================================================ */
const Dashboard = () => {
  const [latestAnalysis, setLatestAnalysis] = useState(null);

  useEffect(() => {
    const stored = sessionStorage.getItem('latestAnalysis');
    if (stored) {
      try {
        setLatestAnalysis(JSON.parse(stored));
      } catch (e) {
        console.error('Failed to parse stored analysis', e);
      }
    }
  }, []);

  return (
    <div className="w-full min-h-screen bg-ms">

      {/* Page header */}
      <div className="bg-si border-b border-si-700">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-14">
          <p className="label-caps text-sv-light mb-4">Session Dashboard</p>
          <h1 className="text-h-lg font-semibold text-sw mb-4">
            Analysis Results
          </h1>
          <p className="text-body-lg text-ag max-w-xl">
            PhishScope shows the most recent analysis from your current session. Historical data is not persisted.
          </p>
        </div>
      </div>

      <div className="max-w-content mx-auto px-5 lg:px-8 py-12">

        {/* Empty state */}
        {!latestAnalysis ? (
          <div className="surface-card py-20 flex flex-col items-center text-center">
            <div
              className="w-16 h-16 rounded-card-lg flex items-center justify-center mb-6"
              style={{ background: '#f6f7fc' }}
              aria-hidden="true"
            >
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#999999" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </div>
            <h2 className="text-h-sm font-semibold text-si mb-3">No analysis in this session yet</h2>
            <p className="text-body text-cg max-w-md mb-8">
              Run an analysis in the Analyzer and your results will appear here. Results are kept in your browser session only.
            </p>
            <Link to="/analyzer" className="btn-primary">
              Go to Analyzer
            </Link>
          </div>
        ) : (
          <div className="space-y-6 animate-ps-enter">

            {/* Session banner */}
            <div className="surface-card px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center gap-4 flex-wrap">
                <div>
                  <p className="label-caps mb-1">Analyzed URL</p>
                  <p className="text-body font-mono text-si break-all">{latestAnalysis.url}</p>
                </div>
                {latestAnalysis.data?.hybrid?.verdict && (
                  <VerdictBadge verdict={latestAnalysis.data.hybrid.verdict} size="default" />
                )}
              </div>
              <Link to="/analyzer" className="btn-secondary text-body-sm shrink-0">
                New Analysis
              </Link>
            </div>

            <ResultCard result={latestAnalysis.data} />

            {latestAnalysis.data.explanation && !latestAnalysis.data.explanation.error && (
              <ExplanationCard explanation={latestAnalysis.data.explanation} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
