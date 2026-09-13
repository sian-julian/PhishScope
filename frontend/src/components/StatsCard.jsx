const StatsCard = ({ title, value, colorClass }) => (
  <div className="surface-card p-6">
    <p className="label-caps mb-3">{title}</p>
    <p className={`text-h font-semibold ${colorClass || 'text-si'}`}>{value}</p>
  </div>
);

export default StatsCard;
