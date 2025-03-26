# app.py
import streamlit as st
from retrieval import retrieve_relevant_sentences
from duckduck_retrieval import duckduckgo_search
from llm_checker import check_fact_llm
from check_fact_rug import check_fact_rug
from utils import measure_latency, calculate_relevance
import time

st.set_page_config(page_title="Fakt-checker", layout="centered")
st.title("🔍 Ověřovač faktů")

# API klice
openai_api_key = st.secrets.get("OPENAI_API_KEY")
groq_api_key = st.secrets.get("GROQ_API_KEY")

# Zadani tvrzeni
tvrzeni = st.text_input("Zadejte tvrzení, které chcete ověřit:")

# Vyber metody
metoda = st.radio(
    "Vyberte metodu ověření:",
    ["Klasický retrieval", "LLM - OpenAI GPT", "LLM - LLaMA (Groq)", "LLM + Web (RUG)"]
)

if st.button("Ověřit fakt") and tvrzeni:
    st.write("---")
    st.subheader("📄 Tvrzení:")
    st.write(tvrzeni)

    if metoda == "Klasický retrieval":
        with st.spinner("Vyhledávám relevantní informace ze zdrojů..."):
            start = time.time()
            tema, relevant_sentences = retrieve_relevant_sentences(tvrzeni)
            latency = measure_latency(start)

        if isinstance(relevant_sentences, str):
            st.warning("Nepodařilo se najít článek na Wikipedii.")
        else:
            st.subheader("💬 Nalezené informace k tvrzení:")
            for i, (sentence, score) in enumerate(relevant_sentences):
                st.markdown(f"**{i+1}.** *{sentence}*  ")
                st.caption(f"Relevance skóre: {score}")

        st.caption(f"Latence: {latency:.2f} sekundy")

    elif metoda == "LLM + Web (RUG)":
        model = "openai" if st.radio("Model:", ["OpenAI GPT", "LLaMA (Groq)"]) == "OpenAI GPT" else "groq"
        with st.spinner("Získávám aktuální informace z webu..."):
            start = time.time()
            kontext = duckduckgo_search(tvrzeni)
            verdict, comment, confidence = check_fact_rug(tvrzeni, model, openai_api_key, groq_api_key, kontext)
            latency = measure_latency(start)
            relevance = calculate_relevance(tvrzeni, comment)

        st.subheader("🌐 Kontext z webu:")
        for i, k in enumerate(kontext):
            st.markdown(f"**{i+1}.** {k}")

        st.success(f"Verdikt: {verdict}")
        st.markdown(f"**Komentář:** {comment}")
        st.caption(f"Latence: {latency:.2f} s")
        st.caption(f"Relevance komentáře: {relevance:.2f}")

    else:
        model = "openai" if metoda == "LLM - OpenAI GPT" else "groq"
        with st.spinner(f"Dotazuji model {model.upper()}..."):
            start = time.time()
            verdict, comment, confidence = check_fact_llm(tvrzeni, model, openai_api_key, groq_api_key)
            latency = measure_latency(start)
            relevance = calculate_relevance(tvrzeni, comment)

        st.success(f"Verdikt: {verdict}")
        st.markdown(f"**Komentář:** {comment}")
        st.caption(f"Latence: {latency:.2f} s")
        st.caption(f"Důležitost odpovědi (relevance): {relevance:.2f}")
        st.caption(f"Odhad jistoty: {confidence}")
