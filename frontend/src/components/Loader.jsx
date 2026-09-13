const Loader = ({ text = 'Analyzing URL...' }) => (
  <div className="flex flex-col items-center justify-center py-16 px-8" role="status" aria-live="polite" aria-label={text}>
    {/* Scan-ring spinner */}
    <div className="relative w-16 h-16 mb-8">
      {/* Outer ring */}
      <div
        className="absolute inset-0 rounded-full border-2 border-ch"
        aria-hidden="true"
      />
      {/* Spinning segment */}
      <div
        className="absolute inset-0 rounded-full border-2 border-transparent animate-ps-spin"
        style={{ borderTopColor: '#6b2bea' }}
        aria-hidden="true"
      />
      {/* Inner dot */}
      <div
        className="absolute inset-0 flex items-center justify-center"
        aria-hidden="true"
      >
        <div className="w-2 h-2 rounded-full bg-sv" />
      </div>
    </div>

    <p className="text-body font-medium text-si mb-2">{text}</p>
    <p className="text-body-sm text-ag text-center max-w-xs">
      Running the hybrid analysis engine. This typically takes under a second.
    </p>
  </div>
);

export default Loader;
