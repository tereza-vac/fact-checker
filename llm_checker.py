# llm_checker.py
from openai import OpenAI
import requests
import json

def check_fact_llm(tvrzeni, model, openai_key, groq_key):
    if model == "openai":
        prompt = f"""
Zkontroluj následující tvrzení a vyhodnoť ho jako PRAVDA / NEPRAVDA / NEJISTÉ. Poté připoj krátké vysvětlení.

Tvrzení: {tvrzeni}

Odpověz přesně tímto formátem:
Verdikt: <PRAVDA / NEPRAVDA / NEJISTÉ>
Komentář: <stručné vysvětlení>
"""
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        verdict_line = next((line for line in answer.split("\n") if "Verdikt:" in line), "")
        comment_line = next((line for line in answer.split("\n") if "Komentář:" in line), "")
        verdict = verdict_line.replace("Verdikt:", "").strip()
        comment = comment_line.replace("Komentář:", "").strip()
        return verdict, comment, "N/A"

    elif model == "groq":
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": f"Zkontroluj následující tvrzení a vyhodnoť ho jako PRAVDA / NEPRAVDA / NEJISTÉ. Připoj i stručné vysvětlení.\n\nTvrzení: {tvrzeni}\n\nOdpověz přesně tímto formátem:\nVerdikt: <PRAVDA / NEPRAVDA / NEJISTÉ>\nKomentář: <stručné vysvětlení>"}],
            "temperature": 0.3
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(data))
        answer = r.json()["choices"][0]["message"]["content"]

        verdict_line = next((line for line in answer.split("\n") if "Verdikt:" in line), "")
        comment_line = next((line for line in answer.split("\n") if "Komentář:" in line), "")
        verdict = verdict_line.replace("Verdikt:", "").strip()
        comment = comment_line.replace("Komentář:", "").strip()
        return verdict, comment, "N/A"

    else:
        return "Chyba: neznámý model", "", ""
