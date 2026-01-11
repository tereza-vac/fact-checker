# Fact Checker — Streamlit App

This app demonstrates several approaches to fact-checking statements:

1. **Classic retrieval** (Wikipedia + TF-IDF / embeddings)  
2. **LLM models** (GPT-4 via OpenAI, LLaMA3 via Groq API)  
3. **RAG** (Retrieval using DuckDuckGo + LLM evaluation)

The app is built with Streamlit and is designed for educational and demonstration purposes, easy testing, and potential extensibility.

---

## Installation & Run

1. **Create a virtual environment (optional):**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
streamlit run app.py
```

---

##API Keys

Add your keys to `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
GROQ_API_KEY = "gsk_..."
```

---

## Project Structure

```text
├── app.py                        # Main UI of the app
├── retrieval.py                 # Wikipedia retrieval logic
├── llm_checker.py               # GPT / LLaMA evaluation without context
├── duckduck_retrieval.py       # DuckDuckGo scraping (RAG)
├── check_fact_rug.py           # LLM evaluation with web context
├── utils.py                     # Latency, relevance scoring, helpers
├── requirements.txt             # List of dependencies
└── .streamlit/secrets.toml      # Local API key config
```

---

## Available Modes

### 1. Classic Retrieval
- Retrieves a Wikipedia article
- Uses embeddings (sentence-transformers) to extract the most relevant sentences
- Displays them to the user

### 2. LLM (GPT or LLaMA)
- Evaluates the statement based solely on internal model knowledge
- Returns: verdict + brief explanation

### 3. LLM + Web (RAG)
- Uses DuckDuckGo to gather current web information
- LLM makes a decision based on these snippets

---

## Metrics

Each result includes:
- Latency
- Relevance score (embedding similarity)
- Estimated answer length and confidence

---

## Stability & Extensibility

- Advanced features are modularized
- Modes can be easily added or removed
- Tip: maintain a backup `app_base.py` or use `EXPERIMENTAL_MODE`

---

## Notes on Functionality

- LLM results are non-deterministic — outputs may vary across runs
- DuckDuckGo scraping is basic — HTML format may change (watch for updates)
- For RAG, other sources can be used (e.g., Bing, Google News, custom datasets)

