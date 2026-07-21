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
        return "Unable to connect to the assistant service. Please check your network."
    except requests.exceptions.Timeout:
        return "The request timed out. Please try asking again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

# Page Configuration
st.set_page_config(
    page_title="AI Workspace",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling — Slate & Crisp Ice-Blue Minimalist Theme
st.markdown("""
<style>
    /* Font & Base Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Hide standard Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    /* Top Brand Bar */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }

    .brand-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .brand-tag {
        font-size: 0.75rem;
        font-weight: 600;
        color: #0284c7;
        background: #e0f2fe;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        border: 1px solid #bae6fd;
    }

    /* Starter Cards / Prompts Grid */
    .welcome-box {
        margin-bottom: 2rem;
    }

    .welcome-heading {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }

    /* Custom Prompt Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.85rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        text-align: left !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
    }

    div.stButton > button:hover {
        background-color: #f0f9ff !important;
        border-color: #38bdf8 !important;
        color: #0284c7 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px -2px rgba(56, 189, 248, 0.15) !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
    }

    [data-testid="stChatMessage"] p {
        color: #0f172a !important; /* Pure high contrast slate for text */
        font-size: 0.98rem !important;
        line-height: 1.65 !important;
        font-weight: 400 !important;
    }

    /* User Message Styling Accent */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background-color: #f8fafc;
        border-color: #cbd5e1;
    }

    /* Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 14px !important;
        border: 1.5px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #0284c7 !important;
    }

    [data-testid="stChatInput"] input {
        font-size: 0.95rem !important;
        color: #0f172a !important;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Controls")
    
    st.markdown('<div class="status-pill"><div class="status-dot"></div> Agent Online</div>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("✨ Clear Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-section-title">System Specs</div>', unsafe_allow_html=True)
    st.caption("**Model Engine:** Flowise Orchestrator")
    st.caption("**Response Latency:** Dynamic (<1s)")
    st.caption("**UI State:** High-Contrast Mode")

# Main Header
st.markdown("""
<div class="brand-bar">
    <div class="brand-title">
        <span>✦ Assistant Workspace</span>
    </div>
    <span class="brand-tag">v2.4 Ready</span>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Only displayed when there are no messages)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-heading">How can I assist you today?</div>
        <div class="welcome-sub">Ask a complex question, summarize concepts, or choose a prompt to start:</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💡 Explain what this agent can do"):
            st.session_state.prompt_trigger = "Explain what this AI agent can do and how to best interact with it."
        if st.button("📝 Summarize a complex document or topic"):
            st.session_state.prompt_trigger = "Provide a clean framework for summarizing complex technical documents."

    with c2:
        if st.button("⚡ Give me a quick brainstorming technique"):
            st.session_state.prompt_trigger = "Share 3 highly effective techniques for brainstorming creative ideas."
        if st.button("🔍 Analyze technical architecture principles"):
            st.session_state.prompt_trigger = "Outline the key principles of reliable cloud infrastructure."

# Trigger pre-filled prompts
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Message History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✦"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle AI Response Generation
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="✦"):
        with st.spinner("Generating response..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Chat Input Component
if user_input := st.chat_input("Type your question or request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
