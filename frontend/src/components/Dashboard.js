import React from 'react';
import { useNavigate } from 'react-router-dom';

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
          <li><a href="/loan-application">Personal Loan Application</a></li>
          <li><a href="/support">Support</a></li>
          <li><button onClick={handleLogout}>Log Out</button></li>
        </ul>
      </nav>
      <div>
        <h1>Welcome to Your Dashboard</h1>
        <img src="/professional_photo.jpg" alt="Professional" />
        <p>This is your dashboard. From here, you can navigate through the application.</p>
        <h2>About Us</h2>
        <p>We are a financial service provider focused on making loan applications simple and accessible for everyone. Our goal is to use advanced technology to provide an easy and seamless loan application process for users. We pride ourselves on customer satisfaction and support throughout the process, ensuring you have the best experience possible.</p>
      </div>
    </div>
  );
}

export default Dashboard;
