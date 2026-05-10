from langchain.tools import tool
import urllib.parse

PLATFORMS = {
    "amazon":   "https://www.amazon.in/s?k={query}",
    "flipkart": "https://www.flipkart.com/search?q={query}",
    "meesho":   "https://www.meesho.com/search?q={query}",
    "ajio":     "https://www.ajio.com/search/?text={query}",
    "myntra":   "https://www.myntra.com/search?q={query}",
    "snapdeal": "https://www.snapdeal.com/search?keyword={query}",
    "nykaa":    "https://www.nykaa.com/search/result/?q={query}",
    "croma":    "https://www.croma.com/searchB?q={query}",
}

# Category → best platforms to show
CATEGORY_PLATFORMS = {
    "electronics": ["amazon", "flipkart", "croma", "snapdeal"],
    "phone":       ["amazon", "flipkart", "croma"],
    "laptop":      ["amazon", "flipkart", "croma"],
    "headphone":   ["amazon", "flipkart", "meesho"],
    "watch":       ["amazon", "flipkart", "myntra", "ajio"],
    "clothing":    ["myntra", "ajio", "meesho", "amazon", "flipkart"],
    "shoes":       ["myntra", "ajio", "amazon", "flipkart"],
    "footwear":    ["myntra", "ajio", "amazon", "flipkart"],
    "beauty":      ["nykaa", "amazon", "flipkart", "meesho"],
    "skincare":    ["nykaa", "amazon", "flipkart"],
    "furniture":   ["amazon", "flipkart", "snapdeal"],
    "default":     ["amazon", "flipkart", "meesho", "ajio"],
}

def detect_category(product_name: str) -> str:
    p = product_name.lower()
    for cat in CATEGORY_PLATFORMS:
        if cat in p:
            return cat
    if any(w in p for w in ["iphone","samsung","redmi","oneplus","realme","pixel"]):
        return "phone"
    if any(w in p for w in ["hp","dell","lenovo","asus","acer","macbook"]):
        return "laptop"
    if any(w in p for w in ["shirt","jeans","kurta","dress","t-shirt","kurti"]):
        return "clothing"
    if any(w in p for w in ["nike","puma","adidas","bata","sneaker","heel","slipper"]):
        return "shoes"
    if any(w in p for w in ["cream","serum","moisturizer","lipstick","perfume"]):
        return "beauty"
    return "default"

def build_links(product_name: str, brand: str = "") -> dict:
    search_term = f"{brand} {product_name}".strip()
    encoded     = urllib.parse.quote_plus(search_term)
    cat         = detect_category(product_name)
    platforms   = CATEGORY_PLATFORMS.get(cat, CATEGORY_PLATFORMS["default"])

    return {
        platform: PLATFORMS[platform].format(query=encoded)
        for platform in platforms
        if platform in PLATFORMS
    }

def format_links(links: dict) -> str:
    icons = {
        "amazon":   "🛒 Amazon",
        "flipkart": "🔵 Flipkart",
        "meesho":   "🩷 Meesho",
        "ajio":     "🟠 Ajio",
        "myntra":   "🔴 Myntra",
        "snapdeal": "🟡 Snapdeal",
        "nykaa":    "💄 Nykaa",
        "croma":    "🟢 Croma",
    }
    result = "\n🛍️ **Buy Now:**\n"
    for platform, url in links.items():
        label = icons.get(platform, platform.title())
        result += f"• [{label}]({url})\n"
    return result

@tool
def ecommerce_links_tool(product_query: str) -> str:
    """
    Generate real shopping links for Amazon India, Flipkart, Meesho, Ajio, Myntra, Nykaa, Croma etc.
    Automatically picks the best platforms based on product category.
    Input format: "product_name | brand_name" (brand optional).
    Example: "Sony WH-1000XM5 | Sony" or "Nike Air Max 270"
    """
    parts  = product_query.split("|")
    name   = parts[0].strip()
    brand  = parts[1].strip() if len(parts) > 1 else ""
    links  = build_links(name, brand)
    return format_links(links)
