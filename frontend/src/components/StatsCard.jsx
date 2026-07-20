const StatsCard = ({ title, value, colorClass }) => {
  return (
    <div className={`glass p-6 rounded-2xl border-l-4 ${colorClass}`}>
      <p className="text-gray-400 text-sm uppercase tracking-wider mb-2">{title}</p>
      <p className="text-4xl font-bold text-white">{value}</p>
    </div>
  );
};

export default StatsCard;
