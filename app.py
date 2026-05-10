from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv(override=True)



from shoppingbot.router.semantic_router import (
    SemanticRouter, PRODUCT_ROUTE_NAME, CHITCHAT_ROUTE_NAME, OFFTOPIC_ROUTE_NAME
)
from shoppingbot.chain import create_chitchat_chain
from shoppingbot.agent import ShoppingAgent
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory

# ─── Setup ────────────────────────────────────────────────────────────────────
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY not found! Check your .env file")
LLM = ChatGroq(
    temperature=0.3,
    model_name=os.getenv("LLM_MODEL", "llama-3.1-8b-instant"),
    groq_api_key=GROQ_KEY
)
SHARED_MEMORY = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
    input_key="input",
)
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
    content = "Sorry, I didn't understand that. Could you rephrase?"
    
    try:
        guided_route = SEMANTIC_ROUTER.guide(query)
    except Exception:
        guided_route = CHITCHAT_ROUTE_NAME

    if guided_route == OFFTOPIC_ROUTE_NAME:
        return {"response": OFF_TOPIC_MSG, "type": "offtopic"}

    elif guided_route == CHITCHAT_ROUTE_NAME:
        try:
            chain    = create_chitchat_chain(LLM, SHARED_MEMORY)
            response = chain.invoke({"input": query})
            content  = response.get("response", str(response))
        except Exception as e:
            content = f"Sorry I had an issue: {str(e)}"

    elif guided_route == PRODUCT_ROUTE_NAME:
        try:
            # Build conversation history string
            messages = SHARED_MEMORY.chat_memory.messages
            history = ""
            for msg in messages[-10:]:
                role = "Customer" if msg.type == "human" else "ShopBot"
                history += f"{role}: {msg.content}\n"

            # Add context to query if it seems like a follow-up
            follow_up_words = [
                "first one", "that", "it", "those", "this",
                "the same", "above", "previous", "last one",
                "price of", "link for", "buy that", "show links",
                "where to buy", "how much"
            ]

            is_followup = any(w in query.lower() for w in follow_up_words)

            if is_followup and history:
                enhanced_query = f"""Previous conversation:
{history}

Current question: {query}

Based on the conversation above, answer the current question."""
            else:
                enhanced_query = query

            agent    = ShoppingAgent(LLM, SHARED_MEMORY)
            response = agent.invoke(enhanced_query)
            content  = (
                response.content if hasattr(response, "content")
                else response.get("output", str(response))
            )
        except Exception as e:
            content = f"Sorry I had an issue: {str(e)}"

    # Save to memory
    try:
        SHARED_MEMORY.chat_memory.add_user_message(query)
        SHARED_MEMORY.chat_memory.add_ai_message(content)
    except Exception:
        pass

    return {"response": content, "type": guided_route}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
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
    print("✅  Ready → http://localhost:5000\n")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))