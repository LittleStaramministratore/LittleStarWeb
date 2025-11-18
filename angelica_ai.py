import json
from typing import Dict, Optional
from openai import OpenAI

client = OpenAI()

def genera_risposta(testo: str, knowledge: Optional[Dict] = None) -> str:
    system_prompt = (
        "Sei Angelica, l'assistente virtuale della Little Star International School. "
        "La tua voce è calda e dolce. Parli con gentilezza, amore e professionalità. "
        "Conosci educazione infantile, psicologia, giochi educativi, alimentazione sana, "
        "benessere dei bambini e cultura generale semplice. "
        "Rispondi sempre in italiano, con tono affettuoso ma chiaro."
    )

    messages = [{"role": "system", "content": system_prompt}]

    if knowledge:
        messages.append({
            "role": "system",
            "content": "Dati scuola:\n" + json.dumps(knowledge, ensure_ascii=False)
        })

    messages.append({"role": "user", "content": testo})

    risposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return risposta.choices[0].message.content
