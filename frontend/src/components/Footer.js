import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <img src="/images/nexus-icon.png" alt="Nexus Icon" className="footer-logo" />
          <p>Revolutionizing lending through innovative technology and customer-centric services.</p>
        </div>
        
        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><Link to="/about">About Us</Link></li>
            <li><Link to="/loan-application">Apply for Loan</Link></li>
            <li><Link to="/support">Support</Link></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h3>Contact</h3>
          <ul>
            <li>Email: support@nexuslending.com</li>
            <li>Phone: (555) 123-4567</li>
            <li>Hours: Mon-Fri 9AM-5PM EST</li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; 2024 Nexus Lending Solutions. All rights reserved.</p>
        <div className="footer-links">
          <Link to="/privacy">Privacy Policy</Link>
          <Link to="/terms">Terms of Service</Link>
        </div>
      </div>
    </footer>
  );
}

export default Footer; 