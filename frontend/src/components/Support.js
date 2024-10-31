import React, { useState } from 'react';
import './Support.css';

function Support() {
    const [testResult, setTestResult] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [ticketData, setTicketData] = useState({
        subject: '',
        description: '',
        email: ''
    });

    const testConnection = async () => {
        setIsLoading(true);
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/test-freshdesk', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();
            setTestResult(data);
            console.log('Connection test result:', data);
        } catch (err) {
            setError(err.message);
            console.error('Connection test error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const createTicket = async (e) => {
        e.preventDefault();
        setIsLoading(true);
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
                alert('Ticket created successfully!');
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
            <h2>Support System</h2>
            
            <button 
                onClick={testConnection}
                disabled={isLoading}
            >
                {isLoading ? 'Testing...' : 'Test Connection'}
            </button>
            
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
            
            {testResult && (
                <div className="test-results">
                    <h3>Test Results:</h3>
                    <ul>
                        <li>Database Connected: {testResult.container_status.db_connected ? '✅' : '❌'}</li>
                        <li>Freshdesk Connected: {testResult.container_status.freshdesk_connected ? '✅' : '❌'}</li>
                        <li>Freshdesk Status: {testResult.freshdesk_status}</li>
                    </ul>
                </div>
            )}
            
            {error && (
                <div className="error-message">
                    Error: {error}
                </div>
            )}
        </div>
    );
}

export default Support;
