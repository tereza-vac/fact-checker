
import streamlit as st
from retrieval import check_fact_retrieval
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
