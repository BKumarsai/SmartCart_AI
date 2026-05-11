import os
from dotenv import load_dotenv
load_dotenv(override=True)

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="SmartCart AI",
    page_icon="🛒",
    layout="wide",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': '🛒 SmartCart AI'}
)

# ── Load API Key ──────────────────────────────────────────
groq_api_key = ""
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    .title-box {
        background: linear-gradient(135deg, #FF6B35, #FF8C42);
        padding: 20px 30px; border-radius: 12px; margin-bottom: 10px;
    }
    .title-text { color: white; font-size: 2.2rem; font-weight: 900; margin: 0; }
    .subtitle-text { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin: 4px 0 0 0; }
    .chat-user {
        background: linear-gradient(135deg, #FF6B35, #FF8C42);
        color: white; padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0; max-width: 75%;
        margin-left: auto; font-size: 0.95rem;
    }
    .chat-bot {
        background: #1a1a2e; color: #e0e0e0;
        padding: 15px 18px; border-radius: 18px 18px 18px 4px;
        margin: 8px 0; max-width: 85%; font-size: 0.95rem;
        border-left: 3px solid #FF6B35;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #FF8C42) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    .stTextInput > div > div > input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #FF6B35 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── System Prompt (defined first!) ───────────────────────
SYSTEM_PROMPT = """You are SmartCart AI — a professional AI shopping assistant for Indian e-commerce.

RULES:
1. ONLY answer shopping queries: products, prices, brands, reviews, recommendations, policies, delivery, returns.
2. If non-shopping question → politely refuse and redirect to shopping.
3. Always show prices in ₹ (Indian Rupees).
4. Always provide clickable shopping links like:
   - 🛒 [Amazon](https://www.amazon.in/s?k=PRODUCT_NAME)
   - 🔵 [Flipkart](https://www.flipkart.com/search?q=PRODUCT_NAME)
   - 🔴 [Myntra](https://www.myntra.com/search?q=PRODUCT_NAME)
   - 🩷 [Meesho](https://www.meesho.com/search?q=PRODUCT_NAME)
   - 💄 [Nykaa](https://www.nykaa.com/search/result/?q=PRODUCT_NAME)
5. Format responses with emojis and bullet points.
6. For brand comparisons — give pros/cons of each brand clearly.
7. For product recommendations — give top 3-5 options with prices in ₹.
8. Always end with buying tips or advice.
9. Be friendly, professional and helpful.

Replace PRODUCT_NAME in URLs with URL-encoded actual product name."""

# ── Chat History ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Groq Response Function (defined before sidebar!) ─────
def get_response(user_message: str) -> str:
    if not groq_api_key:
        return "⚠️ API Key not configured! Please contact admin."
    try:
        client = Groq(api_key=groq_api_key)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.messages[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1500,
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <p class="title-text">🛒 SmartCart AI</p>
    <p class="subtitle-text">AI-powered Shopping Assistant — Find products, compare brands, get reviews and buy links</p>
</div>
""", unsafe_allow_html=True)

# ── Top Badges (Clickable!) ───────────────────────────────
badge_cols = st.columns(6)
badge_searches = [
    ("🔍 Product Search", "Best smartphones under ₹20000"),
    ("⭐ Reviews",         "Top rated wireless headphones reviews"),
    ("🏷️ Brand Advisor",  "Nike vs Adidas shoes which is better"),
    ("🔗 Live Links",     "Show buy links for Samsung Galaxy S24"),
    ("📦 Policy Search",  "What is Amazon return policy"),
    ("🚫 Off-topic Guard","What is shopping policy for returns"),
]
for i, (label, query) in enumerate(badge_searches):
    with badge_cols[i]:
        if st.button(label, key=f"badge_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": query})
            with st.spinner("🔍 Searching..."):
                resp = get_response(query)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

st.divider()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Status")
    if not groq_api_key:
        st.error("⚠️ API Key missing!")
    else:
        st.success("✅ SmartCart AI Ready!")

    st.divider()
    st.markdown("### 💡 Quick Search")

    searches = [
        ("📱", "Best phones under ₹20000"),
        ("👟", "Nike vs Adidas shoes comparison"),
        ("💻", "Best laptops for students under ₹50000"),
        ("⌚", "Smart watches under ₹5000"),
        ("🎧", "Best wireless headphones"),
        ("💄", "Best skincare products for oily skin"),
        ("📺", "4K TVs under ₹50000"),
        ("👗", "Summer dresses on Myntra"),
    ]

    for emoji, search_text in searches:
        if st.button(f"{emoji} {search_text}", use_container_width=True, key=f"sidebar_{search_text}"):
            st.session_state.messages.append({"role": "user", "content": search_text})
            with st.spinner("🔍 Searching..."):
                resp = get_response(search_text)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_btn"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**Powered by:**")
    st.markdown("🤖 LLaMA 3.1 via Groq API")
    st.markdown("🔗 Amazon • Flipkart • Myntra")
    st.markdown("🔗 Meesho • Nykaa • Croma")

# ── Chat Display ──────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:40px;color:#666;">
        <h2 style="color:#FF6B35;">👋 Hello! I am SmartCart AI</h2>
        <p style="font-size:1.1rem;">Your AI shopping assistant for Indian e-commerce</p>
        <p>Ask me anything about products, prices, brands or reviews!</p>
        <p style="color:#FF6B35;font-size:1.1rem;">Try: "Best phones under ₹20000" 📱</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">👤 {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-bot">🛒 {msg["content"]}</div>',
                unsafe_allow_html=True
            )

# ── Input Area ────────────────────────────────────────────
st.divider()
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Search products, compare brands, check reviews...",
        label_visibility="collapsed",
        key="main_input"
    )

with col2:
    send_btn = st.button("Send 🚀", use_container_width=True, key="send_btn")

if send_btn and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🔍 SmartCart AI is searching..."):
        response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ── Footer ────────────────────────────────────────────────
st.divider()
st.markdown("Built with ❤️ | **SmartCart AI** | For Indian shoppers 🇮🇳")