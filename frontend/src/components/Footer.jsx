const Footer = () => {
  return (
    <footer className="glass rounded-t-2xl mt-auto">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-gray-400">
          &copy; {new Date().getFullYear()} PhishScope. AI-Powered Hybrid Phishing Detection.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
