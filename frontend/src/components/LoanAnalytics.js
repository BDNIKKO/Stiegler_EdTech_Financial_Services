import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoanAnalytics.css';

function LoanAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem('token');
        console.log('Using token:', token);
        
        if (!token) {
          setError('No authentication token found');
          navigate('/login');
          return;
        }

        const response = await fetch('http://localhost:5000/api/loan-analytics', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        
        console.log('Response status:', response.status);
        
        if (response.status === 401) {
          setError('Authentication failed. Please log in again.');
          navigate('/login');
          return;
        }
        
        if (response.status === 403) {
          setError('Access denied. Admin privileges required.');
          navigate('/dashboard');
          return;
        }

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to fetch analytics');
        }

        const data = await response.json();
        console.log('Received data:', data);
        setAnalytics(data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
        setError(error.message);
      }
    };

    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 120000);
    return () => clearInterval(interval);
  }, [navigate]);

  if (error) return <div className="error-message">{error}</div>;
  if (!analytics) return <div className="loading">Loading analytics...</div>;

  return (
    <div className="analytics-dashboard">
      <h2>Loan Analytics Dashboard</h2>
      
      <div className="analytics-grid">
        {/* Summary Cards */}
        <div className="analytics-card total">
          <h3>Total Applications</h3>
          <div className="value">{analytics.total_applications}</div>
        </div>
        
        <div className="analytics-card approved">
          <h3>Approved Loans</h3>
          <div className="value">{analytics.approved_count}</div>
          <div className="rate">({analytics.approval_rate.toFixed(1)}%)</div>
        </div>
        
        <div className="analytics-card denied">
          <h3>Denied Loans</h3>
          <div className="value">{analytics.denied_count}</div>
          <div className="rate">({(100 - analytics.approval_rate).toFixed(1)}%)</div>
        </div>
        
        <div className="analytics-card amount">
          <h3>Average Loan Amount</h3>
          <div className="value">
            ${analytics.avg_loan_amount.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </div>
        </div>
      </div>

      {/* Progress Bar for Approval Rate */}
      <div className="approval-rate-container">
        <h3>Approval Rate</h3>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${analytics.approval_rate}%` }}
          />
          <span className="progress-label">{analytics.approval_rate.toFixed(1)}%</span>
        </div>
      </div>

      <div className="last-updated">
        Last Updated: {new Date(analytics.last_updated).toLocaleString()}
      </div>

      <button className="back-button" onClick={() => navigate('/')}>
        Back to Dashboard
      </button>
    </div>
  );
}

export default LoanAnalytics;
