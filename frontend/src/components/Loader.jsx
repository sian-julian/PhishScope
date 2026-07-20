import { FiLoader } from 'react-icons/fi';

const Loader = ({ text = "Analyzing URL..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12">
      <FiLoader className="w-12 h-12 text-primary animate-spin mb-4" />
      <p className="text-gray-300 font-medium animate-pulse">{text}</p>
    </div>
  );
};

export default Loader;
