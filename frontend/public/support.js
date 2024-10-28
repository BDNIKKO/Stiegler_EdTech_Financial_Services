// Simulated user role (this would come from your backend)
const userRole = 'regular_user'; // Change to 'it_support' for IT staff

// Show/hide IT support tab based on role
window.onload = function() {
    if (userRole === 'it_support') {
        document.getElementById('itSupportTab').classList.remove('hidden');
        fetchTickets();
    }
};

// Handle form submission to create a ticket
document.getElementById('ticketForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const subject = document.getElementById('subject').value;
    const description = document.getElementById('description').value;
    
    // Send the ticket to the backend (Freshdesk API)
    const response = await fetch('/api/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject, description })
    });
    
    if (response.ok) {
        alert('Ticket submitted successfully!');
        document.getElementById('ticketForm').reset();
    } else {
        alert('Error submitting ticket');
    }
});

// Function to fetch and display tickets (for IT support users)
async function fetchTickets() {
    const response = await fetch('/api/tickets');
    const tickets = await response.json();
    
    const ticketList = document.getElementById('ticketList');
    ticketList.innerHTML = ''; // Clear previous list
    
    tickets.forEach(ticket => {
        const li = document.createElement('li');
        li.innerText = `Ticket #${ticket.id}: ${ticket.subject}`;
        ticketList.appendChild(li);
    });
}
