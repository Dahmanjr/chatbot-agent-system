import streamlit as st
import requests
import time
from datetime import datetime

# -------------------- Configuration --------------------
OPENROUTER_API_KEY = "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"

SYSTEM_PROMPT = """You are an expert B2B lead generation researcher specializing in ERP systems in Cairo, Egypt.

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
- If the user asks for a specific sector, focus on that.
- Format each company as a clear structured card.
- After listing companies, suggest follow‑up searches.
- Never fabricate contact details.

When you respond, use this format for each company:

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 [Company Name]
🏭 Industry: [Industry]
📋 ERP Status: [Uses ERP / Planning ERP]
🌐 Website: [URL or "Not available"]
📧 Email: [email or "Not publicly available"]
💼 LinkedIn: [URL or "Not publicly available"]
📍 Cairo Location: [Area in Cairo if known]
━━━━━━━━━━━━━━━━━━━━━━━━━━━

End with a 💡 TIP section."""
# ------------------------------------------------------

# ---- Helper: get free models from OpenRouter ----
@st.cache_data(ttl=3600)
def get_free_models():
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        r.raise_for_status()
        all_models = r.json().get("data", [])
        free_models = [
            m["id"] for m in all_models
            if m.get("pricing", {}).get("prompt") == "0" and m.get("pricing", {}).get("completion") == "0"
        ]
        return free_models if free_models else ["openrouter/free"]
    except Exception:
        return ["openrouter/free"]

# ---- OpenRouter call with fallback ----
def call_openrouter(messages, model_idx=0):
    free_models = get_free_models()
    if model_idx >= len(free_models):
        raise Exception("All free models failed. Try again later.")
    model = free_models[model_idx]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://erp-cairo-agent.streamlit.app",
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
            st.error("❌ Invalid OpenRouter API key. Please update OPENROUTER_API_KEY.")
            raise
        elif r.status_code == 404:
            time.sleep(1)
            return call_openrouter(messages, model_idx + 1)
        elif r.status_code in (429, 503):
            time.sleep(2)
            return call_openrouter(messages, model_idx + 1)
        else:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception:
        time.sleep(2)
        return call_openrouter(messages, model_idx + 1)

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="ERP Cairo Lead Agent", page_icon="🇪🇬", layout="wide")

# ─── Custom CSS for better readability ───
st.markdown("""
<style>
    .company-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        font-family: monospace;
    }
    .stChatMessage {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇪🇬 ERP Cairo Lead Agent")
st.caption("Find companies in Cairo that use or plan to implement ERP systems")

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "model_name" not in st.session_state:
    st.session_state.model_name = "Loading model..."

# Display past messages (skip the system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick‑search buttons
col1, col2, col3, col4, col5 = st.columns(5)
quick_prompts = {
    "🏭 Manufacturing": "Find manufacturing companies in Cairo that use or need ERP systems",
    "🏗️ Construction": "Find construction & real estate companies in Cairo that use or need ERP",
    "🛒 Retail": "Find retail companies in Cairo that use or plan to implement ERP",
    "💊 Pharma": "Find pharmaceutical companies in Cairo using ERP systems",
    "📦 Logistics": "Find logistics & supply chain companies in Cairo that use ERP",
}
for col, (label, prompt) in zip([col1, col2, col3, col4, col5], quick_prompts.items()):
    if col.button(label, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching for ERP leads in Cairo..."):
                try:
                    reply, model = call_openrouter(st.session_state.messages)
                    st.session_state.model_name = model.split('/')[-1]
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.markdown(reply)
                except Exception as e:
                    st.error(f"Error: {e}")
        st.rerun()

# Chat input
if prompt := st.chat_input("Ask about ERP leads in Cairo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⏳ Consulting OpenRouter models..."):
            try:
                reply, model = call_openrouter(st.session_state.messages)
                st.session_state.model_name = model.split('/')[-1]
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            except Exception as e:
                st.error(f"❌ Failed to get response: {e}")
                st.info("Check that your OpenRouter API key is correct and has access to free models.")
    st.rerun()

# Sidebar with model info and reset button
with st.sidebar:
    st.markdown(f"**Current Model:** `{st.session_state.model_name}`")
    if st.button("🗑️ Reset Conversation"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.model_name = "Loading model..."
        st.rerun()
    st.markdown("---")
    st.markdown("**ℹ️ How to use**")
    st.markdown("""
    - Ask for companies by sector (manufacturing, retail, logistics, etc.)
    - Request a specific number of leads, e.g., "Find 5 Cairo pharma companies using ERP"
    - The agent will reply with structured company cards.
    """)
    st.markdown("---")
    st.caption("Powered by OpenRouter free models")
