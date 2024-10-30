import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './LoadingDecision.css';

function LoadingDecision() {
  const navigate = useNavigate();
  const location = useLocation();
  const loanDecision = location.state?.loanDecision;

  useEffect(() => {
    // Simulate processing time (3.5 seconds)
    const timer = setTimeout(() => {
      navigate('/loan-result', { state: { loanDecision } });
    }, 3500);

    return () => clearTimeout(timer);
  }, [navigate, loanDecision]);

  return (
    <div className="loading-container">
      <div className="loading-card">
        <div className="loading-content">
          <div className="spinner"></div>
          <h2>Processing Your Application</h2>
          <div className="loading-steps">
            <div className="step">
              <div className="dot active"></div>
              <span>Verifying Information</span>
            </div>
            <div className="step">
              <div className="dot"></div>
              <span>Analyzing Data</span>
            </div>
            <div className="step">
              <div className="dot"></div>
              <span>Finalizing Decision</span>
            </div>
          </div>
          <p className="loading-message">Please wait while we process your application...</p>
        </div>
      </div>
    </div>
  );
}

export default LoadingDecision; 