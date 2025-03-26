# app.py
import streamlit as st
from retrieval import check_fact_retrieval, get_wikipedia_article
from llm_checker import check_fact_llm
from utils import measure_latency, calculate_relevance
import time

st.set_page_config(page_title="Fakt-checker", layout="centered")
st.title("🔍 Ověřovač faktů (Fakt-checker)")

# API klice
openai_api_key = st.secrets.get("OPENAI_API_KEY")
groq_api_key = st.secrets.get("GROQ_API_KEY")

# Zadani tvrzeni
tvrzeni = st.text_input("Zadejte tvrzení, které chcete ověřit:")

# Vyber metody
metoda = st.radio("Vyberte metodu ověření:", ["Klasický retrieval", "LLM - OpenAI GPT", "LLM - LLaMA (Groq)"])

# Inicializace session stavu pro fallback
if "fallback_word" not in st.session_state:
    st.session_state.fallback_word = ""

# Tlacitko pro spusteni
if st.button("Ověřit fakt") and tvrzeni:
    st.write("---")
    st.subheader("📄 Tvrzení:")
    st.write(tvrzeni)

    if metoda == "Klasický retrieval":
        with st.spinner("Analyzuji pomocí klasického retrievalu..."):
            start = time.time()
            verdict, source = check_fact_retrieval(tvrzeni)
            latency = measure_latency(start)

        if "článek nenalezen" in verdict.lower():
            st.warning("Nepodařilo se automaticky najít relevantní článek na Wikipedii.")
            fallback = st.text_input("Zadejte vlastní klíčové slovo pro hledání ve Wikipedii:", key="fallback")
            if fallback:
                obsah = get_wikipedia_article(fallback)
                if obsah:
                    st.info(f"Nalezen článek pro '{fallback}'. Zkouším ověřit fakt...")
                    start = time.time()
                    verdict, source = check_fact_retrieval(f"{tvrzeni} {fallback}")
                    latency = measure_latency(start)
                else:
                    st.error("Ani ručně zadané slovo nevedlo k nalezení článku.")

        st.success(f"Verdikt: {verdict}")
        st.caption(f"Zdroj: {source}")
        st.caption(f"Latence: {latency:.2f} sekundy")

    else:
        model = "openai" if metoda == "LLM - OpenAI GPT" else "groq"
        with st.spinner(f"Dotazuji model {model.upper()}..."):
            start = time.time()
            verdict, answer, confidence = check_fact_llm(tvrzeni, model, openai_api_key, groq_api_key)
            latency = measure_latency(start)
            relevance = calculate_relevance(tvrzeni, answer)

        st.success(f"Verdikt: {verdict}")
        st.caption(f"Odpověď modelu: {answer}")
        st.caption(f"Latence: {latency:.2f} s")
        st.caption(f"Důležitost odpovědi (relevance): {relevance:.2f}")
        st.caption(f"Odhad jistoty: {confidence}")
