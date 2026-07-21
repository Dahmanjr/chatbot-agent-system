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
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - colourful & smart professional design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: linear-gradient(145deg, #0b0d14 0%, #14172b 50%, #0f1117 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    /* Hide Streamlit's default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ---------- SIDEBAR ---------- */
    .css-1d391kg, .css-1d391kg > div {
        background: rgba(15, 17, 23, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    .sidebar-content {
        padding: 28px 20px;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    }
    .sidebar-subtitle {
        font-size: 13px;
        color: #8b8fa7;
        margin-bottom: 28px;
        font-weight: 400;
    }
    .sidebar-divider {
        border-top: 1px solid rgba(139, 92, 246, 0.15);
        margin: 16px 0;
    }
    .sidebar-section-header {
        font-size: 11px;
        font-weight: 600;
        color: #7c7f9e;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 24px;
        margin-bottom: 8px;
    }
    .sidebar-item {
        padding: 10px 14px;
        border-radius: 10px;
        color: #c8cbe0;
        font-size: 14px;
        cursor: default;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 10px;
        border: 1px solid transparent;
    }
    .sidebar-item:hover {
        background: rgba(139, 92, 246, 0.1);
        border-color: rgba(139, 92, 246, 0.3);
        color: #ffffff;
        transform: translateX(4px);
    }
    .sidebar-item.active {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(96, 165, 250, 0.1));
        border-color: #8b5cf6;
        color: #ffffff;
        font-weight: 500;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.1);
    }
    .sidebar-recent {
        padding: 8px 14px;
        border-radius: 8px;
        color: #8b8fa7;
        font-size: 13px;
        cursor: default;
        transition: all 0.2s;
        border-left: 2px solid transparent;
    }
    .sidebar-recent:hover {
        background: rgba(139, 92, 246, 0.08);
        color: #d4d8f0;
        border-left-color: #8b5cf6;
    }

    /* ---------- MAIN AREA ---------- */
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
        border-bottom: 1px solid rgba(139, 92, 246, 0.15);
        margin-bottom: 12px;
    }
    .chat-header h1 {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 40px rgba(167, 139, 250, 0.15);
    }
    .chat-header p {
        color: #8b8fa7;
        font-size: 14px;
        margin: 4px 0 0 0;
        font-weight: 400;
    }

    /* Messages wrapper */
    .messages-wrapper {
        flex: 1;
        overflow-y: auto;
        padding: 12px 0 20px 0;
        display: flex;
        flex-direction: column;
        gap: 8px;
        scroll-behavior: smooth;
    }

    /* Greeting card - glass with shimmer */
    .greeting-card {
        background: rgba(26, 29, 43, 0.6);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 24px;
        padding: 32px 28px;
        margin: 16px 0 24px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    }
    .greeting-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(139, 92, 246, 0.05), transparent, rgba(96, 165, 250, 0.05), transparent);
        animation: shimmer 6s linear infinite;
        pointer-events: none;
    }
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .greeting-card h2 {
        color: #f0f0ff;
        font-size: 24px;
        font-weight: 600;
        margin: 0 0 8px 0;
        position: relative;
        z-index: 1;
    }
    .greeting-card p {
        color: #b0b4d0;
        font-size: 16px;
        margin: 0 0 22px 0;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }

    /* Suggestion chips - colourful */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 4px;
        position: relative;
        z-index: 1;
    }
    .chip-container .stButton button {
        background: rgba(139, 92, 246, 0.12);
        color: #d4d8f0;
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 30px;
        padding: 10px 22px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.25s ease;
        white-space: nowrap;
        width: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        backdrop-filter: blur(4px);
    }
    .chip-container .stButton button:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(96, 165, 250, 0.2));
        border-color: #8b5cf6;
        color: #ffffff;
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.25);
    }

    /* Chat bubbles - colourful */
    .user-bubble {
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6);
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 24px 24px 6px 24px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        width: fit-content;
        word-wrap: break-word;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
        font-size: 15px;
        line-height: 1.6;
        text-align: left;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .bot-bubble {
        background: rgba(26, 29, 43, 0.7);
        backdrop-filter: blur(8px);
        color: #e8ecf5;
        padding: 14px 20px;
        border-radius: 24px 24px 24px 6px;
        margin: 6px 0;
        max-width: 80%;
        width: fit-content;
        word-wrap: break-word;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.03);
        font-size: 15px;
        line-height: 1.6;
    }

    /* Input area - glowing */
    .input-area {
        position: sticky;
        bottom: 0;
        background: rgba(11, 13, 20, 0.8);
        backdrop-filter: blur(12px);
        padding: 14px 0 10px 0;
        border-top: 1px solid rgba(139, 92, 246, 0.15);
        margin-top: 8px;
        border-radius: 16px 16px 0 0;
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
        background: rgba(26, 29, 43, 0.7);
        color: #f0f0ff;
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 14px 20px;
        font-size: 15px;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
    }
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15), 0 0 30px rgba(139, 92, 246, 0.05);
    }
    .stTextInput > div > div > input::placeholder {
        color: #6b6f8a;
    }
    .send-btn button {
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 14px 32px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
        width: 100%;
        min-width: 80px;
        letter-spacing: 0.3px;
    }
    .send-btn button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 28px rgba(139, 92, 246, 0.45);
        background: linear-gradient(135deg, #7c3aed, #4f46e5, #2563eb);
    }
    .send-btn button:active {
        transform: translateY(0);
    }
    .input-hint {
        color: #6b6f8a;
        font-size: 12px;
        text-align: right;
        margin-top: 6px;
        padding-right: 4px;
    }

    /* Status bar - pulsing dot */
    .status-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px 0 0 0;
        color: #8b8fa7;
        font-size: 13px;
        border-top: 1px solid rgba(139, 92, 246, 0.1);
        margin-top: 6px;
        gap: 16px;
    }
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #8b5cf6;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 16px rgba(139, 92, 246, 0.6);
        animation: pulse-dot 1.8s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 16px rgba(139, 92, 246, 0.6); }
        50% { opacity: 0.6; transform: scale(0.85); box-shadow: 0 0 8px rgba(139, 92, 246, 0.2); }
    }
    .status-url {
        color: #6b6f8a;
        font-weight: 400;
    }
    .status-left {
        display: flex;
        align-items: center;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 12px 16px 12px;
        }
        .chat-header h1 {
            font-size: 24px;
        }
        .greeting-card {
            padding: 24px 18px;
        }
        .greeting-card h2 {
            font-size: 20px;
        }
        .greeting-card p {
            font-size: 15px;
        }
        .user-bubble, .bot-bubble {
            max-width: 90%;
            font-size: 14px;
            padding: 12px 16px;
        }
        .chip-container .stButton button {
            font-size: 13px;
            padding: 8px 16px;
        }
        .send-btn button {
            padding: 12px 18px;
            min-width: 60px;
            font-size: 14px;
        }
        .stTextInput > div > div > input {
            font-size: 14px;
            padding: 12px 16px;
        }
        .status-bar {
            font-size: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="sidebar-title">✨ AI Assistant</div>
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
    <h1>✨ AI Chatbot</h1>
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
        <h2>👋 Hello! I'm your AI assistant.</h2>
        <p>I'm ready to help you with questions, analysis, writing, and more.<br>
        What would you like to explore today?</p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions with colourful chips
    st.markdown('<div class="chip-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("🚀 How does this work?", key="suggest1"):
            st.session_state.messages.append({"role": "user", "content": "How does this work?"})
            with st.spinner("Thinking..."):
                answer = query("How does this work?")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col2:
        if st.button("📝 Summarize a topic", key="suggest2"):
            st.session_state.messages.append({"role": "user", "content": "Summarize a topic for me"})
            with st.spinner("Thinking..."):
                answer = query("Summarize a topic for me")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    with col3:
        if st.button("✍️ Help me write", key="suggest3"):
            st.session_state.messages.append({"role": "user", "content": "Help me write something"})
            with st.spinner("Thinking..."):
                answer = query("Help me write something")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Fourth suggestion centered
    col_extra = st.columns([1,1,1])
    with col_extra[1]:
        if st.button("💡 Answer a question", key="suggest4"):
            st.session_state.messages.append({"role": "user", "content": "Answer a question"})
            with st.spinner("Thinking..."):
                answer = query("Answer a question")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # close messages-wrapper

# ---------- INPUT AREA ----------
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
        send = st.button("Send 🚀", use_container_width=True)

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
