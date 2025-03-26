# check_fact_rug.py
from openai import OpenAI
import requests
import json

def check_fact_rug(tvrzeni, model, openai_key, groq_key, kontext_vety):
    context_text = "\n- " + "\n- ".join(kontext_vety)

    prompt = f"""
Zhodnoť pravdivost následujícího tvrzení na základě poskytnutých informací z webu.

Tvrzení: {tvrzeni}

Informace nalezené online:
{context_text}

Odpověz tímto formátem:
Verdikt: <PRAVDA / NEPRAVDA / NEJISTÉ>
Komentář: <stručné vysvětlení>
"""

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
        return "Chyba: Neznámý model", "", ""

    verdict_line = next((line for line in answer.split("\n") if "Verdikt:" in line), "")
    comment_line = next((line for line in answer.split("\n") if "Komentář:" in line), "")
    verdict = verdict_line.replace("Verdikt:", "").strip()
    comment = comment_line.replace("Komentář:", "").strip()
    return verdict, comment, "N/A"
