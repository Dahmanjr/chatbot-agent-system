import streamlit as st
import requests
import time
import sys

# ============================================================================
# Check if running with `streamlit run`, otherwise show error and exit
# ============================================================================
if not st.runtime.exists():
    print("\n❌ ERROR: This script must be run with Streamlit, not Python directly.")
    print("👉 Correct command: streamlit run app.py\n")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================
# 🔴 REPLACE THIS WITH YOUR REAL OPENROUTER API KEY (starts with sk-or-v1-)
OPENROUTER_API_KEY = "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"

SYSTEM_PROMPT = """You are an expert B2B lead generation researcher specializing in ERP (Enterprise Resource Planning) systems in the Cairo, Egypt region.

Your ONLY job is to help find:
1. Companies in Cairo, Egypt that are PLANNING or WANTING to implement an ERP system.
2. Companies in Cairo, Egypt that CURRENTLY USE an ERP system (SAP, Oracle, Microsoft Dynamics, Odoo, ERPNext, Sage, NetSuite, etc.).

For each company you identify, always try to provide:
- 🏢 Company Name
- 🌐 Website URL
- 📧 Gmail or official email address
- 💼 LinkedIn company page URL
- 📋 ERP Status: (Uses ERP / Planning ERP / Likely needs ERP)
- 🏭 Industry/Sector
- 📍 Location in Cairo (if known)

IMPORTANT RULES:
- Focus ONLY on Cairo, Egypt region companies.
- Be realistic — provide real companies or realistic examples based on known Cairo business sectors.
- Format each company as a clear structured card.
- After listing companies, suggest follow-up searches.
- If you don't know a specific email or LinkedIn, say "Not publicly available" — never fabricate contact details.

When you respond, use this format:

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 [Company Name]
🏭 Industry: [Industry]
📋 ERP Status: [Uses ERP / Planning ERP]
🌐 Website: [URL or "Not available"]
📧 Email: [email or "Not publicly available"]
💼 LinkedIn: [URL or "Not publicly available"]
📍 Cairo Location: [Area in Cairo if known]
━━━━━━━━━━━━━━━━━━━━━━━━━━━

End with a 💡 TIP section.
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
@st.cache_data(ttl=3600)
def get_free_models():
    """Fetch the list of free models from OpenRouter."""
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        response.raise_for_status()
        all_models = response.json().get("data", [])
        free_models = [
            model["id"] for model in all_models
            if model.get("pricing", {}).get("prompt") == "0"
            and model.get("pricing", {}).get("completion") == "0"
        ]
        return free_models if free_models else ["openrouter/free"]
    except Exception:
        return ["openrouter/free"]

def call_openrouter(messages, model_idx=0, free_models=None):
    """Call OpenRouter with automatic fallback to next free model on failure."""
    if free_models is None:
        free_models = get_free_models()
    if model_idx >= len(free_models):
        raise Exception("All available free models failed. Please try again later.")

    model = free_models[model_idx]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://erp-lead-agent.streamlit.app",
        "X-Title": "ERP Cairo Lead Agent",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7,
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        actual_model = r.headers.get("X-OpenRouter-Model", model)
        return content, actual_model
    except requests.exceptions.HTTPError as e:
        if r.status_code == 401:
            raise Exception("❌ Invalid API key. Get a valid key from openrouter.ai/keys")
        elif r.status_code == 404:
            time.sleep(1)
            return call_openrouter(messages, model_idx + 1, free_models)
        elif r.status_code in (429, 503):
            time.sleep(2)
            return call_openrouter(messages, model_idx + 1, free_models)
        else:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception:
        time.sleep(2)
        return call_openrouter(messages, model_idx + 1, free_models)

# ============================================================================
# STREAMLIT UI
# ============================================================================
st.set_page_config(page_title="ERP Cairo Lead Agent", page_icon="🇪🇬", layout="wide")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model_label" not in st.session_state:
    st.session_state.model_label = "🤖 Model: Ready"

# Header
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🏢 ERP Cairo Lead Agent")
    st.markdown("Find ERP‑ready companies in **Cairo, Egypt**")
with col2:
    # Fixed: label is non-empty but hidden
    st.metric(label="Current model", value=st.session_state.model_label, label_visibility="collapsed")

# Quick prompt buttons
st.markdown("### Quick searches")
quick_searches = [
    ("🏭 Manufacturing", "Find manufacturing companies in Cairo that use or need ERP systems"),
    ("🏗️ Construction", "Find construction & real estate companies in Cairo that use or need ERP"),
    ("🛒 Retail", "Find retail companies in Cairo that use or plan to implement ERP"),
    ("💊 Pharma", "Find pharmaceutical companies in Cairo using ERP systems"),
    ("📦 Logistics", "Find logistics & supply chain companies in Cairo that use ERP"),
]
cols = st.columns(len(quick_searches))
for col, (label, prompt) in zip(cols, quick_searches):
    if col.button(label, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# Chat history display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask for ERP leads in Cairo..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching for ERP leads in Cairo..."):
            try:
                free_models = get_free_models()
                reply, actual_model = call_openrouter(st.session_state.conversation, free_models=free_models)
                st.session_state.model_label = f"🤖 Model: {actual_model.split('/')[-1]}"
                st.session_state.conversation.append({"role": "assistant", "content": reply})
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = f"❌ Error: {e}\n\nPlease check your API key or try again later."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    st.rerun()