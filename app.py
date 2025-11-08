
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "dati.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(STATIC_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def carica_dati():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"bambini": [], "eventi": [], "classi": [], "personale": []}

def salva_dati(dati):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)

def gestisci_messaggio(msg):
    import random
    m = (msg or "").strip()
    msg_lower = m.lower()
    dati = carica_dati()

    # Bambini
    if "bambini" in msg_lower:
        n = len(dati.get("bambini", []))
        if n == 0:
            return "Non ho ancora registrato i bambini. Vuoi dirmi quanti sono?"
        return f"Ci sono {n} bambini alla Little Star 🌟"

    # Classi
    if "classe" in msg_lower or "classi" in msg_lower:
        classi = dati.get("classi", [])
        if not classi:
            return "Non ho ancora informazioni sulle classi. Vuoi che le registri?"
        nomi = ", ".join([c.get("nome","(senza nome)") for c in classi])
        return f"Le classi registrate sono: {nomi}"

    # Personale
    if "insegnante" in msg_lower or "maestra" in msg_lower or "maestre" in msg_lower:
        personale = dati.get("personale", [])
        if not personale:
            return "Non ho ancora insegnanti registrate. Vuoi aggiungerle?"
        return "Le insegnanti sono: " + ", ".join([p.get("nome","(senza nome)") for p in personale]) + "."

    # Temi educativi/psicologici
    temi_educativi = ["gioco", "alimentazione", "psicologia", "educazione", "lettura", "pedagogia", "sonno", "nanna"]
    if any(t in msg_lower for t in temi_educativi):
        return random.choice([
            "Il gioco libero è fondamentale per sviluppare la creatività nei bambini 🎨",
            "Una buona alimentazione aiuta concentrazione e crescita sana 🍎",
            "Ogni bambino impara con i propri tempi: la pazienza è la chiave 🕊️",
            "Le storie prima di dormire stimolano linguaggio e immaginazione 📖",
            "L’affetto e la sicurezza emotiva sono le basi di ogni apprendimento 💖"
        ])

    # Apprendimento progressivo: se messaggio contiene informazione strutturata semplice tipo "La classe X è per Y"
    # Esempio: "La classe delle Api è dei piccoli"
    if "classe" in msg_lower and "è" in msg_lower:
        # prova a estrarre "classe <nome>"
        # Semplice euristica:
        parts = m.split("classe", 1)[-1].strip()
        # memorizza come nota libero
        note = {"nota": m}
        dati.setdefault("note", []).append(note)
        salva_dati(dati)
        return "Perfetto! Ho memorizzato questa informazione sulla classe 🐝."

    return "Non conosco ancora questa informazione. Vuoi dirmela così la memorizzo?"

@app.route("/")
def index():
    d = carica_dati()
    return render_template("index.html",
                           bambini=d.get("bambini", []),
                           eventi=d.get("eventi", []),
                           classi=d.get("classi", []),
                           personale=d.get("personale", []))

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    return redirect(url_for("index"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = (data.get("message") or "").strip()
    risposta = gestisci_messaggio(msg)
    return jsonify({"reply": risposta})

# Static route for manifest or icons if needed
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
