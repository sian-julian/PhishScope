import { FiCheckCircle, FiAlertTriangle, FiXCircle } from 'react-icons/fi';

const VerdictBadge = ({ verdict }) => {
  let colorClass = "bg-gray-500 text-white";
  let Icon = FiCheckCircle;

  if (verdict === "SAFE") {
    colorClass = "bg-accent/20 text-accent border-accent/50";
    Icon = FiCheckCircle;
  } else if (verdict === "SUSPICIOUS") {
    colorClass = "bg-yellow-500/20 text-yellow-400 border-yellow-500/50";
    Icon = FiAlertTriangle;
  } else if (verdict === "DANGEROUS") {
    colorClass = "bg-red-500/20 text-red-400 border-red-500/50";
    Icon = FiXCircle;
  }

  return (
    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${colorClass} font-bold tracking-wide`}>
      <Icon className="w-5 h-5" />
      <span>{verdict}</span>
    </div>
  );
};

export default VerdictBadge;
