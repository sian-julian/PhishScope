import { FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

const FeatureCard = ({ feature, impact }) => {
  const isPositive = impact.startsWith('+');
  
  return (
    <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors cursor-default">
      <span className="text-gray-200 text-sm font-medium">{feature}</span>
      <div className={`flex items-center gap-1 text-sm font-bold ${isPositive ? 'text-red-400' : 'text-accent'}`}>
        {isPositive ? <FiTrendingUp /> : <FiTrendingDown />}
        <span>{impact}</span>
      </div>
    </div>
  );
};

export default FeatureCard;
