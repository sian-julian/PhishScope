import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import AnalyzerForm from '../components/AnalyzerForm';
import Loader from '../components/Loader';
import ResultCard from '../components/ResultCard';
import ExplanationCard from '../components/ExplanationCard';
import { analyzeURL } from '../services/api';

/* ============================================================
   Analyzer — all existing logic preserved exactly.
   Only visual presentation changed.
   ============================================================ */
const Analyzer = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result,    setResult]    = useState(null);
  const [error,     setError]     = useState('');
  const [analyzedUrl, setAnalyzedUrl] = useState('');

  const location = useLocation();
  const resultRef = useRef(null);

  useEffect(() => {
    const params   = new URLSearchParams(location.search);
    const urlParam = params.get('url');
    if (urlParam) {
      handleAnalyze(urlParam);
    }
  }, [location]);

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setError('');
    setResult(null);
    setAnalyzedUrl(url);

    try {
      const data = await analyzeURL(url);
      setResult(data);
      sessionStorage.setItem('latestAnalysis', JSON.stringify({ url, data }));
    } catch (err) {
      setError(err.message || 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full min-h-screen bg-ms">

      {/* Page header */}
      <div className="bg-si border-b border-si-700">
        <div className="max-w-content mx-auto px-5 lg:px-8 py-14">
          <p className="label-caps text-sv-light mb-4">URL Analysis Console</p>
          <h1 className="text-h-lg font-semibold text-sw mb-4">
            Analyze any URL
          </h1>
          <p className="text-body-lg text-ag max-w-xl">
            Submit a URL to run PhishScope's full hybrid analysis — ML model, heuristic engine, and consensus decision.
          </p>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-content mx-auto px-5 lg:px-8 py-12">

        {/* Form */}
        <div className="surface-card p-8 mb-10">
          <AnalyzerForm onAnalyze={handleAnalyze} isLoading={isLoading} />
        </div>

        {/* States */}
        {isLoading && (
          <div className="surface-card">
            <Loader />
          </div>
        )}

        {error && (
          <div
            className="rounded-card border p-6 flex items-start gap-4"
            style={{ background: '#fef2f2', borderColor: '#fecaca' }}
            role="alert"
            aria-live="assertive"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0 mt-0.5" aria-hidden="true">
              <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <div>
              <p className="text-body font-medium" style={{ color: '#991b1b' }}>Analysis Error</p>
              <p className="text-body-sm mt-1" style={{ color: '#b91c1c' }}>{error}</p>
            </div>
          </div>
        )}

        {result && !isLoading && (
          <div className="space-y-6 animate-ps-enter" ref={resultRef}>
            {/* Analyzed URL strip */}
            <div className="surface-card px-6 py-4 flex items-center justify-between gap-4 flex-wrap">
              <div>
                <p className="label-caps mb-1">Analyzed URL</p>
                <p className="text-body font-mono text-si break-all">{analyzedUrl}</p>
              </div>
              <button
                onClick={() => { setResult(null); setError(''); setAnalyzedUrl(''); }}
                className="btn-secondary text-body-sm shrink-0"
              >
                Clear
              </button>
            </div>

            <ResultCard result={result} />

            {result.explanation && !result.explanation.error && (
              <ExplanationCard explanation={result.explanation} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Analyzer;
