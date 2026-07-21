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
    page_title="Messenger AI Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — Ultra-Dark Message Boxes for Maximum Text Clarity
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
    }

    /* Messenger Dark Canvas Base */
    .stApp {
        background-color: #03070d; /* Ultra deep background */
        color: #ffffff;
    }

    /* Hide standard Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Container layout width */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* Brand Header */
    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        margin-bottom: 1.75rem;
        border-bottom: 2px solid #111a26;
    }

    .brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #38bdf8;
        letter-spacing: -0.02em;
    }

    /* Welcome Card */
    .welcome-heading {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 1.75rem;
    }

    /* Clear Starter Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #0b131f !important;
        color: #ffffff !important;
        border: 2px solid #1e293b !important;
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }

    div.stButton > button:hover {
        background-color: #0084ff !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateY(-2px);
    }

    /* Base Chat Container Styling */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 1.25rem 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
    }

    /* USER MESSAGE BUBBLE - Dark Messenger Blue Accent with Crisp White Text */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        background: #0066cc !important; /* Rich Darker Messenger Blue */
        border: 1px solid #38bdf8 !important;
    }

    [data-testid="stChatMessage"]:has([aria-label*="user"]) p {
        color: #ffffff !important; /* Crisp Pure White */
        font-size: 1.12rem !important; /* Extra crisp font size */
        line-height: 1.7 !important;
        font-weight: 600 !important;
    }

    /* ASSISTANT MESSAGE BUBBLE - Deep Dark Onyx Box for Pure Contrast */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        background-color: #070d14 !important; /* Deep Dark Box */
        border: 2px solid #1c2b3e !important;
    }

    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) p {
        color: #ffffff !important; /* Ultra-bright White for Maximum Legibility */
        font-size: 1.12rem !important;
        line-height: 1.8 !important; /* Spacious line height for reading comfort */
        font-weight: 500 !important;
    }

    /* High-contrast Highlight for Bold Words inside Assistant Responses */
    [data-testid="stChatMessage"] strong {
        color: #38bdf8 !important; /* Electric Sky Blue for Key Terms */
        font-weight: 700 !important;
    }

    /* Chat Input Bar - Deep Dark Box Styling */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 2px solid #0084ff !important;
        background-color: #070d14 !important; /* Dark Input Box */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8) !important;
    }

    [data-testid="stChatInput"] input {
        font-size: 1.1rem !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    [data-testid="stChatInput"] input::placeholder {
        color: #64748b !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #020509;
        border-right: 2px solid #0f172a;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        background-color: rgba(0, 198, 255, 0.15);
        border: 1.5px solid #00c6ff;
        color: #00c6ff;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #00c6ff;
        box-shadow: 0 0 10px #00c6ff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown("### Menu")
    st.markdown('<div class="status-pill"><div class="status-dot"></div> Connected</div>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("➕ Start New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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
        <div class="welcome-heading">How can I help you today?</div>
        <div class="welcome-sub">Click a prompt below or type your message to begin:</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 What can this AI do?"):
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
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Process Assistant Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
