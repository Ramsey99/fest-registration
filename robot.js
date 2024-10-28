const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");

let userMessage;
const API_KEY = "AIzaSyCXzYwcXFz-4jpv1Yux7bvEvLOxWf4P1N8"; // Ensure this is a valid key

// Function to create chat list item
const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent = className === "outgoing" 
    ? `<p></p>` 
    : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
};

// Function to generate response from the API
const generateResponse = (incomingChatLi) => {
  const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
  const messageElement = incomingChatLi.querySelector("p");

  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
      contents: [{ 
        role: "user", 
        parts: [{ text: userMessage }] 
      }] 
    }),
  };
  fetch(API_URL, requestOptions)
    .then(res => res.json())
    .then(data => {
        // Assuming response contains 'content' and directly includes the text
        messageElement.textContent = data.candidates[0].content.parts[0].text;
      
    }).catch(() => {
      messageElement.textContent = "Oops! Something went wrong, please try again.";
    })
    .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};

// Handle user chat
const handleChat = () => {
  userMessage = chatInput.value.trim();
  if (!userMessage) return;
  
  chatInput.value = ""; // Clear input field
  
  // Append outgoing user message
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  // Simulate a response from the chatbot
  setTimeout(() => {
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 600);
};

// Adjust the height of the input textarea based on its content
chatInput.addEventListener("input", () => {
  chatInput.style.height = "auto";
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Send message on pressing Enter key
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { // Shift+Enter for new line
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn.addEventListener("click", handleChat);
chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
