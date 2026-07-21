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
        return "Error: Unable to establish connection to the Flowise server."
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed. ({str(e)})"

# Page configuration
st.set_page_config(
    page_title="Enterprise AI Workspace",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    /* Global Base Styling */
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
    }

    /* Hide Default Chrome Elements */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Header Section */
    .header-container {
        background-color: #ffffff;
        padding: 24px 32px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0369a1; /* Enterprise Blue */
        margin: 0;
        letter-spacing: -0.3px;
    }
    .header-subtitle {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 4px;
    }

    /* Quick Prompt Cards */
    .section-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 12px;
    }
    
    /* Executive Starter Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #0369a1 !important;
        border: 1px solid #bae6fd !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    div.stButton > button:hover {
        background-color: #f0f9ff !important;
        border-color: #0284c7 !important;
        color: #0284c7 !important;
        box-shadow: 0 2px 4px rgba(2, 132, 199, 0.08);
    }

    /* High-Contrast Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    [data-testid="stChatMessage"] p {
        color: #0f172a !important; /* Pure slate black for crisp text */
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        border-radius: 10px !important;
        border: 1px solid #93c5fd !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    [data-testid="stChatInput"] input {
        color: #0f172a !important;
        font-size: 0.95rem !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 16px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 6px;
        background-color: #e0f2fe;
        border: 1px solid #bae6fd;
        color: #0369a1;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    .status-indicator {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div class="sidebar-header">Workspace Control</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><div class="status-indicator"></div> System Ready</div>', unsafe_allow_html=True)
    
    if st.button("➕ New Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Infrastructure**")
    st.caption("Engine: Flowise AI Flow")
    st.caption("Status: Operational")

# ---------- MAIN WORKSPACE ----------

# Professional Header
st.markdown("""
<div class="header-container">
    <div>
        <div class="header-title">AI Knowledge Workspace</div>
        <div class="header-subtitle">Automated insights, document queries, and tactical analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Prompts Grid if no message exists
if len(st.session_state.messages) == 0:
    st.markdown('<div class="section-title">Suggested Inquiries</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Explain the capabilities of this agent"):
            st.session_state.prompt_trigger = "Explain the primary capabilities of this AI assistant."
        if st.button("📊 Provide a structured analysis framework"):
            st.session_state.prompt_trigger = "Provide a structured framework for analyzing technical project proposals."

    with col2:
        if st.button("📝 Draft a professional executive summary"):
            st.session_state.prompt_trigger = "Provide an outline for writing an executive summary for a project report."
        if st.button("⚡ Summarize technical concepts cleanly"):
            st.session_state.prompt_trigger = "Summarize the core principles of modern cloud architecture."

# Handle Triggered Prompt from Buttons
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Conversation Logs
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="⚡"):
            st.markdown(msg["content"])

# Process Assistant Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Processing request..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input Field
if user_input := st.chat_input("Enter your request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
