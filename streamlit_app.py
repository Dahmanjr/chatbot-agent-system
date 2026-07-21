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
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0f1117;
    }
    /* Sidebar */
    .css-1d391kg, .css-1d391kg > div {
        background-color: #0f1117;
        border-right: 1px solid #2d3148;
    }
    .sidebar-content {
        padding: 20px 16px;
    }
    .sidebar-title {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .sidebar-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 24px;
    }
    .sidebar-section-header {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 0.5px;
        margin-top: 20px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .sidebar-item {
        padding: 8px 12px;
        border-radius: 8px;
        color: #e2e8f0;
        cursor: default;
        transition: background 0.2s;
    }
    .sidebar-item:hover {
        background: #1e2130;
    }
    .sidebar-item.active {
        background: #1e293b;
        color: #ffffff;
    }
    .sidebar-recent {
        padding: 8px 12px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 14px;
        cursor: default;
    }
    .sidebar-recent:hover {
        background: #1e2130;
    }

    /* Main chat area */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    .chat-header {
        text-align: center;
        padding: 10px 0 4px 0;
    }
    .chat-header h1 {
        font-size: 28px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }
    .chat-header p {
        color: #94a3b8;
        font-size: 14px;
        margin: 4px 0 0 0;
    }
    .divider {
        border-top: 1px solid #2d3148;
        margin: 16px 0;
    }

    /* Greeting area */
    .greeting {
        background: #1a1d2b;
        border-radius: 16px;
        padding: 32px 28px;
        margin: 20px 0;
        border: 1px solid #2d3148;
    }
    .greeting h2 {
        color: #ffffff;
        font-size: 22px;
        font-weight: 500;
        margin: 0 0 8px 0;
    }
    .greeting p {
        color: #94a3b8;
        font-size: 16px;
        margin: 0 0 20px 0;
    }

    /* Suggestion chips */
    .suggestion-container {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    .stButton button {
        background-color: #1e2130;
        color: #e2e8f0;
        border: 1px solid #2d3148;
        border-radius: 20px;
        padding: 8px 18px;
        font-size: 14px;
        transition: all 0.2s;
        white-space: nowrap;
    }
    .stButton button:hover {
        background-color: #2d3148;
        border-color: #3b405a;
        color: #ffffff;
    }

    /* Chat bubbles */
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

    /* Input area */
    .input-container {
        position: sticky;
        bottom: 0;
        background: #0f1117;
        padding: 16px 0;
        border-top: 1px solid #2d3148;
        margin-top: 20px;
    }
    .input-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .input-row > div:first-child {
        flex: 1;
    }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
        border: 1px solid #2d3148;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563eb;
        box-shadow: none;
    }
    .send-button button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 15px;
        font-weight: 500;
        transition: background 0.2s;
        width: 100%;
    }
    .send-button button:hover {
        background-color: #1d4ed8;
    }
    .input-hint {
        color: #64748b;
        font-size: 12px;
        margin-top: 4px;
        text-align: right;
    }

    /* Footer status */
    .status-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 8px 0;
        color: #94a3b8;
        font-size: 13px;
        border-top: 1px solid #2d3148;
        margin-top: 12px;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-url {
        color: #64748b;
        margin-left: 4px;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">AI Assistant</div>
        <div class="sidebar-subtitle">Powered by Flowise</div>
        <div class="divider"></div>
        <div style="margin-bottom: 8px;">
            <div class="sidebar-item active">💬 New Chat</div>
        </div>
        <div style="margin-bottom: 4px;">
            <div class="sidebar-item">🔍 Search History</div>
        </div>
        <div class="sidebar-section-header">RECENT</div>
        <div class="sidebar-recent">📎 Previous session</div>
        <div class="sidebar-recent">📎 Previous session</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN CHAT AREA ----------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <h1>🤖 AI Chatbot</h1>
    <p>Powered by Flowise</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# If no messages yet, show greeting with suggestions
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="greeting">
        <h2>Hello! I'm your AI assistant.</h2>
        <p>I'm ready to help you with questions, analysis, writing, and more.<br>
        What would you like to explore today?</p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("How does this work?", key="suggest1"):
            st.session_state.messages.append({"role": "user", "content": "How does this work?"})
            with st.spinner("Thinking..."):
                answer = query("How does this work?")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col2:
        if st.button("Summarize a topic for me", key="suggest2"):
            st.session_state.messages.append({"role": "user", "content": "Summarize a topic for me"})
            with st.spinner("Thinking..."):
                answer = query("Summarize a topic for me")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col3:
        if st.button("Help me write something", key="suggest3"):
            st.session_state.messages.append({"role": "user", "content": "Help me write something"})
            with st.spinner("Thinking..."):
                answer = query("Help me write something")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    # Additional suggestion "Answer a question"
    if st.button("Answer a question", key="suggest4"):
        st.session_state.messages.append({"role": "user", "content": "Answer a question"})
        with st.spinner("Thinking..."):
            answer = query("Answer a question")
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# ---------- INPUT AREA ----------
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.container():
    # Use columns for input + send button
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="user_input"
        )
    with col_send:
        send = st.button("Send", use_container_width=True)

    # Handle send button or Enter key (via text_input's on_change we can't easily, but we use send)
    if send and user_input.strip():
        question = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            answer = query(question)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    # Hint text
    st.markdown('<div class="input-hint">Enter to send &nbsp;·&nbsp; Shift+Enter for new line</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- STATUS BAR ----------
st.markdown("""
<div class="status-bar">
    <span><span class="status-dot"></span>Agent online</span>
    <span class="status-url">localhost:3000</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close chat-container
