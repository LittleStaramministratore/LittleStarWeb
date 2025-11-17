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
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Errore salvando {path}: {e}")

# -------------------- DATI -------------------- #
knowledge = _load_json(KNOW_FILE, {})
memoria = _load_json(MEM_FILE, {"chat": [], "facts": []})

# -------------------- RICONOSCIMENTO "INSEGNAMENTO" -------------------- #
def detect_learning(text):
    """
    Riconosce quando l’utente vuole insegnare qualcosa.
    Frasi come:
    - “impara questo”
    - “devi sapere che”
    - “ricordati che”
    - “da oggi devi sapere”
    - "ti do un'informazione"
    """

    trigger = ["impara", "ricordati", "devi sapere", "da oggi", "informazione", "nota che"]

    t = text.lower()
    return any(k in t for k in trigger)

# -------------------- SALVA NUOVA CONOSCENZA -------------------- #
def save_fact(text):
    """
    Estrae l’informazione e la salva nella memoria permanente.
    """
    memoria["facts"].append({
        "contenuto": text,
        "timestamp": datetime.now().isoformat()
    })
    _save_json(MEM_FILE, memoria)

# -------------------- FUNZIONE PRINCIPALE -------------------- #
def ask_angelica(testo_utente: str) -> str:
    if not testo_utente.strip():
        return "Dimmi qualcosa 💫"

    # Registra la richiesta
    memoria["chat"].append({"utente": testo_utente, "timestamp": datetime.now().isoformat()})

    # 🔥 SE L’UTENTE STA INSEGNANDO QUALCOSA
    if detect_learning(testo_utente):
        save_fact(testo_utente)
        return "Ho imparato questa nuova informazione, grazie per avermela insegnata 🌟"

    # Prepara contesto memoria
    facts_text = "\n".join(f["contenuto"] for f in memoria.get("facts", []))
    knowledge_text = json.dumps(knowledge, ensure_ascii=False)

    try:
        system_prompt = (
            "Tu sei Angelica, un'assistente AI gentile, empatica e preparata. "
            "Esperta in educazione Montessori, psicologia infantile e comunicazione affettiva. "
            "Usa la conoscenza appresa e le informazioni che l’utente ti insegna. "
            "Rispondi in modo affettuoso e umano, con grande empatia."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Conoscenza base: {knowledge_text}"},
            {"role": "system", "content": f"Memoria permanente appresa: {facts_text}"},
            {"role": "user", "content": testo_utente}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400
        )

        reply = response.choices[0].message.content.strip()

        # Salva risposta
        memoria["chat"].append({"angelica": reply, "timestamp": datetime.now().isoformat()})
        _save_json(MEM_FILE, memoria)

        return reply

    except Exception as e:
        print(f"❌ Errore Angelica: {e}")
        return "Ops… Sembra ci sia stato un problema con la rete 💫"
