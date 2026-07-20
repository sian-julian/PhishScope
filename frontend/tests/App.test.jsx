import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';
import App from '../src/App';
import AnalyzerForm from '../src/components/AnalyzerForm';
import * as api from '../src/services/api';
import ResultCard from '../src/components/ResultCard';
import ExplanationCard from '../src/components/ExplanationCard';
import VerdictBadge from '../src/components/VerdictBadge';

// Mock API
vi.mock('../src/services/api', () => ({
  analyzeURL: vi.fn(),
}));

describe('Frontend Rendering and Routing Tests', () => {
  it('renders Navbar correctly', () => {
    render(<MemoryRouter><App /></MemoryRouter>);
    expect(screen.getByText(/PhishScope/i)).toBeDefined();
    expect(screen.getByText(/Home/i)).toBeDefined();
    expect(screen.getByText(/Analyzer/i)).toBeDefined();
  });

  it('renders Hero on Home page', () => {
    render(<MemoryRouter initialEntries={['/']}><App /></MemoryRouter>);
    expect(screen.getByText(/AI-Powered Hybrid Phishing Detection/i)).toBeDefined();
  });

  it('renders Dashboard page', () => {
    render(<MemoryRouter initialEntries={['/dashboard']}><App /></MemoryRouter>);
    expect(screen.getByText(/Global Dashboard/i)).toBeDefined();
    expect(screen.getByText(/Total URLs/i)).toBeDefined();
  });

  it('renders About page', () => {
    render(<MemoryRouter initialEntries={['/about']}><App /></MemoryRouter>);
    expect(screen.getByText(/About PhishScope/i)).toBeDefined();
  });

  it('renders Documentation page', () => {
    render(<MemoryRouter initialEntries={['/docs']}><App /></MemoryRouter>);
    expect(screen.getByText(/Phase 1-7 Summary/i)).toBeDefined();
  });

  it('renders 404 for unknown routes', () => {
    render(<MemoryRouter initialEntries={['/unknown']}><App /></MemoryRouter>);
    expect(screen.getByText(/404/i)).toBeDefined();
    expect(screen.getByText(/Page Not Found/i)).toBeDefined();
  });
});

describe('AnalyzerForm Tests', () => {
  it('disables submit button when URL is empty', () => {
    const mockOnAnalyze = vi.fn();
    render(<AnalyzerForm onAnalyze={mockOnAnalyze} isLoading={false} />);
    const button = screen.getByRole('button', { name: /Analyze/i });
    expect(button.disabled).toBe(true);
  });

  it('calls onAnalyze on submit with valid URL', () => {
    const mockOnAnalyze = vi.fn();
    render(<AnalyzerForm onAnalyze={mockOnAnalyze} isLoading={false} />);
    const input = screen.getByPlaceholderText(/https:\/\/g00gle.xyz/i);
    const button = screen.getByRole('button', { name: /Analyze/i });
    
    fireEvent.change(input, { target: { value: 'https://test.com' } });
    expect(button.disabled).toBe(false);
    fireEvent.click(button);
    expect(mockOnAnalyze).toHaveBeenCalledWith('https://test.com');
  });

  it('displays loading state correctly', () => {
    const mockOnAnalyze = vi.fn();
    render(<AnalyzerForm onAnalyze={mockOnAnalyze} isLoading={true} />);
    const button = screen.getByRole('button');
    expect(button.textContent).toBe('Analyzing...');
    expect(button.disabled).toBe(true);
  });
});

describe('ResultCard Tests', () => {
  it('renders DANGEROUS verdict correctly', () => {
    const mockResult = {
      hybrid: { verdict: 'DANGEROUS', score: 91, confidence: 'VERY_HIGH' },
      ml: { probability: 0.98 },
    };
    render(<ResultCard result={mockResult} />);
    expect(screen.getByText(/DANGEROUS/i)).toBeDefined();
    expect(screen.getByText(/91/i)).toBeDefined();
    expect(screen.getByText(/98.0%/i)).toBeDefined();
  });
});

describe('ExplanationCard Tests', () => {
  it('renders SHAP explanations correctly', () => {
    const explanation = {
      summary: "This URL is phishing.",
      top_features: [
        { feature: "lookalike", impact: "+24%" }
      ]
    };
    render(<ExplanationCard explanation={explanation} />);
    expect(screen.getByText(/This URL is phishing./i)).toBeDefined();
    expect(screen.getByText(/lookalike/i)).toBeDefined();
    expect(screen.getByText(/\+24%/i)).toBeDefined();
  });
});

describe('VerdictBadge Tests', () => {
  it('renders SAFE badge', () => {
    render(<VerdictBadge verdict="SAFE" />);
    expect(screen.getByText(/SAFE/i)).toBeDefined();
  });
});
