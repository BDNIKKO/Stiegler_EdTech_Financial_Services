import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div>
      <nav>
        <ul>
          <li><Link to="/loan-application">Personal Loan Application</Link></li>
          <li><Link to="/about-us">About Us</Link></li>
          <li><Link to="/support">Support</Link></li>
          <li><button onClick={handleLogout}>Log Out</button></li>
        </ul>
      </nav>
      <div>
        <h1>Welcome to Your Dashboard</h1>
        <img src="/professional_photo.jpg" alt="Professional" />
        <p>This is your dashboard. From here, you can navigate through the application.</p>
      </div>
    </div>
  );
}

export default Dashboard;
