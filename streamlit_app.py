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
    initial_sidebar_state="auto"
)

# Custom CSS matching the dark theme with Mobile & High-Contrast Adjustments
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
      --bg:        #0a0a0f;
      --surface:   #111118;
      --panel:     #161622;
      --border:    #242436;
      --border-hi: #3b3b54;
      --accent:    #7c6af7;
      --accent-hi: #a79afb;
      --accent-lo: rgba(124, 106, 247, 0.18);
      --text:      #f0f0f8;
      --text-sub:  #a0a0c0;
      --text-dim:  #626282;
      --user-bg:   #211d42;
      --user-bd:   #38326a;
      --green:     #34d399;
      --radius:    14px;
    }

    /* Force dark background across all containers */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* Hide standard Streamlit header & footer elements */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stSidebarNav"] {
        visibility: hidden;
        display: none;
    }

    /* Main Container Layout - Mobile Optimized */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 820px;
    }

    /* ── TOPBAR ── */
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 0.8rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--border);
    }

    .topbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .topbar-left h1 {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text);
      margin: 0;
    }

    .model-chip {
      font-size: 0.7rem;
      font-family: 'JetBrains Mono', monospace;
      background: var(--accent-lo);
      color: var(--accent-hi);
      border: 1px solid rgba(124,106,247,0.3);
      padding: 3px 8px;
      border-radius: 20px;
      font-weight: 500;
    }

    /* ── DATE DIVIDER ── */
    .date-divider {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 12px 0 20px 0;
    }

    .date-divider::before,
    .date-divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    .date-divider span {
      font-size: 0.68rem;
      color: var(--text-sub);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    /* ── SUGGESTION CHIPS ── */
    div.stButton > button {
        background: var(--panel) !important;
        color: var(--text) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        padding: 8px 14px !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        text-align: center !important;
        width: 100% !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    div.stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent-hi) !important;
        background: var(--accent-lo) !important;
    }

    /* ── MESSAGES & BUBBLES (HIGH CONTRAST FIX) ── */
    [data-testid="stChatMessage"] {
        border-radius: var(--radius) !important;
        padding: 14px 18px !important;
        margin-bottom: 1rem !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* Agent Message Styling */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        background: var(--panel) !important;
        border: 1px solid var(--border-hi) !important;
        border-top-left-radius: 4px !important;
        color: #ffffff !important;
    }

    /* User Message Styling */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: var(--user-bg) !important;
        border: 1px solid var(--user-bd) !important;
        border-top-right-radius: 4px !important;
        color: #ffffff !important;
    }

    /* Text Legibility inside Chat Messages */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: var(--text) !important;
        font-size: 0.93rem !important;
        line-height: 1.6 !important;
    }

    [data-testid="stChatMessage"] code {
        background: rgba(0, 0, 0, 0.3) !important;
        color: var(--accent-hi) !important;
        border-radius: 4px;
        padding: 2px 6px;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ── CHAT INPUT AREA (MOBILE STICKY FIX) ── */
    [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background-color: var(--bg) !important;
    }

    [data-testid="stChatInput"] {
        background-color: var(--panel) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: var(--radius) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(124,106,247,0.2) !important;
    }

    [data-testid="stChatInput"] textarea, 
    [data-testid="stChatInput"] input {
        color: #ffffff !important;
        background-color: transparent !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.93rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {
        color: var(--text-sub) !important;
    }

    /* Send Button inside Input */
    [data-testid="stChatInput"] button {
        background-color: var(--accent) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }

    .sidebar-logo-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 16px;
        margin-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    .orb {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background: linear-gradient(135deg, #7c6af7, #a78bfa, #60a5fa);
      background-size: 200% 200%;
      animation: orbShift 4s ease infinite;
      flex-shrink: 0;
      box-shadow: 0 0 16px rgba(124,106,247,0.4);
    }

    @keyframes orbShift {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .sidebar-label {
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-sub);
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

    /* ── MOBILE SPECIFIC RESPONSIVE BREAKPOINTS ── */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 0.5rem !important;
        }

        [data-testid="stChatMessage"] {
            padding: 10px 14px !important;
            font-size: 0.88rem !important;
        }

        div.stButton > button {
            font-size: 0.78rem !important;
            padding: 6px 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-box">
        <div class="orb"></div>
        <div>
            <h2 style="font-size: 0.9rem; font-weight: 600; color: var(--text); margin:0;">AI Assistant</h2>
            <span style="font-size: 0.72rem; color: var(--text-sub);">Powered by Flowise</span>
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

    # Suggestion Chips (Adaptive Grid)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("How does this work?", use_container_width=True):
            st.session_state.prompt_trigger = "How does this work?"
        if st.button("Summarize a topic for me", use_container_width=True):
            st.session_state.prompt_trigger = "Summarize a topic for me"
    with c2:
        if st.button("Help me write something", use_container_width=True):
            st.session_state.prompt_trigger = "Help me write something"
        if st.button("Answer a question", use_container_width=True):
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
