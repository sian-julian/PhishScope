const About = () => {
  return (
    <div className="w-full max-w-4xl mx-auto py-8 text-gray-300">
      <h1 className="text-4xl font-bold text-white mb-8">About PhishScope</h1>
      
      <div className="glass p-8 rounded-2xl mb-8 space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-white mb-4">Project Overview</h2>
          <p>
            PhishScope is a state-of-the-art hybrid phishing detection system. It combines 
            traditional heuristic rules (Phase 2) with a powerful Random Forest Machine Learning 
            model (Phase 5) to achieve 98.3% accuracy in detecting malicious URLs.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-4 mt-8">Architecture</h2>
          <p>
            The pipeline consists of high-speed URL feature extraction, heuristic scoring, 
            machine learning prediction, and a consensus engine. We then use Explainable AI (SHAP) 
            to translate the ML model's decision into human-readable text.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-4 mt-8">Technologies Used</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li><strong>Frontend:</strong> React 19, Vite, Tailwind CSS, Recharts</li>
            <li><strong>Backend:</strong> Python, Flask, Pandas</li>
            <li><strong>Machine Learning:</strong> Scikit-Learn (Random Forest), Joblib</li>
            <li><strong>Explainable AI:</strong> SHAP (SHapley Additive exPlanations)</li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default About;
