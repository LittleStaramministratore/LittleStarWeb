import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# -------------------- CARICA VARIABILI .ENV -------------------- #
load_dotenv()

# -------------------- PERCORSI BASE -------------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "dati.json")
KNOW_FILE = os.path.join(BASE_DIR, "little_star_knowledge.json")
MEM_FILE = os.path.join(BASE_DIR, "memoria.json")

# -------------------- CLIENT OPENAI -------------------- #
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Nessuna API Key trovata! Controlla le variabili Render.")
else:
    print("🔑 API Key trovata:", api_key[:10] + "...")

client = OpenAI(api_key=api_key)

print("🚀 Avvio di Angelica su Render completato.")
print("✨ Angelica pronta a conversare con l’universo!")

# -------------------- FUNZIONI DI SUPPORTO -------------------- #
def _load_json(path, default):
    """Carica un file JSON o restituisce un valore di default."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path, data):
    """Salva un file JSON."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Errore salvando {path}: {e}")

# -------------------- DATI DI CONOSCENZA -------------------- #
knowledge = _load_json(KNOW_FILE, {})
memoria = _load_json(MEM_FILE, {"chat": []})

# -------------------- FUNZIONE PRINCIPALE -------------------- #
def ask_angelica(testo_utente: str) -> str:
    """Elabora la risposta intelligente di Angelica."""
    if not testo_utente.strip():
        return "Dimmi qualcosa 💫"

    memoria["chat"].append({
        "utente": testo_utente,
        "timestamp": datetime.now().isoformat()
    })

    try:
        system_prompt = (
            "Tu sei Angelica, un'assistente AI gentile, empatica e preparata. "
            "Esperta in educazione Montessori, psicologia infantile e comunicazione affettiva. "
            "Rispondi sempre nella lingua dell’utente, con tono dolce, umano e rassicurante."
        )

        know_text = json.dumps(knowledge, ensure_ascii=False)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Conoscenza base: {know_text}"},
            {"role": "user", "content": testo_utente}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400
        )

        reply = response.choices[0].message.content.strip()

        memoria["chat"].append({
            "angelica": reply,
            "timestamp": datetime.now().isoformat()
        })
        _save_json(MEM_FILE, memoria)

        return reply

    except Exception as e:
        print(f"❌ Errore Angelica: {e}")
        return "Ops, c’è stato un problema con la connessione 🌙"
