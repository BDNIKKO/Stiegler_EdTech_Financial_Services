import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

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
      const decoded = jwtDecode(token);  // Correct usage
      return decoded.user === 'admin';  // Adjust based on your JWT structure
    } catch (error) {
      console.error('Invalid token:', error);
      return false;
    }
  };
  

  return (
    <div>
      <nav>
        <ul>
          <li><Link to="/loan-application">Personal Loan Application</Link></li>
          <li><Link to="/support">Support</Link></li>

          {/* Use Link or button with navigate */}
          {isAdmin() && (
            <li>
              <Link to="/loan-dashboard" className="nav-button">
                Loan Dashboard
              </Link>
            </li>
          )}

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
