import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <img 
          src="/images/nexus-icon.png"
          alt="Nexus" 
          className="navbar-logo"
        />
      </Link>
    </nav>
  );
}

export default Navbar; 