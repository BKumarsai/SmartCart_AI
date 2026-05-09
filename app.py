from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

from shoppingbot.router.semantic_router import (
    SemanticRouter, PRODUCT_ROUTE_NAME, CHITCHAT_ROUTE_NAME, OFFTOPIC_ROUTE_NAME
)
from shoppingbot.chain import create_chitchat_chain
from shoppingbot.agent import ShoppingAgent
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory

# ─── Setup ────────────────────────────────────────────────────────────────────
LLM = ChatGroq(
    temperature=0.3,
    model_name=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
    groq_api_key=os.getenv("GROQ_API_KEY")
)
SHARED_MEMORY   = ConversationBufferMemory(return_messages=True)
SEMANTIC_ROUTER = SemanticRouter()

OFF_TOPIC_MSG = (
    "🚫 That's outside my expertise! I'm **ShopBot** — your dedicated shopping assistant.\n\n"
    "I can help you with:\n"
    "• 🛍️ Finding products & comparing prices\n"
    "• ⭐ Product reviews & ratings\n"
    "• 🏷️ Brand recommendations\n"
    "• 📦 Shipping, returns & policies\n\n"
    "What are you shopping for today? 😊"
)

app = Flask(__name__)

# ─── Core Handler ─────────────────────────────────────────────────────────────
def handle_query(query: str) -> dict:
    try:
        guided_route = SEMANTIC_ROUTER.guide(query)
    except Exception:
        guided_route = CHITCHAT_ROUTE_NAME

    if guided_route == OFFTOPIC_ROUTE_NAME:
        return {"response": OFF_TOPIC_MSG, "type": "offtopic"}

    elif guided_route == CHITCHAT_ROUTE_NAME:
        chain    = create_chitchat_chain(LLM, SHARED_MEMORY)
        response = chain.invoke({"input": query})
        content  = response.get("response", str(response))

    elif guided_route == PRODUCT_ROUTE_NAME:
        agent    = ShoppingAgent(LLM, SHARED_MEMORY)
        response = agent.invoke(query)
        content  = (
            response.content if hasattr(response, "content")
            else response.get("output", str(response))
        )
    else:
        content = "Sorry, I didn't understand that. Could you rephrase?"

    SHARED_MEMORY.chat_memory.add_user_message(query)
    SHARED_MEMORY.chat_memory.add_ai_message(content)

    return {"response": content, "type": guided_route}

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data         = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    result = handle_query(user_message)
    return jsonify(result)

@app.route("/clear", methods=["POST"])
def clear_chat():
    SHARED_MEMORY.chat_memory.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    print("\n🛍️  ShoppingBot Pro — Groq Edition")
    print("⚡  LLaMA 3 70B · Semantic Router · 5 AI Tools")
    print("🔗  Real Amazon · Flipkart · Meesho · Ajio · Myntra links")
    print("⭐  Product reviews · Brand advisor · Policy search")
    print("✅  Ready → http://localhost:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))