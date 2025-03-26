# retrieval.py
import wikipedia
from sentence_transformers import SentenceTransformer, util
import torch
from itertools import combinations

wikipedia.set_lang("cs")
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

# Pomocná funkce: získání článku
def get_wikipedia_article(topic):
    try:
        page = wikipedia.page(topic)
        return page.content
    except:
        return ""

def retrieve_relevant_sentences(tvrzeni, top_k=5):
    slova = [slovo.strip(".,") for slovo in tvrzeni.split() if len(slovo) > 2]
    tema = None
    obsah = ""

    # Zkusíme 2slovné kombinace
    for dvojice in combinations(slova, 2):
        spojeni = " ".join(dvojice).capitalize()
        obsah = get_wikipedia_article(spojeni)
        if obsah:
            tema = spojeni
            break

    # Pokud selže, zkusíme jednotlivá slova
    if not obsah:
        for slovo in slova:
            tema_kandidat = slovo.capitalize()
            obsah = get_wikipedia_article(tema_kandidat)
            if obsah:
                tema = tema_kandidat
                break

    if not obsah:
        return "Žádný článek nenalezen.", []

    sentences = obsah.split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    embeddings = model.encode([tvrzeni] + sentences, convert_to_tensor=True)
    query_embedding = embeddings[0]
    sentence_embeddings = embeddings[1:]

    cosine_scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(top_k, len(sentences)))

    relevant_sentences = []
    for score, idx in zip(top_results.values, top_results.indices):
        relevant_sentences.append((sentences[idx], round(score.item(), 2)))

    return tema, relevant_sentences