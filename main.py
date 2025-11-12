from flask import Flask, render_template, jsonify, request, redirect, url_for
import os, json
from angelica_ai import angelica_risponde

# -------------------- PERCORSI BASE -------------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "dati.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------- GESTIONE FILE DATI -------------------- #
if not os.access(DATA_FILE, os.W_OK):
    print("⚠️ Il file non è scrivibile. Provo a sistemare i permessi...")
    try:
        os.chmod(DATA_FILE, 0o666)
    except Exception as e:
        print("❌ Errore nel cambiare i permessi:", e)

def carica_dati():
    """Carica i dati dal file JSON principale."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ Errore nel caricamento dati:", e)
        return {"bambini": [], "eventi": []}

def salva_dati(dati):
    """Salva i dati aggiornati nel file JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("⚠️ Errore nel salvataggio dati:", e)

# -------------------- ROTTE PRINCIPALI -------------------- #
@app.route("/")
def index():
    """Pagina principale del sito."""
    dati = carica_dati()
    return render_template(
        "index.html",
        bambini=dati.get("bambini", []),
        eventi=dati.get("eventi", [])
    )

@app.route("/api/dati")
def api_dati():
    """API che restituisce tutti i dati in formato JSON."""
    dati = carica_dati()
    return jsonify(dati)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Gestisce il caricamento dei file ne
