import { Link } from 'react-router-dom';
import { FiShield, FiArrowRight } from 'react-icons/fi';

const Hero = () => {
  return (
    <div className="relative py-20 lg:py-32 flex flex-col items-center justify-center text-center px-4">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/20 via-secondary to-secondary"></div>
      </div>
      
      <div className="relative z-10 max-w-4xl mx-auto">
        <div className="flex justify-center mb-6">
          <div className="p-4 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-md shadow-2xl">
            <FiShield className="w-16 h-16 text-primary" />
          </div>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 tracking-tight mb-6">
          PhishScope
        </h1>
        
        <p className="text-xl md:text-2xl text-gray-400 mb-10 max-w-2xl mx-auto font-light">
          AI-Powered Hybrid Phishing Detection System. Combining heuristics and machine learning for unmatched accuracy and explainability.
        </p>
        
        <Link 
          to="/analyzer" 
          className="inline-flex items-center gap-2 bg-primary hover:bg-blue-500 text-white px-8 py-4 rounded-full font-bold text-lg transition-all hover:scale-105 shadow-[0_0_20px_rgba(37,99,235,0.4)]"
        >
          Analyze URL <FiArrowRight />
        </Link>
      </div>
    </div>
  );
};

export default Hero;
