import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import HeroPage from './components/HeroPage';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import Support from './components/Support';
import LoanAnalytics from './components/LoanAnalytics';
import Navbar from './components/Navbar';
import './styles/styles.css';

function LoanApplication() {
  const [formData, setFormData] = useState({
    income: '',
    loan_amount: '',
    loan_term: '',
    employment_length: ''
  });

  const [prediction, setPrediction] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if token is present; if not, redirect to login
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Add the rest of your LoanApplication component code here
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<HeroPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/support" element={<Support />} />
          <Route path="/loan-dashboard" element={<LoanAnalytics />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
