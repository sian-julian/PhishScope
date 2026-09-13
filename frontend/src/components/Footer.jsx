import { Link } from 'react-router-dom';
import logo from '../assets/PhishScope-logo.png';

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-si text-ag border-t border-si-700 mt-auto">
      <div className="max-w-content mx-auto px-5 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12">

          {/* Brand */}
          <div className="md:col-span-1">
            <Link to="/" aria-label="PhishScope home" className="inline-block mb-4">
              <img src={logo} alt="PhishScope" className="h-16 w-auto opacity-90 hover:opacity-100 transition-opacity" />
            </Link>
            <p className="text-body-sm text-ag leading-relaxed max-w-xs">
              AI-powered hybrid phishing detection. Know what's behind every URL before it reaches you.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <p className="label-caps mb-5 text-ag/60">Platform</p>
            <ul className="space-y-3">
              {[
                { to: '/analyzer',  label: 'Analyzer' },
                { to: '/dashboard', label: 'Dashboard' },
                { to: '/docs',      label: 'Documentation' },
                { to: '/about',     label: 'About' },
              ].map((link) => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className="text-body-sm text-ag hover:text-sw transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Detection */}
          <div>
            <p className="label-caps mb-5 text-ag/60">Detection Engine</p>
            <ul className="space-y-3 text-body-sm text-ag">
              <li>Machine Learning (Random Forest)</li>
              <li>Heuristic Analysis</li>
              <li>Hybrid Decision Engine</li>
              <li>Explainable AI (SHAP)</li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-si-700 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-caption text-ag">
            © {year} PhishScope. Academic research project. Not for commercial use.
          </p>
          <p className="text-caption text-ag">
            Detect. Analyze. Protect.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
