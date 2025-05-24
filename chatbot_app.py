import streamlit as st
from openai import OpenAI
import random

# Your fallback intents
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
    # Add more intents if needed
]

def fallback_response(user_input):
    user_input_lower = user_input.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input_lower:
                return random.choice(intent["responses"])
    return "Sorry, I didn't understand that."

# Initialize OpenAI client using your Streamlit secret key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

# Initialize session state messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Massaburi, your friendly chatbot. Ask me anything!"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def get_openai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        err_str = str(e).lower()
        if "rate limit" in err_str or "ratelimit" in err_str or "too many requests" in err_str:
            # Rate limit reached -> fallback
            user_message = messages[-1]["content"]
            return "⚠️ (Fallback mode) " + fallback_response(user_message)
        else:
            return "⚠️ Sorry, something went wrong. Please try again later."

# Use Streamlit built-in chat input widget
user_input = st.chat_input("You:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show assistant message with spinner while waiting
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_openai_response(st.session_state.messages)
            st.markdown(response)

    # Append assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
