import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:5000/api/user/applications', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const isAdmin = () => {
    const token = localStorage.getItem('token');
    if (!token) return false;
    try {
      const decoded = jwtDecode(token);
      return decoded.user === 'admin';
    } catch (error) {
      console.error('Invalid token:', error);
      return false;
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'approved': return 'var(--success-color)';
      case 'denied': return 'var(--danger-color)';
      default: return 'var(--pending-color)';
    }
  };

  return (
    <div className="dashboard-container">
      <nav className="dashboard-nav">
        <div className="nav-logo">
          <img src="/images/nexus-icon.png" alt="Nexus Icon" className="nav-logo-img" />
        </div>
        <ul className="nav-links">
          <li><Link to="/loan-application" className="nav-link">Personal Loan Application</Link></li>
          <li><Link to="/about" className="nav-link">About Us</Link></li>
          <li><Link to="/support" className="nav-link">Support</Link></li>
          <li><button onClick={handleLogout} className="logout-button">Log Out</button></li>
        </ul>
      </nav>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h1>Welcome, {userData?.firstName || 'User'}</h1>
          <p className="welcome-text">
            Manage your loan applications and track their status.
          </p>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h2>Quick Actions</h2>
            <div className="action-buttons">
              <Link to="/loan-application" className="action-button">
                Apply for a New Loan
              </Link>
              <Link to="/support" className="action-button">
                Contact Support
              </Link>
            </div>
          </div>

          {userData?.recentApplication && (
            <div className="dashboard-card">
              <h2>Latest Application Status</h2>
              <div className="status-container">
                <div className="status-badge" 
                     style={{ backgroundColor: getStatusColor(userData.recentApplication.decision) }}>
                  {userData.recentApplication.decision}
                </div>
                <div className="application-details">
                  <div className="detail-row">
                    <span>Loan Amount:</span>
                    <span>{formatCurrency(userData.recentApplication.loan_amount)}</span>
                  </div>
                  <div className="detail-row">
                    <span>Term:</span>
                    <span>{userData.recentApplication.loan_term} months</span>
                  </div>
                  <div className="detail-row">
                    <span>Applied:</span>
                    <span>{new Date(userData.recentApplication.timestamp).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {userData?.stats && (
            <div className="dashboard-card">
              <h2>Your Application History</h2>
              <div className="history-stats">
                <div className="stat-item">
                  <span className="stat-value">{userData.stats.totalApplications}</span>
                  <span className="stat-label">Total Applications</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">
                    {formatCurrency(userData.stats.averageLoanAmount)}
                  </span>
                  <span className="stat-label">Average Loan Amount</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
