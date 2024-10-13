// Establish WebSocket connection
const socket = new WebSocket('ws://localhost:8080');

// Real-Time Event Updates
const eventUpdates = document.getElementById('event-updates');

socket.addEventListener('message', function (event) {
  const data = JSON.parse(event.data);

  // If the data is for event updates
  if (data.type === 'event-update') {
    const update = document.createElement('p');
    update.textContent = data.message;
    eventUpdates.appendChild(update);
  }

  // If the data is a chat message
  if (data.type === 'chat-message') {
    const chatMessages = document.getElementById('chat-messages');
    const message = document.createElement('p');
    message.textContent = data.username + ": " + data.message;
    chatMessages.appendChild(message);
  }
});

// Sending chat messages
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', function () {
  const message = chatInput.value;
  if (message) {
    socket.send(JSON.stringify({ type: 'chat-message', message: message }));
    chatInput.value = ''; // Clear input after sending
  }
});
