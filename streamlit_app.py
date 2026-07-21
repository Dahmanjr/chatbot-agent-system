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
    page_title="Flowise AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Vivid, modern, glassmorphic design
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background: radial-gradient(circle at top left, #1a103c, #0b0d19, #05060a);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f8fafc;
    }

    /* Hide default Streamlit headers & footers */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Vibrant Hero Header */
    .hero-container {
        text-align: center;
        padding: 30px 20px 10px 20px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Glassmorphic Cards for Suggestions */
    .welcome-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    .welcome-card h3 {
        color: #f3e8ff;
        font-size: 1.3rem;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    /* Neon Pill Buttons */
    div.stButton > button {
        width: 100%;
        background: rgba(30, 27, 75, 0.6) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(8px);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(236, 72, 153, 0.3)) !important;
        border-color: #ec4899 !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.25);
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 13, 25, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .sidebar-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(59, 130, 246, 0.2));
        border: 1px solid rgba(168, 85, 247, 0.4);
        color: #c084fc;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<span class="sidebar-badge">⚡ FLOWISE POWERED</span>', unsafe_allow_html=True)
    st.title("Control Panel")
    st.markdown("---")
    
    if st.button("➕ New Chat Session"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📊 Status")
    st.markdown("🟢 **Agent Status:** Online")
    st.markdown("⚡ **Latency:** ~240ms")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tip")
    st.caption("You can ask me to write code, explain complex scientific concepts, or brainstorm new product ideas!")

# ---------- MAIN CONTENT ----------

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Welcome to Next-Gen AI</div>
    <div class="hero-subtitle">Ask questions, generate ideas, or analyze concepts in real time.</div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Prompt Cards if conversation hasn't started
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h3>🚀 Get Started Fast</h3>
        <p style="color: #94a3b8; margin-bottom: 0;">Select a starter prompt below to kickstart your conversation:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 How does Flowise AI work?"):
            st.session_state.prompt_trigger = "How does Flowise AI work?"
        if st.button("📝 Help me write a creative story"):
            st.session_state.prompt_trigger = "Help me write a creative story"

    with col2:
        if st.button("📊 Summarize complex tech trends"):
            st.session_state.prompt_trigger = "Summarize modern technology trends for me."
        if st.button("🎯 Brainstorm 5 startup ideas"):
            st.session_state.prompt_trigger = "Brainstorm 5 innovative startup ideas for 2026."

# Handle Triggered Prompt from Cards
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Chat Messages via Native Chat Elements
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# Trigger API response for unanswered user prompt
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("✨ Processing query..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input Field
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
