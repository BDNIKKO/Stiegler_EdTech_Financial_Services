import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AboutUs.css';

function AboutUs() {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="about-page">
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
          <li><button onClick={handleLogout} className="logout-button">Log Out</button></li>
        </ul>
      </nav>

      <div className="about-container">
        <div className="about-content">
          <div className="about-header">
            <h1>Our Story</h1>
          </div>
          
          <div className="about-sections">
            <div className="about-section">
              <h2>Who We Are</h2>
              <p>
                Founded in 2020, Nexus Lending Solutions emerged from a vision to revolutionize 
                the lending industry through innovative technology and customer-centric services. 
                We've grown from a small startup to a trusted name in digital lending, serving 
                thousands of clients nationwide.
              </p>
            </div>

            <div className="about-section">
              <h2>Our Mission</h2>
              <p>
                We're committed to making financial services more accessible, transparent, and 
                efficient. Through our advanced lending platform, we provide quick, secure, and 
                personalized loan solutions that empower our clients to achieve their financial goals.
              </p>
            </div>

            <div className="about-section">
              <h2>Our Values</h2>
              <div className="values-grid">
                <div className="value-item">
                  <h3>Innovation</h3>
                  <p>Continuously improving our technology to provide better services</p>
                </div>
                <div className="value-item">
                  <h3>Integrity</h3>
                  <p>Maintaining the highest standards of transparency and ethics</p>
                </div>
                <div className="value-item">
                  <h3>Security</h3>
                  <p>Protecting our clients' data with state-of-the-art security measures</p>
                </div>
                <div className="value-item">
                  <h3>Excellence</h3>
                  <p>Delivering exceptional service in everything we do</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutUs; 