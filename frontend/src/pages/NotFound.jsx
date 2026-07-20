import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] text-center">
      <h1 className="text-6xl font-bold text-white mb-4">404</h1>
      <p className="text-2xl text-gray-400 mb-8">Page Not Found</p>
      <Link to="/" className="bg-primary hover:bg-blue-500 text-white px-6 py-3 rounded-full font-bold transition-colors">
        Return Home
      </Link>
    </div>
  );
};

export default NotFound;
