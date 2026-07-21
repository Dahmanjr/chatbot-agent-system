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
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling — Deep Dark Theme with Luminous Neon Accents
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main App Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #15102a 0%, #090d16 60%, #05070d 100%);
        color: #f8fafc;
    }

    /* Hide standard Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    /* Neon Gradient Brand Header */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }

    .brand-tag {
        font-size: 0.75rem;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(14, 165, 233, 0.12);
        padding: 0.3rem 0.7rem;
        border-radius: 9999px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }

    /* Welcome Section */
    .welcome-heading {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.75rem;
    }

    /* Neon Glowing Starter Buttons */
    div.stButton > button {
        width: 100%;
        background: rgba(22, 27, 46, 0.7) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.1rem !important;
        font-weight: 600 !important;
        font-size: 0.93rem !important;
        text-align: left !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        backdrop-filter: blur(10px);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(236, 72, 153, 0.25)) !important;
        border-color: #f43f5e !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(244, 63, 94, 0.35) !important;
    }

    /* Chat Messages - Dark Cards with Vivid Borders */
    [data-testid="stChatMessage"] {
        background: rgba(18, 22, 38, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
    }

    /* High-contrast crisp white body text */
    [data-testid="stChatMessage"] p {
        color: #f8fafc !important;
        font-size: 1rem !important;
        line-height: 1.65 !important;
        font-weight: 400 !important;
    }

    /* Distinctive User Message Border Accent */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: rgba(28, 25, 56, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.15);
    }

    /* Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 14px !important;
        border: 1.5px solid rgba(6, 182, 212, 0.4) !important;
        background-color: rgba(15, 20, 35, 0.95) !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.15) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #a855f7 !important;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.3) !important;
    }

    [data-testid="stChatInput"] input {
        font-size: 0.98rem !important;
        color: #f8fafc !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        background-color: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: #4ade80;
        font-size: 0.82rem;
        font-weight: 700;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2);
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #22c55e;
        box-shadow: 0 0 8px #22c55e;
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
    st.caption("**Engine:** Flowise Orchestrator")
    st.caption("**Theme:** Dark Neon High-Contrast")
    st.caption("**Status:** Operational")

# Main Header
st.markdown("""
<div class="brand-bar">
    <div class="brand-title">
        <span>⚡ AI Workspace</span>
    </div>
    <span class="brand-tag">v2.5 Ready</span>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Only displayed when there are no messages)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-heading">What are we exploring today?</div>
        <div class="welcome-sub">Choose a starter prompt or type your query below:</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🟣 Explain what this agent can do"):
            st.session_state.prompt_trigger = "Explain what this AI agent can do and how to best interact with it."
        if st.button("💗 Summarize a complex document or topic"):
            st.session_state.prompt_trigger = "Provide a clean framework for summarizing complex technical documents."

    with c2:
        if st.button("🔵 Give me a quick brainstorming technique"):
            st.session_state.prompt_trigger = "Share 3 highly effective techniques for brainstorming creative ideas."
        if st.button("🟢 Analyze technical architecture principles"):
            st.session_state.prompt_trigger = "Outline the key principles of reliable cloud infrastructure."

# Trigger pre-filled prompts
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Message History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle AI Response Generation
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Generating response..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Chat Input Component
if user_input := st.chat_input("Type your question or request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
