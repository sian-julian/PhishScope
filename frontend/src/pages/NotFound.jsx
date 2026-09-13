import { Link } from 'react-router-dom';

const NotFound = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-5">
    <p className="label-caps text-sv mb-4">404</p>
    <h1 className="text-h font-semibold text-si mb-3">Page not found</h1>
    <p className="text-body text-cg mb-8 max-w-sm">
      The page you're looking for doesn't exist. It may have been moved or the URL is incorrect.
    </p>
    <Link to="/" className="btn-primary">
      Return to Home
    </Link>
  </div>
);

export default NotFound;
