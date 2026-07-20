import { Link } from 'react-router-dom';
import { FiShield } from 'react-icons/fi';

const Navbar = () => {
  return (
    <nav className="glass sticky top-0 z-50 rounded-b-2xl mb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 text-white hover:text-primary transition-colors">
            <FiShield className="w-8 h-8 text-primary" />
            <span className="font-bold text-xl tracking-tight">PhishScope</span>
          </Link>
          
          <div className="hidden md:block">
            <div className="flex items-baseline space-x-8">
              <Link to="/" className="text-gray-300 hover:text-white transition-colors px-3 py-2 rounded-md text-sm font-medium">Home</Link>
              <Link to="/analyzer" className="bg-primary/20 text-primary hover:bg-primary/30 transition-colors px-3 py-2 rounded-md text-sm font-medium">Analyzer</Link>
              <Link to="/dashboard" className="text-gray-300 hover:text-white transition-colors px-3 py-2 rounded-md text-sm font-medium">Dashboard</Link>
              <Link to="/about" className="text-gray-300 hover:text-white transition-colors px-3 py-2 rounded-md text-sm font-medium">About</Link>
              <Link to="/docs" className="text-gray-300 hover:text-white transition-colors px-3 py-2 rounded-md text-sm font-medium">Documentation</Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
