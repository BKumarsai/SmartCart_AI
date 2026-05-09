from langchain.tools import tool
from langchain_groq import ChatGroq
from shoppingbot.config import GROQ_API_KEY

BRAND_GUIDE_PROMPT = """You are a brand expert for Indian e-commerce.
A customer doesn't know which brand to choose for a product category.
Give a concise, honest brand guide in this format:

**Top Brands for [Category]**

| Brand | Best For | Price Range | Trust Score |
|-------|----------|-------------|-------------|
| ...   | ...      | ...         | ⭐⭐⭐⭐⭐   |

Then add 2-3 lines: "**Our Recommendation:**" based on their needs/budget.
Keep it practical, India-focused, and under 200 words.

Customer query: {query}
"""

@tool
def brand_advisor_tool(query: str) -> str:
    """
    Use this when a customer doesn't know which brand to choose, asks 'which brand is best',
    or needs brand guidance for a product category. Provides a comparison table of top Indian
    market brands with trust scores, price ranges, and a personalized recommendation.
    Input: customer's query about brand selection.
    """
    try:
        llm = ChatGroq(
            temperature=0.4,
            model_name="llama3-70b-8192",
            groq_api_key=GROQ_API_KEY
        )
        prompt = BRAND_GUIDE_PROMPT.format(query=query)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error getting brand advice: {str(e)}"
