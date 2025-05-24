import streamlit as st
import random

# ---- Chatbot Intents ----
intents = [
    {
        "tag": "greeting",
        "patterns": ["hi", "hello", "hey", "how are you", "what's up"],
        "responses": ["Hi there!", "Hello!", "Hey!", "I'm fine, thank you.", "Not much!"]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "see you later", "goodbye", "take care"],
        "responses": ["Goodbye!", "See you later!", "Take care!"]
    },
    {
        "tag": "thanks",
        "patterns": ["thank you", "thanks", "thanks a lot", "i appreciate it"],
        "responses": ["You're welcome!", "No problem!", "Glad I could help!"]
    },
    {
        "tag": "about",
        "patterns": ["what can you do", "who are you", "what are you", "what is your purpose"],
        "responses": ["I'm a chatbot.", "I assist with simple tasks.", "I'm here to help!"]
    },
    {
        "tag": "help",
        "patterns": ["help", "i need help", "can you help me", "what should i do"],
        "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?"]
    },
    {
        "tag": "age",
        "patterns": ["how old are you", "what's your age"],
        "responses": ["I don't have an age—I'm a bot!", "Age is just a number. Especially for me!"]
    },
    {
        "tag": "weather",
        "patterns": ["what's the weather like", "how's the weather today"],
        "responses": ["I can't provide real-time weather. Try a weather app!", "Check a weather site for live updates."]
    },
    {
        "tag": "budget",
        "patterns": ["how can i make a budget", "what's a good budgeting strategy", "how do i create a budget"],
        "responses": [
            "Start by tracking your income and expenses.",
            "Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings.",
            "Set goals, track spending, and adjust monthly."
        ]
    },
    {
        "tag": "credit_score",
        "patterns": ["what is a credit score", "how do i check my credit score", "how can i improve my credit score"],
        "responses": [
            "A credit score shows your creditworthiness.",
            "You can check your score on sites like Credit Karma.",
            "Pay bills on time and reduce credit card usage."
        ]
    }
]

# ---- Fallback Response Logic ----
def get_response(user_input):
    user_input = user_input.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return random.choice(intent["responses"])
    return "Sorry, I didn't understand that."

# ---- Streamlit UI Setup ----
st.set_page_config(page_title="Massaburi Chatbot", layout="centered")
st.title("Massaburi Chatbot 😁")

# Hide Streamlit branding, menu, and footer
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-bottom: 150px;}
    </style>
""", unsafe_allow_html=True)

# ---- Chat State ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Massaburi, your friendly chatbot. Ask me anything!"}
    ]

# ---- Display Chat History ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat Input ----
user_input = st.chat_input("Say something...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    response = get_response(user_input)

    # Display bot response
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
