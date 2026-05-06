import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import requests
import json
import re
import time
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
# 🔴 REPLACE THIS with your REAL OpenRouter API key (starts with sk-or-v1-)
OPENROUTER_API_KEY = "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"

# No hardcoded model list – we'll fetch it dynamically

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
- Be realistic — provide real companies or realistic examples based on known Cairo business sectors (manufacturing, logistics, retail, FMCG, pharma, construction, real estate, services).
- If the user asks for a specific sector (e.g., manufacturing, retail), focus on that.
- Format each company as a clear structured card.
- After listing companies, suggest follow-up searches the user can do.
- If you don't know a specific email or LinkedIn, say "Not publicly available" — never fabricate contact details.
- Always be helpful, professional, and sales-oriented in tone.

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

End with a 💡 TIP section with suggestions for finding more leads.
"""

# ── Colors / Fonts ────────────────────────────────────────────────────────
BG_DARK    = "#0d1117"
BG_CARD    = "#161b22"
BG_INPUT   = "#21262d"
ACCENT     = "#00d4aa"
ACCENT2    = "#0ea5e9"
TEXT_MAIN  = "#e6edf3"
TEXT_DIM   = "#8b949e"
TEXT_USER  = "#ffffff"
BORDER     = "#30363d"
FONT_MAIN  = ("Segoe UI", 11)
FONT_BOLD  = ("Segoe UI", 11, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 10)

# ── Dynamic model discovery ──────────────────────────────────────────────
def get_free_models():
    """Fetch the list of free models directly from OpenRouter."""
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        response.raise_for_status()
        all_models = response.json().get("data", [])
        
        # Filter for models that are free (pricing prompt == "0" and completion == "0")
        free_models = [
            model["id"] for model in all_models 
            if model.get("pricing", {}).get("prompt") == "0" and model.get("pricing", {}).get("completion") == "0"
        ]
        
        if free_models:
            return free_models
        else:
            # Fallback to the smart free router if no free models found
            return ["openrouter/free"]
    except Exception as e:
        print(f"Model discovery failed: {e}. Falling back to 'openrouter/free'.")
        return ["openrouter/free"]  # Safe fallback

# Fetch models once at module load
FREE_MODELS = get_free_models()

# ── OpenRouter call with robust fallback ────────────────────────────────
def call_openrouter(messages: list, model_idx: int = 0) -> tuple:
    """Call OpenRouter, automatically trying next free model on failure."""
    if model_idx >= len(FREE_MODELS):
        raise Exception("All available free models failed. Please try again later or check your API key.")

    model = FREE_MODELS[model_idx]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://erp-cairo-agent.local",  # Replace with your actual site URL if needed
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
        # Get the actual model used (important when using openrouter/free)
        actual_model = r.headers.get("X-OpenRouter-Model", model)
        return content, actual_model
    except requests.exceptions.HTTPError as e:
        if r.status_code == 401:
            raise Exception("❌ Invalid API key. Get a valid key from openrouter.ai/keys (starts with sk-or-v1-)")
        elif r.status_code == 404:
            # Model not found – try next model
            print(f"Model {model} not found (404). Trying next model...")
            time.sleep(1)
            return call_openrouter(messages, model_idx + 1)
        elif r.status_code in (429, 503):
            # Rate limited or unavailable – try next model
            print(f"Model {model} rate-limited or unavailable. Trying next model...")
            time.sleep(2)
            return call_openrouter(messages, model_idx + 1)
        else:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        # Network errors, timeouts – try next model
        print(f"Error with model {model}: {e}. Trying next model...")
        time.sleep(2)
        return call_openrouter(messages, model_idx + 1)

# ── GUI App (unchanged, works with the new call_openrouter) ──────────────
class ERPCairoAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("ERP Cairo Lead Agent 🇪🇬")
        self.root.geometry("1000x780")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(700, 500)

        self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.model_label_var = tk.StringVar(value="Model: loading…")
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self.root, bg=BG_CARD, pady=12)
        hdr.pack(fill=tk.X)

        tk.Label(hdr, text="🏢", font=("Segoe UI Emoji", 22), bg=BG_CARD, fg=ACCENT).pack(side=tk.LEFT, padx=(18, 6))
        title_frame = tk.Frame(hdr, bg=BG_CARD)
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="ERP Cairo Lead Agent", font=FONT_TITLE, bg=BG_CARD, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(title_frame, text="Find ERP-ready companies in Cairo, Egypt", font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")

        tk.Label(hdr, textvariable=self.model_label_var, font=FONT_SMALL, bg=BG_CARD, fg=ACCENT).pack(side=tk.RIGHT, padx=18)

        # ── Quick-prompt buttons ──
        btn_bar = tk.Frame(self.root, bg=BG_DARK, pady=8)
        btn_bar.pack(fill=tk.X, padx=16)
        tk.Label(btn_bar, text="Quick search:", font=FONT_SMALL, bg=BG_DARK, fg=TEXT_DIM).pack(side=tk.LEFT, padx=(0, 8))
        quick = [
            ("🏭 Manufacturing", "Find manufacturing companies in Cairo that use or need ERP systems"),
            ("🏗️ Construction",  "Find construction & real estate companies in Cairo that use or need ERP"),
            ("🛒 Retail",        "Find retail companies in Cairo that use or plan to implement ERP"),
            ("💊 Pharma",        "Find pharmaceutical companies in Cairo using ERP systems"),
            ("📦 Logistics",     "Find logistics & supply chain companies in Cairo that use ERP"),
        ]
        for label, prompt in quick:
            tk.Button(
                btn_bar, text=label, font=FONT_SMALL,
                bg=BG_INPUT, fg=ACCENT, activebackground=ACCENT, activeforeground=BG_DARK,
                relief=tk.FLAT, bd=0, padx=10, pady=4, cursor="hand2",
                command=lambda p=prompt: self._quick_send(p)
            ).pack(side=tk.LEFT, padx=3)

        # ── Chat area ──
        chat_frame = tk.Frame(self.root, bg=BG_DARK)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 8))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD, state=tk.DISABLED,
            bg=BG_DARK, fg=TEXT_MAIN,
            font=FONT_MONO, bd=0,
            insertbackground=ACCENT,
            selectbackground=ACCENT2,
            padx=12, pady=12,
            relief=tk.FLAT,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Tag styles
        cd = self.chat_display
        cd.tag_config("user_lbl",  foreground=ACCENT2,    font=("Segoe UI", 9, "bold"))
        cd.tag_config("user_msg",  foreground=TEXT_USER,  font=FONT_MAIN,
                      lmargin1=30, lmargin2=30, spacing3=8)
        cd.tag_config("bot_lbl",   foreground=ACCENT,     font=("Segoe UI", 9, "bold"))
        cd.tag_config("bot_msg",   foreground=TEXT_MAIN,  font=FONT_MONO,
                      lmargin1=30, lmargin2=30, spacing3=8)
        cd.tag_config("status",    foreground=TEXT_DIM,   font=FONT_SMALL,
                      lmargin1=30, spacing3=6)
        cd.tag_config("divider",   foreground=BORDER)
        cd.tag_config("company",   foreground=ACCENT,     font=("Consolas", 10, "bold"))
        cd.tag_config("highlight", foreground="#ffd700")

        # ── Input area ──
        inp_frame = tk.Frame(self.root, bg=BG_CARD, pady=10)
        inp_frame.pack(fill=tk.X, padx=16, pady=(0, 12))
        inp_frame.columnconfigure(0, weight=1)

        self.input_box = tk.Text(
            inp_frame, height=3, wrap=tk.WORD,
            bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
            font=FONT_MAIN, bd=0, padx=10, pady=8, relief=tk.FLAT,
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        self.input_box.bind("<Return>",       self._on_enter)
        self.input_box.bind("<Shift-Return>", lambda e: None)

        send_btn = tk.Button(
            inp_frame, text="Send ▶", font=FONT_BOLD,
            bg=ACCENT, fg=BG_DARK, activebackground="#00b894", activeforeground=BG_DARK,
            relief=tk.FLAT, bd=0, padx=18, pady=8, cursor="hand2",
            command=self._send_message,
        )
        send_btn.grid(row=0, column=1, padx=8)

        tk.Label(inp_frame, text="Enter ↵ to send  |  Shift+Enter for new line",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).grid(row=1, column=0, columnspan=2, sticky="w", padx=8)

        # ── Welcome message ──
        self._append_bot(
            "مرحبًا! Welcome! 🇪🇬\n\n"
            "I'm your ERP Lead Generation Agent for Cairo, Egypt.\n\n"
            "I can help you find:\n"
            "  ✅ Companies in Cairo that USE ERP systems\n"
            "  ✅ Companies in Cairo PLANNING to implement ERP\n\n"
            "For each company I'll provide:\n"
            "  🌐 Website  |  📧 Email  |  💼 LinkedIn  |  🏭 Industry\n\n"
            "Use the quick buttons above or type your own query below.\n"
            "Example: 'Find 5 Cairo manufacturing companies that use SAP'"
        )

    def _append_text(self, text, tag):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_user(self, text):
        ts = datetime.now().strftime("%H:%M")
        self._append_text(f"\n👤 You  [{ts}]\n", "user_lbl")
        self._append_text(text + "\n", "user_msg")

    def _append_bot(self, text):
        ts = datetime.now().strftime("%H:%M")
        self._append_text(f"\n🤖 Agent  [{ts}]\n", "bot_lbl")
        lines = text.split("\n")
        for line in lines:
            if line.startswith("🏢"):
                self._append_text(line + "\n", "company")
            elif any(line.startswith(e) for e in ["🌐", "📧", "💼", "📋", "🏭", "📍"]):
                self._append_text(line + "\n", "highlight")
            elif line.startswith("━"):
                self._append_text(line + "\n", "divider")
            else:
                self._append_text(line + "\n", "bot_msg")

    def _append_status(self, text):
        self._append_text(f"  ⏳ {text}\n", "status")

    def _quick_send(self, prompt):
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert("1.0", prompt)
        self._send_message()

    def _on_enter(self, event):
        if not event.state & 0x1:
            self._send_message()
            return "break"

    def _send_message(self):
        user_text = self.input_box.get("1.0", tk.END).strip()
        if not user_text:
            return
        self.input_box.delete("1.0", tk.END)
        self._append_user(user_text)
        self.conversation.append({"role": "user", "content": user_text})
        self._append_status("Searching for ERP leads in Cairo…")
        threading.Thread(target=self._fetch_response, daemon=True).start()

    def _fetch_response(self):
        try:
            reply, model = call_openrouter(self.conversation)
            self.conversation.append({"role": "assistant", "content": reply})
            self.root.after(0, lambda: self.model_label_var.set(f"Model: {model.split('/')[-1]}"))
            self.root.after(0, lambda: self._append_bot(reply))
        except Exception as e:
            err = f"Error: {e}\n\nPlease check your API key or try again."
            self.root.after(0, lambda: self._append_bot(err))

# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ERPCairoAgent(root)
    root.mainloop()