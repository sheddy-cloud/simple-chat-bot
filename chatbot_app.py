import streamlit as st
import random

# Define chatbot intents
intents = [
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"],
        "responses": ["Hi there!", "Hello!", "Hey!", "I'm fine, thank you.", "Not much!"]
    },
    {
        "tag": "goodbye",
        "patterns": ["Bye", "See you later", "Goodbye", "Take care"],
        "responses": ["Goodbye!", "See you later!", "Take care!"]
    },
    {
        "tag": "thanks",
        "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"],
        "responses": ["You're welcome!", "No problem!", "Glad I could help!"]
    },
    {
        "tag": "about",
        "patterns": ["What can you do", "Who are you", "What are you", "What is your purpose"],
        "responses": ["I'm a chatbot.", "I assist with simple tasks.", "I'm here to help!"]
    },
    {
        "tag": "help",
        "patterns": ["Help", "I need help", "Can you help me", "What should I do"],
        "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?"]
    },
    {
        "tag": "age",
        "patterns": ["How old are you", "What's your age"],
        "responses": ["I don't have an age—I'm a bot!", "Age is just a number. Especially for me!"]
    },
    {
        "tag": "weather",
        "patterns": ["What's the weather like", "How's the weather today"],
        "responses": ["I can't provide real-time weather. Try a weather app!", "Check a weather site for live updates."]
    },
    {
        "tag": "budget",
        "patterns": ["How can I make a budget", "What's a good budgeting strategy", "How do I create a budget"],
        "responses": [
            "Start by tracking your income and expenses.",
            "Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings.",
            "Set goals, track spending, and adjust monthly."
        ]
    },
    {
        "tag": "credit_score",
        "patterns": ["What is a credit score", "How do I check my credit score", "How can I improve my credit score"],
        "responses": [
            "A credit score shows your creditworthiness.",
            "You can check your score on sites like Credit Karma.",
            "Pay bills on time and reduce credit card usage."
        ]
    }
]

def fallback_response(user_input):
    user_input_lower = user_input.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input_lower:
                return random.choice(intent["responses"])
    return "Sorry, I didn't understand that."

st.set_page_config(page_title="Massaburi Chatbot", layout="centered")
st.title("Massaburi Chatbot😁")
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# CSS for chat input like ChatGPT
st.markdown("""
    <style>
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 12px;
        background-color: white;
        border-top: 1px solid #eee;
        z-index: 9999;
    }
    .chat-input-container textarea {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border-radius: 10px;
        border: 1px solid #ccc;
        resize: none;
        height: 60px;
    }
    .block-container {
        padding-bottom: 120px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Massaburi, your friendly chatbot. Ask me anything!"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input form at bottom
with st.form(key="chat_form"):
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.text_area("You:", label_visibility="collapsed", key="input_box")
    submitted = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get fallback chatbot response
    response = fallback_response(user_input)

    # Show chatbot response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Rerun to update UI
    st.experimental_rerun()
