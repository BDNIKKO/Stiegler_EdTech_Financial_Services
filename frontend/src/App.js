import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import HeroPage from './components/HeroPage';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import AboutUs from './components/AboutUs';
import Support from './components/Support';
import NavBar from './components/NavBar';

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("Form data being submitted: ", formData);

    try {
      const token = localStorage.getItem('token'); // Get JWT token from local storage

      if (!token) {
        setPrediction('Unauthorized. Please log in again.');
        navigate('/login'); // Redirect to login if token is missing
        return;
      }

      // Convert input values to numbers before submitting
      const numericFormData = {
        income: parseFloat(formData.income),
        loan_amount: parseFloat(formData.loan_amount),
        loan_term: parseFloat(formData.loan_term),
        employment_length: parseFloat(formData.employment_length)
      };

      if (Object.values(numericFormData).some(isNaN)) {
        setPrediction('Error: All input values must be valid numbers!');
        return;
      }

      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Pass token in Authorization header
        },
        body: JSON.stringify(numericFormData),
      });

      if (response.status === 401) {
        setPrediction('Unauthorized. Please log in again.');
        localStorage.removeItem('token'); // Remove invalid token
        navigate('/login'); // Redirect to login
      } else if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction); // Update the prediction state with the result
      } else {
        const errorData = await response.json();
        setPrediction(`Error: ${errorData.message || 'An error occurred while processing your request.'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setPrediction('An error occurred while processing your request.');
    }
  };

  return (
    <div>
      <h1>Personal Loan Application</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Income:</label>
          <input
            type="text"
            name="income"
            value={formData.income}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Loan Amount:</label>
          <input
            type="text"
            name="loan_amount"
            value={formData.loan_amount}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Loan Term (months or years):</label>
          <input
            type="text"
            name="loan_term"
            value={formData.loan_term}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Employment Length (years):</label>
          <input
            type="text"
            name="employment_length"
            value={formData.employment_length}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>

      {/* Display prediction result */}
      {prediction !== null && (
        <div>
          <h2>Prediction Result</h2>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<HeroPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/loan-application" element={<LoanApplication />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/support" element={<Support />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
