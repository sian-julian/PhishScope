import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import Documentation from './pages/Documentation';
import NotFound from './pages/NotFound';

// Full-bleed pages manage their own internal max-width + padding
const fullBleedRoutes = ['/', '/analyzer', '/dashboard', '/about', '/docs'];

const PageWrapper = ({ children }) => {
  const location = useLocation();
  const isFullBleed = fullBleedRoutes.includes(location.pathname);

  return (
    <div key={location.pathname} className={`animate-ps-enter w-full ${isFullBleed ? '' : 'max-w-content mx-auto px-5 lg:px-8 py-10'}`}>
      {children}
    </div>
  );
};

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-ms">
      <Navbar />
      <main className="flex-grow w-full" id="main-content">
        <Routes>
          <Route path="/"          element={<PageWrapper><Home          /></PageWrapper>} />
          <Route path="/analyzer"  element={<PageWrapper><Analyzer      /></PageWrapper>} />
          <Route path="/dashboard" element={<PageWrapper><Dashboard     /></PageWrapper>} />
          <Route path="/about"     element={<PageWrapper><About         /></PageWrapper>} />
          <Route path="/docs"      element={<PageWrapper><Documentation /></PageWrapper>} />
          <Route path="*"          element={<PageWrapper><NotFound      /></PageWrapper>} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
