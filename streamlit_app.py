import streamlit as st
import requests

# Flowise Cloud API endpoint
API_URL = "https://cloud.flowiseai.com/api/v1/prediction/f01957c9-bd79-4f73-b455-3f7fe2496de3"


def query(question):
    """Send a question to the Flowise agent and return its response."""
    try:
        response = requests.post(API_URL, json={"question": question}, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("text") or result.get("answer") or str(result)
    except requests.exceptions.ConnectionError:
        return "Cannot connect to the Flowise server."
    except requests.exceptions.Timeout:
        return "Request timed out."
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"


# Page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="robot",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    .user-bubble {
        background: #2563eb;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        word-wrap: break-word;
    }
    .bot-bubble {
        background: #1e2130;
        color: #e2e8f0;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        word-wrap: break-word;
        border: 1px solid #2d3148;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 12px;
    }
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        width: 100%;
    }
    .stButton > button:hover { background-color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h2 style='text-align:center; color:white;'>🤖 AI Chatbot</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Powered by Flowise</p>", unsafe_allow_html=True)
st.divider()

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# Input area
st.divider()
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Type your message here...",
        label_visibility="collapsed",
        key="input"
    )

with col2:
    send = st.button("Send")

# Handle send
if send and user_input.strip():
    question = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("Thinking..."):
        answer = query(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
