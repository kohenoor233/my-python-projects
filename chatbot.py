import nltk
import random
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.stem.lancaster import LancasterStemmer

# Download resources
nltk.download('punkt')
stemmer = LancasterStemmer()

# --- Define intents ---
intents = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["Hi", "Hey", "How are you", "Hello", "Good day"],
            "responses": ["Hello! How can I help you?", "Hi there!"]
        },
        {
            "tag": "order_status",
            "patterns": ["Where is my order", "Track my order", "Order status", "I want to know my order status"],
            "responses": ["Please provide your order number."]
        },
        {
            "tag": "change_address",
            "patterns": ["Change delivery address", "Update my address", "Wrong address", "I want to change my address"],
            "responses": ["Sorry, you can't change the address after the order is shipped. Please contact the courier."]
        },
        {
            "tag": "goodbye",
            "patterns": ["Bye", "See you", "Goodbye", "Exit"],
            "responses": ["Goodbye!", "Thanks for visiting. See you next time!"]
        },
        {
            "tag": "unknown",
            "patterns": [],
            "responses": ["I'm not sure I understand. Could you rephrase?"]
        }
    ]
}

# --- Train the ML model ---
X = []
y = []
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        X.append(pattern)
        y.append(intent["tag"])

def tokenize_and_stem(text):
    tokens = nltk.word_tokenize(text)
    return " ".join([stemmer.stem(word.lower()) for word in tokens])

X_stemmed = [tokenize_and_stem(sentence) for sentence in X]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X_stemmed)

model = LogisticRegression()
model.fit(X_vec, y)

# --- Predict intent and respond ---
def get_response(user_input):
    stemmed_input = tokenize_and_stem(user_input)
    input_vec = vectorizer.transform([stemmed_input])
    predicted_intent = model.predict(input_vec)[0]

    for intent in intents["intents"]:
        if intent["tag"] == predicted_intent:
            return random.choice(intent["responses"])
    return random.choice(intents["intents"][-1]["responses"])

# --- Build GUI with tkinter ---
def send_message():
    user_input = user_entry.get()
    if user_input.strip() == "":
        return
    chat_box.config(state='normal')
    chat_box.insert(tk.END, "You: " + user_input + "\n")
    response = get_response(user_input)
    chat_box.insert(tk.END, "Bot: " + response + "\n\n")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)
    user_entry.delete(0, tk.END)

# Initialize main window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("500x550")
root.resizable(False, False)

# Chat display area
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 12))
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User input field
user_entry = tk.Entry(root, font=("Arial", 14))
user_entry.pack(fill=tk.X, padx=10, pady=10)
user_entry.focus()

# Send button
send_button = tk.Button(root, text="Send", font=("Arial", 12), command=send_message)
send_button.pack(pady=(0, 10))

# Bind Enter key to send
root.bind('<Return>', lambda event=None: send_message())

# Start the GUI event loop
chat_box.config(state='normal')
chat_box.insert(tk.END, "Bot: Hello! I'm your assistant. How can I help?\n\n")
chat_box.config(state='disabled')
root.mainloop()
