import React from 'react';
import { Link } from 'react-router-dom';
import './HeroPage.css';

function HeroPage() {
  return (
    <div className="hero-container">
      <div className="hero-content">
        <div className="hero-logo-container">
          <img 
            src="/images/nexus-logo.png" 
            alt="Nexus Lending Solutions" 
            className="hero-logo"
          />
        </div>
        <p>Experience seamless lending with our real-time decision platform.<br />
           Fast, secure, and tailored to your needs.</p>
        <div className="hero-buttons">
          <Link to="/register" className="hero-button">Get Started</Link>
          <Link to="/login" className="hero-button">Sign In</Link>
        </div>
      </div>
    </div>
  );
}

export default HeroPage;
