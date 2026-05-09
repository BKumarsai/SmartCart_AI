import sqlite3
from typing import Union, List, Dict
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from shoppingbot.config import GROQ_API_KEY, DATA_PRODUCT_PATH

SQL_PROMPT = PromptTemplate(
    template="""You are an SQL expert. Generate a SQLite query for the products table.

Table 'products' columns:
- product_code (TEXT) - unique ID
- product_name (TEXT) - name of the product
- category (TEXT) - category like Electronics, Clothing, Footwear, etc.
- material (TEXT) - material/specs
- size (TEXT) - available sizes
- color (TEXT) - available colors
- brand (TEXT) - brand name
- gender (TEXT) - male/female/unisex
- stock_quantity (INTEGER) - qty in stock
- price (REAL) - price in Indian Rupees

Rules:
- Use LIKE for text searches (case-insensitive)
- Use LOWER() for case-insensitive matching
- Only return products WHERE stock_quantity > 0 unless asked otherwise
- Limit results to 5 unless asking for all
- Output ONLY the SQL query, nothing else, no markdown, no explanation

Question: {input}
SQL:""",
    input_variables=["input"]
)

class ProductDB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def execute(self, query: str) -> List[Dict]:
        query = query.replace('```sql', '').replace('```', '').strip()
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            conn.close()

def format_products(products: List[Dict]) -> str:
    if not products:
        return "No products found matching your criteria."
    result = f"Found {len(products)} product(s):\n\n"
    for p in products:
        result += f"🏷️ **{p.get('product_name', 'N/A')}**\n"
        result += f"   Brand: {p.get('brand', 'N/A')} | Price: ₹{p.get('price', 'N/A')}\n"
        result += f"   Category: {p.get('category', 'N/A')} | Colors: {p.get('color', 'N/A')}\n"
        result += f"   Sizes: {p.get('size', 'N/A')} | Stock: {p.get('stock_quantity', 0)} units\n\n"
    return result

@tool
def product_search_tool(input: str) -> str:
    """
    Search for products in the store database. Use this when a customer asks about
    products, prices, availability, colors, sizes, brands, or wants recommendations.
    Input should be the customer's product query in plain English.
    """
    try:
        llm = ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",
            groq_api_key=GROQ_API_KEY
        )
        db = ProductDB(DATA_PRODUCT_PATH)

        chain = (
            {"input": RunnablePassthrough()}
            | SQL_PROMPT
            | llm
            | (lambda x: db.execute(x.content))
            | format_products
        )
        return chain.invoke(input)
    except Exception as e:
        return f"Error searching products: {str(e)}"
