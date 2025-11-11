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

if api_key:
    print("🔑 API Key trovata:", api_key[:10] + "...")
else:
    print("❌ Nessuna API Key trovata! Controlla setx o file .env")

# Messaggi di log d’avvio su Render
print("🚀 Avvio di Angelica su Render...")
print("📡 Controllo connessione e caricamento moduli completato.")
print("✨ Angelica pronta a conversare con l’universo!")

client = OpenAI(api_key=api_key)

# -------------------- FUNZIONI UTILI -------------------- #
def _load_json(path, default):
    """Carica un file JSON o restituisce un valore di default."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Errore caricando {path}: {e}")
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
def angelica_risponde(testo_utente):
    """Gestisce la risposta intelligente di Angelica."""
    if not testo_utente:
        return "Dimmi qualcosa 💫"

    memoria["chat"].append({"utente": testo_utente, "timestamp": datetime.now().isofo_
