from flask import Flask, render_template, request
import google.generativeai as palm
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment variable
palm_api_key = os.environ["PALM_API_KEY"]

# Configure the PaLM API to use the API key
palm.configure(api_key=palm_api_key)

# Set up Flask App
app = Flask(__name__)

# Define the home page route
@app.route("/")
def home():
    return render_template("index.html")


# Define the chatbot route
@app.route("/chatbot", methods=["POST"])
def chatbot():
  # Get the message input from the user
  user_input = request.form["message"]

  models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
  model = models[0].name

  # Use the PaLM API to generate a response
  prompt = f"User: {user_input} \nPaLM Bot: "

  # Generate the response
  response = palm.generate_text(
    model=model,
    prompt=prompt,
    stop_sequences=None,
    temperature=0,
    max_output_tokens=100
  )

  # Get the bot's response
  bot_response = response.result

  # Add the user input and bot response to the chat history
  chat_history = []
  chat_history.append(f"User: {user_input}\nPaLM Bot: {bot_response}")

  # Render the Chatbot template with the response text
  return render_template(
    "chatbot.html",
    user_input=user_input,
    bot_response=bot_response,
    chat_history=chat_history,
  )

if __name__ == "__main__":
  app.run(debug=True)
