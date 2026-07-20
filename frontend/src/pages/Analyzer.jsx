import { useState } from 'react';
import AnalyzerForm from '../components/AnalyzerForm';
import Loader from '../components/Loader';
import ResultCard from '../components/ResultCard';
import ExplanationCard from '../components/ExplanationCard';
import { analyzeURL } from '../services/api';

const Analyzer = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [analyzedUrl, setAnalyzedUrl] = useState('');

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setError('');
    setResult(null);
    setAnalyzedUrl(url);

    try {
      const data = await analyzeURL(url);
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto py-8">
      <div className="w-full text-center mb-10">
        <h1 className="text-4xl font-bold mb-4">URL Analyzer</h1>
        <p className="text-gray-400">Enter a URL below to run our hybrid heuristic and AI detection engine.</p>
      </div>

      <AnalyzerForm onAnalyze={handleAnalyze} isLoading={isLoading} />

      <div className="w-full mt-12">
        {isLoading && <Loader />}
        
        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-6 rounded-xl text-center font-medium">
            {error}
          </div>
        )}

        {result && !isLoading && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="bg-white/5 p-4 rounded-xl border border-white/10 text-center break-all">
              <span className="text-gray-400 uppercase tracking-wider text-xs block mb-1">Analyzed URL</span>
              <span className="text-lg font-mono text-white">{analyzedUrl}</span>
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
