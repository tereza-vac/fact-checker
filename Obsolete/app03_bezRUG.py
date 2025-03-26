# app.py
import streamlit as st
from retrieval import retrieve_relevant_sentences
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
