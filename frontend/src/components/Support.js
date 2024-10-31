import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Support.css';

function Support() {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [ticketData, setTicketData] = useState({
        subject: '',
        description: '',
        email: ''
    });

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const createTicket = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setSuccess(null);
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/create-ticket', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ticketData)
            });

            const data = await response.json();
            if (response.ok) {
                setSuccess('Support ticket created successfully. You will receive a confirmation email with your ticket details and status updates.');
                setTicketData({ subject: '', description: '', email: '' });
            } else {
                throw new Error(data.message || 'Failed to create ticket');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="support-container">
            <nav className="dashboard-nav">
                <div className="nav-logo">
                    <Link to="/dashboard">
                        <img src="/images/nexus-icon.png" alt="Nexus Icon" className="nav-logo-img" />
                    </Link>
                </div>
                <ul className="nav-links">
                    <li><Link to="/loan-application" className="nav-link">Personal Loan Application</Link></li>
                    <li><Link to="/about" className="nav-link">About Us</Link></li>
                    <li><Link to="/support" className="nav-link">Support</Link></li>
                    <li><button onClick={handleLogout} className="logout-button">Log Out</button></li>
                </ul>
            </nav>

            <div className="support-content">
                <h2>Help Desk</h2>
                <div className="support-description">
                    <p>Our dedicated support professionals are here to assist you with any questions or concerns you may have. Please provide detailed information to help us serve you better.</p>
                </div>
                
                <form onSubmit={createTicket} className="ticket-form">
                    <h3>Create Support Ticket</h3>
                    <input
                        type="text"
                        placeholder="Subject"
                        value={ticketData.subject}
                        onChange={(e) => setTicketData({...ticketData, subject: e.target.value})}
                        required
                    />
                    <textarea
                        placeholder="Description"
                        value={ticketData.description}
                        onChange={(e) => setTicketData({...ticketData, description: e.target.value})}
                        required
                    />
                    <input
                        type="email"
                        placeholder="Your Email"
                        value={ticketData.email}
                        onChange={(e) => setTicketData({...ticketData, email: e.target.value})}
                        required
                    />
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Creating...' : 'Create Ticket'}
                    </button>
                </form>
                
                {error && (
                    <div className="error-message">
                        Error: {error}
                    </div>
                )}
                
                {success && (
                    <div className="success-message">
                        {success}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Support;
