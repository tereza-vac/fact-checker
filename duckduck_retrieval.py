# duckduck_retrieval.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Funkce pro extrakci snippetů z DuckDuckGo

def duckduckgo_search(tvrzeni, max_results=5):
    query = tvrzeni.replace(" ", "+")
    url = f"https://html.duckduckgo.com/html/?q={query}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        results = []
        for result in soup.find_all("a", class_="result__a"):
            snippet = result.get_text(strip=True)
            if snippet and len(snippet.split()) > 5:
                results.append(snippet)
            if len(results) >= max_results:
                break

        return results
    except Exception as e:
        return [f"Chyba při vyhledávání: {str(e)}"]

# Ukázkové použití (pro testy mimo Streamlit)
if __name__ == "__main__":
    tvrzeni = "Karviná je město na Slovensku"
    vysledky = duckduckgo_search(tvrzeni)
    for i, snippet in enumerate(vysledky, 1):
        print(f"{i}. {snippet}")
