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

def check_fact_retrieval(tvrzeni):
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
        return "Nelze ověřit (článek nenalezen)", "Žádný zdroj"

    sentences = obsah.split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    embeddings = model.encode([tvrzeni] + sentences, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings[0], embeddings[1:])[0]

    best_score = torch.max(cosine_scores).item()
    best_index = torch.argmax(cosine_scores).item()
    best_sentence = sentences[best_index]

    if best_score > 0.5:
        if any(neg in best_sentence.lower() for neg in ["není", "nepravda", "špatně"]):
            return "❌ Nepravda", best_sentence
        else:
            return "✅ Pravda", best_sentence
    else:
        return "⚠️ Nejisté", best_sentence
