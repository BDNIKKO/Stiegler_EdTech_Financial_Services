import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import HeroPage from './components/HeroPage'; // Assuming HeroPage.js is in components folder
import LoginForm from './components/LoginForm'; // Assuming LoginForm.js is created in components folder
import RegisterForm from './components/RegisterForm'; // Assuming RegisterForm.js is created in components folder

function LoanApplication() {
  // State to hold the form data
  const [formData, setFormData] = useState({
    income: '',
    loan_amount: '',
    loan_term: '',
    employment_length: ''
  });

  // State to hold the prediction result from the backend
  const [prediction, setPrediction] = useState(null);

  // Handle form data changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Log the form data to the console
    console.log("Form data being submitted: ", formData);

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setPrediction(data.prediction); // Update the prediction state with the result
    } catch (error) {
      console.error('Error:', error);
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
          <p>{prediction === 'Approved' ? 'Loan Approved' : 'Loan Denied'}</p>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HeroPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/loan-application" element={<LoanApplication />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
