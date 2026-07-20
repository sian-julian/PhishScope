import VerdictBadge from './VerdictBadge';

const ResultCard = ({ result }) => {
  const { heuristic, ml, hybrid } = result;

  return (
    <div className="glass p-6 rounded-2xl flex flex-col items-center text-center">
      <h2 className="text-2xl font-bold mb-6 text-white/90">Analysis Results</h2>
      
      <div className="mb-8">
        <p className="text-sm text-gray-400 uppercase tracking-wider mb-2">Final Verdict</p>
        <VerdictBadge verdict={hybrid?.verdict || "UNKNOWN"} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-4">
        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-gray-400 uppercase tracking-wider mb-1">Hybrid Score</p>
          <p className="text-3xl font-bold text-white">{hybrid?.score ?? "N/A"}</p>
        </div>
        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-gray-400 uppercase tracking-wider mb-1">Confidence</p>
          <p className="text-3xl font-bold text-white">{hybrid?.confidence ?? "N/A"}</p>
        </div>
        <div className="p-4 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-gray-400 uppercase tracking-wider mb-1">ML Probability</p>
          <p className="text-3xl font-bold text-white">{ml?.probability ? `${(ml.probability * 100).toFixed(1)}%` : "N/A"}</p>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
