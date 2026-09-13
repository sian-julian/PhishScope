import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import logo from '../assets/PhishScope-logo.png';

const navLinks = [
  { to: '/',          label: 'Home' },
  { to: '/analyzer',  label: 'Analyzer' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/docs',      label: 'Documentation' },
  { to: '/about',     label: 'About' },
];

const Navbar = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  return (
    <header style={{ isolation: 'isolate' }}>
      <nav
        className="bg-sw border-b border-ch sticky top-0"
        aria-label="Main navigation"
      >
        <div className="max-w-content mx-auto px-5 lg:px-8">
          <div className="flex items-center justify-between h-[72px]">

            {/* Logo */}
            <Link
              to="/"
              className="flex items-center gap-3 shrink-0"
              aria-label="PhishScope home"
            >
              <img
                src={logo}
                alt="PhishScope"
                className="h-14 w-auto"
              />
            </Link>

            {/* Desktop nav — centered */}
            <div className="hidden md:flex items-center gap-1" role="navigation">
              {navLinks.map((link) => {
                const isActive = location.pathname === link.to;
                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    className={`px-4 py-2 text-body-sm font-medium rounded-pill transition-all duration-150 ${
                      isActive
                        ? 'bg-si text-sw'
                        : 'text-cg hover:text-si hover:bg-ms'
                    }`}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </div>

            {/* Desktop CTA */}
            <div className="hidden md:flex items-center gap-3">
              <Link to="/analyzer" className="btn-primary text-body-sm">
                Analyze URL
              </Link>
            </div>

            {/* Mobile hamburger — no z-index, uses DOM order */}
            <button
              className="md:hidden flex flex-col gap-1.5 p-2 text-si"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={mobileOpen}
            >
              <span className={`block h-0.5 w-5 bg-si transition-all duration-200 ${mobileOpen ? 'rotate-45 translate-y-2' : ''}`} />
              <span className={`block h-0.5 w-5 bg-si transition-all duration-200 ${mobileOpen ? 'opacity-0' : ''}`} />
              <span className={`block h-0.5 w-5 bg-si transition-all duration-200 ${mobileOpen ? '-rotate-45 -translate-y-2' : ''}`} />
            </button>
          </div>
        </div>

        {/* Mobile menu — conditional render, no z-index */}
        {mobileOpen && (
          <div className="md:hidden bg-sw border-t border-ch" role="navigation" aria-label="Mobile navigation">
            <div className="max-w-content mx-auto px-5 py-4 space-y-1">
              {navLinks.map((link) => {
                const isActive = location.pathname === link.to;
                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    onClick={() => setMobileOpen(false)}
                    className={`block px-4 py-3 rounded-card-sm text-body font-medium transition-colors ${
                      isActive
                        ? 'bg-si text-sw'
                        : 'text-cg hover:text-si hover:bg-ms'
                    }`}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    {link.label}
                  </Link>
                );
              })}
              <div className="pt-2 border-t border-ch mt-2">
                <Link
                  to="/analyzer"
                  onClick={() => setMobileOpen(false)}
                  className="btn-primary w-full justify-center"
                >
                  Analyze URL
                </Link>
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Navbar;
