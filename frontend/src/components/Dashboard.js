import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();

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
          <h1>Welcome to Your Dashboard</h1>
          <p className="welcome-text">
            Access your loan applications and account information all in one place.
          </p>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card">
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
