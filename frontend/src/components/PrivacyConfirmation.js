import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './PrivacyConfirmation.css';

function PrivacyConfirmation() {
  const [agreed, setAgreed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const loanDecision = location.state?.loanDecision;

  const handleContinue = () => {
    if (agreed) {
      navigate('/loading-decision', { state: { loanDecision } });
    }
  };

  return (
    <div className="privacy-container">
      <div className="privacy-card">
        <h2>Privacy Notice & Consent</h2>
        
        <div className="privacy-content">
          <p>Before we proceed with your loan decision, please review and acknowledge our privacy terms:</p>
          
          <div className="privacy-scroll">
            <h3>Information Collection & Usage</h3>
            <p>We collect and process your personal and financial information to evaluate your loan application and provide our services.</p>

            <h3>Decision Communication</h3>
            <p>Your loan decision will be communicated via secure mail to protect your privacy. Additional details about your application will be sent to your registered address within 7-10 business days.</p>

            <h3>Data Protection</h3>
            <p>Your information is protected using industry-standard security measures and will only be used for the purposes specified in our full privacy policy.</p>
          </div>

          <div className="consent-checkbox">
            <label>
              <input 
                type="checkbox" 
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
              />
              I acknowledge that I have read and agree to the privacy terms
            </label>
          </div>

          <button 
            className={`continue-button ${!agreed ? 'disabled' : ''}`}
            onClick={handleContinue}
            disabled={!agreed}
          >
            Continue to Decision
          </button>
        </div>
      </div>
    </div>
  );
}

export default PrivacyConfirmation; 