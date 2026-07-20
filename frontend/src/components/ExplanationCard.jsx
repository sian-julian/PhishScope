import { FiInfo } from 'react-icons/fi';
import FeatureCard from './FeatureCard';

const ExplanationCard = ({ explanation }) => {
  if (!explanation) return null;

  return (
    <div className="glass p-6 rounded-2xl mt-6">
      <div className="flex items-center gap-3 mb-4">
        <FiInfo className="w-6 h-6 text-primary" />
        <h3 className="text-xl font-bold text-white/90">AI Explanation</h3>
      </div>
      
      <p className="text-lg text-gray-300 mb-6 bg-white/5 p-4 rounded-xl border border-white/10">
        {explanation.summary}
      </p>

      {explanation.top_features && explanation.top_features.length > 0 && (
        <div>
          <h4 className="text-sm text-gray-400 uppercase tracking-wider mb-3">Top Impacting Features</h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
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
