const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

// List of event updates 
const eventUpdates = [
  'Event A is starting in 30 minutes!',
  'Event B has been rescheduled to 2:00 PM.',
  'New event added: Hackathon at 5:00 PM!',
];

// Broadcast to all clients
function broadcast(data) {
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}

wss.on('connection', ws => {
  console.log('New client connected');

  // Send a welcome message with updates of event
  eventUpdates.forEach(update => {
    ws.send(JSON.stringify({ type: 'event-update', message: update }));
  });

  // Handle incoming messages from clients
  ws.on('message', message => {
    const data = JSON.parse(message);

    if (data.type === 'chat-message') {
      broadcast({ type: 'chat-message', message: data.message, username: 'User' });
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});
