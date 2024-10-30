import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './LoanApplication.css';

function LoanApplication() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    loan_amount: '',
    loan_term: '',
    income: '',
    employment_length: '',
    purpose: '',
  });
  const [message, setMessage] = useState({ text: '', type: '', details: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Check for valid token on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const decoded = jwtDecode(token);
      if (decoded.exp * 1000 < Date.now()) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    } catch (error) {
      localStorage.removeItem('token');
      navigate('/login');
    }
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Remove any non-numeric characters for number inputs
    if (['loan_amount', 'income', 'employment_length'].includes(name)) {
      const numericValue = value.replace(/[^0-9]/g, '');
      setFormData(prevState => ({
        ...prevState,
        [name]: numericValue
      }));
    } else {
      setFormData(prevState => ({
        ...prevState,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          annual_income: parseFloat(formData.income),
          loan_amount: parseFloat(formData.loan_amount),
          loan_term: parseFloat(formData.loan_term),
          employment_length: parseFloat(formData.employment_length)
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const loanDecision = {
          approved: data.approved,
          details: data.details
        };
        navigate('/privacy-confirmation', { state: { loanDecision } });
      } else if (response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        throw new Error(data.message || 'Submission failed');
      }
    } catch (error) {
      setMessage({
        text: 'An error occurred while processing your application',
        type: 'error',
        details: error.message
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="loan-application-container">
      <div className="loan-application-card">
        {message.text && (
          <div className={`message-popup ${message.type}`}>
            <div className="message-text">{message.text}</div>
            {message.details && (
              <div className="message-details">{message.details}</div>
            )}
          </div>
        )}
        
        <h1>Loan Application</h1>
        <form onSubmit={handleSubmit} className="loan-form">
          <div className="form-group">
            <label htmlFor="loan_amount">Loan Amount ($)</label>
            <input
              type="text"
              id="loan_amount"
              name="loan_amount"
              value={formData.loan_amount}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="Enter loan amount"
            />
          </div>

          <div className="form-group">
            <label htmlFor="loan_term">Loan Term (months)</label>
            <select
              id="loan_term"
              name="loan_term"
              value={formData.loan_term}
              onChange={handleChange}
              required
              className="form-select"
            >
              <option value="">Select Term</option>
              <option value="12">12 months</option>
              <option value="24">24 months</option>
              <option value="36">36 months</option>
              <option value="48">48 months</option>
              <option value="60">60 months</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="income">Annual Income ($)</label>
            <input
              type="text"
              id="income"
              name="income"
              value={formData.income}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="Enter annual income"
            />
          </div>

          <div className="form-group">
            <label htmlFor="employment_length">Employment Length (years)</label>
            <input
              type="text"
              id="employment_length"
              name="employment_length"
              value={formData.employment_length}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="Enter employment length"
            />
          </div>

          <div className="form-group">
            <label htmlFor="purpose">Loan Purpose</label>
            <select
              id="purpose"
              name="purpose"
              value={formData.purpose}
              onChange={handleChange}
              required
              className="form-select"
            >
              <option value="">Select Purpose</option>
              <option value="debt_consolidation">Debt Consolidation</option>
              <option value="home_improvement">Home Improvement</option>
              <option value="business">Business</option>
              <option value="education">Education</option>
              <option value="other">Other</option>
            </select>
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Processing Application...' : 'Submit Application'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoanApplication;