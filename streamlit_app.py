import streamlit as st
import requests
from datetime import datetime

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
        return "Cannot reach the server. Please check your network connection."
    except requests.exceptions.Timeout:
        return "The request timed out. Please try asking again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

# Page Configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS directly mapping the HTML :root CSS variables & component styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
      --bg:        #0a0a0f;
      --surface:   #111118;
      --panel:     #16161f;
      --border:    #1f1f2e;
      --border-hi: #2e2e42;
      --accent:    #7c6af7;
      --accent-hi: #9b8dfb;
      --accent-lo: rgba(124, 106, 247, 0.12);
      --text:      #e2e2f0;
      --text-sub:  #7a7a9a;
      --text-dim:  #3a3a52;
      --user-bg:   #1d1b36;
      --user-bd:   #2e2a55;
      --err:       #f87171;
      --err-bg:    #1a0e0e;
      --green:     #34d399;
      --radius:    14px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    /* Hide standard Streamlit header & footer */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Main Container Padding and Max-Width */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 820px;
    }

    /* ── TOPBAR ── */
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 1rem;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--border);
    }

    .topbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .topbar-left h1 {
      font-size: 1rem;
      font-weight: 600;
      color: var(--text);
      margin: 0;
    }

    .model-chip {
      font-size: 0.68rem;
      font-family: 'JetBrains Mono', monospace;
      background: var(--accent-lo);
      color: var(--accent-hi);
      border: 1px solid rgba(124,106,247,0.2);
      padding: 3px 8px;
      border-radius: 20px;
      font-weight: 500;
    }

    /* ── DATE DIVIDER ── */
    .date-divider {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 16px 0 24px 0;
    }

    .date-divider::before,
    .date-divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    .date-divider span {
      font-size: 0.67rem;
      color: var(--text-dim);
      font-weight: 500;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    /* ── SUGGESTION CHIPS ── */
    div.stButton > button {
        background: var(--panel) !important;
        color: var(--text-sub) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 20px !important;
        font-size: 0.78rem !important;
        padding: 6px 14px !important;
        font-weight: 400 !important;
        transition: all 0.15s ease !important;
        text-align: center !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent-hi) !important;
        background: var(--accent-lo) !important;
    }

    /* ── MESSAGES & BUBBLES ── */
    [data-testid="stChatMessage"] {
        border-radius: var(--radius);
        padding: 12px 16px !important;
        margin-bottom: 0.75rem !important;
        font-size: 0.875rem !important;
        line-height: 1.65 !important;
    }

    /* Agent Message Styling */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        background: var(--panel) !important;
        border: 1px solid var(--border) !important;
        border-top-left-radius: 4px !important;
        color: var(--text) !important;
    }

    /* User Message Styling */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: var(--user-bg) !important;
        border: 1px solid var(--user-bd) !important;
        border-top-right-radius: 4px !important;
        color: var(--text) !important;
    }

    [data-testid="stChatMessage"] p {
        color: var(--text) !important;
        font-size: 0.875rem !important;
        line-height: 1.65 !important;
    }

    /* ── INPUT ZONE ── */
    [data-testid="stChatInput"] {
        background: var(--panel) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: var(--radius) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(124,106,247,0.1) !important;
    }

    [data-testid="stChatInput"] input {
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
    }

    [data-testid="stChatInput"] input::placeholder {
        color: var(--text-dim) !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    .sidebar-logo-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    .orb {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, #7c6af7, #a78bfa, #60a5fa);
      background-size: 200% 200%;
      animation: orbShift 4s ease infinite;
      flex-shrink: 0;
      box-shadow: 0 0 20px rgba(124,106,247,0.35);
    }

    @keyframes orbShift {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .sidebar-label {
      font-size: 0.65rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-dim);
      margin-top: 15px;
      margin-bottom: 8px;
    }

    .status-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      background: var(--panel);
      border-radius: 8px;
      border: 1px solid var(--border);
      margin-top: 20px;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 6px var(--green);
      animation: blink 2.5s ease infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }

    .status-badge p { font-size: 0.75rem; color: var(--text-sub); margin: 0; }
    .status-badge strong { color: var(--text); font-size: 0.75rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-box">
        <div class="orb"></div>
        <div>
            <h2 style="font-size: 0.88rem; font-weight: 600; color: var(--text); margin:0;">AI Assistant</h2>
            <span style="font-size: 0.7rem; color: var(--text-sub);">Powered by Flowise</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Workspace</div>', unsafe_allow_html=True)
    if st.button("💬 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-label">Recent</div>', unsafe_allow_html=True)
    st.caption("• Previous session")

    st.markdown("""
    <div class="status-badge">
        <div class="status-dot"></div>
        <div>
          <strong>Agent online</strong>
          <p>localhost:3000</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── TOPBAR ──
st.markdown("""
<div class="topbar">
  <div class="topbar-left">
    <h1>Chat</h1>
    <span class="model-chip">flowise-agent</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE INITIALIZATION ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# Date Divider
st.markdown('<div class="date-divider"><span>Today</span></div>', unsafe_allow_html=True)

# Default Welcome Message (when message history is empty)
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🔮"):
        st.markdown("""
        Hello! I'm your AI assistant. I'm ready to help you with questions, analysis, writing, and more.
        
        What would you like to explore today?
        """)

    # Suggestion Chips
    c1, c2 = st.columns(2)
    with c1:
        if st.button("How does this work?"):
            st.session_state.prompt_trigger = "How does this work?"
        if st.button("Summarize a topic for me"):
            st.session_state.prompt_trigger = "Summarize a topic for me"
    with c2:
        if st.button("Help me write something"):
            st.session_state.prompt_trigger = "Help me write something"
        if st.button("Answer a question"):
            st.session_state.prompt_trigger = "Answer a question"

# Handle Suggestion Chips Actions
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Message History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🔮"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Process Assistant Query Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🔮"):
        with st.spinner("Thinking..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Input Zone
if user_input := st.chat_input("Message the assistant…"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
