import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './LoanResult.css';

function LoanResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const { approved, details } = location.state?.loanDecision || {};
  const confirmationNumber = React.useMemo(() => 
    `LN-${Math.random().toString(36).substr(2, 4)}-${Date.now().toString().substr(-4)}`.toUpperCase(),
  []);

  return (
    <div className="result-container">
      <div className="result-card">
        <div className={`result-header ${approved ? 'approved' : 'denied'}`}>
          <h2>Application {approved ? 'Approved' : 'Status Update'}</h2>
          <div className="confirmation-number">
            Confirmation #: {confirmationNumber}
          </div>
        </div>

        <div className="result-content">
          <div className="status-message">
            <p>
              {approved 
                ? "We're pleased to inform you that your loan application has been approved." 
                : "We have completed our initial review of your loan application."}
            </p>
          </div>

          <div className="next-steps-section">
            <h3>Next Steps</h3>
            <p>A comprehensive decision package will be sent to your registered address within 7-10 business days.</p>
            
            <div className="package-contents">
              <h4>Your package will include:</h4>
              <ul>
                <li>
                  <span className="bullet">•</span>
                  <span>Detailed decision explanation</span>
                </li>
                <li>
                  <span className="bullet">•</span>
                  <span>Terms and conditions</span>
                </li>
                <li>
                  <span className="bullet">•</span>
                  <span>Required documentation checklist</span>
                </li>
                <li>
                  <span className="bullet">•</span>
                  <span>Next steps instructions</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="contact-info">
            <p>If you don't receive your package within 10 business days, please contact our loan services department.</p>
            <p className="reference">Please reference confirmation number: {confirmationNumber}</p>
          </div>

          <button 
            className="dashboard-button"
            onClick={() => navigate('/dashboard')}
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoanResult;