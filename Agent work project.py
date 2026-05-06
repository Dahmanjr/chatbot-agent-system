import streamlit as st
import requests
import time

OPENROUTER_API_KEY = "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"

SYSTEM_PROMPT = """You are an expert B2B lead generation researcher..."""  # (full prompt from your code)

@st.cache_data(ttl=3600)
def get_free_models():
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        r.raise_for_status()
        all_models = r.json().get("data", [])
        free_models = [m["id"] for m in all_models if m.get("pricing", {}).get("prompt") == "0" and m.get("pricing", {}).get("completion") == "0"]
        return free_models if free_models else ["openrouter/free"]
    except Exception:
        return ["openrouter/free"]

def call_openrouter(messages, model_idx=0):
    free_models = get_free_models()
    if model_idx >= len(free_models):
        raise Exception("All free models failed.")
    model = free_models[model_idx]
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": 2000, "temperature": 0.7}
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"], r.headers.get("X-OpenRouter-Model", model)
    except requests.exceptions.HTTPError as e:
        if r.status_code in (404, 429, 503) and model_idx + 1 < len(free_models):
            time.sleep(2)
            return call_openrouter(messages, model_idx + 1)
        raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception:
        time.sleep(2)
        return call_openrouter(messages, model_idx + 1)

# Streamlit UI
st.set_page_config(page_title="ERP Cairo Lead Agent", page_icon="🇪🇬")
st.title("🇪🇬 ERP Cairo Lead Agent")
st.caption("Find companies in Cairo that use or plan ERP")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about ERP leads in Cairo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            try:
                reply, model = call_openrouter(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
                st.caption(f"Model: {model.split('/')[-1]}")
            except Exception as e:
                st.error(f"Error: {e}")
    st.rerun()
