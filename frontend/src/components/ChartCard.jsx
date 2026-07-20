const ChartCard = ({ title, children }) => {
  return (
    <div className="glass p-6 rounded-2xl w-full flex flex-col items-center">
      <h3 className="text-xl font-bold text-white/90 mb-6 w-full text-left">{title}</h3>
      <div className="w-full h-72 flex justify-center">
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
