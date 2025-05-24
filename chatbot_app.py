import os
import ssl
import nltk
import random
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Fix SSL for NLTK downloads
ssl._create_default_https_context = ssl._create_unverified_context

# Download NLTK data
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Define chatbot intents
intents = [
    {"tag": "greeting", "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"], "responses": ["Hi there!", "Hello!", "Hey!", "I'm fine, thank you.", "Not much!"]},
    {"tag": "goodbye", "patterns": ["Bye", "See you later", "Goodbye", "Take care"], "responses": ["Goodbye!", "See you later!", "Take care!"]},
    {"tag": "thanks", "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"], "responses": ["You're welcome!", "No problem!", "Glad I could help!"]},
    {"tag": "about", "patterns": ["What can you do", "Who are you", "What are you", "What is your purpose"], "responses": ["I'm a chatbot.", "I assist with simple tasks.", "I'm here to help!"]},
    {"tag": "help", "patterns": ["Help", "I need help", "Can you help me", "What should I do"], "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?"]},
    {"tag": "age", "patterns": ["How old are you", "What's your age"], "responses": ["I don't have an age—I'm a bot!", "Age is just a number. Especially for me!"]},
    {"tag": "weather", "patterns": ["What's the weather like", "How's the weather today"], "responses": ["I can't provide real-time weather. Try a weather app!", "Check a weather site for live updates."]},
    {"tag": "budget", "patterns": ["How can I make a budget", "What's a good budgeting strategy", "How do I create a budget"], "responses": ["Start by tracking your income and expenses.", "Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings.", "Set goals, track spending, and adjust monthly."]},
    {"tag": "credit_score", "patterns": ["What is a credit score", "How do I check my credit score", "How can I improve my credit score"], "responses": ["A credit score shows your creditworthiness.", "You can check your score on sites like Credit Karma.", "Pay bills on time and reduce credit card usage."]}
]

# Train ML model
tags, patterns = [], []
for intent in intents:
    for pattern in intent["patterns"]:
        tags.append(intent["tag"])
        patterns.append(pattern)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)
y = tags

clf = LogisticRegression(random_state=0, max_iter=10000)
clf.fit(X, y)

# Chatbot response function
def get_bot_response(user_input):
    input_vec = vectorizer.transform([user_input])
    predicted_tag = clf.predict(input_vec)[0]
    for intent in intents:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"])
    return "Sorry, I didn't understand that."

# Streamlit UI
st.set_page_config(page_title="Massaburi Chatbot", layout="centered")
st.title(" Massaburi Chatbot😁")
st.markdown("Welcome! Ask me anything.")

# Session state to hold conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.chat_input("Type your message...")

# Process user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
