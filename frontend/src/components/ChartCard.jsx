const ChartCard = ({ title, children }) => (
  <div className="surface-card p-6">
    <h3 className="text-h-sm font-semibold text-si mb-6">{title}</h3>
    <div className="w-full">{children}</div>
  </div>
);

export default ChartCard;
