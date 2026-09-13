const VerdictBadge = ({ verdict, size = 'default' }) => {
  const configs = {
    SAFE: {
      label: 'SAFE',
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <polyline points="20 6 9 17 4 12" />
        </svg>
      ),
      color: '#16a34a',
      bg: '#f0fdf4',
      border: '#bbf7d0',
      animClass: 'animate-verdict-safe',
    },
    SUSPICIOUS: {
      label: 'SUSPICIOUS',
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
      ),
      color: '#d97706',
      bg: '#fffbeb',
      border: '#fde68a',
      animClass: 'animate-verdict-warn',
    },
    DANGEROUS: {
      label: 'DANGEROUS',
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
      ),
      color: '#dc2626',
      bg: '#fef2f2',
      border: '#fecaca',
      animClass: 'animate-verdict-danger',
    },
  };

  const config = configs[verdict] || {
    label: verdict || 'UNKNOWN',
    icon: null,
    color: '#999999',
    bg: '#f6f7fc',
    border: '#e5e7eb',
    animClass: '',
  };

  if (size === 'large') {
    return (
      <div
        className={`flex flex-col items-center gap-4 py-8 px-10 rounded-card ${config.animClass}`}
        style={{ background: config.bg, border: `2px solid ${config.border}` }}
        role="status"
        aria-label={`Verdict: ${config.label}`}
      >
        <span style={{ color: config.color }}>{config.icon && <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{
          verdict === 'SAFE' ? <polyline points="20 6 9 17 4 12" /> :
          verdict === 'SUSPICIOUS' ? <><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></> :
          verdict === 'DANGEROUS' ? <><circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" /></> :
          null
        }</svg>}</span>
        <span
          className="font-semibold tracking-wide"
          style={{ color: config.color, fontSize: '28px', letterSpacing: '0.04em' }}
        >
          {config.label}
        </span>
      </div>
    );
  }

  // Default (inline) size
  return (
    <span
      className="inline-flex items-center gap-2 px-3 py-1.5 rounded-pill text-body-sm font-medium"
      style={{ background: config.bg, color: config.color, border: `1px solid ${config.border}` }}
      aria-label={`Verdict: ${config.label}`}
    >
      <span style={{ color: config.color }} className="shrink-0">{config.icon}</span>
      {config.label}
    </span>
  );
};

export default VerdictBadge;
