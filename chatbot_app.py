import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Massaburi Chatbot", layout="centered")
st.title("Massaburi Chatbot😁")

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

def get_openai_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Chat input form at bottom
with st.form(key="chat_form"):
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.text_area("You:", label_visibility="collapsed", key="input_box")
    submitted = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_openai_response(st.session_state.messages)
            st.markdown(response)

    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Rerun app to refresh messages
    st.experimental_rerun()
