// Establish WebSocket connection
const socket = new WebSocket('ws://localhost:8080');

// Real-Time Event Updates
const eventUpdates = document.getElementById('event-updates');

socket.addEventListener('message', function (event) {
  const data = JSON.parse(event.data);

  if (data.type === 'event-update') {
    const update = document.createElement('p');
    update.textContent = data.message;
    eventUpdates.appendChild(update);
  }

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
    chatInput.value = '';
  }
});

// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  document.body.classList.toggle('light-mode');
  
  // Toggle icon between sun and moon
  const icon = themeToggle.querySelector('i');
  icon.classList.toggle('fa-sun');
  icon.classList.toggle('fa-moon');
});
