const Documentation = () => {
  return (
    <div className="w-full max-w-4xl mx-auto py-8 text-gray-300">
      <h1 className="text-4xl font-bold text-white mb-8">Documentation</h1>
      
      <div className="space-y-6">
        <div className="glass p-8 rounded-2xl">
          <h2 className="text-2xl font-bold text-white mb-4">Phase 1-7 Summary</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li><strong>Phase 1:</strong> Feature Extraction (Entropy, Lookalike, Punycode).</li>
            <li><strong>Phase 2:</strong> Heuristic Engine (Basic static rules).</li>
            <li><strong>Phase 3:</strong> Flask API (`POST /analyze`).</li>
            <li><strong>Phase 4:</strong> Dataset Prep (99,996 URLs).</li>
            <li><strong>Phase 5:</strong> ML Training (98.3% Accuracy).</li>
            <li><strong>Phase 6:</strong> Hybrid Consensus Engine.</li>
            <li><strong>Phase 7:</strong> SHAP Integration (XAI).</li>
          </ul>
        </div>

        <div className="glass p-8 rounded-2xl">
          <h2 className="text-2xl font-bold text-white mb-4">API Documentation</h2>
          <pre className="bg-black/50 p-4 rounded-lg overflow-x-auto">
            <code>
{`POST /analyze
Content-Type: application/json

{
  "url": "https://g00gle.xyz"
}

Response (200 OK):
{
  "hybrid": { "verdict": "DANGEROUS", ... },
  "explanation": { "summary": "...", "top_features": [...] }
}`}
            </code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default Documentation;
