import { useState } from 'react';
import { FiSearch } from 'react-icons/fi';

const AnalyzerForm = ({ onAnalyze, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onAnalyze(url.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative flex items-center bg-secondary rounded-full border border-gray-700 p-2 shadow-2xl">
          <div className="pl-4">
            <FiSearch className="text-gray-400 w-6 h-6" />
          </div>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://g00gle.xyz"
            required
            disabled={isLoading}
            className="w-full bg-transparent text-white px-4 py-3 outline-none placeholder-gray-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="bg-primary hover:bg-blue-500 text-white px-8 py-3 rounded-full font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>
    </form>
  );
};

export default AnalyzerForm;
