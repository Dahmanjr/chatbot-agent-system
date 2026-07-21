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

# Custom CSS - professional & responsive
st.markdown("""
<style>
    /* Reset and base */
    .stApp {
        background-color: #0b0d14;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit's default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Sidebar styling */
    .css-1d391kg, .css-1d391kg > div {
        background-color: #0f1117;
        border-right: 1px solid #2a2d3a;
    }
    .sidebar-content {
        padding: 28px 20px;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.3px;
        margin-bottom: 2px;
    }
    .sidebar-subtitle {
        font-size: 13px;
        color: #6b7a8f;
        margin-bottom: 28px;
        font-weight: 400;
    }
    .sidebar-divider {
        border-top: 1px solid #2a2d3a;
        margin: 16px 0;
    }
    .sidebar-section-header {
        font-size: 11px;
        font-weight: 600;
        color: #5a6a7e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 24px;
        margin-bottom: 8px;
    }
    .sidebar-item {
        padding: 10px 14px;
        border-radius: 8px;
        color: #d1d9e8;
        font-size: 14px;
        cursor: default;
        transition: all 0.15s;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-item:hover {
        background: #1a1d2b;
        color: #ffffff;
    }
    .sidebar-item.active {
        background: #1e293b;
        color: #ffffff;
        font-weight: 500;
    }
    .sidebar-recent {
        padding: 8px 14px;
        border-radius: 6px;
        color: #8a9bb0;
        font-size: 13px;
        cursor: default;
        transition: background 0.15s;
    }
    .sidebar-recent:hover {
        background: #1a1d2b;
        color: #d1d9e8;
    }

    /* Main container */
    .main-container {
        max-width: 820px;
        margin: 0 auto;
        padding: 0 20px 20px 20px;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* Header */
    .chat-header {
        text-align: center;
        padding: 18px 0 8px 0;
        border-bottom: 1px solid #1f2232;
        margin-bottom: 12px;
    }
    .chat-header h1 {
        font-size: 26px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .chat-header p {
        color: #6b7a8f;
        font-size: 14px;
        margin: 4px 0 0 0;
        font-weight: 400;
    }

    /* Chat messages container - scrollable */
    .messages-wrapper {
        flex: 1;
        overflow-y: auto;
        padding: 12px 0 20px 0;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    /* Greeting card */
    .greeting-card {
        background: rgba(26, 29, 43, 0.7);
        backdrop-filter: blur(4px);
        border: 1px solid #2a2d3a;
        border-radius: 20px;
        padding: 32px 28px;
        margin: 16px 0 24px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .greeting-card h2 {
        color: #ffffff;
        font-size: 22px;
        font-weight: 500;
        margin: 0 0 8px 0;
    }
    .greeting-card p {
        color: #94a3b8;
        font-size: 16px;
        margin: 0 0 22px 0;
        line-height: 1.5;
    }

    /* Suggestion chips */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 4px;
    }
    .chip-container .stButton button {
        background: #1a1d2b;
        color: #d1d9e8;
        border: 1px solid #2a2d3a;
        border-radius: 30px;
        padding: 8px 20px;
        font-size: 14px;
        font-weight: 400;
        transition: all 0.2s;
        white-space: nowrap;
        width: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .chip-container .stButton button:hover {
        background: #2a2d3a;
        border-color: #3b405a;
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* Chat bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 20px 20px 6px 20px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        width: fit-content;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        font-size: 15px;
        line-height: 1.5;
        text-align: left;
    }
    .bot-bubble {
        background: #1a1d2b;
        color: #e2e8f0;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 6px;
        margin: 6px 0;
        max-width: 80%;
        width: fit-content;
        word-wrap: break-word;
        border: 1px solid #2a2d3a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-size: 15px;
        line-height: 1.5;
    }

    /* Input area - sticky bottom */
    .input-area {
        position: sticky;
        bottom: 0;
        background: #0b0d14;
        padding: 14px 0 10px 0;
        border-top: 1px solid #1f2232;
        margin-top: 8px;
    }
    .input-row {
        display: flex;
        align-items: flex-end;
        gap: 12px;
    }
    .input-row > div:first-child {
        flex: 1;
    }
    .stTextInput > div > div > input {
        background: #1a1d2b;
        color: #ffffff;
        border: 1px solid #2a2d3a;
        border-radius: 16px;
        padding: 14px 18px;
        font-size: 15px;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }
    .stTextInput > div > div > input::placeholder {
        color: #6b7a8f;
    }
    .send-btn button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 12px 28px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        width: 100%;
        min-width: 80px;
    }
    .send-btn button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    }
    .send-btn button:active {
        transform: translateY(0);
    }
    .input-hint {
        color: #5a6a7e;
        font-size: 12px;
        text-align: right;
        margin-top: 6px;
        padding-right: 4px;
    }

    /* Status bar */
    .status-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px 0 0 0;
        color: #6b7a8f;
        font-size: 13px;
        border-top: 1px solid #1f2232;
        margin-top: 6px;
        gap: 16px;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 8px rgba(34, 197, 94, 0.3);
    }
    .status-url {
        color: #5a6a7e;
        font-weight: 400;
    }
    .status-left {
        display: flex;
        align-items: center;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 12px 16px 12px;
        }
        .chat-header h1 {
            font-size: 22px;
        }
        .greeting-card {
            padding: 24px 18px;
        }
        .greeting-card h2 {
            font-size: 19px;
        }
        .greeting-card p {
            font-size: 15px;
        }
        .user-bubble, .bot-bubble {
            max-width: 90%;
            font-size: 14px;
            padding: 10px 14px;
        }
        .chip-container .stButton button {
            font-size: 13px;
            padding: 6px 16px;
        }
        .send-btn button {
            padding: 12px 18px;
            min-width: 60px;
            font-size: 14px;
        }
        .stTextInput > div > div > input {
            font-size: 14px;
            padding: 12px 14px;
        }
        .status-bar {
            font-size: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .sidebar-title {
            font-size: 18px;
        }
        .sidebar-content {
            padding: 20px 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">AI Assistant</div>
        <div class="sidebar-subtitle">Powered by Flowise</div>
        <div class="sidebar-divider"></div>
        <div style="margin-bottom: 4px;">
            <div class="sidebar-item active">💬 New Chat</div>
        </div>
        <div style="margin-bottom: 4px;">
            <div class="sidebar-item">🔍 Search History</div>
        </div>
        <div class="sidebar-section-header">RECENT</div>
        <div class="sidebar-recent">📎 Previous session</div>
        <div class="sidebar-recent">📎 Previous session</div>
        <div class="sidebar-recent">📎 Previous session</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN AREA ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <h1>🤖 AI Chatbot</h1>
    <p>Powered by Flowise</p>
</div>
""", unsafe_allow_html=True)

