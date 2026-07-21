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
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Bright Baby Blue & White with High Contrast Text
st.markdown("""
<style>
    /* Main Page Background */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ffffff 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0f172a; /* Deep charcoal black for ultra-clear readability */
    }

    /* Hide default Streamlit headers & footers */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden;
    }

    /* Hero Title Header */
    .hero-container {
        text-align: center;
        padding: 24px 20px 10px 20px;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #0284c7; /* Bright sky/baby blue accent */
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #334155; /* High contrast dark gray */
        font-size: 1.15rem;
        font-weight: 500;
    }

    /* Crisp White Welcome Card */
    .welcome-card {
        background: #ffffff;
        border: 2px solid #bae6fd;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.08);
    }
    .welcome-card h3 {
        color: #0369a1;
        font-size: 1.35rem;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .welcome-card p {
        color: #334155 !important;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 0;
    }
    
    /* Interactive Starter Buttons */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #0369a1 !important; /* Deep baby-blue shade for clear text */
        border: 2px solid #7dd3fc !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(186, 230, 253, 0.4);
    }
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #0284c7 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
    }

    /* High Contrast Chat Bubbles & Text */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e0f2fe;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }
    [data-testid="stChatMessage"] p {
        color: #0f172a !important; /* Deep black-slate for maximum readability */
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        font-weight: 450 !important;
    }

    /* Custom Chat Input Box */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 2px solid #7dd3fc !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.1) !important;
    }
    [data-testid="stChatInput"] input {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f0f9ff;
        border-right: 2px solid #e0f2fe;
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
    .sidebar-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        background-color: #e0f2fe;
        border: 1.5px solid #7dd3fc;
        color: #0369a1 !important;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<span class="sidebar-badge">⚡ POWERED BY FLOWISE</span>', unsafe_allow_html=True)
    st.title("Control Panel")
    st.markdown("---")
    
    if st.button("➕ Start New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📊 Status")
    st.markdown("🟢 **Agent Status:** Online")
    st.markdown("⚡ **Latency:** ~240ms")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tip")
    st.caption("Feel free to ask me questions, request writing help, or summarize documents!")

# ---------- MAIN CONTENT ----------

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Welcome! How can I help today?</div>
    <div class="hero-subtitle">Ask questions, brainstorm ideas, or analyze concepts in seconds.</div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Prompt Cards if conversation hasn't started
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h3>🚀 Get Started Quickly</h3>
        <p>Pick one of the suggestions below to instantly test the chatbot:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 How does Flowise AI work?"):
            st.session_state.prompt_trigger = "How does Flowise AI work?"
        if st.button("📝 Help me write a creative story"):
            st.session_state.prompt_trigger = "Help me write a creative story"

    with col2:
        if st.button("📊 Summarize complex tech concepts"):
            st.session_state.prompt_trigger = "Summarize modern technological trends for me in simple terms."
        if st.button("🎯 Brainstorm 5 startup ideas"):
            st.session_state.prompt_trigger = "Brainstorm 5 innovative startup ideas for this year."

# Handle Triggered Prompt from Cards
if "prompt_trigger" in st.session_state:
    prompt = st.session_state.pop("prompt_trigger")
    st.session_state.messages.append({"role": "user", "content": prompt})

# Render Chat Messages with High Contrast Styling
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# Trigger API response for unanswered user prompt
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response_text = query(st.session_state.messages[-1]["content"])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Native Chat Input Field
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
