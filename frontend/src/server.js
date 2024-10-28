const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const { createTicket, fetchTickets } = require('./freshdeskService');

const app = express();
const PORT = 3000;

// Middleware to serve static files from the public folder
app.use(express.static(path.join(__dirname, '../public'))); // Adjusted path to point to the public folder
app.use(bodyParser.json());

// POST route to create a ticket
app.post('/api/tickets', async (req, res) => {
    const { subject, description } = req.body;
    try {
        const ticket = await createTicket(subject, description);
        res.status(200).json(ticket);
    } catch (error) {
        console.error('Error creating ticket:', error);
        res.status(500).send('Error creating ticket');
    }
});

// GET route to fetch tickets for IT support users
app.get('/api/tickets', async (req, res) => {
    try {
        const tickets = await fetchTickets();
        res.json(tickets);
    } catch (error) {
        console.error('Error fetching tickets:', error);
        res.status(500).send('Error fetching tickets');
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
