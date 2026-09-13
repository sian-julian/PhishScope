/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // NEVERHACK-inspired PhishScope design tokens
        'si':        '#0a0f1f',   // Sovereign Ink — primary text/dark surfaces
        'si-700':    '#1a2340',   // Sovereign Ink lighter
        'sw':        '#ffffff',   // Signal White — cards/surfaces
        'ms':        '#f6f7fc',   // Mist Surface — page background
        'ch':        '#e5e7eb',   // Cool Hairline — borders/dividers
        'sd':        '#d8d7e2',   // Shadow Lichen
        'cg':        '#4e4e4e',   // Carbon Gray — secondary text
        'ag':        '#999999',   // Ash Gray — muted text
        'sv':        '#6b2bea',   // Sovereign Violet — AI/brand accent
        'sv-light':  '#afa9fd',   // Violet Wash
        'cc':        '#28d3fe',   // Cyber Cyan — very limited
        'ib':        '#2563eb',   // Info Blue — links/informational
        'ib-hover':  '#1d4ed8',   // Info Blue hover
        // Verdict semantics — strict usage
        'verdict-safe':    '#16a34a',
        'verdict-warn':    '#d97706',
        'verdict-danger':  '#dc2626',
        'verdict-safe-bg': '#f0fdf4',
        'verdict-warn-bg': '#fffbeb',
        'verdict-danger-bg': '#fef2f2',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      fontSize: {
        'caption':  ['11px', { lineHeight: '1.4' }],
        'body-sm':  ['14px', { lineHeight: '1.5' }],
        'body':     ['16px', { lineHeight: '1.6' }],
        'body-lg':  ['18px', { lineHeight: '1.6' }],
        'sub':      ['22px', { lineHeight: '1.3' }],
        'h-sm':     ['24px', { lineHeight: '1.25', letterSpacing: '-0.01em' }],
        'h':        ['32px', { lineHeight: '1.2',  letterSpacing: '-0.02em' }],
        'h-lg':     ['40px', { lineHeight: '1.15', letterSpacing: '-0.025em' }],
        'display':  ['52px', { lineHeight: '1.1',  letterSpacing: '-0.03em' }],
        'display-xl': ['72px', { lineHeight: '1.0', letterSpacing: '-0.04em' }],
      },
      borderRadius: {
        'card':  '14px',
        'card-lg': '18px',
        'card-sm': '10px',
        'pill':  '9999px',
      },
      boxShadow: {
        'card':  '0px 4px 12px -4px rgba(40,30,93,0.06), 0 1px 3px rgba(0,0,0,0.04)',
        'card-hover': '0px 8px 24px -8px rgba(40,30,93,0.12), 0 2px 6px rgba(0,0,0,0.06)',
        'hero':  '0px 30px 45px -30px rgba(40,30,93,0.20)',
        'none':  'none',
      },
      spacing: {
        '18': '72px',
        '22': '88px',
      },
      maxWidth: {
        'content': '1200px',
      },
    },
  },
  plugins: [],
}
