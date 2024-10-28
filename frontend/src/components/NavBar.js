import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <nav>
      <ul>
        <li><Link to="/loan-application">Loan Application</Link></li>
        <li><Link to="/about-us">About Us</Link></li>
        <li><Link to="/support">Support</Link></li>
        <li><Link to="/login">Logout</Link></li>
      </ul>
    </nav>
  );
}

export default NavBar;
