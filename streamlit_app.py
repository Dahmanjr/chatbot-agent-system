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
        return "Unable to connect to the assistant service. Please check your connection."
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

# Custom CSS — Executive Professional Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    /* Executive Dark Obsidian Canvas */
    .stApp {
        background-color: #090c10;
        color: #f8fafc;
    }

    /* Hide standard Streamlit header & footer */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Main Container Width & Centering */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 860px;
    }

    /* Professional Top Navigation Bar */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #1e293b;
    }

    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .brand-title span {
        color: #38bdf8;
    }

    .brand-tag {
        font-size: 0.75rem;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.08);
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }

    /* Welcome Header Section */
    .welcome-heading {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    /* Professional Dark Action Cards */
    div.stButton > button {
        width: 100%;
        background-color: #0e131b !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    }

    div.stButton > button:hover {
        background-color: #141c28 !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.15) !important;
    }

    /* Chat Messages Base Structure */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 1.25rem 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }

    /* USER MESSAGE BUBBLE - Deep Steel Blue */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: #0f172a !important;
        border: 1px solid #2563eb !important;
    }

    [data-testid="stChatMessage"]:has([aria-label*="user"]) p {
        color: #f8fafc !important;
        font-size: 1.08rem !important;
        line-height: 1.7 !important;
        font-weight: 600 !important;
    }

    /* ASSISTANT MESSAGE BUBBLE - Dark Obsidian Metallic Card */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        background-color: #0d1117 !important;
        border: 1px solid #1e293b !important;
    }

    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) p {
        color: #f8fafc !important;
        font-size: 1.08rem !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
    }

    /* Precise Blue Highlights for AI Formatting */
    [data-testid="stChatMessage"] strong {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    /* Code blocks inside chat */
    [data-testid="stChatMessage"] code {
        background-color: #161b22 !important;
        color: #38bdf8 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        padding: 0.2rem 0.4rem !important;
    }

    /* Professional Dark Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid #1e293b !important;
        background-color: #0d1117 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2) !important;
    }

    [data-testid="stChatInput"] input {
        font-size: 1.05rem !important;
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    [data-testid="stChatInput"] input::placeholder {
        color: #64748b !important;
    }

    /* Professional Dark Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #05070a;
        border-right: 1px solid #1e293b;
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
        gap: 0.5rem;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        background-color: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #4ade80;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #22c55e;
        box-shadow: 0 0 8px #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown("### Controls")
    st.markdown('<div class="status-pill"><div class="status-dot"></div> System Active</div>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("➕ Start New Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-section-title">System Architecture</div>', unsafe_allow_html=True)
    st.caption("**Engine:** Flowise Cloud Agent")
    st.caption("**Security:** Encrypted Session")
    st.caption("**Theme:** Executive Dark Obsidian")

# Main Header Bar
st.markdown("""
<div class="brand-bar">
    <div class="brand-title">
        <span>✦</span> Workspace Assistant
    </div>
    <span class="brand-tag">v3.0 Enterprise</span>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen (Only renders on fresh sessions)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div>
        <div class="welcome-heading">How can I assist you today?</div>
        <div class="welcome-sub">Select an enterprise capability below or type a query:</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 System Capability Overview"):
            st.session_state.prompt_trigger = "Explain what this AI agent can do and how to best interact with it."
        if st.button("📝 Technical Document Summarization"):
            st.session_state.prompt_trigger = "Provide a clean framework for summarizing complex technical documents."

    with c2:
        if st.button("💡 Strategic Brainstorming Method"):
            st.session_state.prompt_trigger = "Share 3 highly effective techniques for brainstorming creative ideas."
        if st.button("⚡ Cloud Architecture Principles"):
            st.session_state.prompt_trigger = "Explain key cloud architecture principles in simple terms."

# Process Pre-filled Starter Prompts
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Message History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✦"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Generate AI Assistant Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="✦"):
        with st.spinner("Processing request..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input
if user_input := st.chat_input("Type your message or command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
