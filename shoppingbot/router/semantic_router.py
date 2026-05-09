import numpy as np
from shoppingbot.config import EMBEDDINGS

PRODUCT_SAMPLE = [
    "how much does this phone cost", "what colors are available for this shirt",
    "is this item in stock", "what products do you have in your store",
    "can you show me some shoes", "do you have any discounts",
    "what's the warranty on this", "are there any new arrivals this week",
    "do you offer free shipping", "can I return this if it doesn't fit",
    "what's your best-selling item", "what's the material of this",
    "can you recommend a good laptop", "show me phones under 20000",
    "I want to buy a t-shirt", "do you have Nike shoes",
    "I need headphones for music", "what watches do you have",
    "recommend something for my budget of 5000", "any offer on electronics",
    "what is the price of samsung galaxy", "do you have jeans in size 32",
    "what brands do you carry", "is cash on delivery available",
    "how long does delivery take", "show me reviews for sony headphones",
    "which brand is better for laptops", "what are pros and cons of iphone",
    "help me choose between samsung and apple", "is this product worth buying",
    "I don't know which brand to pick", "best budget smartphone",
    "compare nike and adidas shoes", "rate this product",
]

CHITCHAT_SAMPLE = [
    "do you like watching movies", "what's your favorite food",
    "how are you doing", "tell me a joke", "what's your favorite book",
    "what's the meaning of life", "good morning", "hello", "hi there",
    "thanks for your help", "you're so helpful", "bye", "see you later",
    "who are you", "what can you do", "are you a robot", "how was your day",
]

OFF_TOPIC_SAMPLE = [
    "what is java programming", "explain machine learning algorithm",
    "write a python function", "what is the capital of france",
    "explain photosynthesis", "solve this math problem", "history of world war 2",
    "what is quantum physics", "how does blockchain work technically",
    "write me an essay", "translate this sentence", "debug my code",
    "what is recursion", "explain data structures", "cricket match score",
    "what is the stock price of reliance", "give me a recipe for biryani",
    "what is the weather today", "who won the election", "medical symptoms",
]

PRODUCT_ROUTE_NAME   = 'products'
CHITCHAT_ROUTE_NAME  = 'chitchat'
OFFTOPIC_ROUTE_NAME  = 'offtopic'

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

class SemanticRouter:
    def __init__(self):
        print("  ⚙️  Building semantic router (3 routes: products / chitchat / off-topic)...")
        self.embedding          = EMBEDDINGS
        self.product_embeddings  = [self.embedding.embed_query(p) for p in PRODUCT_SAMPLE]
        self.chitchat_embeddings = [self.embedding.embed_query(p) for p in CHITCHAT_SAMPLE]
        self.offtopic_embeddings = [self.embedding.embed_query(p) for p in OFF_TOPIC_SAMPLE]
        print("  ✅  Semantic router ready!")

    def guide(self, query: str) -> str:
        q_emb        = self.embedding.embed_query(query)
        score_prod   = max(cosine_similarity(q_emb, e) for e in self.product_embeddings)
        score_chat   = max(cosine_similarity(q_emb, e) for e in self.chitchat_embeddings)
        score_off    = max(cosine_similarity(q_emb, e) for e in self.offtopic_embeddings)

        best = max(score_prod, score_chat, score_off)
        if best == score_off and score_off > 0.55:
            return OFFTOPIC_ROUTE_NAME
        elif score_prod >= score_chat:
            return PRODUCT_ROUTE_NAME
        else:
            return CHITCHAT_ROUTE_NAME
