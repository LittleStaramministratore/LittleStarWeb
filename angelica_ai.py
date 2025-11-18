from openai import OpenAI

client = OpenAI()


def genera_risposta(testo: str) -> str:
    """
    Genera la risposta testuale di Angelica usando OpenAI.
    Ritorna una semplice stringa.
    """
    # Qui puoi dare il carattere ad Angelica
    system_prompt = (
        "Sei Angelica, l'assistente virtuale della Little Star International School. "
        "Parli in modo gentile, chiaro e adatto a genitori e bambini. "
        "Rispondi sempre in italiano."
    )

    risposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": testo},
        ]
    )

    # Nella libreria openai 2.x il contenuto è in .choices[0].message.content
    return risposta.choices[0].message.content
