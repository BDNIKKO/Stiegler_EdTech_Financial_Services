const axios = require('axios');

const freshdeskApiKey = 'BKLJtkXkZ2dA8W4gaW';
const freshdeskDomain = 'stiegler.freshdesk.com';

// Create an axios instance for Freshdesk API
const freshdeskApi = axios.create({
    baseURL: `https://${freshdeskDomain}/api/v2`,
    headers: {
        'Authorization': `Basic ${Buffer.from(freshdeskApiKey + ':X').toString('base64')}`,
        'Content-Type': 'application/json'
    }
});

// Create a ticket
const createTicket = async (subject, description) => {
    try {
        const response = await freshdeskApi.post('/tickets', {
            subject,
            description,
            email: 'user@example.com', // Add email of the user creating the ticket
            priority: 1,
            status: 2
        });
        return response.data;
    } catch (error) {
        console.error('Error creating ticket:', error);
        throw error;
    }
};

// Fetch all tickets (for IT support users)
const fetchTickets = async () => {
    try {
        const response = await freshdeskApi.get('/tickets');
        return response.data;
    } catch (error) {
        console.error('Error fetching tickets:', error);
        throw error;
    }
};

module.exports = { createTicket, fetchTickets };
