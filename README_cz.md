# 🧠 Ověřovač faktů (Fakt-checker) — Streamlit aplikace

Tato aplikace slouží k demonstraci různých přístupů k ověřování pravdivosti tvrzení:

1. **Klasický retrieval** (Wikipedia + TF-IDF / embeddingy)
2. **LLM modely** (GPT-4 přes OpenAI, LLaMA3 přes Groq API)
3. **RUG / RAG** (Retrieval pomocí DuckDuckGo + vyhodnocení LLM)

Aplikace je psaná ve Streamlit a je navržena pro edukativní demonstrativní účely, snadné testování, i případné rozšiřování.

---

## 🔧 Instalace a spuštění

1. **Vytvoření prostředí (volitelné):**
```bash
python -m venv venv
source venv/bin/activate  # nebo venv\Scripts\activate na Windows
```

2. **Instalace požadavků:**
```bash
pip install -r requirements.txt
```

3. **Spuštění aplikace:**
```bash
streamlit run app.py
```

---

## 🔐 API klíče
Vlož své klíče do `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
GROQ_API_KEY = "gsk_..."
```

---

## 📦 Struktura projektu

```text
├── app.py                        # Hlavní UI aplikace
├── retrieval.py                 # Retrieval z Wikipedie
├── llm_checker.py               # GPT / LLaMA bez kontextu
├── duckduck_retrieval.py       # DuckDuckGo scraping (RUG)
├── check_fact_rug.py           # LLM + web context
├── utils.py                     # Měření latence, relevance
├── requirements.txt             # Seznam balíčků
└── .streamlit/secrets.toml      # API klíče (lokálně)
```

---

## 🎮 Dostupné režimy

### 1. Klasický retrieval
- Vyhledává článek z Wikipedie
- Pomocí embeddingů (sentence-transformers) vybere nejrelevantnější věty
- Zobrazí je uživateli

### 2. LLM (GPT nebo LLaMA)
- Zhodnotí tvrzení pouze na základě interních znalostí
- Vrací: verdikt + stručný komentář

### 3. LLM + Web (RUG)
- Použije DuckDuckGo k získání aktuálních informací z webu
- LLM rozhoduje na základě těchto snippetů

---

## 📊 Metriky
Každý výstup obsahuje:
- Latenci
- Relevance skóre (embeddingová podobnost)
- Odhad délky a jistoty odpovědi

---

## 🛡️ Stabilita a rozšiřitelnost

- Všechny pokročilé funkce jsou v oddělených modulech
- Lze snadno přidat / odebrat jednotlivé režimy
- Dopručení: mít záložní `app_base.py` nebo používat `EXPERIMENTAL_MODE`

---

## Poznámky k funkčnosti:

- Výsledky z LLM nejsou deterministické — při opakování se mohou lišit
- DuckDuckGo scraping je jednoduchý a může se změnit formát HTML (nutné ošetřit)
- Pro RAG lze použít i jiné zdroje než DuckDuckGo (např. Bing, Google News, vlastní data)

---
