import streamlit as st
import openai

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="Massaburi Chatbot", layout="centered")
st.title("Massaburi Chatbot😁")

# Custom CSS for ChatGPT-style input
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

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Massaburi, your friendly chatbot. Ask me anything!"}
    ]

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# GPT-based response function
def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use gpt-4 if available
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Custom input area
with st.form(key="chat_form"):
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.text_area("You:", label_visibility="collapsed", key="input_box")
    submitted = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_openai_response(st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.experimental_rerun()
