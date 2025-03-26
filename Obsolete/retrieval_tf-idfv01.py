# retrieval.py
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

wikipedia.set_lang("cs")

# Pomocná funkce: získání článku
def get_wikipedia_article(topic):
    try:
        page = wikipedia.page(topic)
        return page.content
    except:
        return ""

# Základní heuristika: pokud podobnost přesáhne práh, považujeme to za shodu
THRESHOLD = 0.3

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
    corpus = [tvrzeni] + sentences
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()

    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
    best_score = max(cosine_similarities)
    best_index = cosine_similarities.argmax()
    best_sentence = sentences[best_index]

    if best_score > THRESHOLD:
        if any(neg in best_sentence.lower() for neg in ["není", "nepravda", "špatně"]):
            return "❌ Nepravda", best_sentence
        else:
            return "✅ Pravda", best_sentence
    else:
        return "⚠️ Nejisté", best_sentence
