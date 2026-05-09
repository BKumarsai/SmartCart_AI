# 🛍️ ShoppingBot — Groq Edition

> Full LangChain agent shopping bot — now powered by **Groq** (free & ultra-fast) instead of Google Gemini.

---

## ✅ What changed from the original

| Component | Original | Groq Edition |
|-----------|----------|--------------|
| LLM | `ChatGoogleGenerativeAI` (Gemini 1.5 Flash) | `ChatGroq` (LLaMA 3 70B) |
| Embeddings | `GoogleGenerativeAIEmbeddings` | `HuggingFaceEmbeddings` (local, free) |
| API Key needed | Google API Key | Groq API Key |
| SQL generation | Gemini | Groq LLaMA 3 |
| FAISS / SQLite | ✅ unchanged | ✅ unchanged |
| Semantic router | ✅ unchanged | ✅ unchanged |
| Frontend | ✅ unchanged | ✅ unchanged |

---

## 🚀 Setup (4 steps)

### Step 1 — Get your FREE Groq API key
Go to → https://console.groq.com → Sign up → API Keys → Create Key

### Step 2 — Add your key to `.env`
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ First run downloads ~90MB HuggingFace model for embeddings (cached after that)

### Step 4 — Initialize the product database (run ONCE)
```bash
python init_db.py
```

### Step 5 — Run the bot
```bash
python app.py
```
Open → http://localhost:5000

---

## 🔄 Switch Groq Models

In `app.py`, change `model_name`:

| Model | Speed | Context |
|-------|-------|---------|
| `llama3-70b-8192` | Fast | 8K (default) |
| `mixtral-8x7b-32768` | Fast | 32K — better for long conversations |
| `gemma2-9b-it` | Fastest | 8K — lightest option |

---

## 📁 Project Structure

```
shopbot-groq/
├── app.py                        # Flask app + Groq LLM setup
├── init_db.py                    # Run once to create products DB
├── requirements.txt
├── .env                          # Your GROQ_API_KEY goes here
├── data/
│   ├── products.db               # Created by init_db.py
│   ├── policy.txt                # Store policies
│   └── faiss_store/              # Created automatically on first run
├── templates/
│   └── index.html                # Chat UI
└── shoppingbot/
    ├── config.py                 # Groq key + HuggingFace embeddings
    ├── chain.py                  # Chitchat chain
    ├── agent.py                  # ReAct shopping agent
    ├── router/
    │   └── semantic_router.py    # Routes: shopping vs chitchat
    └── tools/
        ├── product_search.py     # SQL tool — queries products.db
        └── policy_search.py      # FAISS tool — queries policy.txt
```

---

## 💡 Example Queries
- "Show me phones under ₹25000"
- "Do you have Nike shoes in size 9?"
- "What's your return policy?"
- "Recommend a laptop for college under ₹50000"
- "What colors is the Sony headphone available in?"
- "Tell me a joke" ← chitchat route
- "Hello, who are you?" ← chitchat route
