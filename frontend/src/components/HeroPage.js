import React from 'react';
import { Link } from 'react-router-dom';
import './HeroPage.css';

function HeroPage() {
  return (
    <div className="hero-container">
      <div className="hero-content">
        <h1>Welcome to Stiegler EdTech Financial Services</h1>
        <p>Apply for loans easily and get real-time decisions.</p>
        <div className="hero-buttons">
          <Link to="/register" className="hero-button">Register</Link>
          <Link to="/login" className="hero-button">Login</Link>
        </div>
      </div>
    </div>
  );
}

export default HeroPage;
