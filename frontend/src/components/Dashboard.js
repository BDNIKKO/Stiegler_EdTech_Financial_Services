import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const [userLoans, setUserLoans] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserLoans = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:5000/api/user/loans', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        const data = await response.json();
        setUserLoans(data);
      } catch (error) {
        console.error('Error fetching user loans:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserLoans();
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

  const getStatusDisplay = (status) => {
    return status.toLowerCase() === 'denied' ? 'Pending Review' : status;
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
          {isAdmin() && (
            <li>
              <Link to="/loan-dashboard" className="nav-link admin-link">
                Loan Dashboard
              </Link>
            </li>
          )}
          <li><button onClick={handleLogout} className="logout-button">Log Out</button></li>
        </ul>
      </nav>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h1>Welcome, {userLoans?.firstName || 'User'}</h1>
          <p className="welcome-text">
            Track your loan applications and financial journey with us.
          </p>
        </div>

        <div className="dashboard-grid">
          {/* Latest Application Status */}
          {userLoans?.recentLoan && (
            <div className="dashboard-card status-card">
              <h2>Latest Application</h2>
              <div className={`status-badge ${userLoans.recentLoan.decision.toLowerCase()}`}>
                {getStatusDisplay(userLoans.recentLoan.decision)}
              </div>
              <div className="loan-details">
                <div className="detail-item">
                  <span className="detail-label">Amount</span>
                  <span className="detail-value">{formatCurrency(userLoans.recentLoan.loan_amount)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Term</span>
                  <span className="detail-value">{userLoans.recentLoan.loan_term} months</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Applied</span>
                  <span className="detail-value">
                    {new Date(userLoans.recentLoan.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Application History */}
          <div className="dashboard-card">
            <h2>Your Statistics</h2>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-value">{userLoans?.stats?.totalApplications || 0}</div>
                <div className="stat-label">Total Applications</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">
                  {formatCurrency(userLoans?.stats?.totalAmount || 0)}
                </div>
                <div className="stat-label">Total Amount Requested</div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="dashboard-card action-card">
            <h2>Quick Actions</h2>
            <div className="action-buttons">
              <Link to="/loan-application" className="action-button">
                New Loan Application
              </Link>
              <Link to="/support" className="action-button">
                Contact Support
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

