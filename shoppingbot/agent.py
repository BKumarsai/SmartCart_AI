from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from shoppingbot.tools.product_search import product_search_tool
from shoppingbot.tools.policy_search import policy_search_tool
from shoppingbot.tools.brand_advisor import brand_advisor_tool
from shoppingbot.tools.ecommerce_links import ecommerce_links_tool
from shoppingbot.tools.review_fetcher import review_fetcher_tool

# ── Non-shopping topics to hard-block ────────────────────────────────────────
BLOCKED_TOPICS = [
    "what is java", "what is python", "explain algorithm", "data structure",
    "how does machine learning", "what is ai", "capital of", "history of",
    "geography", "solve math", "physics formula", "chemical formula",
    "write code", "debug", "homework", "essay", "translate this",
    "who invented", "general knowledge", "trivia", "movie plot",
    "song lyrics", "recipe for", "cooking", "medical diagnosis",
    "legal advice", "stock market tips", "crypto price", "forex"
]

SHOPPING_SIGNALS = [
    "buy", "price", "cost", "product", "brand", "review", "recommend",
    "₹", "rs.", "rupee", "shop", "store", "purchase", "order", "shipping",
    "return", "exchange", "refund", "delivery", "discount", "offer", "sale",
    "available", "in stock", "size", "color", "specification", "features"
]

BLOCK_RESPONSE = (
    "🚫 I'm **ShopBot** — your dedicated shopping assistant!\n\n"
    "I only help with:\n"
    "• 🛍️ Product search & recommendations\n"
    "• 💰 Prices, deals & offers\n"
    "• ⭐ Product reviews & ratings\n"
    "• 🏷️ Brand guidance\n"
    "• 📦 Shipping, returns & store policies\n\n"
    "Try asking: *\"Best phone under ₹20000\"* or *\"Show me Nike shoes\"* 😊"
)


def is_blocked(query: str) -> bool:
    q = query.lower()
    for topic in BLOCKED_TOPICS:
        if topic in q:
            if not any(s in q for s in SHOPPING_SIGNALS):
                return True
    return False


AGENT_PROMPT = PromptTemplate.from_template("""You are ShopBot — a STRICT, professional AI shopping assistant for an Indian online store.

🚨 ABSOLUTE RULES:
1. ONLY answer shopping queries: products, prices, brands, reviews, recommendations, policies, delivery, returns.
2. If anything non-shopping → refuse and redirect to shopping topics.
3. NEVER fabricate product data — use tools to fetch real data.
4. Always show prices in ₹ (Indian Rupees).
5. When user doesn't know which brand to pick → use brand_advisor_tool.
6. Always generate real e-commerce links via ecommerce_links_tool.
7. For reviews/ratings → use review_fetcher_tool.
8. Format responses clearly with emojis. Be professional and concise.

Available tools:
{tools}

Format STRICTLY:
Question: the question
Thought: step by step thinking
Action: one of [{tool_names}]
Action Input: input
Observation: result
... (repeat up to 4 times)
Thought: I now know the final answer
Final Answer: well-formatted answer with all details

Previous conversation:
{chat_history}

Question: {input}
Thought:{agent_scratchpad}""")


class ShoppingAgent:
    def __init__(self, llm, memory):
        self.llm    = llm
        self.memory = memory
        self.tools  = [
            product_search_tool,
            policy_search_tool,
            brand_advisor_tool,
            ecommerce_links_tool,
            review_fetcher_tool,
        ]

    def invoke(self, query: str) -> dict:
        if is_blocked(query):
            return {"output": BLOCK_RESPONSE}

        try:
            agent = create_react_agent(self.llm, self.tools, AGENT_PROMPT)

            messages = self.memory.chat_memory.messages
            history  = ""
            for msg in messages[-6:]:
                role     = "Customer" if msg.type == "human" else "ShopBot"
                history += f"{role}: {msg.content}\n"

            executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=False,
                max_iterations=25, max_execution_time=60,
                handle_parsing_errors=True
            )
            result = executor.invoke({"input": query, "chat_history": history})
            return result

        except Exception as e:
            return {"output": f"⚠️ I ran into an issue. Could you rephrase? *(Error: {str(e)})*"}
