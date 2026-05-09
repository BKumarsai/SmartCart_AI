from langchain.tools import tool
from langchain_groq import ChatGroq
from shoppingbot.config import GROQ_API_KEY

REVIEW_PROMPT = """You are a product review expert for the Indian market.
Give a detailed, honest product review summary based on real-world user feedback patterns.

Format your response EXACTLY like this:

⭐ **Overall Rating: X.X/5** (based on aggregated user reviews)

📊 **Rating Breakdown:**
| Aspect        | Score  |
|---------------|--------|
| Build Quality | ⭐⭐⭐⭐☆ |
| Performance   | ⭐⭐⭐⭐⭐ |
| Value for ₹  | ⭐⭐⭐⭐☆ |
| After-sales   | ⭐⭐⭐☆☆ |

✅ **What Users Love:**
• Point 1
• Point 2  
• Point 3

❌ **Common Complaints:**
• Point 1
• Point 2

💡 **ShopBot Verdict:** One sentence honest verdict for Indian buyers.

🏷️ **Best For:** Type of user this suits most
💰 **Value:** Worth the price? (Yes/No/Only on sale)

Product: {product}
"""

@tool
def review_fetcher_tool(product_name: str) -> str:
    """
    Get detailed product reviews, ratings, pros and cons for any product.
    Use this when a customer asks about reviews, ratings, is it worth buying,
    what do users think, pros and cons, or before-buy advice.
    Input: product name (e.g., "Sony WH-1000XM5 headphones" or "iPhone 15")
    """
    try:
        llm = ChatGroq(
            temperature=0.3,
            model_name="llama3-70b-8192",
            groq_api_key=GROQ_API_KEY
        )
        prompt   = REVIEW_PROMPT.format(product=product_name)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error fetching reviews: {str(e)}"
