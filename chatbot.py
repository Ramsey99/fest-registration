import os
import openai
import taipy

# Initialize OpenAI client with API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create a Taipy GUI
gui = taipy.get_gui()

# Define the chatbot interface
page = """
<|{conversation}|table|show_all|width=100%|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

# Function to send messages and handle responses
def send_message(state: taipy.State) -> None:
    # Prepare the conversation context
    user_message = state.current_user_message.strip()
    if user_message:
        # Append user message to the context
        state.context += f"Human: {user_message}\nAI:"
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": state.context}]
        )
        
        # Extract the AI's response
        ai_message = response['choices'][0]['message']['content'].strip()
        
        # Update the conversation state
        state.context += f"{ai_message}\n"
        state.conversation.append({"Human": user_message, "AI": ai_message})
        
        # Clear the input field for the next message
        state.current_user_message = ""

# Run the Taipy application
if __name__ == "__main__":
    gui.run(dark_mode=True, title="Fest Registration Chatbot", page=page)