# Messages container
st.markdown('<div class="messages-wrapper">', unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# If no messages, show greeting + suggestions
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="greeting-card">
        <h2>Hello! I'm your AI assistant.</h2>
        <p>I'm ready to help you with questions, analysis, writing, and more.<br>
        What would you like to explore today?</p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions using columns for responsive layout
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("How does this work?", key="suggest1"):
            st.session_state.messages.append({"role": "user", "content": "How does this work?"})
            with st.spinner("Thinking..."):
                answer = query("How does this work?")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col2:
        if st.button("Summarize a topic", key="suggest2"):
            st.session_state.messages.append({"role": "user", "content": "Summarize a topic for me"})
            with st.spinner("Thinking..."):
                answer = query("Summarize a topic for me")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col3:
        if st.button("Help me write", key="suggest3"):
            st.session_state.messages.append({"role": "user", "content": "Help me write something"})
            with st.spinner("Thinking..."):
                answer = query("Help me write something")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    # Fourth suggestion as a standalone row
    col_extra = st.columns([1,1,1])
    with col_extra[1]:
        if st.button("Answer a question", key="suggest4"):
            st.session_state.messages.append({"role": "user", "content": "Answer a question"})
            with st.spinner("Thinking..."):
                answer = query("Answer a question")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # close messages-wrapper

# ---------- INPUT AREA (sticky) ----------
st.markdown('<div class="input-area">', unsafe_allow_html=True)
with st.container():
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

    if send and user_input.strip():
        question = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            answer = query(question)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    st.markdown('<div class="input-hint">Enter to send · Shift+Enter for new line</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- STATUS BAR ----------
st.markdown("""
<div class="status-bar">
    <span class="status-left"><span class="status-dot"></span>Agent online</span>
    <span class="status-url">localhost:3000</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-container
