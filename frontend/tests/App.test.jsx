import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, vi, afterEach } from 'vitest';
import App from '../src/App';
import AnalyzerForm from '../src/components/AnalyzerForm';
import ResultCard from '../src/components/ResultCard';
import ExplanationCard from '../src/components/ExplanationCard';
import VerdictBadge from '../src/components/VerdictBadge';

// Mock API — preserves real integration by preventing actual network calls in tests
vi.mock('../src/services/api', () => ({
  analyzeURL: vi.fn(),
}));

afterEach(() => {
  cleanup();
});

// ── Routing ──────────────────────────────────────────────────
describe('Routing Tests', () => {
  it('renders Navbar on all pages', () => {
    render(<MemoryRouter><App /></MemoryRouter>);
    expect(screen.getAllByText(/PhishScope/i).length).toBeGreaterThan(0);
  });

  it('renders Home page hero heading', () => {
    render(<MemoryRouter initialEntries={['/']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/Know what.*s behind every URL/i).length).toBeGreaterThan(0);
  });

  it('renders Analyzer page', () => {
    render(<MemoryRouter initialEntries={['/analyzer']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/Analyze any URL/i).length).toBeGreaterThan(0);
  });

  it('renders Dashboard page with empty state', () => {
    render(<MemoryRouter initialEntries={['/dashboard']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/No analysis in this session yet/i).length).toBeGreaterThan(0);
  });

  it('renders About page', () => {
    render(<MemoryRouter initialEntries={['/about']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/What is PhishScope/i).length).toBeGreaterThan(0);
  });

  it('renders Documentation page', () => {
    render(<MemoryRouter initialEntries={['/docs']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/How PhishScope Works/i).length).toBeGreaterThan(0);
  });

  it('renders 404 for unknown route', () => {
    render(<MemoryRouter initialEntries={['/unknown-route']}><App /></MemoryRouter>);
    expect(screen.getAllByText(/Page not found/i).length).toBeGreaterThan(0);
  });
});

// ── AnalyzerForm ──────────────────────────────────────────────
describe('AnalyzerForm Tests', () => {
  it('renders URL input and Analyze button', () => {
    render(<AnalyzerForm onAnalyze={vi.fn()} isLoading={false} />);
    expect(screen.getByLabelText(/URL to Analyze/i)).toBeDefined();
    const buttons = screen.getAllByRole('button');
    const analyzeBtn = buttons.find(b => b.textContent.includes('Analyze URL'));
    expect(analyzeBtn).toBeDefined();
  });

  it('shows loading state on button', () => {
    render(<AnalyzerForm onAnalyze={vi.fn()} isLoading={true} />);
    const buttons = screen.getAllByRole('button');
    const loadingBtn = buttons.find(b => b.textContent.includes('Analyzing...'));
    expect(loadingBtn).toBeDefined();
    expect(loadingBtn.disabled).toBe(true);
  });

  it('calls onAnalyze on submit', () => {
    const mockOnAnalyze = vi.fn();
    render(<AnalyzerForm onAnalyze={mockOnAnalyze} isLoading={false} />);
    const input = screen.getByLabelText(/URL to Analyze/i);
    fireEvent.change(input, { target: { value: 'https://test.example.com' } });
    const form = input.closest('form');
    fireEvent.submit(form);
    expect(mockOnAnalyze).toHaveBeenCalledWith('https://test.example.com');
  });
});

// ── ResultCard ────────────────────────────────────────────────
describe('ResultCard Tests', () => {
  it('renders DANGEROUS verdict prominently', () => {
    const result = {
      hybrid: { verdict: 'DANGEROUS', score: 91, confidence: 'VERY_HIGH', reasons: ['Lookalike domain'] },
      ml:     { prediction: 'PHISHING', confidence: 0.985 },
      heuristic: { score: 80, verdict: 'DANGEROUS' },
    };
    render(<ResultCard result={result} />);
    expect(screen.getAllByText(/DANGEROUS/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/91/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/98.5%/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Lookalike domain/i).length).toBeGreaterThan(0);
  });

  it('renders SAFE verdict', () => {
    const result = {
      hybrid: { verdict: 'SAFE', score: 10, confidence: 'HIGH', reasons: [] },
      ml:     { prediction: 'SAFE', confidence: 0.05 },
      heuristic: { score: 10, verdict: 'SAFE' },
    };
    render(<ResultCard result={result} />);
    expect(screen.getAllByText(/SAFE/i).length).toBeGreaterThan(0);
  });
});

// ── ExplanationCard ───────────────────────────────────────────
describe('ExplanationCard Tests', () => {
  it('renders summary and top features', () => {
    const explanation = {
      summary: 'This URL contains phishing indicators.',
      top_features: [
        { feature: 'domain_entropy', impact: '+0.42' },
        { feature: 'url_length',     impact: '-0.15' },
      ],
    };
    render(<ExplanationCard explanation={explanation} />);
    expect(screen.getAllByText(/This URL contains phishing indicators/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/domain_entropy/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/\+0\.42/i).length).toBeGreaterThan(0);
  });

  it('returns null when no explanation', () => {
    const { container } = render(<ExplanationCard explanation={null} />);
    expect(container.firstChild).toBeNull();
  });
});

// ── VerdictBadge ──────────────────────────────────────────────
describe('VerdictBadge Tests', () => {
  it('renders SAFE badge with text', () => {
    render(<VerdictBadge verdict="SAFE" />);
    expect(screen.getAllByText(/SAFE/i).length).toBeGreaterThan(0);
  });

  it('renders SUSPICIOUS badge', () => {
    render(<VerdictBadge verdict="SUSPICIOUS" />);
    expect(screen.getAllByText(/SUSPICIOUS/i).length).toBeGreaterThan(0);
  });

  it('renders DANGEROUS badge in large size', () => {
    render(<VerdictBadge verdict="DANGEROUS" size="large" />);
    expect(screen.getAllByText(/DANGEROUS/i).length).toBeGreaterThan(0);
  });
});
