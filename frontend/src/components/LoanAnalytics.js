import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoanAnalytics.css';

function formatDateTime(isoString) {
  return new Date(isoString).toLocaleString('en-US', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short'
  });
}

function ApplicationItem({ app }) {
  return (
    <div key={app.id} className="application-item">
      <div className="applicant-name">
        {app.firstName} {app.lastName}
      </div>
      <div className="loan-amount">
        ${app.loanAmount.toLocaleString()}
      </div>
      <div className="contact-section">
        <div className="contact-header">Contact Information</div>
        <div className="contact-info">
          <div className="contact-detail">
            <span className="contact-label">Email:</span> {app.email}
          </div>
          <div className="contact-detail">
            <span className="contact-label">Phone:</span> {app.phone}
          </div>
        </div>
      </div>
    </div>
  );
}

function LoanAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [applications, setApplications] = useState({ approved: [], denied: [] });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('No authentication token found');
          navigate('/login');
          return;
        }

        const headers = {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        };

        // Fetch both analytics and applications data
        const [analyticsResponse, applicationsResponse] = await Promise.all([
          fetch('http://localhost:5000/api/loan-analytics', { headers }),
          fetch('http://localhost:5000/api/loan-applications/list', { headers })
        ]);

        if (analyticsResponse.status === 401 || applicationsResponse.status === 401) {
          setError('Authentication failed. Please log in again.');
          navigate('/login');
          return;
        }

        if (analyticsResponse.status === 403 || applicationsResponse.status === 403) {
          setError('Access denied. Admin privileges required.');
          navigate('/dashboard');
          return;
        }

        const [analyticsData, applicationsData] = await Promise.all([
          analyticsResponse.json(),
          applicationsResponse.json()
        ]);

        setAnalytics(analyticsData);
        setApplications({
          approved: applicationsData.filter(app => app.status === 'approved'),
          denied: applicationsData.filter(app => app.status === 'denied')
        });
      } catch (error) {
        console.error('Error:', error);
        setError(error.message);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 120000);
    return () => clearInterval(interval);
  }, [navigate]);

  if (error) return <div className="error-message">{error}</div>;
  if (!analytics) return <div className="loading">Loading analytics...</div>;

  return (
    <div className="analytics-container">
      <nav className="dashboard-nav">
        <div className="nav-logo">
          <Link to="/dashboard">
            <img src="/images/nexus-icon.png" alt="Nexus Icon" className="nav-logo-img" />
          </Link>
        </div>
        <ul className="nav-links">
          <li><Link to="/loan-application" className="nav-link">Personal Loan Application</Link></li>
          <li><Link to="/about" className="nav-link">About Us</Link></li>
          <li><Link to="/support" className="nav-link">Support</Link></li>
          <li><button onClick={() => {
            localStorage.removeItem('token');
            navigate('/login');
          }} className="logout-button">Log Out</button></li>
        </ul>
      </nav>

      <div className="analytics-content">
        <h2>Loan Analytics Dashboard</h2>
        
        <div className="analytics-grid">
          {/* Existing analytics cards */}
          <div className="analytics-card">
            <h3>Total Applications</h3>
            <div className="value">{analytics.total_applications}</div>
          </div>
          
          <div className="analytics-card">
            <h3>Approved Loans</h3>
            <div className="value">{analytics.approved_count}</div>
            <div className="rate">({analytics.approval_rate.toFixed(1)}%)</div>
          </div>
          
          <div className="analytics-card">
            <h3>Denied Loans</h3>
            <div className="value">{analytics.denied_count}</div>
            <div className="rate">({(100 - analytics.approval_rate).toFixed(1)}%)</div>
          </div>
          
          <div className="analytics-card">
            <h3>Average Loan Amount</h3>
            <div className="value">
              ${analytics.avg_loan_amount.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              })}
            </div>
          </div>
        </div>

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

        <div className="applications-grid">
          {/* Approved Applications */}
          <div className="applications-card">
            <h3>Approved Applications</h3>
            <div className="applications-list">
              {applications.approved.map(app => (
                <ApplicationItem key={app.id} app={app} />
              ))}
            </div>
          </div>

          {/* Denied Applications */}
          <div className="applications-card">
            <h3>Denied Applications</h3>
            <div className="applications-list">
              {applications.denied.map(app => (
                <ApplicationItem key={app.id} app={app} />
              ))}
            </div>
          </div>
        </div>

        <div className="last-updated">
          Last Updated: {formatDateTime(analytics.last_updated)}
        </div>
      </div>
    </div>
  );
}

export default LoanAnalytics;
