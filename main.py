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
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ Errore nel caricamento dati:", e)
        return {"bambini": [], "eventi": []}

def salva_dati(dati):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("⚠️ Errore nel salvataggio dati:", e)

# -------------------- ROTTE PRINCIPALI -------------------- #
@app.route("/")
def index():
    dati = carica_dati()
    return render_template(
        "index.html",
        bambini=dati.get("bambini", []),
        eventi=dati.get("eventi", [])
    )

@app.route("/api/dati")
def api_dati():
    dati = carica_dati()
    return jsonify(dati)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
    return redirect(url_for('index'))

# -------------------- ROTTA CHAT CON ANGELICA -------------------- #
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = (data.get("message") or "").strip()
    try:
        risposta = angelica_risponde(msg)
    except Exception as e:
        print("❌ Errore in angelica_risponde:", e)
        risposta = "Mi dispiace, ma non riesco a rispondere ora 💫"
    print(f"💬 Messaggio ricevuto: {msg[:80]}... → Risposta: {risposta[:80]}...")
    return jsonify({"reply": risposta})

# 🔹 Rotta di test per verificare che Render risponde
@app.route("/ping")
def ping():
    return "✅ Little Star Web è online su Render!"

# -------------------- AVVIO SERVER PER RENDER -------------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Server Flask avviato su porta {port} — Little Star Web attivo 🌟")
    app.run(host="0.0.0.0", port=port, debug=False)
