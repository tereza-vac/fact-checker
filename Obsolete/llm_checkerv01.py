
from openai import OpenAI
import requests
import json

def check_fact_llm(tvrzeni, model, openai_key, groq_key):
    prompt = f"Zkontroluj prosím pravdivost následujícího tvrzení a odpověz PRAVDA / NEPRAVDA / NEJSEM SI JISTÝ.\nTvrzení: {tvrzeni}"

    if model == "openai":
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        answer = response.choices[0].message.content

    elif model == "groq":
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(data))
        answer = r.json()["choices"][0]["message"]["content"]

    else:
        return "Chyba: neznámý model", "", 0

    verdict = "⚠️ Nejisté"
    confidence = "N/A"

    if "pravda" in answer.lower():
        if "nepravda" in answer.lower() or "není pravda" in answer.lower():
            verdict = "❌ Nepravda"
        else:
            verdict = "✅ Pravda"
    elif "nejsem si jistý" in answer.lower() or "nelze určit" in answer.lower():
        verdict = "⚠️ Nejisté"

    return verdict, answer.strip(), confidence
