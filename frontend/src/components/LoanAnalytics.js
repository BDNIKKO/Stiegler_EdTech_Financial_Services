import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoanAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:5000/api/loan-analytics', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => setAnalytics(data))
      .catch((error) => setError(error.message));
  }, []);

  if (error) return <p>{error}</p>;
  if (!analytics) return <p>Loading analytics...</p>;

  return (
    <div className="analytics-card">
      <h2>Loan Analytics</h2>
      <table>
        <tbody>
          <tr>
            <td>Total Applications:</td>
            <td>{analytics.total_applications}</td>
          </tr>
          <tr>
            <td>Approved Loans:</td>
            <td>{analytics.approved_count}</td>
          </tr>
          <tr>
            <td>Denied Loans:</td>
            <td>{analytics.denied_count}</td>
          </tr>
          <tr>
            <td>Approval Rate:</td>
            <td>{analytics.approval_rate.toFixed(2)}%</td>
          </tr>
          <tr>
            <td>Average Loan Amount:</td>
            <td>${analytics.avg_loan_amount.toFixed(2)}</td>
          </tr>
          <tr>
            <td>Last Updated:</td>
            <td>{new Date(analytics.last_updated).toLocaleString()}</td>
          </tr>
        </tbody>
      </table>
      <button onClick={() => navigate('/')}>Back to Home</button>
    </div>
  );
}

export default LoanAnalytics;
