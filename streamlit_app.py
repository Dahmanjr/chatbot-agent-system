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
    page_title="Messenger AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling — Messenger Dark Mode Palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Messenger Dark Canvas */
    .stApp {
        background-color: #0b141f;
        color: #ffffff;
    }

    /* Hide standard Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Container constraints */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 850px;
    }

    /* Brand Header */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #1c2938;
    }

    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0084ff 0%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Welcome Card */
    .welcome-heading {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
    }

    .welcome-sub {
        font-size: 1.05rem;
        color: #93a3b8;
        margin-bottom: 1.5rem;
    }

    /* Messenger-Style Interactive Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #162436 !important;
        color: #e2e8f0 !important;
        border: 1px solid #24364e !important;
        border-radius: 18px !important;
        padding: 0.85rem 1.1rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0084ff 0%, #00c6ff 100%) !important;
        border-color: #00c6ff !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 132, 255, 0.4) !important;
    }

    /* Chat Messages Base Styling */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }

    /* User Message - Messenger Blue Gradient Bubble */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: linear-gradient(135deg, #0084ff 0%, #00a6ff 100%);
        border: none;
    }

    [data-testid="stChatMessage"]:has([aria-label*="user"]) p {
        color: #ffffff !important;
        font-size: 1.02rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }

    /* Assistant Message - Crisp High-Contrast White Bubble */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        background-color: #1e2d42;
        border: 1px solid #2c3e55;
    }

    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) p {
        color: #ffffff !important;
        font-size: 1.02rem !important;
        line-height: 1.65 !important;
        font-weight: 400 !important;
    }

    /* Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 22px !important;
        border: 2px solid #24364e !important;
        background-color: #162436 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #0084ff !important;
        box-shadow: 0 0 15px rgba(0, 132, 255, 0.3) !important;
    }

    [data-testid="stChatInput"] input {
        font-size: 1rem !important;
        color: #ffffff !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080e17;
        border-right: 1px solid #162436;
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
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        background-color: rgba(0, 198, 255, 0.12);
        border: 1px solid rgba(0, 198, 255, 0.3);
        color: #00c6ff;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #00c6ff;
        box-shadow: 0 0 8px #00c6ff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown("### Menu")
    
    st.markdown('<div class="status-pill"><div class="status-dot"></div> Connected</div>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-section-title">System Information</div>', unsafe_allow_html=True)
    st.caption("**Engine:** Flowise Cloud")
    st.caption("**Palette:** Messenger Dark Blue")

# Main Header
st.markdown("""
<div class="brand-bar">
    <div class="brand-title">
        <span>⚡ AI Assistant</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen Prompt Cards
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div>
        <div class="welcome-heading">Welcome back!</div>
        <div class="welcome-sub">Choose a suggestion below to start messaging:</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Explain what this assistant can do"):
            st.session_state.prompt_trigger = "Explain what this AI assistant can do and how to best interact with it."
        if st.button("📝 Help me summarize a topic"):
            st.session_state.prompt_trigger = "Provide a clean framework for summarizing complex technical documents."

    with c2:
        if st.button("💡 Brainstorm 3 creative ideas"):
            st.session_state.prompt_trigger = "Share 3 highly effective techniques for brainstorming creative ideas."
        if st.button("⚡ Explain complex tech simply"):
            st.session_state.prompt_trigger = "Explain how cloud architecture works in simple terms."

# Handle Triggered Starter Prompts
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Message History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Process Assistant Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Thinking..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input
if user_input := st.chat_input("Message AI..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
