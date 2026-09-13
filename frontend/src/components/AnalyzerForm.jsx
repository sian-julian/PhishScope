const AnalyzerForm = ({ onAnalyze, isLoading }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    const input = e.target.elements['analyzer-url'];
    if (input.value.trim()) {
      onAnalyze(input.value.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full" aria-label="URL analysis form">
      <label htmlFor="analyzer-url" className="block label-caps-dark mb-3">
        URL to Analyze
      </label>
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <input
            id="analyzer-url"
            name="analyzer-url"
            type="url"
            required
            disabled={isLoading}
            placeholder="https://example.com/path?query=value"
            defaultValue=""
            autoComplete="url"
            className="w-full bg-sw border border-ch text-si placeholder-ag rounded-pill px-5 py-4 text-body outline-none transition-all disabled:opacity-50"
            style={{ '--tw-ring-color': '#6b2bea' }}
            onFocus={(e) => {
              e.target.style.borderColor = '#6b2bea';
              e.target.style.boxShadow = '0 0 0 3px rgba(107,43,234,0.12)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = '#e5e7eb';
              e.target.style.boxShadow = 'none';
            }}
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary shrink-0 py-4 px-8 text-body"
        >
          {isLoading ? 'Analyzing...' : 'Analyze URL'}
        </button>
      </div>
      <p className="text-caption text-ag mt-3">
        Submit any URL — PhishScope will analyze it using the full hybrid engine.
      </p>
    </form>
  );
};

export default AnalyzerForm;
