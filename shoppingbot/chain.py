from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

CHITCHAT_PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template="""You are ShopBot, a friendly AI shopping assistant for an Indian online store.
You are warm, witty, and focused on helping customers shop.
For casual greetings, be friendly and brief. ALWAYS guide the conversation back toward shopping.
NEVER answer off-topic questions (coding, science, history, etc.) — redirect to shopping instead.
If unsure, ask: "Looking for any product today? I can help find the best deals! 🛍️"

Conversation:
{history}

Customer: {input}
ShopBot:"""
)

def create_chitchat_chain(llm, memory):
    return ConversationChain(
        llm=llm,
        memory=memory,
        prompt=CHITCHAT_PROMPT,
        verbose=False
    )
